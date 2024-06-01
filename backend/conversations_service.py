from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dataclasses

DATABASE_URI = 'sqlite:///db/chat.db'
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    role = Column(String)
    message = Column(String)

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@dataclasses.dataclass
class Message:
    id: int
    role: str
    content: str

def get_conversation(user_id: str):
    session = Session()
    conversations_tuples = session.query(Conversation.id, Conversation.role, Conversation.message).filter(Conversation.user_id == user_id).all()
    session.close()
    return [Message(id=id, role=role, content=message) for id, role, message in conversations_tuples]

def add_conversation_message(user_id: str, role: str, message: str):
    session = Session()
    new_message = Conversation(user_id=user_id, role=role, message=message)
    session.add(new_message)
    session.flush()
    session.refresh(new_message)
    message_entry = Message(id=new_message.id, role=new_message.role, content=new_message.message)
    session.commit()
    session.close()
    return message_entry


def delete_conversation(user_id: str):
    session = Session()
    session.query(Conversation).filter(Conversation.user_id == user_id).delete()
    session.commit()
    session.close()