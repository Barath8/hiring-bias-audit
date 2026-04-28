import streamlit as st
import requests

st.title("Hiring Bias Audit System")

text = st.text_area("Paste Resume")

if st.button("Analyze"):
    res = requests.post(
        "http://localhost:8000/predict",
        json={"text": text}
    ).json()

    st.write("Prediction:", res["prediction"])

    if res["bias_flag"]:
        st.error("⚠️ Bias Detected")
    else:
        st.success("No Bias Detected")

    # Feedback
    feedback = st.radio("Was this fair?", ["Yes", "No"])

    if st.button("Submit Feedback"):
        with open("feedback.csv", "a") as f:
            f.write(f"{text},{feedback}\n")
        st.success("Feedback recorded")