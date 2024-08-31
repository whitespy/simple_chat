from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        db_index=True,
    )
    email = models.EmailField(_("email address"), db_index=True)

    class Meta(AbstractUser.Meta):
        ordering = ["date_joined"]
        constraints = [
            UniqueConstraint(
                Upper("username"),
                name="%(app_label)s_%(class)s_username_key",
            ),
            UniqueConstraint(
                Upper("email"),
                name="%(app_label)s_%(class)s_email_key",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if (
            User.objects.exclude(pk=self.pk)
            .filter(username__iexact=self.username)
            .exists()
        ):
            raise ValidationError(
                {"username": _("A user with that username already exists.")}
            )

        if User.objects.exclude(pk=self.pk).filter(email__iexact=self.email).exists():
            raise ValidationError(
                {"email": _("A user with that email already exists.")}
            )
