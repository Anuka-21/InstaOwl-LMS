from datetime import date

import streamlit as st

from components.session import initialize

initialize()

student = st.session_state.student_name
course = "AI Foundations"
issued = date.today().strftime("%d %B %Y")

st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>Course Certificate</h2>
    <p>Generate and download your completion certificate.</p>
  </div>
  <span class="status">READY</span>
</section>

<section class="certificate">
  <p class="eyebrow">INSTAOwl LEARNING PLATFORM</p>
  <h1>Certificate of<br>Completion</h1>
  <p class="card-copy">This certifies that</p>
  <h2>{student} Hayes</h2>
  <p class="card-copy">has successfully completed the course</p>
  <h3>{course}</h3>
  <div class="row-title">
    <span>{issued}</span>
    <span>InstaOwl Learning Platform<br><b>Learning, made clear.</b></span>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

st.download_button(
    "📄 Download Certificate",
    data=f"""CERTIFICATE OF COMPLETION

Student: {student} Hayes
Course: {course}
Date: {issued}

Issued by InstaOwl Learning Platform""",
    file_name="InstaOwl_Certificate.txt",
    use_container_width=True,
)
