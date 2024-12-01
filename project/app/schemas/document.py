from pydantic import BaseModel
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    chatbot_id: int
    filename: str
    s3_key: str
    uploaded_at: datetime

    class Config:
        orm_mode = True