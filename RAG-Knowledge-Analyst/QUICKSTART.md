# 🚀 Quick Start Guide

## 5-Minute Setup

### For Windows Users

1. **Download Project**
   ```bash
   cd RAG-Knowledge-Analyst
   ```

2. **Run Setup Script**
   - Double-click `setup.bat`
   - Wait for installation to complete

3. **Add API Key**
   - Open `.env` file
   - Replace `your_groq_api_key_here` with your actual Groq API key
   - Get key from: https://console.groq.com

4. **Start Application**
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**
   - Go to `http://localhost:8501`

---

### For macOS/Linux Users

1. **Download Project**
   ```bash
   cd RAG-Knowledge-Analyst
   ```

2. **Make Setup Script Executable**
   ```bash
   chmod +x setup.sh
   ```

3. **Run Setup Script**
   ```bash
   ./setup.sh
   ```

4. **Add API Key**
   - Open `.env` file
   - Replace `your_groq_api_key_here` with your actual Groq API key
   - Get key from: https://console.groq.com

5. **Start Application**
   ```bash
   streamlit run app.py
   ```

6. **Open Browser**
   - Go to `http://localhost:8501`

---

## Getting Your Groq API Key (2 Minutes)

1. Visit: https://console.groq.com
2. Click "Sign Up"
3. Complete registration (free)
4. Go to "API Keys" section
5. Click "Create API Key"
6. Copy the key
7. Paste into `.env` file

---

## First Time Using the App

### Step 1: Upload PDFs
- Click "Upload & Process" tab
- Click the upload button
- Select your PDF files
- Click "Process Documents"
- Wait for processing (2-5 minutes for large files)

### Step 2: Ask Questions
- Click "Ask Questions" tab
- Enter your question
- Click "Ask Question"
- Review the answer and sources

### Step 3: Explore Insights
- Click "Insights" tab
- View automatically extracted risks, dates, and stakeholders

### Step 4: View Document Info
- Click "Document Info" tab
- Check statistics and preview chunks

---

## Troubleshooting

### Setup Script Doesn't Run (Windows)
```bash
# Run manually in CMD or PowerShell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### GROQ_API_KEY Error
- Make sure `.env` file exists in project root
- Add your API key to `.env`
- Restart Streamlit app

### Port Already in Use
```bash
# Run on different port
streamlit run app.py --server.port=8502
```

---

## Common Tasks

### Process More Documents
- Sidebar → Upload PDFs → Click "Process Documents"
- You can upload 1 or 100 PDFs at once

### Clear Session
- Use the "Clear" button in Ask Questions tab
- Or refresh browser page

### Change Processing Speed
- Select "Fast", "Balanced", or "Thorough"
- Affects detail level of analysis

### View Raw Document Content
- Click "Document Info" tab
- Select chunk number
- View full content in preview

---

## Tips for Best Results

1. **PDF Quality**: Use clear, machine-readable PDFs (not scanned images)
2. **Document Length**: Works best with 5-100 page documents
3. **Question Specificity**: Ask specific questions for better answers
4. **Multiple Documents**: Upload related documents for comprehensive analysis

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [Requirements.txt](requirements.txt) for dependencies
- Review code comments in `app.py`, `rag_pipeline.py`, `utils.py`

---

## Need Help?

1. Check README.md "Troubleshooting" section
2. Review Groq documentation: https://console.groq.com/docs
3. Check LangChain docs: https://python.langchain.com

**You're all set! Happy analyzing! 🚀**
