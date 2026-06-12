import argparse
import datetime
import json
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

import chromadb
from sentence_transformers import SentenceTransformer


BASE_URL = "https://www.dankook.ac.kr/web/kor/-2014-"
API_BASE_URL = "https://www.dankook.ac.kr/o/dku_calendar-rest/calendar/events"
EMBEDDING_MODEL = "BAAI/bge-m3"
CHROMA_PATH = str(Path(__file__).resolve().parents[1] / "vector_store" / "chroma")
CHROMA_COLLECTION = "academic_document_chunks"
TIMEZONE = ZoneInfo("Asia/Seoul")


def to_millis(value):
    return int(value.timestamp() * 1000)


def academic_year_range(year):
    start = datetime.datetime(year, 3, 1, 0, 0, 0, 0, tzinfo=TIMEZONE)
    end = datetime.datetime(year + 1, 2, 28, 23, 59, 59, 999000, tzinfo=TIMEZONE)
    return to_millis(start), to_millis(end)


def format_date(timestamp_millis):
    value = datetime.datetime.fromtimestamp(int(timestamp_millis) / 1000, tz=TIMEZONE)
    return value.strftime("%Y.%m.%d")


def fetch_events(year, group_id):
    start_time, end_time = academic_year_range(year)
    url = f"{API_BASE_URL}/{group_id}/{start_time}/{end_time}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; DKU-RAG-Calendar-Ingest/1.0)",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload.get("status"):
        raise RuntimeError(f"calendar API returned failure: {url}")
    return payload.get("data", [])


def event_text(event, year):
    title = event.get("title", "").strip()
    content = event.get("content", "").strip()
    start_date = format_date(event.get("startTime"))
    end_date = format_date(event.get("endTime"))
    period = start_date if start_date == end_date else f"{start_date} ~ {end_date}"
    lines = [
        f"{year}학년도 학사일정",
        f"일정명: {title}",
        f"기간: {period}",
        f"분류: {event.get('calendar', '학사일정')}",
    ]
    if content:
        lines.append(f"내용: {content}")
    return "\n".join(lines)


def event_id(event, year, index):
    title = event.get("title", "").strip()
    start = event.get("startTime", "")
    end = event.get("endTime", "")
    return f"dku_academic_calendar_{year}_{start}_{end}_{index}_{abs(hash(title))}"


def ingest_years(years, group_ids):
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(CHROMA_COLLECTION)

    total = 0
    for year in years:
        merged_events = []
        for group_id in group_ids:
            events = fetch_events(year, group_id)
            print(f"{year} group {group_id}: {len(events)} events", flush=True)
            merged_events.extend(events)

        seen = set()
        documents = []
        ids = []
        metadatas = []
        for index, event in enumerate(merged_events):
            key = (event.get("title", ""), event.get("startTime", ""), event.get("endTime", ""))
            if key in seen:
                continue
            seen.add(key)

            text = event_text(event, year)
            item_id = event_id(event, year, index)
            start_date = format_date(event.get("startTime"))
            end_date = format_date(event.get("endTime"))
            documents.append(text)
            ids.append(item_id)
            metadatas.append(
                {
                    "title": event.get("title", "학사일정"),
                    "source_url": BASE_URL,
                    "document_id": f"dku_academic_calendar_{year}",
                    "chunk_id": item_id,
                    "date": start_date,
                    "end_date": end_date,
                    "year": str(year),
                    "kind": "academic_calendar",
                }
            )

        if not documents:
            continue

        embeddings = model.encode(documents, normalize_embeddings=True, show_progress_bar=False).tolist()
        collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        total += len(documents)
        print(f"{year}: upserted {len(documents)} academic calendar events", flush=True)

    print(f"Done: upserted {total} academic calendar events", flush=True)
    print(f"Current collection chunk count: {collection.count()}", flush=True)


def parse_years(value):
    years = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            years.extend(range(int(start), int(end) + 1))
        else:
            years.append(int(part))
    return sorted(set(years))


def main():
    parser = argparse.ArgumentParser(description="단국대학교 학사일정을 RAG Chroma DB에 추가합니다.")
    parser.add_argument("--years", default="2026", help="예: 2026 또는 2023-2026 또는 2025,2026")
    parser.add_argument("--group-ids", default="0,20118", help="캘린더 API group id 목록")
    args = parser.parse_args()

    years = parse_years(args.years)
    group_ids = [item.strip() for item in args.group_ids.split(",") if item.strip()]
    ingest_years(years, group_ids)


if __name__ == "__main__":
    main()
