

# project directory



from django.shortcuts import render,redirect # this is the start
import datetime
from django.http import JsonResponse,HttpResponse

from adminpanel.models import Admin, CategoryOffer, ProductOffer
from adminpanel.forms import AdminForm
from django.contrib import messages
from accounts.models import Account
import json 
from adminpanel.decorator import adminlogin,logout
from category.models import Category
from orders.context import order_product
from store.models import Product
from adminpanel.forms import ProductForm,CategoryForm,CategoryOfferForm,ProductOfferForm
import os
from adminpanel.forms import OrderFilter

from orders.models import Order,OrderProduct, Payment


# order Edit Form for admin
from orders.forms import OrderFormEdit
from accounts.models import Account
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import TruncMonth

# coupon models from cart
from carts.models import Coupon
from adminpanel.forms import CouponForm
# pdf convertion packages
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# table views 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# this is for the csv file
import csv  
# for paginator
from django.core.paginator import Paginator

#admin home
@logout
def adminHome(request):

    users = Account.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    cancelled_orders = Order.objects.filter(status='Cancelled')
    completed_orders = Order.objects.filter(status='Completed')
    accepted_orders = Order.objects.filter(status='Accepted')
    new_orders = Order.objects.filter(status='New')

    payment_details = Payment.objects.all()
    payment_completd = Payment.objects.filter(status='COMPLETED')
    pending_completd = Payment.objects.filter(status='PENDING')
    order_revenue = Payment.objects.all()
    orderd_products = OrderProduct.objects.filter(ordered=True)
    today = datetime.date.today()
    year_wise = Order.objects.filter(created_at__year = today.year) 
                     
    # aggrecation error int + str not support 
    # total_income = Order.objects.aggregate(sum('order_total'))
    total_revenue = 0
    for amounts in order_revenue:

        if isinstance(amounts.amount, str):
            total_revenue+= float(amounts.amount)
        else:
            total_revenue += amounts.amount

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_registerd_users = Account.objects.filter(date_joined__range=(today_min, today_max))
    today_revenue_list = Payment.objects.filter(created__range=(today_min, today_max))
    
    today_revenue= 0
    for amounts in today_revenue_list:
        if isinstance(amounts.amount, str):
            today_revenue+= float(amounts.amount)
        else:
            today_revenue += amounts.amount
    

    payment_methods = {}
    if Payment.objects.filter(payment_method='COD').exists():
        cod = Payment.objects.filter(payment_method='COD')
    else:
        cod = None
    if Payment.objects.filter(payment_method='PAYPAL').exists():
        paypal = Payment.objects.filter(payment_method='PAYPAL')
    else:
        paypal = None
    payment_method_type = None

    # this is checking the count of  paypal and cod,
    if cod and paypal:
        if cod.count() > paypal.count():

            payment_methods = cod
            payment_method_type= cod[0]
        else:
            payment_methods = paypal
            payment_method_type= paypal[0]
    
    
    context = {
    'total_orders': total_orders,
    'total_revenue':round(total_revenue,2),
    'users':users,
    'today_registerd_users':today_registerd_users,
    'cancelled_orders':cancelled_orders,
    'cod':cod,
    'paypal': paypal,
    'payment_methods':payment_methods,
    'payment_method_type':payment_method_type,
    'today_revenue':round(today_revenue,2),
    'cod': cod,
    'paypal': paypal,
    'orderd_products':orderd_products,
    'payment_details':payment_details,
    'completed_orders':completed_orders,
    'accepted_orders':accepted_orders,
    'new_orders':new_orders,
    'payment_completd':payment_completd,
    'pending_completd':pending_completd,
    'year_wise':year_wise,
    'order_revenue':order_revenue,
     }
    return render(request,'adminindex.html',context)

@adminlogin
def adminLogin(request):

    form = AdminForm(request.POST or None)
    if request.method == 'POST':
        user_name = request.POST.get('admin_name')
        password1 = request.POST.get('password')

        if Admin.objects.filter(admin_name=user_name,password=password1).exists():
            user = Admin.objects.get(admin_name=user_name,password=password1)
            authenticated = user.admin_authenticate(user_name,password1)
            if authenticated:
                request.session['id']=user.id
                
                return redirect('adminhome')
        else:
            messages.error(request, 'Not valid credentials')

    context = {
            'form':form
        }

    return render(request,'adminlogin.html',context)


