import os
import pandas as pd
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.parser import parse_resume

os.makedirs("data/processed", exist_ok=True)

raw_resumes = [
    "B.Tech student with Python and ML experience 3 years",
    "No skills and no education",
    "M.Tech from IIT with Java experience 2 years",
    "College dropout no experience"
]

labels = [1, 0, 1, 0]

processed_data = []

for text, label in zip(raw_resumes, labels):
    parsed = parse_resume(text)

    processed_text = (
        " ".join(parsed["skills"]) + " " +
        " ".join(parsed["education"]) + " " +
        f"{parsed['experience']} years"
    )

    processed_data.append({
        "text": processed_text.strip(),
        "label": label
    })

df = pd.DataFrame(processed_data)
df.to_csv("data/processed/train.csv", index=False)

print("Training data created")