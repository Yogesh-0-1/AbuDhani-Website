from django.shortcuts import render
# from .models import Customer,Product,Cart,OrderPlaced
from .models import *
from django.views import View
from .forms import CustomerRegistrationForm
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
   
def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def sherwanis(request,data=None):
   if data==None :
      sherwani=Product.objects.filter(category='SH')
   elif data== 'Manyavar' or data=='Samyakk':
      sherwani=Product.objects.filter(category='SH').filter(brand=data)
   return render(request, 'app/sherwani.html',{'sherwani':sherwani})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
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

