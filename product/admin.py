from django.contrib import admin
from .models import Product, Category, ProductCart, Cart

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)