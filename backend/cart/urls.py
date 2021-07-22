from django.urls import path
from cart.views import CartItem, Carts, Checkout, ToggleCartItem
app_name = 'cart'

urlpatterns = [
    path('carts/', Carts.as_view(),name='cart-list'),
    path('carts/items/<slug:slug>/<size>/', CartItem.as_view(), name='add-remove-cart-item'),
    path('carts/toggle/items/<slug:slug>/<size>/', ToggleCartItem.as_view(), name='toggle-cart-item'),
    path('carts/checkout/', Checkout.as_view(), name='checkout'),
]