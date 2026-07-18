import pandas as pd
import streamlit as st

from components.session import initialize

initialize()

study = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "Hours": [1.2, 2, 1.5, 3, 2.5, 4, 2]})
quiz = pd.DataFrame({"Quiz": ["Quiz 1", "Quiz 2", "Quiz 3", "Quiz 4"], "Score": [70, 80, 90, st.session_state.quiz_score * 20]})

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>Learning Analytics</h2>
    <p>Track your rhythm, XP, quiz scores, and course progress.</p>
  </div>
  <span class="status blue">+24.8% VS LAST WEEK</span>
</section>
<section class="metric-grid four">
  <article class="wire-card metric"><p>TOTAL XP</p><strong>{st.session_state.xp}</strong><small>+320 this month</small></article>
  <article class="wire-card metric"><p>CURRENT STREAK</p><strong>{st.session_state.streak} Days</strong><small>Personal best: 21</small></article>
  <article class="wire-card metric"><p>COURSES</p><strong>{st.session_state.courses} / 12</strong><small>50% completion</small></article>
  <article class="wire-card metric"><p>AVG. QUIZ SCORE</p><strong>86%</strong><small>+4% improvement</small></article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.35, 1], gap="large")
with left:
    st.markdown(
        """
<section class="wire-card">
  <div class="row-title">
    <div>
      <p class="eyebrow">XP GAINED</p>
      <h3>Weekly study hours</h3>
    </div>
    <span class="status blue">LIVE</span>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )
    st.line_chart(study.set_index("Day"), height=260)

with right:
    st.markdown(
        """
<section class="wire-card">
  <p class="eyebrow">QUIZ PERFORMANCE</p>
  <h3>Recent attempts</h3>
</section>
""",
        unsafe_allow_html=True,
    )
    st.bar_chart(quiz.set_index("Quiz"), height=260)

st.markdown(
    """
<section class="wire-card">
  <div class="row-title">
    <div>
      <p class="eyebrow">COURSE COMPLETION</p>
      <h3>Current enrollments</h3>
    </div>
    <span class="status">IN PROGRESS</span>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

st.dataframe(
    pd.DataFrame({"Course": ["AI Foundations", "Python", "Science", "Mathematics"], "Completion": [35, 60, 78, 52]}),
    use_container_width=True,
)

st.markdown(
    """
<section class="wire-card recommend">
  <p class="eyebrow">AI LEARNING INSIGHTS</p>
  <h3>Excellent consistency</h3>
  <p class="card-copy">Start attempting harder modules and keep practicing quiz recall after each lesson.</p>
</section>
""",
    unsafe_allow_html=True,
)
