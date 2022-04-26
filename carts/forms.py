from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'class':'border-5 border-warning form-control bg-dark text-white p-4',
				   'placeholder':'Enter the Coupon Code'}),label='')


