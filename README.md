# Vectorless RAG with Local PageIndex & Ollama

Local, API-key-free document intelligence system using PageIndex and Ollama.

---

## Clone PageIndex Repository

```bash
cd /path/to/vectorless_rag

# Clone using SSH
git clone git@github.com:VectifyAI/PageIndex.git

# OR clone using HTTPS
git clone https://github.com/VectifyAI/PageIndex.git
```

---

## Run the Code

### Step 1: Install Ollama

**macOS:**
- Download from [ollama.ai](https://ollama.ai)
- Or: `brew install ollama`

### Step 2: Start Ollama

```bash
ollama serve
```

### Step 3: Pull the Model (new terminal)

```bash
ollama pull qwen2.5:1.5b
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Index a PDF

```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf
```

### Step 6: Query the Document

```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What are the skills?"
```

---

## Features

- ✅ No API keys required
- ✅ 100% local processing
- ✅ Completely offline
- ✅ Free and private
