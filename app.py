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

 

# Configure CORS

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # Update this to the list of allowed origins

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

 

class SimilarityRequest(BaseModel):

    job_description: str = Form(...)

    resume_file: UploadFile = File(...)

 

@app.post("/resume_matcher")

async def resume_matcher(job_description: str, resume_file: UploadFile = File(...)):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_name = "bert-base-uncased"

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModel.from_pretrained(model_name)

    model.to(device)

    try:

        job_description = job_description

        resume_file = resume_file

 

        # Check if both job description and resume file are provided

        if not job_description or not resume_file:

            return {"error": "Please provide both a job description and a resume file."}

 

        # Preprocess job description

        job_description = preprocess_text(job_description)

 

        # Read the uploaded resume PDF

        resume_text = extract_text_from_pdf(resume_file.file)

 

        # Preprocess resume text

        resume_text_features = preprocess_text(resume_text)

 

        # Get BERT embeddings for job description and resume

        job_desc_embedding = get_embeddings(job_description['feature'], model_name, device)

        resume_embedding = get_embeddings(resume_text_features['feature'], model_name, device)

 

        # job_desc_embedding = job_desc_embedding.reshape(-1)  # Reshape to 1D array

        # resume_embedding = resume_embedding.reshape(-1)      # Reshape to 1D array

 

 

        # Calculate cosine similarity

        similarity = cosine_similarity(job_desc_embedding, resume_embedding)

        # print(similarity)

 

        # return {"similarity": similarity}

        # return {"embeddings": job_desc_embedding.shape}

        # , "resume_embedding": resume_embedding.shape}

        # Log the similarities

        logging.info("Similarities: %s", similarity)

 

        similarity_list = similarity.tolist()

 

        return {"similarity": similarity_list[0]}

        # response_data = {"similarity": similarity_list}

        # return JSONResponse(content=response_data)

    except Exception as e:

        # Log the error

        logging.error("Error: %s", str(e))

        error_message = {"error": str(e)}

        return JSONResponse(content=error_message, status_code=400)