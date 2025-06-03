import logging
import requests

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QPlainTextEdit

from server_response import ApiClient


# Обработчик логов, который отправляет логи в FastAPI
class FastAPILogHandler(logging.Handler):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record):
        try:
            log_entry = self.format(record)
            # Отправляем POST-запрос с логом
            payload = {
                'log': log_entry,
                'level': record.levelname,
                'logger': record.name,
                "filename": record.filename,
                "line": record.lineno
            }

            response = ApiClient.request_post(self.url, payload)

        except requests.exceptions.RequestException as e:
            logger.critical(f'Ошибка при отправке логов {e}')
            return
        except Exception as e:
            logger.critical(f'Ошибка при обработке исключений при отправке логов {e}')
            return


# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем обработчики
file_handler = logging.FileHandler('my_app.log')
console_handler = logging.StreamHandler()

# Создаем обработчик для отправки логов на FastAPI
fastapi_handler = FastAPILogHandler(ApiClient.send_logger_message())  # Укажите ваш URL API

# Устанавливаем форматтеры
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
fastapi_handler.setFormatter(formatter)

# Добавляем обработчики
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(fastapi_handler)

# class QPlainTextEditLogger(logging.Handler, QObject):
#     appendPlainText = pyqtSignal(str)
#
#     def __init__(self, parent):
#         super().__init__()
#         QObject.__init__(self)
#         self.widget = QPlainTextEdit(parent)
#         self.widget.setReadOnly(True)
#         self.appendPlainText.connect(self.widget.appendPlainText)
#
#     def emit(self, record):
#         msg = self.format(record)
#         self.appendPlainText.emit(msg)
