#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate
export RAG_SERVER_URL="${RAG_SERVER_URL:-http://127.0.0.1:8001/answer}"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
