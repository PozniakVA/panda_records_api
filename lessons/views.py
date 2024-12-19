from rest_framework import viewsets

from lessons.models import Lesson
from lessons.serializer import LessonSerializer
from panda_records_api.permissions import IsAdminUserOrReadOnly


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = LessonSerializer
