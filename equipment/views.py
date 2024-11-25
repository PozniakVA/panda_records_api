from rest_framework import viewsets

from equipment.models import Equipment
from equipment.serializer import EquipmentSerializer, EquipmentListSerializer
from panda_records_api.permissions import IsAdminUserOrReadOnly


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return EquipmentListSerializer
        return EquipmentSerializer
