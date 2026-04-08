import pymysql
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'finalproject'
}

def seed():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Clean tables safely due to newly enabled CASCADE
    cursor.execute("DELETE FROM users")
    
    # 1. Register Manager
    pw1 = bcrypt.generate_password_hash('password').decode('utf-8')
    cursor.execute("INSERT INTO users (username, email, password, role) VALUES ('Manager', 'testmanager@example.com', %s, 'manager')", (pw1,))
    
    # 2. Register HOD
    pw2 = bcrypt.generate_password_hash('password').decode('utf-8')
    cursor.execute("INSERT INTO users (username, email, password, role) VALUES ('HOD', 'testhod@example.com', %s, 'hod')", (pw2,))
    
    # 3. Register Student
    pw3 = bcrypt.generate_password_hash('password').decode('utf-8')
    cursor.execute("INSERT INTO users (username, email, password, role) VALUES ('Student', 'test_student@example.com', %s, 'student')", (pw3,))
    student_user_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO students (user_id, name, usn, department, semester, email, fee_status) VALUES (%s, 'Test Student', '1RV18CS000', 'Computer Science', 6, 'test_student@example.com', 'Paid')", (student_user_id,))
    student_id = cursor.lastrowid
    
    # Inject diverse dummy requests to ensure frontend dashboard math filters behave accurately
    cursor.execute("INSERT INTO requests (student_id, request_type, reason, status) VALUES (%s, 'Study Certificate', 'Test Logic', 'PENDING_MANAGER')", (student_id,))
    cursor.execute("INSERT INTO requests (student_id, request_type, reason, status) VALUES (%s, 'Scholarship', 'Test Logic', 'APPROVED')", (student_id,))
    cursor.execute("INSERT INTO requests (student_id, request_type, reason, status) VALUES (%s, 'Bus Pass', 'Test Logic', 'REJECTED')", (student_id,))
    cursor.execute("INSERT INTO requests (student_id, request_type, reason, status) VALUES (%s, 'Bus Pass', 'Test Logic 4', 'REJECTED')", (student_id,))

    conn.commit()
    conn.close()
    print("Database officially seeded with Student, Manager, HOD and request testing metrics!")

if __name__ == "__main__":
    seed()
