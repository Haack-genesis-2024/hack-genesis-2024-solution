import { FC, useEffect, useRef } from "react";
import { Message } from "../api/chatApi";
import { VStack } from "@chakra-ui/react";
import ChatMessage from "./ChatMessage";

type ChatMessageListProps = {
  messages: Message[];
};

const ChatMessageList: FC<ChatMessageListProps> = ({ messages }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages.length]);

  return (
    <VStack
      flexGrow={1}
      overflowY="scroll"
      align="stretch"
      gap={2}
      ref={containerRef}
    >
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
    </VStack>
  );
};

export default ChatMessageList;
