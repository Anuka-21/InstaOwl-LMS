import streamlit as st

from components.gemini import ask_gemini_stream, get_ai_status
from components.session import initialize

initialize()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! 👋 I'm AI Owl. I can explain topics, generate quizzes, summarize notes, and help with homework step by step.",
        }
    ]

ready, status_message = get_ai_status()


def queue_prompt(prompt: str):
    st.session_state.pending_ai_prompt = prompt
    st.rerun()


def clear_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Fresh page, sharp pencil. 🦉 What should we learn next?",
        }
    ]
    st.rerun()


st.markdown(
    f"""
<section class="page-head">
  <div>
    <h2>AI Owl</h2>
    <p>Your organized AI tutor for explanations, quizzes, notes, homework, and performance coaching.</p>
  </div>
  <span class="status {'blue' if ready else ''}">{'GEMINI ONLINE' if ready else 'LOCAL FALLBACK'}</span>
</section>

<section class="wire-card owl-panel">
  <div class="figma-owl-head">
    <div class="figma-owl-icon">🦉<i></i></div>
    <div>
      <h2>{'Gemini connected' if ready else 'Local AI fallback active'}</h2>
      <p>{status_message}</p>
    </div>
    <span>{'ONLINE' if ready else 'FALLBACK'}</span>
  </div>
</section>

<section class="feature-grid">
  <article class="feature-card"><span class="status blue">01</span><strong>Explain</strong><p>Break hard concepts into simple steps and examples.</p></article>
  <article class="feature-card"><span class="status">02</span><strong>Practice</strong><p>Create quiz questions, answer keys, and revision drills.</p></article>
  <article class="feature-card"><span class="status blue">03</span><strong>Coach</strong><p>Analyze progress, XP, streaks, and suggest next actions.</p></article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.45, 0.75], gap="large")

with left:
    st.markdown('<section class="chat-frame">', unsafe_allow_html=True)
    st.markdown('<p class="eyebrow">LIVE TUTOR CHAT</p>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    pending_prompt = st.session_state.pop("pending_ai_prompt", None)
    typed_prompt = st.chat_input("Ask AI Owl anything...")
    prompt = pending_prompt or typed_prompt

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            reply = st.write_stream(ask_gemini_stream(st.session_state.messages))

        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown("</section>", unsafe_allow_html=True)

with right:
    st.markdown(
        f"""
<section class="wire-card">
  <p class="eyebrow">LEARNING CONTEXT</p>
  <h3>{st.session_state.current_course}</h3>
  <p class="card-copy">{st.session_state.current_chapter}</p>
  <div class="wire-meter"><i style="width:{st.session_state.course_progress}%"></i></div>
  <div class="admin-status-grid" style="margin-top:1rem;grid-template-columns:1fr 1fr;">
    <div class="status-tile"><span>XP</span><strong>{st.session_state.xp}</strong></div>
    <div class="status-tile"><span>Streak</span><strong>{st.session_state.streak} days</strong></div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<section class="ai-composer"><p class="eyebrow">QUICK AI TOOLS</p>', unsafe_allow_html=True)
    if st.button("📚 Explain current chapter", use_container_width=True):
        queue_prompt(f"Explain {st.session_state.current_chapter} from {st.session_state.current_course} in simple steps with one example.")

    if st.button("📝 Generate practice quiz", use_container_width=True):
        queue_prompt(f"Generate a 5 question quiz on {st.session_state.current_chapter}. Include answers and short explanations.")

    if st.button("📄 Summarize notes format", use_container_width=True):
        queue_prompt("Give me a clean format to paste messy notes so you can summarize them into key points, terms, and revision questions.")

    if st.button("🏠 Homework helper", use_container_width=True):
        queue_prompt("Help me solve homework step by step. Ask for the exact question and guide me without only giving the final answer.")

    if st.button("📊 Analyze my performance", use_container_width=True):
        queue_prompt(
            f"Analyze my learning performance. Progress: {st.session_state.progress}%, "
            f"XP: {st.session_state.xp}, streak: {st.session_state.streak} days, "
            f"quiz score: {st.session_state.quiz_score}. Give 3 specific next steps."
        )

    st.markdown("</section>", unsafe_allow_html=True)

    if st.button("🗑 Clear chat", use_container_width=True):
        clear_chat()

st.markdown(
    """
<section class="wire-card">
  <p class="eyebrow">SUGGESTED STUDY FLOW</p>
  <div class="ordered-flow">
    <div class="flow-item"><b>1</b><div><h4>Ask for a simple explanation</h4><p>Start with the core idea and one example.</p></div><span class="status blue">LEARN</span></div>
    <div class="flow-item"><b>2</b><div><h4>Generate a short quiz</h4><p>Check recall immediately after learning.</p></div><span class="status">PRACTICE</span></div>
    <div class="flow-item"><b>3</b><div><h4>Review mistakes</h4><p>Turn weak areas into a mini revision plan.</p></div><span class="status blue">IMPROVE</span></div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)
