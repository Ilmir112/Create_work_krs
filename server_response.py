import requests
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class ResponseWork(QMainWindow):
    SERVER_API = 'http://localhost:8000'

    @classmethod
    def read_wells_silencing_response_for_add_well(cls):
        return f'{ResponseWork.SERVER_API}/wells_silencing_response/add_data_well_silencing'

    @classmethod
    def read_wells_silencing_response_for_delete_well(cls):
        return f'{ResponseWork.SERVER_API}/wells_silencing_router/delete_well_silencing'

    def delete_wells_by_region(self, region, path=None):
        api_url = f'{ResponseWork.SERVER_API}{path}'

        data = {"region": region}
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: статус код {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None

    def add_well_in_database(self, payload, path=None):
        api_url = f'{ResponseWork.SERVER_API}{path}'
        params_dict = {"data": payload}
        try:
            response = requests.post(api_url, json=params_dict)
            if response.status_code == 200:
                QMessageBox.information(self, 'обновление', f'Вставлены в базу данных {len(payload)} скважин')
                return response.json()
            else:
                print(f"Ошибка: статус код {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Запрос не удался: {e}")
            return None





