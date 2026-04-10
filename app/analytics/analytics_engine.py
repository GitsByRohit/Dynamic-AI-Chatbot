from app.db.database import get_db_connection


# -------------------------------------------------
# LOG CHAT ANALYTICS
# -------------------------------------------------

def log_chat_analytics(user_id: int, intent: str, sentiment: str):
    """
    Stores analytics information for each chat message.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analytics_logs (user_id, intent, sentiment)
        VALUES (?, ?, ?)
    """, (user_id, intent, sentiment))

    conn.commit()
    conn.close()


# -------------------------------------------------
# GET CHAT TREND (Chats per Day)
# -------------------------------------------------

def get_chat_trend():
    """
    Returns number of chats per day for trend analysis.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(timestamp) as day, COUNT(*)
        FROM chat_history
        GROUP BY day
        ORDER BY day
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        {"date": row[0], "count": row[1]}
        for row in data
    ]


# -------------------------------------------------
# GET CHAT VOLUME BY HOUR
# -------------------------------------------------

def get_chat_volume_by_hour():
    """
    Returns number of chats grouped by hour of day.
    Useful for usage heatmaps.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%H', timestamp) as hour, COUNT(*)
        FROM chat_history
        GROUP BY hour
        ORDER BY hour
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        {"hour": row[0], "count": row[1]}
        for row in data
    ]


# -------------------------------------------------
# GET MOST ACTIVE USERS
# -------------------------------------------------

def get_most_active_users(limit=10):
    """
    Returns users with highest number of chats.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, COUNT(*) as total
        FROM chat_history
        GROUP BY user_id
        ORDER BY total DESC
        LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    conn.close()

    return [
        {"user_id": row[0], "total_chats": row[1]}
        for row in data
    ]