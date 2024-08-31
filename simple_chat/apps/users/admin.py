from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ("-id",)
    filter_horizontal = ()
    list_display_links = list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = (
        (
            _("Account data"),
            {
                "fields": (
                    "username",
                    "email",
                    ("first_name", "last_name"),
                    "password",
                ),
            },
        ),
        (
            _("Statuses"),
            {
                "classes": ("collapse",),
                "fields": ("is_superuser", "is_active", "is_staff"),
            },
        ),
        (
            _("Important dates"),
            {
                "classes": ("collapse",),
                "fields": ("last_login", "date_joined"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    ("first_name", "last_name"),
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
