from django.shortcuts import render,redirect
from .models import *
from django.views import View
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django .views.decorators.csrf import csrf_exempt
from .PayTm import Checksum

# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'Your-Merchant-Key-Here'

class ProductView(View):
 def get(self, request):
    #  Filtering products to home page  by categrty and subcategory
     sherwani=Product.objects.filter(category='SH')
     suits=Product.objects.filter(category='S')
     bottomwears=Product.objects.filter(category='BW')
     totalitem=0
     if request.user.is_authenticated:
                 totalitem=len(Cart.objects.filter(user=request.user))
     return render(request, 'app/home.html',
                   {'sherwani':sherwani,'bottomwears':bottomwears,'suits':suits,'totalitem':totalitem})

class ProductDetailsVeiw(View):
   def get(self,request,pk):
             
          
          product=Product.objects.get(pk=pk)
          item_already_in_cart=False
          totalitem=0
          if request.user.is_authenticated:
                 totalitem=len(Cart.objects.filter(user=request.user))
                 item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()      
          return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


@method_decorator(login_required ,name="dispatch")
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
 
 
 
@login_required   
def add_to_cart(request):
       user=request.user
       product=request.GET.get('prod_id')
       product=Product.objects.get(id =product) 
       print(product)
       Cart(user=user,product=product).save()
       return redirect('/Cart')
    
    
    
@login_required
def show_cart(request):
       if request.user.is_authenticated:
              user=request.user
              cart=Cart.objects.filter(user=user)
              amount=0.0
              shiping_amount=45.00
              total=0.0
              cart_product=[p for p in Cart.objects.all() if p.user==user  ]
              
              if cart_product:
                     for p in cart_product:
                            tempamount=(p.quantity * p.product.discounted_price)
                            amount += tempamount
                            totalamount= shiping_amount + amount
                     return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount , 'amount':amount})
              else:
                 return render(request, 'app/emptycart.html') 


       
def plus_cart(request):
          if request.method=='GET':
                 prod_id=request.GET['prod_id']
                 c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
                 c.quantity+=1
                 c.save()
                 user=request.user
                 amount=0.0
                 shiping_amount=45.00
                 total=0.0
                 cart_product=[p for p in Cart.objects.all() if p.user==user  ]
              
                 if cart_product:
                     for p in cart_product:
                            tempamount=(p.quantity * p.product.discounted_price)
                            amount += tempamount
                            
                     data={
                              'quantity': c.quantity,
                              'totalamount':amount+shiping_amount,   
                              'amount':amount
                            }
                     return JsonResponse(data)


def minus_cart(request):
          if request.method=='GET':
                 prod_id=request.GET['prod_id']
                 c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
                 c.quantity-=1
                 c.save()
                 user=request.user
                 amount=0.0
                 shiping_amount=45.00
                 total=0.0
                 cart_product=[p for p in Cart.objects.all() if p.user==user  ]
              
                 if cart_product:
                     for p in cart_product:
                            tempamount=(p.quantity * p.product.discounted_price)
                            amount += tempamount
                            
                     data={
                              'quantity': c.quantity,
                             'totalamount':amount+shiping_amount, 
                              'amount':amount
                            }
                     return JsonResponse(data)
  
                  
def remove_cart(request):
       
          if request.method=='GET':
                 prod_id=request.GET['prod_id']
                 c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
                 
                 c.delete()
                 user=request.user
                 amount=0.0
                 shiping_amount=45.00
                 total=0.0
                 cart_product=[p for p in Cart.objects.all() if p.user==user  ]
              
                 if cart_product:
                     for p in cart_product:
                            tempamount=(p.quantity * p.product.discounted_price)
                            amount += tempamount
                            
                     data={
                              'totalamount':amount+shiping_amount, 
                              'amount':amount
                              
                            }
                     return JsonResponse(data)
                  
                  
@login_required
def buy_now(request):      
 return render(request, 'app/buynow.html')


@login_required
def address(request):
   add=Customer.objects.filter(user=request.user)
   return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})



@login_required
def orders(request):
       op=OrderPlaced.objects.filter(user=request.user)
       return render(request, 'app/orders.html',{'order_place': op})
    
    
    
@login_required
def sherwani(request,data=None):
   if data==None :
      sherwanis=Product.objects.filter(category='SH')
   elif data== 'Manyavar' or data=='Samyakk':
      sherwanis=Product.objects.filter(category='SH').filter(brand=data)
   return render(request, 'app/sherwani.html',{'sherwani':sherwanis})



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
   
   
   
@login_required
def checkout(request):
       user=request.user
       add=Customer.objects.filter(user=user )
       cart_items=Cart.objects.filter(user=user)
       amount=0.0
       shiping_amount=45.00
       total=0.0
       cart_product=[p for p in Cart.objects.all() if p.user==user  ]
              
       if cart_product:
          for p in cart_product:
                   tempamount=(p.quantity * p.product.discounted_price)
                   amount += tempamount
          total_amount=amount+shiping_amount
       # param_dict={
       #      'MID': 'rqrfsb40106025550938',
       #      'ORDER_ID': 'OrderPlaced.id',
       #      'TXN_AMOUNT': str(amount),
       #      'CUST_ID': 'email',
       #      'INDUSTRY_TYPE_ID': 'Retail',
       #      'WEBSITE': 'WEBSTAGING',
       #      'CHANNEL_ID': 'WEB',
       #      'CALLBACK_URL':'http://127.0.0.1:8000/app/handlerequest/',}
       # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
       # return  render(request, 'app/paytm.html', {'param_dict': param_dict})
       # return  render(request, 'app/paytm.html')
       
       return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})
    
    
    
@login_required
def payment_done(request):
       user=request.user
       custid=request.GET.get('custid')
       customer=Customer.objects.get(id= custid)
       cart=Cart.objects.filter(user=user)
       for c in cart:
              OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
              c.delete() 
       return redirect("orders")

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'app/paymentstatus.html', {'response': response_dict})
              
