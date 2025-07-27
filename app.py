import streamlit as st
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

# --- CONFIGURATION ---
DATA_PATH = "data/"
MODEL_NAME = "llama3" # Make sure this model is pulled in Ollama

# --- RAG PIPELINE ---

# 1. Load Documents
@st.cache_resource
def load_and_index_documents():
    """
    Loads documents from the data directory, splits them, creates embeddings,
    and builds a FAISS vector store. This is cached to avoid reloading on every run.
    """
    # Using the more stable TextLoader to avoid NLTK dependency issues.
    # This treats .md files as plain text, which is sufficient for this use case.
    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf8'},
        show_progress=True
    )
    documents = loader.load()

    # 2. Split Documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)

    # 3. Create Embeddings and Vector Store
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever()

# --- STREAMLIT UI ---

st.set_page_config(page_title="Indian Travel Visa AI Agent", page_icon="✈️")

st.title("✈️ Indian Travel Visa AI Agent")
st.markdown("""
Welcome! I can help you with visa information for Indian citizens for a few selected countries.
""")

# Load the retriever once
retriever = load_and_index_documents()

# Initialize the LLM
llm = Ollama(model=MODEL_NAME)

# Define the prompt template
prompt_template = """
You are an expert AI assistant for Indian travelers. Your task is to answer visa-related questions based on the provided context.
- Answer ONLY from the context provided.
- If the information is not in the context, clearly state "I don't have information on that in my current knowledge base."
- Structure your answer clearly using bullet points or lists if needed.
- Be friendly and helpful.
"

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Create the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# User input
user_question = st.text_input("Ask your visa question:", placeholder="What are the documents needed for a Schengen tourist visa?")

if st.button("Get Visa Info"):
    if user_question:
        with st.spinner("Searching for the best answer..."):
            response = rag_chain.invoke(user_question)
            st.markdown(response)
    else:
        st.warning("Please enter a question.")

st.sidebar.header("About")
st.sidebar.info("This is a demo AI agent using Streamlit, Ollama, and LangChain to answer visa questions for Indian travelers.")
