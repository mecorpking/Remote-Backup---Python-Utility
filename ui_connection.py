from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class ConnectionForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configure Connection")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Server input
        self.lbl_server = QLabel("Server Address:")
        layout.addWidget(self.lbl_server)

        self.txt_server = QLineEdit()
        layout.addWidget(self.txt_server)

        # Username input
        self.lbl_username = QLabel("Username:")
        layout.addWidget(self.lbl_username)

        self.txt_username = QLineEdit()
        layout.addWidget(self.txt_username)

        # Password input
        self.lbl_password = QLabel("Password:")
        layout.addWidget(self.lbl_password)

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.txt_password)

        # Connect button
        self.btn_connect = QPushButton("Test Connection")
        layout.addWidget(self.btn_connect)
        self.btn_connect.clicked.connect(self.test_connection)

        self.setLayout(layout)

    def test_connection(self):
        server = self.txt_server.text()
        username = self.txt_username.text()
        password = self.txt_password.text()

        if not server or not username or not password:
            QMessageBox.warning(self, "Warning", "All fields are required.")
        else:
            # Simulate a connection test (implement actual logic)
            QMessageBox.information(self, "Success", "Connection successful!")
            self.close()