import re
import sqlite3

from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLineEdit, QHeaderView, QVBoxLayout
from openpyxl import load_workbook

def open_to_sqlite_without_juming(self, table, costumer, region):
    layout = QVBoxLayout()
    self.edit_well_number = QLineEdit()
    self.edit_well_number.setPlaceholderText("Ввести номер скважины для фильтрации")
    self.edit_well_number.textChanged.connect(self.filter)
    layout.addWidget(self.edit_well_number)

    data = get_data_from_db(self, region)

    table.setColumnCount(len(data[0]))
    table.setRowCount(len(data))
    table.setCellWidget(0, 0, self.edit_well_number)
    for row in range(len(data)):
        for col in range(len(data[row])):
            item = QTableWidgetItem(str(data[row][col]))
            table.setItem(row+1, col, item)

    table.setHorizontalHeaderLabels(['номер скважины', 'площадь', 'Текущий квартал'])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # layout.addWidget(table)
    self.setLayout(layout)

def open_to_sqlite_class_well(self, table, costumer, region):
    layout = QVBoxLayout()
    self.edit_well_number = QLineEdit()
    self.edit_well_number.setPlaceholderText("Ввести номер скважины для фильтрации")
    self.edit_well_number.textChanged.connect(self.filter_class)
    layout.addWidget(self.edit_well_number)

    self.edit_well_area = QLineEdit()
    self.edit_well_area.setPlaceholderText("Ввести площадь для фильтрации")
    self.edit_well_area.textChanged.connect(self.filter_class_area)
    layout.addWidget(self.edit_well_area)

    data = get_data_from_class_well_db(self, region)
    # print(data)

    table.setColumnCount(len(data[0]))
    table.setRowCount(len(data))
    table.setCellWidget(0, 1, self.edit_well_number)
    table.setCellWidget(0, 2, self.edit_well_area)
    for row in range(len(data)):
        for col in range(len(data[row])):
            if col in [5, 6, 10, 11, 13]:
                if data[row][col].replace('.', '').isdigit() and data[row][col].count('.') < 2:
                    item = QTableWidgetItem(str(round(float(data[row][col]), 1)))
                else:
                    item = QTableWidgetItem(str(data[row][col]))
            elif col in [9]:
                if data[row][col].replace('.', '').isdigit() and data[row][col].count('.') < 2:
                    item = QTableWidgetItem(str(round(float(data[row][col]), 7)))
                else:
                    item = QTableWidgetItem(str(data[row][col]))
            # elif col in [7]:
            #     date_string = data[row][col]
            #     date_format = "%Y-%m-%d %H:%M"
            #     date = datetime.strptime(date_string, date_format)
            #     print(date)
            #     item = QTableWidgetItem(str(date))
            else:
                item = QTableWidgetItem(str(data[row][col]))
            table.setItem(row + 1, col, item)

    table.setHorizontalHeaderLabels(['ЦДНГ','номер скважины', 'площадь', 'Месторождение', 'Категория \n по Рпл',
                                     'Ргд', 'Рпл', 'Дата замера', 'категория \nH2S', 'H2S-%', "H2S-мг/л",
                                        "H2S-мг/м3",'Категория по газу', "Газовый фактор", "версия от"])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # layout.addWidget(table)
    self.setLayout(layout)

def get_data_from_db(self, region):
    # Создание подключения к базе данных SQLite
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('data_base/database_without_juming.db')  # Замените database.db на имя вашей базы данных SQLite

    if not db.open():
        print("Не удалось установить соединение с базой данных.")
        return []

    # Выполнение SQL-запроса для получения данных
    query = QSqlQuery()
    query.prepare(f"SELECT well_number, deposit_area, today FROM {region}")  # Замените table_name на имя вашей таблицы SQLite
    if not query.exec():
        print("Не удалось выполнить запрос.")
        return []

    data = []
    while query.next():
        row = [query.value(i) for i in range(query.record().count())]
        data.append(row)

    db.close()

    return data

def get_data_from_class_well_db(self, region):
    # Создание подключения к базе данных SQLite
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('data_base/database_without_juming.db')  # Замените database.db на имя вашей базы данных SQLite
    print(db)
    print(region)
    print('ТГМ_классификатор')
    if not db.open():
        print("Не удалось установить соединение с базой данных.")
        return []

    # Выполнение SQL-запроса для получения данных
    query = QSqlQuery()
    query.prepare(f"SELECT cdng, well_number, deposit_area, oilfield, categoty_pressure,pressure_Ppl, pressure_Gst, date_measurement, categoty_h2s, h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, gas_factor, today FROM {region}")  # Замените table_name на имя вашей таблицы SQLite
    if not query.exec():
        print("Не удалось выполнить запрос.")
        return []

    data = []
    while query.next():
        row = [query.value(i) for i in range(query.record().count())]
        data.append(row)

    db.close()

    return data


