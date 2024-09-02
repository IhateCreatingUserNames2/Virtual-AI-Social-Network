import sqlite3

# Path to your SQLite database
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# SQL script to create the necessary tables
sql_script = """
-- Table for storing agent profiles
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    personality_type VARCHAR(10) NOT NULL,
    profile TEXT NOT NULL,
    tuning TEXT NOT NULL
);

-- Table for storing interactions between agents and/or posts
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    interaction_type VARCHAR(50),
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for logging the posts made by agents
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    prompt TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INT DEFAULT 0,
    comments_count INT DEFAULT 0
);

-- Table for logging comments made on posts
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INT REFERENCES posts(id),
    agent_id INT REFERENCES agents(id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing relationships between agents (e.g., friends, followers)
CREATE TABLE IF NOT EXISTS agent_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    related_agent_id INT REFERENCES agents(id),
    relationship_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing personality types with prompts and tuning
CREATE TABLE IF NOT EXISTS personalities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personality_type VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    tuning JSON NOT NULL
);

-- Table for storing actions available for each personality
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personality_type VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    probability_level VARCHAR(10) NOT NULL
);

-- Table for logging the actions performed by agents
CREATE TABLE IF NOT EXISTS agent_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INT REFERENCES agents(id),
    action_id INT REFERENCES actions(id),
    target_agent_id INT REFERENCES agents(id),
    post_id INT REFERENCES posts(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Connect to the database and execute the script
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    print("Database schema updated successfully.")
