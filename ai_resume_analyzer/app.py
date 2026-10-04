"""Beginner-friendly Streamlit dashboard for resume and job-role matching."""

from pathlib import Path

import pandas as pd
import streamlit as st

from job_matcher import rank_roles
from resume_parser import extract_text
from roadmap_generator import make_roadmap
from skill_extractor import find_skills, load_skill_dictionary
from text_cleaner import clean_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MAX_FILE_SIZE = 10 * 1024 * 1024

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("AI Resume Analyzer and Job Recommendations")
st.write(
    "Upload a resume to see which listed technical skills it contains, compare it with job roles, "
    "and get a starter learning plan. This is an educational estimate, not a hiring decision."
)

uploaded_file = st.file_uploader("Choose a PDF or DOCX resume", type=["pdf", "docx"])

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    if len(file_bytes) > MAX_FILE_SIZE:
        st.error("The file is larger than 10 MB. Please choose a smaller resume.")
        st.stop()

    try:
        resume_text = extract_text(file_bytes, uploaded_file.name)
    except Exception as error:
        st.error(f"I could not read this file: {error}")
        st.stop()

    if not resume_text.strip():
        st.warning("No selectable text was found. This may be a scanned image PDF; try a text-based PDF or DOCX.")
        st.stop()

    dictionary = load_skill_dictionary(DATA_DIR / "skill_dictionary.csv")
    roles = pd.read_csv(DATA_DIR / "job_roles.csv").fillna("").to_dict(orient="records")
    skills = find_skills(clean_text(resume_text), dictionary)
    rankings = rank_roles(skills, roles)

    st.caption(f"Processed {uploaded_file.name}. The resume is held in memory for this session and is not saved by this app.")

    left, right = st.columns(2)
    with left:
        st.subheader("Skills found")
        if skills:
            st.write(", ".join(skills))
        else:
            st.info("No skills from the current dictionary were found. Try adding terms to data/skill_dictionary.csv.")

    with right:
        st.subheader("Top role recommendations")
        st.bar_chart(pd.DataFrame(rankings[:3]).set_index("role")["score"], y_label="Required skills found (%)")
        for item in rankings[:3]:
            st.write(f"**{item['role']} — {item['score']}%**")

    role_names = [item["role"] for item in rankings]
    selected_role = st.selectbox("Choose a role to inspect", role_names)
    selected = next(item for item in rankings if item["role"] == selected_role)

    st.subheader(f"Skill gaps for {selected_role}")
    st.metric("Required skills found", f"{selected['score']}%")
    col_found, col_missing = st.columns(2)
    with col_found:
        st.markdown("**Found**")
        st.write(", ".join(selected["matched"]) if selected["matched"] else "None from this role's list yet")
    with col_missing:
        st.markdown("**Not found in the resume**")
        st.write(", ".join(selected["missing"]) if selected["missing"] else "No listed skill gaps")

    st.subheader("Starter learning roadmap")
    for week in make_roadmap(selected["missing"]):
        st.write(f"- {week}")

    report = pd.DataFrame(
        [{"role": item["role"], "estimated_match_percent": item["score"], "skills_found": ", ".join(item["matched"]), "skills_not_found": ", ".join(item["missing"])} for item in rankings]
    )
    st.download_button(
        "Download role comparison (CSV)",
        data=report.to_csv(index=False).encode("utf-8"),
        file_name="resume_role_analysis.csv",
        mime="text/csv",
    )

    st.caption(
        "Scores count the share of a role's listed skills detected in the resume. "
        "A missing keyword does not prove a person lacks that ability. Add skills to the resume only when accurate."
    )
else:
    st.info("Start by uploading a text-based PDF or DOCX resume. Your file is not permanently stored by this app.")
