from django.http.response import JsonResponse
from product.models import Cart, Gallery, Product, ProductCart
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework import authentication, permissions
from product.serializers import CartSerializer, GallerySerializer, ProductSerializer
from rest_framework import status
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Products(APIView):
    def get(self, request):
        products = [product for product in Product.objects.all()]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeaturedProducts(APIView):
    def get(self, request):
        products = [product for product in Product.objects.filter(is_featured=True)]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        product = self.get_object(slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GalleryList(APIView):
    def get(self, request):
        gallery = Gallery.objects.all().order_by('product')
        serialize = GallerySerializer(gallery, many=True)
        return Response(serialize.data)

class Carts(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'Login Required': 'API call is failed as client are not logged in'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        carts = [cart for cart in Cart.objects.filter(user__username=user)]
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class AddToCart(APIView):
    def post(self, request, slug, size):
        if not request.user.is_authenticated:
            return Response({'Login Required': 'API call is failed as client are not logged in'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product = get_object_or_404(Product, slug=slug)
        product_cart, created = ProductCart.objects.get_or_create(user=request.user, product=product, checked_out=False, size=size)
        cart_qs = Cart.objects.filter(user=request.user, checked_out=False)

        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.products.filter(product__slug=product.slug, size=size).exists():
                product_cart.qty += 1
                product_cart.save()
            else:
                cart.products.add(product_cart)
        else:
            cart = Cart.objects.create(user=request.user)
            cart.products.add(product_cart)
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class RemoveFromCart(APIView):
    def get_product(self, request, slug, size):
        try:
            return ProductCart.objects.get(product__slug=slug, user=request.user, size=size, checked_out=False)
        except ProductCart.DoesNotExist:
            raise ParseError('Product did not exists in cart')

    def post(self, request, slug, size):
        if not request.user.is_authenticated:
            return Response({'Login Required': 'API call is failed as client are not logged in'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product_cart = self.get_product(request, slug, size)
        cart = Cart.objects.get(user=request.user, checked_out=False)
        if product_cart.qty > 1:
            product_cart.qty -= 1
            product_cart.save()
        else:
            cart.products.remove(product_cart)
            product_cart.delete()
            cart.save()

        serialize = CartSerializer(cart)
        return Response(serialize.data)


class Checkout(APIView):
    def get_cart(self, request):
        try:
            return Cart.objects.get(user=request.user, checked_out=False)
        except Cart.DoesNotExist:
            raise ParseError('User current cart is empty')

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'Login Required': 'API call is failed as client are not logged in'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        cart = self.get_cart(request)
        cart.checked_out = True

        for product in cart.products.all():
            product.checked_out = True
            product.save()

        cart.save()
        serialize = CartSerializer(cart)
        return Response(serialize.data)