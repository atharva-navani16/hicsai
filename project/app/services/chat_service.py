import requests
from sqlalchemy.orm import Session
import time

from app.models.conversation import Conversation
from app.schemas.conversation import ConversationOut
from app.config import settings

def get_bot_response(user_input: str, chatbot_config: dict):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.2-8b",
        "prompt": user_input,
        "temperature": 0.7,
        "max_tokens": 150
    }
    try:
        response = requests.post(settings.GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "I'm sorry, I couldn't process that.")
    except requests.RequestException as e:
        print(f"Groq API Error: {e}")
        return "I'm sorry, I'm experiencing some issues right now."

def store_conversation(db: Session, chatbot_id: int, user_message: str, bot_response: str):
    conversation = Conversation(
        chatbot_id=chatbot_id,
        user_message=user_message,
        bot_response=bot_response,
        timestamp=int(time.time())
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def handle_chat(db: Session, chatbot_id: int, user_input: str):
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not chatbot:
        return "Chatbot not found."
    
    # You can enhance the prompt with initial_message or other configurations
    prompt = f"{chatbot.initial_message}\nUser: {user_input}\nBot:"
    bot_response = get_bot_response(prompt, chatbot.ui_settings)
    conversation = store_conversation(db, chatbot_id, user_input, bot_response)
    return bot_response