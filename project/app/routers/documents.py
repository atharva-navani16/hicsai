from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.schemas.document import DocumentOut
from app.services import document_service
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

@router.post("/{chatbot_id}/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    chatbot_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify chatbot ownership
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.client_id == current_user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    s3_key = document_service.upload_document_to_s3(file, chatbot_id)
    if not s3_key:
        raise HTTPException(status_code=500, detail="Failed to upload document")
    
    document = document_service.create_document_record(db, chatbot_id, file.filename, s3_key)
    return document

@router.get("/{chatbot_id}/", response_model=List[DocumentOut])
def get_documents(chatbot_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id, Chatbot.client_id == current_user.id).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    documents = document_service.get_documents_by_chatbot(db, chatbot_id)
    return documents