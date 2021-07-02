from django.urls import path
from .views import  Categories, CategoryDetail, GalleryList, ProductDetail, Products, ProductReviews
app_name = 'product'

urlpatterns = [
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('categories/', Categories.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', Products.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<slug:slug>/reviews/', ProductReviews.as_view(), name='product-detail'),
]