import sqlite3
conn = sqlite3.connect ("tracker.db")
cursor = conn.cursor()

cursor.execute ("""
                CREATE TABLE IF NOT EXISTS tracker(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                topic TEXT,
                duration INTEGER,
                weakness_level INTEGER
                )
""")

cursor.execute("""
INSERT INTO tracker (date, topic, duration, weakness_level)
VALUES (?, ?, ?, ?)
""",("2026-04-13", "Math", 60, 5)
)

conn.commit()
conn.close()