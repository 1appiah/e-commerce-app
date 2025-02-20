from django import forms
from . models import Profile


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['phone','address1','address2','city','state','zipcode','country']

