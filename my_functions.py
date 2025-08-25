import re
import pdfplumber
from io import BytesIO
from docx import Document

def extract_text_fromfile(file_bytes: bytes, file_type: str) -> str:
    text = ""
    if file_type=="pdf":
        try:
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                text = "\n".join(pages)
        except Exception as e:
            text = f"Error reading PDF: {e}"

    elif file_type=="docx":
        # DOCX extraction
        doc = Document(BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs)

    elif file_type=="txt":
        # TXT extraction
        text = file_bytes.decode("utf-8", errors="ignore")

    else:
        raise ValueError(f"Unsupported file type Please upload PDF, DOCX, or TXT.")

    return text

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
    # jd_text = input.get("jd_text") or next(iter(input.values()))

    # Extract skills
    found_skills = [skill for skill in skills_list if skill.lower() in jd_text.lower()]

    # Extract experience
    # pattern = r'(\d+)\+?\s\n*(?:years|yrs)'
    pattern = r'(\d+)\+?\s*(?:years|yrs|year|yr)(?:\s+of\s+experience)?'
    experience = re.findall(pattern, jd_text, re.IGNORECASE)

    # Format output
    jd_result = {
        "skills": found_skills,
        "experience_years": [int(y) for y in experience] if experience else []
    }
    return jd_result

def extract_details_from_resume(resume_text: str):
    # resume_text = input.get("resume_text") or next(iter(input.values()))

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
    # Match skills
    matched = list(set(jd_result['skills']).intersection(resume_result['skills']))
    
    # Skill score (weight 70)
    skill_score = round(len(matched) / max(len(jd_result['skills']), 1) * 70, 2)
    
    # Experience score (weight 30)
    jd_exp = jd_result['experience_years']
    candidate_exp = resume_result.get('experience_years', 0)
    
    if candidate_exp:
        exp_score = min(candidate_exp / jd_exp, 1) * 30
    else:
        exp_score = 0
    
    total_score = round(skill_score + exp_score)
    
    return {
        "matched": matched,
        "score": total_score
    }


def extract_score(summary):
    # summary_text = summary.get('summary') 
    # regex to extract percentage value
    match = re.search(r'(\d+)%', str(summary))

    if match:
        score = int(match.group(1))
        return score
    else:
        return []
    

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        r'D:\Works\resume_checker_agent\Agent_logic&LLM\credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)
    return service

def schedule_interview(name, email, start_datetime):
    service = get_calendar_service()
    end_datetime = start_datetime + timedelta(hours=1)  # default 1-hour interview

    event = {
        'summary': f'Interview: {name}',
        'description': 'Interview scheduled via Streamlit Resume App',
        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': email}],
        'reminders': {'useDefault': True},
    }

    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    print(f"Event created: {event.get('htmlLink')}")

import os
import yagmail
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

def send_email(name, email, datetime):
    yag = yagmail.SMTP(user=EMAIL, password=PASSWORD)
    subject = "Interview Scheduled"
    body = f"Dear {name},\n\nYour interview is scheduled on {datetime}.\n\nBest regards,\nHR Team"
    yag.send(to=email, subject=subject, contents=body)
