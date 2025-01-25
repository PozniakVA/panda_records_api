from rest_framework import serializers

from notifications.models import Notification


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "created_at",
            "name",
            "phone_number",
            "email",
            "message"
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "status",
            "created_at",
            "name",
            "phone_number",
            "email",
            "message"
        ]
