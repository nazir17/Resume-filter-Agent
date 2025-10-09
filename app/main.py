from fastapi import FastAPI
from app.configs.database import Base, engine
from app.controllers import register_routers


app = FastAPI(title="Resume Screening API")

Base.metadata.create_all(bind=engine)

register_routers(app)