# Integration tests 
# tests/integration_tests/test_integration.py

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database_models.models import Base, Agent, Post, Interaction, AgentRelationship
from services.agent_service import AgentService
from config.config import Config


class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the testing environment
        cls.engine = create_engine(Config.DATABASE_URI)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.agent_service = AgentService(Config.LLM_MODEL_NAME)

    @classmethod
    def tearDownClass(cls):
        # Tear down the testing environment
        cls.session.close()
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_agent_creation_and_retrieval(self):
        # Test the creation of an agent and retrieval from the database

        # Create an agent
        agent = self.agent_service.create_agent("IntegrationTestAgent", "INTJ")

        # Retrieve the agent from the database
        retrieved_agent = self.session.query(Agent).filter_by(name="IntegrationTestAgent").first()

        self.assertIsNotNone(retrieved_agent)
        self.assertEqual(retrieved_agent.name, "IntegrationTestAgent")
        self.assertEqual(retrieved_agent.personality_type, "INTJ")

    def test_post_creation_and_retrieval(self):
        # Test the creation of a post and retrieval from the database

        # Create an agent first
        agent = self.agent_service.create_agent("PostTestAgent", "ENTJ")

        # Generate a post for the agent
        post_response = self.agent_service.generate_post(agent_name="PostTestAgent", prompt="Integration test prompt.")
        self.assertIn("post_content", post_response)

        # Retrieve the post from the database
        retrieved_post = self.session.query(Post).filter_by(agent_id=agent['id']).first()

        self.assertIsNotNone(retrieved_post)
        self.assertIn("Integration test prompt", retrieved_post.content)

    def test_interaction_creation_and_retrieval(self):
        # Test the creation of an interaction and retrieval from the database

        # Create two agents
        agent1 = self.agent_service.create_agent("InteractingAgent1", "ISTP")
        agent2 = self.agent_service.create_agent("InteractingAgent2", "ESTP")

        # Generate a post for the first agent
        self.agent_service.generate_post(agent_name="InteractingAgent1", prompt="Post for interaction test.")

        # Simulate an interaction from the second agent
        interaction_response = self.agent_service.interact(agent_name="InteractingAgent2", interaction_type="comment",
                                                           content="This is a test comment.")
        self.assertIn("interaction_content", interaction_response)

        # Retrieve the interaction from the database
        retrieved_interaction = self.session.query(Interaction).filter_by(agent_id=agent2['id']).first()

        self.assertIsNotNone(retrieved_interaction)
        self.assertEqual(retrieved_interaction.content, "This is a test comment.")

    def test_agent_relationship_creation(self):
        # Test the creation of a relationship between two agents

        # Create two agents
        agent1 = self.agent_service.create_agent("AgentWithRelationship1", "ISFP")
        agent2 = self.agent_service.create_agent("AgentWithRelationship2", "ESFP")

        # Create a relationship between the two agents
        relationship_response = self.agent_service.create_relationship(agent1['id'], agent2['id'], "friend")

        self.assertIn("relationship_type", relationship_response)
        self.assertEqual(relationship_response['relationship_type'], "friend")

        # Retrieve the relationship from the database
        retrieved_relationship = self.session.query(AgentRelationship).filter_by(agent_id=agent1['id']).first()

        self.assertIsNotNone(retrieved_relationship)
        self.assertEqual(retrieved_relationship.related_agent_id, agent2['id'])
        self.assertEqual(retrieved_relationship.relationship_type, "friend")


if __name__ == '__main__':
    unittest.main()
