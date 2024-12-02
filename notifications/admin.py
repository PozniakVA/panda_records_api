from django.contrib import admin

from notifications.models import Notification, Chat


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass
