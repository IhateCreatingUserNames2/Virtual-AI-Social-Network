# End-to-end tests 
# tests/e2e_tests/test_e2e.py

import unittest
import json
from flask import Flask
from routes.routes import app
from config.config import Config
from models.database_models.models import Base, Agent, Post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the testing environment
        cls.engine = create_engine(Config.DATABASE_URI)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.client = app.test_client()
        app.config['TESTING'] = True

    @classmethod
    def tearDownClass(cls):
        # Tear down the testing environment
        cls.session.close()
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_create_agent_and_generate_post(self):
        # Test creating an agent and generating a post

        # Step 1: Create a new agent
        agent_data = {
            "name": "TestAgent",
            "personality_type": "INTP"
        }
        response = self.client.post('/create_agent', data=json.dumps(agent_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        agent_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('id', agent_response)
        self.assertEqual(agent_response['name'], "TestAgent")
        self.assertEqual(agent_response['personality_type'], "INTP")

        # Step 2: Generate a post for the newly created agent
        post_data = {
            "agent_name": "TestAgent",
            "prompt": "This is a test prompt."
        }
        response = self.client.post('/post', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        post_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('post_content', post_response)
        self.assertIn("TestAgent", post_response['post_content'])

    def test_agent_interaction(self):
        # Test interaction between agents

        # Step 1: Create another agent
        agent_data = {
            "name": "InteractingAgent",
            "personality_type": "ENTP"
        }
        response = self.client.post('/create_agent', data=json.dumps(agent_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Step 2: Create a post for the initial agent
        post_data = {
            "agent_name": "TestAgent",
            "prompt": "This is a second test prompt."
        }
        response = self.client.post('/post', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Step 3: Interact with the post as the second agent
        interaction_data = {
            "agent_name": "InteractingAgent",
            "interaction_type": "like",
            "content": "Liked the post"
        }
        response = self.client.post('/interact', data=json.dumps(interaction_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        interaction_response = json.loads(response.data.decode('utf-8'))
        self.assertIn("interaction_content", interaction_response)
        self.assertEqual(interaction_response['interaction_content'], "Liked the post")

    def test_list_agents(self):
        # Test listing all agents
        response = self.client.get('/agents')
        self.assertEqual(response.status_code, 200)
        agents = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(agents, list)
        self.assertGreater(len(agents), 0)

    def test_get_agent_by_id(self):
        # Test retrieving a specific agent by ID
        # Assuming TestAgent was created in previous tests
        response = self.client.get('/agent/1')
        self.assertEqual(response.status_code, 200)
        agent = json.loads(response.data.decode('utf-8'))
        self.assertEqual(agent['id'], 1)
        self.assertEqual(agent['name'], "TestAgent")

if __name__ == '__main__':
    unittest.main()
