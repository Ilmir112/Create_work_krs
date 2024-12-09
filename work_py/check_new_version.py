# -*- coding: utf-8 -*-
import json
import logging
import shutil
import subprocess
import sys
import os
import threading
import time

import psutil
import requests
import zipfile
import data_list
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
        data_list.pause = False
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

            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить обновления: {type(e).__name__}\n\n{str(e)}")



    def on_close(self):
        UpdateChecker.close()
    def get_current_version(self):
        with open(f'{data_list.path_image}users/version_app.json', 'r') as file:
            data = json.load(file)
            version_app = data['version']
        return version_app


class UpdateThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()
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

        # Загрузка архива
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open("ZIMA.zip", "wb") as file:  # Сохраняем архив в папку
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    file.write(data)
                    progress = (downloaded / total_size) * 100
                    self.progress_signal.emit(int(progress))



            # Запускаем обновление в отдельном потоке
            update_thread = threading.Thread(target=self.update_process)
            update_thread.start()

            # QMessageBox.information(None, 'Обновление', 'Обновление скачано, необходимо разархивировать архив и '
            #                                                   'перезапустить приложение')


        except requests.exceptions.RequestException as e:
            QMessageBox.warning(None, "Ошибка", f"Не удалось загрузить обновления: {type(e).__name__}\n\n{str(e)}")

    def move_file(self, source_path, destination_path):
        zima_process_name = "ZIMA.exe"
        print("Ожидание 5 секунд перед закрытием приложения...")
        time.sleep(5)

        # Закрываем приложение
        self.close_zima(zima_process_name)
        print("Приложение закрыто.")

        # Перемещаем файл
        try:
            subprocess.check_call(["cmd", "/c", "move", source_path, destination_path])
            print(f"Файл перемещен из {source_path} в {destination_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при перемещении файла: {type(e).__name__}\n\n{str(e)}")





        print("Ожидание 5 секунд перед запуском обновленного приложения...")
        time.sleep(5)

        # Запускаем обновленное приложение
        try:
            subprocess.check_call(["cmd", "/c", "start", destination_path])
            print("Приложение успешно запущено.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при запуске приложения: {type(e).__name__}\n\n{str(e)}")

    # def wait_for_process_to_close(self, process_name):
    #     """
    #     Ждем, пока процесс с указанным именем не завершится.
    #     """
    #     while True:
    #         # Получаем список всех процессов
    #         tasks = subprocess.check_output("tasklist", shell=True).decode('Windows-1251')
    #         if process_name not in tasks:
    #             break
    #         else:
    #             self.close_zima()


    def update_process(self):

        extract_len = len(data_list.path_image) + len('ZIMA.exe')

        extract_dir = os.path.dirname(os.path.abspath(__file__))[:-extract_len]
        new_extract_dir = extract_dir + '/ZimaUpdate'
        # # Переименовываем текущую версию
        # os.rename(f"{os.path.dirname(sys.executable)}/ZIMA.exe", f"{os.path.dirname(sys.executable)}/ZIMA.exe.old")
        # print(f"Переименование {os.path.dirname(sys.executable)}/ZIMA.exe", f"{os.path.dirname(sys.executable)}/ZIMA.exe.old")

        with zipfile.ZipFile("ZIMA.zip", 'r') as zip_ref:
            zip_ref.extractall(f'{new_extract_dir}')

        # Проверяем, существует ли файл databaseWell.db
        data_base_path = os.path.join(os.path.dirname(sys.executable), "_internal/data_base", "data_base_well")
        database_file = os.path.join(data_base_path, "databaseWell.db")

        ada = os.path.exists(database_file)
        print(f'Местонаходение папки {database_file,  ada}')


        # if os.path.exists(database_file):
        # # if 0 != 0:

        print(f'файл databaseWell.db существует')
        ad = os.listdir(new_extract_dir)
        print(f'папка архива {new_extract_dir}')
        # Файл databaseWell.db существует, перемещаем все, кроме исключений
        for filename in os.listdir(new_extract_dir):
            if filename not in ["databaseWell.db", "data_list.pdb", "krs2.db", 'version_app.json', 'my_app.log']:
                source_path = os.path.join(new_extract_dir, filename)[:-len('/zima')]
                print(f'source_path {source_path}')
                absolute_path = os.path.abspath(__file__)
                print(absolute_path)
                destination_path = absolute_path[:-len('\_internal\work_py\check_new_version.pyc')]
                print(f'destination_path {destination_path}')
                # try:
                #     shutil.copy2(source_path, destination_path)
                #     # print(f"Скопирован файл: {filename}")
                # except PermissionError:
                #     QMessageBox.warning(None, "Ошибка",
                #                         f"Не удалось скопировать файл {os.path.basename(source_path)}. Возможно, он используется другой программой.")
                self.move_file(source_path, destination_path)
                print(f"Перемещен файл: {filename} в папку {destination_path}")
            else:
                print(f"Не Перемещен файл: {filename}")
        # else:
        #     # Файл databaseWell.db не существует, перемещаем все файлы
        #     try:
        #         for filename in os.listdir(new_extract_dir):
        #             shutil.move(f"{extract_dir}/{filename}", f"{os.path.dirname(sys.executable)}/{filename}")

            # except PermissionError:
            #     QMessageBox.warning(None, "Ошибка",
            #                         f"Не удалось переместить файл ZIMA.exe. Возможно, он используется другой программой.")
            #     return

        try:
            # Удаляем папку
            shutil.rmtree(f'{new_extract_dir}')
            print(f"Папка '{new_extract_dir}' удалена.")
        except FileNotFoundError:
            print(f"Папка '{new_extract_dir}' не найдена.")
        except PermissionError:
            print(f"Нет прав для удаления папки '{new_extract_dir}'.")

        try:
            # Удаляем архив
            os.remove('ZIMA.zip')
            print(f'Архив "ZIMA.zip" удален.')
        except FileNotFoundError:
            print(f'Архив "ZIMA.zip" не найден.')
        except PermissionError:
            print(f"Нет прав для удаления архива ZIMA.zip.")

        self.finished_signal.emit(True)
        self.update_version(self.latest_version)

        print(f'изменился файл json')

        # Запускаем обновленную версию
        subprocess.Popen([f"{os.path.dirname(sys.executable)}/ZIMA.exe"])

        # Прекращаем работу текущего процесса
        os._exit(0)  # Прекращаем процесс (не используйте sys.exit())
    @staticmethod
    def run_zima(zima_path):
        """Запускает ZIMA.exe."""
        subprocess.Popen([zima_path])

    @staticmethod
    def close_process_update(process_name):
        try:
            subprocess.run(['taskkill', '/f', '/im', process_name], check=True)
            print(f"Процесс {process_name} успешно закрыт.")
        except subprocess.CalledProcessError:
            print(f"Не удалось закрыть процесс {process_name}.")

    @staticmethod
    def update_version(new_version):
        # Открываем JSON файл для чтения
        with open(f'{data_list.path_image}users/version_app.json', "r") as file:
            data = json.load(file)
            data["version"] = new_version

        with open(f'{data_list.path_image}users/version_app.json', 'w') as file:
            json.dump(data, file, indent=4)
    @staticmethod
    def close_zima(zima_process_name):
        """Закрывает процесс по его имени."""
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == zima_process_name:
                proc.terminate()  # Остановка процесса ZIMA.exe
                  # Ожидание завершения

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateChecker()
    if window.window_close == True:
        window.show()
    # Подключение сигнала aboutToQuit к функции on_close
    app.aboutToQuit.connect(window.on_close())
    sys.exit(app.exec_())