#admin register
@adminlogin
def admin_register(request):

    form = AdminForm()
    if request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminLogin')

    context = {
        'form': form
    }
    return render(request,'adminregister.html',context)


# admin logout
def admin_logout(request):

    if 'id' in request.session:
        request.session.flush()
        return redirect('adminLogin')
    


# user management
@logout
def user_management(request):
    users  = Account.objects.all()

    user_paginator = Paginator(users,5)
    page_number = request.GET.get('page')
    paginated_users = user_paginator.get_page(page_number)

    context = {
        'users': paginated_users,
    }
 
    return render(request,'usermanagement.html',context)

# ajax used put method for activatin the user and inactivate the user
def active_inactive_user(request):

    if request.method == 'PUT':

        # taking the data from the request
        data1 = json.load(request)
        ajax_id = data1.get('id')
        user = Account.objects.get(id=ajax_id)

        # changing the is_active to opposite value
        user.is_active = not user.is_active
        user.save()
        user_active_value = user.is_active

        context = {
            'user_active_value': user_active_value
                }
        return JsonResponse(context)  
    return JsonResponse({'hai':'hello'})


# product management start here
# product_view
@logout
def product_view(request):

    product_form = ProductForm()
    products = Product.objects.all()
    product_count = products.count()
    category_count = Category.objects.all().count()
    product_paginator = Paginator(products,5)
    page = request.GET.get('page')
    products = product_paginator.get_page(page)

    context = {

        'products':products,
        'product_count': product_count,
        'category_count': category_count,
        'product_form': product_form,

    }
    return render(request,'product_management.html',context) 

# ajax call for viewing the product

def single_product(request):
    product_id = request.GET.get('id')

    try:
        product = Product.objects.get(id=product_id)       
                
    except Exception as e:
        raise e

    categories = Category.objects.all()
    count = 0

    for categor in categories:
        count = count+1
        if categor.category_name == product.category.category_name:
            break
    


    items ={

        'id': product.id,
        'name': product.product_name,
        'slug': product.slug,
        'category': product.category.category_name,
        'price': product.price,
        'stock': product.stock,
        'description': product.description,
        'image_1': product.image_1.url,
        'image_2': product.image_2.url,
        'image_3': product.image_3.url,
        'image_4': product.image_4.url,
        'category_count': count,

    }
    


    return JsonResponse({'products':items})
# product add
@logout
def product_add(request):

    form = ProductForm()
    if request.method == 'POST': 
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('product_view')
    
    context = {
        'product_form':form,
    }
    return render(request,'product_add.html',context)

# PRODUCT DELETE
@logout
def product_delete(request,id):

    if Product.objects.filter(id=id).exists():
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request, 'Deleted success fully')
        return redirect('product_view')
        
    else:
        messages.error(request, 'Product is not available')
        return redirect('product_view')
# PRODUCT UPDATE
@logout
def product_update(request,id):

    if Product.objects.filter(id=id).exists():
        product = Product.objects.get(id=id)
    else:
        return redirect('product_view')

    product_form = ProductForm(instance=product)

    if request.method == "POST":
        product_form = ProductForm(request.POST,request.FILES,instance=product)
        print(product_form)
        if product_form.is_valid():
           
            image1_path = product.image_1.path
            image2_path = product.image_2.path
            image3_path = product.image_3.path
            image4_path = product.image_4.path
            path_list = []
            path_list.extend([image1_path,image2_path,image3_path,image4_path])
            for single_path in path_list:
                if os.path.exists(single_path):
                    os.remove(single_path)
            product_form.save()
            return redirect('product_view')



    context = {
        'product_form':product_form,
        'product':product,
    }
    # return redirect('product_view')
    return render(request,'product_update.html',context)
    




# category management
#  category view
@logout
def category_view(request):

    category_form = CategoryForm(request.POST or None)
    if request.method == 'POST':
        if category_form.is_valid():
            category_form.save()
            messages.success(request,'Added succesfully')
            return redirect('category_view')
        else:
            messages.error(request,'Something wrong chekc the data and try again')
            return redirect('category_view')
    
    categories = Category.objects.all()
    category_count = categories.count()
    category_product_count = {}

    for category in categories:
        category_product_count[category.category_name] = category.product_set.count()


    
    context = {
        'categories': categories,
        'category_count': category_count,
        'cat_product_count':category_product_count,
        'category_form':category_form,
    }

    return render(request,'category_management.html',context)


