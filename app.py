from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from pydantic import BaseModel
from extraction import process_resume_data, preprocess_text, extract_text_from_pdf
from embeddings import get_embeddings
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(filename='app.log', level=logging.INFO)

content = ''' '''
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to the list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def resume_matcher(job_description, resume_text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.to(device)

    try:
        job_description = job_description
        resume_text = resume_text


        # Preprocess job description
        job_description = preprocess_text(job_description)
        
        # Preprocess resume text
        resume_text_features = preprocess_text(resume_text)

        # Get BERT embeddings for job description and resume
        job_desc_embedding = get_embeddings(job_description, model_name, device)
        resume_embedding = get_embeddings(resume_text_features, model_name, device)

        # Calculate cosine similarity
        similarity = cosine_similarity(job_desc_embedding, resume_embedding)

        # Log the similarities
        logging.info("Similarities: %s", similarity)

        similarity_list = similarity.tolist()

        return {"similarity": similarity_list[0]}
    except Exception as e:
        # Log the error
        logging.error("Error: %s", str(e))
        error_message = {"error": str(e)}
        return JSONResponse(content=error_message, status_code=400)
    

    
@app.post("/upload_file")
def upload_file(job_description: str,
    resume_file: UploadFile):

        # Extract job_description from the form data
        # (job_description is expected as a regular form field)
    if not job_description:
        return {"error": "Please provide a job description."}

        # Check if a file was uploaded
    if not resume_file:
        return {"error": "Please upload a resume PDF file."}
    # Extract data from the request
    job_description = job_description
    resume_text = extract_text_from_pdf(resume_file)

    # Perform similarity calculation (you can replace this with your calculation logic)
    similarity_score = resume_matcher(job_description, resume_text)

    # Return the similarity score in the response
    return {"similarity_score": similarity_score}
