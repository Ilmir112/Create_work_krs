import json
import os
import sqlite3
import sys
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from dotenv import load_dotenv
import psycopg2

import data_list

from typing import Dict, List
from abc import ABC, abstractmethod

from decrypt import decrypt
from server_response import ApiClient


class DatabaseConnection(ABC):
    @abstractmethod
    def connect_to_database(self):
        pass

    @abstractmethod
    def fetch_user(self, last_name: str, first_name: str, second_name: str) -> Dict:
        pass


class PostgresConnection(DatabaseConnection):
    def __init__(self, db_name):
        self.db_name = db_name
        self.path_index = '%s'

    def connect_to_database(self):
        # Определяем путь к файлу .env
        ext_data_dir = os.getcwd()
        if getattr(sys, 'frozen', False):
            ext_data_dir = sys._MEIPASS

        load_dotenv(dotenv_path=os.path.join(ext_data_dir, '.env'))

        db_user = decrypt('DB_USER')
        db_password = decrypt('DB_PASSWORD')
        db_host = decrypt('DB_HOST')
        db_port = decrypt('DB_PORT')

        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )

            return connection
        except Exception as e:
            print(f'Ошибка подключения к базе {type(e).__name__}\n\n{str(e)}')
            return None

    def fetch_user(self, last_name: str, first_name: str, second_name: str) -> Dict:
        return {'id': first_name, 'last_name': last_name}


class CursorContext:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        try:
            self.cursor = self.connection.cursor()
            return self.cursor
        except:
            return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.cursor.close()
        except:
            pass


class SqlLiteConnection(DatabaseConnection):
    def __init__(self, db_name):
        self.db_name = db_name
        self.path_index = '?'

    @staticmethod
    def connect_to_db_path(name_base):
        # Получаем текущий каталог приложения
        current_dir = os.path.dirname(__file__)

        # Формируем полный путь к файлу базы данных
        db_path = os.path.join(current_dir, name_base)

        return db_path

    def connect_to_database(self):
        try:
            db_path = self.connect_to_db_path(self.db_name)
            connection = sqlite3.connect(f'{db_path}')

            return connection
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Ошибка подключения к базе {type(e).__name__}\n\n{str(e)}')
            return None

    def fetch_user(self, last_name: str, first_name: str, second_name: str) -> Dict:
        return {'id': first_name, 'last_name': last_name}


class UserService:
    def __init__(self, connect_to_database: DatabaseConnection):
        self.db_connection = connect_to_database.connect_to_database()
        self.path_index = connect_to_database.path_index

    def get_user(self, last_name: str, first_name: str, second_name: str) -> Dict:

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(
                f"SELECT last_name, first_name, second_name, password, position_in, organization FROM users "
                f"WHERE last_name=({self.path_index}) AND first_name=({self.path_index}) "
                f"AND second_name=({self.path_index})",
                (last_name, first_name, second_name))
            password_base = cursor.fetchone()
            password_base_dict = None
            if password_base:
                password_base_dict = {'last_name': password_base[0],
                                      'first_name': password_base[1],
                                      'second_name': password_base[2],
                                      'password': password_base[3],
                                      'pozition_id': password_base[4],
                                      'contractor': password_base[5]}

            return password_base_dict

    def get_users_list(self) -> List:

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute("SELECT last_name, first_name, second_name, position_in, organization  FROM users")

            users = cursor.fetchall()
            users_list = []

            for user in users:
                position = user[3] + " " + user[4]
                user_name = user[0] + " " + user[1] + ' ' + user[2] + ' '
                users_list.append((position, user_name))

            return users_list


class RegistrationService:
    def __init__(self, connect_to_database: DatabaseConnection):
        self.db_connection = connect_to_database.connect_to_database()
        self.path_index = connect_to_database.path_index

    def check_user_in_database(self, last_name, first_name, second_name) -> List:

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            # Проверяем, существует ли пользователь с таким именем
            cursor.execute(f"SELECT last_name, first_name, second_name  FROM users "
                           f"WHERE last_name=({self.path_index}) AND first_name=({self.path_index}) "
                           f"AND second_name=({self.path_index})",
                           (last_name, first_name, second_name))

        existing_user = cursor.fetchone()

        return existing_user

    def registration_user(self, last_name, first_name, second_name, position_in, organization, password, region):

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f"INSERT INTO users (last_name, first_name, second_name, position_in, organization, password, ctkrs) " \
                    f"VALUES ({self.path_index},{self.path_index}, {self.path_index}, {self.path_index}," \
                    f" {self.path_index}, {self.path_index}, {self.path_index})"
            cursor.execute(
                query,
                (last_name, first_name, second_name, position_in, organization, password, region))
            # Не забудьте сделать коммит
            self.db_connection.commit()


