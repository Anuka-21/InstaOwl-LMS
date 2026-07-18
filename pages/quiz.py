import streamlit as st
from components.session import initialize

initialize()

# Quiz data - in a real app, this would come from a database or API
QUIZ_DATA = {
    "Science": {
        "Chemical Reactions": [
            {
                "question": "Which reaction is an example of an exothermic process?",
                "options": ["Melting ice", "Photosynthesis", "Burning methane", "Evaporating water"],
                "correct_answer": 2,  # Index of correct answer (0-based)
                "explanation": "Burning methane releases heat to the surroundings, making it exothermic."
            },
            {
                "question": "What is the chemical formula for water?",
                "options": ["H2O", "CO2", "O2", "NaCl"],
                "correct_answer": 0,
                "explanation": "Water consists of two hydrogen atoms and one oxygen atom, hence H2O."
            },
            {
                "question": "Which particle has a negative charge?",
                "options": ["Proton", "Neutron", "Electron", "Neutrino"],
                "correct_answer": 2,
                "explanation": "Electrons have a negative charge, while protons are positive and neutrons are neutral."
            }
        ]
    },
    "Mathematics": {
        "Algebra Basics": [
            {
                "question": "What is the solution to 2x + 5 = 15?",
                "options": ["x = 3", "x = 5", "x = 7", "x = 10"],
                "correct_answer": 1,
                "explanation": "Subtract 5 from both sides: 2x = 10, then divide by 2: x = 5."
            }
        ]
    }
}

def initialize_quiz_state():
    """Initialize quiz-related session state variables."""
    if "quiz_mode" not in st.session_state:
        st.session_state.quiz_mode = "take"  # take, review, or generate

    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

def get_available_quizzes():
    """Get list of available quizzes."""
    return list(QUIZ_DATA.keys())

def get_quiz_categories(course):
    """Get categories for a given course."""
    return list(QUIZ_DATA.get(course, {}).keys())

def get_quiz_questions(course, category):
    """Get questions for a given course and category."""
    return QUIZ_DATA.get(course, {}).get(category, [])

