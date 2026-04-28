import re

SKILLS = ["python", "java", "sql", "machine learning", "deep learning", "react"]

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS if skill in text_lower]

def extract_education(text):
    edu_keywords = ["b.tech", "m.tech", "bsc", "msc", "phd", "iit", "nit"]
    text_lower = text.lower()
    return [edu for edu in edu_keywords if edu in text_lower]

def extract_experience(text):
    match = re.search(r'(\d+)\s+years', text.lower())
    return int(match.group(1)) if match else 0

def parse_resume(text):
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }