import pandas as pd
import streamlit as st

from components.gemini import generate_course_outline, generate_quiz_items, get_ai_status
from components.session import initialize

initialize()

ai_ready, ai_message = get_ai_status()

if "admin_users" not in st.session_state:
    st.session_state.admin_users = [
        {"Name": "April Hayes", "Role": "Student", "Status": "Active"},
        {"Name": "Rahul Mehta", "Role": "Student", "Status": "Active"},
        {"Name": "Priya Shah", "Role": "Tutor", "Status": "Active"},
        {"Name": "Ananya Rao", "Role": "Student", "Status": "Inactive"},
        {"Name": "Aman Verma", "Role": "Tutor", "Status": "Active"},
    ]

if "admin_courses" not in st.session_state:
    st.session_state.admin_courses = [
        {"Course": "AI Foundations", "Level": "Beginner", "Status": "Published"},
        {"Course": "Science", "Level": "Intermediate", "Status": "Published"},
        {"Course": "Mathematics", "Level": "Intermediate", "Status": "Draft"},
        {"Course": "Python", "Level": "Beginner", "Status": "Published"},
    ]

if "admin_announcements" not in st.session_state:
    st.session_state.admin_announcements = ["Welcome to the upgraded InstaOwl LMS dashboard."]

users_df = pd.DataFrame(st.session_state.admin_users)
courses_df = pd.DataFrame(st.session_state.admin_courses)

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>Admin Control Panel</h2>
    <p>Ordered command center for users, courses, AI tools, broadcasts, and platform health.</p>
  </div>
  <span class="status {'blue' if ai_ready else ''}">{'AI CONNECTED' if ai_ready else 'AI FALLBACK'}</span>
</section>

<section class="metric-grid four">
  <article class="wire-card metric"><p>STUDENTS</p><strong>1,248</strong><small>+42 this month</small></article>
  <article class="wire-card metric"><p>TUTORS</p><strong>36</strong><small>+2 this month</small></article>
  <article class="wire-card metric"><p>COURSES</p><strong>{len(st.session_state.admin_courses)}</strong><small>Managed in portal</small></article>
  <article class="wire-card metric"><p>COMPLETION RATE</p><strong>82%</strong><small>+4% improvement</small></article>
</section>
""",
    unsafe_allow_html=True,
)

overview_tab, users_tab, courses_tab, ai_tab, system_tab = st.tabs(
    ["01 Overview", "02 Users", "03 Courses", "04 AI Studio", "05 System"]
)

with overview_tab:
    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        st.markdown('<section class="wire-card"><p class="eyebrow">PLATFORM ANALYTICS</p><h3>Student growth</h3>', unsafe_allow_html=True)
        analytics = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Students": [420, 520, 610, 790, 980, 1248]})
        st.line_chart(analytics.set_index("Month"), height=280)
        st.markdown("</section>", unsafe_allow_html=True)

    with right:
        st.markdown(
            f"""
<section class="wire-card health">
  <div>
    <p class="eyebrow">SYSTEM SUMMARY</p>
    <h3>All core services healthy</h3>
    <p class="card-copy">{ai_message}</p>
  </div>
</section>
<section class="admin-status-grid">
  <div class="status-tile"><span>Server</span><strong>Online</strong></div>
  <div class="status-tile"><span>Database</span><strong>Connected</strong></div>
  <div class="status-tile"><span>Storage</span><strong>Healthy</strong></div>
  <div class="status-tile"><span>AI Owl</span><strong>{'Online' if ai_ready else 'Fallback'}</strong></div>
</section>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<section class="wire-card">
  <p class="eyebrow">ADMIN WORKFLOW</p>
  <div class="ordered-flow">
    <div class="flow-item"><b>1</b><div><h4>Review platform health</h4><p>Check server, AI, database, and storage before publishing content.</p></div><span class="status blue">MONITOR</span></div>
    <div class="flow-item"><b>2</b><div><h4>Manage users and roles</h4><p>Add tutors, review active students, and export user records.</p></div><span class="status">USERS</span></div>
    <div class="flow-item"><b>3</b><div><h4>Create AI content</h4><p>Generate course outlines and assessments from Admin AI Studio.</p></div><span class="status blue">AI</span></div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )

with users_tab:
    left, right = st.columns([1.25, 0.75], gap="large")

    with left:
        st.markdown('<section class="wire-card"><p class="eyebrow">USER MANAGEMENT</p><h3>Current platform users</h3>', unsafe_allow_html=True)
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        st.download_button("Download Users CSV", users_df.to_csv(index=False), file_name="instaowl_users.csv", use_container_width=True)
        st.markdown("</section>", unsafe_allow_html=True)

    with right:
        st.markdown('<section class="wire-card syllabus"><p class="eyebrow">ADD TUTOR</p><h3>Create staff account</h3>', unsafe_allow_html=True)
        name = st.text_input("Tutor Name", key="admin_tutor_name")
        email = st.text_input("Email", key="admin_tutor_email")
        subject = st.selectbox("Subject", ["Artificial Intelligence", "Mathematics", "Science", "English", "Computer Science"], key="admin_tutor_subject")
        if st.button("Add Tutor", use_container_width=True, key="admin_add_tutor"):
            if not name.strip() or not email.strip():
                st.warning("Enter tutor name and email.")
            else:
                st.session_state.admin_users.append({"Name": name.strip(), "Role": "Tutor", "Status": f"Active · {subject}"})
                st.success(f"{name.strip()} added as tutor.")
                st.rerun()
        st.markdown("</section>", unsafe_allow_html=True)

