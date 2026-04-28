import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

mlflow.set_experiment("hiring-bias")

df = pd.read_csv("data/processed/train.csv")

X = df["text"]
y = df["label"]

with mlflow.start_run():
    vec = TfidfVectorizer()
    X_vec = vec.fit_transform(X)

    model = RandomForestClassifier()
    model.fit(X_vec, y)

    acc = model.score(X_vec, y)

    mlflow.log_metric("accuracy", acc)

    # ✅ Save BOTH
    pickle.dump(model, open("model/model.pkl", "wb"))
    pickle.dump(vec, open("model/vectorizer.pkl", "wb"))

print("Model trained")