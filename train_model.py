import pandas as pd, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier

os.makedirs("model", exist_ok=True)

data = {
    "text": [
        "Aliens spotted in New York.",
        "COVID vaccines save lives.",
        "5G towers spread virus.",
        "Govt launches green energy scheme."
    ],
    "label": ["FAKE", "REAL", "FAKE", "REAL"]
}

df = pd.DataFrame(data)
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8)
X_train_tfidf = vectorizer.fit_transform(X_train)

model = PassiveAggressiveClassifier(max_iter=1000)
model.fit(X_train_tfidf, y_train)

joblib.dump(model, "model/fake_news_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model saved in /model")