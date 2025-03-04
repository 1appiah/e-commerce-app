from django.contrib import admin # type: ignore
from . models import Category,Product,Profile,Customer,WishList,Product_Reviews
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Product_Reviews)
admin.site.register(Profile)
admin.site.register(WishList)



