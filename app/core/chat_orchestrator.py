from app.nlp.processor import process_message
from app.models.llm import generate_response

from app.core.memory import build_prompt

from app.db.chat_queries import save_chat


# -----------------------------------------
# MAIN CHAT PROCESSOR
# -----------------------------------------

def process_chat(user_id: int, user_message: str, conversation_id: int):
    """
    Main chatbot pipeline controller.
    """

    # -----------------------------------------
    # STEP 1 — NLP PROCESSING
    # -----------------------------------------

    nlp_result = process_message(user_message)

    intent = nlp_result["intent"]
    entities = nlp_result["entities"]
    sentiment = nlp_result["sentiment"]
    rule_response = nlp_result["response"]

    # -----------------------------------------
    # STEP 2 — RULE ENGINE DECISION
    # -----------------------------------------

    if intent != "Fallback":

        response = rule_response

    else:

        # -----------------------------------------
        # STEP 3 — BUILD CONTEXT PROMPT
        # -----------------------------------------

        prompt = build_prompt(user_message, user_id, conversation_id)

        # -----------------------------------------
        # STEP 4 — LLM RESPONSE
        # -----------------------------------------

        response = generate_response(prompt)

    # -----------------------------------------
    # STEP 5 — SAVE CHAT HISTORY
    # -----------------------------------------

    save_chat(user_id, user_message, response, intent, sentiment, conversation_id)

    # -----------------------------------------
    # STEP 6 — RETURN RESPONSE
    # -----------------------------------------

    return {
        "intent": intent,
        "entities": entities,
        "sentiment": sentiment,
        "response": response
    }