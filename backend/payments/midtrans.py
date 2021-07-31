from datetime import date
from django.conf import settings
from django.shortcuts import get_object_or_404

from midtransclient import CoreApi
from midtransclient.error_midtrans import MidtransAPIError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart, ProductCart, Transaction
from user.permissions import IsActive

midtrans = CoreApi(
    is_production=False,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY']
)

midtrans.api_config.custom_headers = {
    'x-override-notification':'http://127.0.0.1:8000'
}

class PaymentAPI(APIView):
    permission_classes = [IsActive]

    def get_users_active_cart(self, request):
        return Cart.objects.get_or_create(user=request.user, checked_out=False)[0]

    def get_selected_product_cart(self, cart):
        selected_product = []

        for product in ProductCart.objects.filter(cart=cart, selected=True):
            selected_product.append({
                'name': product.product.name,
                'description': product.product.description,
                'size': product.size,
                'price': product.product.price,
                'quantity': product.qty,
                'subtotal': product.subtotal,
            })
        
        return selected_product

    def tokenize_todays_date(self):
        tup_date = date.timetuple(date.today())
        mon = tup_date.tm_mon if tup_date.tm_mon >= 10 else '0'+str(tup_date.tm_mon)
        day = tup_date.tm_mday if tup_date.tm_mday >= 10 else '0'+str(tup_date.tm_mday)

        return f'{tup_date.tm_year}{mon}{day}'

    def generate_order_id(self, request):
        cart = self.get_users_active_cart(request)

        order_id = f'{request.user.id}-{cart.id}-'
        order_id += f'{self.tokenize_todays_date()}'
        order_id += f'{str(hash(request.user.username))}-'
        order_id += f'{cart.total}'

        return order_id

    def save_transaction_to_local_database(self, user, cart, midtrans_response):
        order = Transaction.objects.get_or_create(
            user=user,
            cart=cart,
            order_id=midtrans_response['order_id'],
            defaults={
                'status': midtrans_response['transaction_status']
            }
        )

        return order

    def handle_notification(self, status):
        notification = midtrans.transactions.notification(status)
        order_id = notification['order_id']
        transaction_status = notification['transaction_status']
        fraud_status = notification['fraud_status']

        print(f'Transaction notification received. Order ID: {order_id}. Transaction status: {transaction_status}. Fraud status: {fraud_status}')

        transaction = Transaction.objects.get(order_id=order_id)
        transaction.status = transaction_status
        transaction.save()
        
        if transaction_status == 'capture':
            if fraud_status == 'challenge':
                # TODO set transaction status on your databaase to 'challenge'
                None
            elif fraud_status == 'accept':
                # TODO set transaction status on your databaase to 'success'
                None
        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            # TODO set transaction status on your databaase to 'failure'
            None
        elif transaction_status == 'pending':
            # TODO set transaction status on your databaase to 'pending' / waiting payment
            None

class GopayTransaction(PaymentAPI):
    def post(self, request):
        cart = self.get_users_active_cart(request)

        param = {
            "payment_type": "gopay",
            "transaction_details": {
                'order_id': 'GOPAY-'+self.generate_order_id(request),
                "gross_amount": cart.total
            },
            "item_details": self.get_selected_product_cart(cart),
            "customer_details": {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
            "gopay": {
                "enable_callback": False,
            }
        }

        try:
            response = midtrans.charge(param)
            cart.toggle_checkout()
            self.save_transaction_to_local_database(request.user, cart, response)
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])

class CheckGopayTransactionStatus(PaymentAPI):
    def get(self, request, order_id):
        try:
            transaction = get_object_or_404(Transaction, order_id=order_id)

            if (not transaction.user == request.user) and not request.user.is_superuser:
                return Response({'message': 'You do not have permission to view this transaction status'}, 403)

            response = midtrans.transactions.status(order_id)
            response['status_code'] = '200'
            self.handle_notification(response)
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])

class CancelGopayTransaction(PaymentAPI):
    def post(self, request, order_id):
        try:
            transaction = get_object_or_404(Transaction, order_id=order_id)

            if (not transaction.user == request.user) and not request.user.is_superuser:
                return Response({'message': 'You do not have permission to view this transaction status'}, 403)

            response = midtrans.transactions.cancel(order_id)
            self.handle_notification(response)
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])
