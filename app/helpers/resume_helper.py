import PyPDF2
import docx
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from app.configs.database import SessionLocal
from app.models.resume_model import Candidate
from app.models.jd_model import JobDescription
import uuid

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


def save_jd_to_db(position: str, description: str):
    db = SessionLocal()
    jd_id = str(uuid.uuid4())
    jd = JobDescription(id=jd_id, position=position, description=description)
    db.add(jd)
    db.commit()
    db.refresh(jd)
    db.close()
    return jd


def save_candidate_to_db(result: dict, jd_id: str, position: str):
    db = SessionLocal()
    candidate = Candidate(
        id=str(uuid.uuid4()),
        name=result.get("name", "unknown"),
        contact=result.get("contact", "unknown"),
        skills=json.dumps(result.get("skills", [])),
        match_percentage=result.get("match_percentage", 0),
        reason=result.get("reason", ""),
        jd_id=jd_id,
        position=position
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    db.close()


def fetch_top_candidates(top_k=5):
    db = SessionLocal()
    candidates = db.query(Candidate).order_by(Candidate.match_percentage.desc()).limit(top_k).all()
    db.close()
    results = [
        {
            "name": c.name,
            "contact": c.contact,
            "skills": json.loads(c.skills),
            "match_percentage": c.match_percentage,
            "reason": c.reason,
            "position": c.position,
            "jd_id": c.jd_id
        }
        for c in candidates
    ]
    return results
