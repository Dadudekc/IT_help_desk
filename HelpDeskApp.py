import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QTableWidget,
    QTableWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt

class HelpDeskApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_role = self.get_user_role(username)
        self.user_id = self.get_user_id(username)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("IT Help Desk")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Welcome Label
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_submit_ticket_tab(), "Submit Ticket")
        tabs.addTab(self.create_view_tickets_tab(), "View Tickets")
        if self.user_role == 'staff':
            tabs.addTab(self.create_manage_tickets_tab(), "Manage Tickets")
        layout.addWidget(tabs)

        self.setLayout(layout)

    def create_submit_ticket_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Ticket Title
        title_label = QLabel("Ticket Title:")
        self.title_input = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)

        # Ticket Description
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)

        # Submit Button
        submit_button = QPushButton("Submit Ticket")
        submit_button.clicked.connect(self.submit_ticket)
        layout.addWidget(submit_button)

        tab.setLayout(layout)
        return tab

    def create_view_tickets_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Filter by Status
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Status:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Open", "In Progress", "Resolved", "Closed"])
        self.status_filter.currentIndexChanged.connect(self.load_tickets)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.status_filter)
        layout.addLayout(filter_layout)

        # Tickets Table
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(5)
        self.tickets_table.setHorizontalHeaderLabels(["ID", "Title", "Status", "Assigned To", "Resolution"])
        self.tickets_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tickets_table)

        tab.setLayout(layout)
        return tab

    def create_manage_tickets_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Tickets Table for Staff
        self.staff_tickets_table = QTableWidget()
        self.staff_tickets_table.setColumnCount(7)
        self.staff_tickets_table.setHorizontalHeaderLabels(["ID", "Title", "Status", "Assigned To", "Resolution", "Assign", "Resolve"])
        self.staff_tickets_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.staff_tickets_table)

        # Load Tickets Button
        load_button = QPushButton("Load Tickets")
        load_button.clicked.connect(self.load_staff_tickets)
        layout.addWidget(load_button)

        tab.setLayout(layout)
        return tab

    def get_user_role(self, username):
        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'user'

    def get_user_id(self, username):
        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def submit_ticket(self):
        title = self.title_input.text().strip()
        description = self.desc_input.toPlainText().strip()

        if not title or not description:
            QMessageBox.warning(self, "Input Error", "Please provide both title and description.")
            return

        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (user_id, title, description)
            VALUES (?, ?, ?)
        """, (self.user_id, title, description))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Your ticket has been submitted successfully!")
        self.title_input.clear()
        self.desc_input.clear()
        self.load_tickets()

    def load_tickets(self):
        status = self.status_filter.currentText()
        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()

        if self.user_role == 'staff':
            query = "SELECT id, title, status, assigned_to, resolution FROM tickets"
            cursor.execute(query)
        else:
            query = "SELECT id, title, status, assigned_to, resolution FROM tickets WHERE user_id = ?"
            cursor.execute(query, (self.user_id,))

        tickets = cursor.fetchall()
        conn.close()

        # Filter tickets based on status
        if status != "All":
            tickets = [ticket for ticket in tickets if ticket[2] == status]

        self.tickets_table.setRowCount(len(tickets))
        for row_idx, ticket in enumerate(tickets):
            for col_idx, item in enumerate(ticket):
                self.tickets_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def load_staff_tickets(self):
        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status, assigned_to, resolution FROM tickets")
        tickets = cursor.fetchall()
        conn.close()

        self.staff_tickets_table.setRowCount(len(tickets))
        for row_idx, ticket in enumerate(tickets):
            for col_idx, item in enumerate(ticket):
                self.staff_tickets_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

            # Assign Button
            assign_button = QPushButton("Assign")
            assign_button.clicked.connect(lambda checked, tid=ticket[0]: self.assign_ticket(tid))
            self.staff_tickets_table.setCellWidget(row_idx, 5, assign_button)

            # Resolve Button
            resolve_button = QPushButton("Resolve")
            resolve_button.clicked.connect(lambda checked, tid=ticket[0]: self.resolve_ticket(tid))
            self.staff_tickets_table.setCellWidget(row_idx, 6, resolve_button)

    def assign_ticket(self, ticket_id):
        assign_to, ok = QInputDialog.getText(self, "Assign Ticket", "Enter username to assign:")
        if ok and assign_to.strip():
            conn = sqlite3.connect('helpdesk.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (assign_to.strip(),))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE tickets SET assigned_to = ? WHERE id = ?", (assign_to.strip(), ticket_id))
                conn.commit()
                QMessageBox.information(self, "Success", f"Ticket {ticket_id} assigned to {assign_to.strip()}.")
                conn.close()
                self.load_staff_tickets()
            else:
                QMessageBox.warning(self, "Error", "Username not found.")
                conn.close()

    def resolve_ticket(self, ticket_id):
        resolution, ok = QInputDialog.getText(self, "Resolve Ticket", "Enter resolution details:")
        if ok and resolution.strip():
            conn = sqlite3.connect('helpdesk.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status = 'Resolved', resolution = ? WHERE id = ?", (resolution.strip(), ticket_id))
            conn.commit()
            QMessageBox.information(self, "Success", f"Ticket {ticket_id} has been resolved.")
            conn.close()
            self.load_staff_tickets()

def login():
    app = QApplication(sys.argv)
    login_window = QWidget()
    login_window.setWindowTitle("IT Help Desk - Login")
    login_window.setGeometry(100, 100, 300, 150)

    layout = QVBoxLayout()

    # Username
    user_layout = QHBoxLayout()
    user_label = QLabel("Username:")
    user_input = QLineEdit()
    user_layout.addWidget(user_label)
    user_layout.addWidget(user_input)
    layout.addLayout(user_layout)

    # Password (optional: for simplicity, we're not handling passwords here)
    # You can expand this to include password fields and authentication.

    # Login Button
    login_button = QPushButton("Login")
    layout.addWidget(login_button)

    login_window.setLayout(layout)

    def handle_login():
        username = user_input.text().strip()
        if not username:
            QMessageBox.warning(login_window, "Input Error", "Please enter your username.")
            return

        # Check if user exists
        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            login_window.close()
            main_app = HelpDeskApp(username)
            main_app.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.warning(login_window, "Login Failed", "Username not found.")

    login_button.clicked.connect(handle_login)
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    login()
