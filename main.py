import sys
from PyQt5.QtWidgets import QApplication
from ui_main import MainForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainForm()
    main_window.show()
    sys.exit(app.exec_())