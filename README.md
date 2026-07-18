# Vectorless RAG with Local PageIndex & Ollama

## Table of Contents
1. [Overview](#overview)
2. [What Changed - Complete API Key Bypass](#what-changed---complete-api-key-bypass)
3. [Complete Setup Guide](#complete-setup-guide)
4. [Step-by-Step Instructions to Run Offline](#step-by-step-instructions-to-run-offline)
5. [How to Use](#how-to-use)
6. [Configuration Details](#configuration-details)
7. [Architecture](#architecture)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Overview

**PageIndex** is a reasoning-based, **vectorless RAG** framework that performs retrieval in two steps:
1. Generate a tree structure index of documents
2. Perform reasoning-based retrieval through tree search

### Why Vectorless RAG?

Traditional vector-based RAG uses:
- ❌ Vector embeddings (approximate similarity search)
- ❌ Document chunking (artificial fragmentation)
- ❌ Multiple external API calls
- ❌ High latency and costs

**This implementation** uses:
- ✅ **Structured tree indexing** - Preserves document hierarchy
- ✅ **LLM-based reasoning** - Intelligent section selection
- ✅ **Local processing** - Zero external APIs
- ✅ **Transparent retrieval** - See the reasoning process

### PageIndex Features

- **No Vectors Needed**: Uses document structure and LLM reasoning for retrieval
- **No Chunking Needed**: Documents organized into natural sections
- **Human-like Retrieval**: Simulates how experts navigate documents
- **Transparent Process**: Reasoning-based, not "vibe" retrieval
- **Scalable**: Supports multi-document and multi-node reasoning

---

## What Changed - Complete API Key Bypass

### Before (Original Implementation)

```
PDF File
   ↓
PageIndexClient (requires PAGEINDEX_API_KEY)
   ↓
PageIndex Cloud Service
   ↓
OpenAI API (requires OPENAI_API_KEY) - GPT-4o
   ↓
Tree JSON
   ↓
Ollama (local) - Query reasoning
   ↓
Answer
```

**Problems:**
- ❌ Requires PAGEINDEX_API_KEY
- ❌ Requires OPENAI_API_KEY  
- ❌ Cloud dependency
- ❌ API costs ($$$)
- ❌ Privacy concerns
- ❌ Internet required for indexing

### After (This Implementation)

```
PDF File
   ↓
page_index_main() (local library)
   ↓
Ollama (local) - All LLM operations
   ↓
Tree JSON
   ↓
Ollama (local) - Query reasoning
   ↓
Answer
```

**Benefits:**
- ✅ Zero API keys required
- ✅ 100% local processing
- ✅ Offline capable
- ✅ Free (no API costs)
- ✅ Complete privacy
- ✅ Fast (no latency)

### Specific Changes Made

#### 1. **Code Changes** (`local_pageindex.py`)

**Before:**
```python
from pageindex import PageIndexClient

pi_api_key = os.getenv("PAGEINDEX_API_KEY")  # Required!
if not pi_api_key:
    print("✗ PAGEINDEX_API_KEY not found")
    sys.exit(1)

pi_client = PageIndexClient(api_key=pi_api_key)
tree, doc_id = submit_and_index_pdf(pdf_path, pi_client)  # Cloud call
```

**After:**
```python
from pageindex import page_index_main
from pageindex.utils import ConfigLoader

# No API key needed!
config_loader = ConfigLoader()
tree = page_index_main(pdf_path, config)  # Local processing only
```

**Key Improvements:**
- Replaced cloud client with local library function
- Removed API key validation
- Added tree flattening for efficient retrieval
- Improved JSON parsing for Ollama responses
- Added full text content support for better answers

#### 2. **Configuration Changes** (`pageindex/config.yaml`)

**Before:**
```yaml
model: "gpt-4o-2024-11-20"        # OpenAI model - needs API key
retrieve_model: "gpt-5.4"          # OpenAI model - needs API key
if_add_node_text: "no"             # Only summaries
```

**After:**
```yaml
model: "ollama/qwen2.5:1.5b"       # Local Ollama model - no API key!
retrieve_model: "ollama/qwen2.5:1.5b"  # Local Ollama model
if_add_node_text: "yes"            # Include full text for better answers
```

**Impact:**
- All LLM operations now use local Ollama
- No external API calls during tree generation
- Full document context available for reasoning

#### 3. **Architecture Changes**

**Removed Dependencies:**
- ❌ `PageIndexClient` (cloud API client)
- ❌ OpenAI API integration
- ❌ Anthropic API integration
- ❌ Any external LLM service

**Added Components:**
- ✅ `page_index_main()` - Local PageIndex library
- ✅ `ConfigLoader()` - Load local configuration
- ✅ Tree flattening logic - Handle nested structures
- ✅ Robust JSON parsing - Handle Ollama responses

---

## Complete Setup Guide

### Step 1: Install Ollama (Required for Offline Operation)

Ollama is a **local LLM runtime** that lets you run LLMs on your machine without any API keys.

#### On macOS:

**Option A: Download & Install**
1. Visit [ollama.ai](https://ollama.ai)
2. Click "Download" 
3. Choose macOS version
4. Run the installer
5. Ollama will start automatically

**Option B: Homebrew**
```bash
brew install ollama
```

**Start Ollama:**
```bash
# Start Ollama service
ollama serve
```

You should see:
```
Listening on 127.0.0.1:11434
```

#### Verify Installation

```bash
curl http://localhost:11434/api/tags
```

Expected output:
```json
{
  "models": [
    {
      "name": "qwen2.5:1.5b"
    }
  ]
}
```

### Step 2: Pull the Required Model

The script uses `qwen2.5:1.5b` (a 1.5B parameter model optimized for speed).

```bash
# Pull the model (download ~1GB)
ollama pull qwen2.5:1.5b
```

This downloads the model to your machine. It's a one-time operation.

**Alternative Models** (optional):
```bash
# Faster (smaller)
ollama pull qwen:0.5b

# More capable (larger, slower)
ollama pull mistral:7b
ollama pull neural-chat:7b
```

### Step 3: Clone/Setup This Project

```bash
# Navigate to project directory
cd /path/to/vectorless_rag

# Check Python version (3.7+)
python3 --version

# Create virtual environment (optional but recommended)
python3 -m venv vectorless_venv
source vectorless_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

Create/update `.env` file in project root:

```bash
# .env file

# Optional - set Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b

# Note: PAGEINDEX_API_KEY and OpenAI keys are NO LONGER NEEDED!
# You can keep them for backward compatibility, but they won't be used.
```

**No API keys required!** 🎉

### Step 5: Verify Setup

```bash
# Check if Ollama is running
curl -s http://localhost:11434/api/tags | grep -q "qwen2.5" && echo "✓ Ollama setup OK" || echo "✗ Ollama not running"

# Check if Python dependencies are installed
python3 -c "import pageindex; print('✓ PageIndex OK')"
python3 -c "import ollama; print('✓ Ollama Python client OK')" 2>/dev/null || echo "Note: ollama Python client optional"
```

---

## Step-by-Step Instructions to Run Offline

### Before First Run

**1. Start Ollama** (keep this terminal open)
```bash
ollama serve
```

Output should show:
```
Listening on 127.0.0.1:11434
```

**2. Open New Terminal** for the script

### Running the Script (Simple Steps)

#### Step 1: Index a PDF Document

```bash
# Basic syntax
python3 local_pageindex.py <path_to_pdf>

# Real example
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf
```

**What happens:**
```
✓ Ollama is running with 1 model(s)
✨ Using Local PageIndex - NO API KEYS REQUIRED!
📄 Processing PDF locally with PageIndex: Resume_2026.pdf
⏳ Generating tree structure...
Parsing PDF...
[... processing ...]
✓ Tree generation complete!
💾 Tree saved to: indexed_documents/Resume_2026_tree.json
```

**Output:**
- Tree structure saved as JSON in `indexed_documents/` folder
- Ready for querying

#### Step 2: Query the Indexed Document

```bash
# Syntax with query
python3 local_pageindex.py <path_to_pdf> --query "<your question>"

# Real examples
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf --query "What is the total experience?"
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf --query "What are his programming skills?"
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf --query "List all projects"
```

**What happens:**
```
🔍 Searching tree with Ollama reasoning...
💭 Reasoning Process: [LLM analyzes the tree]
📍 Retrieved N relevant nodes: [Found sections]
📝 Generating answer with Ollama...
✨ Answer: [Detailed answer from document]
```

### Complete Workflow Example

```bash
# Terminal 1: Start Ollama
ollama serve
# Keep this running...

# Terminal 2: Run the script
cd /path/to/vectorless_rag

# Index the PDF
python3 local_pageindex.py ~/Desktop/Resume.pdf

# Query it
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What skills?"
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "Total experience?"
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "List projects"
```

---

## How to Use

### Basic Usage

#### 1. Index Multiple PDFs

```bash
# Index different documents
python3 local_pageindex.py ~/Desktop/Resume.pdf
python3 local_pageindex.py ~/Desktop/Report.pdf
python3 local_pageindex.py ~/Desktop/Manual.pdf

# Each creates indexed_documents/<filename>_tree.json
```

#### 2. Query Examples

**Get specific information:**
```bash
python3 local_pageindex.py ~/Documents/resume.pdf --query "education background"
python3 local_pageindex.py ~/Documents/resume.pdf --query "technical skills"
python3 local_pageindex.py ~/Documents/resume.pdf --query "work experience timeline"
```

**Summarize sections:**
```bash
python3 local_pageindex.py ~/Documents/report.pdf --query "executive summary"
python3 local_pageindex.py ~/Documents/report.pdf --query "key findings"
python3 local_pageindex.py ~/Documents/report.pdf --query "recommendations"
```

**Extract lists:**
```bash
python3 local_pageindex.py ~/Documents/manual.pdf --query "list all features"
python3 local_pageindex.py ~/Documents/manual.pdf --query "system requirements"
python3 local_pageindex.py ~/Documents/manual.pdf --query "installation steps"
```

#### 3. Working with Output

**Indexed tree file structure:**
```json
{
  "doc_name": "Resume.pdf",
  "structure": [
    {
      "title": "Experience",
      "node_id": "0003",
      "start_index": 1,
      "end_index": 1,
      "summary": "Professional experience summary...",
      "text": "Full experience section text...",
      "nodes": [
        {
          "title": "Company Name - Role",
          "node_id": "0004",
          "summary": "Role summary...",
          "text": "Full role details..."
        }
      ]
    }
  ]
}
```

**Use the JSON tree for:**
- Building custom retrieval pipelines
- Integration with other tools
- Manual document analysis
- Batch processing

### Advanced Usage

#### Change the Ollama Model

Edit `pageindex/config.yaml`:
```yaml
model: "mistral:7b"           # More capable, slower
retrieve_model: "mistral:7b"
```

Then re-run the script.

#### Customize Query Behavior

Edit `local_pageindex.py`:
```python
# Change tree search prompt (line ~111)
search_prompt = f"""Your custom prompt here..."""

# Change answer generation prompt (line ~142)
answer_prompt = f"""Your custom prompt here..."""
```

#### Process Multiple PDFs

```bash
# Create a script (process_pdfs.sh)
for file in ~/Documents/*.pdf; do
    python3 local_pageindex.py "$file"
    python3 local_pageindex.py "$file" --query "summary"
done
```

---

## Configuration Details

### Main Configuration File: `pageindex/config.yaml`

```yaml
# LLM Models
model: "ollama/qwen2.5:1.5b"           # Main model for tree generation
retrieve_model: "ollama/qwen2.5:1.5b"  # Model for retrieval reasoning

# Tree Generation Parameters
toc_check_page_num: 20                 # Pages to scan for table of contents
max_page_num_each_node: 10             # Max pages per node
max_token_num_each_node: 20000         # Max tokens per node

# Output Options
if_add_node_id: "yes"                  # Include node IDs
if_add_node_summary: "yes"             # Include AI summaries
if_add_doc_description: "no"           # Include doc description
if_add_node_text: "yes"                # Include full text (critical!)
```

### Environment Configuration: `.env`

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434    # Ollama server URL
OLLAMA_MODEL=qwen2.5:1.5b                 # Default model

# Note: PAGEINDEX_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY
# are NOT needed anymore. You can remove them or keep for other tools.
```

### Model Selection Guide

| Model | Size | Speed | Capability | Use Case |
|-------|------|-------|------------|----------|
| `qwen:0.5b` | 500MB | Very Fast | Basic | Quick summaries |
| `qwen2.5:1.5b` | 1.5GB | Fast | Good | **Recommended** |
| `mistral:7b` | 7GB | Moderate | Excellent | Complex queries |
| `neural-chat:7b` | 7GB | Moderate | Excellent | Long documents |

---

## Architecture

### Complete System Flow

```
┌─────────────────┐
│   PDF File      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 1: PDF Parsing & Tree Generation          │
│  ─────────────────────────────────────────────  │
│  • Extract text from PDF pages                  │
│  • Identify sections and hierarchy              │
│  • Use Ollama (local) to generate summaries     │
│  • Build tree structure                         │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Tree Structure (JSON)                          │
│  ─────────────────────────────────────────────  │
│  • Hierarchical nodes                           │
│  • Titles and summaries                         │
│  • Full text content                            │
│  • Page references                              │
└────────┬────────────────────────────────────────┘
         │
         ▼
   User Query
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 2: Query Processing                       │
│  ─────────────────────────────────────────────  │
│  • Extract node info from tree                  │
│  • Send to Ollama with query                    │
│  • LLM reasons over nodes                       │
│  • Returns relevant node IDs                    │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 3: Content Retrieval & Answer Generation  │
│  ─────────────────────────────────────────────  │
│  • Extract text from relevant nodes             │
│  • Send to Ollama with context                  │
│  • Generate comprehensive answer                │
│  • Return to user                               │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Final Answer   │
└─────────────────┘
```

### Data Flow - No Cloud Calls

```
Local Disk (PDF)
      ↓
  Python Code
      ↓
  Local Ollama ──→ LLM Processing ──→ Response
      ↓                                    ↓
  Local Disk (Tree JSON)             User Terminal
```

**Key Point:** Everything stays on your machine. Zero network calls to external services.

### Component Breakdown

| Component | Type | Location | Purpose |
|-----------|------|----------|---------|
| `local_pageindex.py` | Script | Project root | Main entry point |
| `pageindex/` | Library | Project | Local PageIndex library |
| `pageindex/config.yaml` | Config | pageindex/ | LLM & processing settings |
| Ollama | Service | Local (port 11434) | LLM inference |
| indexed_documents/ | Data | Project | Output tree JSONs |

---

## Troubleshooting

### Problem: "Ollama is not running"

**Error:**
```
✗ Cannot connect to Ollama at http://localhost:11434
```

**Solution:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Wait for: "Listening on 127.0.0.1:11434"
```

### Problem: "No models found in Ollama"

**Error:**
```
✗ Ollama is running but no models found
```

**Solution:**
```bash
# Pull the model
ollama pull qwen2.5:1.5b

# Verify
ollama list
```

### Problem: "PAGEINDEX_API_KEY not found"

**Error:**
```
✗ PAGEINDEX_API_KEY not found in .env
```

**Solution:**
This error shouldn't happen with the new version. Update your script:
```bash
git pull
python3 local_pageindex.py <pdf_path>
```

### Problem: "Could not parse Ollama response"

**Error:**
```
⚠️  Could not parse Ollama response as JSON
```

**Possible Causes:**
1. Ollama service restarted → Restart it
2. Out of memory → Close other apps
3. Model too slow → Increase timeout (edit config)

**Solution:**
```bash
# Restart Ollama
ollama serve

# Or use smaller model
# Edit pageindex/config.yaml:
model: "qwen:0.5b"
```

### Problem: Slow Processing

**Solution 1: Use Smaller Model**
```yaml
# pageindex/config.yaml
model: "qwen:0.5b"  # Faster but less capable
```

**Solution 2: Use Larger Model with GPU**
```bash
# If you have NVIDIA GPU (requires nvidia-cuda-toolkit)
ollama run mistral:7b  # Uses GPU automatically
```

**Solution 3: Reduce Document Size**
```bash
# Process smaller PDFs
# Or edit config to reduce max_token_num_each_node
```

---

## FAQ

### Q: Do I really need zero API keys?
**A:** Yes! The system runs completely locally:
- ✅ Ollama for all LLM operations (local)
- ✅ PageIndex library (local)
- ✅ No cloud calls
- ✅ No API keys

### Q: Can I use my own Ollama model?
**A:** Yes! Edit `pageindex/config.yaml`:
```yaml
model: "your-model-name:tag"
retrieve_model: "your-model-name:tag"
```

Then pull it:
```bash
ollama pull your-model-name:tag
```

### Q: How much disk space do I need?
**A:** 
- Ollama models: 500MB - 7GB (depending on model)
- Code: ~200MB
- Indexed documents: varies by document size

Total for basic setup: ~3-4GB

### Q: Can this work completely offline?
**A:** Yes! After initial setup:
1. ✅ Ollama models cached locally
2. ✅ All processing local
3. ✅ No internet needed

Just keep Ollama running.

### Q: How accurate are the answers?
**A:** Depends on:
- Quality of your query
- Ollama model capability
- Document clarity
- Tree structure quality

Use specific, detailed queries for best results.

### Q: Can I use this for production?
**A:** Yes! Considerations:
- Test with your documents first
- Choose appropriate Ollama model
- Monitor performance
- Adjust config as needed

### Q: How do I update to a better model?
**A:** 
```bash
# Pull new model
ollama pull mistral:7b

# Update config
# Edit pageindex/config.yaml:
model: "mistral:7b"

# Reindex documents
python3 local_pageindex.py your-file.pdf
```

### Q: Can I process multiple documents?
**A:** Yes! Each PDF is indexed separately:
```bash
python3 local_pageindex.py doc1.pdf
python3 local_pageindex.py doc2.pdf
python3 local_pageindex.py doc3.pdf

# Each creates its own JSON tree
```

### Q: What happens to my documents?
**A:** Completely private:
- Documents never leave your machine
- No cloud upload
- No data collection
- Only tree JSONs saved locally

---

## Summary

| Aspect | Status | Details |
|--------|--------|---------|
| **API Keys Required** | ✅ NONE | Completely free |
| **Ollama Required** | ✅ YES | Download & run locally |
| **Python 3.7+** | ✅ YES | Standard requirement |
| **Internet for Indexing** | ❌ NO | Completely offline |
| **Internet for Querying** | ❌ NO | Completely offline |
| **Cost** | ✅ FREE | No API charges |
| **Privacy** | ✅ 100% | Data stays local |
| **Speed** | ✅ FAST | No network latency |

---

## Getting Started Now

### Quick Start (5 minutes)

```bash
# 1. Install Ollama
# Visit https://ollama.ai and download

# 2. Start Ollama
ollama serve

# 3. In new terminal, pull model
ollama pull qwen2.5:1.5b

# 4. Install dependencies
pip install -r requirements.txt

# 5. Index a PDF
python3 local_pageindex.py ~/Desktop/Resume.pdf

# 6. Ask questions
python3 local_pageindex.py ~/Desktop/Resume.pdf --query "What are skills?"
```

That's it! No API keys, no signup, no costs. 🎉

---

## Support & Debugging

For detailed debugging:
```bash
# Enable verbose output
python3 local_pageindex.py your-file.pdf -v

# Check Ollama status
curl http://localhost:11434/api/tags

# View indexed tree
cat indexed_documents/your-file_tree.json | head -50
```

---

**Congratulations!** You now have a fully functional, API-key-free Vectorless RAG system running entirely on your machine.
