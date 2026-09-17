from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        # Вываливаем наружу всё твоё добро
        fields = ('id', 'email', 'role', 'phone_number', 'avatar', 'patronymic')
