import { useMutation, useQuery } from "@tanstack/react-query";
import { FC } from "react";
import chatApi from "../api/chatApi";
import {
  Alert,
  Button,
  CircularProgress,
  HStack,
  Heading,
  Text,
  VStack,
} from "@chakra-ui/react";
import ChatMessageList from "./ChatMessageList";
import ChatForm from "./ChatForm";
import authApi from "../api/authApi";
import queryClient from "../api/queryClient";

const Chat: FC = () => {
  const chatQuery = useQuery({
    queryKey: ["chat"],
    queryFn: chatApi.getChat,
  });

  const logoutMutation = useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["chat"] }),
  });

  return (
    <VStack h="100vh" flexGrow={1} p={4} align="stretch">
      <HStack justify="space-between">
        <Heading size="lg">Чат</Heading>
        <Button
          variant="outline"
          onClick={() => logoutMutation.mutate()}
          isLoading={logoutMutation.isPending}
        >
          Очистить чат
        </Button>
      </HStack>
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
