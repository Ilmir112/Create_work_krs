import json
import os
import re
import sqlite3

import openpyxl
import psycopg2
import well_data

from datetime import datetime

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLineEdit, QHeaderView, QVBoxLayout, QMainWindow, QWidget, \
    QTableWidget

from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Color
from openpyxl.utils import get_column_letter, range_boundaries
from data_base.config_base import connect_to_database, connection_to_database, CheckWellExistence

from PIL import Image
from main import MyMainWindow
from work_py.advanted_file import definition_plast_work


class Classifier_well(MyMainWindow):
    number_well = None

    def __init__(self, costumer, region, classifier_well, parent=None):

        super(Classifier_well, self).__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_class = QTableWidget()
        self.region = region
        self.costumer = costumer
        self.number_well = None
        if self.dict_data_well["well_number"]:
            self.number_well = self.dict_data_well["well_number"]._value

        self.setCentralWidget(self.table_class)
        self.model = self.table_class.model()
        if classifier_well == 'classifier_well':
            self.open_to_sqlite_class_well(costumer, region)
        elif classifier_well == 'damping':
            self.open_to_sqlite_without_juming(costumer, region)

    def open_to_sqlite_without_juming(self, costumer, region):
        layout = QVBoxLayout()
        self.edit_well_number = QLineEdit()

        self.edit_well_number.setPlaceholderText("Ввести номер скважины для фильтрации")

        self.edit_well_number.textChanged.connect(self.filter)
        self.edit_well_number.setText(self.number_well)
        layout.addWidget(self.edit_well_number)

        data = self.get_data_from_db(region)
        if data:

            self.table_class.setColumnCount(len(data[0]))
            self.table_class.setRowCount(len(data))
            self.table_class.setCellWidget(0, 0, self.edit_well_number)
            for row in range(len(data)):
                for col in range(len(data[row])):
                    item = QTableWidgetItem(str(data[row][col]))
                    self.table_class.setItem(row + 1, col, item)

        self.table_class.setHorizontalHeaderLabels(['номер скважины', 'площадь', 'Текущий квартал'])
        self.table_class.horizontalHeader().setStretchLastSection(True)
        self.table_class.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # layout.addWidget(table)
        self.setLayout(layout)

    def closeEvent(self, event):
        if self.sender() == None:  # Проверяем вызывающий объект
            # Закрываем основное окно при закрытии окна входа
            self.new_window = None
            event.accept()  # Принимаем событие закрытия

    def open_to_sqlite_class_well(self, costumer, region):
        layout = QVBoxLayout()
        self.edit_well_number = QLineEdit()
        self.edit_well_number.setPlaceholderText("Ввести номер скважины для фильтрации")

        self.edit_well_number.textChanged.connect(self.filter_class)
        self.edit_well_number.setText(self.number_well)
        layout.addWidget(self.edit_well_number)

        self.edit_well_area = QLineEdit()
        self.edit_well_area.setPlaceholderText("Ввести площадь для фильтрации")
        self.edit_well_area.textChanged.connect(self.filter_class_area)
        layout.addWidget(self.edit_well_area)
        region = f'{region}_классификатор'
        # print(region)
        data = self.get_data_from_class_well_db(region)
        if data:
            # print(data)

            self.table_class.setColumnCount(len(data[0]))
            self.table_class.setRowCount(len(data))
            self.table_class.setCellWidget(0, 1, self.edit_well_number)
            self.table_class.setCellWidget(0, 2, self.edit_well_area)
            for row in range(len(data)):
                for col in range(len(data[row])):
                    if col in [5, 6, 10, 11, 13]:
                        if str(data[row][col]).replace('.', '').isdigit() and str(data[row][col]).count('.') < 2:
                            item = QTableWidgetItem(str(round(float(data[row][col]), 1)))
                        else:
                            item = QTableWidgetItem(str(data[row][col]))
                    elif col in [9]:
                        if str(data[row][col]).replace('.', '').isdigit() and str(data[row][col]).count('.') < 2:
                            item = QTableWidgetItem(str(round(float(data[row][col]), 7)))
                        else:
                            item = QTableWidgetItem(str(data[row][col]))

                    else:
                        item = QTableWidgetItem(str(data[row][col]))
                    self.table_class.setItem(row + 1, col, item)

        self.table_class.setHorizontalHeaderLabels(
            ['ЦДНГ', 'номер скважины', 'площадь', 'Месторождение', 'Категория \n по Рпл',
             'Ргд', 'Рпл', 'Дата замера', 'категория \nH2S', 'H2S-%', "H2S-мг/л",
             "H2S-мг/м3", 'Категория по газу', "Газовый фактор", "версия от"])
        self.table_class.horizontalHeader().setStretchLastSection(True)
        self.table_class.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # layout.addWidget(table)
        self.setLayout(layout)

    def get_data_from_db(self, region):
        db = connection_to_database(well_data.DB_CLASSIFICATION)

        well_classification = CheckWellExistence(db)
        data = well_classification.get_data_from_db(region)

        return data

    @staticmethod
    def insert_database(data_base, data_work, query):
        if well_data.connect_in_base:

            # Параметры подключения к PostgreSQL
            try:
                # Создание подключения к базе данных PostgreSQL
                conn = connect_to_database(data_base)
                param = '%s'

            except psycopg2.Error as e:
                QMessageBox.warning(None, 'Ошибка', f'Ошибка подключения к базе данных: {type(e).__name__}\n\n{str(e)}')


        else:
            try:
                db_path = connect_to_db('well_data.db', 'data_base_well')
                # Создание подключения к базе данных SQLite
                conn = sqlite3.connect(db_path)
                query.replace('%s', '?')
                param = '?'


            except sqlite3.Error as e:
                QMessageBox.warning(None, 'Ошибка', f'Ошибка подключения к базе данных {type(e).__name__}\n\n{str(e)}')
        # Выполнение SQL-запроса для получения данных

        cursor = conn.cursor()

        cursor.execute(f"""SELECT * FROM chemistry
                           WHERE well_number={param} AND well_area={param} AND region={param}
                            AND costumer={param} AND contractor={param} AND work_plan={param} AND type_kr={param}
                           """, (data_work[:7]))

        row_exists = cursor.fetchone()

        if row_exists:
            query2 = f'''UPDATE chemistry
            SET today={param}, cement={param}, HCl={param}, HF={param}, NaOH={param}, VT_SKO={param},
                clay={param}, sand={param}, RPK={param}, RPP={param}, RKI={param},
                 ELAN={param},ASPO={param}, RIR_2C={param}, RIR_OVP={param}, gidrofabizator={param}, 
                 norm_time={param}, fluid={param}
            WHERE well_number={param} AND well_area={param} AND region={param} AND
                costumer={param} AND contractor={param} AND work_plan={param} AND type_kr={param}'''
            data_work2 = data_work[7:] + data_work[:7]

            cursor.execute(query2, data_work2)

        else:
            cursor.execute(query, data_work)

        # Сохранение изменений
        conn.commit()

        # Закрыть курсор и соединение
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def get_data_from_class_well_db(self, region):
        db = connection_to_database(well_data.DB_CLASSIFICATION)

        well_classification = CheckWellExistence(db)
        data = well_classification.get_data_from_class_well_db(region)

        return data

    def export_to_sqlite_without_juming(self, fname, costumer, region):
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
                    elif 'ишимбай' in str(value).lower():
                        check_param = 'ИГМ'
                    elif 'чекмагуш' in str(value).lower():
                        check_param = 'ЧГМ'
                    elif 'красно' in str(value).lower():
                        check_param = 'КГМ'
                    elif 'арлан' in str(value).lower():
                        check_param = 'АГМ'
                    if '01.01.' in str(value) or '01.04.' in str(value) or '01.07.' in str(
                            value) or '01.10.' in str(value):

                        version_year = re.findall(r'[0-9.]', str(value))
                        version_year = ''.join(version_year)
                        if version_year[-1] == '.':
                            version_year = version_year[:-1]
            if index_row > 18:
                break

        if well_data.connect_in_base:
            try:
                # Подключение к базе данных
                db = connection_to_database(well_data.DB_CLASSIFICATION)
                self.classification_well = CheckWellExistence(db)

                REGION_LIST = ['ЧГМ', 'АГМ', 'ТГМ', 'ИГМ', 'КГМ', ]

                for region_name in REGION_LIST:
                    if region_name == region:
                        if check_param in region_name:
                            self.classification_well.create_table_without_juming(region_name)
                            QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
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
                                            self.classification_well.insert_data_in_table_without_juming(
                                                str(well_number), area_well, version_year, region_name, costumer)

                                QMessageBox.information(self, 'данные обновлены', 'Данные обновлены')
                            except Exception as e:
                                QMessageBox.warning(self, 'ОШИБКА', f'Выбран файл с не корректными данными {e}')

                        else:
                            QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                                f'в Данном перечне отсутствую скважины {region_name}')


            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(self, 'Ошибка', 'Ошибка подключения к базе данных')

            except sqlite3.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка',
                                    f'Ошибка подключения к базе данных: /n {type(e).__name__}\n\n{str(e)}')

    def filter(self, filter_text):
        for i in range(1, self.table_class.rowCount() + 1):
            for j in range(0, 1, 2):
                item = self.table_class.item(i, j)
                if item:
                    match = filter_text.lower() not in item.text().lower()
                    self.table_class.setRowHidden(i, match)
                    if not match:
                        break

    def filter_class(self, filter_text):
        for i in range(1, self.table_class.rowCount() + 1):
            for j in range(1, 2):
                item = self.table_class.item(i, j)
                if item:
                    match = filter_text.lower() not in item.text().lower()
                    self.table_class.setRowHidden(i, match)
                    if not match:
                        break

    def filter_class_area(self, filter_text):
        for i in range(1, self.table_class.rowCount() + 1):
            for j in range(2):
                item = self.table_class.item(i, j)
                if item:
                    match = filter_text.lower() not in item.text().lower()
                    self.table_class.setRowHidden(i, match)
                    if not match:
                        break

    def export_to_database_class_well(self, fname, costumer, region):

        REGION_LIST = ['ЧГМ_классификатор', 'АГМ_классификатор', 'ТГМ_классификатор', 'ИГМ_классификатор',
                       'КГМ_классификатор']

        # Загрузка файла Excel
        wb = load_workbook(fname)
        ws = wb.active

        try:
            db = connection_to_database(well_data.DB_CLASSIFICATION)
            self.classification_well = CheckWellExistence(db)

            check_param, well_column, cdng, area_column, oilfield, categoty_pressure, pressure_Gst, \
            date_measurement, pressure_Ppl, categoty_h2s, h2s_pr, h2s_mg_l, h2s_mg_m, categoty_gf, \
            gas_factor, area_row, check_file = self.classification_well.read_excel_file_classification(ws)

            for region_name in REGION_LIST:
                if region in region_name:
                    self.classification_well.create_table_classification(region_name)

                    if check_param in region_name:
                        QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                            f'регион выбрано корректно  {region_name}')

                        try:
                            # Вставка данных в таблицу

                            for index_row, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                                if index_row < area_row and check_file:
                                    for col, value in enumerate(row):
                                        if not value is None and col <= 18:
                                            if '01.01.' in str(value) or '01.04.' in str(value) or '01.07.' in str(
                                                    value) or '01.10.' in str(value):
                                                version_year = re.findall(r'[0-9.]', str(value))
                                                version_year = ''.join(version_year)
                                                if version_year[-1] == '.':
                                                    version_year = version_year[:-1]
                                elif index_row > area_row and check_file:
                                    well_number = row[well_column]
                                    area_well = row[area_column]
                                    oilfield_str = row[oilfield]

                                    for col, value in enumerate(row):
                                        if not value is None and col <= 18:
                                            if '01.01.' in str(value) or '01.04.' in str(value) or '01.07.' in str(
                                                    value) or '01.10.' in str(value):
                                                version_year = re.findall(r'[0-9.]', str(value))
                                                version_year = ''.join(version_year)
                                                if version_year[-1] == '.':
                                                    version_year = version_year[:-1]

                                    if well_number:
                                        self.classification_well.insert_data_in_classification(
                                            region_name, row[cdng], well_number, area_well, oilfield_str,
                                            row[categoty_pressure],
                                            row[pressure_Ppl], row[pressure_Gst], row[date_measurement],
                                            row[categoty_h2s],
                                            row[h2s_pr], row[h2s_mg_l], row[h2s_mg_m], row[categoty_gf],
                                            row[gas_factor],
                                            version_year, region, costumer
                                        )
                        except:
                            QMessageBox.warning(self, 'ОШИБКА', 'Выбран файл с не корректными данными')

                    else:
                        QMessageBox.warning(self, 'ВНИМАНИЕ ОШИБКА',
                                            f'в Данном перечне отсутствую скважины {region_name}')

            QMessageBox.information(self, 'Успешно', 'Классификатор успешно обновлен')

        except (psycopg2.Error, Exception) as e:
            # Выведите сообщение об ошибке
            QMessageBox.warning(self, 'Ошибка', 'Ошибка подключения к базе данных')



