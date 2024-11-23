from rest_framework import viewsets

from songs.models import Song
from songs.serializer import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
