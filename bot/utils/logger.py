"""
Logging configuration for the bot.
"""
import logging
import sys
from pathlib import Path

from config import settings


def setup_logger():
    """
    Configure logging for the bot.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler
            logging.FileHandler(
                logs_dir / "bot.log",
                encoding="utf-8"
            )
        ]
    )
    
    # Set aiogram logging level
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
