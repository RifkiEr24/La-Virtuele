import json
import hashlib

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from Virtuele.settings import MIDTRANS
from rest_framework.response import Response
from rest_framework.decorators import api_view

from cart.models import Transaction
from payments.midtrans import midtrans

def valid_signature_key(notification):
    hasher = hashlib.sha512()
    parameter:str = notification['order_id']+notification['status_code']+notification['gross_amount']+MIDTRANS['SERVER_KEY']
    hasher.update(parameter.encode('utf-8'))
    mock_signature = hasher.hexdigest()

    if notification['signature_key'] == mock_signature:
        return True
    
    return False

@csrf_exempt
@api_view(('POST',))
def notification_webhooks(request):
    notification = json.loads(request.body)
    transaction = midtrans.transactions.status(notification['order_id'])

    # Validate midtrans notification signature key
    if not valid_signature_key(notification):
        return Response(data={'detail': 'Unknown notification provider'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        transaction_local = Transaction.objects.get(order_id=transaction['order_id'])
        transaction_local.status = transaction['transaction_status']
        transaction_local.save()
    except Transaction.DoesNotExist:
        pass
    # Important remove this on non testing environment

    if transaction['transaction_status'] in ['capture', 'settlement']:
        if transaction['fraud_status'] == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            message = 'Notification received. Payments have been received, but it looks like your credit card is challenged'
        elif transaction['fraud_status'] == 'accept':
            # TODO set transaction status on your databaase to 'success'
            message = 'Notification received. Payments have been received, enjoy your new fashion :)'

    elif transaction['transaction_status'] in ['cancel', 'deny', 'expire']:
        # TODO set transaction status on your databaase to 'failure'
        message = 'Notification received. Transactions are discontinued, either expired or customer cancelled it'

    elif transaction['transaction_status'] == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        message = 'Notification received. Transactions found/created, waiting for payment'
    
    return Response(json.dumps(message), status=status.HTTP_200_OK)