import json
import sqlite3
import time

from openpyxl.styles import Font, Alignment

import well_data
import psycopg2

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from datetime import datetime
from krs import TabPageGno, GnoWindow

from work_py.alone_oreration import lifting_unit, weigth_pipe, volume_pod_NKT, pvo_gno, volume_jamming_well
from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import liftingNKT_norm


class TabPageDp(QWidget):
    def __init__(self, work_plan):
        super().__init__()

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)
        self.work_plan = work_plan

        self.well_number_label = QLabel('номер скважины')
        self.well_number_edit = QLineEdit(self)
        self.well_number_edit.setText(f'{well_data.well_number._value}')

        self.well_area_label = QLabel('площадь скважины')
        self.well_area_edit = QLineEdit(self)
        self.well_area_edit.setText(f"{well_data.well_area._value}")

        self.number_DP_label = QLabel('номер дополнительного плана')
        self.number_DP_Combo = QComboBox(self)

        self.number_DP_Combo.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        if well_data.number_dp != 0:
            self.number_DP_Combo.setCurrentIndex(int(well_data.number_dp) - 1)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setValidator(self.validator_float)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.template_depth_label = QLabel('Глубина спуска шаблона')
        self.template_depth_edit = QLineEdit(self)
        self.template_depth_edit.setValidator(self.validator_float)
        self.template_depth_edit.setText(str(well_data.template_depth))

        self.template_lenght_label = QLabel('Длина шаблона')
        self.template_lenght_edit = QLineEdit(self)
        self.template_lenght_edit.setValidator(self.validator_float)

        self.skm_interval_label = QLabel('интервалы скреперования')
        self.skm_interval_edit = QLineEdit(self)

        self.table_name = ''

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        self.fluid_edit.setAlignment(Qt.AlignLeft)
        # if well_data.fluid_work == '':
        #     self.fluid_edit.setText(f'{TabPageGno.calc_fluid(self.work_plan, well_data.current_bottom)}')
        # else:
        #     self.fluid_edit.setText(f'{well_data.fluid_work}')

        self.work_label = QLabel("Ранее проведенные работы:", self)
        self.work_edit = QTextEdit(self)

        # self.work_edit.setFixedWidth(300)
        self.work_edit.setAlignment(Qt.AlignLeft)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.well_number_label, 2, 1)
        self.grid.addWidget(self.well_number_edit, 3, 1)

        self.grid.addWidget(self.well_area_label, 2, 2)
        self.grid.addWidget(self.well_area_edit, 3, 2)

        self.grid.addWidget(self.well_area_label, 2, 3)
        self.grid.addWidget(self.well_area_edit, 3, 3)

        self.grid.addWidget(self.number_DP_label, 2, 4)
        self.grid.addWidget(self.number_DP_Combo, 3, 4)

        self.grid.addWidget(self.current_bottom_label, 4, 1)
        self.grid.addWidget(self.current_bottom_edit, 5, 1)
        self.grid.addWidget(self.fluid_label, 4, 5, 1, 6)
        self.grid.addWidget(self.fluid_edit, 5, 5, 1, 6)
        self.grid.addWidget(self.template_depth_label, 6, 1)
        self.grid.addWidget(self.template_depth_edit, 7, 1)
        self.grid.addWidget(self.template_lenght_label, 6, 2)
        self.grid.addWidget(self.template_lenght_edit, 7, 2)
        self.grid.addWidget(self.skm_interval_label, 8, 1, 1, 3)
        self.grid.addWidget(self.skm_interval_edit, 9, 1, 1, 3)
        self.grid.addWidget(self.work_label, 14, 1)
        self.grid.addWidget(self.work_edit, 15, 1, 2, 4)

        self.well_area_edit.textChanged.connect(self.update_well)
        self.well_number_edit.textChanged.connect(self.update_well)


    def update_well(self):

        self.table_name = str(self.well_number_edit.text()) + self.well_area_edit.text()
        if well_data.data_in_base:
            self.table_in_base_label = QLabel('данные в таблице')
            self.table_in_base_combo = QComboBox()

            table_list = self.get_tables_starting_with(self.well_number_edit.text(), self.well_area_edit.text())
            if table_list:
                self.table_in_base_combo.addItems(table_list)

            self.index_change_label = QLabel('пункт после которого происходят изменения')
            self.index_change_line = QLineEdit(self)
            self.index_change_line.setValidator(self.validator_int)
            self.grid.addWidget(self.table_in_base_label, 2, 5)
            self.grid.addWidget(self.table_in_base_combo, 3, 5)
            self.grid.addWidget(self.index_change_label, 2, 7)
            self.grid.addWidget(self.index_change_line, 3, 7)

            self.index_change_line.textChanged.connect(self.update_table_in_base_combo)
            self.table_in_base_combo.currentTextChanged.connect(self.update_table_in_base_combo)

    def update_table_name(self):
        self.index_change_line.setText('0')
    def update_table_in_base_combo(self):
        time.sleep(0.1)
        index_change_line = self.index_change_line.text()
        table_in_base_combo = self.table_in_base_combo.currentText()
        number_dp = self.number_DP_Combo.currentText()
        well_number, well_area = table_in_base_combo.split(" ")[:2]
        self.well_number_edit.setText(well_number)
        self.well_area_edit.setText(well_area)
        if number_dp != '':
            well_data.number_dp = int(float(number_dp))

        if index_change_line != '':
            index_change_line = int(float(index_change_line))
            DopPlanWindow.extraction_data(self, table_in_base_combo, index_change_line)

            self.template_depth_edit.setText(str(well_data.template_depth))
            self.template_lenght_edit.setText(str(well_data.template_lenght))
            skm_interval = ''
            a = well_data.skm_interval
            if len(well_data.skm_interval) != 0:
                for roof, sole in well_data.skm_interval:
                    skm_interval += f'{roof}-{sole}, '

            self.skm_interval_edit.setText(skm_interval[:-2])
            self.current_bottom_edit.setText(str(well_data.current_bottom))
            self.fluid_edit.setText(str(well_data.fluid_work))
            if well_data.column_additional:
                self.template_depth_addition_label = QLabel('Глубина спуска шаблона в доп колонне')
                self.template_depth_addition_edit = QLineEdit(self)
                self.template_depth_addition_edit.setValidator(self.validator_float)
                self.template_depth_addition_edit.setText(str(well_data.template_depth_addition))

                self.template_lenght_addition_label = QLabel('Длина шаблона в доп колонне')
                self.template_lenght_addition_edit = QLineEdit(self)
                self.template_lenght_addition_edit.setValidator(self.validator_float)
                self.template_lenght_addition_edit.setText(str(well_data.template_lenght_addition))
                self.grid.addWidget(self.template_depth_addition_label, 6, 4)
                self.grid.addWidget(self.template_depth_addition_edit, 7, 4)
                self.grid.addWidget(self.template_lenght_addition_label, 6, 5)
                self.grid.addWidget(self.template_lenght_addition_edit, 7, 5)



    def get_tables_starting_with(self, well_number, well_area):
        """
        Возвращает список таблиц, имена которых начинаются с заданного префикса.
        """
        prefix = well_number
        if 'Ойл' in well_data.contractor:
            contractor = 'ОЙЛ'
        elif 'РН' in well_data.contractor:
            contractor = 'РН'
        if well_data.connect_in_base:
            conn = psycopg2.connect(**well_data.postgres_conn_work_well)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name LIKE %s
            """, (prefix + '%',))

            tables = [row[0] for row in cursor.fetchall()]
            tables.insert(0, '')

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
                conn = sqlite3.connect('data_base/data_base_well/databaseWell.db')
                cursor = conn.cursor()

                # Получаем все имена таблиц в базе данных
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                tables.insert(0, '')

                # Фильтруем таблицы по префиксу и подрядчику
                tables_filter = list(filter(lambda x: contractor in x, tables))

                # Добавляем пустую строку в начало списка
                tables_filter.insert(0, '')

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


class TabWidget(QTabWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.addTab(TabPageDp(work_plan), 'Дополнительный план работ')


class DopPlanWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, ws = None, parent=None):

        super(DopPlanWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.work_plan = work_plan
        self.tabWidget = TabWidget(self.work_plan)
        self.ws = ws

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from data_base.work_with_base import check_in_database_well_data, insert_data_well_dop_plan, round_cell
        from well_data import ProtectedIsNonNone
        from main import MyWindow
        fluid = self.tabWidget.currentWidget().fluid_edit.text()
        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round_cell(current_bottom.replace(',', '.'))

        work_earlier = self.tabWidget.currentWidget().work_edit.toPlainText()
        number_dp = self.tabWidget.currentWidget().number_DP_Combo.currentText()

        template_depth_edit = self.tabWidget.currentWidget().template_depth_edit.text()
        template_lenght_edit = self.tabWidget.currentWidget().template_lenght_edit.text()
        if well_data.column_additional:
            template_depth_addition_edit = self.tabWidget.currentWidget().template_depth_addition_edit.text()
            template_lenght_addition_edit = self.tabWidget.currentWidget().template_lenght_addition_edit.text()
        skm_interval_edit = self.tabWidget.currentWidget().skm_interval_edit.text()

        if current_bottom == '' or fluid == '' or work_earlier == '' or \
                template_depth_edit == '' or template_lenght_edit == '' or skm_interval_edit == '':
            # print(current_bottom, fluid, work_earlier)
            mes = QMessageBox.critical(self, 'Забой', 'не все значения введены')
            return
        if template_lenght_edit == '0':
            mes = QMessageBox.critical(self, 'Длина шаблона', 'Введите длину шаблонов которые были спущены в скважину')
            return
        if float(template_depth_edit) > float(current_bottom):
            mes = QMessageBox.critical(self, 'Забой', 'Шаблонирование не может быть ниже текущего забоя')
            return
        if number_dp != '':
            well_data.number_dp = int(float(number_dp))

        if well_data.data_in_base:

            table_in_base_combo = str(self.tabWidget.currentWidget().table_in_base_combo.currentText())
            index_change_line = self.tabWidget.currentWidget().index_change_line.text()
            well_number = self.tabWidget.currentWidget().well_number_edit.text()
            well_area = self.tabWidget.currentWidget().well_area_edit.text()
            if well_area != '' and well_area != '':
                well_data.well_number, well_data.well_area = \
                    ProtectedIsNonNone(well_number), ProtectedIsNonNone(well_area)
            if index_change_line != '':
                index_change_line = int(float(index_change_line))
            else:
                mes = QMessageBox.critical(self, 'пункт', 'Необходимо выбрать пункт плана работ')
                return
            if table_in_base_combo == '':
                mes = QMessageBox.critical(self, 'База данных', 'Необходимо выбрать план работ')
                return
            data_well = check_in_database_well_data(well_data.well_number, well_data.well_area)[0]
            if data_well:
                insert_data_well_dop_plan(data_well)
            self.extraction_data(table_in_base_combo, index_change_line)

        if (0.87 <= float(fluid[:3].replace(',', '.')) <= 1.64) == False:
            mes = QMessageBox.critical(self, 'рабочая жидкость',
                                       'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
            return
        if well_data.data_in_base:
            if 'г/см3' not in fluid:
                mes = QMessageBox.critical(self, 'уд.вес', 'нужно добавить значение "г/см3" в уд.вес')
                return
            well_data.fluid_work = fluid
            well_data.fluid_work_short = fluid[:7]
            well_data.current_bottom = current_bottom
            well_data.fluid = fluid[:4]
        else:

            if float(current_bottom) > well_data.bottomhole_drill._value:
                mes = QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
                return
            well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(self, fluid)

        well_data.template_depth = float(template_depth_edit)
        well_data.template_lenght = float(template_lenght_edit)
        if well_data.column_additional:

            well_data.template_depth = float(template_depth_addition_edit)
            well_data.template_lenght = float(template_lenght_addition_edit)


        try:
            skm_interval = []
            if ',' in skm_interval_edit:
                for skm in skm_interval_edit.split(','):
                    if '-' in skm:
                       skm_interval.append(skm)
            else:
                if '-' in skm_interval_edit:
                    skm_interval.append(skm_interval_edit)


            well_data.skm_interval = skm_interval
        except:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'в интервале скреперования отсутствует корректные интервалы скреперования')

        if len(well_data.skm_interval) == 0:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'в интервале скреперования отсутствует корректные интервалы скреперования')
            return

        if well_data.data_in_base:
            well_data.dop_work_list = self.work_list(work_earlier)
        else:
            work_list = [self.work_list(work_earlier)]
            MyWindow.populate_row(self, self.ins_ind + 2, work_list, self.table_widget, self.work_plan)

        well_data.pause = False
        self.close()


    def add_work_excel(self, ws2, work_list, ind_ins):
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
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')

    def extraction_data(self, table_name, paragraph_row):
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

                a = well_data.work_plan
                if well_data.work_plan in ['krs', 'plan_change']:
                    work_plan = 'krs'

                    table_name = f'{str(well_data.well_number._value) + " " + well_data.well_area._value + " " + work_plan + " " + contractor}'

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
                mes = QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных,')
            finally:
                # Закройте курсор и соединение
                if cursor1:
                    cursor1.close()
                if conn1:
                    conn1.close()
        else:
            try:
                conn = sqlite3.connect('data_base/data_base_well/databaseWell.db')
                cursor = conn.cursor()

                result_table = 0

                if well_data.work_plan in ['krs', 'plan_change']:
                    work_plan = 'krs'
                    table_name = f'{str(well_data.well_number._value) + " " + well_data.well_area._value + " " + work_plan + " " + contractor}'
                    cursor.execute(
                        f"SELECT name FROM sqlite_master WHERE type='table' AND name=?",
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

        return

    def insert_data_dop_plan(self, result, paragraph_row):
        try:
            paragraph_row = paragraph_row
        except:
            paragraph_row = 1
        if len(result) < paragraph_row:
            mes = QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пункта')
            return
        a = result[paragraph_row][6]
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
            well_data.template_depth, well_data.template_lenght, well_data.template_depth_addition, well_data.template_lenght_addition = json.loads(result[paragraph_row][11])
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
            for index, data in enumerate(row):
                if index == 6:
                    if data == 'false':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            well_data.data_list.append(data_list)

    def work_list(self, work_earlier):
        krs_begin = [None, None,
                      f' Ранее проведенные работ: \n {work_earlier}',
                      None, None, None, None, None, None, None,
                      'Мастер КРС', None]

        return krs_begin
