from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from models.ticket_model import Ticket
from helpers.utilities import log_message

class ManageTicketsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout for the manage tickets tab
        main_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Manage Tickets")
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
        self.ticket_table.setColumnCount(5)
        self.ticket_table.setHorizontalHeaderLabels(["Ticket ID", "User ID", "Title", "Status", "Assigned To"])
        self.ticket_table.setColumnWidth(2, 200)  # Set title column width for better readability
        self.ticket_table.cellDoubleClicked.connect(self.open_ticket_details)
        main_layout.addWidget(self.ticket_table)

        # Assignment Layout
        assignment_layout = QHBoxLayout()

        # Ticket ID Input
        assignment_layout.addWidget(QLabel("Ticket ID:"))
        self.ticket_id_input = QLineEdit()
        assignment_layout.addWidget(self.ticket_id_input)

        # Assigned To Input
        assignment_layout.addWidget(QLabel("Assign To:"))
        self.assign_to_input = QLineEdit()
        assignment_layout.addWidget(self.assign_to_input)

        # Update Status Dropdown
        self.status_update = QComboBox()
        self.status_update.addItems(["Open", "In Progress", "Resolved"])
        assignment_layout.addWidget(QLabel("Update Status:"))
        assignment_layout.addWidget(self.status_update)

        # Assign Button
        assign_button = QPushButton("Assign/Update Ticket")
        assign_button.clicked.connect(self.assign_ticket)
        assignment_layout.addWidget(assign_button)

        main_layout.addLayout(assignment_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Initial ticket load
        self.load_tickets()

    def load_tickets(self):
        """
        Loads tickets from the database and populates the ticket table.
        """
        status_filter = self.status_filter.currentText()
        if status_filter == "All":
            tickets = Ticket.get_all_tickets()
        else:
            tickets = Ticket.get_all_tickets(status=status_filter)

        self.ticket_table.setRowCount(0)  # Clear existing rows
        for ticket in tickets:
            row_position = self.ticket_table.rowCount()
            self.ticket_table.insertRow(row_position)
            self.ticket_table.setItem(row_position, 0, QTableWidgetItem(str(ticket.ticket_id)))
            self.ticket_table.setItem(row_position, 1, QTableWidgetItem(str(ticket.user_id)))
            self.ticket_table.setItem(row_position, 2, QTableWidgetItem(ticket.title))
            self.ticket_table.setItem(row_position, 3, QTableWidgetItem(ticket.status))
            self.ticket_table.setItem(row_position, 4, QTableWidgetItem(ticket.assigned_to or ""))

        log_message("Tickets loaded into Manage Tickets tab.")

    def open_ticket_details(self, row, column):
        """
        Opens a detailed view of the ticket when a table row is double-clicked.
        """
        ticket_id = int(self.ticket_table.item(row, 0).text())
        ticket = Ticket.get_ticket_by_id(ticket_id)

        if ticket:
            details = (f"Ticket ID: {ticket_id}\n"
                       f"User ID: {ticket.user_id}\n"
                       f"Title: {ticket.title}\n"
                       f"Description: {ticket.description}\n"
                       f"Status: {ticket.status}\n"
                       f"Assigned To: {ticket.assigned_to or 'Unassigned'}\n"
                       f"Resolution: {ticket.resolution or 'Not resolved yet'}")
            QMessageBox.information(self, "Ticket Details", details)
        else:
            QMessageBox.warning(self, "Error", "Ticket not found.")
            log_message(f"Error: Ticket ID {ticket_id} not found.", level="warning")

    def assign_ticket(self):
        """
        Assigns a ticket to a staff member and updates its status based on user input.
        """
        ticket_id_text = self.ticket_id_input.text().strip()
        assign_to = self.assign_to_input.text().strip()
        new_status = self.status_update.currentText()

        if not ticket_id_text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Ticket ID must be a number.")
            return

        ticket_id = int(ticket_id_text)
        ticket = Ticket.get_ticket_by_id(ticket_id)
        if not ticket:
            QMessageBox.warning(self, "Error", "Ticket not found.")
            return

        if assign_to:
            Ticket.assign_ticket(ticket_id, assign_to)
            log_message(f"Ticket ID {ticket_id} assigned to '{assign_to}'.")

        Ticket.update_ticket_status(ticket_id, new_status)
        log_message(f"Ticket ID {ticket_id} status updated to '{new_status}'.")

        # Reload the tickets to reflect changes
        self.load_tickets()

        # Clear input fields
        self.ticket_id_input.clear()
        self.assign_to_input.clear()
        self.status_update.setCurrentIndex(0)

        QMessageBox.information(self, "Success", "Ticket updated successfully.")
