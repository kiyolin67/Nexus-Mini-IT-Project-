import sqlite3
conn = sqlite3.connect ("tracker.db")
cursor = conn.cursor ()

cursor.execute ("""
                CREATE TABLE IF NOT EXISTS tracker(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                duration INTEGER,
                weakness_level INTEGER
                )
""")

cursor.execute ("""
INSERT INTO tracker (topic, duration, weakness_level)
VALUES (?, ?, ?)
""",(X, Y, Z)
)

cursor.execute ("""
SELECT * FROM tracker
                """)
print (cursor.fetchall())

conn.commit ()
conn.close ()