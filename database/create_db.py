import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read the SQL schema file
with open('E:/ProjetosPython/NEWAI/database/schema.sql', 'r') as file:
    schema = file.read()

# Execute the schema SQL commands
cursor.executescript(schema)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database schema created successfully!")
