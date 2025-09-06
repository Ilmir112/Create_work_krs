from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from log_files.log import logger

class UncaughtExceptions(QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self, data_well):
        super().__init__()
        self.data_well = data_well

    @pyqtSlot(object)
    def handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        logger.critical(
            "Uncaught exception, application will terminate.",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

        self._exception_caught.emit((exc_type, exc_value))


