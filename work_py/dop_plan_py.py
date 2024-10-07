import json
import sqlite3

from openpyxl.styles import Font, Alignment

import well_data
import psycopg2
from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QPushButton, QTextEdit, QDateEdit
from PyQt5.QtCore import Qt
from datetime import datetime

from data_base.work_with_base import connect_to_db
from krs import GnoWindow
from main import MyMainWindow
from work_py.advanted_file import merge_overlapping_intervals, definition_plast_work


class TabPageDp(QWidget):
    def __init__(self, work_plan, tableWidget, old_index):
        super().__init__()

        self.tableWidget = tableWidget
        self.old_index = old_index

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)
        self.work_plan = work_plan

        self.well_number_label = QLabel('номер скважины')
        self.well_number_edit = QLineEdit(self)
        # self.well_number_edit.setValidator(self.validator_int)

        self.well_area_label = QLabel('площадь скважины')
        self.well_area_edit = QLineEdit(self)

        self.number_DP_label = QLabel('номер \nдополнительного плана')
        self.number_DP_Combo = QComboBox(self)

        self.number_DP_Combo.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        if well_data.number_dp != 0:
            self.number_DP_Combo.setCurrentIndex(int(well_data.number_dp) - 1)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setValidator(self.validator_float)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.current_bottom_date_label = QLabel('дата определения забоя')
        self.current_bottom_date_edit = QDateEdit(self)
        self.current_bottom_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.current_bottom_date_edit.setDate(datetime.now())

        self.method_bottom_label = QLabel('Метод определения \nзабоя')
        self.method_bottom_combo = QComboBox(self)
        self.method_bottom_combo.addItems(['', 'ГИС', 'НКТ'])

        self.template_depth_label = QLabel('Глубина \nшаблонирования ЭК')
        self.template_depth_edit = QLineEdit(self)
        self.template_depth_edit.setValidator(self.validator_float)
        self.template_depth_edit.setText(str(well_data.template_depth))

        self.template_lenght_label = QLabel('Длина шаблона')
        self.template_lenght_edit = QLineEdit(self)
        self.template_lenght_edit.setValidator(self.validator_float)

        self.change_pvr_combo_label = QLabel('Были ли изменения \nв интервале перфорации')
        self.change_pvr_combo = QComboBox(self)
        self.change_pvr_combo.addItems(['', 'Нет', 'Да'])

        self.skm_interval_label = QLabel('интервалы \nскреперования')
        self.skm_interval_edit = QLineEdit(self)

        self.table_name = ''

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        self.fluid_edit.setAlignment(Qt.AlignLeft)

        self.plast_label = QLabel("пласта")
        self.plast_line = QLineEdit(self)
        self.vertical_label = QLabel("по вертикале")
        self.vertical_line = QLineEdit(self)
        self.roof_label = QLabel("Кровля")
        self.roof_edit = QLineEdit(self)
        self.sole_label = QLabel("Подошва")
        self.sole_edit = QLineEdit(self)
        self.date_pvr_label = QLabel("Дата")
        self.date_pvr_edit = QDateEdit(self)
        self.date_pvr_edit.setDisplayFormat("dd.MM.yyyy")
        self.count_pvr_label = QLabel("Кол-во отв")
        self.count_pvr_edit = QLineEdit(self)
        self.type_pvr_label = QLabel("Тип перфоратора")
        self.type_pvr_edit = QLineEdit(self)
        self.pressuar_pvr_label = QLabel("Давление")
        self.pressuar_pvr_edit = QLineEdit(self)
        self.date_pressuar_label = QLabel("Дата замера")
        self.date_pressuar_edit = QDateEdit(self)
        self.date_pressuar_edit.setDisplayFormat("dd.MM.yyyy")

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
        self.grid.addWidget(self.current_bottom_date_label, 4, 2)
        self.grid.addWidget(self.current_bottom_date_edit, 5, 2)
        self.grid.addWidget(self.method_bottom_label, 4, 3)
        self.grid.addWidget(self.method_bottom_combo, 5, 3)

        self.grid.addWidget(self.fluid_label, 4, 4, 1, 6)
        self.grid.addWidget(self.fluid_edit, 5, 4, 1, 6)
        self.grid.addWidget(self.template_depth_label, 6, 1)
        self.grid.addWidget(self.template_depth_edit, 7, 1)
        self.grid.addWidget(self.template_lenght_label, 6, 2)
        self.grid.addWidget(self.template_lenght_edit, 7, 2)
        self.grid.addWidget(self.skm_interval_label, 8, 1, 1, 3)
        self.grid.addWidget(self.skm_interval_edit, 9, 1, 1, 3)
        self.grid.addWidget(self.change_pvr_combo_label, 10, 1)
        self.grid.addWidget(self.change_pvr_combo, 11, 1)

        self.grid.addWidget(self.work_label, 25, 1)
        self.grid.addWidget(self.work_edit, 26, 1, 2, 4)
        self.well_area_edit.setText(f"{well_data.well_area._value}")
        self.well_number_edit.editingFinished.connect(self.update_well)
        self.well_number_edit.setText(f"{well_data.well_number._value}")

        # self.well_area_edit.textChanged.connect(self.update_well)

        self.change_pvr_combo.currentTextChanged.connect(self.update_change_pvr)
        self.change_pvr_combo.setCurrentIndex(1)
        self.change_pvr_combo.setCurrentIndex(0)


        if well_data.data_in_base:

            # self.table_in_base_label = QLabel('данные по скважине')
            # self.table_in_base_combo = QComboBox()
            # self.table_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            self.well_data_label = QLabel('файл excel сохранный в базе')
            self.well_data_in_base_combo = QComboBox()
            self.well_data_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            self.index_change_label = QLabel('пункт после которого происходят изменения')
            self.index_change_line = QLineEdit(self)
            self.index_change_line.setValidator(self.validator_int)

            self.grid.addWidget(self.well_data_label, 2, 6)
            self.grid.addWidget(self.well_data_in_base_combo, 3, 6)
            self.grid.addWidget(self.index_change_label, 2, 7)
            self.grid.addWidget(self.index_change_line, 3, 7)




            self.index_change_line.editingFinished.connect(self.update_table_in_base_combo)


    def check_in_database_well_data(self, number_well):

        if well_data.connect_in_base:
            try:
                conn = psycopg2.connect(**well_data.postgres_params_data_well)
                cursor = conn.cursor()
                param = '%s'


            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка подключения к базе данных, Скважина не '
                                          f'добавлена в базу: \n {type(e).__name__}\n\n{str(e)}')
        else:
            try:
                db_path = connect_to_db('well_data.db', 'data_base_well/')

                conn = sqlite3.connect(f'{db_path}')
                cursor = conn.cursor()
                param = '?'



            except sqlite3.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка подключения к базе данных, Скважина не '
                                          f'добавлена в базу: \n {type(e).__name__}\n\n{str(e)}')

        # Запрос для извлечения всех скважин с наличием данных
        cursor.execute(
            f"SELECT well_number, area_well, type_kr, today, work_plan FROM wells "
            f"WHERE well_number={param} AND contractor={param} AND costumer ={param}",
            (str(number_well), well_data.contractor, well_data.costumer))

        # Получение всех результатов
        wells_with_data = cursor.fetchall()
        # Проверка, есть ли данные
        if wells_with_data:
            well_list = []
            for well in wells_with_data:

                date_string = well[3]
                try:
                    # Преобразуем строку в объект datetime
                    datetime_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")

                    # Форматируем объект datetime в нужный формат
                    formatted_date = datetime_object.strftime("%d.%m.%Y")
                except:
                    formatted_date = well[3]

                # Формируем список скважин
                well_list.append(f'{well[0]} {well[1]} {well[2]} {well[4]} от {formatted_date}')


                self.grid.setColumnMinimumWidth(6, self.well_data_in_base_combo.sizeHint().width())

            return well_list[::-1]
        else:
            return False

    def update_change_pvr(self, index):
        if self.old_index == 0:
            self.tableWidget.setHorizontalHeaderLabels(
                ["Пласт/\nГоризонт", "по вертикали", "кровля,\n м", "подошва, \nм",
                 "Дата\n вскрытия", "Дата \nотключения", "кол-во \nотвер", "Тип \nперф", 'Удлинение,\nм',
                 "Рпл, \nатм", "Дата \nзамера"])
            for i in range(11):
                self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        else:
            self.tableWidget.setHorizontalHeaderLabels(
                ["Пласт/\nГоризонт", "по вертикали", "кровля,\n м", "подошва, \nм",
                 "Дата\n вскрытия\отключения", "кол-во \nотвер", "Тип \nперф", 'Удлинение,\nм',
                 "Рпл, \nатм", "Дата \nзамера"])
            for i in range(10):
                self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        if index == 'Да':
            self.grid.addWidget(self.plast_label, 12, 1)
            self.grid.addWidget(self.plast_line, 13, 1)
            self.grid.addWidget(self.vertical_label, 12, 2)
            self.grid.addWidget(self.vertical_line, 13, 2)
            self.grid.addWidget(self.roof_label, 12, 3)
            self.grid.addWidget(self.roof_edit, 13, 3)
            self.grid.addWidget(self.sole_label, 12, 4)
            self.grid.addWidget(self.sole_edit, 13, 4)
            self.grid.addWidget(self.date_pvr_label, 12, 5)
            self.grid.addWidget(self.date_pvr_edit, 13, 5)
            self.grid.addWidget(self.count_pvr_label, 12, 6)
            self.grid.addWidget(self.count_pvr_edit, 13, 6)
            self.grid.addWidget(self.type_pvr_label, 12, 7)
            self.grid.addWidget(self.type_pvr_edit, 13, 7)
            self.grid.addWidget(self.pressuar_pvr_label, 12, 8)
            self.grid.addWidget(self.pressuar_pvr_edit, 13, 8)
            self.grid.addWidget(self.date_pressuar_label, 12, 9)
            self.grid.addWidget(self.date_pressuar_edit, 13, 9)
            self.tableWidget.show()
        else:
            self.pressuar_pvr_label.setParent(None)

            self.date_pressuar_label.setParent(None)
            self.pressuar_pvr_edit.setParent(None)
            self.date_pressuar_edit.setParent(None)
            self.vertical_line.setParent(None)
            self.plast_label.setParent(None)
            self.plast_line.setParent(None)
            self.vertical_label.setParent(None)

            self.roof_label.setParent(None)
            self.roof_edit.setParent(None)
            self.sole_label.setParent(None)
            self.sole_edit.setParent(None)
            self.date_pvr_label.setParent(None)
            self.date_pvr_edit.setParent(None)
            self.count_pvr_label.setParent(None)
            self.count_pvr_edit.setParent(None)
            self.type_pvr_label.setParent(None)
            self.type_pvr_edit.setParent(None)
            self.tableWidget.hide()

    def update_well(self):

        self.table_name = str(self.well_number_edit.text()) + self.well_area_edit.text()
        if well_data.data_in_base:

            well_list = self.check_in_database_well_data(self.well_number_edit.text())
            if well_list:
                self.well_data_in_base_combo.clear()
                self.well_data_in_base_combo.addItems(well_list)

            self.index_change_line.editingFinished.connect(self.update_table_in_base_combo)


            # self.table_in_base_combo.currentTextChanged.connect(self.update_table_in_base_combo)

    def update_table_name(self):
        self.index_change_line.setText('0')

    def update_table_in_base_combo(self):

        number_dp = self.number_DP_Combo.currentText()
        index_change_line = self.index_change_line.text()
        well_data_in_base_combo = self.well_data_in_base_combo.currentText()
        if ' ' in well_data_in_base_combo:
            well_number, well_area = well_data_in_base_combo.split(" ")[:2]
            # self.well_number_edit.setText(well_number)
            self.well_area_edit.setText(well_area)
        if number_dp != '':
            well_data.number_dp = int(float(number_dp))

        if index_change_line != '':
            index_change_line = int(float(index_change_line))
            DopPlanWindow.extraction_data(self, well_data_in_base_combo, index_change_line)

            self.template_depth_edit.setText(str(well_data.template_depth))
            self.template_lenght_edit.setText(str(well_data.template_lenght))
            skm_interval = ''

            try:
                asd = well_data.skm_interval
                if len(well_data.skm_interval) != 0:
                    for roof, sole in well_data.skm_interval:
                        if f'{roof}-{sole}' not in skm_interval:
                            skm_interval += f'{roof}-{sole}, '
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не получилось сохранить данные скреперования '
                                                    f'{type(e).__name__}\n\n{str(e)}')

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


