import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Email Writer",
    page_icon="📧"
)

st.sidebar.title("📧 AI Email Writer")

st.title("📧 AI Email Writer")

purpose = st.text_input(
    "Email Purpose"
)

tone = st.selectbox(
    "Email Tone",
    [
        "Professional",
        "Friendly",
        "Formal",
        "Polite"
    ]
)

if st.button("Generate Email"):

    if purpose:

        with st.spinner(
            "Writing email..."
        ):

            prompt = f"""
            Write an email.

            Purpose:
            {purpose}

            Tone:
            {tone}

            Include:
            - Subject
            - Greeting
            - Email Body
            - Closing
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
                        "You are a professional email writer."
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

                email_text = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📧 Generated Email"
                )

                st.write(
                    email_text
                )

                st.download_button(
                    "📥 Download Email",
                    email_text,
                    file_name="email.txt"
                )

            except:

                st.error(
                    "Error generating email"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter a purpose."
        )