class WorkDatabaseWell:
    from find import FindIndexPZ
    def __init__(self, connect_to_database: DatabaseConnection, dict_data_well=None):
        self.db_connection = connect_to_database.connect_to_database()
        self.path_index = connect_to_database.path_index
        self.dict_data_well = dict_data_well

    def get_tables_starting_with(self, well_number, well_area, work_plan, type_kr):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f"""SELECT well_number, area_well, type_kr, work_plan
                                FROM wells
                                WHERE well_number={self.path_index} AND area_well={self.path_index} 
                                AND type_kr={self.path_index} AND work_plan={self.path_index}"""
            cursor.execute(query, (str(well_number), well_area, type_kr, work_plan))

            rezult = cursor.fetchone()
            return rezult

    def determining_well_in_database(self, cursor, well_number, well_area, contractor, costumer, work_plan_str):

        cursor.execute(f"""
                                   SELECT EXISTS (
                                       SELECT 1 
                                       FROM wells
                                       WHERE well_number = {self.path_index} AND area_well = {self.path_index} 
                                       AND contractor = {self.path_index} 
                                       AND costumer = {self.path_index} AND work_plan = {self.path_index}
                                   ), today -- Добавляем contractor в SELECT
                               FROM wells 
                               WHERE well_number = {self.path_index} AND area_well ={self.path_index} AND 
                               contractor = {self.path_index} AND 
                               costumer = {self.path_index} AND work_plan ={self.path_index}
                               """, (
            str(well_number), well_area, contractor, costumer, work_plan_str,
            str(well_number), well_area, contractor, costumer, work_plan_str))

        row_exists = cursor.fetchone()
        return row_exists

    def insert_in_database_well_data(self, data_well: FindIndexPZ, contractor: str, costumer: str, excel: str) -> None:
        from server_response import ApiClient
        work_plan = data_well.work_plan
        well_number = data_well.well_number.get_value
        well_area = data_well.well_area.get_value

        data_well_dict = json.dumps(ApiClient.serialize_datetime(data_well.data_well_dict), ensure_ascii=False)
        excel_json = json.dumps(excel, ensure_ascii=False)
        date_today = datetime.now().strftime('%Y-%m-%d')

        type_kr = data_well.type_kr.split(' ')[0]

        data_paragraph = json.dumps(data_well.data_list, ensure_ascii=False)
        cdng = data_well.cdng.get_value

        wellhead_fittings = data_well.wellhead_fittings
        well_oilfield = data_well.well_oilfield.get_value
        inv_number = data_well.inventory_number.get_value
        appointment_well = data_well.appointment_well.get_value
        category_dict = json.dumps(data_well.dict_category, ensure_ascii=False)
        angle_data = json.dumps(data_well.angle_data, ensure_ascii=False)

        # print(row, self.dict_data_well["count_row_well"])

        if 'dop_plan' in work_plan:
            work_plan_str = f'ДП№{data_well.number_dp}'
        elif 'krs' in work_plan:
            work_plan_str = 'ПР'
        elif 'prs' in work_plan:
            work_plan_str = 'ПР_ТРС'
        elif work_plan == 'plan_change':
            if data_well.work_plan_change == 'krs':
                work_plan_str = 'ПР'
            else:
                work_plan_str = f'ДП№{data_well.number_dp}'

        try:
            if not self.db_connection:
                return None
            with CursorContext(self.db_connection.cursor()) as cursor:
                row_exists = self.determining_well_in_database(cursor, well_number, well_area,
                                                               contractor, costumer, work_plan_str)
                if row_exists:
                    row_exists, date_in_base = row_exists
                    reply = QMessageBox.question(None, 'Строка найдена',
                                                 f'План работ {well_number} {well_area} {work_plan_str} уже '
                                                 f'существует от {date_in_base} в базе данных. '
                                                 f'Обновить данные?')
                    if reply == QMessageBox.Yes:
                        cursor.execute(f"""
                                        DELETE FROM wells                                                                                                   
                                        WHERE well_number ={self.path_index} AND area_well ={self.path_index} 
                                        AND contractor ={self.path_index}
                                         AND costumer ={self.path_index} AND work_plan ={self.path_index} 
                                         AND type_kr={self.path_index} AND today={self.path_index}
                                                    """, (
                            str(well_number), well_area, contractor, costumer, work_plan_str,
                            type_kr, date_in_base))

                        QMessageBox.information(None, 'Успешно', 'Данные в базе обновлены')
                    else:
                        # Не забудьте сделать коммит
                        self.db_connection.commit()

                        # Закрытие соединения после завершения всех операций
                        self.db_connection.close()
                        return

                # Подготовленный запрос для вставки данных с параметрами
                query = f"INSERT INTO wells " \
                        f"VALUES ({self.path_index}, {self.path_index}, {self.path_index}, " \
                        f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                        f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                        f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                        f"{self.path_index}, {self.path_index}, {self.path_index})"

                data_values = (str(well_number), well_area,
                               data_well_dict, excel_json, contractor, data_list.costumer,
                               work_plan_str, data_list.user[1], type_kr, data_paragraph, cdng, category_dict,
                               well_oilfield, appointment_well, str(inv_number), wellhead_fittings, angle_data,
                               date_today)

                # Выполнение запроса с использованием параметров
                cursor.execute(query, data_values)
                # Не забудьте сделать коммит
                self.db_connection.commit()
                # # Закрытие соединения после завершения всех операций
                # self.db_connection.close()



        except psycopg2.Error as e:
            # Выведите сообщение об ошибке
            QMessageBox.warning(None, 'Ошибка', f'Ошибка подключения к базе данных  well_data'
                                                f' {type(e).__name__}\n\n{str(e)}')
        except sqlite3.Error as e:
            # Выведите сообщение об ошибке
            QMessageBox.warning(None, 'Ошибка', f'Ошибка подключения к базе данных  well_data'
                                                f' {type(e).__name__}\n\n{str(e)}')

    def insert_data_in_chemistry(self, data_well: FindIndexPZ) -> None:
        if data_well.work_plan in ['dop_plan', 'dop_plan_in_base']:
            string_work = f' ДП№ {data_well.number_dp}'
        elif data_well.work_plan == 'krs':
            string_work = 'ПР'
        elif data_well.work_plan == 'plan_change':
            if data_well.work_plan_change == 'krs':
                string_work = 'ПР изм'
            else:
                string_work = f'ДП№{data_well.number_dp} изм '

        elif data_well.work_plan == 'gnkt_bopz':
            string_work = 'ГНКТ БОПЗ ВНС'
        elif data_well.work_plan == 'gnkt_opz':
            string_work = 'ГНКТ ОПЗ'
        elif data_well.work_plan == 'gnkt_after_grp':
            string_work = 'ГНКТ ОСВ ГРП'
        else:
            string_work = 'ГНКТ'

        date_today = datetime.now()
        data_work = (data_well.well_number.get_value,
                     data_well.well_area.get_value,
                     data_well.region,
                     data_list.costumer,
                     data_list.contractor,
                     string_work,
                     data_well.type_kr.split(" ")[0],
                     date_today,
                     data_list.DICT_VOLUME_CHEMISTRY['цемент'],
                     data_list.DICT_VOLUME_CHEMISTRY['HCl'],
                     data_list.DICT_VOLUME_CHEMISTRY['HF'],
                     data_list.DICT_VOLUME_CHEMISTRY['NaOH'],
                     data_list.DICT_VOLUME_CHEMISTRY['ВТ СКО'],
                     data_list.DICT_VOLUME_CHEMISTRY['Глина'],
                     data_list.DICT_VOLUME_CHEMISTRY['песок'],
                     data_list.DICT_VOLUME_CHEMISTRY['РПК'],
                     data_list.DICT_VOLUME_CHEMISTRY['РПП'],
                     data_list.DICT_VOLUME_CHEMISTRY["извлекаемый пакер"],
                     data_list.DICT_VOLUME_CHEMISTRY["ЕЛАН"],
                     data_list.DICT_VOLUME_CHEMISTRY['растворитель'],
                     data_list.DICT_VOLUME_CHEMISTRY["РИР 2С"],
                     data_list.DICT_VOLUME_CHEMISTRY["РИР ОВП"],
                     data_list.DICT_VOLUME_CHEMISTRY['гидрофабизатор'],
                     round(data_well.norm_of_time, 1),
                     data_well.fluid
                     )

        cursor = self.db_connection.cursor()
        query = f"""SELECT * FROM chemistry
           WHERE well_number={self.path_index} AND well_area={self.path_index} AND region={self.path_index}
            AND costumer={self.path_index} AND contractor={self.path_index} AND work_plan={self.path_index} 
            AND type_kr={self.path_index}
           """

        cursor.execute(query, (data_work[:7]))

        row_exists = cursor.fetchone()

        if row_exists:
            query2 = f'''UPDATE chemistry
            SET today={self.path_index}, cement={self.path_index}, HCl={self.path_index}, HF={self.path_index}, 
            NaOH={self.path_index}, VT_SKO={self.path_index},
                clay={self.path_index}, sand={self.path_index}, RPK={self.path_index}, RPP={self.path_index}, 
                RKI={self.path_index},
                 ELAN={self.path_index},ASPO={self.path_index}, RIR_2C={self.path_index}, 
                 RIR_OVP={self.path_index}, gidrofabizator={self.path_index}, 
                 norm_time={self.path_index}, fluid={self.path_index}
            WHERE well_number={self.path_index} AND well_area={self.path_index} AND region={self.path_index} AND
                costumer={self.path_index} AND contractor={self.path_index} AND work_plan={self.path_index} 
                AND type_kr={self.path_index}'''
            data_work2 = data_work[7:] + data_work[:7]

            cursor.execute(query2, data_work2)

        else:
            query = f"INSERT INTO chemistry " \
                    f"VALUES ({self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}," \
                    f" {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index})"
            cursor.execute(query, data_work)
        self.db_connection.commit()
        if cursor:
            cursor.close()
        if self.db_connection:
            self.db_connection.close()

    def read_excel_in_base(self, number_well, area_well, work_plan, type_kr):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(f"SELECT excel_json "
                           f"FROM wells "
                           f"WHERE well_number = {self.path_index} AND area_well = {self.path_index} "
                           f"AND contractor = {self.path_index} AND costumer = {self.path_index}"
                           f" AND work_plan={self.path_index} AND type_kr={self.path_index}",
                           (str(number_well), area_well, data_list.contractor, data_list.costumer, work_plan, type_kr))
            data_well = cursor.fetchall()
            return data_well

    def extraction_data(self, well_number, well_area, type_kr, work_plan, date_table, contractor):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f'''
                    SELECT data_change_paragraph, data_well, type_kr, category_dict, angle_data FROM wells 
                    WHERE well_number={self.path_index} AND area_well={self.path_index} AND type_kr={self.path_index} 
                    AND work_plan={self.path_index} AND today={self.path_index} AND contractor={self.path_index}'''

            cursor.execute(query,
                           (str(well_number), well_area, type_kr, work_plan, date_table, contractor))

            result_table = cursor.fetchone()
            return result_table

    def check_well_in_database_well_data(self, number_well: str) -> List:
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(
                f"SELECT well_number, area_well, type_kr, today, work_plan FROM wells "
                f"WHERE well_number={self.path_index} AND contractor={self.path_index} AND costumer ={self.path_index}",
                (str(number_well), data_list.contractor, data_list.costumer))

            # Получение всех результатов
            wells_with_data = cursor.fetchall()
            return wells_with_data

    def check_in_database_well_data(self, number_well, area_well, work_plan, today):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(f"SELECT data_well, today, type_kr, category_dict, well_oilfield, "
                           f"appointment, inv_number, wellhead_fittings, angle_data "
                           f"FROM wells "
                           f"WHERE well_number = {self.path_index} AND area_well = {self.path_index} "
                           f"AND contractor = {self.path_index} AND costumer = {self.path_index} AND "
                           f"work_plan={self.path_index} AND today={self.path_index}",
                           (str(number_well), area_well, data_list.contractor, data_list.costumer, work_plan, today))

            data_well = cursor.fetchone()
            return data_well

        return False

    def check_in_database_dp_data(self, number_well, area_well, work_plan):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(f"SELECT data_well, today, type_kr, category_dict "
                           f"FROM wells "
                           f"WHERE well_number = {self.path_index} AND area_well = {self.path_index} "
                           f"AND contractor = {self.path_index} AND costumer = {self.path_index} AND "
                           f"work_plan={self.path_index}",
                           (str(number_well), area_well, data_list.contractor, data_list.costumer, work_plan))

            data_well = cursor.fetchone()
            return data_well

        return False


