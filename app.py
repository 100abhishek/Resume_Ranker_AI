
import gradio as gr
import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pdfplumber
from docx import Document

model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract text from PDF or DOCX
def extract_text(file_path, ext):
    try:
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                return ' '.join(page.extract_text() or '' for page in pdf.pages)
        elif ext == 'docx':
            return '\n'.join(p.text for p in Document(file_path).paragraphs)
    except:
        return ''
    return ''

# Identify JD
def is_probable_jd(text, filename):
    jd_keywords = [
        "responsibilities", "requirements", "qualifications", "job description", "skills",
        "preferred", "desired", "job summary", "position", "job title"
    ]
    resume_keywords = [
        "education", "projects", "certifications", "linkedin", "experience", "internship", "objective"
    ]
    text_lower = text.lower()
    jd_score = sum(text_lower.count(k) for k in jd_keywords)
    resume_score = sum(text_lower.count(k) for k in resume_keywords)
    filename_hint = "jd" in filename.lower() or "description" in filename.lower()
    return jd_score + (20 if filename_hint else 0) > resume_score

# Keyword extractor
def extract_top_keywords(text1, text2, top_n=5):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        feature_names = vectorizer.get_feature_names_out()
        diff = tfidf[0] - tfidf[1]
        abs_diff = abs(diff.toarray()[0])
        top_indices = abs_diff.argsort()[-top_n:][::-1]
        return [feature_names[i] for i in top_indices]
    except:
        return []

def score_resumes(files):
    try:
        if not files or len(files) < 2:
            raise gr.Error("Please upload at least 1 JD and 1 resume.")

        text_data, jd_files, resume_files = {}, {}, {}

        # Read and extract text directly from file paths
        for file_path in files:
            ext = file_path.split('.')[-1].lower()
            text = extract_text(file_path, ext)
            text_data[os.path.basename(file_path)] = text

        # Classify into JD and Resumes
        for filename, text in text_data.items():
            if is_probable_jd(text, filename):
                jd_files[filename] = text
            else:
                resume_files[filename] = text

        if not jd_files:
            raise gr.Error("No Job Description detected.")
        if not resume_files:
            raise gr.Error("No resumes detected.")

        results = []
        for resume_name, resume_text in resume_files.items():
            resume_embedding = model.encode([resume_text])
            for jd_name, jd_text in jd_files.items():
                jd_embedding = model.encode([jd_text])
                sim = cosine_similarity(resume_embedding, jd_embedding)[0][0]
                top_keywords = extract_top_keywords(jd_text, resume_text)
                results.append((
                    os.path.basename(resume_name),
                    os.path.basename(jd_name),
                    round(sim * 100, 2),
                    ', '.join(top_keywords)
                ))

        df = pd.DataFrame(results, columns=["Resume", "Job Description", "Match %", "Top Keywords"])
        df = df.sort_values(by="Match %", ascending=False).reset_index(drop=True)

        # Plot
        plt.figure(figsize=(10, 4))
        bars = plt.barh(df["Resume"], df["Match %"], color="skyblue")
        plt.xlabel("Match %")
        plt.title("Resume Match Score")
        plt.gca().invert_yaxis()
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width:.2f}%', va='center')
        plot_path = os.path.join(tempfile.gettempdir(), "match_plot.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        # Save CSV
        csv_path = os.path.join(tempfile.gettempdir(), "resume_ranking_results.csv")
        df.to_csv(csv_path, index=False)

        return df, plot_path, csv_path

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise gr.Error(f"⚠️ Something went wrong:\n\n{e}")

# Gradio Interface
gr.Interface(
    fn=score_resumes,
    inputs=gr.File(file_types=[".pdf", ".docx"], file_count="multiple", label="Upload Resumes and Job Descriptions"),
    outputs=[
        gr.Dataframe(label="Resume Match Results"),
        gr.Image(type="filepath", label="Score Chart"),
        gr.File(label="📥 Download CSV")
    ],
    title="Resume Ranker AI",
    description="Upload resumes and job descriptions (.pdf or .docx) in any order. The app will automatically detect the JD and rank resumes by similarity."
).launch()
