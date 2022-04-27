from django.urls import path
from orders import views


urlpatterns = [
    path('place_orders/',views.palce_orders_view,name='place_orders'),
    path('payments/<str:order_id>/',views.payments_view,name='payments'),
    path('cash_on_delivery/<str:order_id>/',views.cash_on_delivery_view,name='cash_on_delivery'),

    # user_ordrs_list

    path('user_order/',views.user_oreder_list_view,name='user_orders'),
    path('cancel_order/<str:order_id>/',views.cancel_order_view,name='cancel_order'),

    # paypal success view

    path('success_paypal/<str:order_id>/',views.paypal_payment_view,name='success_paypal'),
    path('payment_success/',views.payment_succesfull,name = 'payment_success'),

    # paypal serverside integrations aan tto

    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('payment_success_paypal',views.paypal_backend_integrations,name='payment_success_paypal'),
    # razor pay call back means after the success ful payment redirect to this view
    path("razor_pay_payment/", views.razorpay_payment, name="razor_pay_payment"),
    path("return_order/<str:order_id>/", views.return_order_view, name="return_order"),
  
    


]