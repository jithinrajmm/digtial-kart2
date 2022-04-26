
from accounts.models import Account #starting here
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import UserProfile,UserAddress
from PIL import Image
from django.core.files import File


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone','password1','password2']
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.HiddenInput())
    address_line_1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    address_line_2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    profile_pic = forms.ImageField(widget=forms.FileInput,)

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ['x','y','width','height','user','first_name','last_name','username','email','phone','address_line_1','address_line_2','country','state','city','profile_pic']

    def save(self):

        photo = super(UserProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_pic)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        print(resized_image,'resized_image')
        resized_image.save(photo.profile_pic.path)

            
        return photo

# user address form
class UserAddressForm(forms.ModelForm):

    address_line_1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    address_line_2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    
    class Meta:
        model = UserAddress
        fields = ['first_name','last_name','email','phone','address_line_1',
                   'address_line_2','country','state','city']