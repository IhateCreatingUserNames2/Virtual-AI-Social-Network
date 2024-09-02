# Logging configuration 
# config/logging_config.py

import os
import logging
import sys
from logging.config import dictConfig
from loguru import logger

class InterceptHandler(logging.Handler):
    """
    Default handler to route standard logging messages to Loguru.
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        level = logger.level(record.levelname).name if logger.level(record.levelname) else record.levelno
        logger.log(level, record.getMessage())

def setup_logging():
    """
    Set up logging configuration using Loguru and standard logging.
    This allows for Loguru to capture logs from libraries using the standard logging module.
    """
    LOG_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO').upper()

    # Remove default handlers for Loguru to avoid duplication
    logger.remove()

    # Add custom handler with configuration
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    # Set up standard logging interception
    logging.basicConfig(handlers=[InterceptHandler()], level=LOG_LEVEL)
    logging.getLogger().handlers = [InterceptHandler()]

    # Example of setting log level for external libraries (e.g., SQLAlchemy)
    logging.getLogger('sqlalchemy').setLevel(LOG_LEVEL)

# Example usage
if __name__ == '__main__':
    setup_logging()
    logger.info("Logging is set up.")
