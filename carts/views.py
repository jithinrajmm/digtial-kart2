

from statistics import quantiles
from unicodedata import category
from django.shortcuts import render,redirect #start 
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.contrib import messages
from adminpanel.models import CategoryOffer, ProductOffer 

from store.models import Product
from carts.models import Cart,CartItems,Coupon,CouponUsedUsers
from accounts.models import UserProfile,UserAddress


from django.contrib.auth.decorators import login_required
import requests
from orders.forms import OrderForm
from accounts.forms import UserAddressForm
from carts.forms import CouponApplyForm
from carts.models import Coupon

# Create your views here.
# This method used to add to cart items
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# this function is used to checking the 
# offers and returning the price of items in cart
def offer_checking_function(items):
    
    total_price = 0
    quantity = 0

    if CategoryOffer.objects.filter(category=items.product.category).exists():
        
        if items.product.category.catoffer:
            
            if ProductOffer.objects.filter(product=items.product).exists():
                
                if items.product.product_off and items.product.product_off.product_offer_check and items.product.category.catoffer.category_offer_check:
                        # if items.product.category.catoffer.category_offer_check:
                    product = Product.objects.get(id=items.product.id)
                    total_price = items.product.category.catoffer.category_offer_price(product) * items.quantity
                    quantity += items.quantity

            else:
                if items.product.category.catoffer.category_offer_check:
                    
                    product = Product.objects.get(id=items.product.id)
                    total_price = items.product.category.catoffer.category_offer_price(product) * items.quantity
                    quantity += items.quantity
                    

    elif ProductOffer.objects.filter(product=items.product).exists():
                
        if items.product.product_off and items.product.product_off.product_offer_check:
                # if items.product.product_off.product_offer_check:
            product = Product.objects.get(id=items.product.id)
            total_price = items.product.product_off.product_offer_price(product)* items.quantity
            quantity += items.quantity
    else:
        total_price += items.total_price()#items.product.price * items.quantity
        quantity += items.quantity

    return total_price,quantity

def _get_cart_id(reqeust):
    cart_id = reqeust.session.session_key
    if not cart_id:
        cart_id = reqeust.session.create()
    return cart_id

def add_to_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        user = request.user
        try:
            cart_item = CartItems.objects.get(product=product,user=user)
            cart_item.quantity += 1
            if product.stock < cart_item.quantity:
                cart_item.save()
            else:
                messages.error(request,'Stock is less Sorry')
                url = request.META.get('HTTP_REFERER')
                return redirect(url)

            
        except CartItems.DoesNotExist:
            cart_items = CartItems.objects.create(product=product,user=user,quantity=1)
            cart_items.save()       
    else:
        try:
            cart_ = Cart.objects.get(cart_id=_get_cart_id(request))
            
        except Cart.DoesNotExist:
            cart_ = Cart.objects.create(cart_id = _get_cart_id(request))
            cart_.save()
            
        try:

            cart_item = CartItems.objects.get(product=product,cart=cart_)
            cart_item.quantity += 1
            cart_item.save()

        except CartItems.DoesNotExist:

            cart_items = CartItems.objects.create(product=product,cart=cart_,quantity=1)
            cart_items.save()

    url = request.META.get('HTTP_REFERER')


    return redirect(url)

def buy_now_view(request,product_id):
    
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        user = request.user
        try:
            cart_item = CartItems.objects.get(product=product,user=user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            cart_items = CartItems.objects.create(product=product,user=user,quantity=1)
            cart_items.save()       
    else:
        try:
            cart_ = Cart.objects.get(cart_id=_get_cart_id(request))
            
        except Cart.DoesNotExist:
            cart_ = Cart.objects.create(cart_id = _get_cart_id(request))
            cart_.save()
           
        try:

            cart_item = CartItems.objects.get(product=product,cart=cart_)
            cart_item.quantity += 1
            cart_item.save()

        except CartItems.DoesNotExist:

            cart_items = CartItems.objects.create(product=product,cart=cart_,quantity=1)
            cart_items.save()
            
    return redirect('check_out')



def cart(request):

    total_price =  0
    all_total = 0
    quantity = 0
    cart_items= None
    shipping_charge = 0

    if request.session.get('coupon_id'):
        del request.session['coupon_id']



    try:
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user)

        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItems.objects.filter(cart=cart,is_active=True)

        # if coupon is available
    
        for items in cart_items:
            if items.quantity == 0:
                items.delete()
                cart_items = CartItems.objects.filter(cart__cart_id=_get_cart_id(request))
                continue
            # i need this function every where to calculate the offer
            # thats why i Write a function above this page 
            price_calculation = offer_checking_function(items)
            total_price += price_calculation[0]
            quantity +=  price_calculation[1]
            
           
        if total_price<1000:
            shipping_charge = 30
            all_total = total_price + shipping_charge
   
        else:
            shipping_charge = 0
            all_total = total_price

    except Cart.DoesNotExist:
        pass

         
    context = {
        'total_price':total_price,
        'product_total_count':quantity,
        'cart_items': cart_items,
        'shipping_charge':shipping_charge,
        'all_total': round(all_total,2),
        
        
            }
    return render(request,'home/cart.html',context)




