import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4321",
    database="school_event_db"
)

print("MySQL 연결 성공!")