import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
CHROMA_PATH = os.getenv("CHROMA_PATH", str(Path(__file__).resolve().parents[1] / "vector_store" / "chroma"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "academic_document_chunks")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "1800"))
RAG_HOST = os.getenv("RAG_HOST", "127.0.0.1")
RAG_PORT = int(os.getenv("RAG_PORT", "8001"))

print(f"임베딩 모델 로딩: {EMBEDDING_MODEL}", flush=True)
MODEL = SentenceTransformer(EMBEDDING_MODEL)
CHROMA_CLIENT = chromadb.PersistentClient(path=CHROMA_PATH)
COLLECTION = CHROMA_CLIENT.get_collection(CHROMA_COLLECTION)
print(f"RAG 서버 준비 완료: http://{RAG_HOST}:{RAG_PORT}", flush=True)


def search_context(query):
    query_embedding = MODEL.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0].tolist()

    result = COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=RAG_TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    contexts = []
    used_chars = 0

    for index, (document, metadata, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        remaining = MAX_CONTEXT_CHARS - used_chars
        if remaining <= 0:
            break

        text = document[:remaining]
        used_chars += len(text)

        contexts.append(
            {
                "index": index,
                "distance": distance,
                "title": metadata.get("title", "제목 없음"),
                "source_url": metadata.get("source_url", ""),
                "document_id": metadata.get("document_id", ""),
                "chunk_id": metadata.get("chunk_id", ""),
                "content": text,
            }
        )

    return contexts


def build_prompt(query, contexts):
    context_text = "\n\n".join(
        [
            f"[근거 {item['index']}]\n"
            f"제목: {item['title']}\n"
            f"출처: {item['source_url']}\n"
            f"내용: {item['content']}"
            for item in contexts
        ]
    )

    return f"""
너는 단국대학교 학사/공지 안내 챗봇이다.
아래 검색 근거만 사용해서 한국어로 답변해라.
근거에 없는 내용은 추측하지 말고, 모르면 근거에서 확인되지 않는다고 말해라.
날짜나 기간이 있으면 구체적으로 말해라.
참고 출처나 URL은 답변에 직접 쓰지 마라. 출처는 시스템 코드가 따로 붙인다.

사용자 질문:
{query}

검색 근거:
{context_text}

답변 형식:
- 핵심 답변을 먼저 말한다.
- 필요한 경우 신청 기간, 대상, 방법을 나누어 설명한다.
""".strip()


def call_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data.get("response", "").strip()


def build_sources(contexts):
    sources = []
    seen = set()

    for item in contexts:
        source_url = item.get("source_url", "")
        title = item.get("title", "제목 없음")
        key = (title, source_url)

        if key in seen:
            continue

        seen.add(key)
        sources.append({"title": title, "source_url": source_url})

    return sources


def remove_model_sources(answer):
    return re.split(r"\n\s*참고\s*출처\s*:", answer, maxsplit=1)[0].rstrip()


def attach_sources(answer, sources):
    answer = remove_model_sources(answer)

    if not sources:
        return answer

    lines = ["", "참고 출처:"]
    for index, source in enumerate(sources, start=1):
        title = source["title"]
        source_url = source["source_url"]
        if source_url:
            lines.append(f"[{index}] {title}\n{source_url}")
        else:
            lines.append(f"[{index}] {title}")

    return f"{answer.rstrip()}\n" + "\n".join(lines)


def answer_question(query):
    contexts = search_context(query)
    if not contexts:
        return {"answer": "관련 근거를 찾지 못했습니다.", "sources": [], "contexts": []}

    prompt = build_prompt(query, contexts)
    answer = call_ollama(prompt)
    sources = build_sources(contexts)

    return {
        "answer": attach_sources(answer, sources),
        "sources": sources,
        "contexts": contexts,
    }


class RagHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"ok": True, "model": EMBEDDING_MODEL, "collection": CHROMA_COLLECTION})
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/answer":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body or "{}")
            question = str(data.get("question", "")).strip()

            if not question:
                self.send_json(400, {"error": "question 값이 필요합니다."})
                return

            result = answer_question(question)
            self.send_json(200, result)
        except urllib.error.URLError as error:
            self.send_json(500, {"error": f"Ollama 호출 실패: {error}"})
        except Exception as error:
            self.send_json(500, {"error": str(error)})

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}", flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer((RAG_HOST, RAG_PORT), RagHandler)
    server.serve_forever()