## HR AI Agent for Resume Checker
### Project Overview 

The HR AI Agent for Resume Checker is designed to automatically analyze resumes against job descriptions and 
generate a compatibility score. The system extracts candidate details, required skills, and experience from 
uploaded resumes and job descriptions, then computes a matching score and generates a concise summary using an LLM.

---
project structure
```
work flow
    A[Upload JD & Resumes] --> B[Extract Text]
    B --> C[Parse Skills & Experience]
    C --> D[Score Candidates]
    D --> E[Generate Summary via Groq LLM]
    E --> F[Display Ranked Table]
    F --> G[Schedule Interview via Calendar API]
    G --> H[Send Email via Yagmail]
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

Add Google Calendar credentials

* Download credentials.json from Google Cloud Console
* Place it in your project directory
  
Run the App

* streamlit run app.py

LLM Platforms

* Groq LLaMA 3 (8B) → Used to generate candidate-job match summaries
* Future Enhancements: Upgrade to GPT-4 or larger LLaMA 3 models
---
Tools

- pdfplumber
- python-docx
- re (Regex)
- Streamlit
- google-api-python-client
- google-auth-oauthlib
- Yagmail
- datetime
