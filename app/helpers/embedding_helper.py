import os
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_embedding(text: str):
    model = "models/embedding-001"
    embedding = genai.embed_content(model=model, content=text, task_type="retrieval_document")
    return embedding["embedding"]


# def get_embedding(text: str):
#     response = client.embeddings.create(
#         input=text,
#         model="text-embedding-3-small"
#     )
#     return response.data[0].embedding