from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
import sys

from ui.submit_ticket_tab import SubmitTicketTab
from ui.view_tickets_tab import ViewTicketsTab
from ui.manage_tickets_tab import ManageTicketsTab
from ui.ai_assistant_tab import AIAssistantTab
from helpers.utilities import setup_logging, log_message
from config.config import APP_TITLE, APP_VERSION, ICONS_DIR

class MainWindow(QMainWindow):
    def __init__(self, user_id, user_role):
        super().__init__()

        # Store user information
        self.user_id = user_id
        self.user_role = user_role

        # Set up logging
        setup_logging()
        log_message("Application started.")

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Main window settings
        self.setWindowTitle(f"{APP_TITLE} - v{APP_VERSION}")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon(f"{ICONS_DIR}/app_icon.png"))

        # Set up tabs
        self.tabs = QTabWidget()

        # Add Submit and View Tickets tabs for all users
        self.tabs.addTab(SubmitTicketTab(self.user_id), "Submit Ticket")
        self.tabs.addTab(ViewTicketsTab(self.user_id), "View Tickets")

        # Add Manage Tickets tab only for staff users
        if self.user_role == "staff":
            self.tabs.addTab(ManageTicketsTab(), "Manage Tickets")

        # Add AI Assistant tab for all users
        self.tabs.addTab(AIAssistantTab(), "AI Assistant")

        # Set the central widget
        self.setCentralWidget(self.tabs)

        # Set up the menu bar
        self.init_menu_bar()

    def init_menu_bar(self):
        # Create main menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About action
        about_action = QAction("About", self)
        about_action.setStatusTip("About the application")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def close_application(self):
        """
        Handles closing the application with confirmation.
        """
        reply = QMessageBox.question(self, "Exit Application",
                                     "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            log_message("Application closed.")
            QApplication.instance().quit()

    def show_about_dialog(self):
        """
        Displays an About dialog with application information.
        """
        QMessageBox.about(self, "About",
                          f"{APP_TITLE} v{APP_VERSION}\n"
                          "An IT Help Desk application powered by Mistral 7B AI.\n\n"
                          "Developed by FreeRideInvestor.")

    def closeEvent(self, event):
        """
        Override closeEvent to handle application close with logging.
        """
        log_message("Application closed via closeEvent.")
        event.accept()

# Main entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example user information
    user_id = 1  # Replace with actual user authentication
    user_role = "staff"  # Replace with actual role, e.g., "user" or "staff"

    main_window = MainWindow(user_id, user_role)
    main_window.show()
    sys.exit(app.exec_())
