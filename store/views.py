from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,Category,Profile,WishList
from payment.models import ShippingAdrress
from payment.forms import shippingForm
from django.contrib import messages
from . forms import UserUpdateForm
from django.db.models import Q
import json

from cart.cart import Cart
import random
from django.http import HttpResponse


# Create your views here.

def home(request):
    if request.user.is_authenticated:
    #shopping stuff
        current_user =Profile.objects.get(user__id=request.user.id)
        # get saved cart from database
        saved_cart = current_user.old_cart
        # convert it to python dictionary
        if saved_cart:
            converted_cart = json.loads(saved_cart)
            # add loaded cart dictionary to session
            cart = Cart(request)
            # loop through the cart and add items from the database
            for key,value in converted_cart.items():
                cart.db_add(product=key,quantity=value)
    ## retrieve products based on catgories,best deals, best selling, just show about few and bring view more button
    kids = Product.objects.all().order_by('?')[:4]
    products = Product.objects.all().order_by('-id')[:4]

    
    return render(request,'store/home.html',{'products':products,'kids':kids})

def about(request):
    return render(request,'store/about.html',{})

## make product detail remarkable by adding related products from same category and styling it well.
def productDetail(request,pk):
    item = Product.objects.get(id=pk)
    category = Category.objects.get(name=item.category)
    related_products = Product.objects.filter(category=category).order_by('?')[:4]
    wishlist= WishList.objects.get(customer=request.user.id)
    if wishlist.products.contains(item):
        in_wishlist = True
    else:
        in_wishlist = False
    cart = Cart(request)
    cart_products = cart.get_prods()
    if item in cart_products:
        in_cart = True
    else:
        in_cart = False
        print('not in ooo')
    return render(request,'store/product-detail.html',{'item':item,'obj':related_products,'in_cart':in_cart,'in_wishlist':in_wishlist})

def category(request):
    categories = Category.objects.all()
    return render(request,'store/category.html',{'categories':categories})

def categoryDetails(request,pk):
    cats = Category.objects.get(id=pk)
    products = Product.objects.filter(category=cats)
    return render(request,'store/categoryDetail.html',{'cats':cats,'products':products})


### updating the profile of users -
def update_profile(request):
    pro = Profile.objects.get(user=request.user)
    ship =  ShippingAdrress.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=pro)
        if form.is_valid():
            form.save()
            return redirect('update-profile')
        else:
            return redirect('update-profile')
    else:
        form = UserUpdateForm(instance=pro)
        form1 = shippingForm(instance=ship)
    context = {
        'form':form,
        'pro':pro,
        'form1':form1
    }
    return render(request,'store/update_user.html',context)



### updating the profile of users --- shipping address
def update_shipping_address(request):
    pro = Profile.objects.get(user=request.user)
    ship =  ShippingAdrress.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        form1 = shippingForm(request.POST,instance=ship)
        if form1.is_valid():
            form1.save()
            return redirect('update-profile')
        else:
            return redirect('update-profile')
    else:
        return redirect('update-profile')

def search_product(request):
    if request.method == "POST":
        item = request.POST.get('item')
        if item != "":
            products = Product.objects.filter(Q(name__icontains=item) | Q(description__icontains=item) | Q(category__name__icontains=item))
            return render(request,'store/search_product.html',{'products':products})
        else:
            return render(request,'store/search_product.html')
    else:
        return render(request,'store/search_product.html')

### wishlistview

def wishlist(request):
    if request.user.is_authenticated:
        if request.POST:
            pk = request.POST.get('product_id')   
            product = Product.objects.get(pk=pk)
            if WishList.objects.get(customer = request.user):
                    wishlist = WishList.objects.get(customer = request.user)
                    if wishlist:
                        if wishlist.products.contains(product):
                            wishlist.products.remove(product)
                            product.in_wishlist = False
                            product.save()
                            messages.info(request,'product removed from wishlist')
                            return HttpResponse("done")
                        else:
                            wishlist.products.add(product)
                            #product.in_wishlist = True
                            #product.save()
                            messages.info(request,'product added to wishlist')
                            return HttpResponse("done")
            else:
                wishlist = WishList(products=product,customer=request.user)
                return HttpResponse("done")
            
        else:
            messages.info(request,'request is not post')
            return redirect('home')
                
    else:
        return redirect('home')
            
def view_wishlist(request):
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(customer=request.user)
        context = {
            'wishlist':wishlist
        }
        return render(request,'store/wishlist.html',context)
    else:
        return redirect('home')

### removing a product from wishlist

def remove_from_wishlist(request):
     if request.POST:
            pk = request.POST.get('product_id')   
            product = Product.objects.get(pk=pk)
            wishlist = WishList.objects.get(customer = request.user)
            wishlist.products.remove(product)
            #product.in_wishlist = False
            #product.save()
            messages.info(request,'product removed from wishlist')
            return HttpResponse("done")




### create a profile for the customer