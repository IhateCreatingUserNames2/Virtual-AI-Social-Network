import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'


def check_agents_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agents';")
    table_exists = cursor.fetchone()

    if table_exists:
        print("The 'agents' table exists.")
    else:
        print("The 'agents' table does NOT exist.")

    conn.close()


if __name__ == "__main__":
    check_agents_table()
