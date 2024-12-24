import os

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from panda_records_api import settings
from users.models import User, PasswordReset
from users.serializer import ResetPasswordRequestSerializer, ResetPasswordSerializer


class CustomTokenViewBaseForAccess(TokenViewBase):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        tokens = serializer.validated_data
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        email = request.data["email"]
        user = get_user_model().objects.get(email=email)

        response = Response(
            {"access_token": access_token, "telegram_bot": user.your_telegram_bot},
            status=status.HTTP_200_OK
        )

        if refresh_token:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="None",
            )

        return response


class CustomTokenObtainPairView(CustomTokenViewBaseForAccess):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


class CustomTokenViewBaseForRefresh(generics.GenericAPIView):
    def get(self, request: Request, *args, **kwargs) -> Response:

        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "You do not have a refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
        except TokenError as e:
            raise InvalidToken({"error": f"Invalid refresh token: {e}"})

        access_token = str(token.access_token)

        return Response(
            {"access_token": access_token},
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.COOKIES.get("refresh_token", None)
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = f"{settings.PASSWORD_RESET_URL}/{token}"

            subject = "Зміна пароля"
            context = {
                "user": user,
                "reset_url": reset_url,
            }
            message = render_to_string("emails/password_reset.html", context)
            email_message = EmailMessage(subject, message, to=[email])
            email_message.content_subtype = "html"

            # Send the email
            email_message.send()

            return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()

            return Response({"success": "Password updated"})
        else:
            return Response({"error": "No user found"}, status=404)
