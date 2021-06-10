from product.models import Cart, Gallery, Product, ProductCart
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError
from product.serializers import CartSerializer, CreateProductSerializer, GallerySerializer, ProductSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from user.permissions import IsActive, IsStaffOrReadOnly
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

class Products(APIView):

    permission_classes = [IsStaffOrReadOnly]
    
    def get(self, request):
        products = [product for product in Product.objects.all()]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'detail': 'Product successfully created',
                    'id': serializer.data['id'],
                    'slug': serializer.data['slug']
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeaturedProducts(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = [product for product in Product.objects.filter(is_featured=True)]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):

    permission_classes = [IsStaffOrReadOnly]

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, slug):
        product = self.get_object(slug)
        try:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        product = self.get_object(slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GalleryList(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: GallerySerializer(),
            204: 'No gallery results found'
        }
    )
    def get(self, request):
        """
        Gallery

        Return all available gallery image.
        You can set a GET parameter to filter the result.

        GET parameter list:<br>
        **featured**: If set to 'true' will only return featured product's gallery<br>
        **product_slug**: Will only return product's gallery with mentioned slug
        """
        gallery = Gallery.objects.all().order_by('product')

        if request.GET.get('featured') == 'true':
            gallery = gallery.filter(product__is_featured=True)

        if request.GET.get('product_slug'):
            gallery = gallery.filter(product__slug=request.GET.get('product_slug'))
        
        if not gallery:
            """
            Return early with no content (204) if no queryset found
            """
            return Response(status=status.HTTP_204_NO_CONTENT)

        serialize = GallerySerializer(gallery, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)

class Carts(APIView):
    """
    Cart List

    Return a list of user's cart if request is authenticated
    else return 401 code.
    """

    permission_classes = [IsActive]

    @swagger_auto_schema(
        responses={
            200: CartSerializer(),
            401: 'Invalid user\'s credential'
        }
    )
    def get(self, request):
        user = request.user
        carts = [cart for cart in Cart.objects.filter(user__username=user)]
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class CartItem(APIView):
    permission_classes = [IsActive]

    @swagger_auto_schema(
        responses={
            200: CartSerializer(),
            400: 'Invalid size parameter',
            404: 'Can\'t find product with that slug'
        }
    )
    def post(self, request, slug, size):
        """
        Add To Cart

        Appending new product to user's active cart,
        will create a new cart if no active cart exists.
        Will increase the quantity if the product with that size
        already exists on the user's cart.
        
        Allowed size parameters value are: 'S', 'M', 'L' either upper or lowercase
        """
        
        product = get_object_or_404(Product, slug=slug)
        if size.upper() not in ['S', 'M', 'L']:
            return Response(
                {
                    'details': 'Size parameter only accept S, M, or L either uppercase or lowercase'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        product_cart, created = ProductCart.objects.get_or_create(user=request.user, product=product, checked_out=False, size=size.upper())
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: CartSerializer(),
            400: 'Invalid size parameter',
            404: 'There is no product with that slug on the cart',
        }
    )
    def delete(self, request, slug, size):
        """
        Remove From Cart

        Removing product from user's active cart,
        will create a new cart if no active cart exists.
        Will decrease the quantity if the product with that size
        have more than 1 quantity on the cart.
        
        Allowed size parameters value are: 'S', 'M', 'L' either upper or lowercase
        """

        user = request.user

        try:
            cart = Cart.objects.get(user=user, checked_out=False)
            if size.upper() not in ['S', 'M', 'L']: raise ValueError
            product_cart = ProductCart.objects.get(product__slug=slug, user=user, size=size, checked_out=False)
        except (Cart.DoesNotExist, ProductCart.DoesNotExist) as e:
            if e == Cart.DoesNotExist:
                Cart.objects.create(user=user)
            return Response(
                {
                    'detail': f'Trying to remove non existing product from {user.username} cart'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {
                    'details': 'Size parameter only accept S, M, or L either uppercase or lowercase'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

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
    """
    Cart Checkout

    Dummy checkout API.
    No payment gateway implemented.
    Expecting to use midtrans.
    """
    permission_classes = [IsActive]

    def get_cart(self, request):
        try:
            return Cart.objects.get(user=request.user, checked_out=False)
        except Cart.DoesNotExist:
            raise ParseError('User current cart is empty')

    def post(self, request):
        cart = self.get_cart(request)
        cart.checked_out = True

        for product in cart.products.all():
            product.checked_out = True
            product.save()

        cart.save()
        serialize = CartSerializer(cart)
        return Response(serialize.data)