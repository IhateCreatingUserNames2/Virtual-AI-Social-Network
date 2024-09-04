import requests

from models.database_models.models import Agent, Post, Comment, Interaction, AgentRelationship, Action, AgentAction
from models.ml_models.agent_llm import AgentLLM
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.config import Config
import json
import random
import csv
import deepai
import os
from collections import defaultdict
from datetime import datetime, timedelta

# Database setup
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

class AgentService:
    def __init__(self, model_name):
        self.llm = AgentLLM(model_name)
        deepai.api_key = '7c5f0825-9c84-4ed0-8721-8ecd6abf4e63'

    def generate_profile_picture(self, agent_name, description):
        # Call the DeepAI API to generate an image
        try:
            response = deepai.Completion.create(
                'text2img',
                {'text': description},
            )
            # Get the image URL from the response
            image_url = response['output_url']

            # Download and save the image locally
            image_data = requests.get(image_url).content
            image_path = f'E:/ProjetosPython/NEWAI/data/img/{agent_name}.jpg'
            with open(image_path, 'wb') as handler:
                handler.write(image_data)

            return image_path
        except Exception as e:
            print(f"Error generating profile picture: {e}")
            return None

    def generate_agent_reply(self, post, agent_id):
        """
        Generate a reply to a post based on the agent's profile and characteristics.
        """
        agent = session.query(Agent).filter_by(id=agent_id).first()

        if not agent:
            return None

        prompt = f"Imagine if you are a person with the characteristics: {agent.profile}. You are on a social network, and {agent.name} posted: '{post.content}'. Based on your characteristics and tuning, make a reply for this post. Talk in First Person."

        # Generate response using LLM
        response = self.llm.generate_response(prompt, agent.personality_type, json.loads(agent.tuning))

        # Save the generated reply as a comment
        comment = Comment(post_id=post.id, agent_id=agent.id, content=response)
        session.add(comment)
        session.commit()

        return comment

    def load_action_scores(self, file_path):
        scores = {}
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores[row['Ação']] = int(row['Nota'])
        return scores

    # Function to calculate the humor score for an agent
    def calculate_humor(self, actions_by, actions_against, action_scores):
        total_score = 0
        total_actions = 0

        for action in actions_by + actions_against:
            score = action_scores.get(action.action.action, 0)  # Accessing action_name through action.action
            total_score += score
            total_actions += 1

        if total_actions > 0:
            return round(total_score / total_actions, 2)
        return 0

    # Function to calculate friendships based on interactions
    def calculate_friendship(self, agent_id, action_scores, session):
        friendship_scores = defaultdict(int)

        actions_by = session.query(AgentAction).filter(AgentAction.agent_id == agent_id).all()
        actions_against = session.query(AgentAction).filter(AgentAction.target_agent_id == agent_id).all()

        for action in actions_by:
            score = action_scores.get(action.action.action, 0)
            friendship_scores[action.target_agent_id] += score

        for action in actions_against:
            score = action_scores.get(action.action.action, 0)
            friendship_scores[action.agent_id] += score

        sorted_friendships = sorted(friendship_scores.items(), key=lambda item: item[1], reverse=True)

        friendships = []
        for related_agent_id, score in sorted_friendships:
            agent_name = session.query(Agent).filter_by(id=related_agent_id).first().name
            friendships.append({'agent_name': agent_name, 'score': score})

        return friendships

    def calculate_whole_median_humor(self):
        agents = session.query(Agent).all()
        total_humor = 0
        num_agents = 0

        for agent in agents:
            actions_by = session.query(AgentAction).filter_by(agent_id=agent.id).all()
            actions_against = session.query(AgentAction).filter_by(target_agent_id=agent.id).all()
            humor = self.calculate_humor(actions_by, actions_against,
                                         self.load_action_scores('E:/ProjetosPython/NEWAI/data/nota.csv'))
            total_humor += humor
            num_agents += 1

        if num_agents > 0:
            whole_median_humor = round(total_humor / num_agents, 2)
        else:
            whole_median_humor = 0

        # Store the median humor in a file
        try:
            with open('E:/ProjetosPython/NEWAI/data/median_humor.txt', 'w') as file:
                file.write(str(whole_median_humor))
            print(f"Whole Median humor value calculated and stored: {whole_median_humor}")  # Debug output
        except IOError as e:
            print(f"Error writing whole median humor file: {e}")  # Debug output

        return whole_median_humor

    def read_whole_median_humor(self):
        try:
            with open('E:/ProjetosPython/NEWAI/data/median_humor.txt', 'r') as file:
                whole_median_humor = file.read().strip()
                print(f"Whole Median Humor Value Read from file: {whole_median_humor}")  # Debug line
                return float(whole_median_humor)
        except FileNotFoundError:
            print("Error: median_humor.txt file not found.")
            return None
        except ValueError:
            print("Error: Could not convert whole median humor value to float.")
            return None

    # Function to get the agent's profile with all required data
    def get_agent_profile(self, agent_id):
        agent = session.query(Agent).filter_by(id=agent_id).first()

        if not agent:
            return {'error': 'Agent not found'}

        action_scores = self.load_action_scores('E:/ProjetosPython/NEWAI/data/nota.csv')

        actions_by = session.query(AgentAction).filter_by(agent_id=agent_id).all()
        actions_against = session.query(AgentAction).filter_by(target_agent_id=agent_id).all()

        humor = self.calculate_humor(actions_by, actions_against, action_scores)

        friendships = self.calculate_friendship(agent_id, action_scores, session)

        # Hard-coded value for testing
        whole_median_humor = 4.48

        print(f"Debug: Whole Median Humor = {whole_median_humor}")  # Debugging line

        return {
            'agent': agent,
            'posts': session.query(Post).filter_by(agent_id=agent_id).all(),
            'actions_by': actions_by,
            'actions_against': actions_against,
            'humor': humor,
            'friendships': friendships,
            'whole_median_humor': whole_median_humor  # Pass the median humor to the template
        }

    def choose_action(self, agent, post):
        """
        Choose an action for the agent based on its personality and the probabilities of each action.
        """
        actions = self.get_actions_by_personality(agent.personality_type)
        action_probabilities = [(action, action.probability_level) for action in actions]

        # Convert probability descriptions (Low, Medium, High) to numerical values if necessary
        probability_map = {
            'Low': 0.2,
            'Medium': 0.5,
            'High': 0.8
        }
        weighted_actions = [
            (action, probability_map.get(action.probability_level, action.probability_level))
            for action in action_probabilities
        ]

        # Randomly select an action based on the weighted probabilities
        chosen_action = self.weighted_random_choice(weighted_actions)

        # Perform the chosen action
        self.perform_action(agent, post, chosen_action)

    def weighted_random_choice(self, weighted_actions):
        """
        Select an action based on weighted probabilities.
        """
        total = sum(weight for action, weight in weighted_actions)
        r = random.uniform(0, total)
        upto = 0
        for action, weight in weighted_actions:
            if upto + weight >= r:
                return action
            upto += weight



    def create_agent(self, name, personality_type, tuning, description):
        tuning_json = json.dumps(tuning)
        new_agent = Agent(
            name=name,
            personality_type=personality_type,
            profile=f"{name} with {personality_type} profile",
            tuning=tuning_json
        )
        session.add(new_agent)
        session.commit()

        # Generate profile picture based on description
        image_path = self.generate_profile_picture(name, description)
        if image_path:
            new_agent.profile_picture = image_path
            session.commit()

        return {
            'id': new_agent.id,
            'name': new_agent.name,
            'personality_type': new_agent.personality_type,
            'profile': new_agent.profile,
            'profile_picture': image_path,
            'tuning': tuning
        }

    def get_agents(self):
        agents = session.query(Agent).all()
        return [{
            'id': agent.id,
            'name': agent.name,
            'personality_type': agent.personality_type,
            'profile': agent.profile,
            'tuning': json.loads(agent.tuning),
            'profile_picture': agent.profile_picture  # Add this line
        } for agent in agents]

    def get_agent_by_id(self, agent_id):
        agent = session.query(Agent).filter_by(id=agent_id).first()
        if agent:
            return {
                'id': agent.id,
                'name': agent.name,
                'personality_type': agent.personality_type,
                'profile': agent.profile,
                'tuning': json.loads(agent.tuning)
            }
        return None

    def generate_post(self, agent_id, prompt):
        agent = session.query(Agent).filter_by(id=agent_id).first()
        print(f"Agent retrieved: {agent}")
        if not agent:
            print("Agent not found!")
            return {'error': 'Agent not found'}

        # Ensure tuning is a dictionary
        tuning_dict = agent.tuning
        if isinstance(tuning_dict, str):
            tuning_dict = json.loads(tuning_dict)
        elif isinstance(tuning_dict, dict):
            pass  # Already a dictionary
        else:
            print(f"Unexpected tuning type: {type(tuning_dict)}")
            return {'error': 'Unexpected tuning type'}

        print(f"Tuning dictionary: {tuning_dict}")
        response = self.llm.generate_response(prompt, agent.personality_type, tuning_dict)
        print(f"Generated response: {response}")

        if not response:
            print("Failed to generate content")
            return {'error': 'Failed to generate content'}

        new_post = Post(agent_id=agent.id, content=response, prompt=prompt)
        session.add(new_post)
        session.commit()

        print(f"New post created: {new_post}")
        return {
            'agent_name': agent.name,
            'post_content': response,
            'prompt': prompt,
            'timestamp': new_post.timestamp
        }

    def generate_llm_response(self, agent_id, prompt):
        agent = session.query(Agent).filter_by(id=agent_id).first()
        if not agent:
            return {'error': 'Agent not found'}

        tuning_dict = json.loads(agent.tuning)
        response = self.llm.generate_response(prompt, agent.personality_type, tuning_dict)
        return {
            'agent_id': agent.id,
            'agent_name': agent.name,
            'response': response
        }

    def interact(self, agent_name, interaction_type, content):
        agent = session.query(Agent).filter_by(name=agent_name).first()
        if not agent:
            return {'error': 'Agent not found'}

        interaction = Interaction(agent_id=agent.id, interaction_type=interaction_type, content=content)
        session.add(interaction)
        session.commit()

        return {
            'agent_name': agent_name,
            'interaction_type': interaction_type,
            'interaction_content': content,
            'timestamp': interaction.timestamp
        }

    def create_relationship(self, agent_id, related_agent_id, relationship_type):
        agent = session.query(Agent).filter_by(id=agent_id).first()
        related_agent = session.query(Agent).filter_by(id=related_agent_id).first()

        if not agent or not related_agent:
            return {'error': 'Agent or related agent not found'}

        relationship = AgentRelationship(
            agent_id=agent.id,
            related_agent_id=related_agent.id,
            relationship_type=relationship_type
        )
        session.add(relationship)
        session.commit()

        return {
            'agent_id': agent.id,
            'related_agent_id': related_agent.id,
            'relationship_type': relationship_type,
            'timestamp': relationship.timestamp
        }

    def read_posts_and_act(self):
        """
        Method for agents to read posts in the network and react.
        """
        agents = self.get_agents()
        posts = session.query(Post).all()

        for agent in agents:
            for post in posts:
                # Ignore posts created by the agent
                if post.agent_id == agent['id']:
                    continue

                # Determine if the agent will perform an action
                self.analyze_post_and_act(agent, post)

    def analyze_post_and_act(self, agent, post):
        actions = session.query(Action).filter_by(personality_type=agent['personality_type']).all()

        # Ensure tuning is a dictionary
        tuning_dict = agent['tuning']
        if isinstance(tuning_dict, str):
            tuning_dict = json.loads(tuning_dict)
        elif isinstance(tuning_dict, dict):
            pass  # Already a dictionary
        else:
            print(f"Unexpected tuning type: {type(tuning_dict)}")
            return

        # Prepare the prompt with the possible actions
        action_names = [action.action for action in actions]
        prompt = self.create_action_prompt(agent, post, action_names)

        # Send the prompt to Ollama to determine the action
        response_text = self.llm.generate_response(prompt, agent['personality_type'], tuning_dict)

        # Extract the action name from the response
        selected_action_name = self.extract_action_from_response(response_text, action_names)

        # Find the action object that matches the selected action name
        selected_action = next((action for action in actions if action.action == selected_action_name), None)

        if selected_action:
            self.perform_action(agent, post, selected_action)
        else:
            print(f"Ollama returned an invalid action: {response_text}")

    def extract_action_from_response(self, response_text, action_names):
        """
        Extracts the action name from Ollama's response by matching against known action names.
        """
        # Normalize response text to lower case
        response_text = response_text.lower()

        for action_name in action_names:
            # Normalize action name to lower case and check if it's in the response
            if action_name.lower() in response_text:
                return action_name

        return None  # If no valid action is found

    def create_action_prompt(self, agent, post, action_names):
        """
        Creates a prompt to send to Ollama based on the agent, post, and possible actions.
        """
        prompt = (
            f"Agent {agent['name']} is responding to the following post: '{post.content}'. "
            f"Based on their personality ({agent['personality_type']}), they can choose one of the following actions: "
            f"{', '.join(action_names)}. Please return only the action name they would most likely choose."
        )
        return prompt

    def should_perform_action(self, probability_level):
        """
        Determines if an action should be performed based on the probability level.
        """
        levels = {
            "Baixo": 0.3,
            "Médio": 0.6,
            "Alto": 0.9
        }
        return random.random() < levels.get(probability_level, 0.5)

    def perform_action(self, agent, post, action):
        """
        Executes the agent's action.
        """
        target_agent_id = post.agent_id  # The target agent is the creator of the post

        # Ensure agent and action are objects, not dictionaries
        if isinstance(agent, dict):
            agent_id = agent['id']
            agent_name = agent['name']
        else:
            print(f"Expected a dictionary for the agent, but got {type(agent)}")
            return

        # Record the action in the database
        new_action = AgentAction(
            agent_id=agent_id,
            action_id=action.id,  # Ensure this is accessed correctly
            target_agent_id=target_agent_id,
            post_id=post.id
        )
        session.add(new_action)
        session.commit()

        # Display the action in the interface
        print(f"Agent {agent_name} performed action {action.action} against Agent {target_agent_id}")



