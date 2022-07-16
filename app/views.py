from django.shortcuts import render
# from .models import Customer,Product,Cart,OrderPlaced
from .models import *
from django.views import View
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
class ProductView(View):
 def get(self, request):
    #  Filtering products to home page  by categrty and subcategory
     sherwani=Product.objects.filter(category='SH')
     suits=Product.objects.filter(category='S')
     bottomwears=Product.objects.filter(category='BW')
     return render(request, 'app/home.html',
                   {'sherwani':sherwani,'bottomwears':bottomwears,'suits':suits})
 
class ProductDetailsVeiw(View):
   def get(self,request,pk):
      product=Product.objects.get(pk=pk)
      return render(request, 'app/productdetail.html',{'product':product})

class ProfileView(View):
 def get(self, request):
    form=CustomerProfileForm()
    return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
 def post(self,request):
    form=CustomerProfileForm(request.POST)
    if form.is_valid():
       usr=request.user
       name=form.cleaned_data['name']
       locality=form.cleaned_data['locality']
       city=form.cleaned_data['city']
       state=form.cleaned_data['state']
       zipcode=form.cleaned_data['zipcode']
       reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
       reg.save()
       messages.success(request,'Profile Updated Successfully')
    return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
   
def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
   add=Customer.objects.filter(user=request.user)
   return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def sherwanis(request,data=None):
   if data==None :
      sherwani=Product.objects.filter(category='SH')
   elif data== 'Manyavar' or data=='Samyakk':
      sherwani=Product.objects.filter(category='SH').filter(brand=data)
   return render(request, 'app/sherwani.html',{'sherwani':sherwani})
class CustomerRegistrationView(View):
   def get(self,request):
      form=CustomerRegistrationForm()
      return render(request, 'app/customerregistration.html',{'form':form})
   def post(self,request):
      form=CustomerRegistrationForm(request.POST)
      if form.is_valid():
         messages.success(request, 'Registration Successful')
         form.save()
         # return render(request, 'app/login.html')
      return render(request, 'app/customerregistration.html',{'form':form}) 
   
   
   
def checkout(request):
 return render(request, 'app/checkout.html')

