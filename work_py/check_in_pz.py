from PyQt5.QtWidgets import QApplication, QMessageBox, QVBoxLayout, QDialog, QTextEdit, QPushButton


class CustomMessageBox(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Информационное сообщение")

        # Создаем текстовое поле для отображения информации
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(message)
        self.text_edit.setReadOnly(True)  # Запрет редактирования текста

        # Кнопка для закрытия окна
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)

        # Устанавливаем вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(close_button)
        self.setLayout(layout)



