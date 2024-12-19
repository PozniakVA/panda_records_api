from django_q.tasks import async_task
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from notifications.models import Notification
from notifications.serializer import NotificationSerializer, NotificationCreateSerializer
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

    def get_queryset(self):
        queryset = self.queryset

        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-created_at")


    def get_serializer_class(self):
        if self.action == "create":
            return NotificationCreateSerializer
        return NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        async_task(
            "notifications.tasks.send_notification_to_admin_about_client",
            {
                **serializer.data,
                "status": Notification.NotificationStatus.PENDING.label
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
