import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# AIVEN MYSQL CONNECTION
load_dotenv(find_dotenv())
print("Connecting to database...")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database="defaultdb",
    ssl_ca="ca.pem"
)

cursor = conn.cursor()

# CURRENT USER TRACKER

CURRENT_USER = None

# ADMIN ACCOUNT

ADMIN_ID = "Lin"
ADMIN_PASSWORD = "1234"

# TABLE CREATION
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255)
)
""")

try:
    cursor.execute("""
    ALTER TABLE users
    ADD COLUMN password VARCHAR(255)
    """)
except:
    pass

cursor.execute("""
CREATE TABLE IF NOT EXISTS tracker3(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50),
    topic VARCHAR(255),
    duration INTEGER,
    confidence INTEGER,
    friction_tag VARCHAR(255),
    date_logged DATE
)
""")

conn.commit()

# USER FUNCTIONS

def set_current_user(user_id):
    global CURRENT_USER
    CURRENT_USER = user_id


def save_user(user_id, password):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        return False # user already exists
        
    cursor.execute("""
    INSERT INTO users (user_id, password)
    VALUES (%s, %s)
    """, (user_id, password))
    conn.commit()
    return True # user saved successfully


def user_exists(user_id, password):

    cursor.execute("""
    SELECT *
    FROM users
    WHERE user_id = %s AND password = %s
    """, (
        user_id,
        password
))
    return cursor.fetchone()

# ADMIN FUNCTIONS

def is_admin(user_id, password):

    return (
        user_id == ADMIN_ID
        and
        password == ADMIN_PASSWORD
    )


def create_user(user_id, password):

    cursor.execute("""
    INSERT INTO users (
        user_id,
        password
    )
    VALUES (%s, %s)
    """, (
        user_id,
        password
    ))

    conn.commit()


def edit_user(
    old_user_id,
    new_user_id,
    new_password
):

    cursor.execute("""
    UPDATE users
    SET user_id = %s,
        password = %s
    WHERE user_id = %s
    """, (
        new_user_id,
        new_password,
        old_user_id
    ))

    conn.commit()


def delete_user(user_id):

    cursor.execute("""
    DELETE FROM users
    WHERE user_id = %s
    """, (user_id,))

    conn.commit()

# FOCUS TIMER FUNCTION

def save_focus_session(
    subject_name,
    duration,
    confidence,
    friction_tag
):

    global CURRENT_USER

    if CURRENT_USER is None:
        print("No logged in user.")
        return

    today_date = datetime.now().date()

    cursor.execute("""
    INSERT INTO tracker3 (
        user_id,
        topic,
        duration,
        confidence,
        friction_tag,
        date_logged
    )
    VALUES (%s, %s, %s, %s)
    """, (
        CURRENT_USER,
        subject_name,
        duration,
        confidence,
        friction_tag,
        today_date
    ))

    conn.commit()

    print(
        f"Saved -> "
        f"User: {CURRENT_USER}, "
        f"Subject: {subject_name}, "
        f"Duration: {duration}, "
        f"Confidence: {confidence},"
        f"Today's Date: {today_date},"
    )

# DATA RETRIEVAL

def get_all_users():

    cursor.execute("""
    SELECT *
    FROM users
    """)

    return cursor.fetchall()


def get_all_sessions():

    cursor.execute("""
    SELECT *
    FROM tracker3
    """)

    return cursor.fetchall()


def get_user_sessions(user_id):

    cursor.execute("""
    SELECT *
    FROM tracker3
    WHERE user_id = %s
    """, (user_id,))

    return cursor.fetchall()

# OPTIONAL UPDATE / DELETE

def update_weakness(
    record_id,
    new_weakness
):

    cursor.execute("""
    UPDATE tracker3
    SET confidence = %s
    WHERE id = %s
    """, (
        new_weakness,
        record_id
    ))

    conn.commit()


def delete_session(record_id):

    cursor.execute("""
    DELETE FROM tracker3
    WHERE id = %s
    """, (record_id,))

    conn.commit()


def get_user_deadlines(username):
    try:
        query = "SELECT task_name, due_date, is_urgent FROM deadlines WHERE username = %s ORDER BY is_urgent DESC"         
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(f"Error fetching deadlines: {e}")
        return[]

def delete_deadline(username, task_name):
    try:
        query = "DELETE FROM deadlines WHERE username = %s AND task_name = %s"
        cursor.execute(query, (username, task_name))
        conn.commit() # to save into cloud properly
        print(f"Task '{task_name}' successfully deleted.")

    except Exception as e:
        print(f"Error deleting deadline: {e}")

def add_deadline(username, task_name, due_date, is_urgent):
    try:
        urgent_flag = 1 if is_urgent else 0
        query = "INSERT INTO deadlines (username, task_name, due_date, is_urgent) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, task_name, due_date, urgent_flag))
        conn.commit()
        print(f"Task '{task_name}' successfully added to cloud")
    except Exception as e:
        print(f"Error adding deadline: {e}")

# REMINDER 

cursor.execute("""
CREATE TABLE IF NOT EXISTS deadlines (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    task_name VARCHAR(255),
    due_date VARCHAR(100),
    is_urgent BOOLEAN
)
""")
conn.commit()


# DATABASE CLEANUP

def close_database():

    conn.commit()
    conn.close()