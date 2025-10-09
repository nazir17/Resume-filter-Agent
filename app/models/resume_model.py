from sqlalchemy import Column, String, Float, ForeignKey
from app.configs.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255))
    contact = Column(String(255))
    skills = Column(String(1000))
    match_percentage = Column(Float)
    reason = Column(String(1000))

    jd_id = Column(String(36), ForeignKey("job_descriptions.id"))
    position = Column(String(255))