from rest_framework import serializers
from cart.models import ProductCart, Cart
from product.serializers import ProductSerializer

class ProductCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductCart
        fields = ('product', 'qty', 'size', 'subtotal')

class CartSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ('__all__')
