import streamlit as st
import google.generativeai as genai
from typing import List, Dict

# Configure page settings
st.set_page_config(
    page_title="Vibe ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Initialize Gemini-1.5-flash
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat title
st.title("🤖 Vibe ChatBot")
st.subheader("Powered by Gemini 1.5 Flash")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare chat history for Gemini
            chat_history = [
                {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                for msg in st.session_state.messages[:-1]  # Exclude the latest user message
            ]
            
            # Start chat and get response
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
            
            # Display and store assistant's response
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text}) 