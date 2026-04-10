import json
import random

with open("data/intents.json") as file:
    data = json.load(file)

context_state = None
memory = {}


def match_intent(intent_name):
    for intent in data["intents"]:
        if intent["intent"] == intent_name:
            return intent
    return None


def handle_context(intent):
    global context_state

    ctx = intent.get("context", {})

    # Check if valid context
    if ctx.get("in") and ctx["in"] != context_state:
        return False

    # Update context
    if ctx.get("out"):
        context_state = ctx["out"]

    if ctx.get("clear"):
        context_state = None

    return True


def fill_entities(response, entities):
    for key, value in entities.items():
        response = response.replace(f"<{key}>", value)
        response = response.replace(f"%%{key}%%", value)
    return response


def handle_extension(intent, entities):
    ext = intent.get("extension", {})

    if not ext["function"]:
        return None

    # Example: Time extension
    if "gTime.getTime" in ext["function"]:
        from datetime import datetime
        time = datetime.now().strftime("%H:%M")
        return random.choice(ext["responses"]).replace("%%TIME%%", time)

    # Example: Human memory
    if "updateHuman" in ext["function"]:
        memory["HUMAN"] = entities.get("HUMAN", "User")
        return random.choice(ext["responses"]).replace("%%HUMAN%%", memory["HUMAN"])

    if "getCurrentHuman" in ext["function"]:
        name = memory.get("HUMAN", "User")
        return random.choice(ext["responses"]).replace("%%HUMAN%%", name)

    return None


def get_response(intent_name, user_input, entities):
    intent = match_intent(intent_name)

    if not intent:
        return "Sorry, I didn't understand."

    # Context check
    if not handle_context(intent):
        return "Please follow the conversation flow."

    # Extension first
    ext_response = handle_extension(intent, entities)
    if ext_response:
        return ext_response

    response = random.choice(intent["responses"])

    # Fill entities
    response = fill_entities(response, entities)

    return response