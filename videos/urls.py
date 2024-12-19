from rest_framework import routers

from videos.views import VideoViewSet

router = routers.DefaultRouter()
router.register("videos", VideoViewSet)
urlpatterns = router.urls

app_name = "videos"
