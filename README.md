# 📄 AI Resume Screening App  

An intelligent **Streamlit-based web app** that analyzes multiple resumes against a given **Job Description (JD)** to calculate match scores and extract relevant technical skills.  
This helps recruiters and candidates quickly identify the most suitable profiles for a job role.  

---

## 🚀 Features  

✅ Upload multiple resume PDFs at once  
✅ Paste a job description to compare each resume  
✅ Get a **Match Score (%)** based on TF-IDF cosine similarity  
✅ Extract relevant **technical skills** using NLP + fuzzy matching  
✅ View a **bar chart comparison** of all resumes  
✅ Visualize a **skills word cloud** per resume  
✅ Download results as CSV  

---

## 🧠 Tech Stack  

- **Python**  
- **Streamlit**  
- **scikit-learn (TF-IDF, cosine similarity)**  
- **NLTK** (stopwords, text cleaning)  
- **FuzzyWuzzy** (fuzzy skill matching)  
- **Matplotlib** & **Seaborn** (visualization)  
- **WordCloud** (skills visualization)  
- **PyPDF2** (PDF text extraction)  

---

## ⚙️ Installation & Usage  

1. **Clone this repository**
```bash
git clone https://github.com/shambhuraj-patil/AI-Resume-Screening.git
cd AI-Resume-Screening
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
streamlit run app.py
```

## 👨‍💻 Author  

**Shambhuraj Patil**  
📍 Pune, Maharashtra, India  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/shambhurajpatil)  
[![GitHub](https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=github)](https://github.com/shambhuraj-patil)


⭐ If you like this project, consider giving it a star on GitHub!

