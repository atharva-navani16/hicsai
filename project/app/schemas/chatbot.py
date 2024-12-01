from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
from datetime import datetime

class ChatbotCreate(BaseModel):
    name: str
    initial_message: str
    purpose: str  # e.g., Customer Service, Lead Generation
    ui_settings: Dict[str, Optional[str]]  # e.g., {"color": "#FFFFFF", "logo_url": "https://..."}
    
class ChatbotOut(BaseModel):
    id: int
    name: str
    client_id: int
    initial_message: str
    purpose: str
    ui_settings: Dict[str, Optional[str]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True