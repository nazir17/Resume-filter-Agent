from fastapi import APIRouter, UploadFile
from app.schemas.resume_schema import JDRequest
from app.services.resume_service import set_job_description, process_resume, find_best_candidates
from app.services.resume_service import retrieve_candidates, get_ranked_candidates

router = APIRouter()

@router.post("/set_jd/")
async def set_jd(request: JDRequest):
    return set_job_description(request.job_description)

@router.post("/upload_resume/")
async def upload_resume(file: UploadFile):
    return process_resume(file.file, file.filename)

@router.get("/top_candidates/")
async def top_candidates():
    return find_best_candidates()

@router.post("/rag_match/")
async def rag_match(request: JDRequest):
    top_candidates = retrieve_candidates(request.job_description)
    analysis = get_ranked_candidates(request.job_description, top_candidates)
    return {"result": analysis}