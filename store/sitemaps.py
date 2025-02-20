from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . models import Category,Product
class StaticSitemap(Sitemap):
    def items(self):
        return['home','about','categories','wishlist']
    
    def location(self,item):
        return reverse(item)
    

class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()
    
class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
