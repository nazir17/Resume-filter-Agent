from app.helpers.resume_helper import (
    analyze_resume,
    extract_text_from_pdf,
    extract_text_from_docx,
    save_candidate_to_db,
    fetch_top_candidates,
    save_jd_to_db
)

job_description_text = ""


def process_jd_and_resumes(position: str, job_description: str, files: list):
    global job_description_text
    job_description_text = job_description

    jd = save_jd_to_db(position, job_description_text)
    analyzed_results = []

    for file_obj in files:
        filename = file_obj.filename

        
        if filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_obj.file)
        elif filename.endswith(".docx"):
            resume_text = extract_text_from_docx(file_obj.file)
        else:
            resume_text = file_obj.file.read().decode("utf-8")

        
        result = analyze_resume(job_description_text, resume_text)
        analyzed_results.append(result)

    
        if result["fit"].lower() == "yes":
            save_candidate_to_db(result, jd.id, position)

    return {"message": "Resumes analyzed successfully", "results": analyzed_results}


def find_best_candidates(top_k=5):
    results = fetch_top_candidates(top_k)
    return {"top_matches": results}