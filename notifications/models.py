from django.db import models

from users.models import User


class Notification(models.Model):
    class NotificationStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.NOT_STARTED,
    )
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats",
    )
    chat_id = models.IntegerField(null=True)
    notify_allowed = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.email
