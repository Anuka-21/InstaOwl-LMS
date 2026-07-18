from datetime import datetime

import pandas as pd
import streamlit as st

from components.session import initialize

initialize()

hour = datetime.now().hour
if hour < 12:
    greeting = "Good Morning"
elif hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

activities = st.session_state.get("activities", ["👋 Welcome to InstaOwl!"])
weekly = pd.DataFrame(
    {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Hours": [1, 2, 1.5, 2.5, 1, 3, 2],
    }
)

progress = int(st.session_state.progress)
course_progress = int(st.session_state.course_progress)
xp = int(st.session_state.xp)
xp_goal = int(st.session_state.xp_goal)
xp_percent = min(round((xp / xp_goal) * 100), 100)

st.markdown(
    f"""
<section class="figma-hero">
  <div>
    <p class="figma-date">{datetime.now().strftime("%A, %d %B")}</p>
    <h1>{greeting}, {st.session_state.student_name}! <span>👋</span></h1>
    <p class="figma-muted">Continue your AI learning journey with InstaOwl.</p>
  </div>
  <div class="figma-top-actions">
    <span class="figma-streak">🔥 {st.session_state.streak} Days</span>
    <span class="figma-avatar">A</span>
  </div>
</section>

<section class="figma-metric-grid">
  <article class="figma-card metric-card">
    <p class="figma-eyebrow">CURRENT LEVEL</p>
    <h3>Level 08 <span>Scholar</span></h3>
    <div class="figma-progress"><i style="width:{xp_percent}%"></i></div>
    <div class="figma-row"><small>{xp} XP</small><small>{xp_goal} XP</small></div>
  </article>
  <article class="figma-card metric-card">
    <p class="figma-eyebrow">TODAY'S GOAL</p>
    <h3>2h 40m</h3>
    <p class="figma-muted">of 3 hours focused study</p>
    <div class="figma-progress amber"><i style="width:78%"></i></div>
  </article>
  <article class="figma-card metric-card">
    <p class="figma-eyebrow">COURSE COMPLETION</p>
    <h3>{progress}%</h3>
    <p class="figma-muted">{st.session_state.completed_modules} module completed</p>
    <div class="figma-progress"><i style="width:{progress}%"></i></div>
  </article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        f"""
<article class="figma-card course-card">
  <div class="figma-card-head">
    <div>
      <p class="figma-eyebrow">CONTINUE LEARNING</p>
      <h2>Your next lesson awaits</h2>
    </div>
    <span class="figma-link">View all courses</span>
  </div>
  <div class="figma-course-body">
    <div class="figma-course-art">⚗️</div>
    <div class="figma-course-copy">
      <div><span class="figma-pill">SCIENCE</span><span class="figma-muted"> • Module 04</span></div>
      <h3>{st.session_state.current_chapter}</h3>
      <p class="figma-muted">Balancing equations & energy changes</p>
      <div class="figma-progress amber"><i style="width:{course_progress}%"></i></div>
      <div class="figma-row"><small>{course_progress}% Complete</small><small>{st.session_state.current_course}</small></div>
    </div>
  </div>
</article>
""",
        unsafe_allow_html=True,
    )

    if st.button("▶ Resume Learning", use_container_width=True):
        st.session_state.page = "AI Course"
        st.rerun()

    st.markdown(
        """
<article class="figma-card quiz-card">
  <div class="figma-card-head">
    <div>
      <p class="figma-eyebrow">QUICK CHECK</p>
      <h2>Can you identify the reaction?</h2>
    </div>
    <span class="figma-pill blue">01 / 03</span>
  </div>
  <p class="figma-question">Which reaction is an example of an <b>exothermic process</b>?</p>
  <div class="figma-options">
    <span><b>A</b> Melting ice</span>
    <span><b>B</b> Photosynthesis</span>
    <span class="selected"><b>C</b> Burning methane</span>
    <span><b>D</b> Evaporating water</span>
  </div>
</article>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<article class="figma-card chart-card">
  <div class="figma-card-head">
    <div>
      <p class="figma-eyebrow">ANALYTICS</p>
      <h2>Your learning rhythm</h2>
    </div>
    <div class="figma-positive">+24.8%<br><small>vs last week</small></div>
  </div>
</article>
""",
        unsafe_allow_html=True,
    )
    st.line_chart(weekly.set_index("Day"), height=220)

with right:
    st.markdown(
        """
<article class="figma-card owl-panel">
  <div class="figma-owl-head">
    <div class="figma-owl-icon">🦉<i></i></div>
    <div>
      <h2>AI Owl</h2>
      <p>Your learning companion</p>
    </div>
    <span>ONLINE</span>
  </div>
  <div class="figma-chat">
    <p class="bot">Hi April! I noticed you're almost done with <b>Chemical Reactions</b>. Want a quick recap before your quiz?</p>
    <p class="user">Yes, explain activation energy!</p>
    <p class="bot blue">Think of it as the initial push needed to get a reaction started — like the spark that lights a match. ✨</p>
  </div>
  <p class="figma-eyebrow">QUICK ACTIONS</p>
</article>
""",
        unsafe_allow_html=True,
    )

    action_1, action_2 = st.columns(2)
    with action_1:
        if st.button("📚 Explain Topic", use_container_width=True):
            st.session_state.page = "AI Owl"
            st.session_state.pending_ai_prompt = "Explain Chemical Reactions in simple steps."
            st.rerun()
    with action_2:
        if st.button("📝 Generate Quiz", use_container_width=True):
            st.session_state.page = "Quiz"
            st.rerun()

    st.markdown('<article class="figma-card compact-card">', unsafe_allow_html=True)
    st.markdown("#### 📅 Today's Schedule")
    st.info("Physics class • Today at 5:00 PM")
    st.markdown("#### 📝 Homework")
    for index, homework in enumerate(st.session_state.get("homework_list", ["No homework assigned"])):
        st.checkbox(homework, key=f"homework_{index}")
    st.markdown("</article>", unsafe_allow_html=True)

    st.markdown('<article class="figma-card compact-card">', unsafe_allow_html=True)
    st.markdown("#### 📌 Recent Activity")
    for item in activities[:4]:
        st.markdown(f'<div class="figma-activity">{item}</div>', unsafe_allow_html=True)
    st.markdown("</article>", unsafe_allow_html=True)

st.markdown(
    f"""
<section class="figma-card recommendation-card">
  <p class="figma-eyebrow">PERSONALIZED RECOMMENDATION</p>
  <h2>Ready for Deep Learning</h2>
  <p>You've mastered the basics. Continue <b>{st.session_state.current_course}</b>, then explore neural networks with AI Owl guidance.</p>
</section>
""",
    unsafe_allow_html=True,
)

if st.button("🚀 Continue to Deep Learning", use_container_width=True):
    st.session_state.page = "AI Course"
    st.rerun()
