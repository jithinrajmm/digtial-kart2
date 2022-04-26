
from unicodedata import name
from django.urls import  path
from adminpanel import views



urlpatterns = [

    path('',views.adminHome, name='adminhome'),
    path('adminLogin/',views.adminLogin,name='adminLogin'),
    path('adminregister/',views.admin_register,name='adminregister'),
    path('adminLogout/',views.admin_logout,name='adminLogout'),

    # user management
    path('usermanagement/active_inactive/',views.active_inactive_user,name='active_inactive'),
    path('usermanagement/',views.user_management,name='usermanagement'),

    # product management
    path('product_view/',views.product_view,name='product_view'),
    path('product_view/testing', views.single_product, name='single_product'),
    path('product_add/',views.product_add,name='product_add'),
    path('product_update/<int:id>/',views.product_update,name='product_update'),
    path('product_delete/<int:id>/',views.product_delete,name='product_delete'),

    # category management
    path('category_view/', views.category_view, name='category_view'),
    path('category_delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category_edit/<int:id>/', views.category_edit, name='category_edit'),

    # order management
    path('order_view',views.order_management_view,name='order_view'),
    path('order_cancel_admin/<str:order_id>/',views.order_cancel_view,name='order_cancel_admin'),
    path('order_products/',views.order_product_table,name='order_products'),
    path('order_edit/<str:order_id>/',views.order_edit_view,name='order_edit'),

    # coupon_management_view
    path('coupon_management',views.coupon_management_view,name='coupon_management'),
    path('delete_coupon/<str:coupon_id>/',views.delete_coupon_view,name='delete_coupon'),
    path('update_coupon/<str:coupon_id>/',views.update_coupon_view,name='update_coupon'),
    path('active_coupon/<str:coupon_id>/',views.active_coupon_view,name='active_coupon'),
    path('coupon_add/',views.coupon_add_view,name='coupon_add'),

    # product_offer 
    path('product_offer_management/',views.product_offer_mangement_view,name='product_offer_management'),
    path('delete_product_offer/<str:id>/',views.delete_product_offer_view,name='delete_product_offer'),
    path('update_product_offer/<str:id>/',views.edit_product_offer_view,name='update_product_offer'),
    path('active_deactive_product_offer/<str:id>/',views.active_deactive_product_offer_view,name='active_deactive_product_offer'),

    # category offer urls 
    path('category_offer/',views.category_offer_view,name='category_offer'),
    path('delete_category_offer/<str:id>/',views.delete_category_offer_view,name='delete_category_offer'),
    path('update_category_offer/<str:id>/',views.edit_category_offer_view,name='update_category_offer'),
    path('active_deactive_category_offer/<str:id>/',views.active_deactive_category_offer_view,name='active_deactive_category_offer'),

    # admin report urls
    path('admin_report/',views.admin_report_view,name='admin_report'),
 
    
    
    


    

    
]