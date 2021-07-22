from product.models import Product
from cart.serializers import CartSerializer
from django.contrib.auth import get_user_model
from cart.models import Cart
from rest_framework.test import APIClient
from rest_framework import status

from Virtuele.helpers import VirtueleTestBase

class CartCRUD(VirtueleTestBase):
    def setUp(self):
        self.product_factory(n=5)
        self.account_factory(n=3)
        self.client = APIClient()

    def test_get_all_carts(self):
        user = get_user_model().objects.get(id=1)
        carts = CartSerializer(Cart.objects.filter(user=user), many=True)

        response = self.client.get('/api/v1/carts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/api/v1/carts/', **self.account_jwt(1))
        if carts.data == []:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        else:
            self.assertEqual(response.data, carts.data)

    def test_add_item_to_a_cart(self):
        user = get_user_model().objects.get(id=1)
        product = Product.objects.get(id=1)
        product_2 = Product.objects.get(id=2)

        response = self.client.post(f'/api/v1/carts/items/{product.slug}/S/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(f'/api/v1/carts/items/invalidslug/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f'/api/v1/carts/items/{product.slug}/XXX/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CartSerializer(Cart.objects.get(user=user, checked_out=False)).data)

        response = self.client.post(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CartSerializer(Cart.objects.get(user=user, checked_out=False)).data)

        response = self.client.post(f'/api/v1/carts/items/{product_2.slug}/M/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CartSerializer(Cart.objects.get(user=user, checked_out=False)).data)

    def test_remove_item_from_a_cart(self):
        user = get_user_model().objects.get(id=1)
        product = Product.objects.get(id=1)
        self.client.post(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))

        response = self.client.delete(f'/api/v1/carts/items/{product.slug}/S/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(f'/api/v1/carts/items/invalidslug/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f'/api/v1/carts/items/{product.slug}/XXX/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CartSerializer(Cart.objects.get(user=user, checked_out=False)).data)

        response = self.client.delete(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_item_selected_status(self):
        product = Product.objects.get(id=1)

        # By default all newly created product cart will have its selected set to true
        response = self.client.post(f'/api/v1/carts/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.data['products'][0]['selected'], True)

        response = self.client.post(f'/api/v1/carts/toggle/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.data['products'][0]['selected'], False)

        response = self.client.post(f'/api/v1/carts/toggle/items/{product.slug}/S/', **self.account_jwt(1))
        self.assertEqual(response.data['products'][0]['selected'], True)
