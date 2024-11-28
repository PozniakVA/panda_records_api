from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from panda_records_api import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls"), name="users"),
    path("api/", include("songs.urls"), name="songs"),
    path("api/", include("equipment.urls"), name="equipment"),
    path("api/", include("lessons.urls"), name="lessons"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
