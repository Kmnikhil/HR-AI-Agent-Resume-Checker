import re
import os

# Predefined skills list
skills_list = ["Python", "Java", "C++", "JavaScript", "R", "PHP", "Swift", "Kotlin", 
               "SQL","Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", 
               "PyTorch", "Scikit-learn", "Pandas", "NumPy","AWS", "Azure", "GCP", "Docker", 
               "Kubernetes", "Jenkins", "CI/CD", "Terraform", "Ansible", "Linux","HTML", 
               "CSS", "JavaScript", "React", "Angular", "Vue", "Node.js", "Django", "Flask", 
               "Spring Boot","MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
               "Communication", "Problem-Solving", "Leadership", "Teamwork", "Critical Thinking", 
               "Adaptability"]

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{7,}\d")
NAME_RE = re.compile(r"^[A-Z][a-z]+\s[A-Z][a-z]+", re.MULTILINE)

def extract_details_from_jd(jd_text: str):
    # Extract skills
    found_skills = [skill for skill in skills_list if skill.lower() in jd_text.lower()]

    # Extract experience
    pattern = r'(\d+)\+?\s\n*(?:years|yrs)'
    experience = re.findall(pattern, jd_text, re.IGNORECASE)

    # Format output
    jd_result = {
        "skills": found_skills,
        "experience_years": {skill: int(years) for years, skill in experience}
    }
    return jd_result

def extract_details_from_resume(resume_text: str):
    # Extract skills
    found_skills = [skill for skill in skills_list if skill.lower() in resume_text.lower()]

    # Extract experience
    pattern = r'(\d+)\+?\s\n*(?:years|yrs)'
    experience = re.findall(pattern, resume_text, re.IGNORECASE)
    name = NAME_RE.search(resume_text)
    email = EMAIL_RE.search(resume_text)
    phone = PHONE_RE.search(resume_text)

    # Format output
    resume_result = {
        "name":name.group(0) if name else None,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": found_skills,
        # "experience_years": {skill: int(years) for years, skill in experience},
        "experience_years": [int(y) for y in experience]

    }
    return resume_result

def score_resume(jd_result, resume_result):
    matched = set(jd_result['skills']).intersection(resume_result['skills'])
    score_result = {
        "matched": list(matched),
        "score": round(len(matched) / max(len(jd_result['skills']), 1) * 100, 2) if resume_result else 0
    }
    return score_result
