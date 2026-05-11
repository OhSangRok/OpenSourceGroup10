from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import mysql.connector
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

# JWT 설정
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# MySQL 연결
db = mysql.connector.connect(
    host="localhost",
    user="root",
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
    return {"message": "백엔드 서버 실행 성공"}

# 회원가입 API
@app.post("/register")
def register(user: UserRegister):

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