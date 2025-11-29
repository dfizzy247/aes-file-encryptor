import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
from backend.app import app as flask_app
from frontend.main import MainWindow

class FlaskThread(QThread):
    def run(self):
        # Disable Flask's reloader to avoid thread issues
        flask_app.run(port=5000, use_reloader=False)

if __name__ == '__main__':
    # Add the project root directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Start Flask in a separate thread
    flask_thread = FlaskThread()
    flask_thread.start()

    # Start the PyQt application
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # When the GUI closes, stop Flask
    exit_code = qt_app.exec_()
    flask_thread.terminate()
    flask_thread.wait()
    sys.exit(exit_code)