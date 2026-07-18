import streamlit as st

def get_achievements():

    achievements = []

    # First Quiz
    if st.session_state.quiz_score > 0:
        achievements.append("📝 First Quiz Completed")

    # XP
    if st.session_state.xp >= 1300:
        achievements.append("⭐ AI Beginner")

    if st.session_state.xp >= 1500:
        achievements.append("🏆 AI Explorer")

    if st.session_state.xp >= 2000:
        achievements.append("👑 AI Master")

    # Progress
    if st.session_state.progress >= 50:
        achievements.append("📚 Halfway There")

    if st.session_state.progress >= 100:
        achievements.append("🎓 Course Completed")

    # Streak
    if st.session_state.streak >= 7:
        achievements.append("🔥 7 Day Streak")

    if st.session_state.streak >= 15:
        achievements.append("💪 Consistency Champion")

    return achievements
