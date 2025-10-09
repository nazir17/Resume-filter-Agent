from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.resume_schema import JDRequest
from app.services.resume_service import process_jd_and_resumes, find_best_candidates
from typing import List

router = APIRouter()



@router.post("/upload_resume/")
async def upload_resumes_with_jd(
    position: str = Form(...),
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):

    result = process_jd_and_resumes(position, job_description, files)
    return result

@router.get("/top_candidates/")
async def top_candidates():
    return find_best_candidates()
