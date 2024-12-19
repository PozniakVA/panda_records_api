from django.urls import path

from users.views import (
    CustomTokenObtainPairView,
    CustomTokenViewBaseForRefresh
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "refresh/",
        CustomTokenViewBaseForRefresh.as_view(),
        name="token_refresh"
    ),
]

app_name = "users"
