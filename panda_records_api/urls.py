from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls"), name="users"),
    path("api/", include("songs.urls"), name="songs"),
    path("api/", include("equipment.urls"), name="equipment"),
    path("api/", include("videos.urls"), name="videos"),
    path("api/", include("services.urls"), name="services"),
    path("api/", include("notifications.urls"), name="notifications"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
