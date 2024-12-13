from rest_framework import viewsets

from panda_records_api.permissions import IsAdminUserOrReadOnly
from songs.models import Song
from songs.serializer import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = self.queryset
        top = self.request.query_params.get("top")

        option = {"true": True, "false": False}

        if top and top.lower() in option:
            queryset = queryset.filter(top=option[top.lower()])

        return queryset
