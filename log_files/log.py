import logging
import sys
import threading
import traceback

import requests

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QPlainTextEdit

import data_list
from server_response import ApiClient


# Обработчик логов, который отправляет логи в FastAPI
class FastAPILogHandler(logging.Handler):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.error_logger = logging.getLogger('FastAPILogHandler')
        # Можно установить уровень и форматтер при необходимости

    def emit(self, record):
        try:
            log_entry = self.format(record)
            # Пытаемся достать full traceback даже если в вызове логгера не передали exc_info=True.
            # В момент emit() мы обычно находимся внутри except-блока, поэтому sys.exc_info() доступен.
            exc_info = record.exc_info
            if not exc_info or exc_info[0] is None:
                exc_info = sys.exc_info()
            error_reason = None
            if exc_info and exc_info[0] is not None:
                error_reason = "".join(traceback.format_exception(*exc_info))
            payload = {
                'log': log_entry,
                'level': record.levelname,
                'logger': record.name,
                'filename': record.filename,
                'line': record.lineno,
                # Контекст, необходимый для быстрого поиска причины на backend
                'well_number': getattr(data_list, 'current_well_number', None),
                'well_area': getattr(data_list, 'current_well_area', None),
                'well_region': getattr(data_list, 'current_well_region', None),
                'operation_type': getattr(data_list, 'current_operation_type', None),
                # Полная причина ошибки (traceback)
                'error_reason': error_reason or record.getMessage(),
            }
            # Выполняем отправку в отдельном потоке, чтобы не блокировать основной поток
            threading.Thread(target=self.send_log, args=(payload,), daemon=True).start()

        except Exception as e:
            # Логируем ошибку внутри обработчика без рекурсии
            self.error_logger.exception(f'Ошибка при подготовке лога: {e}')

    def send_log(self, payload):
        try:
            response = ApiClient.request_post(self.url, payload)
            # request_post при ошибке возвращает int (status_code) или None, а не объект Response
            if response is not None and isinstance(response, int):
                self.error_logger.debug(f'Сервер логов вернул код: {response}')
        except requests.exceptions.RequestException as e:
            self.error_logger.exception(f'Ошибка при отправке лога: {e}')


# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем обработчики
file_handler = logging.FileHandler('logs.log')
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


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.critical(
        "Uncaught exception, application will terminate.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


sys.excepthook = handle_uncaught_exception

#
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


