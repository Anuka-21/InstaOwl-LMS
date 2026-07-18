import streamlit as st
from components.session import initialize

initialize()

# Initialize login-related session state
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = "student"  # student, tutor, admin

# Demo users database (in a real app, this would be a real database)
DEMO_USERS = {
    "student": {"password": "student123", "role": "student", "name": "April Hayes"},
    "tutor": {"password": "tutor123", "role": "tutor", "name": "Alex Johnson"},
    "admin": {"password": "admin123", "role": "admin", "name": "Sam Wilson"}
}

def login_form():
    """Display login form"""
    st.markdown(
        """
        <section class="login-hero">
          <div class="login-hero-copy">
            <span class="login-kicker">INSTAOWL LEARNING PLATFORM</span>
            <h1>Learn with clarity.<br><span>Grow with confidence.</span></h1>
            <p>Your focused learning space for courses, practice, AI guidance, and measurable progress.</p>
          </div>
          <div class="login-hero-badge">
            <div class="login-owl-mark">🦉</div>
            <strong>Ready when you are</strong>
            <span>Personalized learning, one step at a time.</span>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown(
            """
            <section class="login-welcome-card">
              <span class="eyebrow">A BETTER STUDY RHYTHM</span>
              <h2>Everything you need to keep moving.</h2>
              <p>Build momentum with a calm dashboard, bite-sized lessons, and an AI tutor that explains concepts in your language.</p>
              <div class="login-feature-list">
                <div><b>01</b><span><strong>Learn at your pace</strong><small>Clear lessons with progress you can see.</small></span></div>
                <div><b>02</b><span><strong>Practice with purpose</strong><small>Quizzes and feedback that build confidence.</small></span></div>
                <div><b>03</b><span><strong>Ask AI Owl anything</strong><small>Helpful guidance whenever you get stuck.</small></span></div>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="login-form-heading">
              <span class="eyebrow">WELCOME BACK</span>
              <h2>Sign in to continue</h2>
              <p>Choose a demo account to explore InstaOwl.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            username = st.selectbox(
                "Account type",
                options=list(DEMO_USERS.keys()),
                format_func=lambda x: {
                    "student": "Student Account",
                    "tutor": "Tutor Account",
                    "admin": "Admin Account"
                }[x]
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your demo password",
            )

            col_a, col_b = st.columns([1, 1])
            with col_a:
                submit_button = st.form_submit_button("Continue  →", use_container_width=True, type="primary")
            with col_b:
                clear_button = st.form_submit_button("Clear", use_container_width=True)

            if clear_button:
                st.rerun()

            if submit_button:
                if username in DEMO_USERS and DEMO_USERS[username]["password"] == password:
                    st.session_state.is_logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = DEMO_USERS[username]["role"]

                    # Update session with user-specific data
                    user_data = DEMO_USERS[username]
                    st.session_state.student_name = user_data["name"]

                    # Set role-specific defaults
                    if username == "admin":
                        st.session_state.xp = 5000
                        st.session_state.streak = 30
                        st.session_state.progress = 100
                        st.session_state.courses = 12
                    elif username == "tutor":
                        st.session_state.xp = 2500
                        st.session_state.streak = 45
                        st.session_state.progress = 85
                        st.session_state.courses = 8
                    else:  # student
                        st.session_state.xp = 1260
                        st.session_state.streak = 15
                        st.session_state.progress = 63
                        st.session_state.courses = 6

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("""
        <div class="login-demo-card">
          <div class="login-demo-heading"><span class="eyebrow">DEMO ACCESS</span><span class="status blue">3 ACCOUNTS</span></div>
          <div class="login-demo-row"><strong>Student</strong><code>student123</code></div>
          <div class="login-demo-row"><strong>Tutor</strong><code>tutor123</code></div>
          <div class="login-demo-row"><strong>Admin</strong><code>admin123</code></div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main login page for direct execution"""
    if st.session_state.is_logged_in:
        # If already logged in, redirect to dashboard
        st.session_state.page = "Dashboard"
        st.rerun()
    else:
        login_form()

if __name__ == "__main__":
    main()
