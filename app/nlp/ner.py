def extract_entities(user_input, intent_data):
    words = user_input.split()
    entities = {}

    for entity in intent_data.get("entities", []):
        name = entity["entity"]
        start = entity["rangeFrom"]
        end = entity["rangeTo"]

        value = " ".join(words[start:end])
        entities[name] = value

    return entities