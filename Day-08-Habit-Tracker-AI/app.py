import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page Config
st.set_page_config(
    page_title="Habit Tracker AI",
    page_icon="✅"
)

# Sidebar
st.sidebar.title("✅ Habit Tracker AI")
st.sidebar.write(
    "Track and improve your habits using AI."
)

# Title
st.title("✅ Habit Tracker AI")

st.write(
    "Enter your habits and get personalized improvement suggestions."
)

# Habit Category
habit_type = st.selectbox(
    "Habit Focus",
    [
        "Health",
        "Learning",
        "Career",
        "Fitness",
        "Productivity"
    ]
)

# Consistency Level
experience = st.selectbox(
    "Current Consistency Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Current Streak
streak = st.number_input(
    "Current Habit Streak (Days)",
    min_value=0,
    value=0
)

# Habits Input
habits = st.text_area(
    "Enter your habits:",
    height=250
)

# Word Count
st.write(
    "Word Count:",
    len(habits.split())
)

# Character Count
st.write(
    "Character Count:",
    len(habits)
)

# Progress Bar
st.progress(
    min(len(habits) / 500, 1.0)
)

# Analyze Button
if st.button("Analyze Habits"):

    if habits:

        with st.spinner(
            "Analyzing habits..."
        ):

            prompt = f"""
            Analyze these habits.

            Habit Focus:
            {habit_type}

            Consistency Level:
            {experience}

            Current Streak:
            {streak} days

            Give:

            1. Habit Categories
            2. Tracking Suggestions
            3. Consistency Tips
            4. Weekly Improvement Advice
            5. Priority Habits
            6. Weekly Habit Score out of 100
            7. Top 3 Habits To Focus On First
            8. Personalized Motivation Message

            Habits:

            {habits}
            """

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization":
                f"Bearer {API_KEY}",
                "Content-Type":
                "application/json"
            }

            data = {
                "model":
                "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role":
                        "system",
                        "content":
                        "You are an expert habit coach."
                    },
                    {
                        "role":
                        "user",
                        "content":
                        prompt
                    }
                ]
            }

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            result = response.json()

            try:

                habit_report = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📊 Habit Analysis Report"
                )

                st.write(
                    habit_report
                )

                with st.expander(
                    "View Full Report"
                ):
                    st.code(
                        habit_report
                    )

                # Download Button
                st.download_button(
                    label="📥 Download Report",
                    data=habit_report,
                    file_name="habit_report.txt",
                    mime="text/plain"
                )

            except:

                st.error(
                    "Error analyzing habits"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter some habits."
        )