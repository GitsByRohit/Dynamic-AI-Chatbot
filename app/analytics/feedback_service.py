from app.db.analytics_queries import insert_feedback, get_feedback_stats


# -------------------------------------------------
# SUBMIT FEEDBACK
# -------------------------------------------------

def submit_feedback(user_id: int, message: str, response: str, rating: str):
    """
    Stores user feedback for chatbot responses.
    
    rating values:
    - helpful
    - not_helpful
    """

    if rating not in ["helpful", "not_helpful"]:
        raise ValueError("Invalid rating value")

    insert_feedback(user_id, message, response, rating)

    return {
        "status": "success",
        "message": "Feedback submitted successfully"
    }


# -------------------------------------------------
# GET FEEDBACK ANALYTICS
# -------------------------------------------------

def get_feedback_distribution():
    """
    Returns feedback statistics for analytics dashboard.
    """

    stats = get_feedback_stats()

    result = {
        "helpful": 0,
        "not_helpful": 0
    }

    for item in stats:
        if item["rating"] == "helpful":
            result["helpful"] = item["count"]

        elif item["rating"] == "not_helpful":
            result["not_helpful"] = item["count"]

    return result


# -------------------------------------------------
# GET NEGATIVE FEEDBACK QUERIES
# -------------------------------------------------

def get_negative_feedback_queries(limit=10):
    """
    Returns queries that users rated as not helpful.
    Useful for improving chatbot training data.
    """

    from app.db.database import get_db_connection

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response
        FROM feedback
        WHERE rating = 'not_helpful'
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    conn.close()

    return [
        {
            "message": row[0],
            "response": row[1]
        }
        for row in data
    ]