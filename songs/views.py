from rest_framework import viewsets

from panda_records_api.permissions import IsAdminUserOrReadOnly
from songs.models import Song
from songs.serializer import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = SongSerializer
