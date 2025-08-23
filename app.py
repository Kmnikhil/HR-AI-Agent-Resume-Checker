import streamlit as st
import pdfplumber
from io import BytesIO
from docx import Document
import pandas as pd
import os
from groq import Groq
from agent import extract_details_from_jd, extract_details_from_resume, score_resume
from dotenv import load_dotenv
load_dotenv()

def extract_text(file_bytes: bytes, file_type: str) -> str:
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

st.title("Resume Ranking Prototype")

jd_file = st.file_uploader("Upload Job Description", type=["txt", "pdf", "docx"])
uploaded_files = st.file_uploader(
    "Upload resumes (select multiple files or drag-drop entire folder contents)", 
    type=["pdf", "docx"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Total files uploaded: {len(uploaded_files)}")
    for file in uploaded_files:
        st.write("📄", file.name)


if jd_file and uploaded_files:
    # Extract job description once
    jd_file_type = jd_file.name.split(".")[-1].lower()
    jd_raw = extract_text(jd_file.read(), jd_file_type)
    jd_text = extract_details_from_jd(jd_raw)
    results = []

    for resume in uploaded_files:
        file_type = resume.name.split(".")[-1].lower()
        resume_raw = extract_text(resume.read(), file_type)
        resume_text = extract_details_from_resume(resume_raw)

        match_score = score_resume(jd_text,resume_text)
        summary_prompt = f"""
                        You are a hiring assistant. Summarize the following candidate evaluation **in 2-3 concise sentences**, focusing on skills match, experience, and overall fit.

                        Job Description Skills: {jd_text['skills']}
                        Job Description Experience Required: {jd_text['experience_years']}

                        Candidate Name: {resume_text['name']}
                        Candidate Email: {resume_text['email']}
                        Candidate Phone: {resume_text['phone']}
                        Candidate Skills: {resume_text['skills']}
                        Candidate Experience: {resume_text['experience_years']}

                        Matched Skills: {match_score['matched']}
                        Match Score: {match_score['score']}

                        Summarize how well this candidate fits the job.
                        """
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "You are a helpful hiring assistant."},
                        {"role": "user", "content": summary_prompt}
                        ]
                    )
        summary = response.choices[0].message.content

        final_output = {
                        "Candidate Name": {resume_text['name']},
                        "Candidate Email": {resume_text['email']},
                        "Candidate Phone": {resume_text['phone']},
                        "Candidate Skills": resume_text['skills'],
                        "Candidate Match Score":{match_score['score']},
                        "Candidate Experience": resume_text['experience_years'],
                        "summary": summary
                        }
        results.append(final_output)
    # st.table(results)
    st.dataframe(pd.DataFrame(results))
else:
    st.info("Please upload a Job Description and at least one Resume.")