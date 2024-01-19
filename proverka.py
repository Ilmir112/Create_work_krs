from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QDoubleValidator, QColor, QPalette, QValidator
from PyQt5.QtCore import Qt


class FloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(FloatLineEdit, self).__init__(parent)

        # Устанавливаем валидатор для проверки на float
        self.setValidator(QDoubleValidator())

    def focusOutEvent(self, event):
        # При потере фокуса проверяем, является ли текст float
        if self.validator().validate(self.text(), 0)[0] != QValidator.Acceptable:
            # Если текст не является числом, меняем цвет фона на красный
            palette = self.palette()
            palette.setColor(QPalette.Base, QColor(Qt.red))
            self.setPalette(palette)
        else:
            # Если текст является числом, возвращаем цвет фона по умолчанию
            self.setPalette(self.parentWidget().palette())


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        layout = QVBoxLayout()

        line_edit1 = FloatLineEdit()
        layout.addWidget(line_edit1)

        line_edit2 = FloatLineEdit()
        layout.addWidget(line_edit2)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()