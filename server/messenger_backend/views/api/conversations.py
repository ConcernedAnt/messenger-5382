from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from messenger_backend.common.utils import get_num_unread_messages, get_formatted_messages, get_time_stamp, \
    get_conversation_with_messages, get_last_read_message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request
from datetime import datetime


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                    .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                    .all()
            )

            conversations_response = []

            for convo in conversations:
                convo_dict = {
                    "id": convo.id,
                    "messages": get_formatted_messages(convo)
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]
                last_read_time_stamp = get_time_stamp(user_id, convo)

                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]

                other_user_time_stamp = None
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                    other_user_time_stamp = convo.user1TimeStamp
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)
                    other_user_time_stamp = convo.user2TimeStamp

                # Get the number of unread messages
                convo_dict["numUnreadMessages"] = get_num_unread_messages(user.id, last_read_time_stamp,
                                                                          convo_dict["messages"])

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                # get the timestamp of the other user
                convo_dict["otherUser"]["lastRead"] = get_last_read_message(convo_dict["messages"],
                                                                            convo_dict["otherUser"]["id"],
                                                                            other_user_time_stamp)
                conversations_response.append(convo_dict)
            conversations_response.sort(
                key=lambda convo: convo["messages"][-1]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)

    """Adds a timestamp for the current user to the conversation and returns the updated number of unread messages 
    and last read """

    def put(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            body = request.data
            conversation_id = body.get("convoId")
            time_stamp = body.get("timeStamp")

            # Convert timestamp to datetime to allow comparison
            time_stamp = datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S.%f%z")

            if conversation_id:
                convo = get_conversation_with_messages(conversation_id)

                if convo.user1 and convo.user1.id == user.id:
                    convo.user1TimeStamp = time_stamp
                elif convo.user2 and convo.user2.id == user.id:
                    convo.user2TimeStamp = time_stamp
                convo.save()

                messages = get_formatted_messages(convo)

                # Get your number of unread messages
                num_unread_messages = get_num_unread_messages(user.id, time_stamp, messages)

                # Get the last message that you read
                last_read = get_last_read_message(messages, user.id, time_stamp)

                return JsonResponse(
                    {"numUnreadMessages": num_unread_messages, "currentUser": user.id, "lastRead": last_read})
            return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(status=500)
