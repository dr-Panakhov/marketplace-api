from django.contrib import admin
from .models import ChatRoom, Message

admin.site.register(ChatRoom)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'text', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
