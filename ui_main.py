from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CKBackup - Protect Your Data")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        add_schedule_btn = QPushButton("Add Schedule")
        configure_connection_btn = QPushButton("Configure Connection")
        manage_schedules_btn = QPushButton("Manage Schedules")

        layout.addWidget(add_schedule_btn)
        layout.addWidget(configure_connection_btn)
        layout.addWidget(manage_schedules_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        add_schedule_btn.clicked.connect(self.open_add_schedule)
        configure_connection_btn.clicked.connect(self.open_configure_connection)
        manage_schedules_btn.clicked.connect(self.open_manage_schedules)

    def open_add_schedule(self):
        # Code to open the Add Schedule form
        pass

    def open_configure_connection(self):
        # Code to open the Connection form
        pass

    def open_manage_schedules(self):
        # Code to open the Manage Schedules form
        pass