from django.urls import path # type: ignore
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),

    
    #path('register/', views.register, name='register'),
    ##path('login/', login.as_view(), name='login'),
    #path('login/', LoginView.as_view(template_name ='registration/login.html'), name='login'),
    #path('logout/', LogoutView.as_view(template_name ='registration/logout.html'), name='logout'),
    path('product/<int:pk>',views.productDetail,name='product-detail'),
    path('categories/',views.category,name='categories'),
    path('categories-detail/<int:pk>',views.categoryDetails,name='categories-detail'),

    # profile page
    path('update-profile/',views.update_profile,name='update-profile'),
    path('update-shipping-address',views.update_shipping_address,name='update-shipping-address'),

    # search product
    path('search-product',views.search_product,name='search-product'),
    ## product reviews
    path('product-reviews/<int:pk>',views.product_reviews,name='product-reviews'),

    ##wishlist
    path('wishlist',views.wishlist,name='wishlist'),
    path('view-wishlist',views.view_wishlist,name='view-wishlist'),
    path('remove-from-wishlist',views.remove_from_wishlist,name='remove-from-wishlist'),


    ### to handle referral codes
    path('referral-view/',views.referral_view,name='referral-view'),
    path('referral-view/<str:ref_code>/',views.referral_view,name='referral-view'),
    path('save-referral-code',views.save_referral_code,name="save_referral_code")
]
