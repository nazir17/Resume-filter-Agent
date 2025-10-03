from pydantic import BaseModel
from typing import List


class JDRequest(BaseModel):
    job_description: str


class CandidateResponse(BaseModel):
    fit: str
    match_percentage: float
    name: str
    contact: str
    skills: List[str]
    reason: str

    class Config:
        orm_mode = True
