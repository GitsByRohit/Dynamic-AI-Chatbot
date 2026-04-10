from app.db.database import get_db_connection
from datetime import datetime


# -----------------------------------------
# SAVE CHAT MESSAGE
# -----------------------------------------


def save_chat(user_id: int, message: str, response: str, intent: str, sentiment: str, conversation_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO chat_history
        (user_id, conversation_id, message, response, intent, sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, conversation_id, message, response, intent, sentiment, timestamp))

    conn.commit()
    cursor.close()
    conn.close()

# -----------------------------------------
# GET USER CHAT HISTORY
# -----------------------------------------

def get_user_history(user_id: int):
    """
    Retrieve full chat history for a user.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response, timestamp
        FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return history


# -----------------------------------------
# GET LAST N MESSAGES (FOR MEMORY)
# -----------------------------------------

def get_last_messages(user_id: int, limit: int = 5):
    """
    Retrieve last N messages for conversation memory.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response
        FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# -----------------------------------------
# DELETE USER CHAT HISTORY
# -----------------------------------------

def delete_user_history(user_id: int):
    """
    Delete all chat history of a user.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chat_history
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()

    cursor.close()
    conn.close()

#--------------------------------------
#--------------------------------------

def get_conversations(user_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT conversation_id, MIN(message)
        FROM chat_history
        WHERE user_id = ?
        GROUP BY conversation_id
        ORDER BY MAX(timestamp) DESC
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

#--------------------------------------
#--------------------------------------

def get_conversation_messages(user_id: int, conversation_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response, timestamp
        FROM chat_history
        WHERE user_id = ?
        AND conversation_id = ?
        ORDER BY timestamp ASC
    """, (user_id, conversation_id))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows