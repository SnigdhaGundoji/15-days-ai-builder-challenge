import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Notes Organizer",
    page_icon="📝"
)

# Sidebar
st.sidebar.title("📝 AI Notes Organizer")
st.sidebar.write("Organize messy notes using AI")

# Title
st.title("📝 AI Notes Organizer")

st.write(
    "Paste your notes and let AI organize them."
)

# Notes Input
notes_text = st.text_area(
    "Paste your notes here:",
    height=250
)

# Counters
st.write(
    "Word Count:",
    len(notes_text.split())
)

st.write(
    "Character Count:",
    len(notes_text)
)

# Button
if st.button("Organize Notes"):

    if notes_text:

        with st.spinner("Organizing notes..."):

            prompt = f"""
            Organize the following notes.

            Group similar topics together.

            Add headings and bullet points.

            Notes:

            {notes_text}
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
                        "content":
                        "You are an expert note organizer."
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

                organized_notes = result[
                    "choices"
                ][0]["message"]["content"]

                st.subheader(
                    "📚 Organized Notes"
                )

                st.write(
                    organized_notes
                )

                with st.expander(
                    "View Organized Notes"
                ):
                    st.code(
                        organized_notes
                    )

            except:

                st.error(
                    "Error organizing notes"
                )

                st.write(result)

    else:

        st.warning(
            "Please enter some notes."
        )