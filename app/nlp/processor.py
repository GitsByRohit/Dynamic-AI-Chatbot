from app.nlp.intent import get_intent
from app.nlp.ner import extract_entities
from app.nlp.response import get_response, match_intent
from app.nlp.sentiment import analyze_sentiment


def process_message(user_input):
    intent_name = get_intent(user_input)

    intent_data = match_intent(intent_name)

    entities = extract_entities(user_input, intent_data) if intent_data else {}

    response = get_response(intent_name, user_input, entities)

    sentiment = analyze_sentiment(user_input)

    return {
        "intent": intent_name,
        "entities": entities,
        "sentiment": sentiment,
        "response": response
    }