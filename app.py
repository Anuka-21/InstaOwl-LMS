import streamlit as st
from pathlib import Path

from components.session import initialize
from components.sidebar import render_sidebar
from components.router import render_page

BASE_DIR = Path(__file__).resolve().parent


def inject_theme():
    if st.session_state.get("theme", "dark") != "light":
        return

    st.markdown(
        """
<style>
.stApp{
    background:
        radial-gradient(circle at 78% 8%, rgba(37,99,235,.10), transparent 30%),
        radial-gradient(circle at 33% 83%, rgba(245,158,11,.12), transparent 28%),
        #F8FAFC !important;
    color:#0F172A !important;
}

[data-testid="stSidebar"]{
    background:rgba(255,255,255,.88) !important;
    border-right:1px solid #E2E8F0 !important;
}

h1,h2,h3,h4,h5,h6,
.sidebar-brand strong,
.sidebar-user strong,
.wire-card h2,
.wire-card h3,
.card h2,
.card h3,
.feature-card strong,
.flow-item h4,
.metric strong,
.status-tile strong,
.certificate h1,
.certificate h2,
.certificate h3{
    color:#0F172A !important;
}

p,label,span,
.figma-muted,
.card-copy,
.page-head p,
.feature-card p,
.flow-item p,
.sidebar-user span{
    color:#475569 !important;
}

.wire-card,
.card,
.figma-card,
.feature-card,
.status-tile,
.chat-frame,
.ai-composer,
.certificate,
[data-testid="metric-container"]{
    background:rgba(255,255,255,.82) !important;
    border-color:#E2E8F0 !important;
    box-shadow:0 14px 35px rgba(15,23,42,.08) !important;
}

.recommend,
.ai-hero,
.owl-shortcut,
.syllabus,
.metric-card:nth-child(2){
    background:linear-gradient(135deg, rgba(245,158,11,.16), rgba(255,255,255,.86)) !important;
}

.owl-panel{
    background:linear-gradient(180deg, rgba(59,130,246,.12), rgba(255,255,255,.86)) !important;
}

.figma-course-body,
.figma-options span,
.figma-activity,
.flow-item,
.tool-pill,
.quick,
.bubble{
    background:rgba(241,245,249,.82) !important;
    border-color:#E2E8F0 !important;
    color:#334155 !important;
}

.user-bubble,
.figma-chat .user{
    background:rgba(37,99,235,.14) !important;
    color:#1E3A8A !important;
}

[data-testid="stSidebar"] .stButton>button{
    color:#334155 !important;
}

[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(37,99,235,.08) !important;
    color:#1D4ED8 !important;
}

.sidebar-section,
.eyebrow,
.figma-eyebrow,
.figma-date,
.status-tile span{
    color:#64748B !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stDateInput input{
    background:#FFFFFF !important;
    color:#0F172A !important;
    border-color:#CBD5E1 !important;
}

hr{
    border-color:#E2E8F0 !important;
}

.login-hero{
    border-color:#BFDBFE !important;
    background:
        radial-gradient(circle at 90% 20%, rgba(96,165,250,.18), transparent 28%),
        linear-gradient(135deg, rgba(219,234,254,.92), rgba(255,255,255,.94) 60%) !important;
    box-shadow:0 24px 70px rgba(15,23,42,.08) !important;
}

.login-hero h1,
.login-welcome-card h2,
.login-form-heading h2,
.login-hero-badge strong,
.wire-card h2,
.wire-card h3,
.figma-card h2,
.figma-card h3{
    color:#0F172A !important;
}

.login-hero p,
.login-hero-badge>span,
.login-welcome-card>p,
.login-form-heading p{
    color:#475569 !important;
}

.login-hero-badge,
.login-welcome-card,
.login-demo-card,
[data-testid="stForm"]{
    background:rgba(255,255,255,.86) !important;
    border-color:#E2E8F0 !important;
    box-shadow:0 20px 50px rgba(15,23,42,.08) !important;
}

.login-feature-list>div,
[data-testid="stChatMessage"]{
    background:rgba(241,245,249,.82) !important;
    border-color:#E2E8F0 !important;
}

.login-feature-list strong,
.login-demo-row,
[data-testid="stChatMessage"] p{
    color:#334155 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] [data-baseweb="select"]>div,
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stChatInput"]{
    background:#FFFFFF !important;
    color:#0F172A !important;
    border-color:#CBD5E1 !important;
}

[data-testid="stChatInput"] textarea{
    color:#0F172A !important;
}
</style>
""",
        unsafe_allow_html=True,
    )

# ---------------- PAGE ---------------- #

st.set_page_config(
    page_title="InstaOwl LMS",
    page_icon="🦉",
    layout="wide"
)

initialize()

# Check if user is logged in
if not st.session_state.get("is_logged_in", False):
    # Show login page if not logged in
    st.session_state.page = "Login"
else:
    # If logged in but no page set, default to Dashboard
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

# ---------------- CSS ---------------- #

with open(BASE_DIR / "styles" / "style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

inject_theme()

# ---------------- SIDEBAR ---------------- #

# Only show sidebar for logged-in users
if st.session_state.get("is_logged_in", False):
    render_sidebar()

# ---------------- PAGE ROUTER ---------------- #

render_page()
