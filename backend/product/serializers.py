from django.contrib.auth import get_user_model
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q
from rest_framework import serializers
from product.models import Cart, Gallery, Product, ProductCart, Review, SIZE_CHOICES, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id')

class GallerySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    type = serializers.CharField(source='get_image_type_display')
    type_code = serializers.CharField(source='image_type')
    
    class Meta:
        model = Gallery
        fields = ('image', 'width', 'height', 'product', 'type', 'type_code')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    gallery = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()

    def get_gallery(self, product):
        qs = Gallery.objects.filter(product=product).exclude(image_type='M')
        return GallerySerializer(instance=qs, many=True).data

    def get_model(self, product):
        qs = Gallery.objects.filter(image_type='M', product=product)
        return GallerySerializer(instance=qs, many=True).data

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'material', 'rating', 'is_featured', 'category', 'model', 'gallery')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
    
    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.add(*categories)
        return product

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'review')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    def get_user(self, review):
        user = get_user_model().objects.get(id=review.user.id)
        return {'username': user.username, 'email': user.email}

    def get_product(self, review):
        product = Product.objects.get(id=review.product.id)
        return {'name': product.name, 'slug': product.slug, 'rating':product.rating}

    class Meta:
        model = Review
        fields = ('user', 'product', 'rating', 'review')

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
