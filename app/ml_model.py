import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

MODEL_PATH = "models/sensitivity_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

def train_model():
    data = pd.read_csv("data/training_data.csv")

    X = data["text"]
    y = data["label"]

    vectorizer = TfidfVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vectorized, y)

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model trained and saved.")

def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def predict(text):
    model, vectorizer = load_model()
    text_vectorized = vectorizer.transform([text])
    probability = model.predict_proba(text_vectorized)[0][1]
    return probability
