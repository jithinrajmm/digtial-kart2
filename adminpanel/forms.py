

from cProfile import label
from django import forms #this is the first line
from django.contrib.auth.models import User
from django.forms import ModelForm
from adminpanel.models import Admin,CategoryOffer,ProductOffer
from carts.models import Coupon
from store.models import Product
from category.models import Category
from orders.models import Order,OrderProduct,Payment

from PIL import Image
from django.core.files import File
import django_filters



class AdminForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control'}))
    admin_name = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control'}))

    class Meta:
        model = Admin
        fields = ['admin_name','password']

class ProductForm(ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    # image 1 croping axis
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    # image 3 cropping axis
    """ i am skipping the second image , its already croped from the models plese look there"""
    x_3 = forms.FloatField(widget=forms.HiddenInput())
    y_3 = forms.FloatField(widget=forms.HiddenInput())
    width_3 = forms.FloatField(widget=forms.HiddenInput())
    height_3 = forms.FloatField(widget=forms.HiddenInput())

    # image 4 cropping axis
    x_4 = forms.FloatField(widget=forms.HiddenInput())
    y_4 = forms.FloatField(widget=forms.HiddenInput())
    width_4 = forms.FloatField(widget=forms.HiddenInput())
    height_4 = forms.FloatField(widget=forms.HiddenInput())


    class Meta:
        model = Product
        fields = '__all__'

    def save(self):

        photo = super(ProductForm, self).save()
        photo_3 = super(ProductForm, self).save()
        photo_4  = super(ProductForm,self).save()
        self.is_available= True

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image_1)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.image_1.path)

        # image_3 this is for the image 3 axis
        x3 = self.cleaned_data.get('x_3')
        y3 = self.cleaned_data.get('y_3')
        w3 = self.cleaned_data.get('width_3')
        h3 = self.cleaned_data.get('height_3')

        

        image3 = Image.open(photo_3.image_3)
        cropped_image3 = image3.crop((x3, y3, w3+x3, h3+y3))
        resized_image3 = cropped_image3.resize((200, 200), Image.ANTIALIAS)
        resized_image3.save(photo.image_3.path)

        # image_4 this is for the image 4 axis
        x4 = self.cleaned_data.get('x_4')
        y4 = self.cleaned_data.get('y_4')
        w4 = self.cleaned_data.get('width_4')
        h4 = self.cleaned_data.get('height_4')

        

        image4 = Image.open(photo_4.image_4)
        cropped_image4 = image4.crop((x4, y4, w4+x4, h4+y4))
        resized_image4 = cropped_image4.resize((200, 200), Image.ANTIALIAS)
        resized_image4.save(photo.image_4.path)


        return photo,photo_3,photo_4

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code','valid_from','valid_to','discount','active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to': DateInput(),
        }

# this is for the type setting to date in forms
class DateOnlyInput(forms.DateInput):
    input_type = 'date'


# this is for the ProductOfferForm
class ProductOfferForm(ModelForm):
    class Meta:
        model = ProductOffer
        fields = '__all__'
        widgets = {
            'valid_from': DateOnlyInput(),
            'valid_to': DateOnlyInput(),
        }

# this is for the categoryOfferForm
class CategoryOfferForm(ModelForm):
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        widgets = {
            'valid_from': DateOnlyInput(),
            'valid_to': DateOnlyInput(),
        }
    
# this is for the django filtering for admin report


class OrderFilter(django_filters.FilterSet):
    
    # status = django_filters.CharFilter(field_name='payment__status',lookup_expr='iexact',label='Whatever you want')
    methods = django_filters.CharFilter(field_name='payment__payment_method',lookup_expr='icontains',label='Payment Methods')
    product__product_name = django_filters.CharFilter(field_name='product__product_name',lookup_expr='icontains',label='Product Name')
    product__category__category_name = django_filters.CharFilter(field_name='product__category__category_name',lookup_expr='icontains',label='Category Name')
  
    product_price__lt = django_filters.NumberFilter(field_name='product_price', lookup_expr='lt',label='Price Lessthan')
    product_price__gt = django_filters.NumberFilter(field_name='product_price', lookup_expr='gt',label='Price Greaterthan')

    # created_at__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='date__gt')
    # created_at__lt = django_filters.NumberFilter(field_name='created_at', lookup_expr='date__lt')

    # created_at = django_filters.NumberFilter(field_name='created_at', lookup_expr='month')


    # this is for the year 
    release_year = django_filters.NumberFilter(field_name='created_at', lookup_expr='year',label='Year')
    release_year__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__gt',label='Greater Than Year')
    release_year__lt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__lt',label='Less Than Year')

    # this is for the date checking
    created_at = django_filters.DateFilter(
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),lookup_expr='date',label='Date Wise'
    )
    created_at__gt = django_filters.DateFilter(field_name='created_at',        
                                                widget=DateInput(attrs={
                                                                        'type': 'date',
                                                                    }),lookup_expr='date__gt',label='Date Greater Than')
    created_at__lt = django_filters.DateFilter(field_name='created_at',widget=DateInput(attrs={
                                                                        'type': 'date',
                                                                    }),lookup_expr='date__lt',label = 'Date Less Than')

    # # crated_month = django_filters.CharFilter(field_name='created_at',widget=DateInput(attrs={
    #                                                                     'type': 'year',
    #                                                                 }),lookup_expr='contains',)



    # created_at__lt= django_filters.DateFromToRangeFilter()

    class Meta:
        model = OrderProduct
        fields = ['payment__status','product__category',]


                