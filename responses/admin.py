from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('ad', 'master', 'status', 'created_at')
    list_filter = ('status',)
