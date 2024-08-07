
import json
import sqlite3

import well_data
import psycopg2
from openpyxl.styles import Font, Alignment

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton
from PyQt5.QtCore import Qt
from datetime import datetime

from data_base.work_with_base import connect_to_db

from work_py.advanted_file import definition_plast_work


class TabPageDp(QWidget):
    def __init__(self, work_plan, tableWidget, old_index):
        super().__init__()
        self.validator_int = QIntValidator(0, 8000)

        self.tableWidget = tableWidget
        self.old_index = old_index

        self.work_plan = work_plan

        self.well_number_label = QLabel('номер скважины')
        self.well_number_edit = QLineEdit(self)
        self.well_number_edit.setValidator(self.validator_int)

        self.well_area_label = QLabel('площадь скважины')
        self.well_area_edit = QLineEdit(self)

        self.table_name = ''

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.well_number_label, 2, 1)
        self.grid.addWidget(self.well_number_edit, 3, 1)

        self.grid.addWidget(self.well_area_label, 2, 2)
        self.grid.addWidget(self.well_area_edit, 3, 2)

        self.grid.addWidget(self.well_area_label, 2, 3)
        self.grid.addWidget(self.well_area_edit, 3, 3)

        self.well_area_edit.setText(f"{well_data.well_area._value}")
        # self.well_area_edit.textChanged.connect(self.update_well)
        self.well_number_edit.editingFinished.connect(self.update_well)
        # self.change_pvr_combo.currentTextChanged.connect(self.update_change_pvr)
        # self.change_pvr_combo.setCurrentIndex(1)
        # self.change_pvr_combo.setCurrentIndex(0)
        if well_data.work_plan not in ['dop_plan_in_base']:
            self.well_number_edit.setText(f'{well_data.well_number._value}')

        if well_data.data_in_base:
            self.table_in_base_label = QLabel('данные по скважине')
            self.table_in_base_combo = QComboBox()
            self.table_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            self.well_data_label = QLabel('файл excel')
            self.well_data_in_base_combo = QComboBox()
            self.well_data_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            table_list = self.get_tables_starting_with(self.well_number_edit.text(), self.well_area_edit.text())
            if table_list:
                self.table_in_base_combo.clear()
                self.table_in_base_combo.addItems(table_list[::-1])

            self.grid.addWidget(self.table_in_base_label, 2, 5)
            self.grid.addWidget(self.table_in_base_combo, 3, 5)
            self.grid.addWidget(self.well_data_label, 2, 6)
            self.grid.addWidget(self.well_data_in_base_combo, 3, 6)

            self.table_in_base_combo.currentTextChanged.connect(self.update_area)

    def update_area(self):
        table_in_base_combo = self.table_in_base_combo.currentText()
        if len(table_in_base_combo.split(" ")) > 1:
            well_area = table_in_base_combo.split(" ")[1]
            self.well_area_edit.setText(well_area)
            self.well_number_edit.setText(table_in_base_combo.split(" ")[0])

            well_list = self.check_in_database_well_data(self.well_number_edit.text())
            if well_list:
                self.well_data_in_base_combo.clear()
                self.well_data_in_base_combo.addItems(well_list)

    def check_in_database_well_data(self, number_well):
        table_in_base_combo = self.table_in_base_combo.currentText()
        if ' от' in table_in_base_combo:
            table_in_base_combo = table_in_base_combo[:-14]

        if number_well and len(table_in_base_combo.split(" ")) > 3:
            well_number, well_area = table_in_base_combo.split(" ")[:2]
            self.well_number_edit.setText(well_number)
            self.well_area_edit.setText(well_area)

            if well_area != ' ':
                if well_data.connect_in_base:
                    try:
                        conn = psycopg2.connect(**well_data.postgres_params_data_well)
                        cursor = conn.cursor()

                        # Запрос для извлечения всех скважин с наличием данных
                        cursor.execute(
                            "SELECT well_number, area_well, contractor, costumer, today, work_plan FROM wells "
                            "WHERE well_number=(%s) AND area_well=(%s)",
                            (str(number_well), well_area))


                    except psycopg2.Error as e:
                        # Выведите сообщение об ошибке
                        mes = QMessageBox.warning(None, 'Ошибка',
                                                  f'Ошибка подключения к базе данных, Скважина не добавлена в базу: \n {e}')
                else:
                    try:
                        db_path = connect_to_db('well_data.db', 'data_base_well/')

                        conn = sqlite3.connect(f'{db_path}')
                        cursor = conn.cursor()

                        cursor.execute(
                            "SELECT  well_number, area_well, contractor, costumer, today, work_plan FROM wells "
                            "WHERE well_number = ? AND area_well = ? "
                            "AND contractor = ? AND costumer = ?",
                            (str(well_number), well_area, well_data.contractor, well_data.costumer))



                    except sqlite3.Error as e:
                        # Выведите сообщение об ошибке
                        mes = QMessageBox.warning(None, 'Ошибка',
                                                  f'Ошибка подключения к базе данных, Скважина не добавлена в базу: \n {e}')
                # Получение всех результатов
                wells_with_data = cursor.fetchall()
                # Проверка, есть ли данные
                if wells_with_data:
                    well_list = []
                    for well in wells_with_data:
                        try:
                            if 'Ойл' in well[2]:
                                contractor = 'Ойл'
                            elif 'РН' in well[2]:
                                contractor = 'РН'
                        except:
                            contractor = 'Ойл'
                        date_string = well[4]
                        try:
                            # Преобразуем строку в объект datetime
                            datetime_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")

                            # Форматируем объект datetime в нужный формат
                            formatted_date = datetime_object.strftime("%d.%m.%Y")
                        except:
                            formatted_date = well[4]

                        # Формируем список скважин
                        well_list.append(f'{well[0]} {well[1]} {contractor} {well[5]} от {formatted_date}')

                        self.grid.setColumnMinimumWidth(5, self.table_in_base_combo.sizeHint().width())
                        self.grid.setColumnMinimumWidth(6, self.well_data_in_base_combo.sizeHint().width())

                    return well_list[::-1]
                else:
                    return False

    def update_well(self):

        self.table_name = str(self.well_number_edit.text()) + self.well_area_edit.text()
        if well_data.data_in_base:

            table_list = self.get_tables_starting_with(self.well_number_edit.text(), self.well_area_edit.text())

            if table_list:
                table_list = table_list[::-1]
                self.table_in_base_combo.clear()
                self.table_in_base_combo.addItems(table_list)

            well_list = self.check_in_database_well_data(self.well_number_edit.text())
            if well_list:
                self.well_data_in_base_combo.clear()
                self.well_data_in_base_combo.addItems(well_list)

    def update_table_in_base_combo(self):
        from work_py.dop_plan_py import DopPlanWindow

        number_dp = self.number_DP_Combo.currentText()

        table_in_base_combo = self.table_in_base_combo.currentText()
        if ' от' in table_in_base_combo:
            table_in_base_combo = table_in_base_combo[:-14]

        well_number, well_area = table_in_base_combo.split(" ")[:2]
        self.well_number_edit.setText(well_number)
        self.well_area_edit.setText(well_area)
        if number_dp != '':
            well_data.number_dp = int(float(number_dp))

            DopPlanWindow.extraction_data(self, table_in_base_combo, 1)

    def get_tables_starting_with(self, well_number, well_area):
        from data_base.work_with_base import connect_to_db, get_table_creation_time
        """
        Возвращает список таблиц, имена которых начинаются с заданного префикса.
        """
        prefix = well_number
        if 'Ойл' in well_data.contractor:
            contractor = 'ОЙЛ'
        elif 'РН' in well_data.contractor:
            contractor = 'РН'

        if prefix != '':
            if well_data.connect_in_base:
                conn = psycopg2.connect(**well_data.postgres_conn_work_well)
                cursor = conn.cursor()
                cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE %s
                """, (prefix + '%',))
                tables = []

                for row in cursor.fetchall():
                    data_in = get_table_creation_time(conn, row[0])

                    tables.append(row[0] + data_in)
                # tables.insert(0, '')

                cursor.close()

                tables_filter = list(filter(lambda x: contractor in x, tables))
                if len(tables_filter) == 0:
                    tables_filter = tables.insert(0, ' ')
                try:
                    tables_filter = tables_filter[::-1]
                    return tables_filter
                except:
                    return
            else:
                try:
                    # Формируем полный путь к файлу базы данных
                    db_path = connect_to_db('databaseWell.db', 'data_base_well')
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")

                    tables = []
                    table_in_base = cursor.fetchall()[1:]

                    for table_name in table_in_base:
                        if prefix in table_name[0].split(' ')[0]:
                            data_in = get_table_creation_time(conn, table_name[0])
                            tables.append(table_name[0] + data_in)
                    # tables.insert(0, '')

                    # Фильтруем таблицы по префиксу и подрядчику
                    tables_filter = list(filter(lambda x: contractor in x, tables))

                    # Сортируем таблицы в обратном порядке
                    tables_filter = tables_filter[::-1]

                    return tables_filter

                except sqlite3.Error as e:
                    print(f"Ошибка получения списка таблиц: {e}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
        else:
            return []


class TabWidget(QTabWidget):
    def __init__(self, work_plan, tableWidget=0, old_index=0):
        super().__init__()
        self.addTab(TabPageDp(work_plan, tableWidget, old_index), 'Корректировка плана работ')


class CorrectPlanWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, ws=None, parent=None):

        super(CorrectPlanWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.work_plan = work_plan
        self.dict_perforation = []

        self.ws = ws
        self.data, self.rowHeights, self.colWidth, self.boundaries_dict = None, None, None, None
        self.target_row_index = None
        self.target_row_index_cancel = None
        self.old_index = 0

        self.tabWidget = TabWidget(self.work_plan)

        self.buttonadd_work = QPushButton('Загрузить план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)

        vbox.addWidget(self.buttonadd_work, 3, 0, 1, 2)

    def read_excel_in_base(self, number_well, area_well, work_plan):
        if well_data.connect_in_base:
            conn = psycopg2.connect(**well_data.postgres_params_data_well)
            cursor = conn.cursor()

            cursor.execute("SELECT excel_json FROM wells WHERE well_number = %s AND area_well = %s "
                           "AND contractor = %s AND costumer = %s AND work_plan = %s",
                           (str(number_well), area_well, well_data.contractor, well_data.costumer, work_plan))

            data_well = cursor.fetchall()

            if cursor:
                cursor.close()
            if conn:
                conn.close()

        else:
            db_path = connect_to_db('well_data.db', 'data_base_well/')

            conn = sqlite3.connect(f'{db_path}')
            cursor = conn.cursor()

            cursor.execute("SELECT excel_json FROM wells WHERE well_number = ? AND area_well = ? "
                           "AND contractor = ? AND costumer = ?",
                           (str(number_well), area_well, well_data.contractor, well_data.costumer))
            data_well = cursor.fetchall()
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        try:
            dict_well = json.loads(data_well[len(data_well) - 1][0])
            data = dict_well['data']
            rowHeights = dict_well['rowHeights']
            colWidth = dict_well['colWidth']
            boundaries_dict = dict_well['merged_cells']

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Введены не все параметры {e}')
            return

        return data, rowHeights, colWidth, boundaries_dict

    def add_work(self):
        from data_base.work_with_base import check_in_database_well_data, insert_data_well_dop_plan, round_cell
        from work_py.dop_plan_py import DopPlanWindow

        from well_data import ProtectedIsNonNone
        from main import MyWindow

        well_number = self.tabWidget.currentWidget().well_number_edit.text()
        well_area = self.tabWidget.currentWidget().well_area_edit.text()

        if well_data.data_in_base:
            data_well_data_in_base_combo, data_table_in_base_combo = '', ''
            table_in_base_combo = str(self.tabWidget.currentWidget().table_in_base_combo.currentText())
            well_data_in_base_combo = self.tabWidget.currentWidget().well_data_in_base_combo.currentText()
            if ' от' in table_in_base_combo:
                data_table_in_base_combo = table_in_base_combo.split(' ')[-1]
                table_in_base = table_in_base_combo.split(' ')[2]
                number_dp_in_base = "".join(c for c in table_in_base if c.isdigit())
                table_in_base = table_in_base_combo.split(' ')[2].replace('krs', 'ПР').replace('dop_plan_in_base',
                                                                                               'ДП№').replace(
                    'dop_plan', 'ДП№')

            if ' от' in well_data_in_base_combo:
                data_well_data_in_base_combo = well_data_in_base_combo.split(' ')[-1]
                well_data_in_base = well_data_in_base_combo.split(' ')[3]

            if data_well_data_in_base_combo != data_table_in_base_combo:
                mes = QMessageBox.critical(self, 'пункт', 'Даты в двух таблицах не совпадают')
                return
            if table_in_base != well_data_in_base:
                mes = QMessageBox.critical(self, 'пункт', 'Планы в двух таблицах не совпадают')
                return

            if table_in_base_combo == '':
                mes = QMessageBox.critical(self, 'База данных', 'Необходимо выбрать план работ')
                return
            if well_area != table_in_base_combo.split(' ')[1]:
                mes = QMessageBox.critical(self, 'База данных', 'Площадь не совпадает с базой')
                return

            data_well = check_in_database_well_data(well_number, well_area, table_in_base)[0]

            if data_well:
                insert_data_well_dop_plan(data_well)

            DopPlanWindow.work_with_excel(self, well_number, well_area, table_in_base)

            well_data.data, well_data.rowHeights, well_data.colWidth, well_data.boundaries_dict = \
                DopPlanWindow.change_pvr_in_bottom(self, self.data, self.rowHeights, self.colWidth,
                                                   self.boundaries_dict)

            name_table = table_in_base_combo[:-14]

            self.extraction_data(name_table)
            if well_area != '' and well_area != '':
                well_data.well_number, well_data.well_area = \
                    ProtectedIsNonNone(well_number), ProtectedIsNonNone(well_area)
            well_data.pause = False
            self.close()

    def delete_data(self, number_well, area_well, work_plan):
        if well_data.connect_in_base:
            try:
                conn = psycopg2.connect(**well_data.postgres_params_data_well)
                cursor = conn.cursor()

                cursor.execute("""
                DELETE FROM wells 
                WHERE well_number = %s AND area_well = %s AND contractor = %s AND costumer = %s AND work_plan= %s """,
                               (str(number_well), area_well, well_data.contractor, well_data.costumer, work_plan)
                               )

                conn.commit()
                cursor.close()
                conn.close()

            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                mes = QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка удаления {e}')
        else:
            try:
                db_path = connect_to_db('well_data.db', 'data_base_well/')

                conn = sqlite3.connect(f'{db_path}')
                cursor = conn.cursor()

                cursor.execute("DELETE FROM wells  WHERE well_number = ? AND area_well = ? "
                               "AND contractor = ? AND costumer = ? AND work_plan=?",
                               (str(number_well._value), area_well._value, well_data.contractor, well_data.costumer,
                                work_plan))

                conn.commit()
                cursor.close()
                conn.close()

            except sqlite3.Error as e:
                # Выведите сообщение об ошибке
                mes = QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка удаления {e}')

    def add_work_excel(self, ws2, work_list, ind_ins):
        from well_data import ProtectedIsDigit
        for i in range(1, len(work_list) + 1):  # Добавлением работ
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):

                    if i >= ind_ins:

                        if j != 1:
                            cell.border = well_data.thin_border
                        if j == 11:
                            cell.font = Font(name='Arial', size=11, bold=False)
                        # if j == 12:
                        #     cell.value = work_list[i - 1][j - 1]
                        else:
                            cell.font = Font(name='Arial', size=13, bold=False)
                        ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                        ws2.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')

                        if 'порядок работы' in str(cell.value).lower() or \
                                'наименование работ' in str(cell.value).lower():
                            well_data.ins_ind2 = i + 1
                            well_data.data_x_max = ProtectedIsDigit(i + 2)

                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')

    def extraction_data(self, table_name, paragraph_row=0):
        from data_base.work_with_base import connect_to_db
        from work_py.dop_plan_py import DopPlanWindow

        if 'Ойл' in well_data.contractor:
            contractor = 'ОЙЛ'
        elif 'РН' in well_data.contractor:
            contractor = 'РН'
        if well_data.connect_in_base:
            try:
                # Устанавливаем соединение с базой данных
                conn1 = psycopg2.connect(**well_data.postgres_conn_work_well)

                cursor1 = conn1.cursor()

                # Проверяем наличие таблицы с определенным именем
                result_table = 0

                if well_data.work_plan in ['krs', 'plan_change']:
                    work_plan = 'krs'

                    # print(cursor1.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables").fetchall())
                    cursor1.execute(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
                    result_table = cursor1.fetchone()

                elif well_data.work_plan in ['dop_plan', 'dop_plan_in_base']:

                    cursor1.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables "
                                    f"WHERE table_name = '{table_name}')")
                    print(f'имя таблицы в {table_name}')
                    result_table = cursor1.fetchone()

                if result_table[0]:
                    well_data.data_in_base = True
                    cursor2 = conn1.cursor()

                    cursor2.execute(f'SELECT * FROM "{table_name}"')
                    result = cursor2.fetchall()

                    if well_data.work_plan in ['dop_plan', 'dop_plan_in_base']:
                        DopPlanWindow.insert_data_dop_plan(self, result, paragraph_row)
                    elif well_data.work_plan == 'plan_change':
                        DopPlanWindow.insert_data_plan(self, result)
                    well_data.data_well_is_True = True

                else:
                    well_data.data_in_base = False
                    mes = QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                              f"Таблицы '{table_name}' нет в базе данных.")


            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных,')
            finally:
                # Закройте курсор и соединение
                if cursor1:
                    cursor1.close()
                if conn1:
                    conn1.close()
        else:
            try:


                # Формируем полный путь к файлу базы данных
                db_path = connect_to_db('databaseWell.db', 'data_base_well')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                result_table = 0

                if well_data.work_plan in ['krs', 'plan_change']:
                    work_plan = 'krs'
                    table_name = f'{str(well_data.well_number._value) + " " + well_data.well_area._value + " " + work_plan + " " + contractor}'

                    cursor.execute(
                        f"SELECT name FROM sqlite_master WHERE type='table' AND name=? ",
                        (table_name,))
                    result_table = cursor.fetchone()

                elif well_data.work_plan in ['dop_plan', 'dop_plan_in_base']:
                    cursor.execute(
                        f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                        (table_name,))
                    result_table = cursor.fetchone()

                if result_table:
                    well_data.data_in_base = True
                    cursor2 = conn.cursor()

                    cursor2.execute(f'SELECT * FROM "{table_name}"')
                    result = cursor2.fetchall()

                    if well_data.work_plan in ['dop_plan', 'dop_plan_in_base']:
                        DopPlanWindow.insert_data_dop_plan(self, result, paragraph_row)
                    elif well_data.work_plan == 'plan_change':
                        DopPlanWindow.insert_data_plan(self, result)
                    well_data.data_well_is_True = True

                else:
                    well_data.data_in_base = False
                    mes = QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                              f"Таблицы '{table_name}' нет в базе данных.")

            except sqlite3.Error as e:
                # Выведите сообщение об ошибке
                mes = QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных.')

            finally:
                # Закройте курсор и соединение
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        definition_plast_work(self)
        return

    def insert_data_dop_plan(self, result, paragraph_row):
        try:
            paragraph_row = paragraph_row - 1
        except:
            paragraph_row = 1
        if len(result) < paragraph_row:
            mes = QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пункта')
            return

        well_data.current_bottom = result[paragraph_row][1]

        well_data.dict_perforation = json.loads(result[paragraph_row][2])
        well_data.plast_all = json.loads(result[paragraph_row][3])
        well_data.plast_work = json.loads(result[paragraph_row][4])
        well_data.leakage = json.loads(result[paragraph_row][5])
        if result[paragraph_row][6] == 'true':
            well_data.column_additional = True
        else:
            well_data.column_additional = False

        well_data.fluid_work = result[paragraph_row][7]

        well_data.category_pressuar = result[paragraph_row][8]
        well_data.category_h2s = result[paragraph_row][9]
        well_data.category_gf = result[paragraph_row][10]
        try:
            well_data.template_depth, well_data.template_lenght, well_data.template_depth_addition, \
            well_data.template_lenght_addition = json.loads(result[paragraph_row][11])
        except:
            well_data.template_depth = result[paragraph_row][11]
        well_data.skm_interval = json.loads(result[paragraph_row][12])
        well_data.problemWithEk_depth = result[paragraph_row][13]
        well_data.problemWithEk_diametr = result[paragraph_row][14]
        well_data.dict_perforation_short = json.loads(result[paragraph_row][2])

    def insert_data_plan(self, result):
        well_data.data_list = []
        for row in result:
            data_list = []
            for index, data in enumerate(row[:-1]):
                if index == 6:
                    if data == 'false' or data == 0 or data == '0':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            well_data.data_list.append(data_list)

    def work_list(self, work_earlier):
        krs_begin = [[None, None,
                      f' Ранее проведенные работ: \n {work_earlier}',
                      None, None, None, None, None, None, None,
                      'Мастер КРС', None]]

        return krs_begin
