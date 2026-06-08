import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🚀"
)

st.sidebar.title("🚀 AI Career Coach")

st.title("🚀 AI Career Coach")

skills = st.text_area(
    "Enter Your Skills:"
)

career_goal = st.text_input(
    "Enter Career Goal:"
)

if st.button("Generate Career Plan"):

    if skills and career_goal:

        with st.spinner(
            "Analyzing profile..."
        ):

            prompt = f"""
            Skills:
            {skills}

            Career Goal:
            {career_goal}

            Provide:

            1. Current Strengths
            2. Missing Skills
            3. Learning Roadmap
            4. Project Suggestions
            5. Career Advice
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
                        "content": "You are an experienced career mentor."
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

                career_plan = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "🚀 Career Plan"
                )

                st.write(
                    career_plan
                )

                st.download_button(
                    "📥 Download Plan",
                    career_plan,
                    file_name="career_plan.txt"
                )

            except:

                st.error(
                    "Error generating plan"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter skills and career goal."
        )
        