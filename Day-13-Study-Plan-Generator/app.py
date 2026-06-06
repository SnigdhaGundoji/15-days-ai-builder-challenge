import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="Study Plan Generator",
    page_icon="📚"
)

st.sidebar.title("📚 Study Plan Generator")

st.title("📚 AI Study Plan Generator")

goal = st.text_input(
    "Enter your learning goal:"
)

duration = st.number_input(
    "Number of Days",
    min_value=1,
    max_value=365,
    value=30
)

if st.button("Generate Study Plan"):

    if goal:

        with st.spinner(
            "Creating study plan..."
        ):

            prompt = f"""
            Create a study plan.

            Goal:
            {goal}

            Duration:
            {duration} days

            Include:

            - Weekly roadmap
            - Important topics
            - Practice suggestions
            - Final project idea
            """

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert study mentor."
                    },
                    {
                        "role": "user",
                        "content": prompt
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

                study_plan = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📚 Study Plan"
                )

                st.write(
                    study_plan
                )

                st.download_button(
                    "📥 Download Plan",
                    study_plan,
                    file_name="study_plan.txt"
                )

            except:

                st.error(
                    "Error generating plan"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter a goal."
        )