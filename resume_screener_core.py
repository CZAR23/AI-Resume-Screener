import fitz  # PyMuPDF
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1️⃣ Load small English NLP model from spaCy
print("[INFO] Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")



# 2️⃣ Extract text from a PDF given a file path
def extract_text_from_pdf(file_path):
    print(f"[INFO] Extracting text from {file_path}...")
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text


# 3️⃣ Clean text with spaCy: tokenize, lemmatize, remove stopwords and punctuation
def clean_text(text):
    print("[INFO] Cleaning text...")
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and token.is_alpha
    ]
    cleaned = " ".join(tokens)
    print(f"[DEBUG] Cleaned text sample: {cleaned[:300]}...")
    return cleaned


# 4️⃣ Compute similarity between resumes and job description
def compute_similarity(resume_texts, job_description_text):
    print("[INFO] Computing similarities...")
    corpus = resume_texts + [job_description_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    

    # Last vector is job description
    job_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(resume_vectors, job_vector)

    return similarities.flatten()


if __name__ == "__main__":
    # 5️⃣ Manually specify file paths for your resumes and job description
    resume_paths = [
        r"D:\github\AI Resume Screener\sample_data\shawn gigo george.pdf",
        #r"D:\github\AI Resume Screener\sample_data\resume2.pdf"
    ]
    job_description_path = r"D:\github\AI Resume Screener\sample_data\job_description.txt"

    # 6️⃣ Read and clean job description
    print(f"[INFO] Reading job description from {job_description_path}...")
    with open(job_description_path, "r", encoding="utf-8") as f:
        job_description_raw = f.read()
    cleaned_job_desc = clean_text(job_description_raw)

    # 7️⃣ Read, extract, and clean each resume
    cleaned_resumes = []
    resume_names = []
    for path in resume_paths:
        raw_resume_text = extract_text_from_pdf(path)
        cleaned_resume = clean_text(raw_resume_text)
        cleaned_resumes.append(cleaned_resume)
        resume_names.append(path.split("\\")[-1])  # Just filename

    # 8️⃣ Compute similarities
    similarity_scores = compute_similarity(cleaned_resumes, cleaned_job_desc)
 

    # 9️⃣ Combine names with scores and print ranked results
    results = sorted(
        zip(resume_names, similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n========== 📊 RANKED RESULTS ==========")
    for name, score in results:
        print(f"Resume: {name} — Similarity Score: {score:.2f}")
