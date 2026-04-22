import sqlite3
from werkzeug.security import generate_password_hash
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,   -- admin / faculty / invigilator
    is_approved INTEGER DEFAULT 0,  -- 0 = pending, 1 = approved
    must_change_password INTEGER DEFAULT 0)
""")

# FACULTY PROFILE
cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    mobile TEXT,
    department TEXT,
    subjects TEXT,
    course_codes TEXT,
    address TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# INVIGILATOR PROFILE
cursor.execute("""
CREATE TABLE IF NOT EXISTS invigilator_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    mobile TEXT,
    department TEXT,
    address TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# PENDING FACULTY
cursor.execute("""
CREATE TABLE IF NOT EXISTS pending_faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    mobile TEXT,
    department TEXT,
    subjects TEXT,
    course_codes TEXT,
    address TEXT
)
""")

# PENDING INVIGILATOR
cursor.execute("""
CREATE TABLE IF NOT EXISTS pending_invigilator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    mobile TEXT,
    department TEXT,
    address TEXT
)
""")

# COURSES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    course_code TEXT UNIQUE,
    department TEXT
)
""")

cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS idx_course_code 
ON courses(course_code)
""")

# STUDENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
roll_no TEXT UNIQUE,
student_name TEXT,
department TEXT,
year TEXT
)
""")

# EXAMS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS exams (
id INTEGER PRIMARY KEY AUTOINCREMENT,
exam_name TEXT
)
""")

# QUESTION PAPERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS question_papers (
id INTEGER PRIMARY KEY AUTOINCREMENT,
course_id INTEGER,
exam_id INTEGER,
file_path TEXT
)
""")

# MODEL ANSWERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS model_answers (
id INTEGER PRIMARY KEY AUTOINCREMENT,
course_id INTEGER,
exam_id INTEGER,
file_path TEXT
)
""")

# STUDENT ANSWERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_answers (
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER,
course_id INTEGER,
exam_id INTEGER,
file_path TEXT
)
""")

# EVALUATION TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_answer_id INTEGER,
    assignment_id INTEGER,

    q1a REAL, q1b REAL, q1c REAL, q1d REAL, q1e REAL, q1f REAL,
    q2a REAL, q2b REAL, q2c REAL,
    q3a REAL, q3b REAL, q3c REAL,

    total REAL,
    comments TEXT,
    evaluator_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exam_assignments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
department TEXT,
year TEXT,
course_id INTEGER,
exam_id INTEGER,
status TEXT DEFAULT 'created',
assigned_faculty INTEGER
)
""")

cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
if not cursor.fetchone():
    cursor.execute("""
    INSERT INTO users (username, email, password, role, is_approved)
    VALUES (?, ?, ?, ?, ?)
    """, (
        "admin",
        "admin@gmail.com",
        generate_password_hash("admin123"),
        "admin",
        1
    ))

# 🟢 STEP 1: SAFE COLUMN ADD FUNCTION

def add_column_if_not_exists(cursor, table, column_def):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
    except sqlite3.OperationalError:
        pass  # Column already exists


# 🟢 STEP 2: APPLY TO ALL TABLES

# ✅ ADD assignment_id SAFELY

add_column_if_not_exists(cursor, "student_answers", "assignment_id INTEGER")
add_column_if_not_exists(cursor, "question_papers", "assignment_id INTEGER")
add_column_if_not_exists(cursor, "model_answers", "assignment_id INTEGER")
add_column_if_not_exists(cursor, "exam_assignments", "assigned_invigilator INTEGER")
add_column_if_not_exists(cursor, "users", "reset_token TEXT")

#---------------
#---------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
# ---------------------------------------------------
# PREDEFINED STUDENTS
# ---------------------------------------------------

cursor.execute("INSERT OR IGNORE INTO students VALUES (1,'CSE001','Rahul Sharma','Computer Engineering','1')")
cursor.execute("INSERT OR IGNORE INTO students VALUES (2,'CSE002','Priya Singh','Computer Engineering','2')")
cursor.execute("INSERT OR IGNORE INTO students VALUES (3,'CSE003','Amit Patel','Computer Engineering','3')")
cursor.execute("INSERT OR IGNORE INTO students VALUES (4,'CSE004','Sneha Verma','Mechanical Engineering','3')")
cursor.execute("INSERT OR IGNORE INTO students VALUES (5,'CSE005','Arjun Gupta','Electronics Engineering','3')")

# ---------------------------------------------------
# PREDEFINED EXAMS
# ---------------------------------------------------

cursor.execute("INSERT OR IGNORE INTO exams VALUES (1,'Progressive Test 1')")
cursor.execute("INSERT OR IGNORE INTO exams VALUES (2,'Progressive Test 2')")
cursor.execute("INSERT OR IGNORE INTO exams VALUES (3,'Semester Exam')")
cursor.execute("INSERT OR IGNORE INTO exams VALUES (4,'Practical Exam')")
cursor.execute("INSERT OR IGNORE INTO exams VALUES (5,'Viva')")

conn.commit()
conn.close()

print("Database created successfully with A NEW sample data")