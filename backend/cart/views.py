from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from user.permissions import IsActive
from cart.serializers import CartSerializer
from cart.models import Cart, ProductCart
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from product.models import Product

class Carts(APIView):
    """
    Cart List

    Return a list of user's cart if request is authenticated
    else return 401 code.<br>
    You can set a GET parameter to filter its result.<br>

    GET parameter list:
    **checked**: If set to 'true' will return only checked out cart,
    else if you set it to 'false' will return only non checked out cart (active cart)
    """

    permission_classes = [IsActive]

    @swagger_auto_schema(
        responses={
            200: CartSerializer(),
            204: 'No Result Found',
            401: 'Invalid User\'s Credential'
        }
    )
    def get(self, request):
        user = request.user
        cart_qs = Cart.objects.filter(user__username=user)
        cart_condition = None
        if request.GET.get('checked') == 'true':
            cart_condition = True
        elif request.GET.get('checked') == 'false':
            cart_condition = False

        cart_qs = cart_qs.filter(checked_out=cart_condition) if not cart_condition == None else cart_qs
        carts = [cart for cart in cart_qs]

        if not carts:
            # Return early with no content (204) if no queryset found
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class CartItem(APIView):
    permission_classes = [IsActive]

    @swagger_auto_schema(
        responses={
            200: CartSerializer(),
            400: 'Invalid Size Parameter',
            404: 'Can\'t Find Product With That Slug'
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
            400: 'Invalid Size Parameter',
            404: 'There Is No Product With That Slug On The Cart',
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
