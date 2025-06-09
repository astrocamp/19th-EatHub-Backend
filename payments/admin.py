from django.contrib import admin

from .models import PaymentOrder, Product, Subscription

# Register your models here.
admin.site.register(Product)
admin.site.register(PaymentOrder)
admin.site.register(Subscription)
