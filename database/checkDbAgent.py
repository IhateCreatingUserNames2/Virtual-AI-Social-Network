import sqlite3

# Define the path to your SQLite database
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to select all agents
query = "SELECT * FROM agents"

try:
    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the executed query
    agents = cursor.fetchall()

    # Check if any agents exist in the table
    if agents:
        print("List of all agents:")
        for agent in agents:
            print(
                f"ID: {agent[0]}, Name: {agent[1]}, Personality Type: {agent[2]}, Profile: {agent[3]}, Tuning: {agent[4]}")
    else:
        print("No agents found in the database.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
