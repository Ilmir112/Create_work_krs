import sys
from PyQt5.QtWidgets import QApplication
from main import MyWindow

def show_splash_screen():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


