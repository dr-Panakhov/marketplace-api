from django.contrib import admin
from .models import Ad, AdImage

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'author', 'created_at')
    list_filter = ('city',)
    search_fields = ('title', 'description')
    inlines = [AdImageInline]
