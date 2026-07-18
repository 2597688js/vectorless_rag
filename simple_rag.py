#!/usr/bin/env python3
"""
Simple RAG with Local Ollama - No complex parsing, just direct Q&A
Works perfectly with small models like Qwen 2.5 1.5B and Mistral 7B
"""

import asyncio
import os
import sys
from pathlib import Path
import PyPDF2
import requests


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
                return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama at {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
        print(f"  Error: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False


async def call_ollama(prompt, model="mistral:7b", temperature=0):
    """Call Ollama LLM locally"""
    import httpx

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


async def rag_query(pdf_path, query, model="qwen2.5:1.5b"):
    """Run RAG: extract PDF text and query with Ollama"""

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"✗ File not found: {pdf_path}")
        sys.exit(1)

    # Extract text from PDF
    print(f"📄 Extracting text from: {pdf_path.name}")
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(pdf_reader.pages, 1):
            text += f"\n--- Page {i} ---\n"
            text += page.extract_text() + "\n"

    char_count = len(text)
    page_count = len(pdf_reader.pages)
    print(f"✓ Extracted {char_count} characters from {page_count} page(s)\n")

    # Query with Ollama
    prompt = f"""Answer the following question based ONLY on the document provided.
If the answer is not in the document, clearly state that.

Question: {query}

Document:
{text}

Answer:"""

    print(f"🔍 Querying with {model}...\n")
    answer = await call_ollama(prompt, model=model)

    print("✨ Answer:")
    print("=" * 60)
    print(answer)
    print("=" * 60)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Simple RAG with Local Ollama - No PageIndex complexity"
    )
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--query", required=True, help="Question to ask about the document")
    parser.add_argument("--model", default="mistral:7b",
                       help="Ollama model to use (default: mistral:7b)")

    args = parser.parse_args()

    if not verify_ollama():
        sys.exit(1)

    print("\n✨ Simple RAG with Local Ollama - NO API KEYS NEEDED!\n")

    asyncio.run(rag_query(args.pdf_path, args.query, args.model))


if __name__ == "__main__":
    main()
