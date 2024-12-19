from rest_framework import routers

from services.views import ServiceViewSet

router = routers.DefaultRouter()
router.register("services", ServiceViewSet)
urlpatterns = router.urls

app_name = "services"
