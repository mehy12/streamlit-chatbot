import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="Bushiee – Meesam's Personal AI 🤖", layout="centered")

# 🌟 Sidebar for branding
with st.sidebar:
    st.title("🤖 Bushiee")
    st.markdown("Welcome to Meesam’s personal AI assistant!")
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# 💬 Load chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔐 Load API key
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# 🤖 Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 💬 Display conversation history
for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(message)

# ⌨️ Chat input at bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("You", user_input))

    # Call Gemini model
    with st.chat_message("assistant"):
        response = llm.invoke(user_input)
        st.markdown(response.content)
        st.session_state.chat_history.append(("AI", response.content))
