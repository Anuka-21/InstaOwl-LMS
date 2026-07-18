import streamlit as st

def initialize():

    defaults = {

        # Authentication state
        "is_logged_in": False,
        "username": "",
        "user_role": "student",

        "student_name": "April",

        "theme": "dark",

        "xp": 1260,

        "streak": 15,

        "progress": 63,  # Aligned with 1260/2000 XP (63%)

        "completed_modules": 1,

        "quiz_score": 0,

        "certificates": 2,  # Aligned with 2 certificates earned

        "homework": 3,

        "courses": 6,

        "current_course": "Science",

        "current_chapter": "Chemical Reactions",

        "course_progress": 78,

        "recommended_course": "Mathematics",

        "recommended_topic": "Machine Learning Basics",

        "quiz_history": [84, 90, 74, 88, 92],

        "notifications": [
            "Physics class at 5 PM",
            "Homework due tomorrow"
        ],

        "achievements": [],

        "xp_goal": 2000,

        "homework_list": [
            "Physics homework due tomorrow",
            "Maths worksheet 3"
        ],

        "activities": [
            "Completed “Energy Changes” lesson · Science",
            "Scored 8 / 10 on Chemistry Quiz",
            "Earned 120 XP from daily study goal"
        ]
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
