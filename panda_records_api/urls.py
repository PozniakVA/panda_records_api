from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls"), name="users"),
    path("api/", include("songs.urls"), name="songs"),
    path("api/", include("equipment.urls"), name="equipment"),
    path("api/", include("lessons.urls"), name="lessons"),
]
