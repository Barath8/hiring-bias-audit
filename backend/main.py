from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from metrics import REQUESTS, ERRORS, BIAS

from parser import parse_resume
from preprocess import validate_resume, preprocess

app = FastAPI()

model = pickle.load(open("model/model.pkl", "rb"))

class Resume(BaseModel):
    text: str

def predict(text):
    return model.predict([text])[0]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict_resume(resume: Resume):
    # 🔹 Parse
    parsed = parse_resume(resume.text)

    # 🔹 Validate
    valid, msg = validate_resume(parsed)
    if not valid:
        return {"error": msg}

    # 🔹 Preprocess
    clean_text = preprocess(parsed)

    # 🔹 Base Prediction
    base_pred = predict(clean_text)

    # 🔹 Bias Simulation
    male_text = resume.text.replace("She", "He")
    female_text = resume.text.replace("He", "She")

    parsed_m = parse_resume(male_text)
    parsed_f = parse_resume(female_text)

    pred_m = predict(preprocess(parsed_m))
    pred_f = predict(preprocess(parsed_f))

    bias = abs(pred_m - pred_f)
    
    BIAS.set(bias)

    return {
        "prediction": int(base_pred),
        "bias_score": float(bias),
        "bias_flag": bias > 0.2,
        "parsed_data": parsed
    }