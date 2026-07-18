import streamlit as st

from components.gemini import generate_syllabus, get_ai_status
from components.session import initialize

initialize()

ready, status_message = get_ai_status()

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>AI Syllabus Generator</h2>
    <p>Draft structured learning pathways in minutes.</p>
  </div>
  <span class="status {'blue' if ready else ''}">{'AI ONLINE' if ready else 'AI FALLBACK'}</span>
</section>

<section class="wire-card syllabus">
  <p class="eyebrow">AI TOOLS</p>
  <h3>{status_message}</h3>
</section>
""",
    unsafe_allow_html=True,
)

st.markdown('<section class="wire-card syllabus">', unsafe_allow_html=True)
course_name = st.text_input("Course Name", placeholder="Introduction to Artificial Intelligence")
col_1, col_2 = st.columns(2)
with col_1:
    level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    audience = st.selectbox("Target Audience", ["CBSE Class 8", "CBSE Class 9", "CBSE Class 10", "CBSE Class 11", "CBSE Class 12"])
with col_2:
    duration = st.selectbox("Course Duration", ["2 Weeks", "4 Weeks", "6 Weeks", "8 Weeks", "12 Weeks"])
    topics = st.text_area("Topics", placeholder="Machine Learning, Deep Learning, NLP...")

if st.button("✨ Generate AI Course", use_container_width=True):
    if not course_name.strip():
        st.warning("Please enter a course name.")
        st.stop()
    with st.spinner("Designing syllabus..."):
        st.session_state.generated_syllabus = generate_syllabus(course_name, level, duration, audience, topics)
st.markdown("</section>", unsafe_allow_html=True)

if st.session_state.get("generated_syllabus"):
    st.markdown('<section class="wire-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.generated_syllabus)
    st.download_button(
        "Download Syllabus",
        st.session_state.generated_syllabus,
        file_name=f"{course_name or 'course'}_syllabus.md",
        use_container_width=True,
    )
    st.markdown("</section>", unsafe_allow_html=True)
