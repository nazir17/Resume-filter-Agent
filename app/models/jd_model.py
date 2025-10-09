from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.configs.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String(36), primary_key=True, index=True)
    position = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
