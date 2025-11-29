from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from backend.crypto_utils import get_full_history, clear_history, get_recent_events

class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # History label and text area
        self.history_label = QLabel("Encryption & Decryption History:")
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)

        # Buttons for history management
        self.refresh_button = QPushButton("Refresh History")
        self.refresh_button.clicked.connect(self.load_recent_history)

        self.show_history_button = QPushButton("Show History")
        self.show_history_button.clicked.connect(self.load_full_history)

        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)

        # Add widgets to layout
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_text)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.show_history_button)
        layout.addWidget(self.clear_history_button)
        self.setLayout(layout)

        # Load recent history on startup
        self.load_recent_history()

    def load_recent_history(self):
        """Loads the most recent encryption/decryption events with color coding."""
        self.history_text.setHtml(self.format_history(get_recent_events()))

    def load_full_history(self):
        """Loads the complete encryption history with color coding."""
        self.history_text.setHtml(self.format_history(get_full_history()))

    def format_history(self, log_text):
        """Format log entries with color and spacing."""
        if not log_text:
            return "<i>No history available.</i>"
        lines = log_text.strip().split('\n')
        html_lines = []
        for line in lines:
            # Example log: [timestamp] EVENT - filename - STATUS - output_path
            parts = line.split(' - ')
            if len(parts) >= 4:
                timestamp_event = parts[0]
                filename = parts[1]
                status = parts[2]
                output_path = parts[3]
                # Color status
                if "SUCCESS" in status:
                    status_html = f'<span style="color: #2ecc40; font-weight: bold;">{status}</span>'
                else:
                    status_html = f'<span style="color: #e74c3c; font-weight: bold;">{status}</span>'
                html_lines.append(
                    f'<div style="padding:8px 0 8px 0; margin-bottom:6px;">'
                    f'<span style="color:#888;">{timestamp_event}</span><br>'
                    f'<b>File:</b> {filename}<br>'
                    f'<b>Status:</b> {status_html}<br>'
                    f'<b>Saved at:</b> <span style="color:#555;">{output_path}</span>'
                    f'</div>'
                )
            else:
                html_lines.append(f'<div style="padding:8px 0;">{line}</div>')
        return "<div>" + "".join(html_lines) + "</div>"

    def clear_history(self):
        """Clears the history log and updates the display."""
        clear_history()  # Call the backend utility function
        self.load_recent_history()