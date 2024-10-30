import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from helpers.utilities import setup_logging, log_message
from models.user_model import User
from config.config import APP_TITLE

def authenticate_user():
    """
    Mock authentication function. In a production application, 
    this would involve a login form and actual authentication logic.
    """
    # Sample user data for demonstration
    sample_users = [
        {"user_id": 1, "username": "alice", "role": "user"},
        {"user_id": 2, "username": "bob", "role": "user"},
        {"user_id": 3, "username": "charlie", "role": "staff"},
    ]
    
    # Simulate a login by selecting a user (for demo purposes)
    selected_user = sample_users[2]  # This could be dynamically selected
    return selected_user["user_id"], selected_user["role"]

def main():
    # Initialize logging
    setup_logging()
    log_message("Starting IT Help Desk Application.")

    # Authenticate the user
    user_id, user_role = authenticate_user()
    log_message(f"Authenticated user ID: {user_id} with role: {user_role}")

    # Initialize the application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)

    # Create and show the main window
    main_window = MainWindow(user_id=user_id, user_role=user_role)
    main_window.show()

    # Handle app exit
    try:
        sys.exit(app.exec_())
    except Exception as e:
        log_message(f"Application exited with error: {e}", level="error")
        QMessageBox.critical(None, "Application Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
