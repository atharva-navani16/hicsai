from sqlalchemy.orm import Session

from app.models.chatbot import Chatbot
from app.schemas.chatbot import ChatbotCreate

def create_chatbot(db: Session, chatbot: ChatbotCreate, client_id: int):
    db_chatbot = Chatbot(
        name=chatbot.name,
        initial_message=chatbot.initial_message,
        purpose=chatbot.purpose,
        ui_settings=chatbot.ui_settings,
        client_id=client_id
    )
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

def get_chatbots_by_client(db: Session, client_id: int):
    return db.query(Chatbot).filter(Chatbot.client_id == client_id).all()

def get_chatbot(db: Session, chatbot_id: int):
    return db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()