class CheckWellExistence:
    def __init__(self, connect_to_database: DatabaseConnection, path_index="%s"):
        self.db_connection = connect_to_database.connect_to_database()
        self.path_index = connect_to_database.path_index

    @staticmethod
    def check_correct_month():
        current_year = datetime.now().year
        month = datetime.now().month

        # print(f'месяц {month}')
        date_string = None
        if 1 <= month < 4:
            date_string = datetime(current_year, 1, 1).strftime('%d.%m.%Y')

        elif 4 <= month < 7:
            date_string = datetime(current_year, 4, 1).strftime('%d.%m.%Y')

        elif 7 <= month < 10:
            date_string = datetime(current_year, 7, 1).strftime('%d.%m.%Y')

        elif 10 <= month <= 12:
            date_string = datetime(current_year, 10, 1).strftime('%d.%m.%Y')
        print(f'Корректная таблица перечня без глушения от {date_string}')
        return date_string

    def create_table_without_juming(self, region_name: str):

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            self.drop_table(cursor, region_name)

            # Создание таблицы в базе данных
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {region_name}'
                           f'(well_number TEXT,'
                           f'deposit_area TEXT, '
                           f'today TEXT,'
                           f'region TEXT,'
                           f'costumer TEXT)')

    def insert_data_in_table_without_juming(self, well_number: str, area_well: str,
                                            version_year: str, region_name: str, costumer: str):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f"INSERT INTO {region_name} (well_number, deposit_area, today, region, costumer) " \
                    f"VALUES ({self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index})"

            cursor.execute(query,
                           (well_number, area_well, version_year, region_name, costumer))
            # print(well_number, version_year)
            # Не забудьте сделать коммит
            self.db_connection.commit()

    def create_table_classification(self, region_name: str):

        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            self.drop_table(cursor, region_name)
            # Создание таблицы, если она не существует
            cursor.execute(f"""
                            CREATE TABLE IF NOT EXISTS {region_name} (
                                ID SERIAL PRIMARY KEY,
                                cdng TEXT,
                                well_number TEXT,
                                deposit_area TEXT,
                                oilfield TEXT,
                                categoty_pressure TEXT,
                                pressure_Ppl TEXT,
                                pressure_Gst TEXT,
                                date_measurement TEXT,
                                categoty_h2s TEXT,
                                h2s_pr TEXT,
                                h2s_mg_l TEXT,
                                h2s_mg_m TEXT,
                                categoty_gf TEXT,
                                gas_factor TEXT,
                                today TEXT,
                                region TEXT,
                                costumer TEXT
                            );
                        """)
            # Не забудьте сделать коммит
            self.db_connection.commit()

    @staticmethod
    def read_excel_file_classification(ws):

        # Определение столбцов
        well_column, cdng, area_column, oilfield, categoty_pressure = None, None, None, None, None
        pressure_Gst, date_measurement, pressure_Ppl, categoty_h2s = None, None, None, None
        h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, gas_factor = None, None, None, None, None
        area_row = 0
        check_file = False
        check_param = None

        for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
            if 'Классификация' in row:
                check_file = True
            elif any(['фонд' in str(value).lower() for col, value in enumerate(row)]):
                for col, value in enumerate(row):
                    if 'туймазин' in str(value).lower():
                        check_param = 'ТГМ'
                    if 'ишимбай' in str(value).lower():
                        check_param = 'ИГМ'
                    if 'чекмагуш' in str(value).lower():
                        check_param = 'ЧГМ'
                    if 'красно' in str(value).lower():
                        check_param = 'КГМ'
                    if 'арлан' in str(value).lower():
                        check_param = 'АГМ'

            elif 'Скважина' in row:
                area_row = index_row + 2
                for col, value in enumerate(row):
                    if not value is None and col <= 20:
                        if 'Скважина' == value:
                            well_column = col
                        elif 'Цех' == value:
                            cdng = col
                        elif 'Площадь' == value:
                            area_column = col
                        elif 'Месторождение' == value:
                            oilfield = col
                        elif 'Пластовое давление' == value:
                            categoty_pressure = col
                            pressure_Gst = col + 1
                            date_measurement = col + 2
                            pressure_Ppl = col + 3
                        elif 'содержание сероводорода' in str(value).lower():
                            categoty_h2s = col
                            h2s_pr = col + 1
                            h2s_mg_l = col + 2
                            h2s_mg_m = col + 3
                        elif 'Газовый фактор' == value:
                            categoty_gf = col
                            gas_factor = col + 1
        return check_param, well_column, cdng, area_column, oilfield, categoty_pressure, \
            pressure_Gst, date_measurement, pressure_Ppl, categoty_h2s, h2s_pr, h2s_mg_l, \
            h2s_mg_m, categoty_gf, gas_factor, area_row, check_file

    def insert_data_in_classification(self, region_name, cdng, well_number, area_well,
                                      oilfield_str, categoty_pressure, pressure_Ppl, pressure_Gst,
                                      date_measurement, categoty_h2s,
                                      h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf,
                                      gas_factor, version_year, region, costumer):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f"""INSERT INTO {region_name} (
                                cdng, well_number, deposit_area, oilfield,
                                categoty_pressure, pressure_Ppl, pressure_Gst, date_measurement,
                                categoty_h2s, h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, gas_factor,
                                today, region, costumer
                            )
                            VALUES ({self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, 
                            {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, 
                            {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, 
                            {self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, 
                            {self.path_index});
                        """
            data = (cdng, well_number, area_well,
                    oilfield_str, categoty_pressure, pressure_Ppl, pressure_Gst,
                    date_measurement, categoty_h2s,
                    h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf,
                    gas_factor, version_year, region, costumer)
            print(well_number, version_year)

            cursor.execute(query, data)

            self.db_connection.commit()

    def drop_table(self, cursor, region_name):
        cursor.execute(f"DROP TABLE IF EXISTS {region_name}")

    def checking_well_database_month(self, region: str):
        date_string = self.check_correct_month()
        result = None
        if data_list.connect_in_base is False:

            if not self.db_connection:
                return None
            cursor = self.db_connection.cursor()
            query = f"SELECT *  FROM {region} WHERE today=({self.path_index})"
            cursor.execute(query, (date_string,))

            result = cursor.fetchone()

            if cursor:
                cursor.close()
        else:
            region_json = {"region": region}
            data = ApiClient.request_post(ApiClient.read_wells_silencing_response_first(), region_json)

            if data:
                date_in_base = data["today"]
                date_in_base = datetime.strptime(date_in_base, "%Y-%m-%d").strftime('%d.%m.%Y')
                if date_in_base == date_string:
                    result = True

        # if self.db_connection:
        #     self.db_connection.close()

        if result is None:
            QMessageBox.warning(None, 'Некорректная дата перечня',
                                f'Необходимо обновить перечень скважин без '
                                f'глушения на текущий квартал {region} от {date_string}, '
                                f'необходимо обратиться к администратору')
            return True
        else:
            return False

    def checking_well_database_without_juming(self, well_number, deposit_area, region):
        stop_app = self.checking_well_database_month(region)
        if data_list.connect_in_base is False:
            if not self.db_connection:
                return None
            with CursorContext(self.db_connection.cursor()) as cursor:
                # Проверка наличия записи в базе данных
                cursor.execute(f"SELECT * "
                               f"FROM {region} "
                               f"WHERE well_number=({self.path_index}) AND deposit_area=({self.path_index})",
                               (str(well_number), deposit_area.replace('_', ' ')))
                result = cursor.fetchone()


        else:
            self.params = {
                "well_number": well_number,
                "well_area": deposit_area,
            }
            result = ApiClient.request_params_get(
                ApiClient.read_wells_silencing_by_well_number_and_well_area(),
                self.params,
            )
        # Если запись найдена, возвращается True, в противном случае возвращается False
        if result:
            QMessageBox.information(None, 'перечень без глушения',
                                    f'Скважина {well_number} {deposit_area} состоит в перечне скважин без'
                                    f' глушения на текущий квартал, '
                                    f'в перечне от  {region}')
            return True, stop_app
        return False, stop_app

    def check_category(self, well_number: str, deposit_area: str, region: str) -> List:
        try:
            if not self.db_connection:
                return None
            with CursorContext(self.db_connection.cursor()) as cursor:
                # Проверка наличия записи в базе данных
                query = f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM {region}_классификатор " \
                        f"WHERE well_number =({self.path_index}) and deposit_area =({self.path_index})"
                data = (str(well_number.get_value), str(deposit_area.get_value).replace("_", " "))
                cursor.execute(query, data)

                result = cursor.fetchone()
                return result
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка работы с базой данных {e}')

    def get_data_from_class_well_db(self, region) -> List:
        # Выполнение SQL-запроса для получения данных
        with CursorContext(self.db_connection.cursor()) as cur:
            cur.execute(f"""
                        SELECT cdng, well_number, deposit_area, oilfield, categoty_pressure,
                               pressure_Ppl, pressure_Gst, date_measurement, categoty_h2s,
                               h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, gas_factor, today
                        FROM {region};
                                    """)
            data = cur.fetchall()
            return data

    def get_data_from_db(self, region: str) -> List:
        # Выполнение SQL-запроса для получения данных
        with CursorContext(self.db_connection.cursor()) as cur:
            cur.execute(f"""
                                SELECT well_number, deposit_area, today
                                FROM {region};
                            """)
            data = cur.fetchall()
            return data
        return None


