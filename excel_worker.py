from PyQt5.QtCore import QThread, pyqtSignal
import os

import data_list
from data_base.config_base import CheckWellExistence, connection_to_database
from decrypt import decrypt
from server_response import ApiClient

class ExcelWorker(QThread):
    finished = pyqtSignal()
    error_signal = pyqtSignal(str, str)
    drives = ['D:\\', 'C:\\Users']

    def __init__(self, data_well):
        super().__init__()
        self.data_well = data_well

    def check_well_existence(self, well_number, deposit_area, region):
        check_true = True

        try:
            if data_list.connect_in_base:
                db = connection_to_database(decrypt("DB_NAME_USER"))
                self.check_correct_well = CheckWellExistence(db)
            check_true, stop_app = (
                self.check_correct_well.checking_well_database_without_juming(
                    well_number, deposit_area, region
                )
            )
            self.finished.emit()
            return check_true, stop_app
        except Exception as e:
            self.error_signal.emit("Ошибка при проверке записи", f"Ошибка при проверке записи: {type(e).__name__}\n\n{str(e)}")
            return check_true

    @staticmethod
    def find_and_delete_files(drive):
        for root, dirs, files in os.walk(drive):
            for file in files:
                filename_lower = file.lower()
                if 'для' in filename_lower.lower() and 'планов' in filename_lower.lower():
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"файл: {file_path}")
                    except Exception as e:
                        print(f"Не удалось {file_path}: {e}")

    def check_category(self, well_number, deposit_area, region):
        if data_list.connect_in_base:
            self.params = {
                "well_number": well_number.get_value,
                "well_area": deposit_area.get_value,
            }
            result = ApiClient.request_params_get(
                ApiClient.read_wells_classifier_by_well_number_and_well_area(),
                self.params,
            )
        else:
            result = self.check_correct_well.check_category(
                well_number, deposit_area, region
            )
        return result


