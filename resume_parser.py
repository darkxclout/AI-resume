import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    skill_keywords = ['python', 'sql', 'excel', 'communication', 'machine learning',
                      'data analysis', 'flask', 'django', 'java', 'project management']
    text = text.lower()
    return list(set([skill for skill in skill_keywords if skill in text]))

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    doc = nlp(text)
    name = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    skills = extract_skills(text)
    return {
        "name": name[0] if name else "Unknown",
        "skills": skills,
        "text": text[:500]
    }
