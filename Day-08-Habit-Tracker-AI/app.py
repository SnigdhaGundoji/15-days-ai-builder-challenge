import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="Habit Tracker AI",
    page_icon="✅"
)

# Sidebar
st.sidebar.title("✅ Habit Tracker AI")
st.sidebar.write(
    "Track and improve your habits using AI."
)

# Main Title
st.title("✅ Habit Tracker AI")

st.write(
    "Enter your habits and get tracking suggestions."
)

# Input
habits = st.text_area(
    "Enter your habits:",
    height=250
)

# Counters
st.write(
    "Word Count:",
    len(habits.split())
)

# Button
if st.button("Analyze Habits"):

    if habits:

        with st.spinner(
            "Analyzing habits..."
        ):

            prompt = f"""
            Analyze these habits.

            Give:

            1. Habit Categories
            2. Tracking Suggestions
            3. Consistency Tips
            4. Weekly Improvement Advice
            5. Priority Habits

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
                    "📊 Habit Analysis"
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

            except:

                st.error(
                    "Error analyzing habits"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter some habits."
        )