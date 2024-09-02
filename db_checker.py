import sqlite3

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to retrieve all posts
query_posts = """
SELECT * FROM posts;
"""

cursor.execute(query_posts)
results_posts = cursor.fetchall()

# Print out the posts
if results_posts:
    print("Found the following posts:")
    for row in results_posts:
        print(row)
else:
    print("No posts found.")

# Query to retrieve all interactions
query_interactions = """
SELECT * FROM interactions;
"""

cursor.execute(query_interactions)
results_interactions = cursor.fetchall()

# Print out the interactions
if results_interactions:
    print("Found the following interactions:")
    for row in results_interactions:
        print(row)
else:
    print("No interactions found.")

# Close the connection
conn.close()
