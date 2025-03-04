from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from django.db.models.signals import post_save
# Create your models here.


class Category(models.Model):
    name  = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/categories-detail/{self.pk}>'
    

#### categories to be used-- ladies,gents, couples, mothers,fathers, surprises, birthday, special packages
## customer model

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    
### Product model

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.CASCADE,default = 0)
    description = models.CharField(max_length=250, blank=True,default="",null=True)
    image = models.ImageField( upload_to='uploads/product_image/')
    is_sale = models.BooleanField(default=False)
    #in_cart = models.BooleanField(default=False)
    #in_wishlist = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    ## others images to be viewed at detailed page
    ## product reviews by customers
    
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return f'/product/{self.pk}>'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone =  models.CharField(max_length=20, blank=True)
    address1 =  models.CharField(max_length=200, blank=True)
    address2 =  models.CharField(max_length=200, blank=True)
    state =  models.CharField(max_length=200, blank=True)
    city =  models.CharField(max_length=200, blank=True)
    zipcode =  models.CharField(max_length=200, blank=True)
    country =  models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self) -> str:
        return self.user.username

# create userprofile

def create_profile(sender,instance,created,**kwargs):
    if created:

        pro = Profile(user=instance)
        pro.save()
post_save.connect(create_profile,sender=User)




###  wishlist
class WishList(models.Model):
    products = models.ManyToManyField(Product,blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)



# create wishlist

def create_wishlist(sender,instance,created,**kwargs):
    if created:
        pro = WishList(customer=instance)
        pro.save()
post_save.connect(create_wishlist,sender=User)



class Product_Reviews(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    stars_rating = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    email = models.EmailField(blank=True,null=True)
    remain_stars =  models.PositiveIntegerField(blank=True,default=0)

    def save(self, *args, **kwargs):
       self.remain_stars = 5 - int(self.stars_rating)
       super().save(*args, **kwargs) # Call the real save() method