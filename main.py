from fastapi import FastAPI, UploadFile
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
import os
import PyPDF2
import docx
import json
from dotenv import load_dotenv



load_dotenv()


google_api_key = os.environ["GOOGLE_API_KEY"]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

app = FastAPI()

class JDRequest(BaseModel):
    job_description: str


job_description_text = ""


@app.post("/set_jd/")
async def set_job_description(request: JDRequest):
    global job_description_text
    job_description_text = request.job_description
    return {"message": "Job description set successfully"}


def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text


@app.post("/upload_resume/")
async def upload_resume(file: UploadFile):
    global job_description_text
    if not job_description_text:
        return {"error": "Please set a job description first!"}

    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file.file)
    else:
        resume_text = (await file.read()).decode("utf-8")

    prompt = f"""
    You are a recruitment AI. 
    Compare the following resume with the given Job Description.

    Job Description:
    {job_description_text}

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
        text = text[text.find("{") : text.rfind("}") + 1]
        result = json.loads(text)

    return result
