from app.models.ml_model import IntentModel

model = IntentModel()
model.load()  # now safe always

try:
    model.load()
except:
    pass


def get_intent(user_input):
    try:
        return model.predict(user_input)
    except:
        return "unknown"