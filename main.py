from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error, IntegrityError
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
import os
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

import chromadb
from contextlib import contextmanager

app = FastAPI()
security = HTTPBearer()

# JWT 설정
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

DB_CONFIG = {
    "host": "localhost",
    "user": "school_app",
    "password": "4321",
    "database": "school_event_db"
}
# helper: create a fresh connection per request
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def get_cursor(commit: bool = False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    str(Path(__file__).resolve().parent / "vector_store" / "chroma")
)
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "academic_document_chunks")




def get_index_buildings():
    html_text = (Path(__file__).resolve().parent / "index.html").read_text(encoding="utf-8")
    pattern = re.compile(
        r'building_id:\s*(\d+),\s*name:\s*"([^"]+)",\s*lat:\s*([0-9.]+),\s*lng:\s*([0-9.]+),\s*info:\s*"([^"]*)"'
    )
    buildings = []
    for match in pattern.finditer(html_text):
        buildings.append({
            "building_id": int(match.group(1)),
            "building_name": match.group(2),
            "latitude": float(match.group(3)),
            "longitude": float(match.group(4)),
            "description": match.group(5)
        })
    return buildings


# 회원가입 데이터 형식
class UserRegister(BaseModel):
    student_id: str
    password: str
    name: str
    college: str
    department: str
    grade: int

# 로그인 데이터 형식
class UserLogin(BaseModel):
    student_id: str
    password: str

#행사 데이터 형식
class EventCreate(BaseModel):
    title: str
    description: str
    building_id: int
    college: str
    department: str
    start_datetime: datetime
    end_datetime: datetime

# 챗봇 질문 데이터 형식
class ChatRequest(BaseModel):
    question: str

# 개인 일정 데이터 형식
class PersonalScheduleCreate(BaseModel):
    title: str
    schedule_date: str
    schedule_time: str = ""
    building_id: int | None = None
    memo: str = ""


def ensure_personal_schedules_table():
    create_sql = """
    CREATE TABLE IF NOT EXISTS personal_schedules (
        schedule_id INT NOT NULL AUTO_INCREMENT,
        student_id VARCHAR(20) NOT NULL,
        title VARCHAR(100) NOT NULL,
        schedule_date DATE NOT NULL,
        schedule_time TIME DEFAULT NULL,
        building_id INT DEFAULT NULL,
        memo TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (schedule_id),
        KEY student_id (student_id),
        KEY building_id (building_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """
    with get_cursor(commit=True) as cur:
        cur.execute(create_sql)
        cur.execute("SHOW COLUMNS FROM personal_schedules")
        columns = {row[0] for row in cur.fetchall()}
        if "schedule_time" not in columns:
            cur.execute("ALTER TABLE personal_schedules ADD COLUMN schedule_time TIME DEFAULT NULL AFTER schedule_date")
        if "building_id" not in columns:
            cur.execute("ALTER TABLE personal_schedules ADD COLUMN building_id INT DEFAULT NULL AFTER schedule_time")
        if "created_at" not in columns:
            cur.execute("ALTER TABLE personal_schedules ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")

# JWT 토큰 생성 함수
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# JWT 토큰 검증 함수
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        student_id = payload.get("student_id")

        if student_id is None:
            raise HTTPException(status_code=401, detail="토큰 정보가 잘못되었습니다.")

        return student_id

    except Exception:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
