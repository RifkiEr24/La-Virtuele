from django.db.models import fields
from rest_framework import serializers
from product.models import Cart, Product, ProductCart, SIZE_CHOICES, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category',)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('__all__')

class ProductCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductCart
        fields = ('product', 'qty', 'size', 'total')

class CartSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ('__all__')