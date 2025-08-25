from crewai import Crew, Process, Agent, Task, LLM
import os
from dotenv import load_dotenv
load_dotenv()

groq_llm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
    api_base="https://api.groq.com/openai/v1" 
)

# -------------------------------------------------
"""Agents"""

summary_agent = Agent(
    role="Summary Writer",
    goal="Write a short 2–3 sentence summary of the candidate evaluation focusing on skills, experience, and fit.",
    backstory="An HR assistant that creates concise summaries for recruiters.",
    llm=groq_llm ,
    verbose=True
)
# -------------------------------------------------

"""Tasks"""

summary_task = Task(
    description="""
    You are a hiring assistant. Summarize the following candidate evaluation in 2–3 concise sentences:
    - Job Description Skills: {jd_skills}
    - Job Description Experience Required: {jd_experience}
    - Candidate Name: {resume_name}
    - Candidate Email: {resume_email}
    - Candidate Phone: {resume_phone}
    - Candidate Skills: {resume_skills}
    - Candidate Experience: {resume_experience}
    - Candidate Score: {resume_score}
    Assessment: 2–3 sentences summarizing alignment between candidate’s skills and job requirements

    Conclusion: Summarize how well this candidate fits the job.
    """,
    agent=summary_agent,
    expected_output="A 2–3 sentence professional summary of the candidate’s suitability for the role."
)

# -------------------------------------------------
"""Crew"""
resume_checker_crew = Crew(
    agents=[summary_agent],
    tasks=[summary_task],
    process=Process.sequential  
)
