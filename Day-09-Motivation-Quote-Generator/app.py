import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="Motivation Quote Generator",
    page_icon="💡"
)

# Sidebar
st.sidebar.title("💡 Motivation Generator")
st.sidebar.write(
    "Generate motivational quotes using AI."
)

# Main Title
st.title("💡 Motivation Quote Generator")

st.write(
    "Describe your situation and get motivation."
)

# Situation Input
situation = st.text_area(
    "Describe your situation:",
    height=200
)

# Mood Selection
mood = st.selectbox(
    "Select Mood",
    [
        "Study",
        "Career",
        "Fitness",
        "Failure",
        "Success",
        "General"
    ]
)

# Generate Button
if st.button("Generate Motivation"):

    if situation:

        with st.spinner(
            "Generating motivation..."
        ):

            prompt = f"""
            Situation:
            {situation}

            Mood:
            {mood}

            Generate:

            1. Motivational Quote
            2. Short Advice
            3. One Action Step
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
                        "You are a motivational coach."
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

                motivation = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "🔥 Your Motivation"
                )

                st.write(
                    motivation
                )

                with st.expander(
                    "View Full Motivation"
                ):
                    st.code(
                        motivation
                    )

                st.download_button(
                    "📥 Download Motivation",
                    motivation,
                    file_name="motivation.txt"
                )

            except:

                st.error(
                    "Error generating motivation"
                )

                st.write(result)

    else:

        st.warning(
            "Please describe your situation."
        )