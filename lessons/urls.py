from rest_framework import routers

from lessons.views import LessonViewSet

router = routers.DefaultRouter()
router.register("lessons", LessonViewSet)
urlpatterns = router.urls

app_name = "lessons"
