from django.contrib import admin
from .models import SingleChatGroup, TextMessage, MediaMessage, Message, Room

# Register your models here.

admin.site.register(SingleChatGroup)
admin.site.register(TextMessage)
admin.site.register(MediaMessage)
admin.site.register(Message)
admin.site.register(Room)