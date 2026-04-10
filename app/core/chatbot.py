from app.models.llm import generate_response
from app.nlp.processor import process_message
from app.core.memory import build_conversation_context


def get_chatbot_response(user_message: str, user_id: int = None):

    # Run NLP pipeline
    nlp_result = process_message(user_message)

    intent = nlp_result["intent"]

    # If rule engine handled it
    if intent != "Fallback":
        return {
            "intent": nlp_result["intent"],
            "entities": nlp_result["entities"],
            "sentiment": nlp_result["sentiment"],
            "response": nlp_result["response"]
        }

    # Use conversation memory if user_id is available
    if user_id:
        context = build_conversation_context(user_id, user_message)
    else:
        context = user_message

    # Generate AI response with context
    ai_response = generate_response(context)

    return {
        "intent": intent,
        "entities": nlp_result["entities"],
        "sentiment": nlp_result["sentiment"],
        "response": ai_response
    }