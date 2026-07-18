import streamlit as st

from components.achievements import get_achievements
from components.session import initialize

initialize()

badges = get_achievements()

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>Student Profile</h2>
    <p>Manage your learner identity, achievements, and settings.</p>
  </div>
  <span class="status blue">LEVEL 08</span>
</section>

<section class="wire-card profile-hero row-title">
  <div class="profile-avatar">A</div>
  <div>
    <p class="eyebrow">STUDENT PROFILE</p>
    <h2>{st.session_state.student_name} Hayes <span class="status blue">SCHOLAR</span></h2>
    <p class="card-copy">april@student.com · CBSE Class 10 · InstaOwl Learning · India</p>
  </div>
  <span class="status">🔥 {st.session_state.streak} DAY STREAK</span>
</section>

<section class="metric-grid four">
  <article class="wire-card metric"><p>COURSES COMPLETED</p><strong>{st.session_state.courses}</strong><small>of 12 enrolled</small></article>
  <article class="wire-card metric"><p>TOTAL XP</p><strong>{st.session_state.xp}</strong><small>Level 08 Scholar</small></article>
  <article class="wire-card metric"><p>CERTIFICATES</p><strong>{st.session_state.certificates}</strong><small>Ready to share</small></article>
  <article class="wire-card metric"><p>QUIZ SCORE</p><strong>{st.session_state.quiz_score}</strong><small>Latest quiz result</small></article>
</section>
""",
    unsafe_allow_html=True,
)

st.markdown('<section class="wire-card"><p class="eyebrow">ACCOMPLISHMENTS</p><h3>Milestone timeline</h3>', unsafe_allow_html=True)
if badges:
    for index, badge in enumerate(badges, start=1):
        st.markdown(f'<div class="figma-activity"><b>{index:02d}</b> · {badge}</div>', unsafe_allow_html=True)
else:
    st.info("Complete lessons and quizzes to unlock achievements.")
st.markdown("</section>", unsafe_allow_html=True)

st.markdown(
    """
<section class="wire-card recommend">
  <p class="eyebrow">CERTIFICATES</p>
  <h3>AI Foundations</h3>
  <p class="card-copy">Completed · Certificate ready for download.</p>
</section>
""",
    unsafe_allow_html=True,
)

if st.button("📄 Open Certificate", use_container_width=True):
    st.session_state.page = "Certificate"
    st.rerun()

st.markdown('<section class="wire-card syllabus"><p class="eyebrow">ACCOUNT SETTINGS</p><h3>Profile details</h3>', unsafe_allow_html=True)
st.text_input("Full Name", "April Hayes")
st.text_input("Email", "april@student.com")
st.selectbox("Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"], index=2)
st.button("Save Changes", use_container_width=True)
st.markdown("</section>", unsafe_allow_html=True)
