from rest_framework import serializers
from .models import Response

class ResponseSerializer(serializers.ModelSerializer):
    master_name = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = ['id', 'ad', 'master', 'master_name', 'message', 'status', 'created_at']
        read_only_fields = ['master', 'status']

    def get_master_name(self, obj):
        if obj.master:
            return f"{obj.master.first_name} {obj.master.last_name}".strip()
        return "Неизвестный исполнитель"
