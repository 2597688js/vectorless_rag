# Local Vectorless RAG with PageIndex + Ollama

This script combines PageIndex (cloud tree generation) with Ollama (local LLM reasoning) for a hybrid vectorless RAG system that requires **no external LLM API keys**.

## Setup

### 1. Install Ollama
- Download from: https://ollama.ai
- Install and run: `ollama serve`

### 2. Pull a Model
```bash
ollama pull qwen2.5:1.5b    # Default (fast, ~1.5B params)
# Or other models:
ollama pull mistral         # Fast & capable
ollama pull llama2          # Strong reasoning
ollama pull neural-chat     # Optimized for chat
```

### 3. Update Environment (already configured)
Your `.env` file already has:
```
PAGEINDEX_API_KEY=...        # Cloud indexing service
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b   # Change to your preferred model
```

### 4. Install Dependencies
```bash
source vectorless_venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Basic: Index a PDF only
```bash
python3 local_pageindex.py /path/to/document.pdf
```
This submits to PageIndex cloud API to generate a tree structure, saves it as JSON.

### Advanced: Index + Search + Answer
```bash
python3 local_pageindex.py /path/to/document.pdf \
  --query "What are the key conclusions?"
```

This:
1. 📄 Submits PDF to PageIndex cloud API
2. ⏳ Waits for tree generation
3. 🔍 Uses Ollama to reason over the tree and find relevant nodes
4. 📝 Uses Ollama to generate a final answer

### Options
```bash
python3 local_pageindex.py document.pdf \
  --query "Your question here" \
  --model mistral \                          # Use different Ollama model
  --output-dir my_indexes                    # Save trees here
```

## What Runs Locally vs Cloud

| Component | Location | Requires API Key |
|-----------|----------|------------------|
| PDF → Tree structure | PageIndex Cloud API | ✓ (PAGEINDEX_API_KEY) |
| Tree search reasoning | Ollama (local) | ✗ No |
| Answer generation | Ollama (local) | ✗ No |
| LLM calls | Your machine | ✗ No |

## No External LLM API Keys!

- ❌ No OpenAI API key needed
- ❌ No Anthropic API key needed  
- ✅ Everything runs locally once the tree is generated

## Troubleshooting

**"Cannot connect to Ollama"**
```bash
# In another terminal:
ollama serve
```

**"No models found"**
```bash
ollama pull qwen2.5:1.5b
```

**"LimitReached" from PageIndex**
- You've hit your quota on the free PageIndex account
- Get an API key: https://dash.pageindex.ai/api-keys

**Slow responses?**
- Switch to a smaller, faster model:
  ```bash
  python3 local_pageindex.py doc.pdf --model qwen2.5:0.5b
  ```

## Example Output

```
✓ Ollama is running with 3 model(s)

📄 Submitting PDF to PageIndex: research.pdf
✓ Document submitted. Doc ID: abc123def456
⏳ Waiting for tree generation...
.....
✓ Tree generation complete!
💾 Tree saved to: indexed_documents/research_tree.json

==================================================
RETRIEVAL & GENERATION
==================================================

🔍 Searching tree with Ollama reasoning...

💭 Reasoning Process:
Based on the question "What are the main findings?", the relevant nodes appear to be...

📍 Retrieved 3 relevant nodes:
  - Main Results (Page 5)
  - Experimental Setup (Page 3)
  - Discussion (Page 8)

📝 Generating answer with Ollama...

✨ Answer:
--------------------------------------------------
The main findings of this research include:
1. A 15% improvement in baseline performance
2. Novel architecture reduces inference latency
3. Results are reproducible across three datasets
--------------------------------------------------
```

## Advanced: Using Different Models

### Fast models (good for simple queries)
```bash
ollama pull qwen2.5:0.5b
ollama pull tinyllama
```

### Balanced models  
```bash
ollama pull mistral
ollama pull qwen2.5:1.5b   # Default
```

### Powerful models (better reasoning)
```bash
ollama pull llama2:13b
ollama pull mistral:7b
```

Check available models:
```bash
ollama list
```

## Notes

- **First run is slow**: PageIndex needs to generate the tree (can take a few minutes for large PDFs)
- **Subsequent queries are fast**: Tree is cached, Ollama runs locally
- **Privacy**: Document tree is sent to PageIndex cloud once. After that, all reasoning happens locally.
- **Cost**: Only PageIndex API calls cost money (if beyond free tier). Ollama is free.
