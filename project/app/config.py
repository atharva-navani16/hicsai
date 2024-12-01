import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/chatbot_db")
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME: str = os.getenv("AWS_S3_BUCKET_NAME")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_API_URL: str = os.getenv("GROQ_API_URL", "https://api.groq.com/v1/query")
    
    # Other Configurations
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()