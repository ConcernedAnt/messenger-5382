async_mode = None

import os

import socketio
from online_users import online_users
from messenger_backend.models import User

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode, logger=False, cors_allowed_origins='*')
thread = None


@sio.event
def connect(sid, environ):
    sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)


@sio.on("go-online")
def go_online(sid, user_id):
    if user_id not in online_users:
        online_users.append(user_id)
    sio.emit("add-online-user", user_id, skip_sid=sid)


@sio.on("new-message")
def new_message(sid, message):
    user = User.get_by_id(message["message"]["senderId"])
    recipientInfo = {"username": user.username, "userId": user.id}

    sio.emit(
        "new-message",
        {"message": message["message"], "sender": message["sender"], "recipientInfo": recipientInfo,
         "numUnreadMessages": message["numUnreadMessages"]},
        skip_sid=sid,
    )


@sio.on("logout")
def logout(sid, user_id):
    if user_id in online_users:
        online_users.remove(user_id)
    sio.emit("remove-offline-user", user_id, skip_sid=sid)


@sio.on("update-read-receipt")
def update_read_receipt(sid, message):
    sio.emit(
        "update-read-receipt",
        {"convoId": message["convoId"], "lastRead": message["lastRead"], },
        skip_sid=sid,
    )
