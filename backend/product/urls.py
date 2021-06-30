from django.urls import path
from .views import CartItem, Carts, Categories, CategoryDetail, Checkout, GalleryList, ProductDetail, Products, ProductReviews
app_name = 'product'

urlpatterns = [
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('cart/', Carts.as_view(),name='cart-list'),
    path('cart/item/<slug:slug>/<size>/', CartItem.as_view(), name='add-to-cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
    path('categories/', Categories.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', Products.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<slug:slug>/reviews/', ProductReviews.as_view(), name='product-detail'),
]