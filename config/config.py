import os

# Database Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'helpdesk.db')

# Mistral 7B AI Configuration
MISTRAL_API_ENDPOINT = "https://api.mistral.ai/v1/generate"  # Replace with the actual endpoint
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "your-default-api-key")  # API key for authentication

# Application Settings
APP_TITLE = "IT Help Desk"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Default Users for Testing (Only Used When Initializing the Database)
DEFAULT_USERS = [
    ("alice", "user"),
    ("bob", "user"),
    ("victor", "staff")
]

# Paths for Resources
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')
STYLESHEET_PATH = os.path.join(RESOURCES_DIR, 'styles.qss')
ICONS_DIR = os.path.join(RESOURCES_DIR, 'icons')

# Log Configuration
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Ensure necessary directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

