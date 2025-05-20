import streamlit as st
import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# ✅ Streamlit config
st.set_page_config(page_title="🧾 TaxGPT - Chat with your Tax Docs", layout="centered")

st.title("🧾 TaxGPT - Ask your Tax & Audit Questions")

# 🔐 API Key from secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 📎 File uploader
uploaded_file = st.file_uploader("Upload a CA-related PDF (e.g., GST Act)", type="pdf")

# 🤖 Initialize chatbot only if PDF uploaded
if uploaded_file:
    # Save to temp file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # 🔍 Load and split PDF
    loader = PyMuPDFLoader("temp.pdf")
    pages = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(pages)

    # 📚 Vector DB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = FAISS.from_documents(docs, embeddings)

    # 🔁 Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 💬 RAG Chain
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(),
        memory=memory
    )

    # 🧠 Chat history init
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ✍️ Chat input
    user_input = st.chat_input("Ask a question about the document...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = qa_chain.run(user_input)
            st.markdown(response)
            st.session_state.chat_history.append((user_input, response))

    # 📝 Display chat history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Bot:** {a}")

else:
    st.info("📄 Please upload a PDF to begin chatting.")
