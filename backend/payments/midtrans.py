import json
from django.conf import settings

from midtransclient import Snap, CoreApi
from midtransclient.error_midtrans import MidtransAPIError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

core_api = CoreApi(
    is_production=False,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY']
)

snap = Snap(
    is_production=False,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY']
)

# Todo: Create a testing ready transaction function
class MidtransTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        param = {
            "payment_type": "bank_transfer",
            "transaction_details": {
                "gross_amount": 24145,
                "order_id": "test-transaction-321",
            },
            "bank_transfer":{
                "bank": "bni"
            }
        }

        try:
            response = core_api.charge(param)
            return Response(response, status=status.HTTP_200_OK)
        except MidtransAPIError as e:
            return Response(e.api_response_dict, status=status.HTTP_401_UNAUTHORIZED)