# 관리자 권한 확인 함수
def verify_admin(student_id: str = Depends(verify_token)):

    sql = """
    SELECT is_admin
    FROM users
    WHERE student_id = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (student_id,))
        result = cur.fetchone()

    if result is None or result[0] != 1:
        raise HTTPException(
            status_code=403,
            detail="관리자만 사용할 수 있는 기능입니다."
        )

    return student_id


# RAG 챗봇 API
@app.post("/api/chat")
def chat_with_rag(chat: ChatRequest):
    question = chat.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    rag_server_url = os.getenv("RAG_SERVER_URL", "http://127.0.0.1:8001/answer")
    payload = json.dumps({"question": question}).encode("utf-8")

    request = urllib.request.Request(
        rag_server_url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "question": question,
                "answer": data.get("answer", "응답이 없습니다."),
                "sources": data.get("sources", [])
            }
    except urllib.error.URLError as error:
        raise HTTPException(
            status_code=502,
            detail=f"RAG 서버에 연결하지 못했습니다: {error}"
        )

# 기본 페이지
@app.get("/")
def home():
    return FileResponse("index.html", headers={"Cache-Control": "no-store"})


# 챗봇 페이지
@app.get("/chatbot")
def chatbot_page():
    return FileResponse("chatbot.html", headers={"Cache-Control": "no-store"})

# 이벤트 페이지
@app.get("/event")
def event_page():
    return FileResponse("event.html", headers={"Cache-Control": "no-store"})

# 개인 페이지
@app.get("/mypage")
def mypage_page():
    return FileResponse("mypage.html", headers={"Cache-Control": "no-store"})

# 로그인 페이지
@app.get("/login")
def login_page():
    return FileResponse("login.html")


# 회원가입 페이지
@app.get("/register")
def register_page():
    return FileResponse("register.html")

# 회원가입 API
@app.post("/register")
def register(user: UserRegister):

    if (
        not user.student_id.strip()
        or not user.password.strip()
        or not user.name.strip()
        or not user.college.strip()
        or (user.college != "퇴계혁신칼리지" and not user.department.strip())
        or user.grade < 1
        or user.grade > 4
    ):
        raise HTTPException(
            status_code=400,
            detail="모든 항목을 올바르게 입력해주세요."
        )

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    sql = """
    INSERT INTO users
    (student_id, password_hash, name, college, department, grade)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        user.student_id,
        hashed_password.decode("utf-8"),
        user.name,
        user.college,
        user.department,
        user.grade
    )

    try:
        with get_cursor(commit=True) as cur:
            cur.execute(sql, values)
    except IntegrityError:
        
        raise HTTPException(
            status_code=409,
            detail="이미 가입된 학번입니다."
        )
    except Error as error:
        
        raise HTTPException(
            status_code=500,
            detail=f"회원가입 처리 중 DB 오류가 발생했습니다: {error}"
        )

    return {"message": "회원가입 성공!"}

# 로그인 API
@app.post("/login")
def login(user: UserLogin):

    sql = """
    SELECT password_hash, name
    FROM users
    WHERE student_id = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (user.student_id,))
        result = cur.fetchone()

    if result is None:
        return {"message": "존재하지 않는 학번입니다."}

    password_hash = result[0]
    name = result[1]

    if bcrypt.checkpw(
        user.password.encode("utf-8"),
        password_hash.encode("utf-8")
    ):
        access_token = create_access_token(
            data={"student_id": user.student_id}
        )

        return {
            "message": "로그인 성공!",
            "name": name,
            "access_token": access_token,
            "token_type": "bearer"
        }

    else:
        return {"message": "비밀번호가 틀렸습니다."}

# 내 정보 조회 API
@app.get("/me")
def get_me(student_id: str = Depends(verify_token)):
    sql = """
    SELECT student_id, name, college, department, grade
    FROM users
    WHERE student_id = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (student_id,))
        result = cur.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return {
        "student_id": result[0],
        "name": result[1],
        "college": result[2],
        "department": result[3],
        "grade": result[4]
    }

# 전체 건물 조회 API
@app.get("/buildings")
def get_buildings():
    return get_index_buildings()

# 전체 행사 조회 API
@app.get("/events")
def get_events():

    sql = """
    SELECT *
    FROM events
    """
    with get_cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()

    events = []

    for row in results:
        events.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7]
        })

    return events


