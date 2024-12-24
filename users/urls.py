from django.urls import path

from users.views import (
    CustomTokenObtainPairView,
    CustomTokenViewBaseForRefresh,
    LogoutView, ResetPassword, RequestPasswordReset
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "refresh/",
        CustomTokenViewBaseForRefresh.as_view(),
        name="token_refresh"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot_password/", RequestPasswordReset.as_view(), name="forgot_password"),
    path("password_reset/<str:token>/", ResetPassword.as_view(), name="password_reset"),
]

app_name = "users"
