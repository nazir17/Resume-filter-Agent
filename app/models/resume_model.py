from sqlalchemy import Column, Integer, String, Float
from app.configs.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    contact = Column(String(255))
    skills = Column(String(1000))
    match_percentage = Column(Float)
    reason = Column(String(1000))