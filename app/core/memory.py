from app.db.chat_queries import get_last_messages
from app.db.database import get_db_connection


# -----------------------------------------
# GET USER MEMORY
# -----------------------------------------

def get_conversation_memory(user_id: int, limit: int = 5):
    """
    Retrieve last N conversations for a user.
    Used to provide context to the AI model.
    """

    rows = get_last_messages(user_id, limit)

    if not rows:
        return ""

    context = ""

    # Reverse order to maintain chronological flow
    for row in reversed(rows):
        user_message = row["message"]
        bot_response = row["response"]

        context += f"User: {user_message}\n"
        context += f"Bot: {bot_response}\n"

    return context


# -----------------------------------------
# BUILD PROMPT WITH MEMORY
# -----------------------------------------

def build_prompt(user_message, user_id, conversation_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response
        FROM chat_history
        WHERE user_id = ? AND conversation_id = ?
        ORDER BY timestamp ASC
        LIMIT 10
    """, (user_id, conversation_id))

    history = cursor.fetchall()

    prompt = ""

    for msg, resp in history:
        prompt += f"User: {msg}\nBot: {resp}\n"

    prompt += f"User: {user_message}\nBot:"

    conn.close()

    return prompt



def build_conversation_context(user_id: int, current_message: str, limit: int = 5):
    """
    Builds a conversation context using previous chat history.
    This context will be passed to the AI model so it can understand
    the conversation flow.
    """

    history = get_chat_history(user_id, limit)

    context = "Conversation history:\n"

    # Add previous chats to context
    for chat in history:
        user_message = chat[2]
        bot_response = chat[3]

        context += f"User: {user_message}\n"
        context += f"Bot: {bot_response}\n"

    # Add current message
    context += f"\nUser: {current_message}\nBot:"

    return context