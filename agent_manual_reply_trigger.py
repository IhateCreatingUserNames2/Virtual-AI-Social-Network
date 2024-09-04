import sqlite3
from services.agent_service import AgentService
from config.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.database_models.models import Agent, Post

# Database setup
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize AgentService with the specified LLM model name
agent_service = AgentService(Config.LLM_MODEL_NAME)

def trigger_agent_comments(agent_name='Elena'):
    # Fetch the agent by name
    agent = session.query(Agent).filter_by(name=agent_name).first()
    if not agent:
        print(f"Agent {agent_name} not found.")
        return

    # Fetch all posts
    posts = session.query(Post).all()

    # Trigger the agent to comment on all posts
    for post in posts:
        print(f"Generating comment for post ID {post.id} by Agent {agent.name}...")
        comment = agent_service.generate_agent_reply(post, agent.id)
        if comment:
            print(f"Comment saved: {comment.content}")
        else:
            print(f"Failed to generate comment for post ID {post.id}.")

if __name__ == "__main__":
    trigger_agent_comments('Elena')  # Replace 'Elena' with the name of Agent_2 if different
