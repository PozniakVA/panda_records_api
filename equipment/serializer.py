from rest_framework import serializers

from equipment.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "type",
            "model_name",
            "rental_price",
            "description"
        ]

class EquipmentListSerializer(EquipmentSerializer):
    class Meta:
        model = Equipment
        fields = [
            "name",
            "type",
            "model_name",
            "rental_price",
        ]