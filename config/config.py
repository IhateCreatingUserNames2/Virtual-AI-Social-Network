# config/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'

    # LLM Model Configuration
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER') or 'ollama'  # Default to Ollama, but can be changed
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME') or 'llama3'  # Default model name


    # Ollama and LLaMA specific configurations
    OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL') or 'http://127.0.0.1:11434'  # Updated to correct port for Ollama
    LLAMA_MODEL_PATH = os.environ.get('LLAMA_MODEL_PATH') or '/path/to/llama/model'  # Path to self-hosted LLaMA model

    # OpenAI specific configurations
    OPENAI_API_KEY = ''
    OPENAI_MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME') or 'gpt-3.5-turbo'  # Default OpenAI model

    # Add any additional configuration options you might need
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = os.environ.get('TESTING') or False
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'INFO'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://user:password@localhost/dbname'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///dev.db'

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///test.db'
