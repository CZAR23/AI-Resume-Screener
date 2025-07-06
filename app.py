import streamlit as st
import os
from resume_parser import extract_text_from_pdf
from model import clean_text, compute_similarity

st.title("📄 AI Resume Screener")

# Upload job description text file
job_desc_file = st.file_uploader("Upload Job Description (.txt)", type="txt")

# Upload multiple resumes
uploaded_resumes = st.file_uploader("Upload Resumes (PDFs)", type="pdf", accept_multiple_files=True)

if job_desc_file and uploaded_resumes:
    # Read job description
    job_description_text = job_desc_file.read().decode("utf-8")
    cleaned_job_desc = clean_text(job_description_text)

    resume_texts = []
    resume_names = []

    for resume in uploaded_resumes:
        resume_text = extract_text_from_pdf(resume)
        cleaned_resume = clean_text(resume_text)
        resume_texts.append(cleaned_resume)
        resume_names.append(resume.name)
        print(resume_text)
        print("-------------------------------------------------------------------------")
        print(cleaned_resume)
        print("-------------------------------------------------------------------------")

    # Compute similarity scores
    scores = compute_similarity(resume_texts, cleaned_job_desc)

    # Combine names with scores
    results = sorted(
        zip(resume_names, scores),
        key=lambda x: x[1],
        reverse=True
    )

    st.subheader("📊 Ranked Candidates:")
    for name, score in results:
        st.write(f"**{name}** — Similarity Score: {score:.2f}")
