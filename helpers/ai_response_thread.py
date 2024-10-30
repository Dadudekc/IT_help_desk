import requests
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


from IT_help_desk.config.config import MISTRAL_API_ENDPOINT, MISTRAL_API_KEY

class AIResponseThread(QThread):
    response_signal = pyqtSignal(str)  # Signal to send the AI response

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.api_key = MISTRAL_API_KEY
        self.api_endpoint = MISTRAL_API_ENDPOINT

    def run(self):
        """
        Sends the user prompt to the Mistral 7B API and emits the response via signal.
        Includes timeout and retry logic for robust communication.
        """
        if not self.api_key or not self.api_endpoint:
            self.response_signal.emit("Error: Mistral API key or endpoint is missing.")
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": self.prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }

        # Attempt API call with timeout and retry logic
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    headers=headers,
                    json=data,
                    timeout=10  # 10-second timeout for each attempt
                )
                if response.status_code == 200:
                    response_text = response.json().get("text", "No response text available.")
                    self.response_signal.emit(response_text)
                    return
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    self.response_signal.emit(error_msg)
                    return
            except requests.Timeout:
                self.response_signal.emit("Error: Request timed out. Retrying...")
            except requests.RequestException as e:
                self.response_signal.emit(f"Error communicating with AI: {str(e)}")
                return

        # If retries exhausted
        self.response_signal.emit("Error: Unable to communicate with AI after multiple attempts.")
