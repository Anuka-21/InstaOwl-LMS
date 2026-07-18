from pathlib import Path
import runpy

import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]

PAGES = {
    "Login": "login.py",
    "Dashboard": "dashboard.py",
    "Courses": "courses.py",
    "AI Owl": "ai_owl.py",
    "AI Course": "ai_course.py",
    "Quiz": "quiz.py",
    "Analytics": "analytics.py",
    "Profile": "profile.py",
    "Tutor": "tutor.py",
    "Admin": "admin.py",
    "Certificate": "certificate.py",
    "AI Syllabus": "syllabus_generator.py",
}


def render_page():
    page = st.session_state.get("page", "Dashboard")
    page_file = PAGES.get(page)

    if not page_file:
        st.error(f"Unknown page: {page}")
        st.session_state.page = "Dashboard"
        return

    runpy.run_path(str(BASE_DIR / "pages" / page_file), run_name="__main__")
