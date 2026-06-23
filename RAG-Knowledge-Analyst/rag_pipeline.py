import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ---------------- LOAD PDF ----------------
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    return loader.load()

# ---------------- SPLIT TEXT ----------------
def split_text(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(pages)

# ---------------- VECTOR STORE ----------------
def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(docs, embeddings)

# ---------------- QA CHAIN (GROQ VERSION) ----------------
def create_qa_chain(vectorstore):
    # Get API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Please set GROQ_API_KEY environment variable")

    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.1,  # Low temperature for factual answers
        max_tokens=1024
    )

    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Enhanced prompt for legal documents
    prompt_template = """
You are an expert legal document analyst. Your task is to answer questions about legal documents with precision and accuracy.

CRITICAL RULES:
1. ONLY use information from the provided context
2. If information is not found in the context, say "This information is not found in the provided documents"
3. ALWAYS cite the specific page number or section where you found the information
4. Be precise and quote relevant clauses when possible
5. For legal terms, explain them briefly if context suggests they need clarification
6. Never make assumptions or add external knowledge

Context from document:
{context}

Question: {question}

Answer with citations:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Create QA chain using the newer Runnable interface
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain