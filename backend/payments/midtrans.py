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
    'x-override-notification':'https://03cd47b14d4a.ngrok.io/api/v1/payments/notifications/'
}

class PaymentAPI(APIView):
    permission_classes = [IsActive]

    def get_users_active_cart(self, request):
        return Cart.objects.get_or_create(user=request.user, checked_out=False)[0]

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

class GopayTransaction(PaymentAPI):
    def post(self, request):
        cart = self.get_users_active_cart(request)

        param = {
            'payment_type': 'gopay',
            'transaction_details': {
                'order_id': 'GOPAY-'+self.generate_order_id(request),
                'gross_amount': cart.total
            },
            'item_details': cart.get_selected_product(),
            'customer_details': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            },
            'gopay': {
                'enable_callback': False,
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
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])
