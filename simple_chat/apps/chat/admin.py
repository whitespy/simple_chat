from django.contrib import admin

from .models import Message, Thread


class MessageInline(admin.StackedInline):
    extra = 0
    model = Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "created"]
    inlines = [MessageInline]
