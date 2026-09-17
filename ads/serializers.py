from rest_framework import serializers
from .models import Ad, AdImage

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    # НОВОЕ ПОЛЕ: список ID фоток, которые юзер хочет удалить
    deleted_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ad
        # Не забудь добавить deleted_images сюда!
        fields = ['id', 'title', 'city', 'phone_number', 'description', 'price', 'currency', 'author', 'created_at', 'images', 'uploaded_images', 'deleted_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        ad = Ad.objects.create(**validated_data)
        for image in uploaded_images:
            AdImage.objects.create(ad=ad, image=image)
        return ad

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        deleted_images = validated_data.pop('deleted_images', [])
        
        # Обновляем тексты
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # УДАЛЯЕМ ФОТКИ, если юзер нажал крестик на фронте
        if deleted_images:
            AdImage.objects.filter(id__in=deleted_images, ad=instance).delete()
            
        # Добавляем новые
        if uploaded_images:
            for image in uploaded_images:
                AdImage.objects.create(ad=instance, image=image)
                
        return instance
