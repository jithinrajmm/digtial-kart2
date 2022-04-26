from django.contrib import admin
from store.models import Product
# Register your models here.

class AdminPage(admin.ModelAdmin):
    model=Product
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','category','price','is_available','stock','updated')
    

admin.site.register(Product,AdminPage)
