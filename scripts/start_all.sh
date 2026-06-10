#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

export RAG_HOST="${RAG_HOST:-127.0.0.1}"
export RAG_PORT="${RAG_PORT:-8001}"
export RAG_SERVER_URL="${RAG_SERVER_URL:-http://127.0.0.1:8001/answer}"
export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:3b}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-BAAI/bge-m3}"
export CHROMA_PATH="${CHROMA_PATH:-$(pwd)/vector_store/chroma}"
export CHROMA_COLLECTION="${CHROMA_COLLECTION:-academic_document_chunks}"
export RAG_TOP_K="${RAG_TOP_K:-3}"
export MAX_CONTEXT_CHARS="${MAX_CONTEXT_CHARS:-1800}"

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"

if ! curl -sS --max-time 3 "${OLLAMA_BASE_URL}/api/tags" >/dev/null 2>&1; then
  WINDOWS_HOST="$(ip route | awk '/^default/ {print $3; exit}')"
  if curl -sS --max-time 3 "http://${WINDOWS_HOST}:11434/api/tags" >/dev/null 2>&1; then
    OLLAMA_BASE_URL="http://${WINDOWS_HOST}:11434"
  else
    WINDOWS_HOST="$(awk '/nameserver/ {print $2; exit}' /etc/resolv.conf)"
    if curl -sS --max-time 3 "http://${WINDOWS_HOST}:11434/api/tags" >/dev/null 2>&1; then
      OLLAMA_BASE_URL="http://${WINDOWS_HOST}:11434"
    else
      echo "Ollama server is not reachable from WSL."
      echo "Do not install Ollama in WSL. Start Ollama on Windows first."
      echo "Windows PowerShell: ollama run qwen2.5:3b hello"
      echo "If it still fails, set Windows OLLAMA_HOST=0.0.0.0:11434 and restart Ollama."
      exit 1
    fi
  fi
fi

export OLLAMA_URL="${OLLAMA_BASE_URL}/api/generate"
echo "Using Ollama: ${OLLAMA_BASE_URL}"

if [ ! -d "$CHROMA_PATH" ]; then
  echo "Chroma vector store not found: $CHROMA_PATH"
  echo "Copy vector_store/chroma into this repo or run the embedding build step first."
  exit 1
fi

python rag/rag_server.py &
RAG_PID=$!

sleep 5
if ! kill -0 "$RAG_PID" 2>/dev/null; then
  echo "RAG server failed to start. Run: ./scripts/setup_rag.sh"
  wait "$RAG_PID"
  exit 1
fi

cleanup() {
  kill "$RAG_PID" 2>/dev/null || true
}
trap cleanup EXIT

uvicorn main:app --reload --host 0.0.0.0 --port 8000
