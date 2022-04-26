from django import forms
from orders.models import Order
from django.db.models.fields import BLANK_CHOICE_DASH

class OrderFormEdit(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status',]

class OrderForm(forms.ModelForm):
    address_line_1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    address_line_2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    


    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','order_note']



# this form is used to apply coupon










