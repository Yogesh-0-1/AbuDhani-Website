from django.shortcuts import render
from .models import *
from django.views import View

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
 def get(self, request):
    #  Filtering products to home page  by categrty and subcategory
     sherwani=Product.objects.filter(category='SH')
     suits=Product.objects.filter(category='S')
     bottomwears=Product.objects.filter(category='BW')
     return render(request, 'app/home.html',
                   {'sherwani':sherwani,'bottomwears':bottomwears,'suits':suits})
 
 
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
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

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')
