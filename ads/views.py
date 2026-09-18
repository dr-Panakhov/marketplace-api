from rest_framework import viewsets, permissions
from .models import Ad
from .serializers import AdSerializer
from rest_framework.decorators import action # <--- Добавили
from rest_framework.response import Response   # <--- Добавили

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('author').all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        # Достаем объявы только того юзера, который делает запрос
        my_ads = Ad.objects.filter(author=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_ads, many=True)
        return Response(serializer.data)
