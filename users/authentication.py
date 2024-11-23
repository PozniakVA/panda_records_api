from typing import Optional, Tuple, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token


AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:

        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:

            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token