import os
import requests
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QProgressBar, QMessageBox, QAction
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import qtawesome as qta

class DecryptWorker(QThread):
    """Worker thread for decryption."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)
    error_message = pyqtSignal(str)  # Signal for errors

    def __init__(self, file_path, password, save_path):
        super().__init__()
        self.file_path = file_path
        self.password = password
        self.save_path = save_path

    def run(self):
        """Runs decryption in the background and updates progress."""
        try:
            with open(self.file_path, 'rb') as file:
                files = {'file': file}
                data = {'password': self.password, 'output_path': self.save_path}  # Ensure password is correctly sent
                response = requests.post("http://127.0.0.1:5000/decrypt", files=files, data=data) # Removed stream=True as it's not utilized for content writing

                if response.status_code == 200:
                    # Get filename from Content-Disposition header
                    content_disposition = response.headers.get('content-disposition')
                    filename = None
                    if content_disposition:
                        match = re.search(r'filename="?([^"]+)"?', content_disposition)
                        if match:
                            filename = match.group(1)
                        else:
                            # Try download_name (Flask >=2.0)
                            match = re.search(r'download_name="?([^"]+)"?', content_disposition)
                            if match:
                                filename = match.group(1)
                    if filename:
                        save_path = os.path.join(os.path.dirname(self.save_path), filename)
                    else:
                        save_path = self.save_path
                else:
                    error_msg = response.json().get("error", "Unknown error occurred")
                    print(f"Decryption error from server: {error_msg}")  # Debugging
                    self.error_message.emit(error_msg)
                    self.finished.emit(False)

                with open(save_path, 'wb') as output_file:
                    output_file.write(response.content)                    
                self.finished.emit(True)

        except Exception as e:
            # Catch specific request exceptions for better error messages
            if isinstance(e, requests.exceptions.RequestException):
                self.error_message.emit(f"Network error: {str(e)}")
            else:
                self.error_message.emit(str(e))
            self.finished.emit(False)
        self.progress.emit(100)

class DecryptTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.file_label = QLabel("Drag & Drop a File or Click 'Select File'")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)  # Enable drag-and-drop

        self.file_button = QPushButton("Select Encrypted File")
        self.file_button.clicked.connect(self.select_file)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter decryption password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")

        # Add eye icon as an action inside the QLineEdit
        self.eye_action = QAction(qta.icon('fa5s.eye-slash'), "Show/Hide Password", self)
        self.eye_action.setCheckable(True)
        self.eye_action.toggled.connect(self.toggle_password_visibility)
        self.password_input.addAction(self.eye_action, QLineEdit.TrailingPosition)

        self.save_button = QPushButton("Select Save Location")
        self.save_button.clicked.connect(self.select_save_location)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.start_decryption)

        self.progress = QProgressBar()

        layout.addWidget(self.file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        self.file_path = None
        self.save_path = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted File", "", "Encrypted Files (*.enc)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected: {file_path}")

    def select_save_location(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Select Save Location")
        if save_path:
            self.save_path = save_path

    def start_decryption(self):
        """Start decryption in a separate thread."""
        print(f"File path: {self.file_path}")
        print(f"Password: {self.password_input.text()}")
        print(f"Save path: {self.save_path}")

        if not self.file_path or not self.password_input.text() or not self.save_path:
            QMessageBox.warning(self, "Error", "Please select a file, enter a password, and choose a save location.")
            return

        self.file_label.setText("Decrypting... Please wait")
        self.progress.setValue(0)

        self.worker = DecryptWorker(self.file_path, self.password_input.text(), self.save_path)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.decryption_complete)
        self.worker.error_message.connect(self.show_error)
        self.worker.start()

    def decryption_complete(self, success):
        """Update UI when decryption is complete."""
        if success:
            self.file_label.setText(f"Decryption Successful! Saved at {self.save_path}")
            self.password_input.clear()  # Clear password field
            self.progress.setValue(100)
            QMessageBox.information(self, "Decryption Success", "Decryption Successful!")
        else:
            self.file_label.setText("Decryption Failed.")

    def show_error(self, message):
        """Displays an error message to the user."""
        QMessageBox.critical(self, "Decryption Error", message)
        self.progress.setValue(0)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.eye_action.setIcon(qta.icon('fa5s.eye'))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.eye_action.setIcon(qta.icon('fa5s.eye-slash'))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.file_path = urls[0].toLocalFile()
            self.file_label.setText(f"Selected: {self.file_path}")
