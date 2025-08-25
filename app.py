import streamlit as st
import pdfplumber
from io import BytesIO
from docx import Document
import pandas as pd
import os
from groq import Groq
from my_functions import extract_text_fromfile, extract_details_from_jd, extract_details_from_resume, score_resume
from dotenv import load_dotenv
load_dotenv()

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
    jd_raw = extract_text_fromfile(jd_file.read(), jd_file_type)
    jd_result = extract_details_from_jd(jd_raw)
    results = []

    for resume in uploaded_files:
        file_type = resume.name.split(".")[-1].lower()
        resume_raw = extract_text_fromfile(resume.read(), file_type)
        resume_result = extract_details_from_resume(resume_raw)
        resume_score = score_resume(jd_result,resume_result)

        from build import resume_checker_crew
        inputs = {
                "jd_skills": jd_result['skills'],
                "jd_experience": jd_result['experience_years'],
                "resume_name": resume_result['name'],
                "resume_email": resume_result['email'],
                "resume_phone": resume_result['phone'],
                "resume_skills": resume_result['skills'],
                "resume_experience": resume_result['experience_years'],
                "resume_score":resume_score['score']
            }


        crew_result = resume_checker_crew.kickoff(inputs=inputs)

        final_output = {
                        "Candidate Name": resume_result['name'],
                        "Candidate Email": resume_result['email'],
                        "Candidate Phone": resume_result['phone'],
                        "Candidate Skills": resume_result['skills'],
                        "Candidate Experience": resume_result['experience_years'],
                        "score": resume_score['score'],
                        "summary": crew_result.tasks_output[0].raw  # assuming task 1 is your summary_task


                        }
        
        results.append(final_output)

    df = pd.DataFrame(results)
    df_sorted = df.sort_values(by="score", ascending=False) 
    st.dataframe(df_sorted)
    import streamlit as st
    from datetime import datetime, timedelta
    import streamlit as st
    from datetime import datetime
    from my_functions import schedule_interview, send_email

    for idx, row in enumerate(results):
        st.write(f"Candidate: {row['Candidate Name']}, Email: {row['Candidate Email']}")

        interview_date = st.date_input(f"Select date for {row['Candidate Name']}", datetime.today(), key=f"date_{idx}")
        interview_time = st.time_input(f"Select time for {row['Candidate Name']}", datetime.now().time(), key=f"time_{idx}")
        interview_datetime = datetime.combine(interview_date, interview_time)

        if st.button(f"Schedule Interview for {row['Candidate Name']}", key=f"schedule_{idx}"):
            schedule_interview(row['Candidate Name'], row['Candidate Email'], interview_datetime)
            st.success(f"Interview scheduled for {row['Candidate Name']} on {interview_datetime}")

        if st.button(f"Send Email to {row['Candidate Name']}", key=f"email_{idx}"):
            send_email(row['Candidate Name'], row['Candidate Email'], interview_datetime)
            st.success(f"Email sent to {row['Candidate Name']} confirming interview on {interview_datetime}")
else:
    st.info("Please upload a Job Description and at least one Resume.")