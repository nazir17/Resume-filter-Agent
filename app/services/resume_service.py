from sqlalchemy.orm import Session
from app.helpers.resume_helper import analyze_resume, extract_text_from_pdf, extract_text_from_docx
from app.models.resume_model import Candidate

job_description_text = "" 

def set_job_description(jd: str):
    global job_description_text
    job_description_text = jd
    return {"message": "Job description set successfully"}

def process_resume(file, filename: str, db: Session):
    global job_description_text
    if not job_description_text:
        return {"error": "Please set a job description first!"}

    
    if filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file)
    else:
        resume_text = file.read().decode("utf-8")

    
    result = analyze_resume(job_description_text, resume_text)

    
    if result["fit"].lower() == "yes":
        candidate = Candidate(
            name=result.get("name", "unknown"),
            contact=result.get("contact", "unknown"),
            skills=",".join(result.get("skills", [])),
            match_percentage=result.get("match_percentage", 0),
            reason=result.get("reason", "")
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    return result
