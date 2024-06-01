import { Button, HStack, Input } from "@chakra-ui/react";
import { FC, FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import chatApi, { Message } from "../api/chatApi";
import queryClient from "../api/queryClient";

const ChatForm: FC = () => {
  const [message, setMessage] = useState("");
  const { mutate, isPending } = useMutation({
    mutationFn: chatApi.addMessage,
    onSuccess: (data) => {
      setMessage("");
      queryClient.setQueryData(["chat"], (old: Message[]) => [...old, ...data]);
    },
  });

  const handleSendMessage = (e: FormEvent) => {
    e.preventDefault();
    mutate(message);
  };

  return (
    <HStack as="form" onSubmit={handleSendMessage}>
      <Input
        placeholder="Сообщение"
        onChange={(e) => setMessage(e.target.value)}
        value={message}
        required
      />
      <Button
        type="submit"
        isLoading={isPending}
        flexShrink={0}
        colorScheme="teal"
      >
        Отправить
      </Button>
    </HStack>
  );
};

export default ChatForm;
