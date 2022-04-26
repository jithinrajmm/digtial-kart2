


from email import message
from multiprocessing import context
from django.shortcuts import render,redirect

from accounts.forms import CustomUserCreationForm, UserAddressForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout

from accounts.models import Account, UserAddress
from django.contrib import messages
import random
from accounts.util import send_sms
# database tables
from carts.models import Cart,CartItems
from carts.views import _get_cart_id

import requests
# Create your views here.

# user profile
from accounts.models import UserProfile


def userLogin(request):

    if request.user.is_authenticated:
        return redirect('home')
    forms = AuthenticationForm()
    if request.method == 'POST':
        forms = AuthenticationForm(request,data = request.POST)

        if forms.is_valid():

            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password')
  
            user = authenticate(username=username,password=password)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_get_cart_id(request))
                    cart_items_exists = CartItems.objects.filter(cart=cart).exists()
                    if cart_items_exists:
                        cart_items = CartItems.objects.filter(cart=cart)
                        
                        cart_items_user_exist = CartItems.objects.filter(user=user).exists()
                        if cart_items_user_exist:
                            cart_items_user = CartItems.objects.filter(user=user)
                            for items in cart_items:
                                for user_item in cart_items_user:
                                    if items.product == user_item.product:

                                        user_item.quantity = items.quantity + user_item.quantity
                                        items.delete()
                                        user_item.save()
                        else:
                            for items in cart_items:
                                items.user = user
                                items.save()
                except :
                    pass
                login(request,user)
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    # ?next=/cart/check_out/
                    path = query.split('=')
                    
                    return redirect(path[1])
                except:
                    pass
                

    return render(request,'accounts/userlogin.html',{'authenticationForm': forms})

def userRegister(request):

    forms = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST':
        if forms.is_valid():

           new_user =  forms.save(commit=False)
           username = new_user.email[0:new_user.email.index('@')]
           new_user.is_active = True
           new_user.username = username
           new_user.save()
           return redirect('user_login')

    return render(request,'accounts/userregister.html',{'creationForms':forms})

def otpLogin(request):

    otp_mobile= True

    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        if Account.objects.filter(phone=mobile_number).exists():
            user = Account.objects.get(phone=mobile_number)
            number_list = [i for i in range(10)]
            code_list = []
            for number in range(4):
                random_number = random.choice(number_list)
                code_list.append(random_number)
            string_number = "".join(str(item) for item in code_list)
            request.session['otp_code'] = string_number
            send_sms(string_number,user.phone)
            return redirect('otp_check',id=user.id)
        else:
            messages.error(request, 'The phone number is not registerd')

    return render(request,'accounts/otplogin.html',{'otp_mobile':otp_mobile})

# this method is checking the phone number is existing in the database
def otp_check(request,id):

    user = Account.objects.get(id=id)
    otp_mobile= False      
    if request.method == "POST":
        otp_from_user = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        
        
        if  otp_code == otp_from_user:
            if request.session.get('otp_code'):
                del request.session['otp_code']
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'The otp is not correct')
            
    return render(request,'accounts/otplogin.html',{'otp_mobile':otp_mobile})


# this is for the forget password 
def forgot_password_view(request):
    pass
# user Proifle views
def user_profile_view(request):

    user_profile = UserProfile.objects.get(user=request.user)
    user = Account.objects.get(id=request.user.id)
    form = UserProfileForm(instance=user_profile)
    orders = user.orderproduct_set.all()
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
       
        if form.is_valid():
            
            form.save()
            return redirect('user_profile')
        else:
            pass

    context = {
        'user_profile': user_profile,
        'orders': orders[:4],
        'form': form,
    }
    return render(request,'accounts/user_profile.html',context)

def user_address_add(request):
    
    form = UserAddressForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request,'Address Addedd')
            address_valid = 'True'
            return redirect('check_out',address_valid)
        else:
            address_valid = 'False'
            return redirect('check_out',address_valid = address_valid)


def address_delete_view(request,address_id):
    address = UserAddress.objects.get(id=address_id)
    address.delete()
    messages.success(request,'Deleted success fully')
    return redirect('check_out','False')

def userLogout(request):
    logout(request)
    return redirect('home')