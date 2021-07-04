import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer
from Virtuele.helpers import VirtueleTestBase

class ProductCRUD(VirtueleTestBase):
    def setUp(self):
        self.user_admin_factory()
        self.product_factory()
        self.client = APIClient()

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

    def test_get_all_products(self):
        response = self.client.get('/api/v1/products/')
        products = ProductSerializer(Product.objects.all(), many=True)
        self.assertEqual(response.data, products.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/products/?featured=true')
        products = ProductSerializer(Product.objects.filter(is_featured=True), many=True)
        self.assertEqual(response.data, products.data)
        if not products: self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/v1/products/?category=1')
        products = ProductSerializer(Product.objects.filter(category=1), many=True)
        self.assertEqual(response.data, products.data)
        if not products: self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_a_product(self):
        response = self.client.post('/api/v1/products/',
                                    json.dumps(self.valid_payload),
                                    content_type='application/json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/v1/products/',
                                    json.dumps(self.valid_payload),
                                    content_type='application/json',
                                    **self.admin_jwt)
        product_1_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post('/api/v1/products/',
                                    json.dumps(self.valid_payload),
                                    content_type='application/json',
                                    **self.admin_jwt)
        product_2_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(product_1_slug, product_2_slug)

        response = self.client.post('/api/v1/products/',
                                    json.dumps(self.invalid_payload),
                                    content_type='application/json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/v1/products/',
                                    json.dumps(self.invalid_payload),
                                    content_type='application/json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_product(self):
        product = Product.objects.get(id=1)

        response = self.client.get(f'/api/v1/products/{product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/products/invalid-slug-lmao/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    

    def test_update_single_product(self):
        updated_payload = {
            'name': 'Updated Product Heehe',
            'category': [1]
        }
        product = Product.objects.get(id=1)

        response = self.client.put(f'/api/v1/products/{product.slug}/',
                                   updated_payload,
                                   format='json',
                                   **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(f'/api/v1/products/{product.slug}/',
                                   updated_payload,
                                   format='json',
                                   **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProductSerializer(Product.objects.get(slug='updated-product-heehe')).data)

        response = self.client.put(f'/api/v1/products/{product.slug}/',
                                   updated_payload,
                                   format='json',
                                   **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_product(self):
        product = Product.objects.get(id=1)

        response = self.client.delete(f'/api/v1/products/{product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(f'/api/v1/products/{product.slug}/', **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(f'/api/v1/products/invalidslug/', **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f'/api/v1/products/{product.slug}/', **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CategoryCRUD(VirtueleTestBase):
    def setUp(self):
        self.user_admin_factory()
        self.client = APIClient()
        self.category_factory(n=3)
    
    def test_get_all_categories(self):
        response = self.client.get('/api/v1/categories/')
        categories = CategorySerializer(Category.objects.all(), many=True)
        self.assertEqual(response.data, categories.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_category(self):
        response = self.client.post('/api/v1/categories/',
                                    {'name': 'New Category'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/api/v1/categories/',
                                    {'name': 'New Category'},
                                    format='json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/v1/categories/',
                                    {'name': 'New Category'},
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/v1/categories/',
                                    {'name': ''},
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_category(self):
        response = self.client.get('/api/v1/categories/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/categories/invalidid/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_category(self):
        response = self.client.put('/api/v1/categories/1/',
                                   {'name': 'New Name'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put('/api/v1/categories/1/',
                                   {'name': 'New Name'},
                                   format='json',
                                   **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put('/api/v1/categories/1/',
                                   {'name': ''},
                                   format='json',
                                   **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put('/api/v1/categories/1/',
                                   {'name': 'New Name'},
                                   format='json',
                                   **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Name')
