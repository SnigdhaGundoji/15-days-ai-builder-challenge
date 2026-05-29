import streamlit as st
import requests
import os
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

# Sidebar
st.sidebar.title("📄 AI Resume Analyzer")
st.sidebar.write("Upload your resume and get AI feedback")

# Main Title
st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume PDF and get professional feedback."
)

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

resume_text = ""

# Extract Text
if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    total_pages = len(pdf_reader.pages)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text

    st.success("Resume uploaded successfully!")

    st.write("Pages:", total_pages)

    st.write(
        "Word Count:",
        len(resume_text.split())
    )

# Analyze Button
if st.button("Analyze Resume"):

    if resume_text:

        with st.spinner("Analyzing Resume..."):

            prompt = f"""
            Analyze the following resume.

            Provide:

            1. Strengths
            2. Weaknesses
            3. Missing Skills
            4. Improvement Suggestions
            5. Resume Score out of 10
            6. Suitable Job Roles

            Resume:

            {resume_text}
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
                        "content": (
                            "You are an expert HR manager, "
                            "career coach, and resume reviewer."
                        )
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

                analysis = result["choices"][0]["message"]["content"]

                st.subheader("📊 Resume Analysis")

                st.write(analysis)

                with st.expander(
                    "View Full Analysis"
                ):
                    st.code(analysis)

            except:

                st.error(
                    "Error analyzing resume"
                )

                st.write(result)

    else:

        st.warning(
            "Please upload a resume first."
        )