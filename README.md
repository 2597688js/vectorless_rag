## PageIndex Introduction
PageIndex is a new **reasoning-based**, **vectorless RAG** framework that performs retrieval in two steps:  
1. Generate a tree structure index of documents  
2. Perform reasoning-based retrieval through tree search  


Compared to traditional vector-based RAG, PageIndex features:
- **No Vectors Needed**: Uses document structure and LLM reasoning for retrieval.
- **No Chunking Needed**: Documents are organized into natural sections rather than artificial chunks.
- **Human-like Retrieval**: Simulates how human experts navigate and extract knowledge from complex documents. 
- **Transparent Retrieval Process**: Retrieval based on reasoning — say goodbye to approximate semantic search ("vibe retrieval").

PageIndex framework is built to support far more advanced use cases such as:

- Multi-Node Reasoning with Content Extraction — Scale tree search to extract and select relevant content from multiple nodes.
- Multi-Document Search — Enable reasoning-based navigation across large document collections, extending beyond a single file.
- Efficient Tree Search — Improve tree search efficiency for long documents with a large number of nodes.
- Expert Knowledge Integration and Preference Alignment — Incorporate user preferences or expert insights by adding knowledge directly into the LLM tree search, without the need for fine-tuning.

## Local PageIndex Implementation (Zero API Keys Required! 🎉)

### What Changes Were Made?

The implementation has been completely refactored to use **local PageIndex processing** instead of cloud APIs. Here's what was bypassed:

1. **❌ Removed**: `PageIndexClient` (cloud-based API) 
2. **✅ Added**: `page_index_main()` (local PageIndex library)
3. **❌ Removed**: `PAGEINDEX_API_KEY` requirement
4. **✅ Retained**: Full PageIndex tree generation capabilities locally
5. **✅ Integration**: Ollama for local LLM-based reasoning and answer generation

**Key Implementation Details:**
- PDF parsing and tree generation: **100% Local** using PageIndex library
- LLM reasoning for search: **Local Ollama** (no external LLM APIs)
- Answer generation: **Local Ollama** (no external LLM APIs)  
- Configuration: Uses `pageindex/utils.py` ConfigLoader
- Tree Structure: Automatically flattened for efficient retrieval

### How to Run the File

#### Prerequisites
- **Ollama installed and running** (see [OLLAMA_SETUP.md](./OLLAMA_SETUP.md) for installation instructions)
- Python 3.7+ installed
- Dependencies installed: `pip install -r requirements.txt`

#### ⭐ NO API KEYS NEEDED
- ❌ No PAGEINDEX_API_KEY required
- ❌ No OpenAI/Anthropic API keys needed  
- ✅ Everything runs locally on your machine

#### Basic Usage

**Index a PDF document:**
```bash
python3 local_pageindex.py <path_to_pdf>
```

Example:
```bash
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf
```

Output:
```
✓ Ollama is running with 1 model(s)
✨ Using Local PageIndex - NO API KEYS REQUIRED!
📄 Processing PDF locally with PageIndex: Resume_2026.pdf
⏳ Generating tree structure...
...
✓ Tree generation complete!
💾 Tree saved to: indexed_documents/Resume_2026_tree.json
```

**Query an indexed document:**
```bash
python3 local_pageindex.py <path_to_pdf> --query "Your question here"
```

Example:
```bash
python3 local_pageindex.py ~/Desktop/Resume_2026.pdf --query "What is the total experience?"
```

Output:
```
🔍 Searching tree with Ollama reasoning...
💭 Reasoning Process: [Shows LLM thinking]
📍 Retrieved N relevant nodes: [Lists nodes found]
📝 Generating answer with Ollama...
✨ Answer: [AI-generated answer based on document content]
```

#### Output Structure

When you index a document, a tree structure is created and saved as JSON:
- **Hierarchical Nodes**: Document sections organized by meaning
- **Summaries**: AI-generated summaries for each node
- **Node IDs**: Unique identifiers for retrieval
- **Page References**: Original page numbers

Example output file: `indexed_documents/Resume_2026_tree.json`

```json
{
  "doc_name": "Resume_2026.pdf",
  "structure": [
    {
      "title": "Experience",
      "node_id": "0003",
      "summary": "...",
      "nodes": [...]
    }
  ]
}
```

#### How the API Key Was Bypassed

**Original Flow (Cloud-based):**
```
PDF → PageIndexClient (needs API key) → OpenAI API → Tree JSON → Ollama Reasoning
                       ↓
              REQUIRES: PAGEINDEX_API_KEY + OPENAI_API_KEY
```

**New Local Flow (100% Offline):**
```
PDF → page_index_main() (local) → Ollama (local model) → Tree JSON → Ollama Reasoning
                    ↓
            REQUIRES: Nothing! (just Ollama running)
```

**Technical Implementation:**

1. **PDF Tree Generation:**
   - `page_index_main()` from local PageIndex library (no cloud calls)
   - Configuration: `pageindex/config.yaml` set to use `ollama/qwen2.5:1.5b`
   - No API keys needed for this step

2. **Query Processing:**
   - Ollama-based reasoning over the tree structure
   - Finds relevant document sections locally
   - No external LLM API calls

3. **Answer Generation:**
   - Ollama-based answer synthesis from relevant content
   - All LLM work happens locally on your machine

**Key Configuration:**
```yaml
# pageindex/config.yaml
model: "ollama/qwen2.5:1.5b"           # Uses local Ollama (was: gpt-4o-2024-11-20)
retrieve_model: "ollama/qwen2.5:1.5b"  # Uses local Ollama (was: gpt-5.4)
```

This configuration means PageIndex automatically uses Ollama instead of OpenAI for all LLM operations during tree generation.

#### What Was Bypassed

| API Key | Status | Why |
|---------|--------|-----|
| `PAGEINDEX_API_KEY` | ❌ Bypassed | Using local `page_index_main()` instead of `PageIndexClient` |
| `OPENAI_API_KEY` | ❌ Bypassed | PageIndex configured to use Ollama (`ollama/qwen2.5:1.5b`) |
| `ANTHROPIC_API_KEY` | ❌ Bypassed | Ollama handles all LLM reasoning and generation |
| Any LLM API Key | ❌ Bypassed | Local Ollama provides all LLM capabilities |

#### Benefits of Local PageIndex

✅ **Zero API Costs** — Run completely free on your local machine  
✅ **Zero API Keys** — No external authentication required whatsoever
✅ **Complete Privacy** — All data stays on your machine, nothing leaves
✅ **Offline Access** — Works without internet connection (after Ollama setup)  
✅ **Fast Processing** — No network latency for indexing or queries  
✅ **Full Control** — Customize LLM models and parameters easily  
✅ **Open Source** — Uses open-source PageIndex library locally  
✅ **Sustainable** — No dependency on external service availability
