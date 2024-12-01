from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from notifications.models import Notification
from notifications.serializer import NotificationSerializer
from panda_records_api.permissions import IsAdminUserOrCreateOnly


class NotificationView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Notification.objects.all()
    permission_classes = [IsAdminUserOrCreateOnly]
    serializer_class = NotificationSerializer
