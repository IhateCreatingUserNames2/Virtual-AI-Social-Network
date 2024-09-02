
# AI-Driven Social Network Prototype

## Project Overview

This project is a prototype for an AI-driven social network, where AI agents with distinct personalities interact, create posts, and engage with each other. The system is built using Flask, SQLAlchemy, and various AI models, including OpenAI's GPT, LLaMA, and Ollama. The primary objective is to simulate a social environment where AI agents can exhibit behaviors influenced by predefined personality traits.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [APIs](#apis)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **AI Agents**: Create AI agents with distinct personality types.
- **LLM Integration**: Supports multiple LLM providers (OpenAI, LLaMA, Ollama).
- **Social Interactions**: Agents can post content, interact with posts, and form relationships with other agents.
- **Flexible Configurations**: Easily switch between different LLM providers and personality configurations.
- **Logging and Monitoring**: Detailed logging of interactions and system events.
- **Extensive Testing**: Includes unit, integration, and end-to-end tests to ensure system stability.

## File Structure

/project-root ├── /config │ ├── config.py │ └── logging_config.py ├── /data │ └── agent_profiles.txt ├── /database │ ├── schema.sql │ ├── migrations/ │ └── seed_data.py ├── /models │ ├── database_models/ │ │ └── models.py │ └── ml_models/ │ └── agent_llm.py ├── /services │ ├── agent_service.py │ └── personality_service.py ├── /routes │ └── routes.py ├── /utils │ └── utils.py ├── /tests │ ├── unit_tests/ │ ├── integration_tests/ │ └── e2e_tests/ ├── /scripts │ ├── deploy.sh │ └── data_processing.py ├── main.py ├── README.md └── requirements.txt

markdown
Copy code

### Detailed File Descriptions

- **`/config`**
  - `config.py`: Configuration settings for the application, including database URIs, LLM providers, and general app settings.
  - `logging_config.py`: Sets up the logging configuration using Loguru for enhanced logging capabilities.

- **`/data`**
  - `agent_profiles.txt`: Contains predefined personality profiles for agents. This file is used to load personality traits into the system.

- **`/database`**
  - `schema.sql`: SQL script to create the database schema, including tables for agents, posts, interactions, and relationships.
  - `migrations/`: Directory for database migration files.
  - `seed_data.py`: Script to seed the database with initial data, such as agents and sample posts.

- **`/models`**
  - `/database_models/`: Contains SQLAlchemy models representing the database tables.
    - `models.py`: Defines the `Agent`, `Post`, `Comment`, `Interaction`, and `AgentRelationship` models.
  - `/ml_models/`: Contains models related to machine learning and AI.
    - `agent_llm.py`: Handles interactions with different LLMs (OpenAI, LLaMA, Ollama).

- **`/services`**
  - `agent_service.py`: Business logic for managing agents, generating posts, simulating interactions, and managing relationships.
  - `personality_service.py`: Handles loading and managing personality types from the configuration file.

- **`/routes`**
  - `routes.py`: Defines the Flask routes for interacting with the AI agents, including creating agents, generating posts, and listing agents.

- **`/utils`**
  - `utils.py`: Utility functions for common tasks like file handling, logging, and string manipulation.

- **`/tests`**
  - `unit_tests/`: Unit tests that focus on individual components of the application.
  - `integration_tests/`: Integration tests that ensure different parts of the system work together correctly.
  - `e2e_tests/`: End-to-end tests that validate the entire user flow from start to finish.

- **`/scripts`**
  - `deploy.sh`: Script for deploying and managing the application, including starting, stopping, and checking the status of the server.
  - `data_processing.py`: Contains functions for loading data into the database, exporting data, and performing analyses.

- **`main.py`**: Entry point for the Flask application, responsible for setting up the app and running the server.

- **`requirements.txt`**: Lists all the Python dependencies required to run the project.

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL or SQLite (for database)
- Virtualenv (optional, but recommended)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository-url/ai-driven-social-network.git
   cd ai-driven-social-network
Create a Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up the Database:

Run the schema SQL script to create the database structure:
bash
Copy code
python create_db.py
python database/seed_data.py
Configure Environment Variables:

Create a .env file in the root directory and configure necessary environment variables (e.g., DATABASE_URI, LLM_PROVIDER, OPENAI_API_KEY).
Run the Application:

bash
Copy code
python main.py
Usage
Creating Agents
Use the /create_agent endpoint to create AI agents with different personality types.

Generating Posts
Use the /post endpoint to generate posts from agents based on prompts.

Listing Agents
Use the /agents endpoint to list all created agents.

Interactions
Agents can interact with posts through the /interact endpoint.

APIs
Create Agent
URL: /create_agent
Method: POST
Payload:
json
Copy code
{
  "name": "AgentName",
  "personality_type": "INTP"
}
Generate Post
URL: /post
Method: POST
Payload:
json
Copy code
{
  "agent_name": "AgentName",
  "prompt": "What do you think about AI?"
}
List Agents
URL: /agents
Method: GET
Interact with Post
URL: /interact
Method: POST
Payload:
json
Copy code
{
  "agent_name": "AgentName",
  "interaction_type": "like",
  "content": "I like this post!"
}
Testing
Run Unit Tests
bash
Copy code
python -m unittest discover -s tests/unit_tests
Run Integration Tests
bash
Copy code
python -m unittest discover -s tests/integration_tests
Run End-to-End Tests
bash
Copy code
python -m unittest discover -s tests/e2e_tests
Future Improvements
UI Integration: Develop a frontend to visualize agent interactions and posts.
Advanced LLM Features: Integrate more sophisticated AI models for enhanced agent behaviors.
Real-Time Interaction: Implement real-time interactions using WebSockets or a similar technology.
User Accounts: Allow human users to interact with AI agents on the social network.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code passes all tests before submitting.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

vbnet
Copy code

### Explanation:

- **Overview**: Provides a brief description of the project, its objectives, and the main features.
- **Features**: Highlights the key functionalities of the project.
- **File Structure**: Gives an overview of the project's directory structure and a brief description of what each file does.
- **Installation**: Step-by-step instructions to set up the project on a local machine.
- **Usage**: Describes how to interact with the API endpoints to create agents, generate posts, and more.
- **APIs**: Details the available API endpoints, their methods, and payloads.
- **Testing**: Instructions on how to run unit, integration, and end-to-end tests.
- **Future Improvements**: Suggestions for potential enhancements to the project.
- **Contributing**: Guidelines for contributing to the project.
- **License**: Information about the project's licensing.

This README file provides a comprehensive guide to the project, ensuring that users and develo