@logout
def category_delete(request,id):

    if Category.objects.filter(id=id).exists():
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request,'Deleted succesfully')
        return redirect('category_view')
    else:
        messages.error(request,'The category is not available')
        return redirect('category_view')

@logout
def category_edit(request,id):

    if Category.objects.filter(id=id).exists():
        category = Category.objects.get(id=id)
        form = CategoryForm(instance=category)
        if request.method == 'POST':
            form = CategoryForm(request.POST,instance=category)
            if form.is_valid():
                form.save()
                messages.success(request,'Updated success fully')
                return redirect('category_view')


        context = {
                    'category_edit_form': form
                  }

        return render(request,'category_edit.html',context)
    else:
        messages.error(request,'this data is not present')
        return redirect('category_view')


# its only showing the order table
@logout
def order_management_view(request):

    orders = Order.objects.all()
    user_paginator = Paginator(orders,5)
    page_number = request.GET.get('page')
    orders = user_paginator.get_page(page_number)

    order_products = OrderProduct.objects.all()
    context = {
                'orders': orders,
                'orders_products': order_products,
              }

    return render(request,'order_management.html',context)
@logout
def order_product_table(reqeust):
    
    order_products = OrderProduct.objects.filter()

    context = {
              'order_products': order_products,
              }

    return render(reqeust,'order_product_admin.html',context)

@logout
def order_cancel_view(requset,order_id):

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
    return redirect('order_products')



# order edit 
@logout
def order_edit_view(request,order_id):

    order = Order.objects.get(id=order_id)
    form = OrderFormEdit(request.POST or None,instance=order)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('order_view')
    context = {
        'forms': form,
    }
    return render(request,'order_edit_form.html',context)

# coupon management views
@logout
def coupon_management_view(request):

    coupons = Coupon.objects.all()

    context = {
        'coupons': coupons,
    }

    return render(request,'offer_management/coupon_management.html',context)  

@logout
def coupon_add_view(request):

    form = CouponForm(request.POST or None)
    context = {
        'form': form,
        'update':False,
    }
    if request.method == "POST":
        
        if form.is_valid():
            form.save()
            messages.success(request,'added coupon successfully')
            return redirect('coupon_management')
            
        
    return render(request,'offer_management/coupon_add.html',context)

@logout
def delete_coupon_view(request,coupon_id):
    
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    messages.error(request,'deleted success fully')
    return redirect('coupon_management')
@logout
def update_coupon_view(request,coupon_id):

    coupon  = Coupon.objects.get(id=coupon_id)
    update_form = CouponForm(request.POST or None,instance=coupon)
    
    if update_form.is_valid():
        update_form.save()
        messages.success(request,f'Updated success Fully')
        return redirect('coupon_management')
    context = {
        'update': True,
        'form': update_form,
    }
    return render(request,'offer_management/coupon_add.html',context)
@logout
def active_coupon_view(request,coupon_id):

    coupon = Coupon.objects.get(id=coupon_id)
    coupon.active = not coupon.active
    coupon.save()
    if coupon.active:
        messages.success(request,'Activated Coupon')
    else:
        messages.success(request,'Deactivated  coupon')
    return redirect('coupon_management')

    
    
# coupon management end here


# Product Offer management View Start Heare
@logout
def product_offer_mangement_view(request,message=None):

    if message:
        messages.success(request,'Product Offer Added')

    error = False
    products_offers = ProductOffer.objects.all()
    form = ProductOfferForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Product Offer Added')
            return redirect('product_offer_management')
            
        else:
            error = True
    product_offer_paginator = Paginator(products_offers,5)
    page_number = request.GET.get('page')
    products_offers = product_offer_paginator.get_page(page_number)

    context = {
        'form': form,
        'error':error,
        'products_offers': products_offers,
    }
    return render(request,'offer_management/product_offer.html',context)
@logout
def delete_product_offer_view(request,id):

    offer_product = ProductOffer.objects.get(id=id)
    offer_product.delete()
    messages.success(request,'deleted the Product Offer')
    return redirect('product_offer_management')
