import streamlit as st

from components.session import initialize

initialize()

courses = [
    ("Foundations of Chemistry", "Beginner", 78, "Chemical reactions and lab-ready basics"),
    ("Machine Learning Basics", "Intermediate", 35, "Algorithms, data, training, and predictions"),
    ("World Literature", "Beginner", 62, "Classic and modern prose and poetry"),
    ("Data Visualization", "Intermediate", 12, "Charts, maps, dashboards, and storytelling"),
]

st.markdown(
    """
<section class="page-head">
  <div>
    <h2>Courses</h2>
    <p>Browse enrolled courses and jump back into learning.</p>
  </div>
  <span class="status blue">STUDENT PORTAL</span>
</section>
""",
    unsafe_allow_html=True,
)

search = st.text_input("🔍 Search courses", placeholder="Search courses...")
if search:
    courses = [course for course in courses if search.lower() in course[0].lower()]

st.markdown('<section class="course-grid">', unsafe_allow_html=True)
for index, (title, level, progress, description) in enumerate(courses):
    st.markdown(
        f"""
<article class="wire-card course">
  <div class="course-icon">{title[0]}</div>
  <span class="status">{level}</span>
  <h3>{title}</h3>
  <p class="card-copy">{description}</p>
  <div class="progress-label">
    <div class="wire-meter"><i style="width:{progress}%"></i></div>
    <b>{progress}%</b>
  </div>
</article>
""",
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶ Continue", key=f"course_continue_{index}", use_container_width=True):
            st.session_state.page = "AI Course" if "Machine Learning" in title else "Courses"
            st.rerun()
    with col_b:
        st.button("Details", key=f"course_details_{index}", use_container_width=True)
st.markdown("</section>", unsafe_allow_html=True)

st.markdown(
    """
<section class="wire-card recommend">
  <div class="row-title">
    <div>
      <p class="eyebrow">RECOMMENDED FOR YOU</p>
      <h2>Prompt Engineering for Beginners</h2>
      <p class="card-copy">Learn practical prompting patterns, build your first AI workflow, and complete 6 hands-on exercises.</p>
    </div>
    <span class="status blue">NEW PATH</span>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

if st.button("Explore recommended course", use_container_width=True):
    st.session_state.page = "AI Course"
    st.rerun()
