from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'username', 'password')

class VirtueleTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(VirtueleTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token