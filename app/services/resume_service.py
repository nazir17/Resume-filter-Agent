from app.helpers.resume_helper import analyze_resume, extract_text_from_pdf, extract_text_from_docx
from app.helpers.embedding_helper import get_gemini_embedding
from app.configs.pinecone_config import index
import uuid
from app.helpers.resume_helper import analyze_top_candidates


job_description_text = ""
job_description_vector = None

def set_job_description(jd: str):
    global job_description_text, job_description_vector
    job_description_text = jd
    job_description_vector = get_gemini_embedding(jd)
    return {"message": "Job description set successfully"}

def process_resume(file, filename: str):
    global job_description_text, job_description_vector
    if not job_description_text:
        return {"error": "Please set a job description first!"}

    if filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file)
    else:
        resume_text = file.read().decode("utf-8")

    result = analyze_resume(job_description_text, resume_text)

    if result["fit"].lower() == "yes":
        vector = get_gemini_embedding(resume_text)
        candidate_id = str(uuid.uuid4())

        index.upsert(vectors=[{
            "id": candidate_id,
            "values": vector,
            "metadata": {
                "name": result.get("name", "unknown"),
                "contact": result.get("contact", "unknown"),
                "skills": ",".join(result.get("skills", [])),
                "match_percentage": result.get("match_percentage", 0),
                "reason": result.get("reason", "")
            }
        }])

    return result

def find_best_candidates(top_k=5):
    global job_description_vector
    if job_description_vector is None:
        return {"error": "Please set a job description first!"}

    results = index.query(vector=job_description_vector, top_k=top_k, include_metadata=True)
    matches = []
    for r in results["matches"]:
        matches.append({
            "name": r["metadata"]["name"],
            "contact": r["metadata"]["contact"],
            "skills": r["metadata"]["skills"],
            "match_percentage": r["metadata"]["match_percentage"],
            "reason": r["metadata"]["reason"],
            "score": r["score"]
        })
    return {"top_matches": matches}


def retrieve_candidates(query: str, top_k=5):
    query_vector = get_gemini_embedding(query)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return results["matches"]



def get_ranked_candidates(job_description, candidate_list):
    return analyze_top_candidates(job_description, candidate_list)
