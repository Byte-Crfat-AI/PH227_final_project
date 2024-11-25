import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate


PERSIST_DIRECTORY = "Data\chroma.sqlite3"
GEMINI_API = "AIzaSyCTzgU213N2OTNL5_1ZcOymcnTRLwh7IjM"

# Initialize Components
st.set_page_config(page_title="Physics Department Chatbot", layout="centered")
st.title("QuantumQubie")

# Load RAG Database
embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-large")
db = Chroma(
    persist_directory=PERSIST_DIRECTORY,  
    embedding_function=embeddings,        
)
retriever = db.as_retriever()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API)

# Create RetrievalQA Chain
prompt_template = """You are an AI assistant for the Physics Department at IIT Bombay. Use the following context to answer.
Context:
{context}

Question:
{question}

Answer the question in detail."""
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)

# Streamlit Chat UI
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using .apply()
    result = qa_chain.apply([{"query": user_input}])[0]  # First result
    response = result["result"]  # Main answer

    # Append and display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

