from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase


class CustomTokenViewBase(TokenViewBase):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        tokens = serializer.validated_data
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)

        if refresh_token:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

        return response


class CustomTokenObtainPairView(CustomTokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


class CustomTokenRefreshView(CustomTokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAdminUser])
def simple_endpoint_with_authentication(request):
    """
    A simple endpoint that returns a JSON response.
    Only accessible to admin users.
    """
    return Response({"message": "Hello, this is a simple endpoint with authentication!"})


@api_view(['GET'])

def simple_endpoint_without_authentication(request):
    """
    A simple endpoint that returns a JSON response.
    Only accessible to admin users.
    """
    return Response({"message": "Hello, this is a simple endpoint without authentication!"})
