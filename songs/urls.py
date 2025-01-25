from rest_framework import routers

from songs.views import SongViewSet

router = routers.DefaultRouter()
router.register("songs", SongViewSet, basename="song")
urlpatterns = router.urls

app_name = "songs"
