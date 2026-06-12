import argparse
import hashlib
import html
import re
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_URL = "https://www.dankook.ac.kr/web/kor/-390"
EMBEDDING_MODEL = "BAAI/bge-m3"
CHROMA_PATH = str(Path(__file__).resolve().parents[1] / "vector_store" / "chroma")
CHROMA_COLLECTION = "academic_document_chunks"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if tag in {"p", "br", "div", "li", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"p", "div", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)

    def text(self):
        raw_text = html.unescape(" ".join(self.parts))
        lines = [re.sub(r"\s+", " ", line).strip() for line in raw_text.splitlines()]
        return "\n".join(line for line in lines if line)


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; DKU-RAG-Ingest/1.0)",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def normalize_url(url):
    return urllib.parse.urljoin(BASE_URL, html.unescape(url))


def board_prefix(base_url):
    slug = urllib.parse.urlparse(base_url).path.rstrip("/").split("/")[-1]
    if slug == "-390":
        return "dku_notice"
    return "dku_" + re.sub(r"[^0-9A-Za-z]+", "_", slug).strip("_")


def list_page_url(base_url, page):
    params = {
        "p_p_id": "dku_bbs_web_BbsPortlet",
        "p_p_lifecycle": "0",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "_dku_bbs_web_BbsPortlet_cur": str(page),
        "_dku_bbs_web_BbsPortlet_action": "view",
        "_dku_bbs_web_BbsPortlet_orderBy": "createDate",
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def detail_page_url(base_url, message_id, page):
    params = {
        "p_p_id": "dku_bbs_web_BbsPortlet",
        "p_p_lifecycle": "0",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "_dku_bbs_web_BbsPortlet_cur": str(page),
        "_dku_bbs_web_BbsPortlet_action": "view_message",
        "_dku_bbs_web_BbsPortlet_orderBy": "createDate",
        "_dku_bbs_web_BbsPortlet_bbsMessageId": str(message_id),
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def extract_notice_links(page_html, page, base_url=BASE_URL):
    links = set()
    for match in re.finditer(r'href=["\']([^"\']*bbsMessageId=\d+[^"\']*)["\']', page_html):
        links.add(normalize_url(match.group(1)))
    for match in re.finditer(r"_dku_bbs_web_BbsPortlet_viewMessage\(\s*(\d+)\s*,", page_html):
        links.add(detail_page_url(base_url, match.group(1), page))
    return sorted(links)


def extract_title(page_html, fallback):
    board_title_match = re.search(
        r"<th[^>]*colspan=[\"']?2[\"']?[^>]*>(.*?)</th>",
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    if board_title_match:
        title_parser = TextExtractor()
        title_parser.feed(board_title_match.group(1))
        title = title_parser.text().strip()
        if title:
            return title

    title_match = re.search(r"<title[^>]*>(.*?)</title>", page_html, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = re.sub(r"\s+", " ", html.unescape(title_match.group(1))).strip()
        title = re.sub(r"\s*-\s*단국대학교.*$", "", title).strip()
        if title:
            return title

    heading_match = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", page_html, re.IGNORECASE | re.DOTALL)
    if heading_match:
        title = TextExtractor()
        title.feed(heading_match.group(1))
        if title.text():
            return title.text().splitlines()[0]

    return fallback


def extract_board_body(page_html):
    body_match = re.search(
        r"<td[^>]*class=[\"'][^\"']*\br_cont\b[^\"']*[\"'][^>]*>(.*?)</td>",
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    if body_match:
        body_parser = TextExtractor()
        body_parser.feed(body_match.group(1))
        return body_parser.text()

    table_match = re.search(
        r"<table[^>]*summary=[\"']게시판 상세 내용을 볼 수 있는 페이지[\"'][^>]*>(.*?)</table>",
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    if table_match:
        table_parser = TextExtractor()
        table_parser.feed(table_match.group(1))
        return table_parser.text()

    parser = TextExtractor()
    parser.feed(page_html)
    return parser.text()


def extract_board_metadata(page_html):
    metadata = {}
    row_pattern = re.compile(
        r"<tr>\s*<th[^>]*>.*?</span>\s*(분류|작성자|날짜)\s*</th>\s*<td[^>]*>(.*?)</td>\s*</tr>",
        re.IGNORECASE | re.DOTALL,
    )
    for key, value_html in row_pattern.findall(page_html):
        value_parser = TextExtractor()
        value_parser.feed(value_html)
        value = value_parser.text().strip()
        if value:
            metadata[key] = value
    return metadata


def extract_year(*values):
    for value in values:
        match = re.search(r"(20\d{2})", value or "")
        if match:
            return match.group(1)
    return ""


def extract_document(url):
    page_html = fetch(url)
    title = extract_title(page_html, url)
    metadata = extract_board_metadata(page_html)
    body = extract_board_body(page_html)
    metadata_text = "\n".join(f"{key}: {value}" for key, value in metadata.items())
    text = "\n\n".join(part for part in [title, metadata_text, body] if part)
    return title, text, metadata


def chunk_text(text, chunk_size=900, overlap=120):
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def document_id(url, prefix="dku_notice"):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    message_ids = query.get("_dku_bbs_web_BbsPortlet_bbsMessageId") or query.get("bbsMessageId")
    if message_ids:
        return f"{prefix}_{message_ids[0]}"
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


def crawl_links(base_url, start_page, pages, delay):
    links = []
    seen = set()
    end_page = start_page + pages - 1
    for page in range(start_page, end_page + 1):
        url = list_page_url(base_url, page)
        print(f"Collect list page {page}/{end_page}: {url}", flush=True)
        page_links = extract_notice_links(fetch(url), page, base_url=base_url)
        print(f"Found {len(page_links)} detail links on page {page}", flush=True)
        for link in page_links:
            if link not in seen:
                seen.add(link)
                links.append(link)
        time.sleep(delay)
    return links


def upsert_documents(links, delay, chunk_size, overlap, prefix):
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(CHROMA_COLLECTION)

    total_chunks = 0
    for index, url in enumerate(links, start=1):
        try:
            title, text, board_metadata = extract_document(url)
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
            doc_id = document_id(url, prefix=prefix)
            document_year = extract_year(board_metadata.get("날짜", ""), title, text)

            if not chunks:
                print(f"Skip empty document: {url}", flush=True)
                continue

            ids = [f"{doc_id}_chunk_{chunk_index}" for chunk_index in range(len(chunks))]
            embeddings = model.encode(chunks, normalize_embeddings=True, show_progress_bar=False).tolist()
            metadatas = [
                {
                    "title": title,
                    "source_url": url,
                    "document_id": doc_id,
                    "chunk_id": ids[chunk_index],
                    "date": board_metadata.get("날짜", ""),
                    "year": document_year,
                }
                for chunk_index in range(len(chunks))
            ]

            collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
            total_chunks += len(chunks)
            print(f"[{index}/{len(links)}] Saved: {title} ({len(chunks)} chunks)", flush=True)
        except Exception as error:
            print(f"[{index}/{len(links)}] Failed: {url} - {error}", flush=True)
        time.sleep(delay)

    print(f"Done: checked {len(links)} documents, upserted {total_chunks} chunks", flush=True)
    print(f"Current collection chunk count: {collection.count()}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="단국대학교 공지 게시판을 크롤링해 RAG Chroma DB에 추가합니다.")
    parser.add_argument("--base-url", default=BASE_URL, help="크롤링할 단국대 게시판 기본 URL")
    parser.add_argument("--start-page", type=int, default=1, help="시작 목록 페이지")
    parser.add_argument("--pages", type=int, default=1, help="공지 목록에서 가져올 페이지 수")
    parser.add_argument("--delay", type=float, default=0.5, help="요청 사이 대기 시간(초)")
    parser.add_argument("--chunk-size", type=int, default=900)
    parser.add_argument("--overlap", type=int, default=120)
    args = parser.parse_args()

    prefix = board_prefix(args.base_url)
    print(f"Board URL: {args.base_url}", flush=True)
    print(f"Document ID prefix: {prefix}", flush=True)
    links = crawl_links(args.base_url, args.start_page, args.pages, args.delay)
    print(f"Collected detail URLs: {len(links)}", flush=True)
    upsert_documents(links, args.delay, args.chunk_size, args.overlap, prefix)


if __name__ == "__main__":
    main()
