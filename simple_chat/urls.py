from rest_framework_simplejwt.views import token_obtain_pair as authorize_view

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("authorize/", authorize_view),
                path("chat/", include("simple_chat.apps.chat.api.urls")),
            ]
        ),
    ),
]
