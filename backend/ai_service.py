# from yandex_chain import YandexLLM
from search_pdf import query_information
from langchain.schema import AIMessage, HumanMessage, SystemMessage
# from secrets_service import read_secret
from conversations_service import get_conversation, add_conversation_message


AI = "AI"
HUMAN = "HUMAN"
SYSTEM_MESSAGE = SystemMessage(content="You are Financial assisant AI with ability to seearch in the uploaded documents. Always answer shortly and with respect.")

def format_user_conversation(user_id: str):
  raw_conversation = get_conversation(user_id)
  dialog = [AIMessage(content=message.content) if message.role == AI else HumanMessage(content=message.content) for message in raw_conversation]
  return [SYSTEM_MESSAGE] + dialog


def chat(user_id: str, message: str):
  user_message_entry = add_conversation_message(user_id, HUMAN, message)

  ai_message = "".join(query_information(message, 'opensearch-node1'))
  ai_message_entry = add_conversation_message(user_id, AI, ai_message)

  return [user_message_entry, ai_message_entry]

  