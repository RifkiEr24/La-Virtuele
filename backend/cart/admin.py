from django.contrib import admin
from cart.models import Cart, ProductCart, Transaction

@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    readonly_fields = ('subtotal',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)

@admin.register(Transaction)
class OrderHistoryAdmin(admin.ModelAdmin):
    pass