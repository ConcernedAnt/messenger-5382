from django.db import models
from django.db.models import Q, Count
from . import utils


class Conversation(utils.CustomModel):
    name = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # Find conversation given a list of the user ids
    def find_conversation(user_ids):
        try:
            query = Conversation.objects.annotate(participants_count=Count('participants')).filter(
                participants_count=len(user_ids))

            for user_id in user_ids:
                query = query.filter(participants__userId=user_id)

            return query.first()

        except Conversation.DoesNotExist:
            return None
