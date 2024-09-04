import sqlite3

# Database path
db_path = 'E:/ProjetosPython/NEWAI/app.db'


def get_all_agents_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to select all data from the agents table
        cursor.execute("SELECT * FROM posts")

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [description[0] for description in cursor.description]

        # Print column names
        print(" | ".join(column_names))
        print("-" * 80)

        # Print all rows
        for row in rows:
            print(" | ".join([str(item) for item in row]))

    except sqlite3.Error as e:
        print(f"Error retrieving data from agents table: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    get_all_agents_data()
