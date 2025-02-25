from django.urls import path 
from . import views
urlpatterns = [
    path('payment-success/<str:ref>',views.payment_success,name='payment-success'),
    path('checkout/',views.checkout,name='checkout'),
    path('billing_info/',views.billing_info,name='billing_info'),
    path('process-order/',views.process_order,name='process-order'),
    path('verify-payment/<str:ref>',views.verify_payment,name="verify-payment"),
    path('not-ship-dash/',views.not_ship_dash,name='not-ship-dash'),
    path('ship-dash/',views.ship_dash,name='ship-dash'),
    path('order-detail/<int:pk>',views.order_detail,name='order-detail'),
    path('toggleship/<int:pk>',views.toggleship,name='toggleship'),
    path('paid-unshipped-orders',views.paid_unshipped_orders,name='paid-unshipped-orders'),
    path('invoice/<str:ref>',views.invoice,name='invoice'),
    

]
