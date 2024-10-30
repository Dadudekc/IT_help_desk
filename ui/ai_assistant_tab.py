from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from helpers.ai_response_thread import AIResponseThread
from helpers.utilities import log_message

class AIAssistantTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout for the AI assistant tab
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("IT Help Desk AI Assistant")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        # Instruction Label
        instruction_label = QLabel("Enter your question below and press 'Ask AI' to receive assistance:")
        layout.addWidget(instruction_label)

        # Input Field for User's Question
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Type your question here...")
        layout.addWidget(self.question_input)

        # Response Display Area (TextEdit for multiline responses)
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        layout.addWidget(self.response_display)

        # Ask AI Button
        self.ask_button = QPushButton("Ask AI")
        self.ask_button.clicked.connect(self.ask_ai)
        layout.addWidget(self.ask_button)

        # Set main layout
        self.setLayout(layout)

    def ask_ai(self):
        """
        Handles the action when 'Ask AI' button is clicked.
        """
        question = self.question_input.text().strip()
        if question:
            # Log the question for debugging/auditing purposes
            log_message(f"User asked: {question}", level="info")

            # Clear previous response and disable the button to prevent multiple clicks
            self.response_display.clear()
            self.ask_button.setEnabled(False)

            # Start the AI response thread
            self.ai_thread = AIResponseThread(prompt=question)
            self.ai_thread.response_signal.connect(self.display_response)
            self.ai_thread.start()
        else:
            self.response_display.setText("Please enter a question to ask the AI.")

    def display_response(self, response):
        """
        Displays the AI's response in the response display area.
        Re-enables the 'Ask AI' button.
        """
        self.response_display.append(f"AI: {response}")
        log_message(f"AI responded: {response}", level="info")
        self.ask_button.setEnabled(True)
