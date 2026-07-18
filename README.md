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

## Local PageIndex Implementation

### What Changes Were Made?

A local implementation of PageIndex has been created that allows you to run document indexing and querying **entirely offline without any API keys**. Here's what was implemented:

1. **Ollama Integration**: The system now uses Ollama (a local LLM runtime) instead of cloud-based APIs
2. **Local Indexing**: Documents are indexed locally on your machine using `local_pageindex.py`
3. **Tree-based Storage**: Indexed documents are stored as JSON tree structures in the `indexed_documents/` directory
4. **Reasoning-based Retrieval**: Queries are processed using local LLM reasoning through Ollama
5. **Zero External Dependencies**: No API keys, cloud services, or external APIs required

### How to Run the File

#### Prerequisites
- Ollama installed and running (see [OLLAMA_SETUP.md](./OLLAMA_SETUP.md) for installation instructions)
- Python 3.7+ installed
- Dependencies installed: `pip install -r requirements.txt`

#### Basic Usage

**Index a PDF document:**
```bash
python3 local_pageindex.py <path_to_pdf>
```

Example:
```bash
python3 local_pageindex.py /Users/janarddan/Desktop/JS_Resume_2026.pdf
```

This will:
- Extract and process the PDF content
- Generate a tree structure index
- Save the indexed tree to `indexed_documents/<filename>_tree.json`

**Query an indexed document:**
```bash
python3 local_pageindex.py <path_to_pdf> --query "Your question here"
```

Example:
```bash
python3 local_pageindex.py /Users/janarddan/Desktop/JS_Resume_2026.pdf --query "What is the total experience?"
```

This will:
- Search the indexed tree using reasoning-based retrieval
- Display the thinking process
- Provide an AI-generated answer based on the document content

#### Output Structure

When you index a document, a tree structure is created and saved. The tree contains:
- **Nodes**: Sections of the document with summaries and full text
- **Page Index**: Reference to original page number
- **Hierarchical Organization**: Natural document structure preserved

Example output file: `indexed_documents/JS_Resume_2026_tree.json`

#### Benefits of Local PageIndex

✅ **No API Costs** — Run completely free on your local machine  
✅ **Privacy** — All data stays local, nothing sent to external servers  
✅ **Offline Access** — Works without internet connection (after Ollama setup)  
✅ **Fast Processing** — No network latency for queries  
✅ **Customizable** — Full control over the LLM model and parameters