# this is ajax call for increment the number of product
def cart_increment(request,cart_id):

    all_total = 0
    items_total = 0
    shipping_charge = 0
    all_cart_quantity=0

    if is_ajax(request):

        cart_session_id = request.GET.get('session_cart_id')
        product_id = request.GET.get('product_id')

        if request.user.is_authenticated:

            product = Product.objects.get(id=product_id)
            single_cart_items = CartItems.objects.get(product=product,user=request.user)
            single_cart_items.quantity +=1
            single_cart_items.save()
            cart_items = CartItems.objects.filter(user=request.user)

            for items in cart_items:
                # all_total += items.product.price * items.quantity
                # all_cart_quantity += items.quantity
                # all_total,all_cart_quantity = offer_checking_function(items)
                price_calculation = offer_checking_function(items)
                all_total += price_calculation[0]
                all_cart_quantity +=  price_calculation[1]
            
            if all_total < 1000 and all_total>1:
                shipping_charge = 30
                items_total = all_total+shipping_charge

            else:
                shipping_charge = 0
                items_total = all_total

        else:

            single_cart_items = CartItems.objects.get(id=cart_id)
            single_cart_items.quantity +=1
            single_cart_items.save()
            cart_items = CartItems.objects.filter(cart__cart_id=cart_session_id)

            for items in cart_items:
                # all_total += items.product.price * items.quantity
                # all_cart_quantity += items.quantity
                # all_total,all_cart_quantity = offer_checking_function(items)
                price_calculation = offer_checking_function(items)
                all_total += price_calculation[0]
                all_cart_quantity +=  price_calculation[1]

            
            if all_total < 1000 and all_total>1:
                shipping_charge = 30
                items_total = all_total+shipping_charge

            else:
                shipping_charge = 0
                items_total = all_total


        cart_items_respose = {
            # this totalprice is the single product price
            'totalprice': single_cart_items.total_price(),
            'product_total_count': single_cart_items.quantity,
            'all_total': round(all_total,2),
            'shipping_charge': shipping_charge,
            'items_total':items_total,
            'all_cart_quantity':all_cart_quantity,
        } 
        return JsonResponse(cart_items_respose)

def cart_decrement(request,cart_id):

    all_total = 0
    items_total = 0
    shipping_charge = 0
    all_cart_quantity = 0

    if is_ajax(request):

        cart_session_id = request.GET.get('session_cart_id')
        product_id = request.GET.get('product_id')
        
        if request.user.is_authenticated:

            product = Product.objects.get(id=product_id)
            single_cart_items = CartItems.objects.get(product=product,user=request.user)
            single_cart_items.quantity -= 1
            single_cart_items.save()
            cart_items = CartItems.objects.filter(user=request.user)
            
            for items in cart_items:
                # all_total += items.product.price * items.quantity
                # all_cart_quantity += items.quantity
                # all_total,all_cart_quantity = offer_checking_function(items)
                price_calculation = offer_checking_function(items)
                all_total += price_calculation[0]
                all_cart_quantity +=  price_calculation[1]
 
            if all_total < 1000 and all_total>1:
                shipping_charge = 30
                items_total = all_total+shipping_charge
            else:
                shipping_charge = 0
                items_total = all_total

        else:
        
            single_cart_items = CartItems.objects.get(id=cart_id)
            single_cart_items.quantity -= 1
            single_cart_items.save()
            cart_items = CartItems.objects.filter(cart__cart_id=cart_session_id)
            
            for items in cart_items:
                # all_total += items.product.price * items.quantity
                # all_cart_quantity += items.quantity
                # all_total,all_cart_quantity = offer_checking_function(items)
                price_calculation = offer_checking_function(items)
                all_total += price_calculation[0]
                all_cart_quantity +=  price_calculation[1]
 
            if all_total < 1000 and all_total>1:
                shipping_charge = 30
                items_total = all_total+shipping_charge
            else:
                shipping_charge = 0
                items_total = all_total



        cart_items_respose = {

                'totalprice':single_cart_items.total_price(),
                'product_total_count':single_cart_items.quantity,
                'all_total': round(all_total,2),
                'shipping_charge': shipping_charge,

                'items_total':items_total,
                'all_cart_quantity':all_cart_quantity


                } 
        return JsonResponse(cart_items_respose)

