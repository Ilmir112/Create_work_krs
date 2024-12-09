import smtplib
import urllib
import webbrowser

from PyQt5.QtWidgets import QDialog, QTextEdit, QPushButton, QVBoxLayout, QApplication
import sys


class CustomMessageBox(QDialog):
    def __init__(self, data_well, message):
        super().__init__()
        self.data_well = data_well
        self.setWindowTitle("Информационное сообщение")

        # Создаем текстовое поле для отображения информации
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(message)
        self.text_edit.setReadOnly(True)  # Запрет редактирования текста

        # Кнопка для закрытия окна
        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)

        # Кнопка для отправки текста по электронной почте
        send_button = QPushButton("Отправить по почте", self)
        send_button.clicked.connect(self.send_email)

        # Устанавливаем вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(send_button)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def send_email(self):
        # Получаем текст из текстового поля
        message_content = self.text_edit.toPlainText()
        recipient_email = ""  # Замените на адрес получателя
        subject = f"Замечания по ПЗ скв {self.data_well.well_number.get_value} {self.data_well.well_area.get_value} "

        # Кодируем текст сообщения для URL
        encoded_message = urllib.parse.quote(message_content.replace('\n', '\r\n\r\n'))

        # Создаем URL для почтового клиента
        mailto_link = f"mailto:{recipient_email}?subject={subject}&body={encoded_message}"

        # Открываем почтовый клиент
        webbrowser.open(mailto_link)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    message_box = CustomMessageBox("Ваше сообщение здесь.")
    message_box.exec_()
