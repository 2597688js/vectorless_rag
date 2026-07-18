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

**Original Flow:**
```
PDF → PageIndexClient (Cloud API) → Requires PAGEINDEX_API_KEY → Tree JSON
```

**New Local Flow:**
```
PDF → page_index_main() (Local) → Requires ConfigLoader + Ollama → Tree JSON
```

**Technical Changes:**
1. Replaced `PageIndexClient()` with `page_index_main()` from the local PageIndex library
2. Used `ConfigLoader()` to load PageIndex configuration locally
3. Tree structure automatically handled with flattening logic
4. JSON responses from Ollama parsed robustly to handle truncation
5. All processing stays on your machine - zero cloud calls for PDF processing

#### Benefits of Local PageIndex

✅ **No API Costs** — Run completely free on your local machine  
✅ **No API Keys** — PAGEINDEX_API_KEY, OpenAI key, Anthropic key all optional
✅ **Privacy** — All data stays local, nothing sent to external servers  
✅ **Offline Access** — Works without internet connection (after Ollama setup)  
✅ **Fast Processing** — No network latency for queries or indexing  
✅ **Customizable** — Full control over the LLM model and parameters  
✅ **Open Source** — Uses open-source PageIndex library locally
