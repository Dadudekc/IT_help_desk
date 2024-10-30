import sqlite3
from config.config import DB_PATH
from helpers.utilities import log_message

class Ticket:
    def __init__(self, user_id, title, description, status="Open", assigned_to=None, resolution=None):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.resolution = resolution

    # ---------------------
    # Static Methods
    # ---------------------

    @staticmethod
    def create_ticket(user_id, title, description):
        """
        Creates a new ticket in the database.
        Returns the ID of the created ticket.
        """
        query = "INSERT INTO tickets (user_id, title, description, status) VALUES (?, ?, ?, 'Open')"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, title, description))
            conn.commit()
            ticket_id = cursor.lastrowid
            log_message(f"Ticket {ticket_id} created with title '{title}'.")
            return ticket_id

    @staticmethod
    def get_ticket_by_id(ticket_id):
        """
        Retrieves a ticket by its ID.
        Returns a Ticket instance or None if not found.
        """
        query = "SELECT * FROM tickets WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ticket_id,))
            row = cursor.fetchone()
            if row:
                return Ticket(*row[1:])  # Unpack row data to initialize Ticket instance
            log_message(f"Ticket with ID {ticket_id} not found.", level="warning")
            return None

    @staticmethod
    def get_tickets_by_user(user_id, status=None):
        """
        Retrieves all tickets for a specific user, optionally filtered by status.
        Returns a list of Ticket instances.
        """
        query = "SELECT * FROM tickets WHERE user_id = ?"
        params = [user_id]
        if status:
            query += " AND status = ?"
            params.append(status)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            tickets = [Ticket(*row[1:]) for row in rows]  # Exclude 'id' field from row
            log_message(f"Retrieved {len(tickets)} tickets for user ID {user_id}.")
            return tickets

    @staticmethod
    def get_all_tickets(status=None):
        """
        Retrieves all tickets, optionally filtered by status.
        Returns a list of Ticket instances.
        """
        query = "SELECT * FROM tickets"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            tickets = [Ticket(*row[1:]) for row in rows]
            log_message(f"Retrieved {len(tickets)} tickets with status '{status}'.")
            return tickets

    @staticmethod
    def update_ticket_status(ticket_id, status):
        """
        Updates the status of a specified ticket.
        """
        query = "UPDATE tickets SET status = ? WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (status, ticket_id))
            conn.commit()
            log_message(f"Ticket {ticket_id} status updated to '{status}'.")

    @staticmethod
    def assign_ticket(ticket_id, assigned_to):
        """
        Assigns a ticket to a specified staff member.
        """
        query = "UPDATE tickets SET assigned_to = ? WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (assigned_to, ticket_id))
            conn.commit()
            log_message(f"Ticket {ticket_id} assigned to '{assigned_to}'.")

    @staticmethod
    def resolve_ticket(ticket_id, resolution):
        """
        Resolves a ticket by updating its status to 'Resolved' and adding a resolution note.
        """
        query = "UPDATE tickets SET status = 'Resolved', resolution = ? WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (resolution, ticket_id))
            conn.commit()
            log_message(f"Ticket {ticket_id} resolved with resolution: '{resolution}'.")

    @staticmethod
    def delete_ticket(ticket_id):
        """
        Deletes a ticket from the database.
        """
        query = "DELETE FROM tickets WHERE id = ?"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (ticket_id,))
            conn.commit()
            log_message(f"Ticket {ticket_id} deleted.")
