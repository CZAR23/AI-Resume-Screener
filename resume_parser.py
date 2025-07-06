import fitz  # PyMuPDF

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     doc = fitz.open(pdf_path)
#     for page in doc:
#         text += page.get_text()
#         #print(text)
#     return text

# extract_text_from_pdf("sample_data\shawn gigo george.pdf")

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    text = ""
    # pdf_file can be a file-like object (from Streamlit) or a file path
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

