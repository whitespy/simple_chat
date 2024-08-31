from django.db import models


class ThreadQuerySet(models.QuerySet):

    def get_with_participants(self, participants):
        queryset = self.all()

        for participant in participants:
            queryset = queryset.filter(participants=participant)

        return queryset


class MessageQuerySet(models.QuerySet):

    def unread_by_participant(self, participant):
        return self.filter(
            thread__participants=participant,
            is_read=False,
        ).exclude(sender=participant)
