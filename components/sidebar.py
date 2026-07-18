import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def _nav_button(label: str, page: str, key_suffix: str | None = None):
    # Only show nav buttons for logged-in users
    if not st.session_state.get("is_logged_in", False):
        return

    active = st.session_state.get("page", "Dashboard") == page
    button_label = f"● {label}" if active else f"  {label}"
    key = f"nav_{key_suffix or page}"
    if st.button(button_label, use_container_width=True, key=key):
        st.session_state.page = page


def _section(title: str):
    # Only show sections for logged-in users
    if not st.session_state.get("is_logged_in", False):
        return
    st.markdown(f'<div class="sidebar-section">{title}</div>', unsafe_allow_html=True)


def _theme_toggle():
    # Only show theme toggle for logged-in users
    if not st.session_state.get("is_logged_in", False):
        return

    theme = st.session_state.get("theme", "dark")
    next_theme = "light" if theme == "dark" else "dark"
    label = "☀️ Switch to Light Mode" if theme == "dark" else "🌙 Switch to Dark Mode"

    st.markdown(
        f"""
<div class="theme-chip">
  <span>{'🌙 Dark Mode' if theme == 'dark' else '☀️ Light Mode'}</span>
  <small>Current theme</small>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(label, use_container_width=True, key="theme_toggle"):
        st.session_state.theme = next_theme
        st.rerun()


def render_sidebar():
    with st.sidebar:

        logo_path = BASE_DIR / "assets" / "Logo.png"
        if logo_path.exists():
            st.image(str(logo_path), width=180)
        else:
            if st.session_state.get("is_logged_in", False):
                st.markdown(
                    """
<div class="sidebar-brand">
  <div class="sidebar-mark">🦉</div>
  <div>
    <strong>InstaOwl</strong>
    <span>LMS PLATFORM</span>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
            else:
                # Show login branding when not logged in
                st.markdown(
                    """
<div class="sidebar-brand" style="text-align: center;">
  <div class="sidebar-mark">🦉</div>
  <div>
    <strong>InstaOwl LMS</strong>
    <span>Please log in</span>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )

        # Show login/logout section
        if not st.session_state.get("is_logged_in", False):
            # Login view
            st.markdown(
                """
<div class="sidebar-user">
  <div class="sidebar-avatar">👤</div>
  <div>
    <strong>Please Log In</strong>
    <span>Access your account</span>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
        else:
            # Logged-in user view
            username = st.session_state.get("username", "User")
            user_role = st.session_state.get("user_role", "student")
            display_name = {
                "student": "Student",
                "tutor": "Tutor",
                "admin": "Administrator"
            }.get(user_role, user_role.title())

            # Avatar based on role
            avatar = {
                "student": "👨‍🎓",
                "tutor": "👨‍🏫",
                "admin": "👨‍💼"
            }.get(user_role, "👤")

            st.markdown(
                f"""
<div class="sidebar-user">
  <div class="sidebar-avatar">{avatar}</div>
  <div>
    <strong>{st.session_state.get('student_name', 'User')}</strong>
    <span>{display_name}</span>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

            # Logout button
            if st.button("🚪 Log Out", use_container_width=True, key="logout_button"):
                # Clear login-related session state
                for key in list(st.session_state.keys()):
                    if key.startswith(("is_logged_in", "username", "user_role", "student_name")):
                        if key in ["is_logged_in", "username", "user_role"]:
                            del st.session_state[key]
                    elif key not in ["theme"]:  # Keep theme preference
                        # Reset to defaults for other keys
                        pass

                # Reset to login page
                st.session_state.is_logged_in = False
                st.session_state.page = "Login"
                st.rerun()

        # Only show navigation and theme toggle for logged-in users
        if st.session_state.get("is_logged_in", False):
            _theme_toggle()

            _section("🎓 Learning Space")
            _nav_button("🏠 Dashboard", "Dashboard")
            _nav_button("📚 Courses", "Courses")
            _nav_button("🤖 AI Course", "AI Course")
            _nav_button("🦉 AI Owl", "AI Owl")
            _nav_button("📝 Quiz / Assessment", "Quiz")
            _nav_button("📊 Analytics", "Analytics")
            _nav_button("👤 Profile", "Profile")
            _nav_button("🎓 Certificate", "Certificate")

            _section("🧠 AI Tools")
            _nav_button("🧪 AI Quiz Generator", "Quiz", "ai_quiz")
            _nav_button("📄 AI Syllabus Generator", "AI Syllabus")

            _section("👩‍🏫 Staff Workspace")
            _nav_button("👩‍🏫 Tutor Dashboard", "Tutor")
            _nav_button("🛠 Admin Control Panel", "Admin")
