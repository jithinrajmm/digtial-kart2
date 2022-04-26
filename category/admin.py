from pyexpat import model
from unicodedata import category
from django.contrib import admin
from category.models import Category

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    model=Category
    prepopulated_fields = {'category_slug':('category_name',)}
    list_display = ('category_name','category_slug')
    

admin.site.register(Category,PageAdmin)
