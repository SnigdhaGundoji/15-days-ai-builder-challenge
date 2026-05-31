import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="Daily Planner AI",
    page_icon="📅"
)

# Sidebar
st.sidebar.title("📅 Daily Planner AI")
st.sidebar.write(
    "Generate a productive daily schedule using AI."
)

# Title
st.title("📅 Daily Planner AI")

st.write(
    "Enter your tasks and let AI create a schedule."
)

# Input
tasks = st.text_area(
    "Enter your tasks:",
    height=250
)

# Counters
st.write(
    "Word Count:",
    len(tasks.split())
)

# Button
if st.button("Generate Plan"):

    if tasks:

        with st.spinner(
            "Creating your daily plan..."
        ):

            prompt = f"""
            Create a realistic daily schedule.

            Organize the following tasks:

            {tasks}

            Give:
            - Time slots
            - Priority order
            - Productivity tips
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
                        "You are a productivity coach."
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

                plan = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📋 Your Daily Plan"
                )

                st.write(plan)

                with st.expander(
                    "View Full Plan"
                ):
                    st.code(plan)

            except:

                st.error(
                    "Error generating plan"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter some tasks."
        )