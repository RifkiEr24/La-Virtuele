from django.contrib.auth import get_user_model
from product.models import Product
from rest_framework.test import APIClient
from rest_framework import status

from Virtuele.helpers import VirtueleTestBase
from cart.models import Transaction

class GopayTest(VirtueleTestBase):      
    def setUp(self):
        self.user_admin_factory()
        self.client = APIClient()

    def add_product_to_users_cart(self, jwt):
        self.product_factory(n=2)
        products = Product.objects.all()

        for product in products:
            self.client.post(f'/api/v1/carts/items/{product.slug}/S/', **jwt)
            
    def create_new_transaction(self):
        # This function will be used a lot, so i dont think this need to be a test function
        self.add_product_to_users_cart(self.user_jwt)

        response = self.client.post('/api/v1/payments/gopay/charge/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/api/v1/payments/gopay/charge/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(Transaction.objects.get(order_id=response.data['order_id']), None)

        return response.data['order_id']

    def test_check_transaction_status(self):
        self.account_factory(1)
        order_id = self.create_new_transaction()
       
        response = self.client.get(f'/api/v1/payments/gopay/{order_id}/status/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_type'], 'gopay')
        
        response = self.client.get(f'/api/v1/payments/gopay/{order_id}/status/', **self.account_jwt(3))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'/api/v1/payments/gopay/{order_id}/status/', **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'/api/v1/payments/gopay/{order_id}/status/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f'/api/v1/payments/gopay/invalid_order_id/status/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_transaction(self):
        self.account_factory(1)
        order_id = self.create_new_transaction()

        response = self.client.post(f'/api/v1/payments/gopay/{order_id}/cancel/', **self.account_jwt(3))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(f'/api/v1/payments/gopay/{order_id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(f'/api/v1/payments/gopay/invalid_order_id/cancel/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f'/api/v1/payments/gopay/{order_id}/cancel/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_status'], 'cancel')
        self.assertEqual(Transaction.objects.get(order_id=order_id).transaction_status, 'cancel')

        order_id = self.create_new_transaction()
        response = self.client.post(f'/api/v1/payments/gopay/{order_id}/cancel/', **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_status'], 'cancel')
        self.assertEqual(Transaction.objects.get(order_id=order_id).transaction_status, 'cancel')
