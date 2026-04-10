from fastapi import APIRouter, Depends
from app.auth.utils import get_current_user
from app.db.database import get_db_connection

router = APIRouter()


# -----------------------------------------
# GET CHAT HISTORY (for sidebar)
# -----------------------------------------

@router.get("/chat/history")
def get_chat_history(user=Depends(get_current_user)):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, message

        FROM chat_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 20
    """, (user["id"],))

    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": row[0], "message": row[1]}
        for row in rows
    ]


# -----------------------------------------
# GET FULL CONVERSATION
# -----------------------------------------

@router.get("/chat/history/{chat_id}")
def get_conversation(chat_id: int, user=Depends(get_current_user)):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response
        FROM chat_history
        WHERE id = ?
        AND user_id = ?
    """, (chat_id, user["id"]))

    rows = cursor.fetchall()

    conn.close()

    return [
        {"message": row[0], "response": row[1]}
        for row in rows
    ]