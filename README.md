# Vectorless RAG with Local PageIndex & Ollama

Local, API-key-free document intelligence system using PageIndex and Ollama.

---

## Clone PageIndex Repository

```bash
cd /path/to/vectorless_rag

# Clone pageindex repo
git clone git@github.com:VectifyAI/PageIndex.git

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

### Step 5: Index a PDF (Local or URL)

**Local PDF:**
```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf
```

**From URL:**
```bash
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762
```

### Step 6: Query the Document

```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What are the skills?"
```

**Or query from URL:**
```bash
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is this paper about?"
```

---

**Example 1: Academic paper**
```bash
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is this paper about?"
```

**Example 2: Research document**
```bash
python3 local_pageindex.py https://example.com/research-paper.pdf --query "What are the findings?"
```

### Step-by-Step Example

```bash
# 1. Start Ollama (if not already running)
ollama serve

# 2. In new terminal - Process PDF from URL
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762

# 3. Query the document
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is the architecture?"
```
---

## Features

- ✅ No API keys required
- ✅ 100% local processing
- ✅ Completely offline
- ✅ Free and private
