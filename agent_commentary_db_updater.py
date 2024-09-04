import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

def create_comments_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the comments table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            agent_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(post_id) REFERENCES posts(id),
            FOREIGN KEY(agent_id) REFERENCES agents(id)
        );
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Comments table created successfully.")

if __name__ == "__main__":
    create_comments_table()
