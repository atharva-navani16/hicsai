from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, chatbot, documents, chat
from app.config import settings

app = FastAPI(
    title="AI-Powered Chatbot API",
    description="API for managing AI-powered chatbots for multiple clients.",
    version="1.0.0",
)

# CORS Configuration
origins = [
    "*",  # Update with specific origins in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/api/chatbots", tags=["Chatbots"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Chatbot API"}