from django.urls.conf import include
from payments.midtrans import CancelGopayTransaction, GopayTransaction, CheckGopayTransactionStatus
from payments.notifications import payment_notification
from django.urls import path

urlpatterns = [
    path('payments/', include([
        path('gopay/', include([
            path('charge/', GopayTransaction.as_view(), name='gopay-transaction'),
            path('<slug:order_id>/status/', CheckGopayTransactionStatus.as_view(), name='gopay-transaction-status'),
            path('<slug:order_id>/cancel/', CancelGopayTransaction.as_view(), name='gopay-transaction-status'),
        ])),
        path('notifications/', payment_notification)
        # path('alfamart/'),
        # path('indomaret/'),
        # path('bank/', include([
        #     path('bni/')
        # ]))
    ])),

    ## path('payments/create/', midtrans.MidtransTransaction.as_view(), name='create-transaction')
]