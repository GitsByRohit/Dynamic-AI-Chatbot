from fastapi import APIRouter

from app.analytics.service import (
    get_stats,
    get_chat_trend,
    get_intent_distribution,
    get_sentiment_distribution,
    get_top_queries,
    get_feedback_stats,
    save_feedback
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/stats")
def stats():
    return get_stats()


@router.get("/chat-trend")
def chat_trend():
    return get_chat_trend()


@router.get("/intent-distribution")
def intent_distribution():
    return get_intent_distribution()


@router.get("/sentiment-distribution")
def sentiment_distribution():
    return get_sentiment_distribution()


@router.get("/top-queries")
def top_queries():
    return get_top_queries()


@router.get("/feedback-stats")
def feedback_stats():
    return get_feedback_stats()


@router.post("/feedback")
def feedback(data: dict):

    message = data.get("message", "")
    response = data.get("response", "")
    rating = data.get("rating")

    return save_feedback(
        message,
        response,
        rating
    )