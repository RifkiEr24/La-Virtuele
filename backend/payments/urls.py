from django.urls.conf import include
from payments.gopay import GopayTransaction
from payments.cstore import AlfamartTransaction, IndomaretTransaction
from payments.notifications import notification_webhooks
from payments.midtrans import CancelTransaction, CheckTransactionStatus
from django.urls import path

urlpatterns = [
    path('payments/', include([
        path('gopay/charge/', GopayTransaction.as_view(), name='gopay-transaction'),
        path('alfamart/charge/', AlfamartTransaction.as_view(), name='alfamart-transaction'),
        path('indomaret/charge/', IndomaretTransaction.as_view(), name='indomaret-transaction'),
        
        path('<slug:order_id>/status/', CheckTransactionStatus.as_view(), name='gopay-transaction-status'),
        path('<slug:order_id>/cancel/', CancelTransaction.as_view(), name='gopay-transaction-cancel'),
        path('notifications/', notification_webhooks),
        
        # path('bank/', include([
        #     path('bni/')
        # ]))
    ])),

    ## path('payments/create/', midtrans.MidtransTransaction.as_view(), name='create-transaction')
]