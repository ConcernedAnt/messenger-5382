from django.contrib.auth.middleware import get_user
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from django.db.models.query import Prefetch
from messenger_backend.common.utils import get_num_unread_messages, get_formatted_messages, \
    get_conversation_with_messages, get_time_stamp


class Messages(APIView):
    """expects {recipientId, text, conversationId } in body (conversationId will be null if no conversation exists yet)"""

    def post(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            sender_id = user.id
            body = request.data
            conversation_id = body.get("conversationId")
            text = body.get("text")
            recipient_id = body.get("recipientId")
            sender = body.get("sender")

            # if we already know conversation id, we can save time and just add it to message and return
            if conversation_id:
                conversation = Conversation.objects.filter(id=conversation_id).first()
                message = Message(
                    senderId=sender_id, text=text, conversation=conversation
                )
                message.save()
                message_json = message.to_dict()

                # Gets the number of unread messages for the other user
                convo = get_conversation_with_messages(conversation_id)
                messages = get_formatted_messages(convo)
                time_stamp = get_time_stamp(recipient_id, convo)
                num_unread_messages = get_num_unread_messages(recipient_id, time_stamp, messages)

                return JsonResponse(
                    {"message": message_json, "sender": body["sender"], "numUnreadMessages": num_unread_messages})

            # if we don't have conversation id, find a conversation to m       ake sure it doesn't already exist
            conversation = Conversation.find_conversation(sender_id, recipient_id)
            if not conversation:
                # create conversation
                conversation = Conversation(user1_id=sender_id, user2_id=recipient_id)
                conversation.save()

                if sender and sender["id"] in online_users:
                    sender["online"] = True

            message = Message(senderId=sender_id, text=text, conversation=conversation)
            message.save()
            message_json = message.to_dict()
            return JsonResponse({"message": message_json, "sender": sender, "numUnreadMessages": 1})
        except Exception as e:
            return HttpResponse(status=500)
