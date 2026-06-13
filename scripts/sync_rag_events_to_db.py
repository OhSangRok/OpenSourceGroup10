import argparse
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import chromadb
import mysql.connector


ROOT = Path(__file__).resolve().parents[1]
CHROMA_PATH = os.getenv("CHROMA_PATH", str(ROOT / "vector_store" / "chroma"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "academic_document_chunks")


def load_map_buildings():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    pattern = re.compile(
        r"building_id:\s*(\d+),\s*name:\s*\"([^\"]+)\",\s*lat:\s*([0-9.]+),\s*lng:\s*([0-9.]+),\s*info:\s*\"([^\"]*)\""
    )
    buildings = []
    for match in pattern.finditer(index_html):
        buildings.append({
            "building_id": int(match.group(1)),
            "building_name": match.group(2).replace(" ", ""),
            "display_name": match.group(2),
            "latitude": float(match.group(3)),
            "longitude": float(match.group(4)),
            "description": match.group(5),
        })
    return buildings


def normalize_text(value):
    return re.sub(r"\s+", "", str(value or "")).lower()


def group_documents(collection):
    data = collection.get(include=["documents", "metadatas"])
    grouped = {}
    for item_id, document, metadata in zip(
        data.get("ids", []),
        data.get("documents", []),
        data.get("metadatas", []),
    ):
        doc_id = metadata.get("document_id") or item_id.rsplit("_chunk_", 1)[0]
        grouped.setdefault(doc_id, {
            "ids": [],
            "documents": [],
            "metadata": metadata,
        })
        grouped[doc_id]["ids"].append(item_id)
        grouped[doc_id]["documents"].append(document or "")
    return grouped.values()


def extract_year(*values):
    for value in values:
        match = re.search(r"(20\d{2})", str(value or ""))
        if match:
            return int(match.group(1))
    return None


def parse_date(text, fallback_year):
    text = str(text or "")
    match = re.search(r"(20\d{2})[.\-/년]\s*(\d{1,2})[.\-/월]\s*(\d{1,2})", text)
    if match:
        year, month, day = map(int, match.groups())
        try:
            return datetime(year, month, day)
        except ValueError:
            return None

    match = re.search(r"(\d{1,2})[.\-/월]\s*(\d{1,2})\s*일?", text)
    if match and fallback_year:
        month, day = map(int, match.groups())
        try:
            return datetime(fallback_year, month, day)
        except ValueError:
            return None

    return None


def extract_time(text):
    text = str(text or "")
    match = re.search(r"(오전|오후)\s*(\d{1,2})\s*시(?:\s*(\d{1,2})\s*분?)?", text)
    if match:
        hour = int(match.group(2))
        minute = int(match.group(3) or 0)
        if match.group(1) == "오후" and hour < 12:
            hour += 12
        if match.group(1) == "오전" and hour == 12:
            hour = 0
        return hour, minute

    match = re.search(r"(?<!\d)([01]?\d|2[0-3])[:시]\s*([0-5]\d)?", text)
    if match:
        return int(match.group(1)), int(match.group(2) or 0)

    return None


def extract_event_datetime(text, metadata, require_time):
    fallback_year = extract_year(metadata.get("year"), metadata.get("date"), text)
    base = parse_date(text, fallback_year)
    if not base:
        return None

    time_value = extract_time(text)
    if not time_value and require_time:
        return None

    hour, minute = time_value or (0, 0)
    return base.replace(hour=hour, minute=minute, second=0, microsecond=0)


def clean_document_text(text):
    lines = []
    for line in str(text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith(("분류:", "작성자:", "날짜:")):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def parse_filter_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("날짜는 YYYY-MM-DD 형식으로 입력해주세요.") from error


def find_building(text, buildings):
    normalized = normalize_text(text)
    matches = []
    for building in buildings:
        name = building["building_name"]
        if name and name in normalized:
            matches.append((len(name), building))
    if not matches:
        return None
    return sorted(matches, key=lambda item: item[0], reverse=True)[0][1]


def ensure_buildings(cursor, buildings, apply):
    for building in buildings:
        cursor.execute(
            """
            SELECT building_id
            FROM buildings
            WHERE building_id = %s
            """,
            (building["building_id"],),
        )
        if cursor.fetchone():
            continue

        if apply:
            cursor.execute(
                """
                INSERT INTO buildings
                (building_id, building_name, latitude, longitude, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    building["building_id"],
                    building["display_name"],
                    building["latitude"],
                    building["longitude"],
                    building["description"],
                ),
            )


def event_exists(cursor, title, building_id, start_datetime):
    cursor.execute(
        """
        SELECT event_id
        FROM events
        WHERE title = %s
          AND building_id = %s
          AND start_datetime = %s
        LIMIT 1
        """,
        (title, building_id, start_datetime),
    )
    return cursor.fetchone() is not None


def sync_events(args):
    buildings = load_map_buildings()
    from_date = parse_filter_date(args.from_date) if args.from_date else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    to_date = parse_filter_date(args.to_date).replace(hour=23, minute=59, second=59) if args.to_date else None
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(CHROMA_COLLECTION)

    db = mysql.connector.connect(
        host=args.db_host,
        user=args.db_user,
        password=args.db_password,
        database=args.db_name,
    )
    cursor = db.cursor()

    apply = not args.dry_run
    ensure_buildings(cursor, buildings, apply)

    inserted = 0
    skipped = 0
    candidates = 0

    for item in group_documents(collection):
        metadata = item["metadata"]
        title = metadata.get("title", "제목 없음").strip()
        text = clean_document_text("\n".join(item["documents"]))
        search_text = "\n".join([title, text])

        building = find_building(search_text, buildings)
        start_datetime = extract_event_datetime(search_text, metadata, args.require_time)
        if not building or not start_datetime:
            skipped += 1
            continue
        if start_datetime < from_date or (to_date and start_datetime > to_date):
            skipped += 1
            continue

        candidates += 1
        end_datetime = start_datetime + timedelta(hours=args.default_hours)
        source_url = metadata.get("source_url", "")
        description = text.strip()
        if source_url and source_url not in description:
            description = f"{description}\n\n원문: {source_url}"

        if event_exists(cursor, title, building["building_id"], start_datetime):
            skipped += 1
            continue

        print(
            f"{'[WRITE]' if apply else '[DRY]'} {building['display_name']} | "
            f"{start_datetime:%Y-%m-%d %H:%M} | {title}",
            flush=True,
        )

        if apply:
            cursor.execute(
                """
                INSERT INTO events
                (title, description, building_id, college, department, start_datetime, end_datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    title[:100],
                    description,
                    building["building_id"],
                    None,
                    "RAG",
                    start_datetime,
                    end_datetime,
                ),
            )
            inserted += 1

    if apply:
        db.commit()

    cursor.close()
    db.close()
    print(
        f"Done: candidates={candidates}, inserted={inserted}, skipped={skipped}, dry_run={args.dry_run}",
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser(description="RAG Chroma 문서에서 건물 행사 정보를 추출해 MySQL events에 저장합니다.")
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-user", default="school_app")
    parser.add_argument("--db-password", default="4321")
    parser.add_argument("--db-name", default="school_event_db")
    parser.add_argument("--default-hours", type=float, default=1.0)
    parser.add_argument("--from-date", default=None, help="이 날짜 이후 일정만 저장합니다. 기본값은 오늘입니다. 예: 2026-06-14")
    parser.add_argument("--to-date", default=None, help="이 날짜까지의 일정만 저장합니다. 예: 2026-12-31")
    parser.add_argument("--require-time", action="store_true", help="시간이 명시된 문서만 저장합니다.")
    parser.add_argument("--dry-run", action="store_true", help="DB에 저장하지 않고 추출 결과만 출력합니다.")
    args = parser.parse_args()
    sync_events(args)


if __name__ == "__main__":
    main()
