import decimal
from django.shortcuts import render,redirect,get_object_or_404
from cart.cart import Cart
from . models import ShippingAdrress,Order,OrderItems
from .forms import shippingForm
from django.contrib import messages
from store.models import Product
from payment.models import Payment,Invoice
from django.conf import settings
# Create your views here.

def payment_success(request):
    return render(request,'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    total = cart.total
    quan = cart.get_quants
    customer = request.user
    products = cart.get_prods
    if customer.is_authenticated:
        billing_address = ShippingAdrress.objects.get(user__id=customer.id)
        shipform = shippingForm(request.POST or None,instance=billing_address)
        context = {
            'products':products,
            'shipform':shipform,
            'quan':quan,
            'total':total
        }
        return render(request,'payment/checkout.html',context)
    else:
        shipform = shippingForm(request.POST or None)
        context = {
            'products':products,
            'shipform':shipform,
            'quan':quan,
            'total':total
        }
        return render(request,'payment/checkout.html',context)

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        total = cart.total
        quan = cart.get_quants
        customer = request.user
        products = cart.get_prods

        #create a session with shipping info 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        shipinfo = request.POST 
    
        context = {
                    'products':products,
                    'shipinfo':shipinfo,
                    'quan':quan,
                    'total':total,
        
                }
        if customer.is_authenticated:
        
            return render(request,'payment/billing_info.html',context)
        else:
            return render(request,'payment/billing_info.html',context)
            
    
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    

def process_order(request):
    
    if request.POST:
        cart = Cart(request)
        total = cart.total
        quan = cart.get_quants
        customer = request.user
        products = cart.get_prods
        # get billing info from last page
        my_shipping = request.session.get('my_shipping')

        # gatther order info
        full_name = my_shipping['full_name']
        email = my_shipping['email']
        amount_paid = total()
        amount_paid = decimal.Decimal(amount_paid)
        # get address from my_shipping session
        shipping_address = f"{my_shipping['full_name']}\n{my_shipping['address1']}\n{my_shipping['address2']}\n{my_shipping['state']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"

        #create order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(full_name = full_name,email=email,amount_paid=amount_paid,user=user,shipping_address=shipping_address)
            create_order.save()
            request.session['order'] = create_order.pk
            pk = settings.PAYSTACK_PUBLIC_KEY
            #amount = 20
            payment = Payment.objects.create(amount=amount_paid,email=email,user=user)

            # add order items
            order_id = create_order.id
            user = user
            # get all product ids
            for product in products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quan().items():
                    if int(key) == product_id:
                        product_qty = value
                        create_items = OrderItems(order=create_order,product=product,user=user,quantity=product_qty,price=price)
                        create_items.save()
                cart.delete(product=product_id)
            for car in list(request.session.keys()):
                if car == "session_key":
                    del request.session[car]
            messages.success(request,"Order placed")
            context = {
                'payment':payment,
                'paystack_pub_key':pk,
                'amount_value':payment.amount_value(),
                'amount':amount_paid,
                'create_order':create_order
            }
            return render(request,'payment/make_payment.html',context)

        else:
            create_order = Order(full_name = full_name,email=email,amount_paid=amount_paid,shipping_address=shipping_address)
            create_order.save()
            request.session['order'] = create_order.pk
            pk = settings.PAYSTACK_PUBLIC_KEY
            #amount = 20
            payment = Payment.objects.create(amount=amount_paid,email=email,user=user)
            #add other items
            order_id = create_order.id
            
            # get all product ids
            for product in products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quan().items():
                    if int(key) == product_id:
                        product_qty = value
                        create_items = OrderItems(order=create_order,product=product,quantity=product_qty,price=price)
                        create_items.save()
                cart.delete(product=product_id)

            # delete our cart
            for car in list(request.session.keys()):
                if car == "session_key":
                    del request.session[car]
            messages.success(request,"Order placed")
            context = {
                'payment':payment,
                'paystack_pub_key':pk,
                'amount_value':payment.amount_value(),
                'amount':amount_paid,
                'create_order':create_order
            }
            return render(request,'payment/make_payment.html',context)


    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    


def verify_payment(request,ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        obj = Order.objects.get(pk=request.session['order'])
        obj.is_verified = True
        obj.save()
        invoice = Invoice(ref=ref,order_id=obj.pk,amount=obj.amount_paid)
        invoice.name = request.user.user.shippingaddress_set.full_name
        invoice.save()

        messages.success(request,"Payment Verified. A Dispatch rider is coming soon")
        return redirect('home')
    else:
        messages.warning(request,"Something went wrong with your payment")


#def pay_on_delivery(request,pk):
#    delivery = get_object_or_404(Order,pk=pk)
#    delivery.pay_on_delivery = True
#    delivery.save()
#    messages.success(request,"Dispatch rider is coming soon, remember to pay on pickup/delivery")
#    return redirect('dashboard')




### create a system where someone can send an order to someone to pay for them



### a notification when an order has been delivered or a product has been ordered.








def ship_dash(request):
    shipped_orders = Order.objects.filter(shipped=True)
    context = {
        'shipped_orders':shipped_orders
    }
    return render(request,'payment/ship_dash.html',context)

def not_ship_dash(request):
    unshipped_orders = Order.objects.filter(shipped=False)
    context = {
        'unshipped_orders':unshipped_orders
    }
    return render(request,'payment/not_shipped.html',context)

def order_detail(request,pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItems.objects.filter(order=order)
    context = {
        'order':order,
        'order_items':order_items
    }
    return render(request,'payment/order_detail.html',context)


def toggleship(request,pk):
    if request.user.is_superuser:
        order = Order.objects.get(id=pk)
        if order.shipped:
            order.shipped = False
            order.save()
            return redirect('not-ship-dash')
        else:
            order.shipped = True
            order.save()
            return redirect('ship-dash')
    else:
        return redirect('home')
    


## paid others that has not been shipped

def paid_unshipped_orders(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(is_verified=True,shipped=False)
        return render(request,'payment/paid_unshipped_oders.html',{'orders':orders})