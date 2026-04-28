from fastapi import FastAPI, Response
from pydantic import BaseModel
import pickle
from fastapi import UploadFile, File
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from backend.metrics import REQUESTS, ERRORS, BIAS
from backend.parser import parse_resume
from backend.preprocess import validate_resume, preprocess
app = FastAPI()

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    model = pickle.load(open(os.path.join(BASE_DIR, "model/model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(BASE_DIR, "model/vectorizer.pkl"), "rb"))
except Exception as e:
    print("Model loading failed:", e)
    model = None


class Resume(BaseModel):
    text: str


def predict(text):
    if model is None:
        raise Exception("Model not loaded")

    text_vec = vectorizer.transform([text])  # ✅ transform
    return model.predict(text_vec)[0]


# ✅ Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# ✅ Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ✅ Main API
@app.post("/predict")
async def predict_resume(file: UploadFile = File(...)):
    try:
        REQUESTS.inc()

        pdf_bytes = await file.read()

        # 🔹 Parse PDF
        parsed = parse_resume(pdf_bytes, is_pdf=True)

        # 🔹 Validate
        valid, msg = validate_resume(parsed)
        if not valid:
            ERRORS.inc()
            return {"error": msg}

        clean_text = preprocess(parsed)
        base_pred = predict(clean_text)

        # 🔹 Bias Simulation
        text = parsed["text"]

        male_text = text.replace("She", "He")
        female_text = text.replace("He", "She")

        pred_m = predict(preprocess(parse_resume(male_text)))
        pred_f = predict(preprocess(parse_resume(female_text)))

        bias = abs(pred_m - pred_f)
        BIAS.set(bias)

        return {
            "prediction": int(base_pred),
            "bias_score": float(bias),
            "bias_flag": bias > 0.2,
            "parsed_data": parsed
        }

    except Exception as e:
        ERRORS.inc()
        return {"error": str(e)}