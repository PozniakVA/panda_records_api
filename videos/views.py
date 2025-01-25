from rest_framework import viewsets

from videos.models import Video
from videos.serializer import VideoSerializer
from panda_records_api.permissions import IsAdminUserOrReadOnly


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = VideoSerializer
