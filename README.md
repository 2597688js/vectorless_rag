# Vectorless RAG with Local PageIndex & Ollama

**A complete local, API-key-free document intelligence system using PageIndex and Ollama.**

---

## Quick Overview

PageIndex is a reasoning-based, vectorless RAG framework that:
- ✅ Generates hierarchical tree structures from PDFs
- ✅ Uses LLM reasoning for intelligent retrieval (no vectors needed)
- ✅ Runs 100% locally with Ollama (no cloud APIs)
- ✅ Requires **ZERO API keys**
- ✅ Works offline after setup

### Why This Approach?

| Traditional RAG | Vectorless RAG (This) |
|---|---|
| Vector embeddings | Structured trees |
| Document chunking | Natural sections |
| Approximate search | LLM reasoning |
| Multiple API calls | Single local LLM |
| High costs | Free |

---

## What Changed: Complete API Key Bypass

### Before
```
PDF → PageIndexClient (cloud) → OpenAI API → Needs: PAGEINDEX_API_KEY, OPENAI_API_KEY
```

### After
```
PDF → page_index_main() (local) → Ollama (local) → Needs: Nothing! ✅
```

### Changes Made
1. **Code**: Replaced `PageIndexClient` with `page_index_main()`
2. **Config**: Changed models from `gpt-4o` to `ollama/qwen2.5:1.5b`
3. **Features**: Full text indexing enabled for better answers

---

## Setup (5 minutes)

### 1. Install Ollama

**macOS:**
- Download from [ollama.ai](https://ollama.ai)
- Or: `brew install ollama`

### 2. Start Ollama

```bash
ollama serve
# You should see: "Listening on 127.0.0.1:11434"
```

### 3. Pull the Model (in new terminal)

```bash
ollama pull qwen2.5:1.5b
```

### 4. Install Dependencies

```bash
cd /path/to/vectorless_rag
pip install -r requirements.txt
```

### 5. Verify Setup

```bash
curl -s http://localhost:11434/api/tags | grep qwen2.5
# Should show: qwen2.5:1.5b
```

---

## How to Use

### Index a PDF

```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf
```

Output:
```
✓ Ollama is running with 1 model(s)
✨ Using Local PageIndex - NO API KEYS REQUIRED!
📄 Processing PDF locally with PageIndex: Resume.pdf
⏳ Generating tree structure...
✓ Tree generation complete!
💾 Tree saved to: indexed_documents/Resume_tree.json
```

### Query a Document

```bash
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What skills?"
```

Output:
```
🔍 Searching tree with Ollama reasoning...
💭 Reasoning Process: [LLM analysis]
📍 Retrieved N relevant nodes: [Found sections]
📝 Generating answer with Ollama...
✨ Answer: [Detailed answer]
```

### Example Queries

```bash
python3 local_pageindex.py doc.pdf --query "What is the education background?"
python3 local_pageindex.py doc.pdf --query "List all projects"
python3 local_pageindex.py doc.pdf --query "What are technical skills?"
python3 local_pageindex.py doc.pdf --query "Total years of experience?"
```

---

## Configuration

### Main Config: `pageindex/config.yaml`

```yaml
# LLM Models
model: "ollama/qwen2.5:1.5b"           # Local Ollama (was: gpt-4o)
retrieve_model: "ollama/qwen2.5:1.5b"  # Local Ollama (was: gpt-5.4)

# Tree Generation
toc_check_page_num: 20                 # Pages to scan for TOC
max_page_num_each_node: 10             # Max pages per node
max_token_num_each_node: 20000         # Max tokens per node

# Output
if_add_node_text: "yes"                # Include full text (important!)
if_add_node_summary: "yes"             # Include AI summaries
if_add_node_id: "yes"                  # Include node IDs
if_add_doc_description: "no"           # Skip doc description
```

### Environment: `.env`

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
```

### Alternative Models

```bash
# Faster (smaller)
ollama pull qwen:0.5b

# More capable (slower)
ollama pull mistral:7b
ollama pull neural-chat:7b
```

Then update `pageindex/config.yaml`:
```yaml
model: "mistral:7b"
retrieve_model: "mistral:7b"
```

---

## Troubleshooting

### Ollama Not Running
```
✗ Cannot connect to Ollama at http://localhost:11434
```
**Solution:** Start Ollama in terminal: `ollama serve`

### No Models Found
```
✗ Ollama is running but no models found
```
**Solution:** Pull a model: `ollama pull qwen2.5:1.5b`

### JSON Parse Error
```
⚠️  Could not parse Ollama response as JSON
```
**Solution:** Restart Ollama or use smaller model (qwen:0.5b)

### Slow Processing
**Solution:** 
- Use smaller model: `ollama pull qwen:0.5b`
- Reduce token limit in config.yaml
- Close other applications

---

## FAQ

**Q: Do I really need zero API keys?**
A: Yes! Ollama is local, PageIndex library is local. No cloud calls.

**Q: Can I use a different Ollama model?**
A: Yes. Pull it (`ollama pull model-name`) and update config.yaml.

**Q: How much disk space needed?**
A: ~3-4GB total (Ollama model + code + indexed documents).

**Q: Can this work completely offline?**
A: Yes! After initial setup, everything runs locally. No internet needed.

**Q: How accurate are answers?**
A: Depends on your query clarity and Ollama model. Use specific, detailed queries.

**Q: Can I process multiple PDFs?**
A: Yes! Each creates its own `indexed_documents/<filename>_tree.json`.

**Q: Is my data private?**
A: Completely! Documents never leave your machine. No uploads, no tracking.

**Q: Can I use this in production?**
A: Yes! Test with your documents first and choose appropriate model.

---

## Architecture

### System Flow
```
PDF File
   ↓
Local PageIndex (page_index_main)
   ↓
Local Ollama (LLM reasoning)
   ↓
Tree JSON
   ↓
User Query
   ↓
Ollama Reasoning
   ↓
Answer
```

### Key Features
- **No Cloud Calls**: Everything stays on your machine
- **No API Keys**: No authentication needed
- **Transparent**: See the reasoning process
- **Fast**: No network latency
- **Private**: Your data stays private

---

## File Structure

```
.
├── local_pageindex.py           # Main script
├── pageindex/                   # Local PageIndex library
│   ├── config.yaml              # Configuration file
│   ├── page_index.py            # Core logic
│   └── utils.py                 # Utilities
├── indexed_documents/           # Output tree JSONs
├── README.md                    # This file
└── requirements.txt             # Dependencies
```

---

## Quick Start (Copy-Paste)

```bash
# 1. Install Ollama from https://ollama.ai

# 2. Start Ollama (keep running)
ollama serve

# 3. In new terminal:
ollama pull qwen2.5:1.5b

# 4. Install dependencies
pip install -r requirements.txt

# 5. Index a PDF
python3 local_pageindex.py ~/Desktop/Resume.pdf

# 6. Ask questions
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What skills?"
```

---

## Summary

| Aspect | Status |
|--------|--------|
| API Keys Required | ✅ ZERO |
| Cloud Dependency | ✅ NONE |
| Local Processing | ✅ 100% |
| Offline Capable | ✅ YES |
| Privacy | ✅ COMPLETE |
| Cost | ✅ FREE |
| Setup Time | ✅ 5 min |
| Difficulty | ✅ EASY |

---

**Everything is local. Everything is free. Everything works offline.** 🚀

For detailed setup help, check the Ollama installation at [ollama.ai](https://ollama.ai).
