# streamlit_app.py

import os
import warnings
import logging

import streamlit as st
import pandas as pd
import plotly.express as px

from src.parser.resume_parser import parse_resume
from src.model.predict import predict_ats_score

# ==========================================
# REMOVE TRANSFORMERS WARNINGS
# ==========================================

warnings.filterwarnings("ignore")

logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #4CAF50;
}

.score-box {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
}

.good {
    background-color: #2e7d32;
}

.avg {
    background-color: #f9a825;
}

.bad {
    background-color: #c62828;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
}

.small-text {
    color: gray;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<p class="main-title">📄 ATS Resume Analyzer</p>',
    unsafe_allow_html=True
)

st.caption(
    "No LLM · Semantic AI · Local ML · Resume Intelligence"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Settings")

ml_weight = st.sidebar.slider(
    "ML Weight",
    0.0,
    1.0,
    0.30,
    0.05
)

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "📋 Job Description (Optional)",
    height=220,
    placeholder="Paste full job description here..."
)

# ==========================================
# ANALYZE
# ==========================================

if uploaded_file is not None:

    try:

        # ==================================
        # PARSE RESUME
        # ==================================

        with st.spinner("Parsing resume..."):

            resume_data = parse_resume(
                uploaded_file
            )

        # ==================================
        # ATS PREDICTION
        # ==================================

        with st.spinner("Running ATS analysis..."):

            result = predict_ats_score(
                resume_data,
                job_description,
                ml_weight
            )

        # ==================================
        # SCORE
        # ==================================

        score = result["final_score"]

        if score >= 80:
            box_class = "good"

        elif score >= 60:
            box_class = "avg"

        else:
            box_class = "bad"

        st.markdown(
            f"""
            <div class="score-box {box_class}">
                ATS SCORE<br>
                {score}/100
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==================================
        # BAND
        # ==================================

        st.success(
            f"{result['band']['emoji']} "
            f"{result['band']['label']} - "
            f"{result['band']['message']}"
        )

        # ==================================
        # SCORE BREAKDOWN
        # ==================================

        st.markdown(
            '<p class="section-title">📊 Score Breakdown</p>',
            unsafe_allow_html=True
        )

        score_data = {
            "Category": [],
            "Score": []
        }

        if result["has_jd"]:

            score_data["Category"].append("Keyword")
            score_data["Score"].append(
                result["scores"]["keyword"]
            )

        score_data["Category"].append("Skill")
        score_data["Score"].append(
            result["scores"]["skill"]
        )

        score_data["Category"].append("Section")
        score_data["Score"].append(
            result["scores"]["section"]
        )

        score_data["Category"].append("Format")
        score_data["Score"].append(
            result["scores"]["format"]
        )

        df = pd.DataFrame(score_data)

        fig = px.bar(
            df,
            x="Category",
            y="Score",
            text="Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==================================
        # SEMANTIC MATCH
        # ==================================

        if result["has_jd"]:

            st.markdown(
                '<p class="section-title">🧠 Semantic Match</p>',
                unsafe_allow_html=True
            )

            semantic_score = result.get(
                "semantic_score",
                0
            )

            similarity = result.get(
                "semantic_similarity",
                0
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Semantic Score",
                    f"{semantic_score}%"
                )

            with col2:

                st.metric(
                    "Similarity",
                    similarity
                )

        # ==================================
        # SKILLS
        # ==================================

        st.markdown(
            '<p class="section-title">🛠 Skills</p>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        skill_details = result.get(
            "skill_details",
            {}
        )

        with col1:

            st.subheader("Technical Skills")

            tech_skills = skill_details.get(
                "technical_skills",
                []
            )

            if tech_skills:

                for skill in tech_skills:
                    st.success(skill)

            else:
                st.warning("No technical skills found.")

        with col2:

            st.subheader("Soft Skills")

            soft_skills = skill_details.get(
                "soft_skills",
                []
            )

            if soft_skills:

                for skill in soft_skills:
                    st.info(skill)

            else:
                st.warning("No soft skills found.")

        # ==================================
        # MISSING SKILLS
        # ==================================

        missing_skills = skill_details.get(
            "missing_skills",
            []
        )

        if missing_skills:

            st.markdown(
                '<p class="section-title">❌ Missing Skills</p>',
                unsafe_allow_html=True
            )

            for skill in missing_skills:
                st.error(skill)

        # ==================================
        # KEYWORDS
        # ==================================

        if result["has_jd"]:

            st.markdown(
                '<p class="section-title">🔑 Keywords</p>',
                unsafe_allow_html=True
            )

            keyword_details = result.get(
                "keyword_details",
                {}
            )

            matched = keyword_details.get(
                "phrases",
                {}
            ).get(
                "matched",
                []
            )

            missing = keyword_details.get(
                "phrases",
                {}
            ).get(
                "missing",
                []
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Matched Keywords")

                if matched:

                    for word in matched:
                        st.success(word)

                else:
                    st.warning("No matched keywords.")

            with col2:

                st.subheader("Missing Keywords")

                if missing:

                    for word in missing:
                        st.error(word)

                else:
                    st.success("No missing keywords.")

        # ==================================
        # RESUME INSIGHTS
        # ==================================

        st.markdown(
            '<p class="section-title">📄 Resume Insights</p>',
            unsafe_allow_html=True
        )

        format_details = result.get(
            "format_details",
            {}
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Words",
            format_details.get(
                "word_count",
                0
            )
        )

        c2.metric(
            "Action Verbs",
            format_details.get(
                "action_verb_count",
                0
            )
        )

        c3.metric(
            "Quantified Results",
            format_details.get(
                "quantified_count",
                0
            )
        )

        c4.metric(
            "Bullet Points",
            format_details.get(
                "bullet_line_count",
                0
            )
        )

       # ==================================
        # CONTACT DETAILS
        # ==================================

        st.markdown(
            '<p class="section-title">📞 Contact Details</p>',
            unsafe_allow_html=True
        )

        email = result.get("email")
        phone = result.get("phone")
        linkedin = result.get("linkedin")
        github = result.get("github")

        # Add protocol if missing
        if linkedin and not linkedin.startswith(("http://", "https://")):
            linkedin = f"https://{linkedin}"

        if github and not github.startswith(("http://", "https://")):
            github = f"https://{github}"

        contact_html = f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:15px;
            background-color:#fafafa;
        ">

        <table style="width:100%; border-collapse:collapse;">

        <tr>
            <th style="padding:10px; text-align:left;">Field</th>
            <th style="padding:10px; text-align:left;">Value</th>
        </tr>

        <tr>
            <td style="padding:10px;">📧 Email</td>
            <td style="padding:10px;">
                {
                    f'<a href="mailto:{email}">{email}</a>'
                    if email else "Not Found"
                }
            </td>
        </tr>

        <tr>
            <td style="padding:10px;">📱 Phone</td>
            <td style="padding:10px;">
                {phone if phone else "Not Found"}
            </td>
        </tr>

        <tr>
            <td style="padding:10px;">💼 LinkedIn</td>
            <td style="padding:10px;">
                {
                    f'<a href="{linkedin}" target="_blank">{linkedin}</a>'
                    if linkedin else "Not Found"
                }
            </td>
        </tr>

        <tr>
            <td style="padding:10px;">💻 GitHub</td>
            <td style="padding:10px;">
                {
                    f'<a href="{github}" target="_blank">{github}</a>'
                    if github else "Not Found"
                }
            </td>
        </tr>

        </table>

        </div>
        """

        st.markdown(
            contact_html,
            unsafe_allow_html=True
        )
        # ==================================
        # EDUCATION
        # ==================================

        st.markdown(
            '<p class="section-title">🎓 Education Analysis</p>',
            unsafe_allow_html=True
        )

        education = result.get(
            "education",
            {}
        )

        degrees = education.get(
            "degrees_found",
            []
        )

        institutions = education.get(
            "institutions",
            []
        )

        education_years = education.get(
            "education_years",
            []
        )

        gpa = education.get(
            "gpa",
            None
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Education Details")

            if degrees:

                st.write("### Degrees")

                for degree in degrees:
                    st.success(degree)

            else:
                st.warning("No degree detected")

            if institutions:

                st.write("### Institutions")

                for ins in institutions:
                    st.info(ins)

            else:
                st.warning("No institution detected")

        with col2:

            st.subheader("Academic Information")

            if education_years:

                st.write("### Education Years")

                for year in education_years:
                    st.success(year)

            else:
                st.warning("No education year detected")

            academic_score = education.get("academic_score")
            academic_type = education.get("academic_type")

            if academic_score:

                st.success(
                    f"{academic_type}: {academic_score}"
                )

            else:

                st.warning(
                    "CGPA/GPA/Percentage not found"
                )
        st.write("### Education Status")

        if education.get("has_degree", False):

            st.success(
                "✅ Education section detected successfully"
            )

        else:

            st.error(
                "❌ Education section not detected"
            )

        # ==================================
        # SUGGESTIONS
        # ==================================

        st.markdown(
            '<p class="section-title">💡 Suggestions</p>',
            unsafe_allow_html=True
        )

        suggestions = result.get(
            "suggestions",
            []
        )

        if suggestions:

            for suggestion in suggestions:

                priority = suggestion.get(
                    "priority",
                    "LOW"
                )

                message = suggestion.get(
                    "message",
                    ""
                )

                if priority == "HIGH":
                    st.error(message)

                elif priority == "MEDIUM":
                    st.warning(message)

                else:
                    st.info(message)

        else:

            st.success(
                "Excellent resume. No major issues found."
            )

        # ==================================
        # RAW TEXT
        # ==================================

        with st.expander("📄 Extracted Resume Text"):

            st.text_area(
                "Resume Text",
                resume_data.get(
                    "raw_text",
                    ""
                ),
                height=300
            )

    except Exception as e:

        st.error(
            f"❌ Error analyzing resume: {e}"
        )

else:

    st.info(
        "Upload your resume to begin ATS analysis."
    )