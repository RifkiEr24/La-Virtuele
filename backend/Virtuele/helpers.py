from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

class VirtueleTestBase(TestCase):
    def user_admin_factory(self):
        get_user_model().objects.create_user(email='admin@admin.com',
                                             password='admin',
                                             first_name='admin',
                                             username='adminGod',
                                             is_active=True,
                                             is_superuser=True)

        get_user_model().objects.create_user(email='user@user.com',
                                             password='user',
                                             first_name='user',
                                             username='punyUser',
                                             is_active=True)
    @property
    def admin_jwt(self):
        user = get_user_model().objects.get(username='adminGod')
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION':f'JWT {refresh.access_token}'}

    @property
    def user_jwt(self):
        user = get_user_model().objects.get(username='punyUser')
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION':f'JWT {refresh.access_token}'}
