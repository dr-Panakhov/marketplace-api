from rest_framework import viewsets, permissions
from .models import Ad
from .serializers import AdSerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    
    # Базовая защита: читать могут все, а создавать — только залогиненные
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Перехватываем процесс создания до отправки в БД
    def perform_create(self, serializer):
        # Жестко привязываем текущего юзера (request.user) в качестве автора
        serializer.save(author=self.request.user)
