import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget, QDesktopWidget


class ProgressBarWindow(QMainWindow):
    def __init__(self, max_row):
        super().__init__()
        self.max_row = max_row
        self.setWindowTitle("Сохранение")
        self.setGeometry(100, 100, 300, 100)

        # Создание виджетов
        self.progress = QProgressBar(self)
        self.progress.setGeometry(30, 40, 240, 20)
        self.progress.setMaximum(max_row)
        self.progress.setValue(0)

        # Установка вертикального макета
        layout = QVBoxLayout()
        layout.addWidget(self.progress)
        # layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Центрируем окно
        self.center()

    def center(self):
        # Получаем размеры экрана
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_loading(self, row):
        self.progress.setValue(row)
        QApplication.processEvents()  # Обновление интерфейса

        if self.max_row <= row:
            self.close()
        # self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressBarWindow(200)
    window.show()
    sys.exit(app.exec_())
