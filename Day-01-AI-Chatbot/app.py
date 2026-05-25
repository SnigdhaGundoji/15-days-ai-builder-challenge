import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Sidebar
st.sidebar.title("🤖 AI Chatbot")
st.sidebar.write("Built by Snigdha")
st.sidebar.write("Day 1 - AI Builder Challenge")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Main title
st.title("🤖 AI Chatbot")
st.markdown("### Your AI Mentor & Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:

    # Display user message
    st.chat_message("user").markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # API URL
    url = "https://openrouter.ai/api/v1/chat/completions"

    # Headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # AI personality + conversation
    messages = [
        {
            "role": "system",
            "content": (
                "You are a motivational AI mentor. "
                "You help students learn AI, coding, "
                "confidence, communication, and productivity."
            )
        }
    ] + st.session_state.messages

    # Data
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages
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

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })

    except:
        st.error("Error getting response")
        st.write(result)