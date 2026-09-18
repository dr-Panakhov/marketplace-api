from rest_framework import serializers
from .models import Ad, AdImage


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']

class AdSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'city', 'phone_number', 'description', 'price', 'currency', 'author_name', 'created_at', 'images']

    def get_author_name(self, obj):
        name = ' '.join(
            part.strip()
            for part in (obj.author.first_name, obj.author.last_name)
            if part and part.strip()
        )
        return name or 'Продавец'

    def create(self, validated_data):
        request = self.context.get('request')
        author = validated_data.pop('author', None)
        if author is None and request and request.user.is_authenticated:
            author = request.user
        if author is None:
            raise serializers.ValidationError({'author': 'Автор объявления обязателен.'})

        ad = Ad.objects.create(author=author, **validated_data)
        if request and hasattr(request, 'FILES'):
            for image in request.FILES.getlist('uploaded_images'):
                AdImage.objects.create(ad=ad, image=image)
                
        return ad

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if request:
            deleted_images = request.data.getlist('deleted_images')
            if deleted_images:
                AdImage.objects.filter(id__in=deleted_images, ad=instance).delete()
            if hasattr(request, 'FILES'):
                for image in request.FILES.getlist('uploaded_images'):
                    AdImage.objects.create(ad=instance, image=image)
                    
        return instance
