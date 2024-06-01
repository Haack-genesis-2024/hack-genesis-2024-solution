import { FC, memo } from "react";
import { Message } from "../api/chatApi";
import { Flex, HStack, Text } from "@chakra-ui/react";

type ChatMessageProps = {
  message: Message;
};

const ChatMessage: FC<ChatMessageProps> = memo(({ message }) => (
  <HStack align="flex-start" gap={2} w="100%" width="md">
    <Flex w={8} h={8} align="center" justify="center">
      {message.role === "AI" ? "🤖" : "👤"}
    </Flex>
    <Text lineHeight="taller" size="lg">
      {message.content}
    </Text>
  </HStack>
));

export default ChatMessage;
