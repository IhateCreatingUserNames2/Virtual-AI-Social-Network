import time
from services.agent_service import AgentService
from config.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from models.database_models.models import Agent, Post
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)
db_path = 'E:/ProjetosPython/NEWAI/app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create engine and session for manual queries
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

try:
    session.execute(text('SELECT 1'))
    session.query(Agent).first()  # Check if 'agents' table is accessible
    print("Database connection is successful and 'agents' table is accessible.")
except Exception as e:
    print(f"Error: {e}")
    session.rollback()

# Initialize AgentService with the specified LLM model name
agent_service = AgentService(Config.LLM_MODEL_NAME)


def get_all_agents():
    """Retrieve all agents and cache their information in a dictionary."""
    agent_cache = {}
    try:
        agents = session.query(Agent).all()
        for agent in agents:
            agent_cache[agent.id] = {
                'name': agent.name,
                'personality_type': agent.personality_type,
                'profile': agent.profile,
                'profile_picture': agent.profile_picture,
                'tuning': agent.tuning,
            }
        print(f"Retrieved {len(agent_cache)} agents from the database.")
    except Exception as e:
        print(f"Error retrieving agents: {e}")
        session.rollback()

    return agent_cache


def manual_trigger():
    """Process each agent using cached data."""
    try:
        agent_cache = get_all_agents()  # Retrieve and cache agent information

        for agent_id, agent_info in agent_cache.items():
            print(f"Processing agent: {agent_info['name']} (ID: {agent_id})")

            # Retrieve humor, friendship, and other relevant data for the agent
            profile_data = agent_service.get_agent_profile(agent_id)

            humor = profile_data['humor']
            median_humor = profile_data.get('whole_median_humor', 4.43)  # Default to 4.43 if missing
            friendships = profile_data['friendships']
            median_friendship = sum([f['score'] for f in friendships]) / len(friendships) if friendships else 0
            agent_description = profile_data['agent'].profile

            # Construct the prompt
            friend_list = ', '.join([f"{f['agent_name']} (Friendship Level: {f['score']})" for f in friendships])
            prompt = (
                f"Your humor Level is {humor}, the median humor is {median_humor}. "
                f"Your friendship list is {friend_list}. The median friendship is {median_friendship}. "
                f"Based on that, what would someone of your characteristics ({agent_description}) like to do? "
                "Select to [generate_post] and/or [generate_agent_reply] and/or [choose_action]. "
                "If you choose [generate_agent_reply], you will reply to someone else's post. "
                "If you choose [generate_post], you may say anything you like, preferably related to your characteristic and human behavior. "
                "If you choose [choose_action], you must choose a friend from the friend list and an action based on your Humor Level and Friendship Level with each agent."
            )

            # Send the prompt to the LLM and process the response
            response = agent_service.generate_llm_response(agent_id, prompt)

            if '[generate_agent_reply]' in response['response']:
                posts = session.query(Post).all()  # Get all posts for the agent to reply to
                if posts:
                    chosen_post = posts[0]  # Select the first post (for simplicity, you can add more logic here)
                    agent_service.generate_agent_reply(chosen_post, agent_id)
            elif '[generate_post]' in response['response']:
                agent_service.generate_post(agent_id, prompt)  # Generate a new post
            elif '[choose_action]' in response['response']:
                if friendships:
                    chosen_friend = friendships[
                        0]  # Select the first friend (for simplicity, you can add more logic here)
                    agent_service.choose_action(agent_info, chosen_friend['agent_name'])

            print(f"Agent {agent_info['name']} processed with response: {response['response']}")

    except Exception as e:
        print(f"Error during manual trigger: {e}")


if __name__ == "__main__":
    manual_trigger()
