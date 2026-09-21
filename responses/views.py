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
        response_obj = self.get_object()

        if response_obj.ad.author != request.user:
            raise exceptions.PermissionDenied("Только автор объявления может принять этот отклик.")

        response_obj.status = 'accepted'
        response_obj.save()

        return DRFResponse({'status': 'Отклик успешно принят!'})

    def get_queryset(self):
        user = self.request.user
        return Response.objects.filter(Q(master=user) | Q(ad__author=user)).order_by('-created_at')

    def perform_create(self, serializer):
        ad = serializer.validated_data['ad']
        if ad.author == self.request.user:
            raise exceptions.ValidationError("Нельзя откликаться на свое же объявление!")
        serializer.save(master=self.request.user)
