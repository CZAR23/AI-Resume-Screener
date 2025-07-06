import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load small English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)

def compute_similarity(resume_texts, job_description_text):
    # Combine texts
    corpus = resume_texts + [job_description_text]

    # Convert to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # The last entry is job description
    job_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]

    # Compute similarity scores
    similarities = cosine_similarity(resume_vectors, job_vector)
    return similarities.flatten()
