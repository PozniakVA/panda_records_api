from django.urls import path

from users.views import (
    CustomTokenObtainPairView,
    CustomTokenViewBaseForRefresh,
    LogoutView,
    ResetPassword,
    RequestPasswordReset,
    RequestChangeEmail,
    ConfirmChangeEmail,
    ChangePasswordView,
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "refresh/",
        CustomTokenViewBaseForRefresh.as_view(),
        name="token-refresh"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        RequestPasswordReset.as_view(),
        name="password-reset"
    ),
    path(
        "password-reset/<str:token>/",
        ResetPassword.as_view(),
        name="password-reset-with-token"
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password"
    ),
    path("change-email/", RequestChangeEmail.as_view(), name="change-email"),
    path(
        "confirm-change-email/<str:uid_b64>/<str:token>/<str:encoded_email_b64>/",
        ConfirmChangeEmail.as_view(),
        name="confirm-change-email"
    ),
]

app_name = "users"
