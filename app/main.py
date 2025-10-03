from fastapi import FastAPI
from app.controllers import register_routers


app = FastAPI(title="Resume Screening API")

register_routers(app)