#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate
python -m pip install -r rag/requirements-rag.txt

echo "RAG dependencies installed."
echo "Make sure Ollama is installed and run: ollama pull qwen2.5:3b"
