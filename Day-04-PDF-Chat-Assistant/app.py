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
    page_title="PDF Chat Assistant",
    page_icon="📄"
)

# Sidebar
st.sidebar.title("📄 PDF Chat Assistant")

st.sidebar.write("Upload PDFs and ask questions.")

# Title
st.title("📄 AI PDF Chat Assistant")

st.write("Upload a PDF and ask questions from it.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

pdf_text = ""

# Extract PDF text
if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        pdf_text += page.extract_text()

    st.success("PDF uploaded successfully!")

# User question
user_question = st.text_input(
    "Ask a question from the PDF:"
)

# Ask button
if st.button("Ask AI"):

    if pdf_text and user_question:

        with st.spinner("Reading PDF and generating answer..."):

            # Prompt
            prompt = f"""
            Answer the question using the PDF content below.

            PDF Content:
            {pdf_text}

            Question:
            {user_question}
            """

            # API URL
            url = "https://openrouter.ai/api/v1/chat/completions"

            # Headers
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Request data
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful PDF assistant."
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

                st.subheader("📌 Answer")

                st.write(ai_response)

            except:

                st.error("Error processing PDF")

                st.write(result)