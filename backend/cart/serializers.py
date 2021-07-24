from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from cart.models import ProductCart, Cart
from product.serializers import ProductSerializer
from product.models import Product

class ProductCartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=ProductSerializer())
    def get_product(self, product_cart):
        qs = Product.objects.get(id=product_cart.product.id)
        return ProductSerializer(instance=qs, read_only=True).data

    class Meta:
        model = ProductCart
        fields = ('product', 'qty', 'size', 'selected', 'subtotal')

class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=ProductCartSerializer(many=True))
    def get_products(self, cart):
        qs = ProductCart.objects.filter(cart=cart)
        return ProductCartSerializer(instance=qs, read_only=True, many=True).data

    class Meta:
        model = Cart
        fields = ('id', 'user', 'products', 'checked_out', 'created', 'total')
