from django.db import models
from django.contrib.auth import get_user_model

# Динамически получаем нашу кастомную модель юзера
User = get_user_model()

class Ad(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Если юзер удалит аккаунт (CASCADE), все его объявления тоже удалятся
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.city})"

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads_images/')
    
    def __str__(self):
        return f"Фото для {self.ad.title}"