def parse_date_value(value, fallback_year=None):
    if not value:
        return None

    text = str(value).strip()
    match = re.search(r"(20\d{2})[.\-/년]\s*(\d{1,2})[.\-/월]\s*(\d{1,2})", text)
    if match:
        try:
            return datetime(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            ).date()
        except ValueError:
            return None

    match = re.search(r"(\d{1,2})[.\-/월]\s*(\d{1,2})", text)
    if match and fallback_year:
        try:
            return datetime(
                int(fallback_year),
                int(match.group(1)),
                int(match.group(2))
            ).date()
        except ValueError:
            return None

    return None


def extract_year_from_text(*values):
    for value in values:
        match = re.search(r"(20\d{2})", str(value or ""))
        if match:
            return int(match.group(1))
    return datetime.now().year


def extract_date_ranges(text, fallback_year):
    ranges = []
    if not text:
        return ranges

    range_pattern = re.compile(
        r"((?:20\d{2}[.\-/년]\s*)?\d{1,2}[.\-/월]\s*\d{1,2})\s*(?:~|-|부터|～|∼)\s*((?:20\d{2}[.\-/년]\s*)?\d{1,2}[.\-/월]\s*\d{1,2})"
    )
    for start_text, end_text in range_pattern.findall(text):
        start_date = parse_date_value(start_text, fallback_year)
        end_date = parse_date_value(end_text, fallback_year)
        if start_date and end_date:
            if end_date < start_date:
                end_date = datetime(end_date.year + 1, end_date.month, end_date.day).date()
            ranges.append((start_date, end_date))

    single_pattern = re.compile(r"(20\d{2}[.\-/년]\s*\d{1,2}[.\-/월]\s*\d{1,2})")
    for date_text in single_pattern.findall(text):
        date_value = parse_date_value(date_text, fallback_year)
        if date_value:
            ranges.append((date_value, date_value))

    return ranges


def source_type_from_metadata(metadata):
    document_id = str(metadata.get("document_id", ""))
    source_url = metadata.get("source_url", "")
    kind = metadata.get("kind", "")

    if kind == "academic_calendar":
        return "학사일정"
    if "apply_noti" in document_id or "apply_noti" in source_url:
        return "채용공지"
    if "bid" in document_id or "/bid" in source_url:
        return "입찰공고"
    return "공지"


def build_event_description(document, title, metadata):
    lines = []
    for line in str(document or "").splitlines():
        line = line.strip()
        if not line:
            lines.append("")
            continue
        if line == title:
            continue
        if metadata.get("kind") == "academic_calendar" and line.startswith("분류:"):
            continue
        lines.append(line)

    return "\n".join(lines).strip()


def get_today_vector_events(today):
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_collection(CHROMA_COLLECTION)
        data = collection.get(include=["documents", "metadatas"])
    except Exception:
        return []

    vector_events = []
    seen = set()

    for item_id, document, metadata in zip(data.get("ids", []), data.get("documents", []), data.get("metadatas", [])):
        title = metadata.get("title", "제목 없음")
        source_url = metadata.get("source_url", "")
        fallback_year = extract_year_from_text(metadata.get("year", ""), metadata.get("date", ""), title, document)

        ranges = []
        start_date = parse_date_value(metadata.get("date", ""), fallback_year)
        end_date = parse_date_value(metadata.get("end_date", ""), fallback_year) or start_date
        if start_date and end_date:
            ranges.append((start_date, end_date))

        ranges.extend(extract_date_ranges(document, fallback_year))
        if not ranges:
            continue

        for start_date, end_date in ranges:
            if start_date <= today <= end_date:
                key = (title, source_url, start_date, end_date)
                if key in seen:
                    continue
                seen.add(key)
                vector_events.append({
                    "event_id": f"vector-{item_id}",
                    "title": title,
                    "description": build_event_description(document, title, metadata),
                    "building_id": None,
                    "college": None,
                    "department": source_type_from_metadata(metadata),
                    "start_datetime": datetime.combine(start_date, datetime.min.time()),
                    "end_datetime": datetime.combine(end_date, datetime.max.time()).replace(microsecond=0),
                    "source_url": source_url,
                    "source_type": source_type_from_metadata(metadata)
                })
                break

    return vector_events


