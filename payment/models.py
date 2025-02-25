from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime
import secrets
from . paystack import Paystack
# Create your models here.
CustomUser = User

class ShippingAdrress(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True,blank=True)
    full_name = models.CharField(max_length=200)
    email =  models.CharField(max_length=60, blank=True)
    phone_number =  models.CharField(max_length=20, blank=True)
    address1 =  models.CharField(max_length=200, blank=True)
    address2 =  models.CharField(max_length=200, blank=True)
    town =  models.CharField(max_length=200, blank=True, null=True)
    region =  models.CharField(max_length=200, blank=True)
    
    def __str__(self) -> str:
        return f'Shipping Address - {str(self.id)}'

def create_shipping(sender,instance,created,**kwargs):
    if created:

        pro = ShippingAdrress(user=instance)
        pro.save()
post_save.connect(create_shipping,sender=User)

class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True,blank=True)
    full_name = models.CharField(max_length=100)
    email =  models.EmailField( max_length=254)
    shipping_address =  models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True,null=True)
    
    
    
    def __str__(self) -> str:
        return f'oder - {str(self.id)}'

#Auto add shipping dar
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now




class OrderItems(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True,blank=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'order Item - {str(self.id)}'
    
    def save(self, *args, **kwargs):
        if self.product.is_sale:
           self.price = self.product.sale_price
        else:
            self.price = self.product.price

        super().save(*args, **kwargs) # Call the real save() method


## payment view

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,blank=True)
    amount = models.PositiveIntegerField()
    ref  = models.CharField(max_length=255)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.user

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            similar_ref = Payment.objects.filter(ref=ref)
            if not similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)


    def amount_value(self):
        return int(self.amount) * 100
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)

        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
                self.save()

            if self.verified:
                return True
            else:
                return False
            

class Invoice(models.Model):
    ref = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)