from fastapi import APIRouter, Depends
from app.core.chatbot import get_chatbot_response

from app.auth.utils import get_current_user
from app.core.chat_orchestrator import process_chat
from pydantic import BaseModel
from app.db.chat_queries import get_conversations, get_conversation_messages

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: int 


@router.post("/chat")
def chat(request: ChatRequest, user=Depends(get_current_user)):

    user_id = user["id"]

    result = process_chat(
        user_id,
        request.message,
        request.conversation_id
    )

    return result

@router.get("/chat/history")
def chat_history(user=Depends(get_current_user)):

    user_id = user["id"]

    conversations = get_conversations(user_id)

    return [
        {
            "conversation_id": row[0],
            "title": row[1][:40]
        }
        for row in conversations
    ]

@router.get("/chat/history/{conversation_id}")
def conversation_messages(conversation_id: int, user=Depends(get_current_user)):

    user_id = user["id"]

    messages = get_conversation_messages(user_id, conversation_id)

    return [
        {
            "message": row[0],
            "response": row[1],
            "timestamp": row[2]
        }
        for row in messages
    ]