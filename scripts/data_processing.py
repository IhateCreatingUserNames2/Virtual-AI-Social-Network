# Data processing script 
# scripts/data_processing.py

import pandas as pd
from sqlalchemy import create_engine
from models.database_models.models import Agent, Post, Comment, Interaction, AgentRelationship
from config.config import Config

# Database setup
engine = create_engine(Config.DATABASE_URI)
connection = engine.connect()

def load_agents_from_csv(csv_file_path):
    """
    Load agents from a CSV file and insert them into the database.
    CSV should have columns: name, personality_type, profile
    """
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        agent = Agent(
            name=row['name'],
            personality_type=row['personality_type'],
            profile=row['profile']
        )
        connection.execute(
            Agent.__table__.insert().values(
                name=agent.name,
                personality_type=agent.personality_type,
                profile=agent.profile
            )
        )
    print("Agents loaded from CSV successfully.")

def export_agents_to_csv(csv_file_path):
    """
    Export agents from the database to a CSV file.
    CSV will have columns: id, name, personality_type, profile
    """
    query = connection.execute(Agent.__table__.select())
    df = pd.DataFrame(query.fetchall(), columns=query.keys())
    df.to_csv(csv_file_path, index=False)
    print(f"Agents exported to {csv_file_path} successfully.")

def analyze_post_engagement(csv_file_path):
    """
    Analyze post engagement metrics and export the results to a CSV file.
    The analysis will include the number of likes and comments per post.
    """
    query = connection.execute(
        "SELECT p.id, p.content, p.likes, COUNT(c.id) AS comments_count "
        "FROM posts p LEFT JOIN comments c ON p.id = c.post_id "
        "GROUP BY p.id"
    )
    df = pd.DataFrame(query.fetchall(), columns=query.keys())
    df['engagement_score'] = df['likes'] + df['comments_count']
    df.to_csv(csv_file_path, index=False)
    print(f"Post engagement analysis exported to {csv_file_path} successfully.")

def summarize_agent_interactions(csv_file_path):
    """
    Summarize interactions of each agent and export the results to a CSV file.
    The summary will include the total number of interactions per agent.
    """
    query = connection.execute(
        "SELECT a.id, a.name, COUNT(i.id) AS interactions_count "
        "FROM agents a LEFT JOIN interactions i ON a.id = i.agent_id "
        "GROUP BY a.id"
    )
    df = pd.DataFrame(query.fetchall(), columns=query.keys())
    df.to_csv(csv_file_path, index=False)
    print(f"Agent interaction summary exported to {csv_file_path} successfully.")

def main():
    # Example usage of the functions
    load_agents_from_csv('data/agents.csv')
    export_agents_to_csv('data/exported_agents.csv')
    analyze_post_engagement('data/post_engagement.csv')
    summarize_agent_interactions('data/agent_interactions.csv')

if __name__ == '__main__':
    main()
