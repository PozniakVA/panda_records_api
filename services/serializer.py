from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "details_block1",
            "details_block2",
            "details_block3",
            "price",
            "hourly",
            "photo"
        ]

    def validate_photo(self, value):
        if value and value.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must not be greater than 10 MB.")
        return value
