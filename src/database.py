import sqlite3
conn = sqlite3.connect ("tracker2.db")
cursor = conn.cursor ()

cursor.execute ("""
                CREATE TABLE IF NOT EXISTS tracker2(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                duration INTEGER,
                weakness_level INTEGER
                )
""")

X = input("What subject are you studying right now?").upper()
Y = input("How long did you study?")
Z = input("What is your weakness level in this test?")

cursor.execute ("""
INSERT INTO tracker2 (topic, duration, weakness_level)
VALUES (?, ?, ?)
""",(X, Y, Z)
)

cursor.execute ("""
SELECT * FROM tracker2 WHERE topic = ?
                """, (X,))
print ("Record for this subject is: ",cursor.fetchall())

cursor.execute ("""
SELECT COUNT (*) FROM tracker2 WHERE topic = ?
                """, (X,))
COUNT = cursor.fetchone()[0]
print (f"You have studied {X} {COUNT} times.")

conn.commit ()
conn.close ()