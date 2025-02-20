"""
URL configuration for ECOM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path,include # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
### sitemaps
from django.contrib.sitemaps.views import sitemap
from store.sitemaps import *
from django.views.generic.base import TemplateView
sitemaps = {
    'static':StaticSitemap,
    'categories':CategorySitemap,
    'products':ProductSitemap
}


urlpatterns = [
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/',TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    path('admin/', admin.site.urls),
    path("",include('store.urls')),
    path("cart/",include('cart.urls')),
    path("payment/",include('payment.urls')),
    path('accounts/',include('allauth.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)