from user.serializers import SimpleUserSerializer
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from rest_framework import serializers
from product.models import Gallery, Product, Review, SIZE_CHOICES, Category
from drf_yasg.utils import swagger_serializer_method

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id')

class GallerySerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(source='product__slug', allow_blank=True, required=False)
    type = serializers.CharField(source='get_image_type_display', allow_blank=True, required=False)
    type_code = serializers.CharField(source='image_type', allow_blank=True, required=False)
    
    class Meta:
        model = Gallery
        fields = ('image', 'width', 'height', 'product_slug', 'type', 'type_code')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
    
    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.add(*categories)
        return product

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    gallery = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=GallerySerializer(many=True))
    def get_gallery(self, product):
        qs = Gallery.objects.filter(product=product).exclude(image_type='M')
        return GallerySerializer(instance=qs, many=True).data

    @swagger_serializer_method(serializer_or_field=GallerySerializer(many=True))
    def get_model(self, product):
        qs = Gallery.objects.filter(image_type='M', product=product)
        return GallerySerializer(instance=qs, many=True).data

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'material', 'rating', 'is_featured', 'category', 'model', 'gallery')

class SimpleProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'rating')
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'review')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=SimpleUserSerializer)
    def get_user(self, review):
        user = get_user_model().objects.get(id=review.user.id)
        return {'username': user.username, 'email': user.email}

    @swagger_serializer_method(serializer_or_field=SimpleProductSerializer)
    def get_product(self, review):
        product = Product.objects.get(id=review.product.id)
        return SimpleProductSerializer(instance=product).data

    class Meta:
        model = Review
        fields = ('user', 'product', 'rating', 'review')

class SimpleReviewSerializer(ReviewSerializer):
    class Meta:
        model = Review
        fields = ('user', 'rating', 'review')

class ProductReviewSerializer(ProductSerializer):
    review = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=SimpleReviewSerializer(many=True))
    def get_review(self, product):
        qs = Review.objects.filter(product=product)
        return SimpleReviewSerializer(instance=qs, many=True).data

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'material', 'rating', 'is_featured', 'category', 'model', 'gallery', 'review')
