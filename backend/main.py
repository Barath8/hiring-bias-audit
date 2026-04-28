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

MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

try:
    model = pickle.load(open(MODEL_PATH, "rb"))
    vectorizer = pickle.load(open(VEC_PATH, "rb"))
    print("Model loaded ✅")
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
        parsed = parse_resume(pdf_bytes, is_pdf=True)

        valid, msg = validate_resume(parsed)
        if not valid:
            ERRORS.inc()
            return {"error": msg}

        clean_text = preprocess(parsed)
        base_pred = predict(clean_text)

        male_text = clean_text.replace("she", "he")
        female_text = clean_text.replace("he", "she")

        pred_m = predict(male_text)
        pred_f = predict(female_text)

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