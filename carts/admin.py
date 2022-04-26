from django.contrib import admin
from carts.models import Cart,CartItems,Coupon,CouponUsedUsers

# Register your models here.
class cartAdmin(admin.ModelAdmin):
    model=CartItems
    list_display = ('user','product','cart','quantity','is_active')

admin.site.register(Cart)
admin.site.register(CartItems,cartAdmin)
admin.site.register(Coupon)
admin.site.register(CouponUsedUsers)