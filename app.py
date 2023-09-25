from flask import Flask, request, jsonify
from extraction import process_resume_data, preprocess_text, extract_text_from_pdf
from embeddings import get_embeddings
from sklearn.metrics.pairwise import cosine_similarity
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route("/resume_matcher", methods=["POST"])
def resume_matcher():
    try:
        job_description = request.form.get("job_description")
        resume_files = request.files.getlist("resume_file")  # Get a list of uploaded resume files

        # Check if both job description and at least one resume file are provided
        if not job_description or not resume_files:
            return jsonify({"error": "Please provide both a job description and at least one resume file."})

        # Preprocess job description
        job_description = preprocess_text(job_description)

        # Initialize an empty list to store similarity scores for each resume
        similarities = []

        for resume_file in resume_files:
            # Read the uploaded resume PDF
            resume_text = extract_text_from_pdf(resume_file)

            # Preprocess resume text
            resume_text_features = preprocess_text(resume_text)

            # Get BERT embeddings for job description and resume
            job_desc_embedding = get_embeddings(job_description['feature'], model_name, device)
            resume_embedding = get_embeddings(resume_text_features['feature'], model_name, device)

            # Calculate cosine similarity
            similarity = cosine_similarity([job_desc_embedding], [resume_embedding])[0][0]

            # Append similarity score to the list
            similarities.append(similarity)

        # Log the similarities
        logging.info("Similarities: %s", similarities)

        return jsonify({"similarities": similarities})

    except Exception as e:
        # Log the error
        logging.error("Error: %s", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