def connect_to_db(name_base, folder_base):
    # Получаем текущий каталог приложения
    current_dir = os.path.dirname(__file__)

    # Определяем путь к папке с базой данных
    db_folder = os.path.join(current_dir, folder_base)

    # Формируем полный путь к файлу базы данных
    db_path = os.path.join(db_folder, name_base)

    return db_path





def excel_in_json(self, sheet):
    index_end_copy = 46

    data = {}
    for row_index, row in enumerate(sheet.iter_rows()):
        row_data = []
        if all(cell == None for cell in row[:32]) is False:
            if any([cell.value == "ИТОГО:" for cell in row[:4]]):
                index_end_copy = row_index

                break
            for cell in row[:32]:
                if any([cell.value == "ИТОГО:" for cell in row[:4]]):
                    index_end_copy = row_index

                    break
                row_data = []
                if all(cell == None for cell in row[:32]) is False:
                    if any([cell.value == "ИТОГО:" for cell in row[:4]]):
                        index_end_copy = row_index

                        break
                    for cell in row[:32]:
                        # Получение значения и стилей
                        value = cell.value

                        font = cell.font
                        if font.color:
                            # Преобразуем RGB в строковый формат
                            rgb_string = f"RGB({font.color.rgb})"
                        else:
                            rgb_string = None

                        fill = cell.fill
                        # Преобразуем RGB в строковый формат
                        rgb_string_fill = f"RGB({fill.fgColor.rgb})"

                        borders = cell.border
                        left_border = None
                        right_border = None
                        top_border = None
                        bottom_border = None
                        borders_style_left = None
                        borders_style_right = None
                        borders_style_top = None
                        borders_style_bottom = None
                        if borders.left.style:
                            borders_style_left = borders.left.style
                        if borders.left.color:
                            left_border = f"RGB({borders.left.color.rgb})"
                            if left_border == "RGB(Values must be of type <class 'str'>)":
                                left_border = None
                        else:
                            left_border = None
                        if borders.right.style:
                            borders_style_right = borders.right.style
                        if borders.right.color:
                            right_border = f"RGB({borders.right.color.rgb})"
                            if right_border == "RGB(Values must be of type <class 'str'>)":
                                right_border = None
                        else:
                            right_border = None
                        if borders.top.style:
                            borders_style_top = borders.top.style
                        if borders.top.color:
                            top_border = f"RGB({borders.top.color.rgb})"
                            if top_border == "RGB(Values must be of type <class 'str'>)":
                                top_border = None
                        else:
                            top_border = None

                        if borders.bottom.style:
                            borders_style_bottom = borders.bottom.style
                        if borders.bottom.color:
                            bottom_border = f"RGB({borders.bottom.color.rgb})"
                            if bottom_border == "RGB(Values must be of type <class 'str'>)":
                                bottom_border = None
                        else:
                            bottom_border = None
                        alignment = cell.alignment

                        row_data.append({
                            'value': value,
                            'font': {
                                'name': font.name,
                                'size': font.size,
                                'bold': font.bold,
                                'italic': font.italic,
                                'color': rgb_string
                            },
                            'fill': {
                                'color': rgb_string_fill
                            },
                            'borders': {
                                'left': {
                                    'style': borders_style_left,
                                    'color': left_border
                                },
                                'right': {
                                    'style': borders_style_right,
                                    'color': right_border
                                },
                                'top': {
                                    'style': borders_style_top,
                                    'color': top_border
                                },
                                'bottom': {
                                    'style': borders_style_bottom,
                                    'color': bottom_border
                                },
                            },
                            'alignment': {
                                'horizontal': alignment.horizontal,
                                'vertical': alignment.vertical,
                                'wrap_text': alignment.wrap_text
                            },
                        })
                        data[row[0].row] = row_data

    data['image'] = self.dict_data_well["image_data"]
    rowHeights = [sheet.row_dimensions[i + 1].height for i in range(sheet.max_row) if i <= index_end_copy]
    # rowHeights = [sheet.row_dimensions[i + 1].height for i in range(sheet.max_row)if i <= 46]
    colWidth = [sheet.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 80)] + [None]
    boundaries_dict = {}

    for ind, _range in enumerate(sheet.merged_cells.ranges):
        if range_boundaries(str(_range))[1] <= index_end_copy:
            boundaries_dict[ind] = range_boundaries(str(_range))

    data_excel = {'data': data, 'rowHeights': rowHeights, 'colWidth': colWidth, 'merged_cells': boundaries_dict}

    return data_excel