@logout
def edit_product_offer_view(request,id):

    offer_product = ProductOffer.objects.get(id=id)
    form = ProductOfferForm(instance=offer_product)

    if request.method== "POST":
        form = ProductOfferForm(request.POST,instance=offer_product)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Success fully')
            return redirect('product_offer_management')
        else:
            messages.error(request,'Try again')

    context = {
        'form': form,
    }
    return render(request,'offer_management/product_offer_update.html',context)
@logout
def active_deactive_product_offer_view(request,id):

    product_offer = ProductOffer.objects.get(id=id)
    product_offer.active =  not product_offer.active
    product_offer.save()

    if product_offer.active == True:
        messages.success(request,'Activated Offer')
    else:
        messages.error(request,'Deactivated Offer')

    return redirect('product_offer_management')


@logout
def category_offer_view(reqeust):

    errors = False
    form = CategoryOfferForm(reqeust.POST or None)
    if reqeust.method == "POST":

        if form.is_valid():
            form.save()
            messages.success(reqeust,'Added success fully')
            return redirect('category_offer')

        else:
            errors = True
            messages.error(reqeust,'Check the form')


    category_offers = CategoryOffer.objects.all()

    category_offer_paginator = Paginator(category_offers,5)
    page_number = reqeust.GET.get('page')
    category_offers = category_offer_paginator.get_page(page_number)
    
    context = {
        'category_offers': category_offers,
        'form': form,
        'errors' : errors,

        }

    return render(reqeust,'offer_management/category_offers.html',context)


@logout
def delete_category_offer_view(request,id):

    offer_category = CategoryOffer.objects.get(id=id)
    offer_category.delete()
    messages.success(request,'deleted the Category Offer')
    return redirect('category_offer')
@logout
def edit_category_offer_view(request,id):

    offer_Category = CategoryOffer.objects.get(id=id)
    form = CategoryOfferForm(instance=offer_Category)

    if request.method== "POST":
        form = CategoryOfferForm(request.POST,instance=offer_Category)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Success fully')
            return redirect('category_offer')
        else:
            messages.error(request,'Try again')

    context = {
        'form': form,
    }
    return render(request,'offer_management/category_offer_update.html',context)
@logout
def active_deactive_category_offer_view(request,id):

    offer_Category = CategoryOffer.objects.get(id=id)
    offer_Category.active =  not offer_Category.active
    offer_Category.save()

    if offer_Category.active == True:
        messages.success(request,'Activated Offer')
    else:
        messages.error(request,'Deactivated Offer')

    return redirect('category_offer')

    # End category offer Here

@logout
def admin_report_view(request):

    form = OrderFilter(request.GET, queryset=OrderProduct.objects.all())

    value = request.GET
    filter_query_set = OrderFilter(value, queryset=OrderProduct.objects.all()).qs
   
    pdf = request.GET.get('pdf')
    csvs = request.GET.get('csv')

    if pdf: 

        buffer = io.BytesIO()
        canvas_s = canvas.Canvas(buffer,pagesize = letter) 
        width, height = letter
        textob = canvas_s.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        lines = []
        for order in filter_query_set:
            lines.append((order.product.product_name,order.payment.status,order.payment.payment_method,order.product.category.category_name,
                            order.product_price,order.created_at.strftime("%B-%d-%Y")))
        table = Table(lines, colWidths = [80 for i in range(1,6)] ,rowHeights=[20 for i in range(0,len(filter_query_set))])
        table.setStyle([('BOX',(0,0),(-1,-1),1 ,colors.red),
                        ('GRID',(0,0),(-1,-1),1,colors.green)])
        table.wrapOn(canvas_s, width, height)
        table.drawOn(canvas_s, 20 * mm, 0 * mm)

        canvas_s.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

    if csvs:
        
        response = HttpResponse(content_type='text/csv')  
        response['Content-Disposition'] = 'attachment; filename="file.csv"'  
        orders_product = filter_query_set
        # create a csv writer
        writer = csv.writer(response)  
        # create column headers
        writer.writerow(['Order','Payment','User','product','quantity','porduct-price','Date'])
        # Loop through the orders its show like a column in the csv files
        for order_product in orders_product:  
            writer.writerow([order_product.order,order_product.payment,order_product.user,order_product.product,order_product.quantity,order_product.product_price,order_product.created_at])  
        return response  
    


        

    context = {
        'filter': form,
        'filter_query_set':filter_query_set,
    }
    return render(request,'report_admin/admin_report.html',context)


