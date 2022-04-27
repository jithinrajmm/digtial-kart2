from unicodedata import name
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail


urlpatterns =[
    path('user_login/',views.userLogin,name='user_login'),
    path('user_register/',views.userRegister,name='user_register'),
    path('user_logout/',views.userLogout,name='user_logout'),
    path('otp_login/',views.otpLogin,name='otp_login'),
    path('otp_check/<int:id>/',views.otp_check,name='otp_check'),
    path('user_profile/',views.user_profile_view,name='user_profile'),
    # add address
    path('address_add',views.user_address_add,name='address_add'),
    path('address_delete/<str:address_id>/',views.address_delete_view,name='address_delete'),
    path('address_edit/<str:address_id>/',views.address_edit_view,name='address_edit'),

    # password reset views
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]