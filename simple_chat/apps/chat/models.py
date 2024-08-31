from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import MessageQuerySet, ThreadQuerySet


class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="threads", verbose_name=_("participants")
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = ThreadQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        verbose_name = _("thread")
        verbose_name_plural = _("threads")

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("thread"),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("sender"),
    )
    text = models.TextField(_("text"))
    created = models.DateTimeField(_("created"), auto_now_add=True)
    is_read = models.BooleanField(_("is read"), default=False)

    objects = MessageQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return str(self.pk)

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=["is_read"])
