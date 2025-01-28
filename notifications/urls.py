from rest_framework import routers

from notifications.views import NotificationView

router = routers.DefaultRouter()
router.register("notifications", NotificationView, basename="notification")
urlpatterns = router.urls

app_name = "notifications"
