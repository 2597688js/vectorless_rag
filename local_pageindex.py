#!/usr/bin/env python3
"""
Local Vectorless RAG with Ollama - Pure Local PageIndex + Ollama LLM
No API keys required - Everything runs locally!
"""

import os
import sys
import json
import asyncio
from pathlib import Path

import requests
from pageindex import page_index_main
from pageindex.utils import ConfigLoader
import pageindex.utils as utils


def verify_ollama():
    """Check if Ollama is running"""
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"✓ Ollama is running with {len(models)} model(s)")
                return True
            else:
                print("✗ Ollama is running but no models found")
                print(f"  Pull a model with: ollama pull qwen2.5:1.5b")
                return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama at {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
        print(f"  Error: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False


async def call_ollama_llm(prompt, model=None, temperature=0):
    """Call Ollama LLM locally without any API keys"""
    import httpx

    model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
            }
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            raise Exception(f"Ollama error: {response.text}")


def flatten_tree(tree_structure):
    """Flatten nested tree structure into a single list"""
    flattened = []

    def traverse(nodes):
        if isinstance(nodes, list):
            for node in nodes:
                if isinstance(node, dict):
                    flattened.append(node)
                    if 'nodes' in node:
                        traverse(node['nodes'])
        elif isinstance(nodes, dict):
            flattened.append(nodes)
            if 'nodes' in nodes:
                traverse(nodes['nodes'])

    if isinstance(tree_structure, dict) and 'structure' in tree_structure:
        traverse(tree_structure['structure'])
    else:
        traverse(tree_structure)

    return flattened


def index_pdf_locally(pdf_path, model=None):
    """Generate tree structure locally using PageIndex (no API key needed)"""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        print(f"✗ File not found: {pdf_path}")
        sys.exit(1)

    if not pdf_path.suffix.lower() == ".pdf":
        print(f"✗ Not a PDF file: {pdf_path}")
        sys.exit(1)

    print(f"\n📄 Processing PDF locally with PageIndex: {pdf_path.name}")

    try:
        # Load configuration
        config_loader = ConfigLoader()
        user_opt = {'model': model}
        opt = config_loader.load({k: v for k, v in user_opt.items() if v is not None})

        print("⏳ Generating tree structure...")

        # Generate tree locally - NO API KEY NEEDED!
        tree_raw = page_index_main(str(pdf_path), opt)

        print("✓ Tree generation complete!")

        # Flatten the tree for easier retrieval
        flattened_tree = flatten_tree(tree_raw)

        # Store both the original and flattened versions
        tree = {
            'raw': tree_raw,
            'flattened': flattened_tree
        }

        # Generate a unique doc_id from filename
        doc_id = f"local-{pdf_path.stem}"

        return tree, doc_id

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def tree_search_with_ollama(tree, query, model=None):
    """Use Ollama to reason over the PageIndex tree and find relevant nodes"""

    # Extract only node IDs and titles for conciseness
    def extract_node_info(nodes, info_list=None):
        if info_list is None:
            info_list = []
        if isinstance(nodes, dict):
            if 'node_id' in nodes and 'title' in nodes:
                info_list.append({
                    'node_id': nodes['node_id'],
                    'title': nodes['title'],
                    'summary': nodes.get('summary', '')[:200]  # Truncate summary
                })
            if 'nodes' in nodes:
                extract_node_info(nodes['nodes'], info_list)
        elif isinstance(nodes, list):
            for node in nodes:
                extract_node_info(node, info_list)
        return info_list

    tree_info = extract_node_info(tree.get('structure', tree) if isinstance(tree, dict) and 'structure' in tree else tree)

    search_prompt = f"""You are given a question and a tree structure of a document.
Each node has an ID, title, and summary.
Your task is to find all node IDs that are likely to contain the answer to the question.

Question: {query}

Available nodes:
{json.dumps(tree_info, indent=2)}

Reply ONLY with valid JSON in this exact format:
{{
    "thinking": "Your analysis",
    "node_list": ["0001", "0003"]
}}"""

    print("\n🔍 Searching tree with Ollama reasoning...")
    result = await call_ollama_llm(search_prompt, model)

    try:
        # Try to extract JSON from the response
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = result[json_start:json_end]
            return json.loads(json_str)
        else:
            raise json.JSONDecodeError("No JSON found", result, 0)
    except json.JSONDecodeError:
        print("⚠️  Could not parse Ollama response as JSON")
        print("Response:", result[:300])
        # Fallback: try to extract node_list from the response text
        return {"thinking": "Parse error", "node_list": []}


async def generate_answer_with_ollama(query, relevant_content, model=None):
    """Use Ollama to generate final answer based on retrieved context"""

    answer_prompt = f"""Answer the question based on the context:

Question: {query}

Context:
{relevant_content}

Provide a clear, concise answer based only on the context provided."""

    print("📝 Generating answer with Ollama...")
    answer = await call_ollama_llm(answer_prompt, model)
    return answer


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Vectorless RAG with Local PageIndex + Ollama LLM"
    )
    parser.add_argument("pdf_path", help="Path to PDF file to index")
    parser.add_argument("--query", help="Query to search the document")
    parser.add_argument("--model", help="Ollama model (default: qwen2.5:1.5b)")
    parser.add_argument("--output-dir", default="indexed_documents", help="Output directory")

    args = parser.parse_args()

    # Verify setup
    if not verify_ollama():
        print("\n⚠️  Ollama is not available. Please start it with: ollama serve")
        sys.exit(1)

    print("\n✨ Using Local PageIndex - NO API KEYS REQUIRED!")

    # Index PDF locally (synchronous, before async context)
    tree, doc_id = index_pdf_locally(args.pdf_path, args.model)

    # Save tree
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    tree_file = output_dir / f"{Path(args.pdf_path).stem}_tree.json"
    with open(tree_file, "w") as f:
        json.dump(tree['raw'], f, indent=2)
    print(f"💾 Tree saved to: {tree_file}")

    # If query provided, do retrieval + generation (async)
    if args.query:
        print("\n" + "="*50)
        print("RETRIEVAL & GENERATION")
        print("="*50)

        asyncio.run(query_and_answer(tree, args.query, args.model))
    else:
        print("\n💡 Tip: Use --query to search the document:")
        print(f"  python3 local_pageindex.py {args.pdf_path} --query 'Your question here'")


