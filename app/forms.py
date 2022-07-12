from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ , gettext  

class CustomerRegistrationForm(UserCreationForm):
    password1: forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')
    password2: forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label=' Confirm Password (again)')
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels={'email':'Email','username':'Username'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}
    
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'})) 
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})) 