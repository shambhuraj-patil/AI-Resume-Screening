import time
import PyPDF2
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from utils import clean_text, extract_skills, calculate_match_score

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")

# Initialize session state to hold results
if 'results_df' not in st.session_state:
    st.session_state['results_df'] = None

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", ["📝 Input & Analyze", "📊 Results"])

if page == "📝 Input & Analyze":
    st.title("🧠 AI Resume Analyzer")
    st.caption("Analyze and compare resumes against job descriptions.")
    st.divider()

    job_description = st.text_area(
        "📄 Paste Job Description",
        placeholder="Paste the full job description here...",
        height=200
    )
    uploaded_files = st.file_uploader(
        "📂 Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can upload multiple resumes (PDFs)"
    )

    if st.button("🔍 Analyze Resumes"):
        if not job_description.strip():
            st.warning("⚠️ Please paste a job description before analyzing.")
        elif not uploaded_files:
            st.warning("⚠️ Please upload at least one resume before analyzing.")
        else:
            st.info("🕐 Starting analysis... Please wait a few seconds.")
            progress = st.progress(0)
            results = []
            cleaned_jd = clean_text(job_description)
            jd_skills = extract_skills(cleaned_jd)

            for i, file in enumerate(uploaded_files):
                resume_text = extract_text_from_pdf(file)
                cleaned_resume = clean_text(resume_text)
                resume_skills = extract_skills(cleaned_resume)
                match_score = calculate_match_score(cleaned_resume, cleaned_jd)
                results.append({
                    "Resume": file.name,
                    "Match Score": round(match_score, 2),
                    "Top Skills Found": ", ".join(resume_skills[:10])
                })
                progress.progress(int(((i + 1) / len(uploaded_files)) * 100))
                time.sleep(0.3)

            df_results = pd.DataFrame(results).sort_values(by="Match Score", ascending=False)
            st.session_state['results_df'] = df_results
            st.success("✅ Analysis complete!")
            st.info("Switch to the 'Results' page in the sidebar to view detailed insights.")

    st.divider()
    st.caption("👨💻 Built by **Shambhuraj Patil**")

elif page == "📊 Results":
    st.title("📊 Analysis Results")

    if st.session_state['results_df'] is None:
        st.warning("⚠️ Please perform analysis on the 'Input & Analyze' page first.")
    else:
        df_results = st.session_state['results_df']

        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧩 Skill Insights", "📈 Resume Fit Graph"])

        with tab1:
            best_resume = df_results.iloc[0]
            st.metric(label="📄 Total Resumes Analyzed", value=len(df_results))
            st.metric(label="🏆 Best Match", value=best_resume["Resume"])
            st.metric(label="⭐ Top Score", value=f"{best_resume['Match Score']}%")
            st.divider()
            csv_data = df_results.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name="resume_screening_results.csv",
                mime="text/csv"
            )
            
        with tab2:
            st.dataframe(df_results.reset_index(drop=True), use_container_width=True, hide_index=True)

        with tab3:
            st.subheader("📊 Resume Fit Comparison")
            fig, ax = plt.subplots(figsize=(8,4))
            sns.barplot(data=df_results, x="Match Score", y="Resume", palette="Blues_r", ax=ax, legend=False)
            ax.set_title("Resume vs Job Description Match Score", fontsize=13, weight='bold')
            ax.set_xlabel("Match Score", fontsize=11)
            ax.set_ylabel("Resume", fontsize=11)
            st.pyplot(fig)
