from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer as BaseTokenObtainSerializer,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import update_last_login


class TokenObtainSerializer(BaseTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:

        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["access_token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