async def query_and_answer(tree, query, model):
    """Perform async retrieval and answer generation"""
    # Use the raw tree for search (with full structure)
    tree_raw = tree['raw']
    flattened_tree = tree['flattened']

    # Tree search with Ollama
    search_result = await tree_search_with_ollama(tree_raw, query, model)

    print("\n💭 Reasoning Process:")
    print(search_result.get("thinking", "")[:500])

    # Get node content from flattened tree
    node_list = search_result.get("node_list", [])

    if node_list:
        print(f"\n📍 Retrieved {len(node_list)} relevant nodes:")

        # Create a mapping of node_id to node for quick lookup
        node_map = {node['node_id']: node for node in flattened_tree}

        relevant_nodes = []
        for node_id in node_list:
            if node_id in node_map:
                node = node_map[node_id]
                relevant_nodes.append(node)
                page_info = f" (Page {node.get('start_index', 'N/A')})" if 'start_index' in node else ""
                print(f"  - {node['title']}{page_info}")

        # Extract content from relevant nodes (prefer text over summary)
        relevant_content = "\n\n".join(
            f"## {node['title']}\n{node.get('text', node.get('summary', ''))}"
            for node in relevant_nodes
        )

        # Generate answer
        answer = await generate_answer_with_ollama(query, relevant_content, model)

        print("\n✨ Answer:")
        print("-" * 50)
        print(answer)
        print("-" * 50)
    else:
        print("⚠️  No relevant nodes found")


if __name__ == "__main__":
    main()
