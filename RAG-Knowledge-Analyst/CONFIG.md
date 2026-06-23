# 🔧 Configuration Guide

## Environment Setup

### 1. Create .env File

**Option A: Automatic (Recommended)**
- Use `setup.bat` (Windows) or `setup.sh` (macOS/Linux)
- It automatically creates `.env` from `.env.example`

**Option B: Manual**
1. Copy `.env.example` to `.env`
2. Add your Groq API key

### 2. Get Groq API Key

1. Go to https://console.groq.com
2. Sign up (free account)
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key
6. Add to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   ```

---

## Application Configuration

### RAG Pipeline Settings (`rag_pipeline.py`)

```python
# Document Splitting
chunk_size=1000          # Size of each chunk (words)
chunk_overlap=200        # Overlap between chunks (words)

# LLM Settings
temperature=0.3          # Lower = more consistent, Higher = more creative
max_tokens=1024         # Maximum response length

# Retrieval Settings
search_kwargs={"k": 4}   # Number of documents to retrieve
```

### Streamlit Configuration

Edit `.streamlit/config.toml` if you need custom settings:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = true
```

---

## Performance Tuning

### For Large Documents (100+ pages)

```python
chunk_size = 1500        # Larger chunks
chunk_overlap = 100      # Less overlap
search_kwargs = {"k": 3} # Fewer documents
```

### For Speed (Quick Processing)

```python
chunk_size = 500         # Smaller chunks
temperature = 0.5        # Faster processing
```

### For Accuracy (Detailed Analysis)

```python
chunk_size = 1000        # Balanced size
temperature = 0.3        # More consistent
search_kwargs = {"k": 5} # More context
```

---

## Deployment

### Local Development

```bash
streamlit run app.py
```

### Production Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add environment variables in settings
5. Deploy!

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:

```bash
docker build -t rag-analyst .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key rag-analyst
```

---

## Memory & Storage

### Minimum Requirements
- RAM: 2GB
- Storage: 500MB (+ space for PDFs)
- Internet: Required for Groq API

### Recommended
- RAM: 8GB+
- Storage: 5GB+
- Internet: Broadband

---

## Security Best Practices

1. **Never commit `.env` file**
   - Already in `.gitignore`

2. **Rotate API Keys Regularly**
   - Generate new key in Groq console
   - Update `.env`

3. **Run in Isolated Environment**
   - Use virtual environment
   - Don't use system Python

4. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## Logging & Debugging

### Enable Verbose Logging

In `rag_pipeline.py`:
```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    verbose=True  # Enable debug output
)
```

### Check Streamlit Logs

```bash
streamlit run app.py --logger.level=debug
```

### View Model Configuration

```python
# Add to app.py
if st.checkbox("Show Config"):
    st.json(st.session_state)
```

---

## Troubleshooting Configuration

### Issue: Module Import Errors
**Solution:**
```bash
pip install --upgrade langchain langchain-groq streamlit
```

### Issue: Slow Processing
**Solution:**
- Reduce chunk_size
- Use fewer documents
- Check internet connection

### Issue: Low Quality Answers
**Solution:**
- Increase temperature to 0.5
- Increase k to 5
- Check PDF quality

---

## Advanced Features

### Custom Embeddings

Replace in `rag_pipeline.py`:
```python
# Default
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Alternative
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
```

### Different LLM Models

In `rag_pipeline.py`:
```python
# Groq available models
model_name="llama-3.1-70b-versatile"     # Default
model_name="llama-3.1-8b-instant"        # Fast
model_name="mixtral-8x7b-32768"          # Powerful
```

### Custom Prompts

Edit the prompt template in `create_qa_chain()` function.

---

## Support & Resources

- **Groq Docs**: https://console.groq.com/docs
- **LangChain**: https://python.langchain.com
- **Streamlit**: https://docs.streamlit.io
- **FAISS**: https://ai.meta.com/tools/faiss/

---

**Configuration Tips:**
- Start with default settings
- Adjust based on your needs
- Test with small documents first
- Monitor performance and costs
