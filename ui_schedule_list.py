from PyQt5.QtWidgets import QDialog, QListWidget, QPushButton, QVBoxLayout, QMessageBox

class ScheduleListForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Schedules")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # List widget for schedules
        self.lst_schedules = QListWidget()
        layout.addWidget(self.lst_schedules)

        # Populate list with example data (replace with actual schedule data)
        self.lst_schedules.addItem("Schedule 1 - Daily Backup")
        self.lst_schedules.addItem("Schedule 2 - Weekly Backup")

        # Delete button
        self.btn_delete = QPushButton("Delete Selected Schedule")
        layout.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self.delete_schedule)

        self.setLayout(layout)

    def delete_schedule(self):
        selected_item = self.lst_schedules.currentItem()
        if selected_item:
            self.lst_schedules.takeItem(self.lst_schedules.row(selected_item))
            # Implement actual deletion logic here
            QMessageBox.information(self, "Deleted", "Schedule deleted successfully.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a schedule to delete.")