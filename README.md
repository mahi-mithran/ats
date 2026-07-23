# 📄 ATS Resume Analyzer

A fully local, LLM-free ATS (Applicant Tracking System) resume
analyzer built with Python, spaCy, scikit-learn, and Streamlit.

---

## Features

- PDF and DOCX resume parsing
- 180+ technical skill detection
- Soft skill detection
- Keyword match vs job description (TF-IDF + cosine similarity)
- Section completeness checker
- Format and quality analyzer
- Prioritized improvement suggestions
- Interactive Streamlit dashboard

---

## Tech Stack

| Layer       | Library                        |
|-------------|--------------------------------|
| Parsing     | pdfplumber, PyMuPDF, python-docx |
| NLP / NER   | spaCy (en_core_web_sm)         |
| ML / Scoring| scikit-learn, TF-IDF           |
| Fuzzy Match | rapidfuzz                      |
| UI          | Streamlit                      |
| Charts      | Plotly                         |

---

## Project Structure