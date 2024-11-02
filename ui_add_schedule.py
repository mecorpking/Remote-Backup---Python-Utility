from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QComboBox, QSpinBox, QMessageBox

class AddScheduleForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Schedule")
        self.setGeometry(100, 100, 400, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File path input
        self.lbl_file_path = QLabel("Select File/Folder Path:")
        layout.addWidget(self.lbl_file_path)

        self.txt_file_path = QLineEdit()
        layout.addWidget(self.txt_file_path)

        self.btn_browse = QPushButton("Browse")
        layout.addWidget(self.btn_browse)
        self.btn_browse.clicked.connect(self.browse_file)

        # Backup period selection
        self.lbl_backup_period = QLabel("Backup Period (days):")
        layout.addWidget(self.lbl_backup_period)

        self.combo_backup_period = QComboBox()
        self.combo_backup_period.addItems(["7", "15", "30", "Custom"])
        self.combo_backup_period.currentTextChanged.connect(self.handle_custom_days)
        layout.addWidget(self.combo_backup_period)

        self.spin_custom_days = QSpinBox()
        self.spin_custom_days.setMinimum(1)
        self.spin_custom_days.setValue(7)
        self.spin_custom_days.setVisible(False)
        layout.addWidget(self.spin_custom_days)

        # Save button
        self.btn_save = QPushButton("Save Schedule")
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.save_schedule)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QFileDialog.getExistingDirectory(self, "Select Folder") or QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")[0]
        if file_dialog:
            self.txt_file_path.setText(file_dialog)

    def handle_custom_days(self, text):
        if text == "Custom":
            self.spin_custom_days.setVisible(True)
        else:
            self.spin_custom_days.setVisible(False)

    def save_schedule(self):
        if not self.txt_file_path.text():
            QMessageBox.warning(self, "Warning", "Please select a file or folder.")
        else:
            backup_period = self.spin_custom_days.value() if self.combo_backup_period.currentText() == "Custom" else int(self.combo_backup_period.currentText())
            # Logic to save the file path and backup period (e.g., update a configuration file)
            QMessageBox.information(self, "Success", f"Schedule saved with a backup period of {backup_period} days.")
            self.close()