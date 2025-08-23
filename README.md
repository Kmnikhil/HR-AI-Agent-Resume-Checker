## HR AI Agent for Resume Checker
### Project Overview 

The HR AI Agent for Resume Checker is designed to automatically analyze resumes against job descriptions and 
generate a compatibility score. The system extracts candidate details, required skills, and experience from 
uploaded resumes and job descriptions, then computes a matching score and generates a concise summary using an LLM.

---
project structure
```
📁 hr-ai-agent-resume-checker
│-- 📄 app.py                     # Main Streamlit app (UI for uploading JD & resumes)
│-- 📄 agents.py                  # Python functions (extract JD, extract resume, score calculation)
│-- 📄 llm_summary.py             # LLaMA 3 (Groq) integration for candidate summary
│-- 📄 text_extractors.py         # Utilities using pdfplumber, python-docx, regex
│-- 📄 requirements.txt           # Dependencies
│-- 📄 README.md                  # Project documentation
```
Development Environment

* Language: Python
* IDE: Visual Studio Code (VSCode)
* Environment Management: venv
---
  
Web Frameworks

* Streamlit: Used to build the interactive user interface.
* Upload job description and resume files (.pdf, .docx, .txt)
* Display results in a table with candidate details, score, skills, and summary
---
  
AI & ML Frameworks
* Customized Python functions for skill and experience extraction
  
Agentic AI Frameworks
* Currently, the project simulates agents through Python functions:
* extract_details_from_jd → Extracts required skills and experience from job description
* extract_details_from_resume → Extracts candidate details (skills, experience, contact info)
* score_resume → Calculates compatibility score between JD and resume

**Future Plan: Integrate CrewAI for autonomous, collaborative agents** 


LLM Platforms

* Groq LLaMA 3 (8B) → Used to generate candidate-job match summaries
* Future Enhancements: Upgrade to GPT-4 or larger LLaMA 3 models
---
Tools

* pdfplumber → Extracts text from PDF resumes

* python-docx → Extracts text from DOCX resumes

* Regex (re) → Structured text extraction (skills, years of experience, etc.)

* Streamlit → Interactive front-end
