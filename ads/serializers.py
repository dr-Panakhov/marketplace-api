from rest_framework import serializers
from .models import Ad, AdImage

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ad
        # Убрали те самые фейковые поля (uploaded_images, deleted_images)
        fields = ['id', 'title', 'city', 'phone_number', 'description', 'price', 'currency', 'author', 'created_at', 'images']

    def create(self, validated_data):
        # Достаем сам запрос из контекста
        request = self.context.get('request')
        ad = Ad.objects.create(**validated_data)
        
        # Если юзер прикрепил файлы, жестко вытаскиваем их списком и сохраняем
        if request and hasattr(request, 'FILES'):
            for image in request.FILES.getlist('uploaded_images'):
                AdImage.objects.create(ad=ad, image=image)
                
        return ad

    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        # Обновляем обычные текстовые поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if request:
            # Ловим айдишники на удаление (getlist умеет вытаскивать массивы из FormData)
            deleted_images = request.data.getlist('deleted_images')
            if deleted_images:
                AdImage.objects.filter(id__in=deleted_images, ad=instance).delete()
            
            # Добавляем новые фотки
            if hasattr(request, 'FILES'):
                for image in request.FILES.getlist('uploaded_images'):
                    AdImage.objects.create(ad=instance, image=image)
                    
        return instance
