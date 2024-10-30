from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from models.ticket_model import Ticket
from helpers.utilities import log_message

class ViewTicketsTab(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # Store user ID to filter tickets for the logged-in user
        self.init_ui()

    def init_ui(self):
        # Main layout for the view tickets tab
        main_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("My Tickets")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Filter and Refresh Layout
        filter_layout = QHBoxLayout()

        # Status Filter Dropdown
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Open", "In Progress", "Resolved"])
        self.status_filter.currentIndexChanged.connect(self.load_tickets)
        filter_layout.addWidget(QLabel("Filter by Status:"))
        filter_layout.addWidget(self.status_filter)

        # Refresh Button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_tickets)
        filter_layout.addWidget(refresh_button)

        main_layout.addLayout(filter_layout)

        # Ticket Table
        self.ticket_table = QTableWidget()
        self.ticket_table.setColumnCount(4)
        self.ticket_table.setHorizontalHeaderLabels(["Ticket ID", "Title", "Status", "Assigned To"])
        self.ticket_table.setColumnWidth(1, 200)  # Set title column width for better readability
        self.ticket_table.cellDoubleClicked.connect(self.view_ticket_details)
        main_layout.addWidget(self.ticket_table)

        # Set the main layout
        self.setLayout(main_layout)

        # Initial ticket load
        self.load_tickets()

    def load_tickets(self):
        """
        Loads the user's tickets from the database and populates the ticket table.
        """
        status_filter = self.status_filter.currentText()
        if status_filter == "All":
            tickets = Ticket.get_tickets_by_user(self.user_id)
        else:
            tickets = Ticket.get_tickets_by_user(self.user_id, status=status_filter)

        self.ticket_table.setRowCount(0)  # Clear existing rows
        for ticket in tickets:
            row_position = self.ticket_table.rowCount()
            self.ticket_table.insertRow(row_position)
            self.ticket_table.setItem(row_position, 0, QTableWidgetItem(str(ticket.ticket_id)))
            self.ticket_table.setItem(row_position, 1, QTableWidgetItem(ticket.title))
            self.ticket_table.setItem(row_position, 2, QTableWidgetItem(ticket.status))
            self.ticket_table.setItem(row_position, 3, QTableWidgetItem(ticket.assigned_to or ""))

        log_message(f"Loaded tickets for user ID {self.user_id} in View Tickets tab.")

    def view_ticket_details(self, row, column):
        """
        Displays detailed information about the selected ticket.
        """
        ticket_id = int(self.ticket_table.item(row, 0).text())
        ticket = Ticket.get_ticket_by_id(ticket_id)

        if ticket:
            details = (f"Ticket ID: {ticket_id}\n"
                       f"Title: {ticket.title}\n"
                       f"Description: {ticket.description}\n"
                       f"Status: {ticket.status}\n"
                       f"Assigned To: {ticket.assigned_to or 'Unassigned'}\n"
                       f"Resolution: {ticket.resolution or 'Not resolved yet'}")
            QMessageBox.information(self, "Ticket Details", details)
            log_message(f"Displayed details for Ticket ID {ticket_id}.")
        else:
            QMessageBox.warning(self, "Error", "Ticket not found.")
            log_message(f"Error: Ticket ID {ticket_id} not found.", level="warning")
