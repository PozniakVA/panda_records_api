from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from equipment.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "model",
            "photo"
        ]

    def validate_photo(self, value):
        if value and value.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must not be greater than 10 MB.")
        return value
