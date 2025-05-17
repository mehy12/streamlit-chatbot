import streamlit as st
st.title("Streamlit Chatbot")
import os
os.environ["YOUR_API_KEY"]=st.secrets["GOOGLE_API_KEY"]


import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page title and layout
st.set_page_config(page_title="Bushiee – Meesam's Personal AI 🤖", layout="centered")

# Title and intro
st.title("🤖 Bushiee – Meesam's Personal AI")
st.markdown("Welcome! My name is **Bushiee**. How can I help you today?")

# Securely get API key
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", placeholder="Type your message here...")

if user_input:
    # Save user input
    st.session_state.chat_history.append(("You", user_input))

    # Get response from LLM
    response = llm.invoke(user_input)
    st.session_state.chat_history.append(("AI", response.content))

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**👤 You:** {message}")
    else:
        st.markdown(f"**🤖 Bushiee:** {message}")
