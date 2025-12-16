"""
Logging Configuration

Provides structured logging throughout the framework.
Logs to console and file with appropriate levels per environment.

Usage:
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Test started")
    logger.error("Something failed")
"""

import logging
import os
from pathlib import Path
from config.settings import config


# Create logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log filename based on environment
LOG_FILE = LOGS_DIR / f"{config.env}.log"


def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        # Get log level from config
        log_level = config.logging.get("level", "INFO")
        logger.setLevel(getattr(logging, log_level))
        
        # Console handler (always)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))
        
        # File handler (if enabled in config)
        file_handler = None
        if config.logging.get("to_file", True):
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setLevel(getattr(logging, log_level))
        
        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if file_handler:
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

