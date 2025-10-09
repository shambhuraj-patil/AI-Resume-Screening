# utils.py
import re
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

base_skills = [
    'python', 'java', 'c++', 'machine learning', 'deep learning', 'nlp',
    'data analysis', 'data visualization', 'sql', 'excel', 'pandas', 'numpy',
    'matplotlib', 'power bi', 'tableau', 'django', 'flask', 'html', 'css', 'javascript',
    'tensorflow', 'keras', 'sklearn', 'git', 'linux', 'api', 'docker'
]

def clean_text(text):
    text = re.sub(r'(hobbies|references|objective).*', '', text, flags=re.I)
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text):
    found_skills = set()
    for skill in base_skills:
        if ' ' in skill:  # multi-word skill
            if fuzz.partial_ratio(skill, text) >= 90:
                found_skills.add(skill)
        else:  # single-word skill
            if skill in text.split():
                found_skills.add(skill)
    return list(found_skills)

def calculate_match_score(job_desc, resume_text):
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'), ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform([job_desc, resume_text])
    tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    jd_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume_text)
    skill_overlap = len(set(jd_skills) & set(resume_skills)) / max(len(jd_skills),1)

    overall_score = 0.7 * tfidf_similarity + 0.3 * skill_overlap
    return round(overall_score * 100, 2)