def export_to_sqlite_without_juming(self, fname, costumer, region):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('data_base/database_without_juming.db')
    cursor = conn.cursor()
    region_list = ['ЧГМ', 'АГМ', 'ТГМ', 'ИГМ', 'КГМ', ]

    for region_name in region_list:
        if region_name == region:
            # # Удаление всех данных из таблицы
            # cursor.execute("DROP TABLE my_table")

            # Удаление всех данных из таблицы
            cursor.execute(f"DELETE FROM {region_name}")

            # Создание таблицы в базе данных
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {region_name}'
                           f'(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           f'well_number TEXT,'
                           f'deposit_area TEXT, '
                           f'today TEXT,'
                           f'region TEXT,'
                           f'costumer TEXT)')

            # Загрузка файла Excel
            wb = load_workbook(fname)
            ws = wb.active


            # Получение данных из Excel и запись их в базу данных
            for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                for col, value in enumerate(row):
                    if not value is None and col <= 18:
                        print(value)
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
                        if '01.01.' in str(value) or '01.04.' in str(value) or '01.07.' in str(value) or '01.10.' in str(value):

                            version_year = re.findall(r'[0-9.]', str(value))
                            version_year = ''.join(version_year)
                            if version_year[-1] == '.':
                                version_year = version_year[:-1]
                if index_row > 18:
                    break
            # print(region_name, version_year)
            # print(check_param)
            if check_param == region_name:
                mes = QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                          f'регион выбрано корректно  {region_name}')
                try:
                    # Получение данных из Excel и запись их в базу данных
                    for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                        if 'ПЕРЕЧЕНЬ' in row:
                            check_file = True
                        if 'Скважина' in row:
                            area_row = index_row + 2
                            for col, value in enumerate(row):
                                if not value is None and col <= 20:
                                    if 'Скважина' == value:
                                        well_column = col
                                    elif 'Площадь' == value:
                                        area_column = col

                    for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                        if index_row > area_row:

                            well_number = row[well_column]
                            area_well = row[area_column]

                            if well_number:
                                cursor.execute(
                                    f"INSERT INTO {region_name} (well_number, deposit_area, today, region, costumer) "
                                    f"VALUES (?,?,?,?,?)",
                                    (well_number, area_well, version_year, region_name, costumer))

                    mes = QMessageBox.information(self, 'данные обновлены', 'Данные обновлены')
                except:
                    mes = QMessageBox.warning(self, 'ОШИБКА', 'Выбран файл с не корректными данными')

            else:
                mes = QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                          f'в Данном перечне отсутствую скважины {region_name}')



    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()

def export_to_sqlite_class_well(self, fname, costumer, region):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('data_base/database_without_juming.db')
    cursor = conn.cursor()
    region_list = ['ЧГМ_классификатор', 'АГМ_классификатор', 'ТГМ_классификатор', 'ИГМ_классификатор', 'КГМ_классификатор', ]

    for region_name in region_list:
        if region in region_name:
            # # Удаление всех данных из таблицы
            # cursor.execute("DROP TABLE my_table")

            # Удаление всех данных из таблицы
            cursor.execute(f"DELETE FROM {region_name}")
            print(region_name)
            # Создание таблицы в базе данных
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {region_name}'
                           f'(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           f'cdng TEXT,'
                           f'well_number TEXT,'
                           f'deposit_area TEXT,'
                           f'oilfield TEXT,'
                           f'categoty_pressure TEXT,'
                           f'pressure_Ppl TEXT,'
                           f'pressure_Gst TEXT,'
                           f'date_measurement TEXT,'
                           f'categoty_h2s TEXT,'
                           f'h2s_pr TEXT,'
                           f'h2s_mg_l TEXT,'
                           f'h2s_mg_m TEXT,'
                           f'categoty_gf TEXT,'
                           f'gas_factor TEXT,'
                           f'today TEXT,'
                           f'region TEXT,'
                           f'costumer TEXT)')

            # Загрузка файла Excel
            wb = load_workbook(fname)
            ws = wb.active


            # Получение данных из Excel и запись их в базу данных
            for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                for col, value in enumerate(row):
                    if not value is None and col <= 18:
                        # print(value)
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
                        if '01.01.' in str(value) or '01.04.' in str(value) or '01.07.' in str(value) or '01.10.' in str(value):

                            version_year = re.findall(r'[0-9.]', str(value))
                            version_year = ''.join(version_year)
                            if version_year[-1] == '.':
                                version_year = version_year[:-1]
                if index_row > 18:
                    break
            print(region_name, version_year)
            print(check_param)
            if check_param in region_name:
                mes = QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                          f'регион выбрано корректно  {region_name}')
                try:
                    # Получение данных из Excel и запись их в базу данных
                    for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                        if 'Классификация' in row:
                            check_file = True
                            print(f' класс {check_file}')
                        if 'Скважина' in row:
                            area_row = index_row + 2
                            for col, value in enumerate(row):
                                if not value is None and col <= 20:
                                    if 'Скважина' == value:
                                        well_column = col
                                    elif 'Цех' ==value:
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
                                    elif 'Содержание сероводорода в продукции пробы' == value:
                                        categoty_h2s = col
                                        h2s_pr = col + 1
                                        h2s_mg_l = col + 2
                                        h2s_mg_m = col + 3

                                    elif 'Газовый фактор' == value:
                                        categoty_gf = col
                                        gas_factor = col + 1



                    for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                        if index_row > area_row:

                            well_number = row[well_column]
                            area_well = row[area_column]
                            oilfield_str = row[oilfield]

                            if well_number:
                                cursor.execute(
                                    f"INSERT INTO {region_name} (cdng, well_number, deposit_area, oilfield, "
                                    f"categoty_pressure, pressure_Ppl, pressure_Gst, date_measurement,categoty_h2s, "
                                    f"h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, gas_factor, today, region) "
                                    f"VALUES (?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?)",
                                    (row[cdng], well_number, area_well, oilfield_str, row[categoty_pressure], row[pressure_Ppl],
                                     row[pressure_Gst], row[date_measurement], row[categoty_h2s], row[h2s_pr], row[h2s_mg_l],
                                     row[h2s_mg_m], row[categoty_gf], row[gas_factor], version_year, region))

                    mes = QMessageBox.information(self, 'данные обновлены', 'Данные обновлены')
                except:
                    mes = QMessageBox.warning(self, 'ОШИБКА', 'Выбран файл с не корректными данными')

            else:
                mes = QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                          f'в Данном перечне отсутствую скважины {region_name}')



    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()