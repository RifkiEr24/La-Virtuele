from rest_framework.test import APIClient

from Virtuele.helpers import VirtueleTestBase

class PaymentTest(VirtueleTestBase):
    def setUp(self):
        self.user_admin_factory()
        self.client = APIClient()

    def test_create_a_new_transaction(self):
        response = self.client.get('/api/v1/payments/create/', **self.user_jwt)