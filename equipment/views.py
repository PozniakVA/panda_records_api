from rest_framework import viewsets

from equipment.models import Equipment
from equipment.serializer import EquipmentSerializer
from panda_records_api.permissions import IsAdminUserOrReadOnly


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = EquipmentSerializer

