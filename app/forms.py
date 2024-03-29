from tkinter import Widget
from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ , gettext  
from django.contrib.auth import password_validation
from .models import *
class CustomerRegistrationForm(UserCreationForm):
    
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password, 'align':'center', 'placeholder':'password'}),
    # )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}),
    )

    # password1: forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    # password2: forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    # username={'username':forms.TextInput(attrs={'class':'form-control'})}
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels={'email':'Email','username':'Username','password1':'Password','password2':'Confirm Password'}
        # widgets={'username':forms.TextInput(attrs={'class':'form-control'})}
    
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'})) 
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})) 
    
class MyPasswordChange(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1=forms.CharField(label=_("New password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_("New password confirmation"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))    
    
class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_("Email"),widget=forms.EmailInput(attrs={'autofocus':True,'autocomplete':'email','class':'form-control'}))
    
class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=_("New password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_("New password confirmation"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['name','locality','city','state','zipcode']
        Widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'locality':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'state':forms.Select(attrs={'class':'form-control'}),
                'zipcode':forms.NumberInput(attrs={'class':'form-control'})}