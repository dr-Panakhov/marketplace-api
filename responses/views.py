from rest_framework import viewsets, permissions, exceptions
from .models import Response
from .serializers import ResponseSerializer
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse


class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        # DRF сам найдет объект по ID или отдаст безопасную 404 ошибку
        response_obj = self.get_object()

        # Защита от IDOR: только автор услуги может управлять откликами
        if response_obj.ad.author != request.user:
            raise exceptions.PermissionDenied("Только автор объявления может принять этот отклик.")

        response_obj.status = 'accepted'
        response_obj.save()

        return DRFResponse({'status': 'Отклик успешно принят!'})

    def get_queryset(self):
        user = self.request.user
        # Секьюрность: отдаем только те отклики, к которым юзер имеет отношение
        return Response.objects.filter(Q(master=user) | Q(ad__author=user)).order_by('-created_at')

    def perform_create(self, serializer):
        ad = serializer.validated_data['ad']
        # Защита от дурака и накрутки
        if ad.author == self.request.user:
            raise exceptions.ValidationError("Нельзя откликаться на свое же объявление!")
        # Жестко привязываем токен текущего юзера
        serializer.save(master=self.request.user)
