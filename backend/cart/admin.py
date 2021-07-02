from django.contrib import admin
from cart.models import Cart, ProductCart

@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    readonly_fields = ('subtotal',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)