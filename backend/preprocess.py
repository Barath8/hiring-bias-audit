def validate_resume(parsed):
    if len(parsed["skills"]) == 0:
        return False, "No skills found"
    if len(parsed["education"]) == 0:
        return False, "Education missing"
    return True, "Valid"


def preprocess(parsed):
    skills = " ".join(parsed["skills"])
    education = " ".join(parsed["education"])
    experience = f"{parsed['experience']} years"

    return f"{skills} {education} {experience}"