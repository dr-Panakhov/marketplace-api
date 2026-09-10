from rest_framework import serializers
from .models import Ad, AdImage

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    # Подтягиваем галерею фоток (связь related_name='images' из модели)
    images = AdImageSerializer(many=True, read_only=True)
    # Вытаскиваем email автора, чтобы отдавать контакты, а не просто сухую цифру ID
    author_email = serializers.CharField(source='author.email', read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'city', 'price', 'phone_number', 'description', 'author_email', 'images', 'created_at']
