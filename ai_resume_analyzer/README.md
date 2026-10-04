# AI Resume Analyzer and Job Recommendation System

A beginner-level Python and Streamlit project. Upload a text-based PDF or DOCX resume to find listed skills, compare them with six example job roles, see a simple skill-match estimate, and get a weekly learning plan.

## How the project works

1. `resume_parser.py` reads the uploaded file from memory with `pypdf` or `python-docx`.
2. `text_cleaner.py` lowercases the resume text and cleans extra symbols and spaces.
3. `skill_extractor.py` searches the cleaned text for skill names and aliases in `data/skill_dictionary.csv`.
4. `job_matcher.py` compares found skills with each role in `data/job_roles.csv`.
5. `roadmap_generator.py` turns the selected role's missing listed skills into weekly study topics.
6. `app.py` displays the result and lets you download the role comparison as a CSV.

The score is **required-skill coverage**: `(number of role skills found / number of role skills listed) × 100`. It is a clear beginner baseline, not an AI hiring decision or a measure of someone's full ability. Keyword matching can miss synonyms and skills that are described differently.

## Run on Windows

Open PowerShell in the repository root (the folder containing `data` and `ai_resume_analyzer`).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r ai_resume_analyzer\requirements.txt
streamlit run ai_resume_analyzer\app.py
```

Then open the local address Streamlit prints, usually `http://localhost:8501`.

If PowerShell blocks virtual-environment activation, run the commands with `..\.venv\Scripts\python.exe` from the app folder, or use `\.venv\Scripts\python.exe` from the repository root to install and launch Streamlit.

## Make the project your own

- Add or edit job roles in `data/job_roles.csv`. Separate each required skill with `|`.
- Add skills and aliases in `data/skill_dictionary.csv`. Separate aliases with `|`.
- Start with a text-based PDF or DOCX. Scanned image PDFs need OCR, which is not included in this beginner version.
- Use anonymized sample resumes when demonstrating the project.

Uploaded bytes are processed in memory and are not written to a permanent file by this app. Do not use match scores to accept or reject applicants. The app only compares job-related skill terms and does not score protected personal information.

## Beginner extension ideas

After understanding the current flow, add section detection, a TF-IDF/cosine similarity comparison, OCR for scanned PDFs, then optional hosting. Each can be added as a separate improvement and compared with the simple baseline.
