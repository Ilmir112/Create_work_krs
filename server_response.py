import json
import re
import threading
from datetime import datetime

import certifi
import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import data_list


class ApiClient:
    with open(f'{data_list.path_image}users/server.json', 'r', encoding='utf-8') as file:
        server_dict = json.load(file)

    SERVER_API = server_dict["host"]
    SETTINGS_TOKEN = None
    proxies = {
        'http': SERVER_API,  # Обязательно http
        'https': SERVER_API,  # Обязательно http
    }

    @classmethod
    def run_in_thread(cls, target_method, *args, **kwargs):
        thread = threading.Thread(target=target_method, args=args, kwargs=kwargs)
        thread.start()
        return thread

    @classmethod
    def validate_params(cls, params):
        # Определяем ожидаемые типы для каждого ключа
        expected_types = {
            "id": int,
            "category_dict": dict,
            "type_kr": str,
            "work_plan": str,
            "excel_json": dict,
            "data_change_paragraph": dict,
            "norms_time": (int, float),
            "chemistry_need": list,
            "geolog_id": (int, str),
            "date_create": str,
            "static_level": (
                type(None),
            ),
            "perforation_project": dict,
            "dinamic_level": (type(None),),  # аналогично static_level
            "type_absorbent": str,
            "expected_data": dict,
            "curator": str,
            "region": str,
        }

        for key, expected_type in expected_types.items():
            value = params.get(key)
            if not isinstance(value, expected_type):
                print(
                    f"Ошибка: ключ '{key}' ожидает тип {expected_type}, но получил {type(value)}"
                )
            else:
                print(f"Ключ '{key}' прошёл проверку.")

    @staticmethod
    def get_endpoint(path):
        return f"{ApiClient.SERVER_API}{path}"

    @staticmethod
    def request_post(path, json_data):

        url = ApiClient.get_endpoint(path)

        try:
            response = requests.post(url, json=ApiClient.serialize_datetime(json_data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return response.status_code

    @staticmethod
    def request_params_get(path, json_data):
        headers = {}
        if ApiClient.SETTINGS_TOKEN:
            token = ApiClient.SETTINGS_TOKEN.value("auth_token", "")
            headers["Authorization"] = f"Bearer {token}"
        url = ApiClient.get_endpoint(path)
        try:
            response = requests.get(url, params=json_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None

    @staticmethod
    def request_post_json(path, json_data, param=None, answer="param"):
        url = ApiClient.get_endpoint(path)
        try:
            token = ApiClient.SETTINGS_TOKEN.value("auth_token", "")
            json_data = ApiClient.serialize_datetime(json_data)
            headers = {"Authorization": f"Bearer {token}"}

            if answer == "param":
                response = requests.post(url, params=json_data, headers=headers)
            else:
                response = requests.post(
                    url, params=param, json=json_data, headers=headers
                )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(None, "Запрос", f"Запрос не удался: {e}")
            return None

    @staticmethod
    def request_put_json(path, json_data, param=None, answer="param"):
        url = ApiClient.get_endpoint(path)
        try:
            token = ApiClient.SETTINGS_TOKEN.value("auth_token", "")
            json_data = ApiClient.serialize_datetime(json_data)
            headers = {"Authorization": f"Bearer {token}"}

            if answer == "param":
                response = requests.put(url, params=json_data, headers=headers)
            else:
                response = requests.put(
                    url, params=param, json=json_data, headers=headers
                )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(None, "Запрос", f"Запрос не удался: {e}")
            return None

    @staticmethod
    def request_get_all(path):
        url = ApiClient.get_endpoint(path)
        try:
            print(url)
            response = requests.get(url, verify=False)

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
        elif "excel" == obj:
            return obj
        elif isinstance(obj, str):
            matches = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", obj)
            if matches and len(matches) == 1:
                obj = datetime.strptime(matches[0], "%d.%m.%Y")

        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return obj

    # Методы для конкретных API-запросов
    @classmethod
    def read_wells_silencing_response_for_add_well(cls):
        return "/wells_silencing_router/add_data_well_silencing"

    @classmethod
    def get_all_users(cls):
        return "/auth/all"

    @classmethod
    def login_path(cls):
        return "/auth/login"

    @classmethod
    def me_info(cls):
        return "/auth/me"

    @classmethod
    def register_auth(cls):
        return "/auth/register"

    @classmethod
    def find_wells_data_response_filter_well_number_well_area(cls):
        return "/wells_data_router/find_wells_data"

    @classmethod
    def read_wells_classifier_response_for_add_well(cls):
        return "/wells_classifier/add_data_well_classifier"

    @classmethod
    def read_wells_classifier_response_all(cls):
        return "/wells_classifier/find_well_classifier_all"

    @classmethod
    def read_wells_classifier_by_well_number_and_well_area(cls):
        return "/wells_classifier/find_well_classifier"

    @classmethod
    def read_wells_silencing_response_all(cls):
        return "/wells_silencing_router/find_well_silencing_all"

    @classmethod
    def read_wells_silencing_response_for_delete_well(cls):
        return "/wells_silencing_router/delete_well_silencing"

    @classmethod
    def read_wells_classifier_response_for_delete_well(cls):
        return "/wells_classifier/delete_well_classifier"

    @classmethod
    def read_wells_data_response_for_add(cls):
        return "/wells_data_router/add_wells_data"

    @classmethod
    def update_wells_data_response(cls):
        return "/wells_data_router/update_wells_data"

    @classmethod
    def find_wells_repair_well_by_id(cls):
        return "/wells_repair_router/find_well_id"

    @classmethod
    def read_wells_repair_response_for_add(cls):
        return "/wells_repair_router/add_wells_data"

    @classmethod
    def response_find_well_filter_by_number(cls):
        return "/wells_repair_router/find_well_filter_by_number"

    @classmethod
    def delete_wells_by_region(cls, region, path):
        payload = {"region": region}
        # Запускаем выполнение в отдельном потоке
        thread = cls.run_in_thread(cls.request_post, path, payload)
        return thread

    @classmethod
    def add_well_in_database(cls, payload, path):
        serializable_params = cls.serialize_datetime(payload)
        data = {"data": serializable_params}
        thread = cls.run_in_thread(cls.request_post, path, data)
        return thread

    @classmethod
    def add_new_user(cls, params_dict, api_url):
        serializable_params = cls.serialize_datetime(params_dict)
        return cls.request_post(api_url, serializable_params)

    @classmethod
    def find_all(cls, api_url):
        return cls.request_post(api_url)

    @classmethod
    def get_info_data(cls, params_dict, api_url):
        serializable_params = cls.serialize_datetime(params_dict)
        return cls.request_post(api_url, serializable_params)

    @classmethod
    def add_wells_data_in_database(cls, params_dict, api_url):
        serializable_params = cls.serialize_datetime(params_dict)
        thread = cls.run_in_thread(cls.request_post, api_url, serializable_params)
        return thread

    @classmethod
    def find_wells(cls, well_number, well_area, api_url):
        params = {"well_number": well_number, "well_area": well_area}
        return cls.request_params_get(api_url, params)


class ResponseWork(QMainWindow):
    def add_wells_data_in_database(self, params_dict, api_url):
        result = ApiClient.add_wells_data_in_database(params_dict, api_url)
        if result:
            QMessageBox.information(self, "Обновление", "Данные успешно добавлены")
            return True
        else:
            QMessageBox.information(self, "Обновление", "Ошибка при добавлении данных")
            return False

    def delete_wells_by_region(self, region):
        result = ApiClient.delete_wells_by_region(region)
        if result:
            QMessageBox.information(self, "Удаление", "Объекты успешно удалены")
        else:
            QMessageBox.warning(self, "Удаление", "Ошибка при удалении объектов")
