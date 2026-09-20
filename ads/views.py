from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .models import Ad
from .serializers import AdSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('author').all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        # Достаем объявы только того юзера, который делает запрос
        my_ads = Ad.objects.filter(author=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_ads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        ad = self.get_object()
        if request.user in ad.favorites.all():
            ad.favorites.remove(request.user)
            return Response({'status': 'removed'})
        else:
            ad.favorites.add(request.user)
            return Response({'status': 'added'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_favorites(self, request):
        fav_ads = Ad.objects.filter(favorites=request.user).order_by('-created_at')
        serializer = self.get_serializer(fav_ads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'user/(?P<user_id>\d+)')
    def user_ads(self, request, user_id=None):
        master_ads = Ad.objects.filter(author_id=user_id).order_by('-created_at')
        serializer = self.get_serializer(master_ads, many=True)
        return Response(serializer.data)
