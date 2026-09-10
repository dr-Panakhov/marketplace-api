from rest_framework import serializers
from .models import Ad, AdImage

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.email') # Отдаем email вместо ID юзера

    class Meta:
        model = Ad
        fields = ['id', 'title', 'city', 'phone_number', 'description', 'price', 'author', 'created_at', 'images']
