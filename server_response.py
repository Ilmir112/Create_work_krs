import re
import threading
from datetime import datetime
import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class ApiClient:
    SERVER_API = 'http://localhost:8000/zimaApp'

    @classmethod
    def run_in_thread(cls, target_method, *args, **kwargs):
        thread = threading.Thread(target=target_method, args=args, kwargs=kwargs)
        thread.start()
        return thread

    @staticmethod
    def get_endpoint(path):
        return f'{ApiClient.SERVER_API}{path}'

    @staticmethod
    def request_post(path, json_data):
        url = ApiClient.get_endpoint(path)
        try:
            response = requests.post(url, json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None

    @staticmethod
    def request_post_param(path, json_data):
        url = ApiClient.get_endpoint(path)
        try:
            response = requests.get(url, params=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None

    @staticmethod
    def serialize_datetime(obj):

        if isinstance(obj, dict):
            return {k: ApiClient.serialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ApiClient.serialize_datetime(item) for item in obj]
        elif isinstance(obj, str):
            matches = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", obj)
            if matches:
                obj = datetime.strptime(matches[0], '%d.%m.%Y')
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d')
        else:
            return obj

    # Методы для конкретных API-запросов
    @classmethod
    def read_wells_silencing_response_for_add_well(cls):
        return '/wells_silencing_router/add_data_well_silencing'

    @classmethod
    def find_wells_data_response_filter_well_number_well_area(cls):
        return '/wells_data_router/find_wells_data'

    @classmethod
    def read_wells_classifier_response_for_add_well(cls):
        return '/wells_classifier/add_data_well_classifier'

    @classmethod
    def read_wells_silencing_response_for_delete_well(cls):
        return '/wells_silencing_router/delete_well_silencing'

    @classmethod
    def read_wells_classifier_response_for_delete_well(cls):
        return '/wells_classifier/delete_well_classifier'

    @classmethod
    def read_wells_data_response_for_add(cls):
        return '/wells_data_router/add_wells_data'

    @classmethod
    def delete_wells_by_region(cls, region, path):
        payload = {"region": region}
        # Запускаем выполнение в отдельном потоке
        thread = cls.run_in_thread(cls.request_post,path, payload)
        return thread

    @classmethod
    def add_well_in_database(cls, payload, path):
        serializable_params = cls.serialize_datetime(payload)
        data = {"data": serializable_params}
        thread = cls.run_in_thread(cls.request_post, path, data)
        return thread

    @classmethod
    def add_wells_data_in_database(cls, params_dict, api_url):
        serializable_params = cls.serialize_datetime(params_dict)
        thread = cls.run_in_thread(cls.request_post, api_url, serializable_params)
        return thread

    @classmethod
    def find_wells(cls, well_number, well_area, api_url):
        params = {"well_number": well_number, "well_area": well_area}
        return cls.request_post_param(api_url, params)


class ResponseWork(QMainWindow):
    def add_wells_data_in_database(self, params_dict, api_url):
        result = ApiClient.add_wells_data_in_database(params_dict, api_url)
        if result:
            QMessageBox.information(self, 'Обновление', 'Данные успешно добавлены')
            return True
        else:
            QMessageBox.information(self, 'Обновление', 'Ошибка при добавлении данных')
            return False

    def delete_wells_by_region(self, region):
        result = ApiClient.delete_wells_by_region(region)
        if result:
            QMessageBox.information(self, 'Удаление', 'Объекты успешно удалены')
        else:
            QMessageBox.warning(self, 'Удаление', 'Ошибка при удалении объектов')
