from unicodedata import name
from django.urls import path
from carts import views


urlpatterns = [
    # cart
    path('',views.cart,name='cart'),
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name='add-to-cart'),
    path('delete_cart/<int:cart_id>/',views.delete_cart,name='delete_cart'),
    # checkout
    path('check_out/',views.check_out_view,name='check_out'),
    # buy_now
    
    path('buy_now/<int:product_id>/',views.buy_now_view,name='buy_now'),

    # ajax calls
    path('increment/<int:cart_id>/',views.cart_increment,name='increment'),
    path('decrement/<int:cart_id>/',views.cart_decrement,name='decrement'),
    # user addresee for profile
    path('user_address/',views.User_profile_address,name='user_address'),
    path('coupon_apply',views.coupon_apply_view,name='coupon_apply'),
    path('cancel_coupon',views.cancel_coupon_view,name='cancel_coupon'),
    
]