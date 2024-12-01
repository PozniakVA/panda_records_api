from rest_framework import viewsets

from panda_records_api.permissions import IsAdminUserOrReadOnly
from services.models import Service
from services.serializer import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    # permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ServiceSerializer