with courses_tab:
    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.markdown('<section class="wire-card"><p class="eyebrow">COURSE MANAGEMENT</p><h3>Course catalog</h3>', unsafe_allow_html=True)
        st.dataframe(courses_df, use_container_width=True, hide_index=True)
        selected_course = st.selectbox("Select Course", courses_df["Course"], key="admin_selected_course")
        edit_col, archive_col = st.columns(2)
        with edit_col:
            if st.button("✏ Mark Published", use_container_width=True, key="admin_publish_existing"):
                for course in st.session_state.admin_courses:
                    if course["Course"] == selected_course:
                        course["Status"] = "Published"
                st.success(f"{selected_course} marked as published.")
                st.rerun()
        with archive_col:
            if st.button("Archive Course", use_container_width=True, key="admin_archive_course"):
                for course in st.session_state.admin_courses:
                    if course["Course"] == selected_course:
                        course["Status"] = "Archived"
                st.warning(f"{selected_course} archived.")
                st.rerun()
        st.markdown("</section>", unsafe_allow_html=True)

    with right:
        st.markdown('<section class="wire-card syllabus"><p class="eyebrow">UPLOAD NEW COURSE</p><h3>Publish content</h3>', unsafe_allow_html=True)
        course_name = st.text_input("Course Name", key="admin_new_course")
        course_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], key="admin_new_course_level")
        st.file_uploader("Upload Video", type=["mp4"], key="admin_course_video")
        st.file_uploader("Upload PDF Notes", type=["pdf"], key="admin_course_notes")
        if st.button("Publish Course", use_container_width=True, key="admin_publish_course"):
            if not course_name.strip():
                st.warning("Enter a course name.")
            else:
                st.session_state.admin_courses.append({"Course": course_name.strip(), "Level": course_level, "Status": "Published"})
                st.success(f"{course_name.strip()} published.")
                st.rerun()
        st.markdown("</section>", unsafe_allow_html=True)

with ai_tab:
    st.markdown(
        f"""
<section class="wire-card owl-panel">
  <div class="figma-owl-head">
    <div class="figma-owl-icon">🦉<i></i></div>
    <div>
      <h2>Admin AI Studio</h2>
      <p>{ai_message}</p>
    </div>
    <span>{'ONLINE' if ai_ready else 'FALLBACK'}</span>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )

    course_col, quiz_col = st.columns(2, gap="large")

    with course_col:
        st.markdown('<section class="wire-card syllabus"><p class="eyebrow">AI COURSE GENERATOR</p><h3>Generate course outline</h3>', unsafe_allow_html=True)
        topic = st.text_input("Topic", key="admin_ai_course_topic")
        level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"], key="admin_ai_course_level")
        if st.button("Generate Course Outline", use_container_width=True, key="admin_generate_course"):
            if not topic.strip():
                st.warning("Enter a topic before generating a course.")
            else:
                with st.spinner("Generating course structure..."):
                    st.session_state.admin_course_outline = generate_course_outline(topic, level)
        if st.session_state.get("admin_course_outline"):
            st.markdown(st.session_state.admin_course_outline)
            st.download_button("Download Outline", st.session_state.admin_course_outline, file_name="course_outline.md", use_container_width=True)
        st.markdown("</section>", unsafe_allow_html=True)

    with quiz_col:
        st.markdown('<section class="wire-card syllabus"><p class="eyebrow">AI QUIZ MANAGEMENT</p><h3>Create assessment</h3>', unsafe_allow_html=True)
        quiz = st.text_input("Quiz Topic", key="admin_ai_quiz_topic")
        questions = st.number_input("Number of Questions", 5, 50, 10, key="admin_ai_quiz_questions")
        if st.button("Create Quiz", use_container_width=True, key="admin_create_quiz"):
            if not quiz.strip():
                st.warning("Enter a quiz topic first.")
            else:
                with st.spinner("Creating quiz..."):
                    st.session_state.admin_generated_quiz = generate_quiz_items(quiz, "Medium", int(questions))
        if st.session_state.get("admin_generated_quiz"):
            for index, item in enumerate(st.session_state.admin_generated_quiz, start=1):
                st.markdown(f"**Q{index}. {item['question']}**")
                st.caption("Options: " + ", ".join(item["options"]))
                st.caption(f"Answer: {item['answer']}")
        st.markdown("</section>", unsafe_allow_html=True)

with system_tab:
    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown('<section class="wire-card syllabus"><p class="eyebrow">BROADCAST ANNOUNCEMENT</p><h3>Send platform message</h3>', unsafe_allow_html=True)
        announcement = st.text_area("Message", key="admin_announcement")
        if st.button("Send Announcement", use_container_width=True, key="admin_send_announcement"):
            if not announcement.strip():
                st.warning("Enter an announcement message.")
            else:
                st.session_state.admin_announcements.insert(0, announcement.strip())
                st.success("Announcement sent.")
                st.rerun()
        st.markdown("</section>", unsafe_allow_html=True)

    with right:
        st.markdown('<section class="wire-card"><p class="eyebrow">RECENT ANNOUNCEMENTS</p><h3>Broadcast log</h3>', unsafe_allow_html=True)
        for item in st.session_state.admin_announcements[:5]:
            st.markdown(f'<div class="figma-activity">{item}</div>', unsafe_allow_html=True)
        st.markdown("</section>", unsafe_allow_html=True)

    st.markdown(
        """
<section class="wire-card">
  <p class="eyebrow">SYSTEM STATUS</p>
  <div class="admin-status-grid">
    <div class="status-tile"><span>LMS Server</span><strong>Online</strong></div>
    <div class="status-tile"><span>AI Owl</span><strong>Connected / Fallback Safe</strong></div>
    <div class="status-tile"><span>Database</span><strong>Connected</strong></div>
    <div class="status-tile"><span>Storage</span><strong>Healthy</strong></div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )
