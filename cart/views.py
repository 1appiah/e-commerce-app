from django.shortcuts import render,get_object_or_404 # type: ignore
from store.models import Product
from django.http import JsonResponse # type: ignore
from . cart import Cart
from django.contrib import messages


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    total = cart.total
    return render(request,'cart/cart_summary.html',{'cart_products':cart_products,'quantities':quantities,'total':total})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')

        product = Product.objects.get(id=product_id)
        product.in_cart = True
        product.save()
        cart.add(product=product,quantity=product_qty)
        #Get Cart Quantity
        cart_quantity = cart.__len__()
        #response = JsonResponse({"Product Name":product.name})
        response = JsonResponse({"qty":cart_quantity})
        messages.success(request,"Product added to cart...")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id,quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request,"Cart updated...")
        return response

    

def cart_delete(request):
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id')) 
            product = Product.objects.get(id=product_id)
            product.in_cart = False
            product.save()
            
            cart.delete(product=product_id)
            response = JsonResponse({'del':'del'})
            messages.success(request,"item deleted from cart...")
            return response
