import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="📝"
)

st.sidebar.title("📝 AI Quiz Generator")

st.title("📝 AI Quiz Generator")

topic = st.text_input(
    "Enter Quiz Topic:"
)

difficulty = st.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

if st.button("Generate Quiz"):

    if topic:

        with st.spinner(
            "Generating quiz..."
        ):

            prompt = f"""
            Generate a quiz.

            Topic:
            {topic}

            Difficulty:
            {difficulty}

            Include:

            - 10 MCQs
            - 4 options each
            - Correct answer
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
                        "content": "You are an expert quiz creator."
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

                quiz = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📝 Generated Quiz"
                )

                st.write(quiz)

                st.download_button(
                    "📥 Download Quiz",
                    quiz,
                    file_name="quiz.txt"
                )

            except:

                st.error(
                    "Error generating quiz"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter a topic."
        )