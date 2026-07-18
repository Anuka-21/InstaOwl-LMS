import streamlit as st

from components.session import initialize

initialize()

modules = [
    ("Introduction to AI", 0, "Complete", "Core concepts and terminology"),
    ("Machine Learning Fundamentals", 20, "Unlocked", "Training data, models, and prediction"),
    ("Neural Networks", 45, "Locked", "Layers, weights, and backpropagation"),
    ("Ethics & Responsible AI", 70, "Locked", "Bias, safety, and real-world impact"),
]

st.markdown(
    f"""
<section class="ai-hero">
  <div>
    <p class="eyebrow">AI COURSE PATH</p>
    <h2>AI Foundations</h2>
    <p class="card-copy">Build a clear foundation in artificial intelligence from basics to applications.</p>
  </div>
  <div class="circle">{st.session_state.progress}%</div>
</section>

<section class="metric-grid four">
  <article class="wire-card metric"><p>Progress</p><strong>{st.session_state.progress}%</strong><small>Current path completion</small></article>
  <article class="wire-card metric"><p>Lessons</p><strong>25</strong><small>Across 4 core modules</small></article>
  <article class="wire-card metric"><p>Certificate</p><strong>Ready</strong><small>Unlock at 100%</small></article>
  <article class="wire-card metric"><p>XP Reward</p><strong>+740</strong><small>Available in this path</small></article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown(
        """
<section class="wire-card">
  <div class="row-title">
    <div>
      <p class="eyebrow">SYLLABUS ROADMAP</p>
      <h3>Four modules to complete</h3>
    </div>
    <span class="status blue">1 OF 4 COMPLETE</span>
  </div>
""",
        unsafe_allow_html=True,
    )
    for index, (title, required, state, copy) in enumerate(modules, start=1):
        done = st.session_state.progress >= required
        st.markdown(
            f"""
<div class="road {'done' if done else ''}">
  <span class="road-dot">{'✓' if done else index}</span>
  <div class="road-content">
    <div class="row-title">
      <div>
        <h3>{title}</h3>
        <p class="card-copy">{copy}</p>
      </div>
      <span class="status {'blue' if done else ''}">{state if done else 'LOCKED'}</span>
    </div>
    <div class="wire-meter"><i style="width:{min(st.session_state.progress, 100) if done else required}%"></i></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</section>", unsafe_allow_html=True)

with right:
    st.markdown(
        """
<section class="wire-card">
  <p class="eyebrow">CURRENT LESSON</p>
  <h3>Machine Learning Basics</h3>
  <p class="card-copy">Learn supervised learning, unsupervised learning, training data, testing data, and real-life applications.</p>
</section>
""",
        unsafe_allow_html=True,
    )
    st.video("https://www.youtube.com/watch?v=JMUxmLyrhSk")

    if st.button("📝 Take Quiz", use_container_width=True):
        st.session_state.page = "Quiz"
        st.rerun()
    if st.button("🦉 Ask AI Owl", use_container_width=True):
        st.session_state.page = "AI Owl"
        st.rerun()

st.markdown(
    """
<section class="wire-card recommend">
  <p class="eyebrow">LEARNING RESOURCES</p>
  <h3>Download study materials</h3>
  <p class="card-copy">Notes and cheat sheets for quick revision.</p>
</section>
""",
    unsafe_allow_html=True,
)

col_1, col_2 = st.columns(2)
with col_1:
    st.download_button("Download AI Notes", "Artificial Intelligence Notes\n\nModule 1: Introduction\nModule 2: Machine Learning", file_name="AI_Notes.txt", use_container_width=True)
with col_2:
    st.download_button("Download Cheat Sheet", "Python • ML • AI Cheat Sheet", file_name="AI_CheatSheet.txt", use_container_width=True)
