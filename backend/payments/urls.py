from payments import midtrans
from django.urls import path

urlpatterns = [
    path('payments/create/', midtrans.MidtransTransaction.as_view(), name='create-transaction')
]