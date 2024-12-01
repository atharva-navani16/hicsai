from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"), nullable=False)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)  # Path in S3 bucket
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chatbot = relationship("Chatbot", back_populates="documents")