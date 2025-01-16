import os
import smtplib
from email.mime.text import MIMEText

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from panda_records_api import settings
from users.models import User, PasswordReset
from users.serializer import (
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    ChangeEmailRequestSerializer
)


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
                {"detail": "You do not have a refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
        except TokenError as e:
            raise InvalidToken({"detail": f"Invalid refresh token: {e}"})

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
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


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

            sender = os.getenv("EMAIL_SENDER")
            password = os.getenv("EMAIL_APP_PASSWORD_SENDER")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            template = render_to_string("emails/password_reset.html", {"reset_url": reset_url})

            try:
                server.login(sender, password)
                msg = MIMEText(template, "html")
                msg["Subject"] = "Зміна парооля"
                server.sendmail(sender, email, msg.as_string())
                return Response(
                    {"detail": "We have sent you a link to reset your password"},
                    status=status.HTTP_200_OK
                )
            except Exception:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        else:
            return Response({"detail": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"detail": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()

            return Response({"detail": "Password updated"})
        else:
            return Response({"detail": "No user found"}, status=404)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RequestChangeEmail(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChangeEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = request.user
            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(str(user.pk).encode())

            new_email = serializer.validated_data["new_email"]
            encoded_email = urlsafe_base64_encode(str(new_email).encode())

            change_url = f"http://localhost:8000/api/users/confirm-change-email/{uid}/{token}/{encoded_email}/"

            sender = os.getenv("EMAIL_SENDER")
            password = os.getenv("EMAIL_APP_PASSWORD_SENDER")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            template = render_to_string("emails/change_email.html", {"change_url": change_url})

            try:
                server.login(sender, password)
                msg = MIMEText(template, "html")
                msg["Subject"] = "Зміна електронної пошти"
                server.sendmail(sender, new_email, msg.as_string())
                return Response(
                    {"detail": "We have sent you a link to reset your email"},
                    status=status.HTTP_200_OK
                )
            except Exception:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmChangeEmail(APIView):
    def get(self, request, uid_b64, token, encoded_email_b64):

        try:
            uid = urlsafe_base64_decode(uid_b64).decode()
            new_email = urlsafe_base64_decode(encoded_email_b64).decode()

            user = get_user_model().objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.email = new_email
                user.save()

                return Response({"detail": "Email successfully changed!"}, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid link or token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
