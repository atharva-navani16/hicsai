from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Chatbot(Base):
    __tablename__ = "chatbots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    initial_message = Column(String, nullable=False)
    purpose = Column(String, nullable=False)  # e.g., Customer Service, Lead Generation
    ui_settings = Column(JSON, nullable=False)  # e.g., {"color": "#FFFFFF", "logo_url": "https://..."}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    client = relationship("User", back_populates="chatbots")
    documents = relationship("Document", back_populates="chatbot")
    conversations = relationship("Conversation", back_populates="chatbot")