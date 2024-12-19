from rest_framework import routers

from equipment.views import EquipmentViewSet

router = routers.DefaultRouter()
router.register("equipment", EquipmentViewSet)
urlpatterns = router.urls

app_name = "equipment"
