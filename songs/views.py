from rest_framework import viewsets

from songs.models import Song
from songs.permissions import IsAdminUserOrReadOnly
from songs.serializer import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = SongSerializer