def insert_data_well_dop_plan(self, data_well):
    from well_data import ProtectedIsDigit, ProtectedIsNonNone

    well_data_dict = json.loads(data_well)

    self.dict_data_well["column_direction_diametr"] = ProtectedIsDigit(well_data_dict["направление"]["диаметр"])
    self.dict_data_well["column_direction_wall_thickness"] = ProtectedIsDigit(well_data_dict["направление"]["толщина стенки"])
    self.dict_data_well["column_direction_lenght"] = ProtectedIsDigit(well_data_dict["направление"]["башмак"])
    self.dict_data_well["level_cement_direction"] = ProtectedIsDigit(well_data_dict["направление"]["цемент"])
    self.dict_data_well["column_conductor_diametr"] = ProtectedIsDigit(well_data_dict["кондуктор"]["диаметр"])
    well_data.column_conductor_wall_thicknes = ProtectedIsDigit(well_data_dict["кондуктор"]["толщина стенки"])
    self.dict_data_well["column_conductor_lenght"] = ProtectedIsDigit(well_data_dict["кондуктор"]["башмак"])
    self.dict_data_well["level_cement_conductor"] = ProtectedIsDigit(well_data_dict["кондуктор"]["цемент"])
    self.dict_data_well["column_diametr"] = ProtectedIsDigit(well_data_dict["ЭК"]["диаметр"])
    self.dict_data_well["column_wall_thickness"] = ProtectedIsDigit(well_data_dict["ЭК"]["толщина стенки"])
    self.dict_data_well["shoe_column"] = ProtectedIsDigit(well_data_dict["ЭК"]["башмак"])
    self.dict_data_well["column_additional"] = well_data_dict["допколонна"]["наличие"]
    self.dict_data_well["column_additional_diametr"] = ProtectedIsDigit(well_data_dict["допколонна"]["диаметр"])
    self.dict_data_well["column_additional_wall_thickness"] = ProtectedIsDigit(well_data_dict["допколонна"]["толщина стенки"])
    self.dict_data_well["shoe_column_additional"] = ProtectedIsDigit(well_data_dict["допколонна"]["башмак"])
    self.dict_data_well["head_column_additional"] = ProtectedIsDigit(well_data_dict["допколонна"]["голова"])
    self.dict_data_well["curator"] = well_data_dict["куратор"]
    self.dict_data_well["dict_pump_SHGN"] = well_data_dict["оборудование"]["ШГН"]["тип"]
    self.dict_data_well["dict_pump_SHGN_h"] = well_data_dict["оборудование"]["ШГН"]["глубина "]
    self.dict_data_well["dict_pump_ECN"] = well_data_dict["оборудование"]["ЭЦН"]["тип"]
    self.dict_data_well["dict_pump_ECN_h"] = well_data_dict["оборудование"]["ЭЦН"]["глубина "]
    self.dict_data_well["paker_do"] = well_data_dict["оборудование"]["пакер"]["тип"]
    self.dict_data_well["depth_fond_paker_do"] = well_data_dict["оборудование"]["пакер"]["глубина "]
    self.dict_data_well["paker2_do"] = well_data_dict["оборудование"]["пакер2"]["тип"]
    self.dict_data_well["depth_fond_paker2_do"] = well_data_dict["оборудование"]["пакер2"]["глубина "]
    self.dict_data_well["static_level"] = ProtectedIsDigit(well_data_dict["статика"])
    self.dict_data_well["dinamic_level"] = ProtectedIsDigit(well_data_dict["динамика"])
    try:
        self.dict_data_well["dict_nkt_po"] = well_data_dict["НКТ"]['После']
        self.dict_data_well["dict_nkt"] = well_data_dict["НКТ"]['До']
        self.dict_data_well["dict_sucker_rod_po"] = well_data_dict["штанги"]['После']
        self.dict_data_well["dict_sucker_rod"] = well_data_dict["штанги"]['До']
    except:
        self.dict_data_well["dict_nkt_po"] = well_data_dict["НКТ"]
        self.dict_data_well["dict_nkt"] = well_data_dict["НКТ"]
        self.dict_data_well["dict_sucker_rod_po"] = well_data_dict["штанги"]
        self.dict_data_well["dict_sucker_rod"] = well_data_dict["штанги"]
    self.dict_data_well["Qoil"] = well_data_dict['ожидаемые']['нефть']
    self.dict_data_well["Qwater"] = well_data_dict['ожидаемые']['вода']
    self.dict_data_well["proc_water"] = well_data_dict['ожидаемые']['обводненность']
    self.dict_data_well["expected_P"] = well_data_dict['ожидаемые']['давление']
    self.dict_data_well["expected_Q"] = well_data_dict['ожидаемые']['приемистость']

    self.dict_data_well["bottomhole_drill"] = ProtectedIsDigit(well_data_dict['данные']['пробуренный забой'])
    self.dict_data_well["bottomhole_artificial"] = ProtectedIsDigit(well_data_dict['данные']['искусственный забой'])
    self.dict_data_well["max_angle"] = ProtectedIsDigit(well_data_dict['данные']['максимальный угол'])
    self.dict_data_well["max_angle_H"] = ProtectedIsDigit(well_data_dict['данные']['глубина'])
    self.dict_data_well["max_expected_pressure"] = ProtectedIsDigit(well_data_dict['данные']['максимальное ожидаемое давление'])
    self.dict_data_well["max_admissible_pressure"] = ProtectedIsDigit(well_data_dict['данные']['максимальное допустимое давление'])

    self.dict_data_well["curator"] = well_data_dict['куратор']
    self.dict_data_well["region"] = well_data_dict['регион']
    self.dict_data_well["cdng"] = ProtectedIsNonNone(well_data_dict['ЦДНГ'])

    self.dict_data_well["data_well_dict"] = well_data_dict
    # QMessageBox.information(None, 'Данные с базы', "Данные вставлены из базы данных")

    # definition_plast_work(self)



