#!/bin/bash
# Quick start examples for local_pageindex.py

echo "🚀 Local Vectorless RAG with PageIndex + Ollama"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Prerequisites:${NC}"
echo "1. Ollama running: ollama serve"
echo "2. Model available: ollama pull qwen2.5:1.5b"
echo ""

VENV="vectorless_venv/bin/python3"
SCRIPT="local_pageindex.py"

if [ ! -f "$SCRIPT" ]; then
    echo "❌ local_pageindex.py not found"
    exit 1
fi

if [ ! -f "$VENV" ]; then
    echo "❌ Virtual environment not found. Create with: python3 -m venv vectorless_venv"
    exit 1
fi

echo -e "${GREEN}Example 1: Check Ollama Status${NC}"
echo "  cd /Users/janarddan/1.jana\ files/3.MyMacProjects/6.vectorless_rag"
echo "  $VENV $SCRIPT data/sample.pdf 2>&1 | head -5"
echo ""

echo -e "${GREEN}Example 2: Index a PDF${NC}"
echo "  $VENV $SCRIPT /path/to/document.pdf"
echo ""

echo -e "${GREEN}Example 3: Index + Query${NC}"
echo "  $VENV $SCRIPT /path/to/document.pdf \\"
echo "    --query 'What are the main conclusions?'"
echo ""

echo -e "${GREEN}Example 4: Use Different Model${NC}"
echo "  $VENV $SCRIPT /path/to/document.pdf \\"
echo "    --model mistral \\"
echo "    --query 'Summarize the key findings'"
echo ""

echo -e "${GREEN}Example 5: Save to Custom Directory${NC}"
echo "  $VENV $SCRIPT /path/to/document.pdf \\"
echo "    --output-dir my_indexes \\"
echo "    --query 'What is the methodology?'"
echo ""

echo -e "${BLUE}Helpful Commands:${NC}"
echo "  # List available Ollama models"
echo "  ollama list"
echo ""
echo "  # Pull another model"
echo "  ollama pull mistral"
echo ""
echo "  # View help"
echo "  $VENV $SCRIPT --help"
echo ""
