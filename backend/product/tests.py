from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.test import APIClient

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
                                    self.valid_payload,
                                    format='json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/v1/products/',
                                    self.valid_payload,
                                    format='json',
                                    **self.admin_jwt)
        product_1_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post('/api/v1/products/',
                                    self.valid_payload,
                                    format='json',
                                    **self.admin_jwt)
        product_2_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(product_1_slug, product_2_slug)

        response = self.client.post('/api/v1/products/',
                                    self.invalid_payload,
                                    format='json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/v1/products/',
                                    self.invalid_payload,
                                    format='json',
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
        self.category_factory(n=3)
        self.client = APIClient()
    
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

class ProductCategoryCRUD(VirtueleTestBase):
    def setUp(self):
        self.category_factory(n=5)
        self.product_factory(n=5, category=[category.id for category in Category.objects.all()])
        self.user_admin_factory()
        self.client = APIClient()

    def test_get_product_filter_by_category(self):
        for i in range(1, 5):
            products = ProductSerializer(Product.objects.filter(Q(category__id__icontains=i)), many=True)
            response = self.client.get(f'/api/v1/categories/{i}/products/')

            if products.data == []:
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            else:
                self.assertEqual(response.data, products.data)

    def test_add_category_into_a_product(self):
        product = Product.objects.get(id=1)
        product.category.set([1, 2])
        Category.objects.create(name='New Category')

        response = self.client.post(f'/api/v1/products/{product.slug}/categories/{6}/',
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(f'/api/v1/products/{product.slug}/categories/{6}/',
                                    format='json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(f'/api/v1/products/{product.slug}/categories/{7}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f'/api/v1/products/invalidslug/categories/{6}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f'/api/v1/products/{product.slug}/categories/{1}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'This product already on this category')

        response = self.client.post(f'/api/v1/products/{product.slug}/categories/{6}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProductSerializer(Product.objects.get(id=1)).data)

    def test_remove_category_from_a_product(self):
        product = Product.objects.get(id=1)
        product.category.set([1, 2])
        
        response = self.client.delete(f'/api/v1/products/{product.slug}/categories/{1}/',
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(f'/api/v1/products/{product.slug}/categories/{1}/',
                                    format='json',
                                    **self.user_jwt)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(f'/api/v1/products/{product.slug}/categories/{7}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f'/api/v1/products/invalidslug/categories/{1}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f'/api/v1/products/{product.slug}/categories/{3}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'This product is not already on this category')

        response = self.client.delete(f'/api/v1/products/{product.slug}/categories/{1}/',
                                    format='json',
                                    **self.admin_jwt)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProductSerializer(Product.objects.get(id=1)).data)
