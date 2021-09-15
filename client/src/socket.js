import io from "socket.io-client";
import store from "./store";
import {
  setNewMessage,
  removeOfflineUser,
  addOnlineUser,
  setReadReceipt,
  setUnreadMessages,
} from "./store/conversations";
import { updateReadTimeStamp } from "./store/utils/thunkCreators";

const socket = io(window.location.origin);

socket.on("connect", () => {
  console.log("connected to server");

  socket.on("add-online-user", (id) => {
    store.dispatch(addOnlineUser(id));
  });

  socket.on("remove-offline-user", (id) => {
    store.dispatch(removeOfflineUser(id));
  });

  socket.on("new-message", (data) => {
    const { activeConversation } = store.getState();
    // Info about the recipient of the message
    const { username, userId } = data.recipientInfo;

    const payload = {
      convoId: data.message.conversationId,
      timeStamp: new Date(),
      otherUserId: userId,
    };

    // Updates the timestamps if the conversation is already open
    if (activeConversation === username) {
      store.dispatch(updateReadTimeStamp(payload));
    }

    store.dispatch(setNewMessage(data.message, data.sender));

    store.dispatch(
      setUnreadMessages(data.message.conversationId, data.numUnreadMessages)
    );
  });

  socket.on("update-read-receipt", (data) => {
    store.dispatch(setReadReceipt(data.convoId, data.lastRead));
  });
});

export default socket;
