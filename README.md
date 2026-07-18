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
