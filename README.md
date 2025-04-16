# 🧠 ResumeRanker AI

ResumeRanker AI is an intelligent application that matches resumes with job descriptions using advanced semantic similarity techniques powered by Sentence Transformers. It's built to help recruiters, hiring managers, and job seekers streamline the resume screening process.

---

## 🚀 Demo

https://huggingface.co/spaces/abhisheksingh100/Resume_Rankers_AI

---

## ✨ Features

- ✅ Upload multiple resumes (PDF or DOCX)
- ✅ Upload a job description
- ✅ Auto-detects the job description file
- ✅ Calculates similarity score between job description and each resume
- ✅ Returns a sorted ranking of resumes based on match quality

---

## 📁 File Structure

```
ResumeRanker_AI/
│
├── Resume_Ranker_AI.py        # Main Python script with all logic
├── app.py                     # (Optional) Gradio interface script if deployed
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## 🛠️ Technologies Used

- Python
- Sentence Transformers (all-MiniLM-L6-v2)
- Scikit-learn
- Pandas
- Gradio (if used for interface)
- PDFPlumber & python-docx for file reading

---

## 📦 Installation

To run locally:

```bash
git clone https://github.com/your-username/ResumeRanker_AI.git
cd ResumeRanker_AI
pip install -r requirements.txt
python Resume_Ranker_AI.py
```

To run with a Gradio interface:

```bash
python app.py
```

---

## 📋 Usage

1. Place your resumes (PDF or DOCX) and job description file in the same folder.
2. Run the script.
3. It automatically detects the job description.
4. Outputs ranked list of resumes with similarity scores.

---

## 📸 Example Output

```
Top Matches:
1. John_Doe.pdf - Similarity: 0.87
2. Priya_Kumar.docx - Similarity: 0.82
3. Rahul_Sharma.pdf - Similarity: 0.79
```

---

## 🙌 Acknowledgements

- Hugging Face for Sentence Transformers
- scikit-learn for cosine similarity
- Gradio for simple UI

---

## 📫 Contact

Made by **Abhishek Singh**

Let’s connect on [LinkedIn](https://www.linkedin.com)
