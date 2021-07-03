import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.models import Category, Product
from product.serializers import ProductSerializer
from Virtuele.helpers import VirtueleTestBase

class ProductCRUD(VirtueleTestBase):
    def setUp(self):
        for i in range (10):
            Product.objects.create( name=f'Product Test {i}',
                                    description=f'This is just a sample {i}.',
                                    price=int(f'{i}00000'),
                                    material='Cotton Candy')
        Category.objects.create(name='Cotton 200gsm')

        self.valid_payload = {
            'name': 'Collapse',
            'description': 'Collapse your soul',
            'category': [1],
            'price': 200000,
            'material': 'Cotton 200gsm'
        }

        self.invalid_payload = {
            'name': '',
            'description': 'Collapse your soul',
            'category': [1],
            'price': 200000,
            'material': 'Cotton 200gsm'
        }
        
        self.user_admin_factory()
        self.client = APIClient()

    def test_get_all_products(self):
        response = self.client.get(reverse('product-list'))
        products = ProductSerializer(Product.objects.all(), many=True)
        self.assertEqual(response.data, products.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_valid_product(self):
        response = self.client.post(reverse('product-list'),
                                    json.dumps(self.valid_payload),
                                    content_type='application/json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(reverse('product-list'),
                                    json.dumps(self.valid_payload),
                                    content_type='application/json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_an_invalid_product(self):
        response = self.client.post(reverse('product-list'),
                                    json.dumps(self.invalid_payload),
                                    content_type='application/json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(reverse('product-list'),
                                    json.dumps(self.invalid_payload),
                                    content_type='application/json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_product(self):
        response = self.client.get('/api/v1/products/product-test-1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/products/invalid-slug-lmao/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    

    def test_update_single_product(self):
        updated_payload = {
            'name': 'Updated Product Heehe',
            'category': [1]
        }

        response = self.client.put('/api/v1/products/product-test-1/',
                                   updated_payload,
                                   format='json',
                                   **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put('/api/v1/products/product-test-1/',
                                   updated_payload,
                                   format='json',
                                   **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], 'updated-product-heehe')


