import { useQuery } from "@tanstack/react-query";
import { FC } from "react";
import chatApi from "../api/chatApi";
import {
  Alert,
  CircularProgress,
  Heading,
  Text,
  VStack,
} from "@chakra-ui/react";
import ChatMessageList from "./ChatMessageList";
import ChatForm from "./ChatForm";

const Chat: FC = () => {
  const chatQuery = useQuery({
    queryKey: ["chat"],
    queryFn: chatApi.getChat,
  });

  return (
    <VStack h="100vh" flexGrow={1} p={4} align="stretch">
      <Heading size="lg">Чат</Heading>
      {chatQuery.isError && (
        <Alert status="error">{chatQuery.error.message}</Alert>
      )}
      {chatQuery.isLoading && <CircularProgress isIndeterminate color="teal" />}
      {chatQuery.data &&
        (chatQuery.data.length ? (
          <ChatMessageList messages={chatQuery.data} />
        ) : (
          <Text flexGrow={1}>Начните чат</Text>
        ))}
      <ChatForm />
    </VStack>
  );
};

export default Chat;
