from rest_framework import serializers
from product.models import Cart, Gallery, Product, ProductCart, SIZE_CHOICES, Category

class MyPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        return str(value)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category',)

class GallerySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = Gallery
        fields = ('image', 'width', 'height', 'product')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    gallery = GallerySerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('__all__')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
    
    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.add(*categories)
        return product


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