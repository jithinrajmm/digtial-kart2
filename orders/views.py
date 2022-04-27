
from django.shortcuts import render # this is the first line
from django.http import HttpResponse,JsonResponse
from carts.models import Cart, CartItems, CouponUsedUsers
from accounts.models import Account
from django.shortcuts import redirect
from carts.views import delete_cart
import orders
from orders.context import order_product
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment,RazorPay
from datetime import datetime
from django.urls import reverse
from store.models import Product
from django.views.decorators.csrf import csrf_exempt 

# this is for the paypal data getting 
import json
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseBadRequest
from django.contrib import messages
# this is the coupon model
from carts.models import Coupon
from django.contrib.auth.decorators import login_required

# For the random numbers , paypal backend integrations payment id
import random
# for the razor pay
import razorpay
from django.contrib.sites.shortcuts import get_current_site
from carts.views import offer_checking_function

import urllib.request

def internet_on():
    try:
        urllib.request.urlopen('http:google.com', timeout=2)
        return True
    except:
        return False


@login_required()
def palce_orders_view(request):

    user = request.user
    cart_items = CartItems.objects.filter(user=user)
    cart_items_count = cart_items.count()

    if cart_items_count <=0:
        return redirect('store:Store')

    total_price = 0
    all_total = 0
  

    coupon_code =  request.session.get('coupon_id')
        
    if coupon_code:
        # applied_coupon = True
        if Coupon.objects.filter(id=coupon_code).exists():
            coupon_object = Coupon.objects.get(id=coupon_code)
            for items in cart_items:
                total_price +=  items.coupon_offer(coupon_object)#items.product.price * items.quantity
                total_price = round(total_price, 2)
        else:
            messages.error(request,'coupon not exist ')
            del request.session['coupon_id']
            return redirect('cart')           
    else:
        for item in cart_items:
            # total_price += item.product.price * item.quantity
            price_calculation = offer_checking_function(item)
            total_price += price_calculation[0]
            # quantity +=  price_calculation[1]

    if total_price<1000:
        shipping_charge = 30
        all_total = total_price + shipping_charge
    else:
        shipping_charge = 0
        all_total = total_price

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
          
            single_oder = form.save(commit=False)
            single_oder.user = user
            single_oder.order_total = all_total
            single_oder.ip = request.META.get('REMOTE_ADDR')
            single_oder.save()
            todays_date = datetime.now()
            year = str(todays_date.year)
            day = str(todays_date.day)
            month = str(todays_date.month)
            order_id_generated = year+day+month+str(todays_date.strftime("%H:%M:%S"))+str(single_oder.id)
            single_oder.order_number = order_id_generated

            # checking the coupon is available or not :
            # if it available then it showing the 
            if coupon_code:
                single_oder.coupon = coupon_object
                single_oder.discount = coupon_object.discount

            # this for reference to the order table

            request.session['order_id'] = single_oder.order_number
            print(request.session['order_id'],'))))))))))))))))))))))))))))))))))))))))))**************')
            single_oder.save()
            
            return redirect('payments',order_id=single_oder.order_number)   
        else:
            return HttpResponse('form is not valid')

@login_required()
def payments_view(request,order_id):


    user = request.user
    cart_items = CartItems.objects.filter(user=user)
    orders= Order.objects.get(order_number=order_id)

    host = request.get_host()
    # paypal backend forms 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % orders.order_total,
        'item_name': 'Order {}'.format(orders.order_number),
        'invoice': str(orders.order_number),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_success_paypal')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
    
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    # razor pay integrations end here
    
    cart_items_count = cart_items.count()
    # we need to pass these details to frontend.
    if cart_items_count <=0:
        return redirect('store:Store')

    total_price = 0
    all_total = 0
    for item in cart_items:
        # total_price += item.product.price * item.quantity
        price_calculation = offer_checking_function(item)
        total_price += price_calculation[0]
    
    if total_price<1000:
        shipping_charge = 30
    else:
        shipping_charge = 0


    client = razorpay.Client(auth=("rzp_test_hZS1JbACCy0OBz", "fv8PkwpgAfTokZlamoCt5Ubg"))
    
    DATA = {
                    "amount": int(orders.order_total) * 100,
                    "currency": "INR",
                    "payment_capture": "1"
                    }
    payment = client.order.create(data=DATA)
    RazorPay.objects.create(order=orders,razor_pay=payment['id'])
    
    
    context = {

            'all_total':orders.order_total,
            'shipping_charge': shipping_charge,
            'cart_items': cart_items,
            'orders':orders,
            'total_price':orders.order_total-shipping_charge,
            'form': form,
            'payment_id':payment.get('id'),
            'payment':payment,
            'payment_amount': orders.order_total * 100,
            

        }

    return render(request,'home/payment.html',context)

