import os
import streamlit as st
from rag_pipeline import (
    load_pdf,
    split_text,
    create_vectorstore,
    create_qa_chain
)
from utils import extract_insights

# Configure page
st.set_page_config(
    page_title="📚 Knowledge Analyst - RAG System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
    .info-msg {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #bee5eb;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📚 Knowledge Analyst - RAG System</div>', unsafe_allow_html=True)
st.markdown("### Intelligent Document Analysis & Q&A for Legal Contracts")

# Initialize session state
if "qa" not in st.session_state:
    st.session_state.qa = None
if "docs" not in st.session_state:
    st.session_state.docs = None

# Create directories
os.makedirs("data", exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Upload and analyze your legal documents")

    # API Key input
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get your API key from https://console.groq.com"
    )

    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        st.success("✅ API Key set!")

    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("• 📄 Multi-PDF processing")
    st.markdown("• ❓ Q&A with citations")
    st.markdown("• 📊 Risk analysis")
    st.markdown("• 🔍 Source attribution")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "❓ Ask Questions", "📊 Insights Dashboard"])

# Tab 1: Upload and Process
with tab1:
    st.header("📤 Document Upload & Processing")

    uploaded_files = st.file_uploader(
        "Upload PDF Contracts",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or multiple PDF files to analyze"
    )

    if uploaded_files:
        st.markdown(f'<div class="info-msg">📄 {len(uploaded_files)} file(s) selected for processing</div>', unsafe_allow_html=True)

        # Show file details
        with st.expander("📋 File Details"):
            for file in uploaded_files:
                st.write(f"• {file.name} ({file.size / 1024:.1f} KB)")

        if st.button("🚀 Process Documents", use_container_width=True):
            if not api_key:
                st.markdown('<div class="error-msg">❌ Please enter your Groq API Key in the sidebar first!</div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("🔄 Processing documents..."):
                        progress_bar = st.progress(0)

                        # Save files
                        st.text("💾 Saving files...")
                        progress_bar.progress(10)

                        all_pages = []
                        for i, file in enumerate(uploaded_files):
                            path = os.path.join("data", file.name)
                            with open(path, "wb") as f:
                                f.write(file.read())

                            st.text(f"📖 Loading: {file.name}")
                            pages = load_pdf(path)
                            all_pages.extend(pages)
                            progress_bar.progress(20 + (i * 20) // len(uploaded_files))

                        # Split text
                        st.text("✂️ Splitting documents...")
                        docs = split_text(all_pages)
                        progress_bar.progress(60)

                        # Create vectorstore
                        st.text("🔢 Creating embeddings...")
                        vectorstore = create_vectorstore(docs)
                        progress_bar.progress(80)

                        # Create QA chain
                        st.text("⚡ Initializing AI model...")
                        qa = create_qa_chain(vectorstore)
                        progress_bar.progress(100)

                        # Store in session
                        st.session_state.qa = qa
                        st.session_state.docs = docs

                        st.markdown('<div class="success-msg">✅ Documents processed successfully!</div>', unsafe_allow_html=True)
                        st.balloons()

                except Exception as e:
                    st.markdown(f'<div class="error-msg">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                    st.error("Please check your API key and try again.")
    else:
        st.info("👆 Upload PDF files to get started!")

# Tab 2: Ask Questions
with tab2:
    st.header("❓ Ask Questions About Your Documents")

    if st.session_state.qa is None:
        st.markdown('<div class="info-msg">📤 Please upload and process documents first in the Upload tab.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-msg">✅ AI model ready! Ask any question about your documents.</div>', unsafe_allow_html=True)

        query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What are the key risks mentioned in this contract?",
            height=100
        )

        if st.button("🔍 Ask Question", use_container_width=True) and query:
            try:
                with st.spinner("🤔 Analyzing documents..."):
                    result = st.session_state.qa.invoke(query)

                # Display answer
                st.subheader("📝 Answer")
                st.write(result)

                # Note: With the new chain, we don't have source documents directly
                # The sources are embedded in the context used by the chain
                st.info("📚 Answer generated based on document analysis with citations included in the response.")

            except Exception as e:
                st.markdown(f'<div class="error-msg">❌ Error generating answer: {str(e)}</div>', unsafe_allow_html=True)

# Tab 3: Insights Dashboard
with tab3:
    st.header("📊 Document Insights Dashboard")

    if st.session_state.docs is None:
        st.markdown('<div class="info-msg">📤 Upload and process documents to see insights.</div>', unsafe_allow_html=True)
    else:
        try:
            risks, dates, stakeholders = extract_insights(st.session_state.docs)

            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("⚠️ Risks Identified", len(risks))

            with col2:
                st.metric("📅 Key Dates Found", len(dates))

            with col3:
                st.metric("👥 Stakeholders", len(stakeholders))

            st.markdown("---")

            # Detailed insights
            if risks:
                st.subheader("⚠️ Identified Risks")
                for i, risk in enumerate(risks[:5]):
                    with st.expander(f"Risk {i+1}"):
                        st.write(risk[:500] + "..." if len(risk) > 500 else risk)

            if dates:
                st.subheader("📅 Important Dates")
                for i, date in enumerate(dates[:5]):
                    with st.expander(f"Date Reference {i+1}"):
                        st.write(date[:500] + "..." if len(date) > 500 else date)

            if stakeholders:
                st.subheader("👥 Parties & Stakeholders")
                for i, stakeholder in enumerate(stakeholders[:5]):
                    with st.expander(f"Stakeholder {i+1}"):
                        st.write(stakeholder[:500] + "..." if len(stakeholder) > 500 else stakeholder)

        except Exception as e:
            st.error(f"Error extracting insights: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
🚀 <b>Knowledge Analyst</b> • Powered by LangChain + FAISS + Groq<br>
Advanced RAG System for Legal Document Analysis
</div>
""", unsafe_allow_html=True)