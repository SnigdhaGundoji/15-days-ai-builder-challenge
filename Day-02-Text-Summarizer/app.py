import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝"
)

# Title
st.title("📝 AI Text Summarizer")

st.write("Paste your text below and get a summary.")

# Text input
user_text = st.text_area(
    "Enter long text:",
    height=250
    
)
# Word Counter
word_count = len(user_text.split())

st.write("Word Count:", word_count)

# Summary type
summary_type = st.selectbox(
    "Choose summary type:",
    [
        "Short Summary",
        "Bullet Points",
        "Simple Explanation"
    ]
)

# Button
if st.button("Generate Summary"):

    if user_text:

        with st.spinner("Generating summary..."):

            # Prompt engineering
            prompt = f"""
            Summarize the following text as:
            {summary_type}

            Text:
            {user_text}
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
                        "content": "You are an expert text summarizer."
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

                summary = result["choices"][0]["message"]["content"]

                st.subheader("Summary Result")

                st.success(summary)

            except:

                st.error("Error generating summary")
                st.write(result)