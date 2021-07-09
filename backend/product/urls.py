from django.urls import path
from .views import  Categories, CategoryDetail, CategoryProduct, GalleryList, ProductCategories, ProductDetail, Products, ProductReviews
app_name = 'product'

urlpatterns = [
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('categories/', Categories.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:pk>/products/', CategoryProduct.as_view(), name='categorys-product'),
    path('products/', Products.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<slug:slug>/reviews/', ProductReviews.as_view(), name='product-detail'),
    path('products/<slug:slug>/categories/<int:pk>/', ProductCategories.as_view(), name='product-categories')
]