# Unit tests 
# tests/unit_tests/test_unit.py

import unittest
from services.personality_service import PersonalityService
from models.ml_models.agent_llm import AgentLLM
from unittest.mock import patch, MagicMock

class TestPersonalityService(unittest.TestCase):
    def setUp(self):
        self.personality_service = PersonalityService()

    @patch('services.personality_service.PersonalityService.load_personalities')
    def test_load_personalities(self, mock_load_personalities):
        # Mock the load_personalities method
        mock_load_personalities.return_value = {'INTP': 'Lógico'}

        personalities = self.personality_service.load_personalities()
        self.assertEqual(personalities, {'INTP': 'Lógico'})
        mock_load_personalities.assert_called_once()

    def test_get_personality(self):
        # Test getting a personality that exists
        personality = self.personality_service.get_personality('INTP')
        self.assertEqual(personality, 'Lógico')

        # Test getting a personality that does not exist (should return 'neutral')
        personality = self.personality_service.get_personality('XYZ')
        self.assertEqual(personality, 'neutral')

class TestAgentLLM(unittest.TestCase):
    def setUp(self):
        # We can use a mock or the actual model name if testing with real models
        self.agent_llm = AgentLLM(model_name='gpt-3')

    @patch('models.ml_models.agent_llm.AgentLLM._generate_with_openai')
    def test_generate_response_openai(self, mock_generate_with_openai):
        # Mock the OpenAI response generation
        mock_generate_with_openai.return_value = "This is a test response."

        response = self.agent_llm.generate_response("Hello", "INTP")
        self.assertEqual(response, "This is a test response.")
        mock_generate_with_openai.assert_called_once_with("Hello", "INTP")

    @patch('models.ml_models.agent_llm.AgentLLM._generate_with_ollama')
    def test_generate_response_ollama(self, mock_generate_with_ollama):
        # Mock the Ollama response generation
        mock_generate_with_ollama.return_value = "This is a test response from Ollama."

        # Temporarily set the provider to Ollama for testing
        self.agent_llm.llm_provider = 'ollama'
        response = self.agent_llm.generate_response("Hello", "ENTP")
        self.assertEqual(response, "This is a test response from Ollama.")
        mock_generate_with_ollama.assert_called_once_with("Hello", "ENTP")

    @patch('models.ml_models.agent_llm.AgentLLM._generate_with_llama')
    def test_generate_response_llama(self, mock_generate_with_llama):
        # Mock the LLaMA response generation
        mock_generate_with_llama.return_value = "This is a test response from LLaMA."

        # Temporarily set the provider to LLaMA for testing
        self.agent_llm.llm_provider = 'llama'
        response = self.agent_llm.generate_response("Hello", "ENFP")
        self.assertEqual(response, "This is a test response from LLaMA.")
        mock_generate_with_llama.assert_called_once_with("Hello", "ENFP")

if __name__ == '__main__':
    unittest.main()