# 오늘 진행되는 행사 조회 API
@app.get("/events/today")
def get_today_events():

    sql = """
    SELECT *
    FROM events
    WHERE DATE(start_datetime) <= CURDATE()
      AND DATE(end_datetime) >= CURDATE()
    ORDER BY start_datetime ASC
    """

    with get_cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()

    events = []

    for row in results:
        events.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7]
        })

    today = datetime.now().date()
    events.extend(get_today_vector_events(today))
    events.sort(key=lambda item: (item["start_datetime"], item["title"]))

    return events

# 특정 건물 행사 조회 API
@app.get("/events/building/{building_id}")
def get_building_events(building_id: int):

    sql = """
    SELECT *
    FROM events
    WHERE building_id = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (building_id,))
        results = cur.fetchall()

    events = []

    for row in results:
        events.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7]
        })

    return events

# 행사 즐겨찾기 추가 API
@app.post("/favorites/{event_id}")
def add_favorite(
    event_id: int,
    student_id: str = Depends(verify_token)
):

    sql = """
    INSERT INTO favorite_events
    (student_id, event_id)
    VALUES (%s, %s)
    """

    values = (student_id, event_id)

    try:
        with get_cursor(commit=True) as cur:
            cur.execute(sql, values)
        return {"message": "즐겨찾기 추가 성공!"}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="이미 즐겨찾기한 행사입니다."
        )
    
# 내 즐겨찾기 조회 API
@app.get("/favorites")
def get_favorites(student_id: str = Depends(verify_token)):

    sql = """
    SELECT 
        events.event_id,
        events.title,
        events.description,
        events.building_id,
        events.college,
        events.department,
        events.start_datetime,
        events.end_datetime,
        buildings.building_name
    FROM favorite_events
    JOIN events
    ON favorite_events.event_id = events.event_id
    LEFT JOIN buildings
    ON events.building_id = buildings.building_id
    WHERE favorite_events.student_id = %s
    ORDER BY favorite_events.created_at DESC, favorite_events.favorite_id DESC
    """

    with get_cursor() as cur:
        cur.execute(sql, (student_id,))
        results = cur.fetchall()

    favorites = []

    for row in results:
        favorites.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7],
            "building_name": row[8]
        })

    return favorites

# 개인 일정 조회 API
@app.get("/personal-schedules")
def get_personal_schedules(
    student_id: str = Depends(verify_token)
):
    ensure_personal_schedules_table()
    sql = """
    SELECT
        personal_schedules.schedule_id,
        personal_schedules.title,
        personal_schedules.schedule_date,
        personal_schedules.schedule_time,
        personal_schedules.building_id,
        buildings.building_name,
        personal_schedules.memo
    FROM personal_schedules
    LEFT JOIN buildings
    ON personal_schedules.building_id = buildings.building_id
    WHERE personal_schedules.student_id = %s
    ORDER BY personal_schedules.schedule_date ASC, personal_schedules.schedule_time ASC, personal_schedules.schedule_id ASC
    """

    with get_cursor() as cur:
        cur.execute(sql, (student_id,))
        results = cur.fetchall()

    schedules = []

    for row in results:
        schedules.append({
            "schedule_id": row[0],
            "title": row[1],
            "schedule_date": row[2],
            "schedule_time": str(row[3]) if row[3] else "",
            "building_id": row[4],
            "building_name": row[5],
            "memo": row[6]
        })

    return schedules


# 개인 일정 추가 API
@app.post("/personal-schedules")
def create_personal_schedule(
    schedule: PersonalScheduleCreate,
    student_id: str = Depends(verify_token)
):
    ensure_personal_schedules_table()
    if not schedule.title.strip() or not schedule.schedule_date.strip():
        raise HTTPException(
            status_code=400,
            detail="일정 제목과 날짜를 입력해주세요."
        )

    sql = """
    INSERT INTO personal_schedules
    (student_id, title, schedule_date, schedule_time, building_id, memo)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    schedule_time = schedule.schedule_time.strip() or None

    values = (
        student_id,
        schedule.title.strip(),
        schedule.schedule_date,
        schedule_time,
        schedule.building_id,
        schedule.memo.strip()
    )

    try:
        with get_cursor(commit=True) as cur:
            cur.execute(sql, values)

        return {"message": "일정 추가 성공!"}

    except Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"개인 일정 추가 중 DB 오류가 발생했습니다: {error}"
        )


