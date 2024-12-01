from pydantic import BaseModel
from datetime import datetime

class ConversationOut(BaseModel):
    id: int
    chatbot_id: int
    user_message: str
    bot_response: str
    timestamp: datetime

    class Config:
        orm_mode = True