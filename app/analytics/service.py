import sqlite3
from collections import Counter
from datetime import datetime

DB_PATH = "data/chatbot.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------------
# BASIC STATS
# -------------------------------

def get_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chat_history")
    total_chats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM chat_history")
    active_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chat_history WHERE intent='Fallback'")
    fallback = cursor.fetchone()[0]

    fallback_rate = 0
    if total_chats > 0:
        fallback_rate = round((fallback / total_chats) * 100, 2)

    conn.close()

    return {
        "total_chats": total_chats,
        "active_users": active_users,
        "fallback_rate": fallback_rate
    }


# -------------------------------
# CHAT TREND
# -------------------------------

def get_chat_trend():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(timestamp), COUNT(*)
        FROM chat_history
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """)

    rows = cursor.fetchall()

    conn.close()

    return [{"date": r[0], "count": r[1]} for r in rows]


# -------------------------------
# INTENT DISTRIBUTION
# -------------------------------

def get_intent_distribution():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT intent FROM chat_history")

    intents = [row[0] for row in cursor.fetchall()]

    conn.close()

    counts = Counter(intents)

    return [{"intent": k, "count": v} for k, v in counts.items()]


# -------------------------------
# SENTIMENT DISTRIBUTION
# -------------------------------

def get_sentiment_distribution():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT sentiment FROM chat_history")

    sentiments = [row[0] for row in cursor.fetchall()]

    conn.close()

    counts = Counter(sentiments)

    return [{"sentiment": k, "count": v} for k, v in counts.items()]


# -------------------------------
# TOP USER QUERIES
# -------------------------------

def get_top_queries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, COUNT(*) as count
        FROM chat_history
        GROUP BY message
        ORDER BY count DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return [{"query": r[0], "count": r[1]} for r in rows]


# -------------------------------
# FEEDBACK STATS
# -------------------------------

def get_feedback_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT rating FROM feedback")

    ratings = [row[0] for row in cursor.fetchall()]

    conn.close()

    helpful = ratings.count(1)
    not_helpful = ratings.count(-1)

    return {
        "helpful": helpful,
        "not_helpful": not_helpful
    }


# -------------------------------
# SUBMIT FEEDBACK
# -------------------------------

def save_feedback(message, response, rating):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback(message, response, rating)
        VALUES (?, ?, ?)
    """, (message, response, rating))

    conn.commit()
    conn.close()

    return {"status": "saved"}