def round_cell(data):
    try:
        if data is None or type(data) is datetime:
            return data
        float_item = float(data)
        if float_item.is_integer():
            return int(float_item)
        else:
            return round(float_item, 4)
    except ValueError:
        return data


def insert_data_new_excel_file(self, data, rowHeights, colWidth, boundaries_dict):
    wb_new = openpyxl.Workbook()
    sheet_new = wb_new.active

    for row_index, row_data in data.items():
        if row_index != 'image':
            for col_index, cell_data in enumerate(row_data, 1):
                cell = sheet_new.cell(row=int(row_index), column=int(col_index))
                if cell_data:
                    cell.value = round_cell(cell_data['value'])

    row_max = sheet_new.max_row

    for key, value in boundaries_dict.items():
        if value[1] <= row_max:
            sheet_new.merge_cells(start_column=value[0], start_row=value[1],
                                  end_column=value[2], end_row=value[3])

    # Восстановление данных и стилей из словаря
    for row_index, row_data in data.items():
        if row_index != 'image':
            for col_index, cell_data in enumerate(row_data, 1):
                cell = sheet_new.cell(row=int(row_index), column=int(col_index))

                # Получение строки RGB из JSON
                rgb_string = cell_data['fill']['color']
                if 'color' in list(cell_data['font'].keys()):

                    color_font = change_rgb_to_hex(rgb_string)

                    cell.font = Font(name=cell_data['font']['name'], size=cell_data['font']['size'],
                                     bold=cell_data['font']['bold'], italic=cell_data['font']['italic'],
                                     color=color_font)
                else:
                    # Извлекаем шестнадцатеричный код цвета
                    hex_color = rgb_string[4:-1]

                    if hex_color != '00000000':

                        try:
                            color = Color(rgb=hex_color)

                            # Создание объекта заливки
                            fill = PatternFill(patternType='solid', fgColor=color)
                            cell.fill = fill
                        except:
                            pass
                    cell.font = Font(name=cell_data['font']['name'], size=cell_data['font']['size'],
                                     bold=cell_data['font']['bold'], italic=cell_data['font']['italic'])

                if type(cell_data['borders']['left']) is dict:

                    rgb_string_left = cell_data['borders']['left']['color']

                    color_font_left = change_rgb_to_hex(rgb_string_left)

                    cell.border = openpyxl.styles.Border(
                        left=openpyxl.styles.Side(
                            style=cell_data['borders']['left']['style'],
                            color=color_font_left),
                        right=openpyxl.styles.Side(
                            style=cell_data['borders']['right']['style'],
                            color=change_rgb_to_hex(cell_data['borders']['right']['color'])),
                        top=openpyxl.styles.Side(
                            style=cell_data['borders']['top']['style'],
                            color=change_rgb_to_hex(cell_data['borders']['top']['color'])),
                        bottom=openpyxl.styles.Side(
                            style=cell_data['borders']['bottom']['style'],
                            color=change_rgb_to_hex(cell_data['borders']['bottom']['color'])),
                    )
                else:
                    cell.border = openpyxl.styles.Border(
                        left=openpyxl.styles.Side(style=cell_data['borders']['left']),
                        right=openpyxl.styles.Side(style=cell_data['borders']['right']),
                        top=openpyxl.styles.Side(style=cell_data['borders']['top']),
                        bottom=openpyxl.styles.Side(style=cell_data['borders']['bottom'])
                    )

                wrap_true = cell_data['alignment']['wrap_text']

                cell.alignment = openpyxl.styles.Alignment(horizontal=cell_data['alignment']['horizontal'],
                                                           vertical=cell_data['alignment']['vertical'],
                                                           wrap_text=wrap_true)

    try:
        self.dict_data_well["image_data"] = data['image']
        # Добавьте обработку ошибки, например, пропуск изображения или запись информации об ошибке в лог
    except ValueError as e:
        print(f"Ошибка при вставке изображения: {type(e).__name__}\n\n{str(e)}")

    for col in range(13):
        sheet_new.column_dimensions[get_column_letter(col + 1)].width = colWidth[col]
    index_delete = 47

    for index_row, row in enumerate(sheet_new.iter_rows()):
        # Копирование высоты строки
        if any(['Наименование работ' in str(col.value) for col in row[:13]]) and self.dict_data_well["work_plan"] not in [
            'plan_change']:
            index_delete = index_row + 2
            well_data.gns_ind2 = index_row + 2

        elif any(['ПЛАН РАБОТ' in str(col.value).upper() for col in row[:4]]) and self.dict_data_well["work_plan"] not in [
            'plan_change']:
            sheet_new.cell(row=index_row + 1, column=2).value = f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {self.dict_data_well["number_dp"]}'

        elif any(['ИТОГО:' in str(col.value).upper() for col in row[:4]]) and self.dict_data_well["work_plan"] in ['plan_change']:
            index_delete = index_row + 2
            well_data.gns_ind2 = index_row + 2

        elif all([col is None for col in row[:13]]):
            sheet_new.row_dimensions[index_row].hidden = True
        try:
            sheet_new.row_dimensions[index_row].height = rowHeights[index_row - 1]
        except:
            pass

    if self.dict_data_well["work_plan"] not in ['plan_change']:
        sheet_new.delete_rows(index_delete, sheet_new.max_row - index_delete + 1)

    return sheet_new


def change_rgb_to_hex(rgb_string_font_color):
    if rgb_string_font_color is None or rgb_string_font_color == "RGB(Values must be of type <class 'str'>)":
        rgb_string_font_color = 'RGB(00000000)'

    # Извлекаем шестнадцатеричный код цвета
    hex_color_font = rgb_string_font_color[4:-1]

    color_font = Color(rgb=hex_color_font)
    return color_font


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = Classifier_well()
    window.show()
    sys.exit(app.exec_())
