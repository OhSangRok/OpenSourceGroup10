from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import mysql.connector
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi.responses import FileResponse

app = FastAPI()
security = HTTPBearer()

# JWT 설정
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# MySQL 연결
db = mysql.connector.connect(
    host="localhost",
    user="school_app",
    password="4321",
    database="school_event_db"
)

cursor = db.cursor()

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

# 기본 페이지
@app.get("/")
def home():
    return FileResponse("index.html")

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

    cursor.execute(sql, values)
    db.commit()

    return {"message": "회원가입 성공!"}

# 로그인 API
@app.post("/login")
def login(user: UserLogin):

    sql = """
    SELECT password_hash, name
    FROM users
    WHERE student_id = %s
    """

    cursor.execute(sql, (user.student_id,))
    result = cursor.fetchone()

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

    cursor.execute(sql, (student_id,))
    result = cursor.fetchone()

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

    sql = """
    SELECT *
    FROM buildings
    """

    cursor.execute(sql)

    results = cursor.fetchall()

    buildings = []

    for row in results:
        buildings.append({
            "building_id": row[0],
            "building_name": row[1],
            "latitude": float(row[2]),
            "longitude": float(row[3]),
            "description": row[4]
        })

    return buildings

# 전체 행사 조회 API
@app.get("/events")
def get_events():

    sql = """
    SELECT *
    FROM events
    """

    cursor.execute(sql)

    results = cursor.fetchall()

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

# 특정 건물 행사 조회 API
@app.get("/events/building/{building_id}")
def get_building_events(building_id: int):

    sql = """
    SELECT *
    FROM events
    WHERE building_id = %s
    """

    cursor.execute(sql, (building_id,))

    results = cursor.fetchall()

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
        cursor.execute(sql, values)
        db.commit()

        return {"message": "즐겨찾기 추가 성공!"}

    except:
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
        events.end_datetime
    FROM favorite_events
    JOIN events
    ON favorite_events.event_id = events.event_id
    WHERE favorite_events.student_id = %s
    """

    cursor.execute(sql, (student_id,))
    results = cursor.fetchall()

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
            "end_datetime": row[7]
        })

    return favorites

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

    cursor.execute(sql, (student_id, event_id))
    db.commit()

    if cursor.rowcount == 0:
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

    cursor.execute(sql)
    results = cursor.fetchall()

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

    cursor.execute(sql, (stop_id,))
    results = cursor.fetchall()

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

    cursor.execute(sql, (stop_id,))
    results = cursor.fetchall()

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

# 행사 삭제 API
@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    sql = """
    DELETE FROM events
    WHERE event_id = %s
    """

    cursor.execute(sql, (event_id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="행사를 찾을 수 없습니다."
        )

    return {"message": "행사 삭제 성공!"}

# 행사 수정 API
@app.put("/events/{event_id}")
def update_event(event_id: int, event: EventCreate):

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

    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="행사를 찾을 수 없습니다."
        )

    return {"message": "행사 수정 성공!"}