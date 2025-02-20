from django import forms
from .models import ShippingAdrress

class shippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAdrress
        fields = ['full_name','email','phone_number','address1','address2','city','state','zipcode','country']

        exclude = ['user',]
        
    

