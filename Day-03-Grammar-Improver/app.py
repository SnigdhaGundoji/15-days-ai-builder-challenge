import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Grammar Improver",
    page_icon="✍️"
)

# Title
st.title("✍️ AI Grammar & English Improver")

st.write("Improve your English using AI.")

# User input
user_text = st.text_area(
    "Enter your sentence or paragraph:",
    height=200
)

# Improvement type
improvement_type = st.selectbox(
    "Choose improvement style:",
    [
        "Correct Grammar",
        "Professional English",
        "Simple English",
        "Fluent English"
    ]
)

# Button
if st.button("Improve Text"):

    if user_text:

        with st.spinner("Improving your English..."):

            # Prompt
            prompt = f"""
            Improve the following text.

            Style:
            {improvement_type}

            Text:
            {user_text}

            Also explain the mistakes briefly.
            """

            # API URL
            url = "https://openrouter.ai/api/v1/chat/completions"

            # Headers
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Data
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an expert English teacher "
                            "and grammar correction assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            # API request
            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            result = response.json()

            try:

                ai_response = result["choices"][0]["message"]["content"]

                st.subheader("Improved Text")

                st.success(ai_response)

            except:

                st.error("Error improving text")
                st.write(result)