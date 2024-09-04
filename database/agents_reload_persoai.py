import sys
import os
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.database_models.models import Agent, AgentRelationship
from services.personality_service import PersonalityService
from config.config import Config
import random
import json

# Path to your SQLite database file
db_path = 'E:/ProjetosPython/NEWAI/app.db'

# Database setup using SQLAlchemy
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

# Function to check for existing tables
def check_tables(engine):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]
        return tables

# Check if all necessary tables exist
required_tables = ['agents', 'posts', 'comments', 'interactions', 'agent_relationships']
existing_tables = check_tables(engine)
missing_tables = [table for table in required_tables if table not in existing_tables]

if missing_tables:
    print(f"Missing tables: {', '.join(missing_tables)}")
    sys.exit(1)

print("All required tables are present.")

# Function to reload the persoai.csv file
def reload_persoai_csv():
    # Load personality data using the PersonalityService with the correct path
    csv_path = 'E:/ProjetosPython/NEWAI/data/persoai.csv'
    personality_service = PersonalityService(csv_path)
    personalities = personality_service.list_personalities()

    # Clear existing data
    session.query(Agent).delete()
    session.query(AgentRelationship).delete()
    session.commit()

    # Create agents based on personalities
    agents = []
    for i, (personality_name, personality_data) in enumerate(personalities.items()):
        agent_name = f"Agent_{i + 1}"
        profile = personality_data['prompt']
        tuning = json.dumps(personality_data['tuning'])  # Convert the tuning dictionary to a JSON string

        agent = Agent(
            name=agent_name,
            personality_type=personality_name,
            profile=profile,
            tuning=tuning
        )
        session.add(agent)
        agents.append(agent)
    session.commit()

    # Create sample agent relationships
    for agent in agents:
        related_agents = random.sample(agents, 3)  # Each agent has 3 relationships
        for related_agent in related_agents:
            if agent.id != related_agent.id:  # Avoid self-relationships
                relationship = AgentRelationship(
                    agent_id=agent.id,
                    related_agent_id=related_agent.id,
                    relationship_type=random.choice(["friend", "follower"])
                )
                session.add(relationship)
    session.commit()

    print("Personality data reloaded and database updated successfully!")

if __name__ == "__main__":
    reload_persoai_csv()
