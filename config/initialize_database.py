import sqlite3
import sys
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from IT_help_desk.config.config import DB_PATH
from IT_help_desk.helpers.utilities import log_message

def initialize_database():
    """
    Initializes the database by creating the necessary tables if they do not exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL
            )
        ''')

        # Create tickets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                assigned_to TEXT,
                resolution TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Insert default users if none exist
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ('alice', 'user'),
                ('bob', 'user'),
                ('charlie', 'staff')  # Example IT staff member
            ]
            cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)", users)
            log_message("Default users added to the database.")

        log_message("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
