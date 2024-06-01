import httpClient from "./httpClient";

export type Message = {
  id: number;
  role: "AI" | "HUMAN";
  content: string;
};

const getChat = () =>
  httpClient.get<Message[]>("/chat").then((res) => res.data);

const addMessage = (message: string) =>
  httpClient.post<Message[]>("/chat", { message }).then((res) => res.data);

const chatApi = {
  getChat,
  addMessage,
};

export default chatApi;
