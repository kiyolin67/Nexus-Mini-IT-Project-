import mysql.connector
conn = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "12345qwert@",
    database = "tracker_db" 
)

ADMIN_ID = "ADMIN123"

cursor = conn.cursor ()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255)
)
""")

cursor.execute ("""
                CREATE TABLE IF NOT EXISTS tracker3(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                user_id VARCHAR(50),
                topic VARCHAR(255),
                duration INTEGER,
                weakness_level INTEGER
                )
""")

user_id = input("Enter your User ID: ").upper()

if user_id == ADMIN_ID:
            print("\n" + "="*30 + "\nADMIN MANAGEMENT CONSOLE\n" + "="*30)
            while True:
                print("\n1. View All Study Records\n2. View All Users\n3. Edit User ID/Password\n4. Delete a Record\n5. Exit")
                choice = input("Select an option: ")

                if choice == "1":
                    cursor.execute("SELECT * FROM tracker2")
                    for row in cursor.fetchall(): print(row)
                
                elif choice == "2":
                    cursor.execute("SELECT * FROM users")
                    for row in cursor.fetchall(): print(row)

                elif choice == "3":
                    old_id = input("Enter User ID to edit: ")
                    new_id = input("Enter new User ID (or press enter to keep): ") or old_id
                    new_pass = input("Enter new Password: ")
                    cursor.execute("UPDATE users SET user_id = %s, password = %s WHERE user_id = %s", (new_id, new_pass, old_id))
                    conn.commit()
                    print("User updated.")

                elif choice == "4":
                    del_id = input("Enter Record ID to delete from tracker: ")
                    cursor.execute("DELETE FROM tracker2 WHERE id = %s", (del_id,))
                    conn.commit()
                    print("Record deleted.")

                elif choice == "5":
                    break

else:
    cursor.execute("""
    SELECT * FROM users
    WHERE user_id = %s
    """, (user_id,))

    existing_user = cursor.fetchone()

    if not existing_user:

        cursor.execute("""
        INSERT INTO users (user_id)
        VALUES (%s)
        """, (user_id,))

        conn.commit()

        print("New user created successfully!")

    else:
        print("Welcome back!")

X = input("What subject are you studying right now?:").upper()
Y = int(input("Timer to complete the quiz( Only type in numbers for hours)?:"))
Z = int(input("What is your weakness level in this test?:"))

cursor.execute ("""
INSERT INTO tracker3 (user_id, topic, duration, weakness_level)
VALUES (%s, %s, %s, %s)
""",(user_id, X, Y, Z)
)

cursor.execute ("""
SELECT * FROM tracker3 WHERE topic = %s
                """, (X,))
print ("Record for this subject is: ",cursor.fetchall())

cursor.execute ("""
SELECT COUNT(*) FROM tracker3 WHERE topic = %s
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
    UPDATE tracker3
    SET weakness_level = %s
    WHERE id = %s
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
    DELETE FROM tracker3
    WHERE id = %s
    """, (delete_id,))

    conn.commit()
    print("Record deleted successfully.")

cursor.execute("SELECT * FROM tracker2")
print("\nFinal Records:")
for row in cursor.fetchall():
    print(row)

conn.commit ()
conn.close ()