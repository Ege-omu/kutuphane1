import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
