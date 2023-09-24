from flask import Flask, request, jsonify
from extraction import process_resume_data, preprocess_text, extract_text_from_pdf
from embeddings import get_embeddings

app = Flask(__name__)

@app.route("/resume_matcher", methods=["POST"])
def resume_matcher():
    try:
        job_description = request.form.get("job_description")
        resume_file = request.files["resume_file"]

        # Check if both job description and resume file are provided
        if not job_description or not resume_file:
            return jsonify({"error": "Please provide both a job description and a resume file."})

        # Read the uploaded resume PDF
        resume_text = extract_text_from_pdf(resume_file)

        # Preprocess job description and resume text
        job_description = preprocess_text(job_description)
        resume_text_features = preprocess_text(resume_text)

        # Get BERT embeddings for job description and resume
        job_desc_embedding = get_embeddings(job_description['feature'], model_name, device)
        resume_embedding = get_embeddings(resume_text_features['feature'], model_name, device)

        # Calculate cosine similarity
        similarity = cosine_similarity([job_desc_embedding], [resume_embedding])[0][0]

        return jsonify({"similarity": similarity})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()