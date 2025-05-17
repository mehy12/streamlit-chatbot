import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# 🚨 Set page config FIRST — before any Streamlit elements
st.set_page_config(page_title="Bushiee – Meesam's Personal AI 🤖", layout="centered")

# Now it's safe to call other st.* functions
st.title("🤖 Bushiee – Meesam's Personal AI")
st.markdown("Welcome! My name is **Bushiee**. How can I help you today?")

# Load API key from secrets
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input("You:", placeholder="Type your message here...")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    response = llm.invoke(user_input)
    st.session_state.chat_history.append(("AI", response.content))

# Display messages
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**👤 You:** {message}")
    else:
        st.markdown(f"**🤖 Bushiee:** {message}")