# 개인 일정 삭제 API
@app.delete("/personal-schedules/{schedule_id}")
def delete_personal_schedule(
    schedule_id: int,
    student_id: str = Depends(verify_token)
):
    ensure_personal_schedules_table()
    sql = """
    DELETE FROM personal_schedules
    WHERE schedule_id = %s
    AND student_id = %s
    """

    with get_cursor(commit=True) as cur:
        cur.execute(sql, (schedule_id, student_id))
        rowcount = cur.rowcount

    if rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="일정을 찾을 수 없습니다."
        )

    return {"message": "일정 삭제 성공!"}
    
# 일정 알림 조회 API
# 일정 알림 조회 API
@app.get("/notifications")
def get_notifications(student_id: str = Depends(verify_token)):
    ensure_personal_schedules_table()

    favorite_sql = """
    SELECT 
        events.event_id,
        events.title,
        events.description,
        events.start_datetime,
        events.end_datetime,
        buildings.building_name
    FROM favorite_events
    JOIN events
    ON favorite_events.event_id = events.event_id
    LEFT JOIN buildings
    ON events.building_id = buildings.building_id
    WHERE favorite_events.student_id = %s
    AND events.start_datetime BETWEEN DATE_ADD(UTC_TIMESTAMP(), INTERVAL 9 HOUR)
    AND DATE_ADD(DATE_ADD(UTC_TIMESTAMP(), INTERVAL 9 HOUR), INTERVAL 1 DAY)
    ORDER BY events.start_datetime ASC
    """

    personal_sql = """
    SELECT
        personal_schedules.schedule_id,
        personal_schedules.title,
        personal_schedules.schedule_date,
        personal_schedules.schedule_time,
        personal_schedules.memo,
        buildings.building_name
    FROM personal_schedules
    LEFT JOIN buildings
    ON personal_schedules.building_id = buildings.building_id
    WHERE personal_schedules.student_id = %s
    AND TIMESTAMP(
        personal_schedules.schedule_date,
        IFNULL(personal_schedules.schedule_time, '00:00:00')
    ) BETWEEN DATE_ADD(UTC_TIMESTAMP(), INTERVAL 9 HOUR)
    AND DATE_ADD(DATE_ADD(UTC_TIMESTAMP(), INTERVAL 9 HOUR), INTERVAL 1 DAY)
    ORDER BY personal_schedules.schedule_date ASC, personal_schedules.schedule_time ASC
    """

    notifications = []

    with get_cursor() as cur:
        cur.execute(favorite_sql, (student_id,))
        favorite_results = cur.fetchall()
        print("FAVORITE_RESULTS =", favorite_results)

        cur.execute(personal_sql, (student_id,))
        personal_results = cur.fetchall()
        print("PERSONAL_RESULTS =", personal_results)

    for row in favorite_results:
        start_dt = row[3]
        end_dt = row[4]

        remaining_minutes = int((start_dt - datetime.now()).total_seconds() // 60)

        notifications.append({
            "type": "favorite_event",
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "start_datetime": start_dt,
            "end_datetime": end_dt,
            "building_name": row[5],
            "remaining_minutes": remaining_minutes,
            "message": "곧 시작하는 즐겨찾기 행사입니다."
        })

    for row in personal_results:
        schedule_date = row[2]
        schedule_time = row[3]

        if schedule_time:
            start_dt = datetime.combine(schedule_date, datetime.min.time()) + schedule_time
        else:
            start_dt = datetime.combine(schedule_date, datetime.min.time())

        remaining_minutes = int((start_dt - datetime.now()).total_seconds() // 60)

        notifications.append({
            "type": "personal_schedule",
            "id": row[0],
            "title": row[1],
            "description": row[4],
            "start_datetime": start_dt,
            "end_datetime": start_dt,
            "building_name": row[5],
            "remaining_minutes": remaining_minutes,
            "message": "곧 시작하는 개인 일정입니다."
        })

    notifications.sort(key=lambda item: item["start_datetime"])

    return notifications

# 즐겨찾기 삭제 API
@app.delete("/favorites/{event_id}")
def delete_favorite(
    event_id: int,
    student_id: str = Depends(verify_token)
):

    sql = """
    DELETE FROM favorite_events
    WHERE student_id = %s
    AND event_id = %s
    """

    with get_cursor(commit=True) as cur:
        cur.execute(sql, (student_id, event_id))
        rowcount = cur.rowcount

    if rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="즐겨찾기한 행사가 아닙니다."
        )

    return {"message": "즐겨찾기 삭제 성공!"}

# 전체 버스 정류장 조회 API
@app.get("/bus-stops")
def get_bus_stops():

    sql = """
    SELECT *
    FROM bus_stops
    """
    with get_cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()

    bus_stops = []

    for row in results:
        bus_stops.append({
            "stop_id": row[0],
            "stop_name": row[1],
            "latitude": float(row[2]),
            "longitude": float(row[3]),
            "description": row[4]
        })

    return bus_stops

# 특정 정류장 시간표 조회 API
@app.get("/bus-stops/{stop_id}/schedules")
def get_bus_schedules(stop_id: int):

    sql = """
    SELECT *
    FROM bus_schedules
    WHERE stop_id = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (stop_id,))
        results = cur.fetchall()

    schedules = []

    for row in results:
        schedules.append({
            "schedule_id": row[0],
            "stop_id": row[1],
            "bus_number": row[2],
            "arrival_time": str(row[3]),
            "weekday_type": row[4]
        })

    return schedules

# 현재 시간 기준 다음 버스 조회 API
@app.get("/bus-stops/{stop_id}/next-buses")
def get_next_buses(stop_id: int):

    now = datetime.utcnow() + timedelta(hours=9)

    sql = """
    SELECT bus_number, arrival_time
    FROM bus_schedules
    WHERE stop_id = %s
    ORDER BY arrival_time ASC
    """

    with get_cursor() as cur:
        cur.execute(sql, (stop_id,))
        results = cur.fetchall()

    buses = []

    for row in results:
        bus_number = row[0]
        arrival_time = row[1]

        arrival_datetime = datetime.combine(datetime.today(), datetime.min.time()) + arrival_time

        remaining_minutes = int((arrival_datetime - now).total_seconds() / 60)

        if remaining_minutes >= 0:
            buses.append({
                "bus_number": bus_number,
                "arrival_time": str(arrival_time),
                "remaining_minutes": remaining_minutes
            })

    return buses

# 행사 추가 API
@app.post("/events")
def create_event(
    event: EventCreate,
    admin_id: str = Depends(verify_admin)
):

    sql = """
    INSERT INTO events
    (title, description, building_id, college, department, start_datetime, end_datetime)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        event.title,
        event.description,
        event.building_id,
        event.college,
        event.department,
        event.start_datetime,
        event.end_datetime
    )

    with get_cursor(commit=True) as cur:
        cur.execute(sql, values)

    return {"message": "행사 추가 성공!"}

