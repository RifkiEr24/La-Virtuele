from django.urls import path, include
from .views import AddToCart, Carts, Checkout, FeaturedProducts, ProductDetail, Products, RemoveFromCart

app_name = 'product'

urlpatterns = [
    path('products/', Products.as_view(), name='list'),
    path('products/featured/', FeaturedProducts.as_view(), name='featured-list'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('carts/<user>/', Carts.as_view(),name='cart-list'),
    path('add-to-cart/<slug:slug>/<size>/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/<size>/', RemoveFromCart.as_view(), name='remove-from-cart'),
    path('checkout-cart/', Checkout.as_view(), name='checkout')
]