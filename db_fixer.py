import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

def add_profile_picture_column():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the column already exists
    cursor.execute("PRAGMA table_info(agents)")
    columns = [info[1] for info in cursor.fetchall()]

    if 'profile_picture' not in columns:
        # Add the `profile_picture` column to the `agents` table
        try:
            cursor.execute("ALTER TABLE agents ADD COLUMN profile_picture TEXT")
            conn.commit()
            print("Successfully added the 'profile_picture' column to the 'agents' table.")
        except sqlite3.OperationalError as e:
            print(f"Error adding column: {e}")
    else:
        print("The 'profile_picture' column already exists in the 'agents' table.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    add_profile_picture_column()
