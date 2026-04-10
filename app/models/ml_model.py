import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class IntentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)

    def train(self, path):
        with open(path, 'r') as file:
            data = json.load(file)

        texts = []
        labels = []

        for intent in data["intents"]:
            for sentence in intent["text"]:
                texts.append(sentence.lower())
                labels.append(intent["intent"])

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, text):
        X = self.vectorizer.transform([text.lower()])
        probs = self.model.predict_proba(X)

        max_prob = max(probs[0])
        predicted = self.model.predict(X)[0]

        print("Confidence:", max_prob)
        print("Predicted:", predicted)

        # ✅ IMPORTANT intents (never fallback)
        important_intents = [
            "Greeting",
            "GreetingResponse",
            "CourtesyGreeting",
            "CourtesyGreetingResponse",
            "AboutBot"
        ]

        # ✅ fallback only if:
        # low confidence AND not important intent
        if max_prob < 0.12 and predicted not in important_intents:
            return "Fallback"

        return predicted

    def save(self, path="app/models/model.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)  # ensure folder exists
        with open(path, "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

    def load(self, path="app/models/model.pkl", training_data="data/intents.json"):
        if os.path.exists(path):
            with open(path, "rb") as f:
                self.vectorizer, self.model = pickle.load(f)
            print("✅ Model loaded successfully")
        else:
            print("⚠️ Model not found. Training a new model...")
            self.train(training_data)
            self.save(path)
            print("✅ Model trained and saved automatically")