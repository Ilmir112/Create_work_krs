import json
import subprocess
import sys
import os
import time
import zipfile

import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox, QProgressBar
)
from PyQt5.QtCore import QUrl, QProcess, pyqtSignal, QThread


class UpdateChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Проверка обновлений")

        # Лейбл для отображения версии
        self.version_label = QLabel("Проверка версии...")
        # Кнопка для обновления
        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.start_update)
        self.update_button.setEnabled(False)

        # ProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        # Вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.update_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.check_api_limits()

        # Запуск проверки версии
        self.check_version()

    def start_update(self):
        self.update_button.setEnabled(False)
        self.version_label.setText("Загрузка обновления...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.update_thread = UpdateThread(self)
        self.update_thread.progress_signal.connect(self.update_progress)
        self.update_thread.finished_signal.connect(self.update_finished)
        self.update_thread.start()
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    def update_finished(self, success):
        if success:
            QMessageBox.information(self, "Обновление", "Приложение успешно обновлено!")
            # Выход из приложения (или перезапуск)
            QApplication.exit(0)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить приложение.")
        self.update_button.setEnabled(True)
        self.version_label.setText("Проверка версии...")
        self.progress_bar.setVisible(False)

    def check_version(self):
        # Замените "your_username" и "your_repository" на ваши данные
        url = "https://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки

            # Получение информации о последней версии из GitHub
            self.latest_version = response.json()["tag_name"]
            # Получение текущей версии из файла (например, "version.txt")
            self.current_version = self.get_current_version()

            if self.current_version == self.latest_version:
                self.version_label.setText(f"Текущая версия: {self.current_version}")
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
    @staticmethod
    def check_api_limits():
        url = "https://api.github.com/repos/Ilmir112/Create_work_krs"

        response = requests.get(url)

        remaining_requests = int(response.headers.get('X-RateLimit-Remaining'))
        reset_time = int(response.headers.get('X-RateLimit-Reset'))

        print(f"Осталось запросов: {remaining_requests}")
        print(f"Время сброса лимита: {reset_time}")



class UpdateThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)

    def __init__(self,  parent=None):
        super().__init__( parent)
        self.latest_version = UpdateChecker.get_current_version(self)


    def run(self):

        # на URL архива для загрузки
        url = f"https://github.com/Ilmir112/Create_work_krs/releases/download/{self.latest_version}/ZIMA.zip"

        # Замените "your_download_folder" на путь к папке загрузки
        download_folder = sys.executable

        print(f'место нахождения {download_folder}')

        # Загрузка архива
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open("zima.zip", "wb") as file:  # Сохраняем архив в папку tmp
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    file.write(data)
                    progress = (downloaded / total_size) * 100
                    self.progress_signal.emit(int(progress))


            with zipfile.ZipFile("zima.zip", 'r') as zip_ref:
                zip_ref.extractall(f'{download_folder}')
            # Путь к папке "tmp"
            folder_path = os.path.abspath("tmp")

            # Открываем папку "tmp" в проводнике Windows
            subprocess.Popen(f'explorer "{folder_path}"')

            os.remove("zima.zip")

            # Обновление приложения (может потребоваться перезапуск)
            # ... (ваш код для обновления приложения)
            self.finished_signal.emit(True)
            self.update_version(self.latest_version)

        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить обновления: {e}")

    def update_version(new_version):
        with open('plan_krs/version_app.json', 'r') as file:
            data = json.load(file)
            data['version'] = new_version

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateChecker()
    window.show()
    sys.exit(app.exec_())