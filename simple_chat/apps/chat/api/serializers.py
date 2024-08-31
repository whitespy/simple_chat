from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils.translation import gettext

from simple_chat.apps.chat.models import Message, Thread

UserModel = get_user_model()


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name"]


class ThreadCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ["id", "participants"]

    def validate_participants(self, value):
        participants_number = len(set(value))

        if participants_number < 2:
            raise serializers.ValidationError(
                gettext("A thread may not have less than two participants.")
            )

        if participants_number > 2:
            raise serializers.ValidationError(
                gettext("A thread may not have more than two participants.")
            )

        return value


class ThreadSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Thread
        fields = ["id", "participants"]


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ["id", "text", "created"]


class MessageSerializer(serializers.ModelSerializer):
    sender = ParticipantSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "created", "is_read", "sender"]
