from django.contrib import admin

from orders.models import Payment,Order,OrderProduct,RazorPay
class OrderAdmin(admin.ModelAdmin):
    list_display= ( 'order_number', 'order_total', 'status')
class PaymentAdmin(admin.ModelAdmin):
    list_display= ( 'payment_id', 'payment_method', 'amount','status','created')
# Register your models here.
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(RazorPay)



    
