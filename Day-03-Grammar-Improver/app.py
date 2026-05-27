import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI Grammar Improver",
    page_icon="✍️",
    layout="centered"
)

# Sidebar
st.sidebar.title("✍️ AI Grammar Improver")

st.sidebar.write("Built by Snigdha")

st.sidebar.write("Improve your English using AI")

# Main title
st.title("✍️ AI Grammar & English Improver")

st.write("Improve your grammar, fluency, and communication using AI.")

# User input
user_text = st.text_area(
    "Enter your sentence or paragraph:",
    height=200
)

# Word Counter
word_count = len(user_text.split())

st.write("Word Count:", word_count)

# Character Counter
char_count = len(user_text)

st.write("Character Count:", char_count)

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

# Example text button
if st.button("Use Example Text"):
    user_text = "i wants improve my communication skill"

# Improve button
if st.button("Improve Text"):

    # Check if text exists
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
                            "You are a professional English teacher "
                            "and grammar correction assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            # Send API request
            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            # Convert response to JSON
            result = response.json()

            try:

                # Extract AI response
                ai_response = result["choices"][0]["message"]["content"]

                # Display heading
                st.subheader("✨ Improved English")

                # Display response
                st.write(ai_response)

                # Expandable section
                with st.expander("See Full Response"):

                    # Copy-style output
                    st.code(ai_response)

            except:

                st.error("Error improving text")

                st.write(result)