import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_embedding(text: str):
    model = "models/embedding-001"
    embedding = genai.embed_content(model=model, content=text, task_type="retrieval_document")
    return embedding["embedding"]
