from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def ingest():
    print("Data ingestion done")

def preprocess():
    os.system("python model/preprocess.py")

def train():
    os.system("python model/train.py")

default_args = {
    "start_date": datetime(2024, 1, 1)
}

with DAG("ml_pipeline", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    t1 = PythonOperator(task_id="ingest", python_callable=ingest)
    t2 = PythonOperator(task_id="preprocess", python_callable=preprocess)
    t3 = PythonOperator(task_id="train", python_callable=train)

    t1 >> t2 >> t3
🤖 4. MLflow Integrated Training
model/train.py
Python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

X = ["good python developer", "bad communication"]
y = [1, 0]

mlflow.set_experiment("hiring-bias")

with mlflow.start_run():
    vec = TfidfVectorizer()
    X_vec = vec.fit_transform(X)

    model = RandomForestClassifier()
    model.fit(X_vec, y)

    acc = model.score(X_vec, y)

    mlflow.log_param("model", "RandomForest")
    mlflow.log_metric("accuracy", acc)

    mlflow.sklearn.log_model(model, "model")

    pickle.dump(model, open("model/model.pkl", "wb"))