# 행사 삭제 API
@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    admin_id: str = Depends(verify_admin)
):

    sql = """
    DELETE FROM events
    WHERE event_id = %s
    """

    with get_cursor(commit=True) as cur:
        cur.execute(sql, (event_id,))
        rowcount = cur.rowcount

    if rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="행사를 찾을 수 없습니다."
        )

    return {"message": "행사 삭제 성공!"}

# 행사 수정 API
@app.put("/events/{event_id}")
def update_event(
    event_id: int,
    event: EventCreate,
    admin_id: str = Depends(verify_admin)
):

    sql = """
    UPDATE events
    SET title = %s,
        description = %s,
        building_id = %s,
        college = %s,
        department = %s,
        start_datetime = %s,
        end_datetime = %s
    WHERE event_id = %s
    """

    values = (
        event.title,
        event.description,
        event.building_id,
        event.college,
        event.department,
        event.start_datetime,
        event.end_datetime,
        event_id
    )

    with get_cursor(commit=True) as cur:
        cur.execute(sql, values)
        rowcount = cur.rowcount

    if rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="행사를 찾을 수 없습니다."
        )

    return {"message": "행사 수정 성공!"}

# 전체 셔틀버스 정류장 조회 API
@app.get("/shuttle-stops")
def get_shuttle_stops():

    sql = """
    SELECT DISTINCT
        bus_stops.stop_id,
        bus_stops.stop_name,
        bus_stops.latitude,
        bus_stops.longitude,
        bus_stops.description
    FROM bus_stops
    JOIN shuttle_schedules
    ON bus_stops.stop_id = shuttle_schedules.stop_id
    """

    with get_cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()

    shuttle_stops = []

    for row in results:
        shuttle_stops.append({
            "stop_id": row[0],
            "stop_name": row[1],
            "latitude": float(row[2]) if row[2] is not None else None,
            "longitude": float(row[3]) if row[3] is not None else None,
            "description": row[4]
        })

    return shuttle_stops

