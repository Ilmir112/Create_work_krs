# -*- coding: utf-8 -*-
import json
import shutil
import subprocess
import sys
import os
import psutil
import requests
import zipfile
import well_data
from PyQt5.QtNetwork import QSslConfiguration, QSslCertificate, QSslKey, QSsl

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox, QProgressBar
)
from PyQt5.QtCore import QUrl, QProcess, pyqtSignal, QThread, Qt, QEvent


class ModalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Модальное окно")
        label = QLabel("Это модальное окно!", self)
        label.move(50, 50)


class UpdateChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowFlags(Qt.WindowModal))
        self.setWindowTitle("Проверка обновлений")

        # Установка флага `Qt.WindowModal`

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

        self.progress_zip_bar = QProgressBar()
        self.progress_zip_bar.setValue(0)
        self.progress_zip_bar.setVisible(False)

        self.complete_prog = QPushButton("Продолжить")
        self.complete_prog.clicked.connect(self.def_complete_prog)

        # Вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.version_label)
        layout.addWidget(self.update_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.complete_prog)
        self.setLayout(layout)

        # Запуск проверки версии
        self.check_version()

    def open_modal(self):
        self.modal_window = ModalWindow()
        self.modal_window.show()
        self.block_events()

    def block_events(self):
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.KeyPress:
            if self.modal_window:
                return True  # Блокируем событие
        return super().eventFilter(obj, event)

    def def_complete_prog(self):
        well_data.pause = False
        self.close()

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

        url = "http://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest"

        try:
            response = requests.get(url, verify=True)
            if response.status_code == 200:
                remaining_requests = int(response.headers.get('X-RateLimit-Remaining'))
                print(f"Осталось запросов: {remaining_requests}")
            else:
                print(f"Ошибка: {response.status_code}")

            response = requests.get(url, verify=False)
            response.raise_for_status()  # Проверка на ошибки

            # Получение информации о последней версии из GitHub
            self.latest_version = response.json()["tag_name"]

            UpdateChecker.close(self)
            # Получение текущей версии из файла
            self.current_version = self.get_current_version()
            UpdateChecker.window_close = False

            if self.current_version == self.latest_version:
                self.version_label.setText(f"Текущая версия: {self.current_version}")
                self.close()
                self.update_button.setEnabled(False)

            else:
                self.version_label.setText(f"Доступна новая версия: {self.latest_version}")
                self.update_button.setEnabled(True)
                UpdateChecker.window_close = True


        except requests.exceptions.RequestException as e:

            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить обновления: {e}")
            well_data.pause = False


    def on_close(self):
        UpdateChecker.close()
    def get_current_version(self):
        with open(f'{well_data.path_image}users/version_app.json', 'r') as file:
            data = json.load(file)
            version_app = data['version']
        return version_app


class UpdateThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.latest_version = self.check_version()

    def check_version(self):
        try:
            url = "https://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest"
            print(f'сработало проверка версии {url}')
        except:
            url = "http://api.github.com/repos/Ilmir112/Create_work_krs/releases/latest"

        response = requests.get(url, verify=False)
        response.raise_for_status()  # Проверка на ошибки

        # Получение информации о последней версии из GitHub
        self.latest_version = response.json()["tag_name"]
        return self.latest_version

    def run(self):

        # на URL архива для загрузки
        url = f"https://github.com/Ilmir112/Create_work_krs/releases/download/{self.latest_version}/ZIMA.zip"

        # Замените "your_download_folder" на путь к папке загрузки
        download_folder = sys.executable

        # Загрузка архива
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open("zima.zip", "wb") as file:  # Сохраняем архив в папку
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    file.write(data)
                    progress = (downloaded / total_size) * 100
                    self.progress_signal.emit(int(progress))

            extract_len = len(well_data.path_image) + len('ZIMA.exe')
            print(extract_len, well_data.path_image + 'ZIMA.exe')

            extract_dir = os.path.dirname(os.path.abspath(__file__))[:-extract_len]
            mes = QMessageBox.information(self, 'Обновление', 'Обновление скачано, необходимо разархивировать архив и '
                                                              'перезапустить приложение')
            self.close_process("ZIMA.exe")
            # with zipfile.ZipFile("zima.zip", 'r') as zip_ref:
            #     for info in zip_ref.infolist():
            #         if "ZIMA.exe" not in info.filename:
            #         #     # Извлекаем файл в текущую директорию
            #         #     # Удаляем путь к папке "ZIMA/" из имени файла
            #         #     filename = info.filename[len("ZIMA/"):]
            #         #     zip_ref.extract(info, os.path.join(extract_dir, filename))
            #         # elif info.filename.startswith("ZIMA/"):  # Проверяем, начинается ли имя файла с "zima/"
            #             # Удаляем "zima/" из начала имени файла, чтобы извлечь только содержимое
            #             filename = info.filename[len("ZIMA/"):]
            #             zip_ref.extract(info, os.path.join(extract_dir, filename))
            #             # print(f'фат2 {filename}')

            with zipfile.ZipFile("zima.zip", 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # source_folder = "D:/ZIMA/ZIMA"
            # destination_folder = "D:/ZIMA"

            # if os.path.exists(source_folder):
            #     # Копируем папку и все ее содержимое
            #     shutil.copytree(source_folder, destination_folder)
            #     print("Папка успешно скопирована.")
            # else:
            #     print("Исходная папка не найдена и не может быть скопирована.")

            # Проверяем местонахождение текущей версии приложения
            existing_version_path = "ZIMA/ZIMA.exe"

            self.finished_signal.emit(True)
            self.update_version(self.latest_version)

            well_data.pause = False

            # Запускаем приложение Zima.exe
            subprocess.Popen([f"{download_folder.replace('ZIMA.zip', 'ZIMA.exe')}"])

        except requests.exceptions.RequestException as e:
            mes = QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить обновления: {e}")

    @staticmethod
    def close_process(process_name):
        try:
            subprocess.run(['taskkill', '/f', '/im', process_name], check=True)
            print(f"Процесс {process_name} успешно закрыт.")
        except subprocess.CalledProcessError:
            print(f"Не удалось закрыть процесс {process_name}.")

    @staticmethod
    def update_version(new_version):
        # Открываем JSON файл для чтения
        with open(f'{well_data.path_image}users/version_app.json', "r") as file:
            data = json.load(file)
            data["version"] = new_version

        with open(f'{well_data.path_image}users/version_app.json', 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateChecker()
    if window.window_close == True:
        window.show()
    # Подключение сигнала aboutToQuit к функции on_close
    app.aboutToQuit.connect(window.on_close())
    sys.exit(app.exec_())
