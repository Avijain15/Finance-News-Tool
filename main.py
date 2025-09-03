import os
import streamlit as st
import pickle
import time
import asyncio
import nest_asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially google api key)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for animations and styling
st.set_page_config(page_title="RockyBot", page_icon="🤖", layout="centered", initial_sidebar_state="expanded")
st.markdown("""
<style>
    .stApp {
        background-color: #f9fbff;
        color: #2b2b2b;
    }
    /* Ensure main block has light background */
    .block-container {
        background: #fff7f7;
    }
    /* Force light backgrounds for main view and sidebar */
    [data-testid="stAppViewContainer"] {
        background-color: #fff7f7;
    }
    [data-testid="stHeader"] {
        background: #fff7f7 !important;
        border-bottom: 1px solid #ffd6d6;
    }
    [data-testid="stSidebar"] {
        background: #ffeaea !important;
    }
    [data-testid="stSidebar"] * {
        color: #2b2b2b !important;
    }
    /* Force sidebar inputs to light background */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] [data-baseweb] {
        background-color: #fff1f1 !important;
        color: #2b2b2b !important;
        border-color: #ffb3b3 !important;
    }
    /* Ensure links are readable */
    a, a:visited { color: #c62828; }
    a:hover { color: #b71c1c; }
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #D7263D, #FF4E50, #FF6A88);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #2C3E50;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6A88 0%, #FF4E50 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.18);
    }
    
    .status-message {
        background: linear-gradient(135deg, #FF7E79 0%, #D7263D 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: pulse 2s infinite;
        text-align: center;
        font-weight: 600;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .answer-container {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFE3E3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        animation: slideIn 0.5s ease-out;
    }
    .answer-container, .answer-container * {
        color: #2b2b2b !important;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sources-container {
        background: linear-gradient(135deg, #FFD1D1 0%, #FF9E9E 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input {
        background-color: #fffafa;
        color: #2b2b2b;
    }
    .stTextInput > div > div > input::placeholder {
        color: #a35a5a;
        opacity: 0.8;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF6A88;
        box-shadow: 0 0 10px rgba(255, 106, 136, 0.25);
    }
    .stTextArea textarea {
        background-color: #fffafa !important;
        color: #2b2b2b !important;
        border-color: #ffb3b3 !important;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #D7263D;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🤖 Finance: News Research Tool 📈</h1>', unsafe_allow_html=True)
st.markdown('<div class="sidebar-title">📰 News Article URLs</div>', unsafe_allow_html=True)

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}", placeholder=f"Enter news article URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("🚀 Process URLs")
index_dir = "faiss_store_gemini"

main_placeholder = st.empty()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.9,
    max_output_tokens=500,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

if process_url_clicked:
    try:
        # load data
        loader = UnstructuredURLLoader(urls=urls)
        with main_placeholder.container():
            st.markdown('<div class="status-message"><div class="loading-spinner"></div>Data Loading...Started...✅✅✅</div>', unsafe_allow_html=True)
        data = loader.load()
        
        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        with main_placeholder.container():
            st.markdown('<div class="status-message"><div class="loading-spinner"></div>Text Splitter...Started...✅✅✅</div>', unsafe_allow_html=True)
        docs = text_splitter.split_documents(data)
        
        # create embeddings and save it to FAISS index
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        vectorstore_gemini = FAISS.from_documents(docs, embeddings)
        with main_placeholder.container():
            st.markdown('<div class="status-message"><div class="loading-spinner"></div>Embedding Vector Started Building...✅✅✅</div>', unsafe_allow_html=True)
        time.sleep(2)

        # Save the FAISS index using FAISS's native persistence
        vectorstore_gemini.save_local(index_dir)
        
        with main_placeholder.container():
            st.markdown('<div class="status-message">🎉 Processing Complete! Ready for questions!</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        st.error("Please check your URLs and try again.")

query = st.text_input("💭 Ask your question:", placeholder="What would you like to know about the articles?")

if query:
    if os.path.isdir(index_dir):
        try:
            # Recreate embeddings and load the FAISS index from disk
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                
                # Show loading animation
            with st.spinner('🔍 Searching for answers...'):
                result = chain.invoke({"question": query})
                
                # result will be a dictionary of this format --> {"answer": "", "sources": [] }
                st.markdown('<div class="answer-container">', unsafe_allow_html=True)
                st.markdown("### 💡 Answer")
                st.write(result["answer"])
                st.markdown('</div>', unsafe_allow_html=True)

                # Display sources, if available
                sources = result.get("sources", "")
                if sources:
                    st.markdown('<div class="sources-container">', unsafe_allow_html=True)
                    st.markdown("### 📚 Sources:")
                    sources_list = sources.split("\n")  # Split the sources by newline
                    for source in sources_list:
                        if source.strip():  # Only display non-empty sources
                            st.markdown(f"🔗 {source}")
                    st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
            st.error("Please try again or check if the processed data is still valid.")
    else:
        st.warning("⚠️ Please process some URLs first before asking questions!")

# Add footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-style: italic; margin-top: 2rem;">
        Powered by Google Gemini AI 🚀 | Built with ❤️ using Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)

