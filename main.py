# Entry point for Flask app 
# main.py

from flask import Flask
from config.config import Config
from routes.routes import app
from config.logging_config import setup_logging

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

    # Run the app
    application.run(host='0.0.0.0', port=8000)
