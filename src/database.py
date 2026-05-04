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
Y = input("Timer to complete the quiz")
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

update_choice = input("\nDo you want to update your weakness level? (yes/no): ").lower()

if update_choice == "yes":
    # Show all records so user can choose ID
    cursor.execute("SELECT * FROM tracker2")
    print("\nAll Records:")
    for row in cursor.fetchall():
        print(row)

    update_id = int(input("\nEnter the ID to update weakness level: "))
    new_weakness = int(input("Enter your updated weakness level: "))

    cursor.execute("""
    UPDATE tracker2
    SET weakness_level = ?
    WHERE id = ?
    """, (new_weakness, update_id))

    conn.commit()
    print("Weakness level updated successfully.")

delete_choice = input("\nDo you want to delete a record? (yes/no): ").lower()

if delete_choice == "yes":
    cursor.execute("SELECT * FROM tracker2")
    print("\nAll Records:")
    for row in cursor.fetchall():
        print(row)

    delete_id = int(input("\nEnter the ID of the record you want to delete: "))

    cursor.execute("""
    DELETE FROM tracker2
    WHERE id = ?
    """, (delete_id,))

    conn.commit()
    print("Record deleted successfully.")

cursor.execute("SELECT * FROM tracker2")
print("\nFinal Records:")
for row in cursor.fetchall():
    print(row)

conn.commit ()
conn.close ()