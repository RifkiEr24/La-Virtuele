from django.contrib import admin
from .models import Gallery, Product, Review, Category, ProductCart, Cart

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'is_featured', 'rating')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'date')
    list_filter = ('user', 'product')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    readonly_fields = ('width', 'height')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    readonly_fields = ('subtotal',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('total',)