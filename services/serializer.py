from rest_framework import serializers

from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "details_block1",
            "details_block2",
            "photo"
        ]
