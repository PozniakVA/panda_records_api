from django.urls import path

from users.views import CustomTokenObtainPairView, CustomTokenRefreshView, simple_endpoint_with_authentication, \
    simple_endpoint_without_authentication

urlpatterns = [
    path("with/", simple_endpoint_with_authentication, name="with"),
    path("without/", simple_endpoint_without_authentication, name="without"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "users"
