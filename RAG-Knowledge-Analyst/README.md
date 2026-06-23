# 📄 Knowledge Analyst - RAG System

A sophisticated **Retrieval-Augmented Generation (RAG)** system for intelligent PDF document analysis and Q&A. Built with LangChain, FAISS, and Streamlit.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🚀 Features

- **📚 Multi-PDF Upload**: Process multiple PDF documents simultaneously
- **❓ Intelligent Q&A**: Ask questions and get accurate answers from your documents
- **🔍 Source Attribution**: View the exact sources and page numbers for answers
- **📊 Analytics Dashboard**: Extract risks, dates, and stakeholders automatically
- **⚡ Fast Processing**: Efficient document chunking and embedding with FAISS
- **🎨 Beautiful UI**: Modern, intuitive Streamlit interface with custom styling
- **🔐 Hallucination Control**: Strict prompting to prevent AI hallucinations
- **📋 Document Statistics**: View comprehensive document analytics

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit (UI) |
| **LLM** | Groq - Llama 3.1 70B |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS |
| **Document Processing** | LangChain |
| **PDF Loading** | PyPDF |

---

## 📋 Prerequisites

- Python 3.9 or higher
- pip or conda
- A Groq API key (free at https://console.groq.com)

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
cd RAG-Knowledge-Analyst
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Or set environment variable:
```bash
# Windows (PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"

# Windows (CMD)
set GROQ_API_KEY=your_groq_api_key_here

# macOS/Linux
export GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Get Groq API Key
1. Visit https://console.groq.com
2. Sign up for a free account
3. Generate an API key
4. Copy the key to your `.env` file

---

## 🎯 Usage

### Start the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

### Step-by-Step Guide

1. **📤 Upload Documents**
   - Go to the "Upload & Process" tab
   - Click the upload button in the sidebar
   - Select one or multiple PDF files
   - Click "🚀 Process Documents"

2. **❓ Ask Questions**
   - Navigate to the "Ask Questions" tab
   - Enter your question in the text area
   - Click "🔍 Ask Question"
   - View the answer and sources

3. **📊 View Insights**
   - Check the "Insights" tab
   - See extracted risks, dates, and stakeholders
   - Expand each item for details

4. **📋 Document Info**
   - View document statistics
   - Browse document chunks
   - Check content preview

---

## 📁 Project Structure

```
RAG-Knowledge-Analyst/
│
├── app.py                      # Main Streamlit application
├── rag_pipeline.py             # RAG pipeline components
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
├── README.md                   # This file
│
├── data/                       # Uploaded PDF files (created automatically)
└── vectorstore/                # FAISS vector store (created automatically)
```

---

## 🔧 Configuration

### Advanced Settings

Edit these values in the code to customize behavior:

**In `rag_pipeline.py`:**
```python
# Chunk size for document splitting
chunk_size = 1000
chunk_overlap = 200

# Number of documents to retrieve
search_kwargs={"k": 4}

# Temperature for LLM responses
temperature = 0.3
```

**In `app.py`:**
```python
# Processing detail levels can be adjusted
# Change extraction keywords in utils.py for better results
```

---

## 📝 Examples

### Example Queries

1. **"What are the main risks mentioned in these documents?"**
2. **"List all important dates in the contracts."**
3. **"Who are the key parties involved?"**
4. **"What are the payment terms?"**
5. **"Summarize the key obligations."**

---

## 🐛 Troubleshooting

### Error: `NameError: name 'os' is not defined`
- ✅ **Fixed** - `os` module is now properly imported

### Error: `GROQ_API_KEY not found`
```bash
# Set your API key in .env file:
GROQ_API_KEY=your_key_here
```

### Error: `ModuleNotFoundError: No module named 'streamlit'`
```bash
pip install -r requirements.txt
```

### Slow Processing
- Reduce chunk size in `rag_pipeline.py`
- Use fewer documents initially
- Check internet connection for API calls

### Out of Memory
- Process fewer documents at once
- Reduce chunk size
- Use CPU instead of GPU

---

## 🎨 UI Customization

### Change Color Scheme
Edit the CSS in `app.py` (lines 25-50):
```python
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    # Change gradient colors here
}
```

### Add More Tabs
```python
tab5, tab6 = st.tabs(["New Tab 1", "New Tab 2"])
```

---

## 📊 Performance Tips

1. **Optimize Chunk Size**: Balance between 500-2000 characters
2. **Limit Chunks to Retrieve**: k=3 or k=4 works best
3. **Use Fast Embeddings**: all-MiniLM-L6-v2 is already optimized
4. **Batch Processing**: Process documents in batches if too many

---

## 🔐 Security

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` added to `.gitignore`
- ✅ No user data sent to external services (except Groq LLM)
- ✅ Local vector store (FAISS)

---

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Document export features
- [ ] Advanced analytics dashboard
- [ ] Custom embedding models
- [ ] Integration with more LLM providers
- [ ] Caching for faster responses
- [ ] User authentication
- [ ] Multi-user support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check Groq documentation: https://console.groq.com/docs
4. Check LangChain documentation: https://python.langchain.com

---

## 🙌 Acknowledgments

- **Groq** - Fast LLM inference
- **LangChain** - RAG framework
- **FAISS** - Vector similarity search
- **Streamlit** - Web UI framework
- **HuggingFace** - Embeddings

---

**Created for efficient document analysis and Q&A | Version 1.0**
```bash
streamlit run app.py
```

---

## 📊 How It Works

1. Upload PDF
2. Text is split into chunks
3. Chunks converted into embeddings
4. Stored in FAISS vector database
5. User query retrieves relevant chunks
6. LLM generates answer using retrieved context

---

## 🎯 Example Queries
- What are the risks in this contract?
- Who are the stakeholders?
- What is the termination clause?

---

## 🔥 Future Improvements
- Add chat memory
- Highlight answers in PDF
- Use GPT-4 / Gemini
- Deploy on cloud

---

## 👨‍💻 Author
Muhammad Ali