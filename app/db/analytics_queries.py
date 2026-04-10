from app.db.database import get_db_connection


# ----------------------------------------
# TOTAL CHAT COUNT
# ----------------------------------------

def get_total_chats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chat_history")
    total = cursor.fetchone()[0]

    conn.close()
    return total


# ----------------------------------------
# ACTIVE USERS COUNT
# ----------------------------------------

def get_active_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM chat_history")
    total = cursor.fetchone()[0]

    conn.close()
    return total


# ----------------------------------------
# INTENT DISTRIBUTION
# ----------------------------------------

def get_intent_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT intent, COUNT(*) 
        FROM analytics_logs
        GROUP BY intent
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        {"intent": row[0], "count": row[1]}
        for row in data
    ]


# ----------------------------------------
# SENTIMENT DISTRIBUTION
# ----------------------------------------

def get_sentiment_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sentiment, COUNT(*)
        FROM analytics_logs
        GROUP BY sentiment
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        {"sentiment": row[0], "count": row[1]}
        for row in data
    ]


# ----------------------------------------
# TOP USER QUERIES
# ----------------------------------------

def get_top_queries(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message, COUNT(*) as freq
        FROM chat_history
        GROUP BY user_message
        ORDER BY freq DESC
        LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    conn.close()

    return [
        {"query": row[0], "count": row[1]}
        for row in data
    ]


# ----------------------------------------
# FALLBACK RATE
# ----------------------------------------

def get_fallback_rate():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics_logs
        WHERE intent = 'Fallback'
    """)

    fallback = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics_logs
    """)

    total = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return round((fallback / total) * 100, 2)


# ----------------------------------------
# INSERT FEEDBACK
# ----------------------------------------

def insert_feedback(user_id, message, response, rating):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (user_id, message, response, rating)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, response, rating))

    conn.commit()
    conn.close()


# ----------------------------------------
# FEEDBACK DISTRIBUTION
# ----------------------------------------

def get_feedback_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rating, COUNT(*)
        FROM feedback
        GROUP BY rating
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        {"rating": row[0], "count": row[1]}
        for row in data
    ]