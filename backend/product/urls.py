from django.urls import path, include
from .views import AddToCart, Carts, Checkout, FeaturedProducts, GalleryList, ProductDetail, Products, RemoveFromCart

app_name = 'product'

urlpatterns = [
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('cart/', Carts.as_view(),name='cart-list'),
    path('cart/add-item/<slug:slug>/<size>/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/remove-item/<slug:slug>/<size>/', RemoveFromCart.as_view(), name='remove-from-cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
    path('products/', Products.as_view(), name='product-list'),
    path('products/featured/', FeaturedProducts.as_view(), name='featured-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
]