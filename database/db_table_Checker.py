import sqlite3

# Path to your SQLite database
db_path = 'E:/ProjetosPython/NEWAI/app.db'

def get_table_info(cursor, table_name):
    """
    Retrieves column information for the given table.
    """
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return columns

def main():
    # Connect to the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Retrieve the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"Tables in the database '{db_path}':\n")
        for table_name in tables:
            table_name = table_name[0]
            print(f"Table: {table_name}")

            # Get column info
            columns = get_table_info(cursor, table_name)
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")  # col[1] is the column name, col[2] is the data type

            print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()
