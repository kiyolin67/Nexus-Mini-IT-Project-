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

ADMIN_ID = "ADMIN123"
ADMIN_PASSWORD = "00000"

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

    cursor.execute("""
    SELECT *
    FROM users
    WHERE user_id = %s AND password = %s
    """, (user_id, password))
    return cursor.fetchone()


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

def save_study_session(topic, duration, confidence, friction_tag):
    global CURRENT_USER

    if CURRENT_USER is None:
        print("No logged in user.")
        return
    
    today_date = datetime.now().date()

    cursor.execute("""
    INSERT INTO study_sessions (
        user_id,
        topic,
        duration,
        confidence,
        friction_tag,
        date_logged
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        CURRENT_USER,
        topic,
        duration,
        confidence,
        friction_tag,
        today_date
    ))

    conn.commit()
    print(f"Session Saved -> User: {CURRENT_USER}, Topic: {topic}, Duration: {duration}, Confidence: {confidence}, Friction Tag: {friction_tag}, Date: {today_date}")

def get_user_sessions(user_id):
    cursor.execute("""
    SELECT *
    FROM study_sessions
    WHERE user_id = %s
    ORDER BY date_logged ASC
    """, (user_id,))

    return cursor.fetchall()
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
    confidence
):

    global CURRENT_USER

    if CURRENT_USER is None:
        print("No logged in user.")
        return

    cursor.execute("""
    INSERT INTO tracker3 (
        user_id,
        topic,
        duration,
        weakness_level
    )
    VALUES (%s, %s, %s, %s)
    """, (
        CURRENT_USER,
        subject_name,
        duration,
        confidence
    ))

    conn.commit()

    print(
        f"Saved -> "
        f"User: {CURRENT_USER}, "
        f"Subject: {subject_name}, "
        f"Duration: {duration}, "
        f"Confidence: {confidence}"
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
    SET weakness_level = %s
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

# DATABASE CLEANUP

def close_database():

    conn.commit()
    conn.close()