class TabWidget(QTabWidget):
    def __init__(self, work_plan, tableWidget=0, old_index=0):
        super().__init__()
        self.addTab(TabPageDp(work_plan, tableWidget, old_index), 'Дополнительный план работ')


class DopPlanWindow(MyMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, ws=None, parent=None):

        super(DopPlanWindow, self).__init__()
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
        self.tableWidget = QTableWidget(0, 12)

        self.tabWidget = TabWidget(self.work_plan, self.tableWidget, self.old_index)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить интервалы перфорации в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить интервалы перфорации в таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Создать доп план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddProject = QPushButton('Добавить проектные интервалы перфорации')
        self.buttonAddProject.clicked.connect(self.addPerfProject)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddProject, 3, 1)

    def add_row_table(self):
        current_widget = self.tabWidget.currentWidget()

        plast_line = current_widget.plast_line.text()
        roof_edit = current_widget.roof_edit.text().replace(',', '.')
        sole_edit = current_widget.sole_edit.text().replace(',', '.')
        date_pvr_edit = current_widget.date_pvr_edit.text()
        count_pvr_edit = current_widget.count_pvr_edit.text()
        type_pvr_edit = current_widget.type_pvr_edit.text()
        pressuar_pvr_edit = current_widget.pressuar_pvr_edit.text().replace(',', '.')
        date_pressuar_edit = current_widget.date_pressuar_edit.text()
        vertical_line = current_widget.vertical_line.text().replace(',', '.')

        if '' in [plast_line, roof_edit, sole_edit, count_pvr_edit, type_pvr_edit]:
            QMessageBox.warning(self, 'Ошибка', 'Не введены все даныые')
            return
        udlin = round(float(roof_edit) - float(vertical_line), 1)
        if [plast_line, vertical_line, roof_edit, sole_edit, date_pvr_edit, count_pvr_edit,
            type_pvr_edit, pressuar_pvr_edit, date_pressuar_edit] not in self.dict_perforation:
            self.dict_perforation.append(
                [plast_line, vertical_line, roof_edit, sole_edit, date_pvr_edit, count_pvr_edit,
                 type_pvr_edit, pressuar_pvr_edit, date_pressuar_edit])
        rows = 0
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(plast_line)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(vertical_line)))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(roof_edit)))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(sole_edit)))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(date_pvr_edit)))
        aaaa = self.old_index
        if self.old_index == 0:
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(count_pvr_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(type_pvr_edit)))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(udlin)))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(pressuar_pvr_edit)))
            self.tableWidget.setItem(rows, 10, QTableWidgetItem(str(date_pressuar_edit)))
        else:
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(count_pvr_edit)))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(type_pvr_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(udlin)))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(pressuar_pvr_edit)))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(date_pressuar_edit)))

    def addPerfProject(self):
        current_widget = self.tabWidget.currentWidget()
        table_in_base_combo = str(current_widget.well_data_in_base_combo.currentText())

        if ' от' in table_in_base_combo:
            asdf = table_in_base_combo.split(' ')
            table_in_base = table_in_base_combo.split(' ')[3].replace('krs', 'ПР').replace('dop_plan', 'ДП').replace(
                'dop_plan_in_base', 'ДП')
            type_kr = table_in_base_combo.split(' ')[2]
        well_number = current_widget.well_number_edit.text()
        well_area = current_widget.well_area_edit.text()
        if well_number == '' or well_area == '':
            QMessageBox.critical(self, 'ошибка', 'Ввведите номер площадь скважины')
            return
        self.work_with_excel(well_number, well_area, table_in_base, type_kr)

    def work_with_excel(self, well_number, well_area, work_plan, type_kr):

        self.data, self.rowHeights, self.colWidth, self.boundaries_dict = \
            DopPlanWindow.read_excel_in_base(well_number, well_area, work_plan, type_kr)

        self.target_row_index = 5000
        self.target_row_index_cancel = 5000
        self.bottom_row_index = 5000

        perforation_list = []
        aaaaa = self.data
        for i, row in self.data.items():
            if i != 'image':
                list_row = []
                for col in range(len(row)):
                    if 'оризонт' in str(row[col]['value']) or 'пласт/' in str(row[col]['value']).lower():
                        self.target_row_index = int(i) + 1
                    elif 'вскрытия/отключения' in str(row[col]['value']):
                        self.old_index = 1
                    elif 'II. История эксплуатации скважины' in str(row[col]['value'])  and \
                            well_data.work_plan not in ['plan_change']:
                        self.target_row_index_cancel = int(i) - 1
                        break
                    elif 'внутренний диаметр ( d шарошечного долота) необсаженной части ствола' in str(row[col]['value']) and \
                            well_data.work_plan not in ['plan_change']:
                        self.target_row_index_cancel = int(i)
                        break
                    elif 'Порядок работы' == str(row[col]['value']) and well_data.data_x_max._value == 0:
                        well_data.data_x_max = well_data.ProtectedIsDigit(int(i) + 1)
                        break
                    elif 'ИТОГО:' in str(row[col]['value']) and well_data.work_plan in ['plan_change']:
                        self.target_row_index_cancel = int(i)+1
                        break
                    elif 'Текущий забой ' == str(row[col]['value']):
                        self.bottom_row_index = int(i)

                    if int(i) > self.target_row_index and self.target_row_index_cancel > int(i):
                        list_row.append(row[col]['value'])

                    if int(i) > self.target_row_index_cancel:
                        break

            if len(list_row) != 0 and not 'внутренний диаметр ( d шарошечного долота) необсаженной части ствола' in list_row:
                if all([col == None or col == '' for col in list_row]) is False:
                    perforation_list.append(list_row)
        well_data.ins_ind2 = well_data.data_x_max._value

        if well_data.work_plan != 'plan_change':
            self.tableWidget.setSortingEnabled(False)
            rows = self.tableWidget.rowCount()
            for row_pvr in perforation_list[::-1]:
                self.tableWidget.insertRow(rows)
                for index_col, col_pvr in enumerate(row_pvr):
                    if col_pvr != None:
                        self.tableWidget.setItem(rows, index_col - 1, QTableWidgetItem(str(col_pvr)))
    @staticmethod
    def read_excel_in_base(number_well, area_well, work_plan, type_kr):
        if well_data.connect_in_base:
            conn = psycopg2.connect(**well_data.postgres_params_data_well)
            cursor = conn.cursor()
            param = '%s'

        else:
            db_path = connect_to_db('well_data.db', 'data_base_well/')

            conn = sqlite3.connect(f'{db_path}')
            cursor = conn.cursor()
            param = '?'
        aaa = well_data.contractor
        cursor.execute(f"SELECT excel_json "
                       f"FROM wells "
                       f"WHERE well_number={param} AND area_well={param} AND contractor={param} "
                       f"AND costumer={param} AND work_plan={param} AND type_kr={param}",
                       (str(number_well), area_well, well_data.contractor, well_data.costumer, work_plan, type_kr))
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
            QMessageBox.warning(None, 'Ошибка', f'Введены не все параметры {type(e).__name__}\n\n{str(e)}')
            return

        return data, rowHeights, colWidth, boundaries_dict

    def change_pvr_in_bottom(self, data, rowHeights, colWidth, boundaries_dict, current_bottom=0,
                             current_bottom_date_edit=0, method_bottom_combo=0):

        for i, row in data.items():
            if i != 'image':
                for col in range(len(row)):
                    if 'Текущий забой ' == str(row[col]['value']):
                        self.bottom_row_index = int(i)
                        break
        try:

            data[str(self.bottom_row_index)][3]['value'] = current_bottom

            data[str(self.bottom_row_index)][5]['value'] = current_bottom_date_edit

            data[str(self.bottom_row_index)][-1]['value'] = method_bottom_combo
        except:
            pass
        return data, rowHeights, colWidth, boundaries_dict

    def insert_row_in_pvr(self, data, rowHeights, colWidth, boundaries_dict, plast_list, current_bottom,
                          current_bottom_date_edit, method_bottom_combo):
        count_row_insert = len(plast_list)
        count_row_in_plan = self.target_row_index_cancel - self.target_row_index - 1
        boundaries_dict_new = {}
        if self.target_row_index != 5000:
            n = len(data)-1
            if count_row_in_plan < count_row_insert:
                count_row_insert = count_row_insert - count_row_in_plan
                while n+1 != int(self.target_row_index):
                    data.update({str(n + count_row_insert): data[str(n)]})
                    n -= 1
                rowHeights.insert(int(self.target_row_index) + count_row_insert, None)

                for key, value in boundaries_dict.items():
                    if value[1] >= int(self.target_row_index) + 1:
                        value = [value[0], value[1] + count_row_insert, value[2], value[3] + count_row_insert]
                    boundaries_dict_new[key] = value

            else:

                for key, value in boundaries_dict.items():

                    if int(self.target_row_index) + 1 <= value[1] <= int(self.target_row_index_cancel - 4):
                        value = [value[0], value[1], value[0], value[3]]
                    boundaries_dict_new[key] = value

            for index_row, plast in enumerate(plast_list):
                row_index = str(int(self.target_row_index + index_row + 1))
                a = plast[0]
                data[row_index] = [
                    {'value': '', 'font': {'name': 'Times New Roman Cyr', 'size': 10.0, 'bold': False, 'italic': False},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': None, 'right': None, 'top': None, 'bottom': None},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': True}},
                    {'value': plast[0], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[1], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': None}},
                    {'value': plast[2], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[3], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[4], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': None, 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[5], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': None, 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[6], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[7], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[8], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[9], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': plast[10], 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': None, 'font': {'name': 'Calibri', 'size': 11.0, 'bold': False, 'italic': False},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': None, 'right': None, 'top': None, 'bottom': None},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': None}}]
            rows = self.tableWidget.rowCount()
            while self.target_row_index != self.target_row_index_cancel - rows:
                index = str(int(self.target_row_index + index_row + 2))
                data[index] = [
                    {'value': '', 'font': {'name': 'Times New Roman Cyr', 'size': 10.0, 'bold': False, 'italic': False},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': None, 'right': None, 'top': None, 'bottom': None},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': True}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': None, 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': None, 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': None, 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Arial Cyr', 'size': 12.0, 'bold': False, 'italic': True},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'},
                     'alignment': {'horizontal': 'center', 'vertical': 'center', 'wrap_text': None}},
                    {'value': '', 'font': {'name': 'Calibri', 'size': 11.0, 'bold': False, 'italic': False},
                     'fill': {'color': 'RGB(00000000)'},
                     'borders': {'left': None, 'right': None, 'top': None, 'bottom': None},
                     'alignment': {'horizontal': None, 'vertical': None, 'wrap_text': None}}]

                self.target_row_index += 1
        data[str(self.bottom_row_index)][3]['value'] = current_bottom
        data[str(self.bottom_row_index)][5]['value'] = current_bottom_date_edit
        data[str(self.bottom_row_index)][10 - self.old_index]['value'] = method_bottom_combo
        #     print(i)

        return data, rowHeights, colWidth, boundaries_dict_new

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def add_work(self):
        from data_base.work_with_base import check_in_database_well_data, insert_data_well_dop_plan, round_cell
        from well_data import ProtectedIsNonNone
        
        current_widget = self.tabWidget.currentWidget()
        method_bottom_combo = current_widget.method_bottom_combo.currentText()
        if method_bottom_combo == '':
            QMessageBox.critical(self, 'Забой', 'Выберете метод определения забоя')
            return

        change_pvr_combo = current_widget.change_pvr_combo.currentText()
        if change_pvr_combo == '':
            QMessageBox.warning(self, 'Ошибка', 'Нужно выбрать пункт изменения ПВР')
            return
        if well_data.data_in_base:

            fluid = current_widget.fluid_edit.text().replace(',', '.')
            current_bottom = current_widget.current_bottom_edit.text()
            if current_bottom != '':
                current_bottom = round_cell(current_bottom.replace(',', '.'))

            work_earlier = current_widget.work_edit.toPlainText()
            number_dp = current_widget.number_DP_Combo.currentText()

            current_bottom_date_edit = current_widget.current_bottom_date_edit.text()

            template_depth_edit = current_widget.template_depth_edit.text()
            template_lenght_edit = current_widget.template_lenght_edit.text()
            if well_data.column_additional:
                template_depth_addition_edit = current_widget.template_depth_addition_edit.text()
                template_lenght_addition_edit = current_widget.template_lenght_addition_edit.text()
            skm_interval_edit = current_widget.skm_interval_edit.text()

            if current_bottom == '' or fluid == '' or work_earlier == '' or \
                    template_depth_edit == '' or template_lenght_edit == '':
                # print(current_bottom, fluid, work_earlier)
                QMessageBox.critical(self, 'Забой', 'не все значения введены')
                return
            if template_lenght_edit == '0' or template_lenght_edit == '':
                mes = QMessageBox.question(self, 'Длина шаблона', 'в скважину во время ремонта не был спущен шаблон, '
                                                                  'так ли это?')
                if mes == QMessageBox.StandardButton.No:
                    return
            if float(template_depth_edit) > float(well_data.bottomhole_artificial._value):
                QMessageBox.critical(self, 'Забой', 'Шаблонирование не может быть ниже текущего забоя')
                return
            if number_dp != '':
                well_data.number_dp = int(float(number_dp))

            if (0.87 <= float(fluid[:3].replace(',', '.')) <= 1.64) == False:
                QMessageBox.critical(self, 'рабочая жидкость',
                                           'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
                return
            if well_data.data_in_base:
                if 'г/см3' not in fluid:
                    QMessageBox.critical(self, 'уд.вес', 'нужно добавить значение "г/см3" в уд.вес')
                    return
                well_data.fluid_work = fluid
                well_data.fluid_work_short = fluid[:7]

                well_data.fluid = fluid[:4]
            else:

                if float(current_bottom) > well_data.bottomhole_drill._value:
                    QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
                    return
                well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(fluid)

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
                            skm_interval.append(list(map(int, skm.split('-'))))
                else:
                    if '-' in skm_interval_edit:
                        skm_interval.append(list(map(int, skm_interval_edit.split('-'))))

                skm_interval_new = merge_overlapping_intervals(skm_interval)

                well_data.skm_interval = skm_interval_new

            except:
                QMessageBox.warning(self, 'Ошибка',
                                          'в интервале скреперования отсутствует корректные интервалы скреперования')

            if len(well_data.skm_interval) == 0:
                mes = QMessageBox.question(self, 'Ошибка',
                                           'Интервалы скреперования отсутствуют, так ли это?')
                if mes == QMessageBox.StandardButton.No:
                    return
            well_data.count_template = 1
            if well_data.data_in_base:
                data_well_data_in_base_combo, data_table_in_base_combo = '', ''
                # table_in_base_combo = str(current_widget.table_in_base_combo.currentText())
                well_data_in_base_combo = current_widget.well_data_in_base_combo.currentText()

                if ' от' in well_data_in_base_combo:
                    asd = well_data_in_base_combo.split(' ')
                    data_table_in_base_combo = well_data_in_base_combo.split(' ')[-1]
                    table_in_base = well_data_in_base_combo.split(' ')[3]
                    type_kr = well_data_in_base_combo.split(' ')[2]
                    well_data.type_kr = type_kr + ' ' "vf"
                    number_dp_in_base = "".join(c for c in table_in_base if c.isdigit())
                    table_in_base = well_data_in_base_combo.split(' ')[3].replace('krs', 'ПР').replace('dop_plan_in_base',
                                                                                                   'ДП№').replace(
                        'dop_plan', 'ДП№')

                index_change_line = current_widget.index_change_line.text()
                well_number = current_widget.well_number_edit.text()
                well_area = current_widget.well_area_edit.text()
                if well_area != '' and well_area != '':
                    well_data.well_number, well_data.well_area = \
                        ProtectedIsNonNone(well_number), ProtectedIsNonNone(well_area)
                if index_change_line != '':
                    index_change_line = int(float(index_change_line))
                else:
                    QMessageBox.critical(self, 'пункт', 'Необходимо выбрать пункт плана работ')
                    return
                list_dop_plan = self.get_tables_starting_with(well_data.well_number._value,
                                                                                well_data.well_area._value, table_in_base, type_kr)
                if list_dop_plan:
                    if any([f'ДП№{number_dp}' in dop_plan or f'ДП№{number_dp}' in dop_plan for dop_plan in list_dop_plan]):
                        question = QMessageBox.question(self, 'Ошибка', f'дополнительный план работ № {number_dp} '
                                                                        f'есть в базе, обновить доп план?')
                        if question == QMessageBox.StandardButton.No:
                            return


                if well_data_in_base_combo == '':
                    QMessageBox.critical(self, 'База данных', 'Необходимо выбрать план работ')
                    return

                data_well = check_in_database_well_data(well_number, well_area, table_in_base)

                if data_well:
                    well_data.type_kr = data_well[2]
                    if data_well[3]:
                        well_data.dict_category = json.loads(data_well[3])
                    insert_data_well_dop_plan(data_well[0])

                # self.work_with_excel(well_number, well_area, table_in_base, type_kr)

                self.extraction_data(well_data_in_base_combo, index_change_line)

            well_data.current_bottom = current_bottom

            if skm_interval_edit not in ['', 0, '0-0'] and '-' in skm_interval_edit:
                if ',' in skm_interval_edit:
                    for skm_int in skm_interval_edit.split(','):
                        well_data.skm_interval.append(list(map(int, skm_int.split('-'))))
                else:
                    well_data.skm_interval.append(list(map(int, skm_interval_edit.split('-'))))

            rows = self.tableWidget.rowCount()

            if change_pvr_combo == 'Да':
                if rows == 0:
                    QMessageBox.warning(self, 'Ошибка', 'Нужно загрузить интервалы перфорации')
                    return

                plast_row = []
                for row in range(rows):
                    list_row = []
                    for col in range(13):
                        item = self.tableWidget.item(row, col)
                        if item is not None:
                            list_row.append(item.text())
                        else:
                            list_row.append(None)
                    plast_row.append(list_row)
                well_data.data, well_data.rowHeights, well_data.colWidth, well_data.boundaries_dict = \
                    self.insert_row_in_pvr(self.data, self.rowHeights, self.colWidth, self.boundaries_dict, plast_row,
                                           current_bottom, current_bottom_date_edit, method_bottom_combo)
            else:
                well_data.data, well_data.rowHeights, well_data.colWidth, well_data.boundaries_dict = \
                    self.change_pvr_in_bottom(self.data, self.rowHeights, self.colWidth, self.boundaries_dict,
                                              current_bottom, current_bottom_date_edit, method_bottom_combo)
            if well_data.data_in_base:
                well_data.dop_work_list = self.work_list(work_earlier)
            else:
                work_list = self.work_list(work_earlier)
                self.populate_row(self.ins_ind + 3, work_list, self.table_widget, self.work_plan)

            if len(self.dict_perforation) != 0:
                for plast, vertical_line,  roof_int, sole_int, date_pvr_edit, count_pvr_edit, \
                    type_pvr_edit, pressuar_pvr_edit, date_pressuar_edit in self.dict_perforation:
                    well_data.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                    well_data.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)

                    well_data.dict_perforation.setdefault(plast, {}).setdefault('интервал', []).append(
                        (float(roof_int), float(sole_int)))
                    well_data.dict_perforation_short.setdefault(plast, {}).setdefault('интервал', []).append(
                        (float(roof_int), float(sole_int)))
                    well_data.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                    well_data.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)

        else:
            fluid = current_widget.fluid_edit.text().replace(',', '.')
            current_bottom = current_widget.current_bottom_edit.text()
            if current_bottom != '':
                current_bottom = round_cell(current_bottom.replace(',', '.'))

            work_earlier = current_widget.work_edit.toPlainText()
            number_dp = current_widget.number_DP_Combo.currentText()

            template_depth_edit = current_widget.template_depth_edit.text()
            template_lenght_edit = current_widget.template_lenght_edit.text()
            if well_data.column_additional:
                template_depth_addition_edit = current_widget.template_depth_addition_edit.text()
                template_lenght_addition_edit = current_widget.template_lenght_addition_edit.text()
            skm_interval_edit = current_widget.skm_interval_edit.text()
            try:

                if skm_interval_edit not in ['', 0, '0-0'] and '-' in skm_interval_edit:
                    if ',' in skm_interval_edit:
                        for skm_int in skm_interval_edit.split(','):
                            well_data.skm_interval.append(list(map(int, skm_int.split('-'))))
                    else:
                        well_data.skm_interval.append(list(map(int, skm_interval_edit.split('-'))))

            except:
                QMessageBox.warning(self, 'Ошибка',
                                          'в интервале скреперования отсутствует корректные интервалы скреперования')
                return

            if current_bottom == '' or fluid == '' or work_earlier == '' or \
                    template_depth_edit == '' or template_lenght_edit == '':
                # print(current_bottom, fluid, work_earlier)
                QMessageBox.critical(self, 'Забой', 'не все значения введены')
                return
            if template_lenght_edit == '0':
                QMessageBox.critical(self, 'Длина шаблона',
                                           'Введите длину шаблонов которые были спущены в скважину')
                return
            if float(template_depth_edit) > float(current_bottom):
                QMessageBox.critical(self, 'Забой', 'Шаблонирование не может быть ниже текущего забоя')
                return
            if number_dp != '':
                well_data.number_dp = int(float(number_dp))

            if (0.87 <= float(fluid[:3].replace(',', '.')) <= 1.64) == False:
                QMessageBox.critical(self, 'рабочая жидкость',
                                           'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
                return

            # if float(current_bottom) > well_data.bottomhole_drill._value:
            #     QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
            #     return
            well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(fluid)

            well_data.template_depth = float(template_depth_edit)
            well_data.template_lenght = float(template_lenght_edit)
            if well_data.column_additional:
                well_data.template_depth = float(template_depth_addition_edit)
                well_data.template_lenght = float(template_lenght_addition_edit)

            work_list = self.work_list(work_earlier)
            well_data.ins_ind2 = self.ins_ind + 2
            self.populate_row(self.ins_ind + 2, work_list, self.table_widget, self.work_plan)

        well_data.pause = False
        self.close()

    def delete_data(self, number_well, area_well, work_plan, type_kr):
        if well_data.connect_in_base:
            try:
                conn = psycopg2.connect(**well_data.postgres_params_data_well)
                cursor = conn.cursor()

                cursor.execute("""
                DELETE FROM wells 
                WHERE well_number = %s AND area_well = %s  AND costumer = %s AND work_plan= %s AND type_kr=%s""",
                               (str(number_well), area_well,  well_data.costumer, work_plan, type_kr)
                               )

                conn.commit()
                cursor.close()
                conn.close()

            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка удаления {type(e).__name__}\n\n{str(e)}')
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
                QMessageBox.warning(None, 'Ошибка',
                                          f'Ошибка удаления {type(e).__name__}\n\n{str(e)}')

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
                            well_data.ins_ind2 = i + 1
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')

    def extraction_data(self, table_name, paragraph_row=0):
        from data_base.work_with_base import connect_to_db

        date_table = table_name.split(' ')[-1]
        well_number = table_name.split(' ')[0]
        well_area = table_name.split(' ')[1]
        type_kr = table_name.split(' ')[2].replace('None', 'null')

        work_plan = table_name.split(' ')[3]

        if well_data.connect_in_base:
            try:
                # Устанавливаем соединение с базой данных
                conn = psycopg2.connect(**well_data.postgres_params_data_well)

                cursor = conn.cursor()
                param = '%s'


            except psycopg2.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка', f"Тип ошибки: {e}. Проверьте количество переданных аргументов.")

        else:
            try:
                # Формируем полный путь к файлу базы данных
                db_path = connect_to_db('well_data.db', 'data_base_well')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                param = '?'


            except sqlite3.Error as e:
                # Выведите сообщение об ошибке
                QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных.')


        cursor.execute(f'''
        SELECT data_change_paragraph FROM wells 
        WHERE well_number={param} AND area_well={param} AND type_kr={param} AND work_plan={param} AND today={param}''',
        (str(well_number), well_area, type_kr, work_plan, date_table))

        result_table = cursor.fetchone()
        # Закройте курсор и соединение
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        if result_table is None:
            QMessageBox.warning(self, 'Ошибка',
                                f'В базе данных скв {well_number} {well_area} отсутствует данные, '
                                f'используйте excel вариант плана работ')

        if result_table[0]:
            result = json.loads(result_table[0])

            if well_data.work_plan in ['dop_plan', 'dop_plan_in_base']:
                DopPlanWindow.insert_data_dop_plan(self, result, paragraph_row)
            elif well_data.work_plan == 'plan_change':
                DopPlanWindow.insert_data_plan(self, result)
            well_data.data_well_is_True = True

        else:
            well_data.data_in_base = False
            QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                      f"Таблицы '{table_name}' нет в базе данных.")

        return

    def insert_data_dop_plan(self, result, paragraph_row):
        try:
            paragraph_row = paragraph_row - 1
        except:
            paragraph_row = 1
        if len(result) < paragraph_row:
            QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пункта')
            return

        well_data.current_bottom = result[paragraph_row][1]

        well_data.dict_perforation = json.loads(result[paragraph_row][2])
        aakka = well_data.dict_perforation

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

        definition_plast_work(None)

    def insert_data_plan(self, result):
        well_data.data_list = []
        for ind, row in enumerate(result):
            if ind == 1:
                well_data.bottom = row[1]
                well_data.category_pressuar2 = row[8]
                well_data.category_h2s_2 = row[9]
                well_data.gaz_f_pr_2 = row[10]

                well_data.plast_work_short = json.dumps(row[3], ensure_ascii=False)

            data_list = []
            for index, data in enumerate(row):
                if index == 6:
                    if data == 'false' or data == 0 or data == '0':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            well_data.data_list.append(data_list)
        well_data.current_bottom = result[ind][1]
        well_data.dict_perforation = json.loads(result[ind][2])

        well_data.plast_all = json.loads(result[ind][3])
        well_data.plast_work = json.loads(result[ind][4])
        well_data.leakage = json.loads(result[ind][5])
        well_data.dict_perforation_short = json.loads(result[ind][2])


        definition_plast_work(None)

    def work_list(self, work_earlier):
        krs_begin = [[None, None,
                      f' Ранее проведенные работ: \n {work_earlier}',
                      None, None, None, None, None, None, None,
                      'Мастер КРС', None]]

        return krs_begin
