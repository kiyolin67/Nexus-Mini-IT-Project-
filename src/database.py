import mysql.connector

# AIVEN MYSQL CONNECTION

conn = mysql.connector.connect(
    host="nexusproject-nexusproject-ac15.g.aivencloud.com",
    port=20625,
    user="avnadmin",
    password="AVNS_C34T5eZzIaw4tZvS43_",
    database="defaultdb"
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
    user_id VARCHAR(50) PRIMARY KEY
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
    weakness_level INTEGER
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
    WHERE user_id = %s
    """, (user_id,))

    existing_user = cursor.fetchone()

    if not existing_user:

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


def user_exists(user_id, password):

    cursor.execute("""
    SELECT *
    FROM users
    WHERE user_id = %s
    AND password = %s
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