class GnktDatabaseWell:
    def __init__(self, connect_to_database: DatabaseConnection, path_index="%s"):
        self.db_connection = connect_to_database.connect_to_database()
        self.path_index = connect_to_database.path_index

    def check_data_base_gnkt(self, contractor, well_number, well_area):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as self.cursor:
            filenames = f"{well_number} {well_area} "

            query = f"SELECT * FROM gnkt_{contractor} WHERE well_number LIKE ({self.path_index})"

            # Выполнение запроса
            self.cursor.execute(query, ('%' + filenames + '%',))

            result = self.cursor.fetchall()
            return result

    def update_data_gnkt(self, contractor, previuos_well):
        well_number = previuos_well.split(' ')[0]
        well_area = previuos_well.split(' ')[1]
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            query = f"SELECT * FROM gnkt_{contractor} WHERE well_number LIKE ({self.path_index})"
            filenames = f"{well_number} {well_area} "
            # Выполнение запроса
            cursor.execute(query, ('%' + filenames + '%',))
            result = cursor.fetchone()
        return result

    def insert_data_base_gnkt(self, contractor, gnkt_number, well_name, gnkt_length, diametr_length, iznos,
                              pipe_mileage, pipe_fatigue, previous_well, current_datetime, pvo):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            data_values = (gnkt_number, well_name, gnkt_length, diametr_length, iznos,
                           pipe_mileage, pipe_fatigue, previous_well, current_datetime, pvo)

            # Подготовленный запрос для вставки данных с параметрами
            query = f"INSERT INTO gnkt_{contractor} " \
                    f"(gnkt_number, well_number, length_gnkt, diameter_gnkt, wear_gnkt, mileage_gnkt, " \
                    f"tubing_fatigue, previous_well, today, pvo_number) " \
                    f"VALUES ({self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index}, {self.path_index}, {self.path_index}, " \
                    f"{self.path_index}, {self.path_index})"

            # Выполнение запроса с использованием параметров
            cursor.execute(query, data_values)
            # Не забудьте сделать коммит
            self.db_connection.commit()

    def read_database_gnkt(self, contractor, gnkt_number):
        if not self.db_connection:
            return None
        with CursorContext(self.db_connection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM gnkt_{contractor} WHERE gnkt_number =(%s)", (gnkt_number,))
            return cursor.fetchall()


def connection_to_database(DB_NAME):
    if data_list.connect_in_base:
        try:
            db = PostgresConnection(DB_NAME)
            db2 = db.connect_to_database()
            if db2:
                return db
            else:
                return db2

        except psycopg2.Error as e:
            data_list.connect_in_base = False
            print(f'Ошибка подключения к базе данных, проверьте наличие интернета {type(e).__name__}\n\n{str(e)}')

            return False

    else:
        DB_NAME = f'{DB_NAME}.db'
        try:
            db = SqlLiteConnection(DB_NAME)
            db.connect_to_database()
        except sqlite3.Error as e:
            QMessageBox.warning(None, 'Ошибка',
                                f'Ошибка подключения к базе данных, '
                                f'проверьте наличие базы {type(e).__name__}\n\n{str(e)}')
        return db


#
#
#
# # Функция подключения к базе данных
def connect_to_database(DB_NAME):
    conn = connection_to_database(DB_NAME)
    if conn is None:
        QMessageBox.information(None, 'Проверка соединения',
                                'Проверка показало что с облаком соединения нет, '
                                'будет использована локальная база данных')

        return False, False
    return True, conn

# print(connect_to_database(DB_NAME))
