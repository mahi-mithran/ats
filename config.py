# config.py

import os
from pathlib import Path

# ─────────────────────────────────────────
#  BASE PATHS
# ─────────────────────────────────────────

BASE_DIR       = Path(__file__).resolve().parent
DATA_DIR       = BASE_DIR / "data"
RAW_DIR        = DATA_DIR / "raw"
PROCESSED_DIR  = DATA_DIR / "processed"
MODELS_DIR     = DATA_DIR / "models"

# ─────────────────────────────────────────
#  FILE SETTINGS
# ─────────────────────────────────────────

ALLOWED_EXTENSIONS  = [".pdf", ".docx", ".doc", ".txt"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024   # 5 MB

# ─────────────────────────────────────────
#  SPACY MODEL
# ─────────────────────────────────────────

SPACY_MODEL = "en_core_web_sm"

# ─────────────────────────────────────────
#  SCORING CONFIG
# ─────────────────────────────────────────

SCORING = {
    "keyword_weight":  0.35,
    "skill_weight":    0.30,
    "section_weight":  0.20,
    "format_weight":   0.15,

    # Fuzzy match threshold (0–100)
    "fuzzy_threshold": 85,

    # TF-IDF top keywords to extract from JD
    "tfidf_top_n": 30,

    # Ideal resume word count range
    "ideal_words_min": 300,
    "ideal_words_max": 700,
}

# ─────────────────────────────────────────
#  STREAMLIT UI CONFIG
# ─────────────────────────────────────────

UI = {
    "app_title":   "ATS Resume Analyzer",
    "app_icon":    "📄",
    "primary_color": "#2d6a9f",
    "max_suggestions": 10,
}

# ─────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────

LOG_LEVEL = "INFO"
LOG_FILE  = BASE_DIR / "ats_analyzer.log"

# ─────────────────────────────────────────
#  AUTO-CREATE DIRS ON IMPORT
# ─────────────────────────────────────────

for _dir in [RAW_DIR, PROCESSED_DIR, MODELS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)