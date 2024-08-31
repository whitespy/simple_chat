from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=14),
    "TOKEN_OBTAIN_SERIALIZER": "simple_chat.apps.users.api.serializers.TokenObtainSerializer",
}
