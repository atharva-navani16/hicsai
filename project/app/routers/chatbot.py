from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.chatbot import ChatbotCreate, ChatbotOut
from app.services import chatbot_service
from app.database import SessionLocal
from app.models.user import User
from app.config import settings
from jose import jwt, JWTError

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/", response_model=ChatbotOut, status_code=status.HTTP_201_CREATED)
def create_chatbot(chatbot: ChatbotCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_chatbot = chatbot_service.create_chatbot(db, chatbot, current_user.id)
    return new_chatbot

@router.get("/", response_model=List[ChatbotOut])
def get_chatbots(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbots = chatbot_service.get_chatbots_by_client(db, current_user.id)
    return chatbots

@router.get("/{chatbot_id}", response_model=ChatbotOut)
def get_chatbot(chatbot_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbot = chatbot_service.get_chatbot(db, chatbot_id)
    if not chatbot or chatbot.client_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return chatbot