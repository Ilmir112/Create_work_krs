import json
import re
import threading
from datetime import datetime

from data_list import ProtectedIsDigit, ProtectedIsNonNone
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
    def insert_well_data_from_database(cls, data_well, params=None):
        if params is None:
            params = {
                "well_number": data_well.well_number.get_value,
                "well_area": data_well.well_area.get_value
            }
        response = ApiClient.request_params_get(ApiClient.find_wells_data_response_filter_well_number_well_area(),
                                                params)
        if response:
            if response['column_direction']['diameter'] != 0:
                data_well.column_direction_true = True
            else:
                data_well.column_direction_true = False
            data_well.column_direction_diameter = ProtectedIsDigit(response["column_direction"]['diameter'])
            data_well.column_direction_wall_thickness = ProtectedIsDigit(
                response["column_direction"]['wall_thickness'])
            data_well.column_direction_length = data_list.ProtectedIsDigit(response["column_direction"]["shoe"])
            data_well.level_cement_direction = ProtectedIsDigit(response["column_direction"]["level_cement"])
            data_well.column_conductor_diameter = ProtectedIsDigit(response["column_conductor"]["diameter"])
            data_well.column_conductor_wall_thickness = ProtectedIsDigit(
                response["column_conductor"]["wall_thickness"])
            data_well.column_conductor_length = ProtectedIsDigit(response["column_conductor"]["shoe"])
            data_well.level_cement_conductor = ProtectedIsDigit(response["column_conductor"]["level_cement"])
            if data_well.column_conductor_diameter.get_value not in ['0', None, 0, '']:
                data_well.column_direction_true = True
            data_well.well_oilfield = ProtectedIsDigit(response["well_oilfield"])
            data_well.level_cement_column = ProtectedIsDigit(response["column_production"]["level_cement"])
            data_well.appointment_well = ProtectedIsNonNone(response["appointment"])
            data_well.column_diameter = ProtectedIsDigit(response["column_production"]["diameter"])
            data_well.column_wall_thickness = ProtectedIsDigit(response["column_production"]["wall_thickness"])
            data_well.shoe_column = ProtectedIsDigit(response["column_production"]["shoe"])
            data_well.head_column = ProtectedIsDigit(response["column_production"]["head"])
            data_well.diameter_doloto_ek = ProtectedIsDigit(response["diameter_doloto_ek"])
            data_well.column_additional = False
            data_well.column_additional_diameter = ProtectedIsDigit(response["column_additional"]["diameter"])
            if response["column_additional"]["diameter"] != 0:
                data_well.column_additional = True
            data_well.column_additional_wall_thickness = ProtectedIsDigit(
                response["column_additional"]["wall_thickness"])
            data_well.shoe_column_additional = ProtectedIsDigit(response["column_additional"]["shoe"])
            data_well.head_column_additional = ProtectedIsDigit(response["column_additional"]["head"])
            # data_well.curator = response["куратор"]
            data_well.dict_pump_shgn = response["equipment"]["ШГН"]["тип"]

            data_well.dict_pump_shgn['before'] = data_well.dict_pump_shgn['before']
            data_well.dict_pump_shgn['after'] = data_well.dict_pump_shgn['after']

            data_well.dict_pump_shgn_depth = response["equipment"]["ШГН"]["глубина "]

            data_well.dict_pump_shgn_depth['before'] = data_well.dict_pump_shgn_depth['before']
            data_well.dict_pump_shgn_depth['after'] = data_well.dict_pump_shgn_depth['after']

            data_well.dict_pump_ecn = response["equipment"]["ЭЦН"]["тип"]

            data_well.dict_pump_ecn['before'] = data_well.dict_pump_ecn['before']
            data_well.dict_pump_ecn['after'] = data_well.dict_pump_ecn['after']
            data_well.dict_pump_ecn_depth = response["equipment"]["ЭЦН"]["глубина "]

            data_well.dict_pump_ecn_depth['before'] = data_well.dict_pump_ecn_depth['before']
            data_well.dict_pump_ecn_depth['after'] = data_well.dict_pump_ecn_depth['after']
            data_well.paker_before = response["equipment"]["пакер"]["тип"]

            data_well.paker_before['before'] = data_well.paker_before['before']
            data_well.paker_before['after'] = data_well.paker_before['after']
            data_well.depth_fond_paker_before = response["equipment"]["пакер"]["глубина "]

            data_well.depth_fond_paker_before['before'] = data_well.depth_fond_paker_before['before']
            data_well.depth_fond_paker_before['after'] = data_well.depth_fond_paker_before['after']

            data_well.paker_second_before = response["equipment"]["пакер2"]["тип"]

            data_well.paker_second_before['before'] = data_well.paker_second_before['before']
            data_well.paker_second_before['after'] = data_well.paker_second_before['after']

            data_well.depth_fond_paker_second_before = response["equipment"]["пакер2"]["глубина "]

            data_well.depth_fond_paker_second_before['before'] = data_well.depth_fond_paker_second_before[
                'before']
            data_well.depth_fond_paker_second_before['after'] = data_well.depth_fond_paker_second_before[
                'after']

            data_well.dict_nkt_after = response["nkt_data"]["После"]
            data_well.dict_nkt_before = response["nkt_data"]["До"]
            data_well.dict_sucker_rod_after = response["sucker_pod"]["После"]
            data_well.dict_sucker_rod = response["sucker_pod"]["До"]

            data_well.inventory_number = response["inventory_number"]
            data_well.bottom_hole_drill = ProtectedIsDigit(response["bottom_hole_drill"])
            data_well.bottom_hole_artificial = ProtectedIsDigit(response["bottom_hole_artificial"])
            data_well.max_angle = ProtectedIsDigit(response["max_angle"])
            data_well.max_angle_depth = ProtectedIsDigit(response["max_angle_depth"])
            data_well.max_expected_pressure = ProtectedIsDigit(response["max_expected_pressure"])
            data_well.max_admissible_pressure = ProtectedIsDigit(response["max_admissible_pressure"])
            data_well.cdng = data_list.ProtectedIsNonNone(response["cdng"])
            data_well.date_commissioning = data_list.ProtectedIsNonNone(
                datetime.strptime(response["date_commissioning"], "%Y-%m-%d"))
            data_well.result_pressure_date = data_list.ProtectedIsNonNone(
                datetime.strptime(response["last_pressure_date"], "%Y-%m-%d"))

            # if 'ПВР план' in list(response.keys()):
            #     data_well.dict_perforation_project = response['ПВР план']
            # else:
            #     data_well.dict_perforation_project = ''

            # data_well.data_well_dict = well_data_dict

            from work_py.alone_oreration import well_volume
            data_well.well_volume_in_pz = []
            data_well.check_data_in_pz = []
            data_well.without_damping = False
            return data_well

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
            response = requests.get(url)

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
        elif obj in ["excel", "данные", "сводка"]:
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
    def find_gnkt_data_all(cls):
        return "/gnkt_data_router/find_gnkt_data_all"

    @classmethod
    def find_gnkt_data_by_gnkt(cls):
        return "/gnkt_data_router/find_gnkt_data_by_gnkt"

    @classmethod
    def add_data_gnkt(cls):
        return "/gnkt_data_router/add_data"

    @classmethod
    def find_gnkt_data_by_well_number(cls):
        return "/gnkt_data_router/find_gnkt_data_by_well_number"

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
    def read_wells_silencing_by_well_number_and_well_area(cls):
        return "/wells_silencing_router/find_well_silencing"

    @classmethod
    def read_wells_silencing_response_all(cls):
        return "/wells_silencing_router/find_well_silencing_all"

    @classmethod
    def send_logger_message(cls):
        return "/prometheus/logger_send"

    @classmethod
    def read_wells_silencing_response_first(cls):
        return "/wells_silencing_router/find_well_silencing_all_one"

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
    def send_logs(cls, params_dict, api_url):
        # serializable_params = cls.serialize_datetime(params_dict)
        return cls.request_post(api_url, params_dict)

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
