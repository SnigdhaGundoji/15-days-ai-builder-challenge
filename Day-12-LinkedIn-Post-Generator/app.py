import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🚀"
)

st.sidebar.title("🚀 LinkedIn Post Generator")

st.title("🚀 AI LinkedIn Post Generator")

achievement = st.text_area(
    "Describe your achievement:",
    height=200
)

tone = st.selectbox(
    "Post Tone",
    [
        "Professional",
        "Inspirational",
        "Achievement",
        "Learning Journey"
    ]
)

if st.button("Generate LinkedIn Post"):

    if achievement:

        with st.spinner("Generating post..."):

            prompt = f"""
            Create a LinkedIn post.

            Achievement:
            {achievement}

            Tone:
            {tone}

            Include:
            - Hook
            - Main Content
            - Key Learnings
            - Closing
            - Relevant Hashtags
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
                        "content": "You are a professional LinkedIn content writer."
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

                post = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "🚀 Generated LinkedIn Post"
                )

                st.write(post)

                st.download_button(
                    "📥 Download Post",
                    post,
                    file_name="linkedin_post.txt"
                )

            except:

                st.error(
                    "Error generating post"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter an achievement."
        )