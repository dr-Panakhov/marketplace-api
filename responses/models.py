from django.db import models
from django.contrib.auth import get_user_model
from ads.models import Ad

User = get_user_model()

class Response(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Защита на уровне БД: один мастер = один отклик на одно объявление
    class Meta:
        unique_together = ('ad', 'master')

    def __str__(self):
        return f"Отклик от {self.master.email} на {self.ad.title}"
