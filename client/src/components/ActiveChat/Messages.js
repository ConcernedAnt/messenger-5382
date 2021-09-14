import React from "react";
import { Box } from "@material-ui/core";
import { SenderBubble, OtherUserBubble } from "../ActiveChat";
import moment from "moment";

const Messages = (props) => {
  const { messages, otherUser, userId } = props;

  // Gets the last message read by the other user
  const lastReadMessage = messages
    .slice()
    .reverse()
    .find(
      (message) =>
        message.senderId === userId &&
        new Date(message.createdAt) <= new Date(otherUser.lastRead)
    );

  return (
    <Box>
      {messages.map((message) => {
        const time = moment(message.createdAt).format("h:mm");

        const isLastMessageRead = message.id === lastReadMessage?.id;

        return message.senderId === userId ? (
          <SenderBubble
            key={message.id}
            text={message.text}
            time={time}
            otherUser={otherUser}
            isLastMessageRead={isLastMessageRead}
          />
        ) : (
          <OtherUserBubble
            key={message.id}
            text={message.text}
            time={time}
            otherUser={otherUser}
          />
        );
      })}
    </Box>
  );
};

export default Messages;
