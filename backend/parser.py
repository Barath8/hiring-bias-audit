import re
from io import BytesIO
from PyPDF2 import PdfReader

SKILLS = ["python", "java", "sql", "machine learning", "deep learning", "react"]

# -------------------------------
# 🔹 PDF TEXT EXTRACTION
# -------------------------------
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# -------------------------------
# 🔹 FEATURE EXTRACTION
# -------------------------------
def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS if skill in text_lower]

def extract_education(text):
    text_lower = text.lower()

    patterns = [
        r"(b\.?tech|m\.?tech|bsc|msc|phd)",
        r"(institute|university|college)"
    ]

    found = []
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        found.extend(matches)

    return list(set(found))
    
def extract_experience(text):
    match = re.search(r'(\d+)\s+years', text.lower())
    return int(match.group(1)) if match else 0

def validate_resume(parsed):
    if len(parsed["skills"]) == 0:
        return False, "No skills found"

    # Relax education rule
    if len(parsed["education"]) == 0:
        return True, "Warning: Education not clearly detected"

    return True, "Valid"

# -------------------------------
# 🔹 MAIN PARSER
# -------------------------------
def parse_resume(input_data, is_pdf=False):
    """
    input_data:
        - if is_pdf=True → bytes (PDF file)
        - else → string (resume text)
    """

    if is_pdf:
        text = extract_text_from_pdf(input_data)
    else:
        text = input_data

    return {
        "text": text,   
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }