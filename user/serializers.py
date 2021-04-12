from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'username', 'password')