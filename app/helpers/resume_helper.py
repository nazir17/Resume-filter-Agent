import PyPDF2
import docx
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


google_api_key = os.getenv("GOOGLE_API_KEY")

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, google_api_key=google_api_key)

def analyze_resume(job_description: str, resume_text: str):
    prompt = f"""
    You are a recruitment AI. 
    Compare the following resume with the given Job Description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Task:
    Return ONLY valid JSON in this format:
    {{
      "fit": "Yes" or "No",
      "match_percentage": number (0-100),
      "name": "candidate name or unknown",
      "contact": "contact details or unknown",
      "skills": ["list", "of", "skills"],
      "reason": "short explanation"
    }}
    """

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        text = response.content.strip()
        text = text[text.find("{"): text.rfind("}") + 1]
        result = json.loads(text)

    return result
