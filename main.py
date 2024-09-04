# Entry point for Flask app
# main.py

from flask import Flask
from config.config import Config
from routes.routes import app
from config.logging_config import setup_logging
from services.agent_service import AgentService

def create_app():
    """
    Application factory for creating and configuring the Flask app.
    """
    # Configure logging
    setup_logging()

    # Additional app configuration
    app.config.from_object(Config)

    # Here you could initialize other parts of the application, e.g.,
    # - Initialize database connections
    # - Register blueprints
    # - Set up error handlers

    return app

if __name__ == '__main__':
    # Create the Flask app
    application = create_app()

    # Initialize AgentService with the model name
    agent_service = AgentService(model_name="llama3")

    # Calculate the median humor value and store it
    median_humor = agent_service.calculate_whole_median_humor()

    # Run the app
    application.run(host='0.0.0.0', port=8000)
