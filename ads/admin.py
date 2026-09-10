from django.contrib import admin
from .models import Ad, AdImage

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1  # Сколько пустых слотов для фоток показывать по умолчанию

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'author', 'created_at') # Колонки в общем списке
    list_filter = ('city',) # Боковая панель фильтрации
    search_fields = ('title', 'description') # Поиск по тексту
    inlines = [AdImageInline]  # Подключаем галерею внутрь объявления
