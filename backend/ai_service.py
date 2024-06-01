from yandex_chain import YandexLLM
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from secrets_service import read_secret
from conversations_service import get_conversation, add_conversation_message

folder_id = read_secret('YANDEX_FOLDER_ID')
api_key = read_secret('YANDEX_API_KEY')
yagpt = YandexLLM(folder_id=folder_id, api_key=api_key) 

AI = "AI"
HUMAN = "HUMAN"
SYSTEM_MESSAGE = SystemMessage(content="You are Lord Vader. Answer user messages honestly.")

def format_user_conversation(user_id: str):
  raw_conversation = get_conversation(user_id)
  dialog = [AIMessage(content=message.content) if message.role == AI else HumanMessage(content=message.content) for message in raw_conversation]
  return [SYSTEM_MESSAGE] + dialog


def chat(user_id: str, message: str):
  user_message_entry = add_conversation_message(user_id, HUMAN, message)
  conversation = format_user_conversation(user_id)

  # ai_message = yagpt.invoke(conversation)
  ai_message = "test"
  ai_message_entry = add_conversation_message(user_id, AI, ai_message)

  return [user_message_entry, ai_message_entry]

  