from django.contrib import admin
from . models import ShippingAdrress,Order,OrderItems,Invoice
# Register your models here.

admin.site.register(ShippingAdrress)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(OrderItems)

class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]


admin.site.unregister(Order)

admin.site.register(Order,OrderAdmin)

