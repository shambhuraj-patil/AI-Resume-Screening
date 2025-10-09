# app.py
import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import clean_text, extract_skills, calculate_match_score  # import functions

st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")
st.title("📄 AI Resume Screening App")

job_description = st.text_area("🧾 Paste Job Description here:", height=200)
uploaded_files = st.file_uploader("📂 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

if st.button("🔍 Analyze Resumes"):
    if not job_description.strip():
        st.warning("⚠️ Please paste a job description.")
    elif not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
    else:
        results = []
        job_clean = clean_text(job_description)
        with st.spinner("Analyzing resumes... ⏳"):
            for file in uploaded_files:
                resume_text = extract_text_from_pdf(file)
                resume_clean = clean_text(resume_text)

                skills_found = extract_skills(resume_clean)
                score = calculate_match_score(job_clean, resume_clean)

                results.append({
                    "Resume Name": file.name,
                    "Match Score (%)": score,
                    "Top Skills Found": ', '.join(skills_found) if skills_found else 'N/A'
                })

        df_results = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)
        st.success("✅ Analysis Complete!")
        st.dataframe(df_results, width='stretch')

        # Visualization
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=df_results, x="Match Score (%)", y="Resume Name", palette="Blues_r", ax=ax, legend=False)
        ax.set_title("Resume vs Job Description Match Score", fontsize=13, weight='bold')
        ax.set_xlabel("Match Score (%)", fontsize=11)
        ax.set_ylabel("Resume", fontsize=11)
        st.pyplot(fig)

        # CSV Download
        csv_data = df_results.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Download Results as CSV", data=csv_data,
                           file_name="resume_screening_results.csv", mime="text/csv")

        # Top candidate
        top_candidate = df_results.iloc[0]
        st.markdown(f"### 🏆 Top Match: **{top_candidate['Resume Name']}** — {top_candidate['Match Score (%)']}%")
        st.markdown(f"**Top Skills:** {top_candidate['Top Skills Found']}")
