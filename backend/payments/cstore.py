from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from midtransclient.error_midtrans import MidtransAPIError

from payments.midtrans import PaymentAPI
from payments.midtrans import midtrans
from cart.models import Transaction

class AlfamartTransaction(PaymentAPI):
    def post(self, request):
        cart = self.get_users_active_cart(request)
        param = self.build_transaction_param(request, 'cstore', cart, store='alfamart')

        try:
            response = midtrans.charge(param)
            cart.toggle_checkout()
            self.save_transaction_to_local_database(request.user, cart, response)
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])

class IndomaretTransaction(PaymentAPI):
    def post(self, request):
        cart = self.get_users_active_cart(request)
        param = self.build_transaction_param(request, 'cstore', cart, store='indomaret')

        try:
            response = midtrans.charge(param)
            cart.toggle_checkout()
            self.save_transaction_to_local_database(request.user, cart, response)
            return Response(response, status=response['status_code'])
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=e.api_response_dict['status_code'])