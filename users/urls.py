from django.urls import path

from users.views import (
    CustomTokenObtainPairView,
    CustomTokenViewBaseForRefresh,
    LogoutView
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "refresh/",
        CustomTokenViewBaseForRefresh.as_view(),
        name="token_refresh"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]

app_name = "users"
