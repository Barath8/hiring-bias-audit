import pandas as pd
import pickle
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

mlflow.set_experiment("hiring-bias-audit")

df = pd.read_csv("data/processed/train.csv")

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

with mlflow.start_run():

    # Vectorizer
    vec = TfidfVectorizer()
    X_train_vec = vec.fit_transform(X_train)
    X_test_vec = vec.transform(X_test)

    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_vec, y_train)

    preds = model.predict(X_test_vec)

    acc = accuracy_score(y_test, preds)

    # MLflow logs
    mlflow.log_metric("accuracy", acc)
    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("vectorizer", "TFIDF")

    # Save artifacts to MLflow
    mlflow.sklearn.log_model(model, "model")

    # Local fallback save (for FastAPI)
    pickle.dump(model, open("model/model.pkl", "wb"))
    pickle.dump(vec, open("model/vectorizer.pkl", "wb"))

print("Model trained + logged to MLflow ✅")