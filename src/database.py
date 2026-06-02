import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345qwert@",
    database="tracker_db"
)

ADMIN_ID = "ADMIN123"
ADMIN_PASSWORD = "00000"

cursor = conn.cursor()

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

def save_user(user_id, password):

    cursor.execute("""
    SELECT * FROM users
    WHERE user_id = %s AND password = %s
    """, (user_id, password))

    existing_user = cursor.fetchone()

    if not existing_user:

        cursor.execute("""
        INSERT INTO users (user_id, password)
        VALUES (%s, %s)
        """, (user_id, password))

        conn.commit()

def start_system(user_id, password):

    save_user(user_id, password)

    if user_id == ADMIN_ID and password == ADMIN_PASSWORD:
            print("\n" + "="*30 + "\nADMIN MANAGEMENT CONSOLE\n" + "="*30)
            while True:
                print("\n1. View All Study Records\n2. View All Users\n3. Edit User ID/Password\n4. Delete a Record\n5. Exit")
                choice = input("Select an option: ")

                if choice == "1":
                    cursor.execute("SELECT * FROM tracker3")
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
                    cursor.execute("DELETE FROM tracker3 WHERE id = %s", (del_id,))
                    conn.commit()
                    print("Record deleted.")

                elif choice == "5":
                    break

    else:

        X = input("What subject are you studying right now?: ").upper()
        Y = int(input("Timer (hours only): "))
        Z = int(input("Weakness level: "))

        cursor.execute("""
        INSERT INTO tracker3 (user_id, topic, duration, weakness_level)
        VALUES (%s, %s, %s, %s)
        """, (user_id, X, Y, Z))

        conn.commit()

        cursor.execute("""
        SELECT * FROM tracker3
        WHERE topic = %s
        """, (X,))

        print("\nRecord for this subject:")
        for row in cursor.fetchall():
            print(row)

        cursor.execute("""
        SELECT COUNT(*) FROM tracker3
        WHERE topic = %s
        """, (X,))

        count = cursor.fetchone()[0]
        print(f"\nYou have studied {X} {count} times.")

        update_choice = input("\nUpdate weakness? (yes/no): ").lower()

        if update_choice == "yes":

            cursor.execute("SELECT * FROM tracker3")
            for row in cursor.fetchall():
                print(row)

            update_id = int(input("Enter ID: "))
            new_weakness = int(input("New weakness level: "))

            cursor.execute("""
            UPDATE tracker3
            SET weakness_level = %s
            WHERE id = %s
            """, (new_weakness, update_id))

            conn.commit()
            print("Updated successfully.")

        delete_choice = input("\nDelete record? (yes/no): ").lower()

        if delete_choice == "yes":

            cursor.execute("SELECT * FROM tracker3")
            for row in cursor.fetchall():
                print(row)

            delete_id = int(input("Enter ID: "))

            cursor.execute("""
            DELETE FROM tracker3
            WHERE id = %s
            """, (delete_id,))

            conn.commit()
            print("Deleted successfully.")

        cursor.execute("SELECT * FROM tracker3")
        print("\nFINAL RECORDS:")
        for row in cursor.fetchall():
            print(row)

user_id = input("Enter User ID: ")
password = input("Enter Password: ")

start_system(user_id, password)

conn.commit()
conn.close()