from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Review

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    def to_internal_value(self, data):
        data = data.copy()
        if 'firstName' in data and 'first_name' not in data:
            data['first_name'] = data['firstName']
        if 'lastName' in data and 'last_name' not in data:
            data['last_name'] = data['lastName']
        return super().to_internal_value(data)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'patronymic', 'phone_number')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'avatar', 'patronymic')

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.first_name', read_only=True) 

    class Meta:
        model = Review
        fields = ['id', 'author', 'author_name', 'seller', 'text', 'rating', 'created_at']
        read_only_fields = ['author']
    def validate(self, data):
        request = self.context.get('request')
        if request and request.user == data.get('seller'):
            raise serializers.ValidationError("Нельзя оставлять отзыв самому себе.")
        return data
