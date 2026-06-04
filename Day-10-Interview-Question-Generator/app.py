import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="🎯"
)

st.sidebar.title("🎯 Interview Question Generator")

st.title("🎯 AI Interview Question Generator")

topic = st.text_input(
    "Enter a topic or skill:"
)

level = st.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

if st.button("Generate Questions"):

    if topic:

        with st.spinner(
            "Generating questions..."
        ):

            prompt = f"""
            Generate interview questions on:

            Topic: {topic}

            Difficulty: {level}

            Provide:

            1. 10 Interview Questions
            2. 3 Important Concepts
            3. Interview Preparation Tips
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
                        "You are an expert technical interviewer."
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

                questions = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "🎯 Interview Questions"
                )

                st.write(questions)

                st.download_button(
                    "📥 Download Questions",
                    questions,
                    file_name="interview_questions.txt"
                )

            except:

                st.error(
                    "Error generating questions"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter a topic."
        )