# 셔틀버스 시간표 조회 API
@app.get("/shuttle-stops/{stop_id}/schedules")
def get_shuttle_schedules(stop_id: int):
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM shuttle_schedules WHERE stop_id = %s",
            (stop_id,)
        )
        results = cur.fetchall()

    return [
        {
            "schedule_id": row[0],
            "stop_id": row[1],
            "shuttle_time": str(row[2])
        }
        for row in results
    ]

@app.get("/shuttle-stops/{stop_id}/next-shuttle")
def get_next_shuttle(stop_id: int):

    now = datetime.utcnow() + timedelta(hours=9)

    sql = """
    SELECT shuttle_time
    FROM shuttle_schedules
    WHERE stop_id = %s
    ORDER BY shuttle_time ASC
    """

    with get_cursor() as cur:
        cur.execute(sql, (stop_id,))
        results = cur.fetchall()

    for row in results:

        shuttle_time = row[0]

        shuttle_datetime = (
            datetime.combine(
                datetime.today(),
                datetime.min.time()
            )
            + shuttle_time
        )

        remaining_minutes = int(
            (shuttle_datetime - now).total_seconds() / 60
        )

        if remaining_minutes >= 0:

            return {
                "remaining_minutes": remaining_minutes
            }

    return {
        "remaining_minutes": None
    }

# 특정 단과대 행사 조회 API
@app.get("/events/college/{college}")
def get_college_events(college: str):

    sql = """
    SELECT *
    FROM events
    WHERE college = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (college,))
        results = cur.fetchall()

    events = []

    for row in results:
        events.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7]
        })

    return events


# 특정 학과 행사 조회 API
@app.get("/events/department/{department}")
def get_department_events(department: str):

    sql = """
    SELECT *
    FROM events
    WHERE department = %s
    """

    with get_cursor() as cur:
        cur.execute(sql, (department,))
        results = cur.fetchall()

    events = []

    for row in results:
        events.append({
            "event_id": row[0],
            "title": row[1],
            "description": row[2],
            "building_id": row[3],
            "college": row[4],
            "department": row[5],
            "start_datetime": row[6],
            "end_datetime": row[7]
        })

    return events
