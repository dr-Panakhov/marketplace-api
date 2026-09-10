from rest_framework import serializers
from .models import Response

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'ad', 'master', 'message', 'status', 'created_at']
        # Защита от подмены данных в POST-запросе
        read_only_fields = ['master', 'status']
