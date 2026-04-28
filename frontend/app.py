import streamlit as st
import requests

st.title("Hiring Bias Audit System")

# 🔹 Upload PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:

    if st.button("Analyze"):
        try:
            # 🔹 Send PDF to backend
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }

            res = requests.post(
                "http://localhost:8000/predict",
                files=files
            ).json()

            # 🔹 Handle errors safely
            if "error" in res:
                st.error(res["error"])
            else:
                st.write("Prediction:", res["prediction"])

                if res["bias_flag"]:
                    st.error("⚠️ Bias Detected")
                else:
                    st.success("No Bias Detected")

                # 🔹 Feedback
                feedback = st.radio("Was this fair?", ["Yes", "No"])

                if st.button("Submit Feedback"):
                    with open("feedback.csv", "a") as f:
                        f.write(f"{uploaded_file.name},{feedback}\n")

                    st.success("Feedback recorded")

        except Exception as e:
            st.error(f"Error: {str(e)}")