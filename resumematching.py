# -*- coding: utf-8 -*-
"""ResumeMatching

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iBZUWLrf-zyw1V7jn6aHo2zqto2dvjmG
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import string
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from extraction import process_resume_data, preprocess_text
from embeddings import get_embeddings
from printing import print_top_matching_resumes
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

for dirname, _, filenames in os.walk('/content/drive/MyDrive/archive'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


resume_data = pd.read_csv("/content/drive/MyDrive/archive/Resume/Resume.csv")
resume_data = resume_data.drop(["Resume_html"], axis=1)
resume_data = resume_data.apply(process_resume_data, axis=1)
resume_data = resume_data.drop(columns=['Resume_str'])
resume_data.to_csv("/content/drive/MyDrive/archive/resume_data.csv", index=False)

job_description = pd.read_csv("/content/drive/MyDrive/training_data.csv/training.csv")
job_description = job_description[["job_description", "position_title"]][:15]
job_description['Features'] = job_description['job_description'].apply(lambda x : preprocess_text(x)['feature'])

job_desc_embeddings = np.array([get_embeddings(desc, model_name,device) for desc in job_description['Features']]).squeeze()
resume_embeddings = np.array([get_embeddings(text, model_name,device) for text in resume_data['Feature']]).squeeze()

result_df = pd.DataFrame(columns=['jobId', 'resumeId', 'similarity', 'domainResume', 'domainDesc'])

for i, job_desc_emb in enumerate(job_desc_embeddings):
    similarities = cosine_similarity([job_desc_emb], resume_embeddings)
    top_k_indices = np.argsort(similarities[0])[::-1][:5]
    for j in top_k_indices:
        result_df.loc[i+j] = [i, resume_data['ID'].iloc[j], similarities[0][j], resume_data['Category'].iloc[j], job_description['position_title'].iloc[i]]

result_df = result_df.sort_values(by='similarity', ascending=False)
result_group = result_df.groupby("jobId")
print_top_matching_resumes(result_group)