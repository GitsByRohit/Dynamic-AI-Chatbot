from app.models.ml_model import IntentModel

model = IntentModel()
model.train("data/intents.json")
model.save()

print("✅ Model trained successfully")