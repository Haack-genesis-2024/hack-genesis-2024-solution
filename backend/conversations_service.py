from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:///chat.db'
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

def get_conversation(user_id: str) -> list[tuple[str, str]]:
    session = Session()
    conversations = session.query(Conversation.role, Conversation.message).filter(Conversation.user_id == user_id).all()
    session.close()
    return conversations

def add_conversation_message(user_id: str, role: str, message: str):
    session = Session()
    new_message = Conversation(user_id=user_id, role=role, message=message)
    session.add(new_message)
    session.commit()
    session.close()

def delete_conversation(user_id: str):
    session = Session()
    session.query(Conversation).filter(Conversation.user_id == user_id).delete()
    session.commit()
    session.close()