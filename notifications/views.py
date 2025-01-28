from django_q.tasks import async_task
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializer import (
    NotificationSerializer,
    NotificationCreateSerializer
)
from panda_records_api.permissions import IsAdminUserOrCreateOnly


@extend_schema(
    parameters=[
        OpenApiParameter(
            "status",
            type=OpenApiTypes.STR,
            description="Filter by status (ex. ?status=pending)",
        )
    ]
)
class NotificationView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrCreateOnly]

    def get_queryset(self):
        queryset = Notification.objects.all()

        status_parameter = self.request.query_params.get("status")
        if status_parameter:
            queryset = queryset.filter(status=status_parameter)

        return queryset.order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return NotificationCreateSerializer
        return NotificationSerializer

    def _send_notification(self, serializer_data):
        async_task(
            "notifications.tasks.send_notification_to_admin_about_client",
            {
                **serializer_data,
                "status": Notification.NotificationStatus.PENDING.label,
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)


        self._send_notification(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )