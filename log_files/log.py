import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)


class MainWindow_log(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        logTextBox = QTextEditLogger(self)

        # You can format what is printed to text box
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        logTextBox.setFormatter(formatter)
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Log Messages')
        self.show()

        # code for generate error
        try:
            1 / 0
        except ZeroDivisionError as e:
            logging.exception("Exception occurred")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow_log()
    sys.exit(app.exec_())
