import os
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from IT_help_desk.config.config import LOG_FILE, LOG_DIR

# ---------------------
# Logging Configuration
# ---------------------

def setup_logging():
    """
    Sets up the logging configuration to log messages to a file.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def log_message(message, level="info"):
    """
    Logs a message at the specified level.
    """
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "debug":
        logging.debug(message)

# ---------------------
# Text and Data Utilities
# ---------------------

def format_date(date_str, date_format="%Y-%m-%d"):
    """
    Converts a date string to a specified format.
    - date_str: A date string to be formatted.
    - date_format: The target date format (default: "YYYY-MM-DD").
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime(date_format)
    except ValueError:
        return "Invalid date"

def truncate_text(text, max_length=100):
    """
    Truncates text to a specified maximum length.
    """
    return text if len(text) <= max_length else text[:max_length] + "..."

# ---------------------
# File Utilities
# ---------------------

def ensure_directory(path):
    """
    Ensures that a directory exists; creates it if it doesn't.
    """
    os.makedirs(path, exist_ok=True)

def clear_log_file():
    """
    Clears the contents of the log file.
    """
    with open(LOG_FILE, 'w'):
        pass
    log_message("Log file cleared.", level="info")