@csrf_exempt
def razorpay_payment(request):

    def verify_signature(response_data):

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:


        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        razor_pay = RazorPay.objects.get(razor_pay=provider_order_id)
        # cart_items,and order table data taken
        order = Order.objects.get(order_number=razor_pay.order.order_number)
        
        if verify_signature(request.POST):
            cart_items = CartItems.objects.filter(user=request.user)
            payments = Payment()
            payments.user= request.user
            payments.payment_id = order.order_number
            payments.payment_method = 'RAZOR PAY'
            payments.amount = order.order_total
            payments.status = 'COMPLETED'
            payments.save()
            order.payment = payments
            order.is_ordered = True
            order.save()
            order.save()
            request.session['order_id'] = order.order_number


            for items in cart_items:

                order_product = OrderProduct()
                order_product.order = order
                order_product.payment = payments
                order_product.user =  items.user
                order_product.product =items.product
                order_product.quantity = items.quantity 
                order_product.product_price = items.product.price
                order_product.ordered = True
                order_product.save()

                    # product stock reduce 
                product = Product.objects.get(id=items.product.id)
                product.stock = product.stock - items.quantity

                    # checking the stock of the product
                if product.stock < 0:
                    product.stock= 0 
                    product.is_available=False

                product.save()
                # deleteing the product from the cartitems
                items.delete()
            return redirect('payment_success')
        else:
            messages.error(request, 'Sorry The payment Failed! try again ')
            return redirect('payments',order_id=order.order_number)
    else:
        return render(request, 'home/error.html')
            
@login_required()           
@csrf_exempt
def payment_canceled(request):
    return render(request, 'home/error.html')




def cash_on_delivery_view(request,order_id):

    if Order.objects.filter(order_number=order_id,is_ordered=False).exists():
        orders= Order.objects.get(order_number=order_id,is_ordered=False)
        cart_items = CartItems.objects.filter(user=request.user)
    
    
        payments = Payment()
        payments.user= request.user
        payments.payment_id = order_id
        payments.payment_method = 'COD'
        payments.amount = orders.order_total
        payments.status = 'PENDING'
        payments.save()
        orders.payment = payments
        orders.is_ordered = True
        orders.save()

        # move the cart_items to orders product table 

        for items in cart_items:

            order_product = OrderProduct()
            order_product.order = orders
            order_product.payment = payments
            order_product.user =  items.user
            order_product.product =items.product
            order_product.quantity = items.quantity 
            order_product.product_price = items.product.price
            order_product.ordered = True
            order_product.save()

            # product stock reduce 
            product = Product.objects.get(id=items.product.id)
            product.stock = product.stock - items.quantity

            # checking the stock of the product
            if product.stock < 0:
                product.is_available=False

            product.save()
            # deleteing the product from the cartitems
            items.delete()
        
        return redirect('payment_success')
    else:
        return redirect('store:Store')

@login_required()
def payment_succesfull(request):
    
    if request.session.get('coupon_id'):
        coupon_code =  request.session.get('coupon_id')
        coupon = Coupon.objects.get(id=coupon_code)

        if CouponUsedUsers.objects.filter(user=request.user,coupon=coupon.coupon_code).exists():
            user_used_coupon = CouponUsedUsers.objects.get(user=request.user,coupon=coupon.coupon_code)
            user_used_coupon.count += 1
            user_used_coupon.save()
            del request.session['coupon_id']
        else:
            CouponUsedUsers.objects.create(coupon= coupon.coupon_code,count=1,user=request.user)
            del request.session['coupon_id']
    

    if request.session.get('order_id'):
        order_id = request.session.get('order_id')
        del request.session['order_id']
    else:
        return redirect('home')


    order_products=OrderProduct.objects.filter(user=request.user,order__order_number=order_id)
    order= Order.objects.get(user=request.user,order_number=order_id)
    total_product_price = 0
    delivery_charge = 0
    all_total = 0


    total_product_price = order.order_total
    # some chnages happend here look carefully
    # for item in order_products:
    #     total_product_price += item.product.price * item.quantity
    if total_product_price<1000:
        delivery_charge = total_product_price - 30
        delivery_charge = total_product_price - delivery_charge
        total_product_price = total_product_price - delivery_charge
    else:
        delivery_charge = 0
        

                    
    context = {
                    'total_product_price':total_product_price ,
                    'delivery_charge':delivery_charge,
                    'all_total':total_product_price + delivery_charge,
                    'order_products': order_products,
                    'order': order,
                }
    return render(request,'home/payment_success_page.html',context)





