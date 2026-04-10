from fastapi import APIRouter, Depends

from app.auth.utils import get_current_user

from app.db.analytics_queries import (
    get_total_chats,
    get_active_users,
    get_intent_distribution,
    get_sentiment_distribution,
    get_top_queries,
    get_fallback_rate
)

from app.analytics.analytics_engine import (
    get_chat_trend,
    get_chat_volume_by_hour,
    get_most_active_users
)

from app.analytics.feedback_service import (
    submit_feedback,
    get_feedback_distribution,
    get_negative_feedback_queries
)


router = APIRouter(prefix="/analytics", tags=["Analytics"])


# -------------------------------------------------
# BASIC STATS
# -------------------------------------------------

@router.get("/stats")
def get_basic_stats(current_user=Depends(get_current_user)):

    return {
        "total_chats": get_total_chats(),
        "active_users": get_active_users(),
        "fallback_rate": get_fallback_rate()
    }


# -------------------------------------------------
# INTENT DISTRIBUTION
# -------------------------------------------------

@router.get("/intent-distribution")
def intent_distribution(current_user=Depends(get_current_user)):

    return get_intent_distribution()


# -------------------------------------------------
# SENTIMENT DISTRIBUTION
# -------------------------------------------------

@router.get("/sentiment-distribution")
def sentiment_distribution(current_user=Depends(get_current_user)):

    return get_sentiment_distribution()


# -------------------------------------------------
# CHAT TREND
# -------------------------------------------------

@router.get("/chat-trend")
def chat_trend(current_user=Depends(get_current_user)):

    return get_chat_trend()


# -------------------------------------------------
# CHAT VOLUME BY HOUR
# -------------------------------------------------

@router.get("/chat-volume-hour")
def chat_volume_hour(current_user=Depends(get_current_user)):

    return get_chat_volume_by_hour()


# -------------------------------------------------
# MOST ACTIVE USERS
# -------------------------------------------------

@router.get("/active-users")
def active_users(current_user=Depends(get_current_user)):

    return get_most_active_users()


# -------------------------------------------------
# TOP USER QUERIES
# -------------------------------------------------

@router.get("/top-queries")
def top_queries(current_user=Depends(get_current_user)):

    return get_top_queries()


# -------------------------------------------------
# FEEDBACK SUBMISSION
# -------------------------------------------------

@router.post("/feedback")
def feedback(data: dict, current_user=Depends(get_current_user)):

    user_id = current_user["id"]

    message = data.get("message")
    response = data.get("response")
    rating = data.get("rating")

    return submit_feedback(user_id, message, response, rating)


# -------------------------------------------------
# FEEDBACK DISTRIBUTION
# -------------------------------------------------

@router.get("/feedback-stats")
def feedback_stats(current_user=Depends(get_current_user)):

    return get_feedback_distribution()


# -------------------------------------------------
# NEGATIVE FEEDBACK QUERIES
# -------------------------------------------------

@router.get("/negative-feedback")
def negative_feedback(current_user=Depends(get_current_user)):

    return get_negative_feedback_queries()