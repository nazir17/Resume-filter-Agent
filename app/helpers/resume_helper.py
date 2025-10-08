import PyPDF2
import docx
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=google_api_key)


def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])



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



def analyze_top_candidates(job_description: str, candidates: list):
    candidate_texts = "\n\n".join([
        f"Name: {c['metadata']['name']}\nSkills: {c['metadata']['skills']}\nMatch %: {c['metadata']['match_percentage']}"
        for c in candidates
    ])

    prompt = f"""
    You are a recruitment assistant.
    Job Description: {job_description}

    Candidate data:
    {candidate_texts}

    Task:
    Rank the candidates by match percentage and give a short explanation why they are suitable.
    Return ONLY JSON in this format:
    [
      {{
        "name": "...",
        "skills": [...],
        "match_percentage": number,
        "reason": "..."
      }}
    ]
    """

    response = llm.invoke(prompt)
    return response.content
