import json
import subprocess
import sys
import os
import zipfile

import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import QUrl, QProcess


class UpdateChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Проверка обновлений")

        # Лейбл для отображения версии
        self.version_label = QLabel("Проверка версии...")
        # Кнопка для обновления
        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.update_application)
        self.update_button.setEnabled(False)

        # Вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

        # Запуск проверки версии
        self.check_version()

    def check_version(self):
        # Замените "your_username" и "your_repository" на ваши данные
        url = "https://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки

            # Получение информации о последней версии из GitHub
            self.latest_version = response.json()["tag_name"]
            # Получение текущей версии из файла (например, "version.txt")
            current_version = self.get_current_version()

            if current_version == self.latest_version:
                self.version_label.setText(f"Текущая версия: {current_version}")
                self.update_button.setEnabled(False)
            else:
                self.version_label.setText(f"Доступна новая версия: {self.latest_version}")
                self.update_button.setEnabled(True)

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить обновления: {e}")

    def get_current_version(self):
        with open('D:/python/Create_work_krs/users/version_app.json', 'r') as file:
            data = json.load(file)
            version_app = data['version']

        return version_app

    def update_application(self):

        # Замените "https://github.com/your_username/your_repository/archive/refs/heads/master.zip"
        # на URL архива для загрузки
        url = f"https://github.com/Ilmir112/Create_work_krs/releases/download/{self.latest_version}/ZIMA.zip"

        # Замените "your_download_folder" на путь к папке загрузки
        download_folder = sys.executable

        # Загрузка архива
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open("zima.zip", "wb") as file:  # Сохраняем архив в папку tmp
                file.write(response.content)

            extract_dir = "tmp"

            with zipfile.ZipFile("zima.zip", 'r') as zip_ref:
                zip_ref.extractall(f'{download_folder}/{extract_dir}')
            # Путь к папке "tmp"
            folder_path = os.path.abspath("tmp")

            # Открываем папку "tmp" в проводнике Windows
            subprocess.Popen(f'explorer "{folder_path}"')

            os.remove("zima.zip")

            # Обновление приложения (может потребоваться перезапуск)
            # ... (ваш код для обновления приложения)

            QMessageBox.information(self, "Обновление", "Приложение успешно обновлено!")
            # Выход из приложения (или перезапуск)
            QApplication.exit(0)

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить обновления: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateChecker()
    window.show()
    sys.exit(app.exec_())