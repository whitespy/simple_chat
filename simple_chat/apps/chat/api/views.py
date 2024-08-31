from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from simple_chat.apps.chat.models import Thread

from .filters import ThreadFilter
from .serializers import (
    MessageCreateSerializer,
    MessageSerializer,
    ThreadCreateSerializer,
    ThreadSerializer,
)


class ThreadViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Thread.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ThreadFilter

    def get_permissions(self):
        if self.action in {"create", "destroy"}:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        match self.action:
            case "list":
                queryset = queryset.prefetch_related("participants")
            case "create_message" | "message_list" | "mark_message_as_read":
                queryset = queryset.filter(participants=self.request.user)

        return queryset

    def get_serializer_class(self):

        match self.action:
            case "create":
                return ThreadCreateSerializer
            case "list":
                return ThreadSerializer
            case "create_message":
                return MessageCreateSerializer
            case "message_list" | "mark_message_as_read":
                return MessageSerializer

    def create(self, *args, **kwargs):
        """
        Creates a thread. If a thread with particular participants
        exists just returns one.
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        thread = Thread.objects.get_with_participants(
            serializer.validated_data["participants"]
        ).first()

        if thread is None:
            thread = serializer.save()
            response_status = status.HTTP_201_CREATED
        else:
            response_status = status.HTTP_200_OK

        return Response(ThreadSerializer(thread).data, status=response_status)

    @action(methods=["GET"], detail=True, url_path="messages")
    def message_list(self, *args, **kwargs):
        """
        Returns thread message list.
        """
        thread = self.get_object()
        page = self.paginate_queryset(thread.messages.select_related("sender"))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @message_list.mapping.post
    def create_message(self, *args, **kwargs):
        """
        Creates a thread message.
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(thread=self.get_object(), sender=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True, url_path="unread-messages")
    def get_unread_messages_number(self, *args, **kwargs):
        """
        Returns unread messages number.
        """
        thread = self.get_object()
        unread_messages = thread.messages.unread_by_participant(self.request.user)
        return Response({"count": unread_messages.count()})

    @action(
        methods=["POST"],
        detail=True,
        url_path=r"messages/(?P<message_pk>\d+)/mark-as-read",
    )
    def mark_message_as_read(self, *args, **kwargs):
        """
        Marks a thread message as read.
        """
        thread = self.get_object()
        unread_messages = thread.messages.unread_by_participant(self.request.user)
        unread_message = get_object_or_404(
            unread_messages,
            pk=self.kwargs["message_pk"],
        )
        unread_message.mark_as_read()
        serializer = self.get_serializer(unread_message)
        return Response(serializer.data)