""" this view is for the paypal payment integration from the frontend. dont delete it jithin😀"""
@login_required()
def paypal_payment_view(request,order_id):

    if request.method=="POST":
        request.session['order_id'] = order_id
    
        body = json.loads(request.body)

        orders= Order.objects.get(order_number=order_id)
        cart_items = CartItems.objects.filter(user=request.user)
        total_price = 0
        all_total = 0

        for item in cart_items:
            total_price += item.product.price * item.quantity

        if total_price<1000:
            shipping_charge = 30
            all_total = total_price + shipping_charge
        else:
            shipping_charge = 0
            all_total = total_price

        payments = Payment()
        payments.user= request.user
        payments.payment_id = body['transaction_id']
        payments.payment_method = 'PAYPAL'
        payments.amount = orders.order_total
        payments.status = body['transaction_status']
        payments.save()
        orders.payment = payments
        orders.is_ordered = True
        orders.save()

        # move the cart_items to orders product table 

        for items in cart_items:

            order_product = OrderProduct()
            order_product.order = orders
            order_product.payment = payments
            order_product.user =  items.user
            order_product.product =items.product
            order_product.quantity = items.quantity 
            order_product.product_price = items.product.price
            order_product.ordered = True
            order_product.save()

            # product stock reduce 
            product = Product.objects.get(id=items.product.id)
            product.stock = product.stock - items.quantity

            # check the stock is greater than 0
            if product.stock < 0:
                product.is_available=False
            
            product.save()
            # deleteing the product from the cartitems
            items.delete()

            order_products=OrderProduct.objects.filter(user=request.user,order__order_number=order_id)
            order= Order.objects.get(user=request.user,order_number=order_id)
            total_product_price = 0
            delivery_charge = 0
            all_total = 0

            for item in order_products:
                total_product_price += item.product.price * item.quantity
            if all_total<1000:
                delivery_charge = 30
                all_total = total_product_price + delivery_charge
            else:
                delivery_charge = 0
                all_total = total_product_price
        return JsonResponse({'success': 'completed the deleted car an all things'})

    # return render(request,'home/payment_success_page.html')
''' this view is for the paypal backend integrations'''

@csrf_exempt
@login_required()
def paypal_backend_integrations(request):
   
    order_id = request.session.get('order_id')
    if Order.objects.filter(order_number=order_id,is_ordered=False).exists():
        orders= Order.objects.get(order_number=order_id)
        cart_items = CartItems.objects.filter(user=request.user)
        total_price = 0
        all_total = 0
        for item in cart_items:
            total_price += item.product.price * item.quantity

        if total_price<1000:
            shipping_charge = 30
            all_total = total_price + shipping_charge
        else:
            shipping_charge = 0
            all_total = total_price
        payments = Payment()
        payments.user= request.user
        random_number = random.randint(1,100) 
        payments.payment_id = order_id+str(random_number)
        payments.payment_method = 'PAYPAL'
        payments.amount = orders.order_total
        payments.status = 'COMPLETED'
        payments.save()
        orders.payment = payments
        orders.is_ordered = True
        orders.save()

        # move the cart_items to orders product table 

        for items in cart_items:
            
            order_product = OrderProduct()
            order_product.order = orders
            order_product.payment = payments
            order_product.user =  items.user
            order_product.product =items.product
            order_product.quantity = items.quantity 
            order_product.product_price = items.product.price
            order_product.ordered = True
            order_product.save()

            # product stock reduce 
            product = Product.objects.get(id=items.product.id)
            product.stock = product.stock - items.quantity

            # checking the stock of the product
            if product.stock < 0:
                product.is_available = False

            product.save()
            # deleteing the product from the cartitems
            items.delete()
        
        return redirect('payment_success')
    else:
        return redirect('store:Store')


@login_required()
def user_oreder_list_view(request):
    # the all details i took from the context preprocessor from the order.contex.Orderproduct
    return render(request,'home/user_orders.html')
@login_required()
def cancel_order_view(request,order_id):
    try:
        order_product = OrderProduct.objects.get(id=order_id,ordered=True)
    except OrderProduct.DoesNotExist:
        pass
    order_product.ordered = False
    try:
        product = Product.objects.get(id=order_product.product.id)
        product.stock += order_product.quantity 
        product.save()
    except:
        pass  
    # order_product.order.status = "Cancelled"
    try:
        order = Order.objects.get(id=order_product.order.id)
        order.status = 'Cancelled'
        order.save()
    except:
        pass
    order_product.save()

    return redirect('user_orders')


@login_required()
def return_order_view(request,order_id):

    order_product = OrderProduct.objects.get(id=order_id,user=request.user)
    order_product.order.status = 'Returned'
    order_product.order.save()

    return redirect('user_orders') 
 
    