def delete_cart(request,cart_id):
    
    if CartItems.objects.filter(id=cart_id).exists():
        cart_item = CartItems.objects.get(id=cart_id)
        cart_item.delete()
        return redirect('cart')
    else:
        messages.success(request,'item not exists in cart')
        return redirect('cart')

# this is the check_out function
@login_required
def check_out_view(request):    
    
    total_price =  0
    all_total = 0
    quantity = 0
    applied_coupon = False
    cart_items= None
    shipping_charge = 0
    deducted_amount=0
    without_coupon=0

    try:
        if request.user.is_authenticated:
            user_address = UserAddress.objects.filter(user=request.user)
            user_profile_view = UserProfile.objects.get(user=request.user)
            cart_items = CartItems.objects.filter(user=request.user)
            
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItems.objects.filter(cart=cart,is_active=True)
        
        if bool(cart_items) == False:
            return redirect('store:Store')
        
        # checking the coupon is existing or not 
        coupon_code =  request.session.get('coupon_id')
        
        if coupon_code:
            applied_coupon = True
            if Coupon.objects.filter(id=coupon_code).exists():
                coupon_object = Coupon.objects.get(id=coupon_code)
                for items in cart_items:
                    without_coupon+= items.total_price()
                    total_price +=  items.coupon_offer(coupon_object)#items.product.price * items.quantity
                    deducted_amount += items.deducted_amount(coupon_object)
                    quantity += items.quantity
                total_price = round(total_price, 2)
                deducted_amount = round(deducted_amount,2)
                messages.success(request, 'Coupon  applied Successfully')
            else:
                messages.error(request,'coupon not exist ')
                del request.session['coupon_id']
                return redirect('cart')
        else:
            for items in cart_items:
                if items.quantity == 0:
                    items.delete()
                    cart_items = CartItems.objects.filter(cart__cart_id=_get_cart_id(request))
                    continue
                # total_price += items.product.price * items.quantity
                # quantity += items.quantity
                # total_price,quantity = offer_checking_function(items)
                price_calculation = offer_checking_function(items)
                total_price += price_calculation[0]
                quantity +=  price_calculation[1]

        if total_price<1000:
            shipping_charge = 30
            all_total = total_price + shipping_charge
        else:
            shipping_charge = 0
            all_total = total_price
    except Cart.DoesNotExist:
        pass

    coupons = Coupon.objects.filter(active=True)   
    context = {

        'total_price':total_price,
        'product_total_count':quantity,
        'cart_items': cart_items,
        'shipping_charge':shipping_charge,
        'all_total': all_total,
        'form': OrderForm(),
        'user_profile_view':user_profile_view,
        'user_address':user_address,
        'addressForm': UserAddressForm(),
        'deducted_amount':deducted_amount,
        'applied_coupon':applied_coupon,
        'without_coupon':without_coupon,
        'coupon_apply_form': CouponApplyForm(),
        'coupons': coupons,


        }
    return render(request,'home/checkout.html',context)

# coupon models in cart , form in cart.forms
def coupon_apply_view(request):

    nows = datetime.now()
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(coupon_code__iexact=code,valid_from__lte=nows,valid_to__gte=nows,active=True)
                if CouponUsedUsers.objects.filter(user=request.user,coupon__iexact=coupon.coupon_code).exists():
                    coupon_used_user = CouponUsedUsers.objects.get(user=request.user,coupon__iexact=coupon.coupon_code)
                    if coupon_used_user.count == 2:
                        messages.error(request, 'Only 2 times you can use a single coupon')
                        return redirect('check_out') 
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon Not available')
                request.session['coupon_id'] = None

            return redirect('check_out')

def cancel_coupon_view(request):

    del request.session['coupon_id']
    messages.error(request, 'Coupon Cancelled')
    return redirect('check_out')

# this ajax for fetching the user data from the UserProfile
def User_profile_address(request):

    if request.user.is_authenticated:

        if request.GET.get('id'):
            id = request.GET.get('id')
            address = UserAddress.objects.get(id=id)
            context = {
                'first_name':address.first_name,
                'last_name': address.last_name,
                'email': address.email,
                'phone': address.phone,
                'address_line_1':address.address_line_1,
                'address_line_2':address.address_line_2,
                'country': address.country,
                'state': address.state,
                'city': address.city,
                
            }
            return JsonResponse(context)
        else:
            user_profile = UserProfile.objects.get(user=request.user)
            context = {
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'username': user_profile.username,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'address_line1': user_profile.address_line_1,
                'address_line2': user_profile.address_line_2,
                'country': user_profile.country,
                'state': user_profile.state,
                'city': user_profile.city,
            }

    return JsonResponse(context)

