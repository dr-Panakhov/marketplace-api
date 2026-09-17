from rest_framework import serializers
from .models import Ad, AdImage

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)
    # Специальное поле, чтобы ловить файлы с фронтенда
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ad
        # Не забудь, что тут теперь есть и images, и uploaded_images!
        fields = ['id', 'title', 'city', 'phone_number', 'description', 'price', 'currency', 'author', 'created_at', 'images', 'uploaded_images']

    # Метод для СОЗДАНИЯ объявления (POST)
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        ad = Ad.objects.create(**validated_data)
        
        for image in uploaded_images:
            AdImage.objects.create(ad=ad, image=image)
            
        return ad

    # Метод для РЕДАКТИРОВАНИЯ объявления (PATCH)
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        
        # Обновляем обычные текстовые поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Если прилетели новые фотки — сохраняем их
        if uploaded_images:
            for image in uploaded_images:
                AdImage.objects.create(ad=instance, image=image)
                
        return instance
