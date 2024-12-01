from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services import chat_service
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

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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

@router.post("/{chatbot_id}/message")
def send_message(
    chatbot_id: int,
    user_input: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify chatbot ownership
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.client_id == current_user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    bot_response = chat_service.handle_chat(db, chatbot_id, user_input)
    return {"response": bot_response}