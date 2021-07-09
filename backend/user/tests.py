from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from user.models import User
from Virtuele.helpers import VirtueleTestBase

class UserAuthentication(VirtueleTestBase):
    def setUp(self):
        self.user_admin_factory()
        self.client = APIClient()
        self.admin_credential = {'email': 'admin@admin.com', 'password': 'admin'}
        self.user_credential = {'email': 'user@user.com', 'password': 'user'}
        self.invalid_credential = {'email': 'invalid@user.com', 'password': 'iaminvalid'}

    def test_get_jwt_with_admin_credential(self):
        jwt_token = self.client.post('/api/v1/jwt/create/',
                                    self.admin_credential,
                                    format='json')
        self.assertEqual(jwt_token.status_code, status.HTTP_200_OK)

        return jwt_token.data['access'], jwt_token.data['refresh']

    def test_get_jwt_with_user_credential(self):
        jwt_token = self.client.post('/api/v1/jwt/create/',
                                    self.admin_credential,
                                    format='json')
        self.assertEqual(jwt_token.status_code, status.HTTP_200_OK)

        return jwt_token.data['access'], jwt_token.data['refresh']

    def test_get_jwt_with_invalid_credential(self):
        jwt_token = self.client.post('/api/v1/jwt/create/',
                                    self.invalid_credential,
                                    format='json')
        self.assertEqual(jwt_token.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_jwt(self):
        access, refresh = self.test_get_jwt_with_admin_credential()

        new_access = self.client.post('/api/v1/jwt/refresh/', {'refresh': refresh}, format='json')
        self.assertNotEqual(new_access.data['access'], access)

    def test_login_admin(self):
        access, refresh = self.test_get_jwt_with_admin_credential()

        self.client.credentials(HTTP_AUTHORIZATION='JWT '+access)
        logged_in_user = self.client.get('/api/v1/users/me/', format='json')
        self.assertNotEqual(logged_in_user.status_code, status.HTTP_401_UNAUTHORIZED)

        return self.client

    def test_login_user(self):
        access, refresh = self.test_get_jwt_with_user_credential()

        self.client.credentials(HTTP_AUTHORIZATION='JWT '+access)
        logged_in_user = self.client.get('/api/v1/users/me/', format='json')
        self.assertNotEqual(logged_in_user.status_code, status.HTTP_401_UNAUTHORIZED)

        return self.client

    def test_logout(self):
        logged_in_client = self.test_login_admin()
        logged_in_client.credentials()
        logged_out_user = logged_in_client.get('/api/v1/users/me/', format='json')
        self.assertEqual(logged_out_user.status_code, status.HTTP_401_UNAUTHORIZED)
