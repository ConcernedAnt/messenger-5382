from django.db.models.query import Prefetch
from messenger_backend.models import Conversation


# Formats the messages from the database
def get_formatted_messages(convo):
    messages = [
        message.to_dict(["id", "text", "senderId", "createdAt"])
        for message in convo.messages.all()
    ]
    return messages


# Returns the timestamp of the current user
def get_time_stamp(user_id, convo):
    last_read_time_stamp = None

    if convo.user1 and convo.user1.id == user_id:
        last_read_time_stamp = convo.user1TimeStamp
    elif convo.user2 and convo.user2.id == user_id:
        last_read_time_stamp = convo.user2TimeStamp

    return last_read_time_stamp


# Returns the conversation associated with the conversation id and its messages
def get_conversation_with_messages(convo_id):
    if not convo_id:
        return None

    convo = Conversation.objects.filter(id=convo_id).prefetch_related(
        Prefetch(
            "messages"
        )
    ).first()

    return convo


# Returns the number of unread messages in the conversation
def get_num_unread_messages(current_user, current_user_timestamp, messages):
    if not messages or not current_user_timestamp:
        return None

    unread_messages = [message["id"] for message in messages if
                       message["createdAt"] > current_user_timestamp and message["senderId"] != current_user]

    return len(unread_messages)


# Gets the last message that the user read
def get_last_read_message(messages, user_id, time_stamp):
    if time_stamp:
        for message in reversed(messages):
            if message["senderId"] != user_id and message["createdAt"] <= time_stamp:
                return message["id"]

    return None
