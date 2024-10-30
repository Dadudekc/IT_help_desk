from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from models.ticket_model import Ticket
from helpers.utilities import log_message

class SubmitTicketTab(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # Store the user ID to associate with the ticket
        self.init_ui()

    def init_ui(self):
        # Main layout for the submit ticket tab
        main_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Submit a New Ticket")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Ticket Title Input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter ticket title (e.g., 'VPN connection issue')")
        main_layout.addWidget(QLabel("Title:"))
        main_layout.addWidget(self.title_input)

        # Ticket Description Input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe the issue in detail...")
        main_layout.addWidget(QLabel("Description:"))
        main_layout.addWidget(self.description_input)

        # Submit Button
        submit_button = QPushButton("Submit Ticket")
        submit_button.clicked.connect(self.submit_ticket)
        main_layout.addWidget(submit_button)

        # Set the main layout
        self.setLayout(main_layout)

    def submit_ticket(self):
        """
        Handles ticket submission by saving the ticket details to the database.
        """
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        # Input validation
        if not title or not description:
            QMessageBox.warning(self, "Input Error", "Please fill in both the title and description.")
            return

        try:
            # Create a new ticket in the database
            ticket_id = Ticket.create_ticket(self.user_id, title, description)
            log_message(f"Ticket {ticket_id} submitted by User ID {self.user_id} with title '{title}'.")

            # Display success message and clear input fields
            QMessageBox.information(self, "Success", "Ticket submitted successfully!")
            self.title_input.clear()
            self.description_input.clear()

        except Exception as e:
            # Handle any errors that occur during ticket creation
            log_message(f"Error submitting ticket: {e}", level="error")
            QMessageBox.critical(self, "Submission Error", "An error occurred while submitting the ticket.")
