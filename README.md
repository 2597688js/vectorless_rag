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

## Using URLs (Complete Guide)

### What are URLs?

You can process PDFs directly from web links without downloading them manually. Just pass the URL as the first argument.

### How to Use a URL

**Basic syntax:**
```bash
python3 local_pageindex.py <URL> --query "<your question>"
```

**Example 1: Academic paper**
```bash
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is this paper about?"
```

**Example 2: Research document**
```bash
python3 local_pageindex.py https://example.com/research-paper.pdf --query "What are the findings?"
```

**Example 3: Public PDF**
```bash
python3 local_pageindex.py https://example.org/document.pdf --query "What are the key points?"
```

### Supported URLs

✅ Works with any publicly accessible PDF URL:
- arXiv papers: `https://arxiv.org/pdf/...`
- ResearchGate: `https://researchgate.net/...`
- GitHub: `https://github.com/.../releases/download/...`
- Direct PDF links: `https://example.com/file.pdf`
- Any other public PDF URL

### How It Works

1. **Detects URL** - Checks if input starts with `http://` or `https://`
2. **Downloads PDF** - Automatically downloads to `/tmp/`
3. **Processes Locally** - All processing happens on your machine
4. **No Cloud Calls** - Complete privacy and offline capability

### Step-by-Step Example

```bash
# 1. Start Ollama (if not already running)
ollama serve

# 2. In new terminal - Process PDF from URL
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762

# 3. Query the document
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is the architecture?"
```

### URL Processing Flow

```
Your URL
   ↓
System detects it's a URL
   ↓
Automatically downloads to /tmp/
   ↓
Processes locally (no cloud calls)
   ↓
Creates indexed tree
   ↓
Query with Ollama
   ↓
Get Answer
```

### Examples by Document Type

**Academic Paper:**
```bash
python3 local_pageindex.py https://arxiv.org/pdf/1706.03762 --query "What is the main contribution?"
```

**Technical Manual:**
```bash
python3 local_pageindex.py https://example.com/manual.pdf --query "How do I install this?"
```

**Research Report:**
```bash
python3 local_pageindex.py https://example.org/report.pdf --query "What are the results?"
```

**Whitepaper:**
```bash
python3 local_pageindex.py https://example.io/whitepaper.pdf --query "What problem does this solve?"
```

### Notes

- URLs must be publicly accessible (no authentication required)
- PDF file must be downloadable (not restricted)
- Large PDFs may take time to download and process
- All processing stays local and private
- No API keys needed for URL processing

---

## Features

- ✅ No API keys required
- ✅ 100% local processing
- ✅ Completely offline
- ✅ Free and private
