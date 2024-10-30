import sqlite3
import sys
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from IT_help_desk.config.config import DB_PATH

class DBManager:
    @staticmethod
    def execute_query(query, params=(), fetch_one=False, fetch_all=False):
        """
        Executes a query with given parameters and fetch options.
        - fetch_one: Returns a single result.
        - fetch_all: Returns all results.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    # ---------------------
    # User Management
    # ---------------------
    
    @staticmethod
    def add_user(username, role):
        """
        Adds a new user with specified username and role.
        """
        query = "INSERT INTO users (username, role) VALUES (?, ?)"
        DBManager.execute_query(query, (username, role))

    @staticmethod
    def get_user_by_username(username):
        """
        Fetches a user by their username.
        """
        query = "SELECT * FROM users WHERE username = ?"
        return DBManager.execute_query(query, (username,), fetch_one=True)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetches a user by their user ID.
        """
        query = "SELECT * FROM users WHERE id = ?"
        return DBManager.execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user by their user ID.
        """
        query = "DELETE FROM users WHERE id = ?"
        DBManager.execute_query(query, (user_id,))

    # ---------------------
    # Ticket Management
    # ---------------------
    
    @staticmethod
    def add_ticket(user_id, title, description):
        """
        Adds a new ticket with user_id, title, and description.
        """
        query = "INSERT INTO tickets (user_id, title, description) VALUES (?, ?, ?)"
        DBManager.execute_query(query, (user_id, title, description))

    @staticmethod
    def get_ticket_by_id(ticket_id):
        """
        Fetches a ticket by its ticket ID.
        """
        query = "SELECT * FROM tickets WHERE id = ?"
        return DBManager.execute_query(query, (ticket_id,), fetch_one=True)

    @staticmethod
    def get_tickets_by_user_id(user_id, status=None):
        """
        Fetches all tickets for a given user, with an optional status filter.
        """
        query = "SELECT * FROM tickets WHERE user_id = ?"
        params = [user_id]
        if status:
            query += " AND status = ?"
            params.append(status)
        return DBManager.execute_query(query, params, fetch_all=True)

    @staticmethod
    def get_all_tickets(status=None):
        """
        Fetches all tickets, optionally filtered by status.
        """
        query = "SELECT * FROM tickets"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        return DBManager.execute_query(query, params, fetch_all=True)

    @staticmethod
    def update_ticket_status(ticket_id, status):
        """
        Updates the status of a ticket by its ID.
        """
        query = "UPDATE tickets SET status = ? WHERE id = ?"
        DBManager.execute_query(query, (status, ticket_id))

    @staticmethod
    def assign_ticket(ticket_id, assigned_to):
        """
        Assigns a ticket to a staff member by updating the assigned_to field.
        """
        query = "UPDATE tickets SET assigned_to = ? WHERE id = ?"
        DBManager.execute_query(query, (assigned_to, ticket_id))

    @staticmethod
    def resolve_ticket(ticket_id, resolution):
        """
        Resolves a ticket by updating its status to 'Resolved' and adding resolution notes.
        """
        query = "UPDATE tickets SET status = 'Resolved', resolution = ? WHERE id = ?"
        DBManager.execute_query(query, (resolution, ticket_id))

    @staticmethod
    def delete_ticket(ticket_id):
        """
        Deletes a ticket by its ID.
        """
        query = "DELETE FROM tickets WHERE id = ?"
        DBManager.execute_query(query, (ticket_id,))
