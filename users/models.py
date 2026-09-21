from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным полем')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Ищу услугу'),
        ('master', 'Предлагаю услуги'),
    )

    username = None 
    email = models.EmailField(unique=True)
    
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20) 
    
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='left_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'seller') 

    def __str__(self):
        return f"Отзыв от {self.author} для {self.seller}"
