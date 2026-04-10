from fastapi import FastAPI
from app.api.routes import router as chat_router
from app.api.auth_routes import router as auth_router
from app.analytics.routes import router as analytics_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.history_routes import router as history_router

app = FastAPI(title="Dynamic AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(analytics_router)

app.include_router(chat_router)

app.include_router(history_router)

@app.get("/")
def home():
    return {"message": "AI Chatbot API Running"}