import sqlite3
from config.config import DB_PATH
from helpers.utilities import log_message

class User:
    def __init__(self, username, role, user_id=None):
        self.user_id = user_id
        self.username = username
        self.role = role

    # ---------------------
    # Static Methods
    # ---------------------

    @staticmethod
    def create_user(username, role):
        """
        Creates a new user in the database.
        """
        query = "INSERT INTO users (username, role) VALUES (?, ?)"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, role))
            conn.commit()
            user_id = cursor.lastrowid
            log_message(f"User '{username}' created with role '{role}'.")
            return user_id

    @staticmethod
    def get_user_by_username(username):
        """
        Retrieves a user from the database by their username.
        """
        query = "SELECT * FROM users WHERE username = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                return User(row[1], row[2], user_id=row[0])  # Return User instance
            else:
                log_message(f"User with username '{username}' not found.", level="warning")
                return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user from the database by their user ID.
        """
        query = "SELECT * FROM users WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                return User(row[1], row[2], user_id=row[0])  # Return User instance
            else:
                log_message(f"User with ID '{user_id}' not found.", level="warning")
                return None

    @staticmethod
    def update_user_role(user_id, new_role):
        """
        Updates the role of a user in the database.
        """
        query = "UPDATE users SET role = ? WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_role, user_id))
            conn.commit()
            log_message(f"User ID {user_id} role updated to '{new_role}'.")

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user from the database by their user ID.
        """
        query = "DELETE FROM users WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            log_message(f"User ID {user_id} deleted.")

    @staticmethod
    def get_all_users():
        """
        Retrieves all users from the database.
        """
        query = "SELECT * FROM users"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            users = [User(row[1], row[2], user_id=row[0]) for row in rows]  # List of User instances
            return users
