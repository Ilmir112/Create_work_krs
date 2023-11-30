import time
from PyQt5 import QtCore, QtWidgets

app = QtWidgets.QApplication([])
w = QtWidgets.QPushButton('Pause')
w.show()

def pause_app():
    while True:
        QtCore.QCoreApplication.instance().processEvents()
        time.sleep(0.01)

thread = QtCore.QThread()
w.clicked.connect(thread.started)
thread.finished.connect(app.quit)
thread.start()
pause_app()