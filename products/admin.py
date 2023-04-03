from django.contrib import admin
from .models import Category, Gender, Product, Cart, Sizes, Order, PaymentOrder

admin.site.register(Category)
admin.site.register(Gender)
admin.site.register(Sizes)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(PaymentOrder)
