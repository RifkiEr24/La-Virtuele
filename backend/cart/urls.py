from django.urls import path
from cart.views import CartItem, Carts, Checkout
app_name = 'cart'

urlpatterns = [
    path('cart/', Carts.as_view(),name='cart-list'),
    path('cart/item/<slug:slug>/<size>/', CartItem.as_view(), name='add-to-cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
]