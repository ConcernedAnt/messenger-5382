from django.db import models
from django.utils import timezone
from . import utils
from .user import User
from .conversation import Conversation


class Participant(utils.CustomModel):
    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="userId"
    )
    conversationId = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        db_column="conversationId",
        related_name="participants",
        related_query_name="participants"
    )
    timeStamp = models.DateTimeField(blank=True, default=timezone.now)
