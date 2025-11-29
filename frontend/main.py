import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QLineEdit, QPushButton, QHBoxLayout, QWidget
from .encrypt_tab import EncryptTab
from .decrypt_tab import DecryptTab
from .history_tab import HistoryTab
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QColor, QIcon
from PyQt5.QtCore import Qt, QSize
import qtawesome as qta 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set application icon
        icon_path = resource_path(os.path.join('asset', 'encrypts.ico'))
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Encryption & Decryption App")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget()
        self.tabs.addTab(EncryptTab(), "🔒 Encrypt")
        self.tabs.addTab(DecryptTab(), "🔓 Decrypt")
        self.tabs.addTab(HistoryTab(), "📜 History")

        # Responsive background image
        self.image_path = resource_path(os.path.join('asset', '900.png'))
        if not os.path.exists(self.image_path):
            print(f"Warning: Image path {self.image_path} does not exist!")
        self.set_background()

        # Improved stylesheet
        self.setStyleSheet("""
            QMainWindow {
                color: white;
            }
            QPushButton {
                background-color: #800080;
                color: white;
                padding: 10px;
                height: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b266ff; /* Light purple */
            }
            QLabel {
                font-size: 14px;
            }
            QProgressBar {
                height: 15px;
                border-radius: 5px;
                background-color: #333;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
            QTabWidget {
                background-color: rgba(255, 255, 255, 0.7);
            }
            QTabWidget::pane {
                border: 1px solid #444;
            }
            QLineEdit#passwordInput {
                border: 2px solid #b266ff;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 16px;
                height: 5px;
                background: #fff;
                color: #333;
                min-height: 36px;
            }
            QLineEdit#passwordInput:focus {
                border: 2px solid #800080;
                background: #f3e6ff;
            }
        """)

        self.setCentralWidget(self.tabs)

    def set_background(self):
        if os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            # Scale the pixmap to always fill the window, keeping aspect ratio, cropping if needed
            scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            # Optionally set a fallback color if image is missing
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor("#f3e6ff"))
            self.setPalette(palette)
            self.setAutoFillBackground(True)

    def resizeEvent(self, event):
        self.set_background()
        super().resizeEvent(event)

    def closeEvent(self, event):
        """Ensure Flask backend is terminated when UI closes."""
        self.backend_process.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