def render_quiz_selection():
    """Render the quiz selection interface."""
    st.markdown(
        """
        <section class="page-head">
          <div>
            <h2>Quiz & Assessment Center</h2>
            <p>Test your knowledge and track your progress</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Quiz selection
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<p class="figma-eyebrow">SELECT COURSE</p>', unsafe_allow_html=True)
        courses = get_available_quizzes()
        selected_course = st.selectbox(
            "Choose a course",
            courses,
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<p class="figma-eyebrow">SELECT TOPIC</p>', unsafe_allow_html=True)
        if selected_course:
            categories = get_quiz_categories(selected_course)
            selected_category = st.selectbox(
                "Choose a topic",
                categories,
                label_visibility="collapsed"
            )
        else:
            selected_category = None
            st.selectbox("Choose a topic", [], label_visibility="collapsed", disabled=True)

    if selected_course and selected_category:
        st.session_state.current_quiz = {
            "course": selected_course,
            "category": selected_category,
            "questions": get_quiz_questions(selected_course, selected_category)
        }

        # Initialize quiz state when changing quiz
        if st.button("Start Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_mode = "take"
            st.session_state.current_question_index = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.rerun()

def render_take_quiz():
    """Render the quiz taking interface."""
    if not st.session_state.current_quiz:
        st.warning("Please select a quiz to begin.")
        return

    quiz = st.session_state.current_quiz
    questions = quiz["questions"]
    current_idx = st.session_state.current_question_index

    if current_idx >= len(questions):
        # Quiz completed
        render_quiz_results()
        return

    question = questions[current_idx]

    # Progress indicator
    progress = (current_idx + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {current_idx + 1} of {len(questions)}")

    # Question display
    st.markdown(f"""
    <div class="figma-card quiz-question-card">
      <div class="figma-question">{question['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options
    selected_option = st.radio(
        "Select your answer:",
        options=range(len(question["options"])),
        format_func=lambda x: f"{chr(65 + x)}) {question['options'][x]}",
        key=f"q_{current_idx}",
        label_visibility="collapsed"
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()

    with col3:
        if current_idx < len(questions) - 1:
            if st.button("Next →", use_container_width=True, type="primary"):
                # Store answer
                st.session_state.quiz_answers[current_idx] = selected_option
                st.session_state.current_question_index += 1
                st.rerun()
        else:
            if st.button("Submit Quiz", use_container_width=True, type="primary"):
                # Store answer for last question
                st.session_state.quiz_answers[current_idx] = selected_option
                st.session_state.quiz_mode = "review"
                st.session_state.quiz_submitted = True

                # Calculate score
                score = 0
                for i, q in enumerate(questions):
                    if i in st.session_state.quiz_answers and st.session_state.quiz_answers[i] == q["correct_answer"]:
                        score += 1

                st.session_state.quiz_score = score
                st.session_state.quiz_score_percentage = int((score / len(questions)) * 100)

                # Update session state quiz score
                if "quiz_history" not in st.session_state:
                    st.session_state.quiz_history = []

                # Add to quiz history (keep last 5)
                st.session_state.quiz_history.append(st.session_state.quiz_score_percentage)
                if len(st.session_state.quiz_history) > 5:
                    st.session_state.quiz_history = st.session_state.quiz_history[-5:]

                st.rerun()

def render_quiz_results():
    """Render the quiz results screen."""
    if not st.session_state.current_quiz:
        # If we somehow got here without a current quiz, go to selection
        st.session_state.quiz_mode = "select"
        st.rerun()
        
    quiz = st.session_state.current_quiz
    questions = quiz["questions"]
    score = st.session_state.quiz_score
    total = len(questions)
    percentage = st.session_state.quiz_score_percentage

    st.markdown(
        f"""
        <section class="page-head">
          <div>
            <h2>Quiz Complete!</h2>
            <p>You scored {score}/{total} ({percentage}%)</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Score visualization
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="figma-card metric-card">
          <p class="figma-eyebrow">YOUR SCORE</p>
          <h3>{percentage}%</h3>
          <p class="figma-muted">{score} out of {total} correct</p>
          <div class="figma-progress"><i style="width:{percentage}%"></i></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Performance feedback
        if percentage >= 90:
            feedback = "Excellent work! 🌟"
            color = "green"
        elif percentage >= 70:
            feedback = "Good job! Keep improving. 👍"
            color = "blue"
        elif percentage >= 50:
            feedback = "You're getting there. Review the material. 📚"
            color = "orange"
        else:
            feedback = "Keep practicing. You'll improve! 💪"
            color = "red"

        st.markdown(f"""
        <div class="figma-card">
          <p class="figma-eyebrow">FEEDBACK</p>
          <h3 style="color: {color};">{feedback}</h3>
        </div>
        """, unsafe_allow_html=True)

    # Question review
    st.markdown('<p class="figma-eyebrow">QUESTION REVIEW</p>', unsafe_allow_html=True)

    for i, question in enumerate(questions):
        user_answer = st.session_state.quiz_answers.get(i, None)
        correct_answer = question["correct_answer"]
        is_correct = user_answer == correct_answer

        # Determine card styling based on correctness
        border_color = "#10B981" if is_correct else ("#EF4444" if user_answer is not None else "#6B7280")
        bg_color = "#D1FAE5" if is_correct else ("#FEE2E2" if user_answer is not None else "#F3F4F6")

        st.markdown(f"""
        <div class="figma-card" style="border-left: 4px solid {border_color}; background-color: {bg_color};">
          <div class="figma-question">{question['question']}</div>
          <div style="margin: 1rem 0;">
        """, unsafe_allow_html=True)

        for j, option in enumerate(question["options"]):
            is_selected = user_answer == j
            is_correct_option = j == correct_answer

            if is_correct_option and is_selected:
                label = f"✓ {chr(65 + j)}) {option} (Correct!)"
                style = "color: #059669; font-weight: bold;"
            elif is_correct_option:
                label = f"✓ {chr(65 + j)}) {option}"
                style = "color: #059669; font-weight: 600;"
            elif is_selected:
                label = f"✗ {chr(65 + j)}) {option}"
                style = "color: #DC2626; font-weight: bold;"
            else:
                label = f"○ {chr(65 + j)}) {option}"
                style = "color: #6B7280;"

            st.markdown(f'<p style="{style}">{label}</p>', unsafe_allow_html=True)

        if not is_correct and "explanation" in question:
            st.markdown(f"""
            <p class="figma-muted">💡 Explanation: {question['explanation']}</p>
            """, unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Retake Quiz", use_container_width=True):
            st.session_state.current_question_index = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_mode = "take"
            st.rerun()

    with col2:
        if st.button("Try Different Quiz", use_container_width=True):
            st.session_state.current_quiz = None
            st.session_state.quiz_mode = "select"
            st.rerun()

    with col3:
        if st.button("View Quiz History", use_container_width=True):
            st.session_state.quiz_mode = "history"
            st.rerun()

def render_quiz_history():
    """Render quiz history and statistics."""
    st.markdown(
        """
        <section class="page-head">
          <div>
            <h2>Quiz History</h2>
            <p>Track your progress over time</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if "quiz_history" not in st.session_state or not st.session_state.quiz_history:
        st.info("You haven't taken any quizzes yet. Start a quiz to see your history here!")
        if st.button("Take Your First Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_mode = "select"
            st.rerun()
        return

    history = st.session_state.quiz_history

    # Statistics
    avg_score = sum(history) / len(history)
    best_score = max(history)
    latest_score = history[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="figma-card metric-card">
          <p class="figma-eyebrow">AVERAGE SCORE</p>
          <h3>{int(avg_score)}%</h3>
          <p class="figma-muted">over {len(history)} quizzes</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="figma-card metric-card">
          <p class="figma-eyebrow">BEST SCORE</p>
          <h3>{best_score}%</h3>
          <p class="figma-muted">personal record</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="figma-card metric-card">
          <p class="figma-eyebrow">LATEST SCORE</p>
          <h3>{latest_score}%</h3>
          <p class="figma-muted">most recent attempt</p>
        </div>
        """, unsafe_allow_html=True)

    # History chart
    if len(history) > 1:
        import pandas as pd
        df = pd.DataFrame({
            "Quiz Attempt": list(range(1, len(history) + 1)),
            "Score (%)": history
        })
        st.line_chart(df.set_index("Quiz Attempt"), height=250)

    # Detailed history
    st.markdown('<p class="figma-eyebrow">RECENT ATTEMPTS</p>', unsafe_allow_html=True)

    for i, score in enumerate(reversed(history[-5:]), 1):
        attempt_num = len(history) - i + 1
        if score >= 90:
            status = "🌟 Excellent"
        elif score >= 70:
            status = "👍 Good"
        elif score >= 50:
            status = "📚 Needs Improvement"
        else:
            status = "💪 Keep Trying"

        st.markdown(f"""
        <div class="figma-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>Attempt #{attempt_num}</span>
            <span><strong>{score}%</strong> {status}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Back to Quiz Selection", use_container_width=True):
        st.session_state.quiz_mode = "select"
        st.rerun()

# Main application logic
initialize_quiz_state()

# Check if we came from AI Quiz Generator with a pending prompt
if st.session_state.get("quiz_mode") == "generate" and st.session_state.get("pending_ai_prompt"):
    # This would integrate with AI quiz generation - for now, redirect to selection
    st.session_state.quiz_mode = "select"
    st.session_state.pending_ai_prompt = None
    st.info("AI Quiz Generator feature coming soon! Please select a quiz manually.")
    st.rerun()

# Auto-switch to selection mode if in take/review mode but no quiz selected
if (st.session_state.quiz_mode == "take" or st.session_state.quiz_mode == "review") and not st.session_state.current_quiz:
    st.session_state.quiz_mode = "select"

# Route to appropriate view based on mode
if st.session_state.quiz_mode == "select":
    render_quiz_selection()
elif st.session_state.quiz_mode == "take":
    render_take_quiz()
elif st.session_state.quiz_mode == "review":
    render_quiz_results()
elif st.session_state.quiz_mode == "history":
    render_quiz_history()
