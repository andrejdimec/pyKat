import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QProgressBar,
    QPushButton,
)
from PySide6.QtCore import Qt, QThread, Signal


class Worker(QThread):
    progress = Signal(int)
    status = Signal(str)

    def run(self):
        total_steps = 100  # Example total steps
        for i in range(total_steps):
            # Simulate a long-running task
            self.msleep(50)  # Sleep for 50ms
            self.progress.emit(i + 1)
            self.status.emit(f"Processing {i + 1}/{total_steps}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Starting...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_process)
        self.layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def start_process(self):
        self.worker = Worker()
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
