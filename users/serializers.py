from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'patronymic', 'phone_number')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        # Добавили first_name и last_name, вываливаем всё добро
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'avatar', 'patronymic')
