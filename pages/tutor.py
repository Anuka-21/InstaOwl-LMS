import pandas as pd
import streamlit as st

from components.gemini import generate_lesson, generate_quiz_items, get_ai_status
from components.session import initialize

initialize()

ready, status_message = get_ai_status()

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>Tutor Dashboard</h2>
    <p>Manage courses, students, assignments, live classes, and AI content.</p>
  </div>
  <span class="status {'blue' if ready else ''}">{'AI ONLINE' if ready else 'AI FALLBACK'}</span>
</section>

<section class="metric-grid four">
  <article class="wire-card metric"><p>STUDENTS</p><strong>245</strong><small>+12 this month</small></article>
  <article class="wire-card metric"><p>ACTIVE COURSES</p><strong>8</strong><small>3 running today</small></article>
  <article class="wire-card metric"><p>ASSIGNMENTS</p><strong>14</strong><small>8 to review</small></article>
  <article class="wire-card metric"><p>COMPLETION RATE</p><strong>82%</strong><small>+3.2% from last term</small></article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown('<section class="wire-card syllabus"><p class="eyebrow">MODULE MANAGEMENT</p><h3>Add a course module</h3>', unsafe_allow_html=True)
    course = st.text_input("Course Name")
    module = st.text_input("Module Name")
    video = st.text_input("Video Link")
    st.file_uploader("Upload Notes (PDF)", type=["pdf"])
    if st.button("➕ Add Module", use_container_width=True):
        st.success(f"Module {module or 'Untitled'} added successfully!")
    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown('<section class="wire-card"><p class="eyebrow">STUDENT PERFORMANCE</p><h3>Progress overview</h3>', unsafe_allow_html=True)
    students = pd.DataFrame({"Student": ["April", "Rahul", "Priya", "Ananya", "Aman"], "Progress": [35, 60, 92, 48, 71]})
    st.dataframe(students, use_container_width=True)
    st.bar_chart(students.set_index("Student"), height=230)
    st.markdown("</section>", unsafe_allow_html=True)

with right:
    st.markdown('<section class="wire-card recommend"><p class="eyebrow">LIVE CLASS</p><h3>Schedule a session</h3>', unsafe_allow_html=True)
    st.text_input("Live Class Title")
    st.date_input("Class Date")
    st.time_input("Class Time")
    if st.button("Schedule Live Class", use_container_width=True):
        st.success("Live class scheduled.")
    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown(f'<section class="wire-card owl-panel"><p class="eyebrow">AI STATUS</p><h3>{status_message}</h3></section>', unsafe_allow_html=True)

st.markdown('<section class="wire-card syllabus"><p class="eyebrow">AI QUIZ GENERATOR</p><h3>Create tutor quiz</h3>', unsafe_allow_html=True)
topic = st.text_input("Enter Topic")
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
questions = st.slider("Number of Questions", 5, 20, 10)

if st.button("⚡ Generate Quiz", use_container_width=True):
    if not topic.strip():
        st.warning("Enter a topic before generating a quiz.")
    else:
        with st.spinner("Generating tutor quiz..."):
            st.session_state.tutor_generated_quiz = generate_quiz_items(topic, difficulty, questions)

if st.session_state.get("tutor_generated_quiz"):
    for index, item in enumerate(st.session_state.tutor_generated_quiz, start=1):
        st.markdown(f"**Q{index}. {item['question']}**")
        st.caption("Options: " + ", ".join(item["options"]))
        st.caption(f"Answer: {item['answer']}")
st.markdown("</section>", unsafe_allow_html=True)

st.markdown('<section class="wire-card syllabus"><p class="eyebrow">AI LESSON GENERATOR</p><h3>Generate lesson outline</h3>', unsafe_allow_html=True)
lesson = st.text_input("Lesson Topic")
level = st.selectbox("Student Level", ["Beginner", "Intermediate", "Advanced"])
if st.button("Generate Lesson", use_container_width=True):
    if not lesson.strip():
        st.warning("Enter a lesson topic first.")
    else:
        with st.spinner("Generating lesson outline..."):
            st.session_state.tutor_generated_lesson = generate_lesson(lesson, level)

if st.session_state.get("tutor_generated_lesson"):
    st.markdown(st.session_state.tutor_generated_lesson)
st.markdown("</section>", unsafe_allow_html=True)
