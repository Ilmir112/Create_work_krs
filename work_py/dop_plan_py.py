import json
from collections import namedtuple

from openpyxl.styles import Font, Alignment

import data_list

from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QPushButton, QTextEdit, QDateEdit
from PyQt5.QtCore import Qt
from datetime import datetime

from data_base.config_base import connection_to_database, WorkDatabaseWell

from krs import GnoWindow
from main import MyMainWindow
from work_py.advanted_file import merge_overlapping_intervals, definition_plast_work
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageDp(TabPageUnion):
    def __init__(self, dict_data_well, tableWidget, old_index, parent =None):
        super().__init__(dict_data_well)

        self.tableWidget = tableWidget
        self.old_index = old_index

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)
        self.work_plan = dict_data_well['work_plan']

        self.well_number_label = QLabel('номер скважины')
        self.well_number_edit = QLineEdit(self)
        # self.well_number_edit.setValidator(self.validator_int)

        self.well_area_label = QLabel('площадь скважины')
        self.well_area_edit = QLineEdit(self)

        self.number_DP_label = QLabel('номер \nдополнительного плана')
        self.number_DP_Combo = QComboBox(self)

        self.number_DP_Combo.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        if self.dict_data_well["number_dp"] != 0:
            self.number_DP_Combo.setCurrentIndex(int(self.dict_data_well["number_dp"]) - 1)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setValidator(self.validator_float)
        # self.current_bottom_edit.setText(f'{self.dict_data_well["current_bottom"]}')

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
        # self.template_depth_edit.setText(str(self.dict_data_well["template_depth"]))

        self.template_lenght_label = QLabel('Длина шаблона')
        self.template_lenght_edit = QLineEdit(self)
        self.template_lenght_edit.setValidator(self.validator_float)

        self.change_pvr_combo_label = QLabel('Были ли изменения \nв интервале перфорации')
        self.change_pvr_combo = QComboBox(self)
        self.change_pvr_combo.addItems(['', 'Нет', 'Да'])

        self.skm_interval_label = QLabel('интервалы \nскреперования')
        self.skm_interval_edit = QLineEdit(self)

        self.raiding_interval_label = QLabel('интервалы \n Райбирования')
        self.raiding_interval_edit = QLineEdit(self)

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

        # if self.dict_data_well["fluid_work"] == '':
        #     self.fluid_edit.setText(f'{TabPageGno.calc_fluid(self.work_plan, self.dict_data_well["current_bottom"])}')
        # else:
        #     self.fluid_edit.setText(f'{self.dict_data_well["fluid_work"]}')

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
        self.grid.addWidget(self.skm_interval_label, 8, 1, 1, 2)
        self.grid.addWidget(self.skm_interval_edit, 9, 1, 1, 2)
        self.grid.addWidget(self.raiding_interval_label, 8, 3, 1, 3)
        self.grid.addWidget(self.raiding_interval_edit, 9, 3, 1, 3)
        self.grid.addWidget(self.change_pvr_combo_label, 10, 1)
        self.grid.addWidget(self.change_pvr_combo, 11, 1)

        self.grid.addWidget(self.work_label, 25, 1)
        self.grid.addWidget(self.work_edit, 26, 1, 2, 4)

        self.well_number_edit.editingFinished.connect(self.update_well)
        try:
            self.well_area_edit.setText(f'{self.dict_data_well["well_area"]._value}')
            self.well_number_edit.setText(f'{self.dict_data_well["well_number"]._value}')
            self.well_area_edit.setEnabled(False)
            self.well_number_edit.setEnabled(False)
        except:
            pass

        # self.well_area_edit.textChanged.connect(self.update_well)

        self.change_pvr_combo.currentTextChanged.connect(self.update_change_pvr)
        self.change_pvr_combo.setCurrentIndex(1)
        self.change_pvr_combo.setCurrentIndex(0)


        if data_list.data_in_base:

            # self.table_in_base_label = QLabel('данные по скважине')
            # self.table_in_base_combo = QComboBox()
            # self.table_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            self.well_data_label = QLabel('файл excel сохранный в базе')
            self.well_data_in_base_combo = QComboBox()
            self.well_data_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
            self.well_data_in_base_combo.currentTextChanged.connect(self.update_well_data_in_base_combo)

            self.index_change_label = QLabel('пункт после которого происходят изменения')
            self.index_change_line = QLineEdit(self)
            self.index_change_line.setValidator(self.validator_int)

            self.grid.addWidget(self.well_data_label, 2, 6)
            self.grid.addWidget(self.well_data_in_base_combo, 3, 6)
            self.grid.addWidget(self.index_change_label, 2, 7)
            self.grid.addWidget(self.index_change_line, 3, 7)




            self.index_change_line.editingFinished.connect(self.update_table_in_base_combo)

    def update_well_data_in_base_combo(self, index):
        if index:
            if index.split(' ')[3] != 'ПР':
                number_dp_in_base = [num for num in index.split(' ')[3] if num.isdigit()][0]
                self.number_DP_Combo.setCurrentIndex(int(number_dp_in_base))

    def check_in_database_well_data2(self, number_well):
        db = connection_to_database(data_list.DB_WELL_DATA)
        data_well_base = WorkDatabaseWell(db, self.dict_data_well)


        # Получение всех результатов
        wells_with_data = data_well_base.check_well_in_database_well_data(number_well)
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
        if data_list.data_in_base:

            well_list = self.check_in_database_well_data2(self.well_number_edit.text())
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
            self.dict_data_well["number_dp"] = int(float(number_dp))

        if index_change_line != '':
            index_change_line = int(float(index_change_line))
            data = DopPlanWindow.extraction_data(self, well_data_in_base_combo, index_change_line)
            if data is None:
                return
            self.template_depth_edit.setText(str(self.dict_data_well["template_depth"]))
            self.template_lenght_edit.setText(str(self.dict_data_well["template_lenght"]))
            skm_interval = ''

            try:

                if len(self.dict_data_well["skm_interval"]) != 0:
                    for roof, sole in self.dict_data_well["skm_interval"]:
                        if f'{roof}-{sole}' not in skm_interval:
                            skm_interval += f'{roof}-{sole}, '
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не получилось сохранить данные скреперования '
                                                    f'{type(e).__name__}\n\n{str(e)}')

            raiding_interval = ''

            try:

                if len(self.dict_data_well["ribbing_interval"]) != 0:
                    asddfg = self.dict_data_well["ribbing_interval"]
                    for roof, sole in self.dict_data_well["ribbing_interval"]:
                        if f'{roof}-{sole}' not in raiding_interval:
                            raiding_interval += f'{roof}-{sole}, '
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не получилось сохранить данные Райбирования '
                                                    f'{type(e).__name__}\n\n{str(e)}')

            self.skm_interval_edit.setText(skm_interval[:-2])
            self.raiding_interval_edit.setText(raiding_interval[:-2])
            self.current_bottom_edit.setText(str(self.dict_data_well["current_bottom"]))
            self.fluid_edit.setText(str(self.dict_data_well["fluid_work"]))
            if self.dict_data_well["column_additional"]:
                self.template_depth_addition_label = QLabel('Глубина спуска шаблона в доп колонне')
                self.template_depth_addition_edit = QLineEdit(self)
                self.template_depth_addition_edit.setValidator(self.validator_float)
                self.template_depth_addition_edit.setText(str(self.dict_data_well["template_depth_addition"]))

                self.template_lenght_addition_label = QLabel('Длина шаблона в доп колонне')
                self.template_lenght_addition_edit = QLineEdit(self)
                self.template_lenght_addition_edit.setValidator(self.validator_float)
                self.template_lenght_addition_edit.setText(str(self.dict_data_well["template_lenght_addition"]))
                self.grid.addWidget(self.template_depth_addition_label, 6, 4)
                self.grid.addWidget(self.template_depth_addition_edit, 7, 4)
                self.grid.addWidget(self.template_lenght_addition_label, 6, 5)
                self.grid.addWidget(self.template_lenght_addition_edit, 7, 5)


class TabWidget(TabWidgetUnion):
    def __init__(self, work_plan, tableWidget=0, old_index=0):
        super().__init__()
        self.addTab(TabPageDp(work_plan, tableWidget, old_index), 'Дополнительный план работ')


class DopPlanWindow(WindowUnion):
    def __init__(self, dict_data_well, table_widget, parent=None):
        super(DopPlanWindow, self).__init__(dict_data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)


        self.table_widget = table_widget
        self.work_plan = self.dict_data_well["work_plan"]
        if self.work_plan == 'dop_plan_in_base':
            self.dict_data_well["number_dp"] = 0
            self.ins_ind = 0
        else:
            self.ins_ind = self.dict_data_well["ins_ind"]

        self.data, self.rowHeights, self.colWidth, self.boundaries_dict = None, None, None, None
        self.target_row_index = None
        self.target_row_index_cancel = None
        self.old_index = 0
        self.tableWidget = QTableWidget(0, 12)

        self.tabWidget = TabWidget(self.dict_data_well, self.tableWidget, self.old_index)
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

        self.plast_line = current_widget.plast_line.text()
        self.roof_edit = current_widget.roof_edit.text().replace(',', '.')
        self.sole_edit = current_widget.sole_edit.text().replace(',', '.')
        self.date_pvr_edit = current_widget.date_pvr_edit.text()
        self.count_pvr_edit = current_widget.count_pvr_edit.text()
        self.type_pvr_edit = current_widget.type_pvr_edit.text()
        self.pressuar_pvr_edit = current_widget.pressuar_pvr_edit.text().replace(',', '.')
        self.date_pressuar_edit = current_widget.date_pressuar_edit.text()
        vertical_line = current_widget.vertical_line.text().replace(',', '.')

        if '' in [self.plast_line, self.roof_edit, self.sole_edit, self.count_pvr_edit, self.type_pvr_edit]:
            QMessageBox.warning(self, 'Ошибка', 'Не введены все даныые')
            return
        udlin = round(float(self.roof_edit) - float(vertical_line), 1)
        if [self.plast_line, vertical_line, self.roof_edit, self.sole_edit, self.date_pvr_edit, self.count_pvr_edit,
            self.type_pvr_edit, self.pressuar_pvr_edit, self.date_pressuar_edit] not in self.dict_perforation:
            self.dict_perforation.append(
                [self.plast_line, vertical_line, self.roof_edit, self.sole_edit, self.date_pvr_edit, self.count_pvr_edit,
                 self.type_pvr_edit, self.pressuar_pvr_edit, self.date_pressuar_edit])
        rows = 0
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(self.plast_line)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(vertical_line)))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(self.roof_edit)))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(self.sole_edit)))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(self.date_pvr_edit)))
        aaaa = self.old_index
        if self.old_index == 0:
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(self.count_pvr_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(self.type_pvr_edit)))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(udlin)))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(self.pressuar_pvr_edit)))
            self.tableWidget.setItem(rows, 10, QTableWidgetItem(str(self.date_pressuar_edit)))
        else:
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(self.count_pvr_edit)))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(self.type_pvr_edit)))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(udlin)))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(self.pressuar_pvr_edit)))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(self.date_pressuar_edit)))


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
        from data_correct import DataWindow

        self.dict_data_well["gips_in_well"] = False
        self.data, self.rowHeights, self.colWidth, self.boundaries_dict = \
            DopPlanWindow.read_excel_in_base(well_number, well_area, work_plan, type_kr)

        self.target_row_index = 5000
        self.target_row_index_cancel = 5000
        self.bottom_row_index = 5000


        perforation_list = []

        for i, row in self.data.items():
            if i != 'image':
                list_row = []
                for col in range(len(row)):
                    if 'оризонт' in str(row[col]['value']) or 'пласт/' in str(row[col]['value']).lower():
                        self.target_row_index = int(i) + 1
                    elif 'вскрытия/отключения' in str(row[col]['value']):
                        self.old_index = 1
                    elif 'II. История эксплуатации скважины' in str(row[col]['value'])  and \
                            self.dict_data_well["work_plan"] not in ['plan_change']:
                        self.target_row_index_cancel = int(i) - 1
                        break
                    elif 'внутренний диаметр ( d шарошечного долота) необсаженной части ствола' in str(row[col]['value']) and \
                            self.dict_data_well["work_plan"] not in ['plan_change']:
                        self.target_row_index_cancel = int(i)
                        break
                    elif 'Порядок работы' in str(row[2]['value']):
                        self.dict_data_well["data_x_max"] = data_list.ProtectedIsDigit(int(i) + 1)
                        break
                    elif 'ИТОГО:' in str(row[col]['value']) and self.dict_data_well["work_plan"] in ['plan_change']:
                        self.target_row_index_cancel = int(i)+1
                        break
                    elif 'Текущий забой ' == str(row[col]['value']):
                        self.bottom_row_index = int(i)

                    if int(i) > self.target_row_index and self.target_row_index_cancel > int(i):
                        list_row.append(row[col]['value'])

                    if int(i) > self.target_row_index_cancel:
                        break
            else:

                self.dict_data_well["image_list"] = row

            if len(list_row) != 0 and not 'внутренний диаметр ( d шарошечного долота) необсаженной части ствола' in list_row:
                if all([col == None or col == '' for col in list_row]) is False:
                    perforation_list.append(list_row)
        self.dict_data_well["ins_ind2"] = self.dict_data_well["data_x_max"]._value
        self.dict_data_well["count_template"] = 1


        if self.dict_data_well["work_plan"] != 'plan_change':
            self.tableWidget.setSortingEnabled(False)
            rows = self.tableWidget.rowCount()
            for row_pvr in perforation_list[::-1]:
                self.tableWidget.insertRow(rows)
                for index_col, col_pvr in enumerate(row_pvr):
                    if col_pvr != None:
                        self.tableWidget.setItem(rows, index_col - 1, QTableWidgetItem(str(col_pvr)))

        DataWindow.definition_open_trunk_well(self)
    @staticmethod
    def read_excel_in_base(number_well, area_well, work_plan, type_kr):
        db = connection_to_database(data_list.DB_WELL_DATA)
        data_well_base = WorkDatabaseWell(db)

        data_well = data_well_base.read_excel_in_base(number_well, area_well, work_plan, type_kr)

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
        if 0 not in [current_bottom, current_bottom_date_edit, method_bottom_combo]:

            data[str(self.bottom_row_index)][3]['value'] = current_bottom
            data[str(self.bottom_row_index)][5]['value'] = current_bottom_date_edit
            data[str(self.bottom_row_index)][-1]['value'] = method_bottom_combo

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
        from data_base.work_with_base import  insert_data_well_dop_plan, round_cell
        from data_list import ProtectedIsNonNone
        from work_py.advanted_file import definition_plast_work
        self.dict_data_well["data_list"] = []
        
        current_widget = self.tabWidget.currentWidget()
        method_bottom_combo = current_widget.method_bottom_combo.currentText()
        if method_bottom_combo == '':
            QMessageBox.critical(self, 'Забой', 'Выберете метод определения забоя')
            return

        change_pvr_combo = current_widget.change_pvr_combo.currentText()
        if change_pvr_combo == '':
            QMessageBox.warning(self, 'Ошибка', 'Нужно выбрать пункт изменения ПВР')
            return
        if data_list.data_in_base:

            fluid = current_widget.fluid_edit.text().replace(',', '.')

            current_bottom = current_widget.current_bottom_edit.text()
            if current_bottom != '':
                current_bottom = round_cell(current_bottom.replace(',', '.'))

            work_earlier = current_widget.work_edit.toPlainText()
            number_dp = current_widget.number_DP_Combo.currentText()

            current_bottom_date_edit = current_widget.current_bottom_date_edit.text()

            template_depth_edit = current_widget.template_depth_edit.text()
            template_lenght_edit = current_widget.template_lenght_edit.text()
            if self.dict_data_well["column_additional"]:
                template_depth_addition_edit = current_widget.template_depth_addition_edit.text()
                template_lenght_addition_edit = current_widget.template_lenght_addition_edit.text()
            skm_interval_edit = current_widget.skm_interval_edit.text()
            raiding_interval_edit = current_widget.raiding_interval_edit.text()

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
            if float(template_depth_edit) > float(self.dict_data_well["bottomhole_drill"]._value):
                QMessageBox.critical(self, 'Забой', 'Шаблонирование не может быть ниже искусственного забоя забоя')
                return
            if number_dp != '':
                self.dict_data_well["number_dp"] = int(float(number_dp))

            if (0.87 <= float(fluid[:3].replace(',', '.')) <= 1.64) == False:
                QMessageBox.critical(self, 'рабочая жидкость',
                                           'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
                return

            if data_list.data_in_base:
                if 'г/см3' not in fluid:
                    QMessageBox.critical(self, 'уд.вес', 'нужно добавить значение "г/см3" в уд.вес')
                    return
                self.dict_data_well["fluid_work"] = fluid
                self.dict_data_well["fluid_work_short"] = fluid[:7]

                self.dict_data_well["fluid"] = float(fluid[:4].replace('г', ''))
            else:
                self.dict_data_well["fluid"] = float(fluid)

                if float(current_bottom) > self.dict_data_well["bottomhole_drill"]._value:
                    QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
                    return
                self.dict_data_well["fluid_work"], self.dict_data_well["fluid_work_short"] = self.calc_work_fluid(self, fluid)

            self.dict_data_well["template_depth"] = float(template_depth_edit)
            self.dict_data_well["template_lenght"] = float(template_lenght_edit)
            if self.dict_data_well["column_additional"]:
                self.dict_data_well["template_depth"] = float(template_depth_addition_edit)
                self.dict_data_well["template_lenght"] = float(template_lenght_addition_edit)

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

                self.dict_data_well["skm_interval"] = skm_interval_new

            except:
                QMessageBox.warning(self, 'Ошибка',
                                          'в интервале скреперования отсутствует корректные интервалы скреперования')
                return

            try:
                raiding_interval = []
                if ',' in raiding_interval_edit:
                    for skm in raiding_interval_edit.split(','):
                        if '-' in skm:
                            raiding_interval.append(list(map(int, skm.split('-'))))
                else:
                    if '-' in raiding_interval_edit:
                        raid = raiding_interval_edit.split('-')
                        raiding_interval.append(list(map(int,  raid)))

                raiding_interval_new = merge_overlapping_intervals(raiding_interval)

                self.dict_data_well["ribbing_interval"] = raiding_interval_new

            except Exception as e:
                QMessageBox.warning(self, 'Ошибка',
                                          f'в интервале райбирования отсутствует корректные интервалы '
                                          f' {e}')
                return

            if len(self.dict_data_well["skm_interval"]) == 0:
                mes = QMessageBox.question(self, 'Ошибка',
                                           'Интервалы скреперования отсутствуют, так ли это?')
                if mes == QMessageBox.StandardButton.No:
                    return

            if len(self.dict_data_well["ribbing_interval"]) == 0:
                mes = QMessageBox.question(self, 'Ошибка',
                                           'Интервалы Райбирования отсутствуют, так ли это?')
                if mes == QMessageBox.StandardButton.No:
                    return

            self.dict_data_well["count_template"] = 1
            well_data_in_base_combo = current_widget.well_data_in_base_combo.currentText()
            if well_data_in_base_combo == '':
                QMessageBox.critical(self, 'База данных', 'Необходимо выбрать план работ')
                return
            list_dop_plan = well_data_in_base_combo.split(' ')
            if list_dop_plan:
                if any([f'ДП№{number_dp}' in dop_plan or f'ДП№{number_dp}' in dop_plan for dop_plan in list_dop_plan]):
                    question = QMessageBox.question(self, 'Ошибка', f'дополнительный план работ № {number_dp} '
                                                                    f'есть в базе, обновить доп план?')
                    if question == QMessageBox.StandardButton.No:
                        return

            index_change_line = current_widget.index_change_line.text()
            well_number = current_widget.well_number_edit.text()
            well_area = current_widget.well_area_edit.text()
            if well_area != '' and well_area != '':
                self.well_number, self.dict_data_well["well_area"] = \
                    ProtectedIsNonNone(well_number), ProtectedIsNonNone(well_area)
            if index_change_line != '':
                index_change_line = int(float(index_change_line))
            else:
                QMessageBox.critical(self, 'пункт', 'Необходимо выбрать пункт плана работ')
                return


            self.dict_data_well["current_bottom"] = current_bottom

            if skm_interval_edit not in ['', 0, '0-0'] and '-' in skm_interval_edit:
                if ',' in skm_interval_edit:
                    for skm_int in skm_interval_edit.split(','):
                        self.dict_data_well["skm_interval"].append(list(map(int, skm_int.split('-'))))
                else:
                    self.dict_data_well["skm_interval"].append(list(map(int, skm_interval_edit.split('-'))))

            rows = self.tableWidget.rowCount()

            self.work_with_excel(well_number, well_area, list_dop_plan[3], list_dop_plan[2])
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
                data_list.data, data_list.rowHeights, data_list.colWidth, data_list.boundaries_dict = \
                    self.insert_row_in_pvr(self.data, self.rowHeights, self.colWidth, self.boundaries_dict, plast_row,
                                           current_bottom, current_bottom_date_edit, method_bottom_combo)
            else:

                data_list.data, data_list.rowHeights, data_list.colWidth, data_list.boundaries_dict = \
                    self.change_pvr_in_bottom(self.data, self.rowHeights, self.colWidth, self.boundaries_dict,
                                              current_bottom, current_bottom_date_edit, method_bottom_combo)
            if data_list.data_in_base:
                data_list.dop_work_list = self.work_list(work_earlier)
            else:
                work_list = self.work_list(work_earlier)
                self.populate_row(self.ins_ind + 3, work_list, self.table_widget, self.work_plan)

                if len(self.dict_perforation) != 0:
                    for plast, vertical_line,  roof_int, sole_int, date_pvr_edit, count_pvr_edit, \
                        type_pvr_edit, pressuar_pvr_edit, date_pressuar_edit in self.dict_perforation:
                        self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('отрайбировано', False)
                        self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('Прошаблонировано', False)

                        self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('интервал', []).append(
                            (float(roof_int), float(sole_int)))
                        self.dict_data_well["dict_perforation_short"].setdefault(plast, {}).setdefault('интервал', []).append(
                            (float(roof_int), float(sole_int)))
                        self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('отключение', False)
                        self.dict_data_well["dict_perforation_short"].setdefault(plast, {}).setdefault('отключение', False)

        else:
            fluid = current_widget.fluid_edit.text().replace(',', '.')
            current_bottom = current_widget.current_bottom_edit.text()
            if current_bottom != '':
                current_bottom = round_cell(current_bottom.replace(',', '.'))

            work_earlier = current_widget.work_edit.toPlainText()
            number_dp = current_widget.number_DP_Combo.currentText()

            template_depth_edit = current_widget.template_depth_edit.text()
            template_lenght_edit = current_widget.template_lenght_edit.text()
            if self.dict_data_well["column_additional"]:
                template_depth_addition_edit = current_widget.template_depth_addition_edit.text()
                template_lenght_addition_edit = current_widget.template_lenght_addition_edit.text()
            skm_interval_edit = current_widget.skm_interval_edit.text()
            try:

                if skm_interval_edit not in ['', 0, '0-0'] and '-' in skm_interval_edit:
                    if ',' in skm_interval_edit:
                        for skm_int in skm_interval_edit.split(','):
                            self.dict_data_well["skm_interval"].append(list(map(int, skm_int.split('-'))))
                    else:
                        self.dict_data_well["skm_interval"].append(list(map(int, skm_interval_edit.split('-'))))

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
                self.dict_data_well["number_dp"] = int(float(number_dp))

            if (0.87 <= float(fluid[:3].replace(',', '.')) <= 1.64) == False:
                QMessageBox.critical(self, 'рабочая жидкость',
                                           'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
                return

            # if float(current_bottom) > self.dict_data_well["bottomhole_drill"]._value:
            #     QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
            #     return
            self.dict_data_well["fluid_work"], self.dict_data_well["fluid_work_short"] = self.calc_work_fluid(self, fluid)

            self.dict_data_well["template_depth"] = float(template_depth_edit)
            self.dict_data_well["template_lenght"] = float(template_lenght_edit)
            if self.dict_data_well["column_additional"]:
                self.dict_data_well["template_depth"] = float(template_depth_addition_edit)
                self.dict_data_well["template_lenght"] = float(template_lenght_addition_edit)

            work_list = self.work_list(work_earlier)
            self.dict_data_well["ins_ind2"] = self.ins_ind + 2
            self.populate_row(self.ins_ind + 2, work_list, self.table_widget, self.work_plan)
            definition_plast_work(self)

        data_list.pause = False
        self.close()

    def add_work_excel(self, ws2, work_list, ind_ins):
        for i in range(1, len(work_list) + 1):  # Добавлением работ
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):

                    if i >= ind_ins:

                        if j != 1:
                            cell.border = data_list.thin_border
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
                            self.dict_data_well["ins_ind2"] = i + 1
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')

    def extraction_data(self, table_name, paragraph_row=0):


        date_table = table_name.split(' ')[-1]
        well_number = table_name.split(' ')[0]
        well_area = table_name.split(' ')[1]
        type_kr = table_name.split(' ')[2].replace('None', 'null')
        contractor = data_list.contractor
        work_plan = table_name.split(' ')[3]

        db = connection_to_database(data_list.DB_WELL_DATA)
        data_well_base = WorkDatabaseWell(db, self.dict_data_well)

        result_table = data_well_base.extraction_data(str(well_number), well_area, type_kr,
                                                      work_plan, date_table, contractor)

        if result_table is None:
            QMessageBox.warning(self, 'Ошибка',
                                f'В базе данных скв {well_number} {well_area} отсутствует данные, '
                                f'используйте excel вариант плана работ')
            return None

        if result_table[0]:
            result = json.loads(result_table[0])
            from data_base.work_with_base import insert_data_well_dop_plan
            insert_data_well_dop_plan(self, result_table[1])

            self.dict_data_well["type_kr"] = result_table[2]
            if result_table[3]:
                dict_data_well = json.loads(result_table[3])
                # self.dict_data_well["dict_category"]
                Pressuar = namedtuple("Pressuar", "category data_pressuar")
                Data_h2s = namedtuple("Data_h2s", "category data_procent data_mg_l poglot")
                Data_gaz = namedtuple("Data_gaz", "category data")
                self.dict_data_well['dict_category'] = {}


                for plast, plast_data in dict_data_well.items():
                    sfdfr = dict_data_well[plast]['по давлению']
                    self.dict_data_well['dict_category'].setdefault(plast, {}).setdefault(
                        'по давлению',
                        Pressuar(*dict_data_well[plast]['по давлению']))
                    self.dict_data_well['dict_category'].setdefault(plast, {}).setdefault(
                        'по сероводороду', Data_h2s(*dict_data_well[plast]['по сероводороду']))
                    self.dict_data_well['dict_category'].setdefault(plast, {}).setdefault(
                        'по газовому фактору', Data_gaz(*dict_data_well[plast]['по газовому фактору']))

                    self.dict_data_well['dict_category'].setdefault(plast, {}).setdefault(
                        'отключение', dict_data_well[plast]['отключение'])



            if self.dict_data_well["work_plan"] in ['dop_plan', 'dop_plan_in_base']:
                data = DopPlanWindow.insert_data_dop_plan(self, result, paragraph_row)
                if data is None:
                    return None
            elif self.dict_data_well["work_plan"] == 'plan_change':
                data = DopPlanWindow.insert_data_plan(self, result)
                if data is None:
                    return None
            data_list.data_well_is_True = True

        else:
            data_list.data_in_base = False
            QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                      f"Таблицы '{table_name}' нет в базе данных.")

        return True

    def insert_data_plan(self, result):
        self.dict_data_well["data_list"] = []
        self.dict_data_well["gips_in_well"] = False
        self.dict_data_well["drilling_interval"] = []
        self.dict_data_well["for_paker_list"] = False
        self.dict_data_well["grp_plan"] = False
        self.dict_data_well["angle_data"] = []
        self.dict_data_well["nkt_opress_true"] = False
        self.dict_data_well['plast_project'] = []
        self.dict_data_well["drilling_interval"] = []
        self.dict_data_well["dict_perforation_project"] = {}
        self.dict_data_well["bvo"] = False
        self.dict_data_well["fluid"] = float(result[0][7][:4].replace('г', ''))
        self.dict_data_well["stabilizator_true"] = False
        self.dict_data_well["current_bottom2"] = 0

        for ind, row in enumerate(result):
            if ind == 1:
                self.dict_data_well["bottom"] = row[1]
                self.dict_data_well["category_pressuar2"] = row[8]
                self.dict_data_well["category_h2s_2"] = row[9]
                self.dict_data_well["gaz_f_pr_2"] = row[10]

                self.dict_data_well['plast_work_short'] = json.dumps(row[3], ensure_ascii=False)

            data_list = []
            for index, data in enumerate(row):
                if index == 6:
                    if data == 'false' or data == 0 or data == '0':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            self.dict_data_well["data_list"].append(data_list)
        self.dict_data_well["current_bottom"] = result[ind][1]
        self.dict_data_well["dict_perforation"] = json.loads(result[ind][2])

        self.dict_data_well['plast_all'] = json.loads(result[ind][3])
        self.dict_data_well['plast_work'] = json.loads(result[ind][4])
        self.dict_data_well["dict_leakiness"] = json.loads(result[ind][5])
        self.dict_data_well["leakiness"] = False
        self.dict_data_well["leakiness_interval"] = []
        if self.dict_data_well["dict_leakiness"]:
            self.dict_data_well["leakiness"] = True
            self.dict_data_well["leakiness_interval"] = list(self.dict_data_well["dict_leakiness"]['НЭК'].keys())

        self.dict_data_well["dict_perforation_short"] = json.loads(result[ind][2])

        self.dict_data_well["category_pressuar"] = result[ind][8]
        self.dict_data_well["category_h2s"] = result[ind][9]
        self.dict_data_well["category_gf"] = result[ind][10]
        if str(result[ind][8]) == '1' or str(result[ind][9]) == '1' or str(result[ind][10]) or '1':
            self.dict_data_well["bvo"] = True

        definition_plast_work(self)
        return True
    def insert_data_dop_plan(self, result, paragraph_row):
        self.dict_data_well['plast_project'] = []
        self.dict_data_well["dict_perforation_project"] = {}
        self.dict_data_well["data_list"] = []
        self.dict_data_well["gips_in_well"] = False
        self.dict_data_well["drilling_interval"] = []
        self.dict_data_well["for_paker_list"] = False
        self.dict_data_well["grp_plan"] = False
        self.dict_data_well["angle_data"] = []
        self.dict_data_well["nkt_opress_true"] = False
        self.dict_data_well["bvo"] = False
        self.dict_data_well["stabilizator_true"] = False
        self.dict_data_well["current_bottom2"] = 0

        paragraph_row = paragraph_row - 1

        if len(result) <= paragraph_row:
            QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пунктов')
            return

        self.dict_data_well["current_bottom"] = result[paragraph_row][1]

        self.dict_data_well["dict_perforation"] = json.loads(result[paragraph_row][2])

        self.dict_data_well['plast_all'] = json.loads(result[paragraph_row][3])
        self.dict_data_well['plast_work'] = json.loads(result[paragraph_row][4])
        self.dict_data_well["dict_leakiness"] = json.loads(result[paragraph_row][5])
        self.dict_data_well["leakiness"] = False
        self.dict_data_well["leakiness_interval"] = []
        if self.dict_data_well["dict_leakiness"]:
            self.dict_data_well["leakiness"] = True
            self.dict_data_well["leakiness_interval"] = list(self.dict_data_well["dict_leakiness"]['НЭК'].keys())

        if result[paragraph_row][6] == 'true':
            self.dict_data_well["column_additional"] = True
        else:
            self.dict_data_well["column_additional"] = False

        self.dict_data_well["fluid_work"] = result[paragraph_row][7]

        self.dict_data_well["category_pressuar"] = result[paragraph_row][8]
        self.dict_data_well["category_h2s"] = result[paragraph_row][9]
        self.dict_data_well["category_gf"] = result[paragraph_row][10]
        self.dict_data_well["kat_pvo"] = 2
        if str(self.dict_data_well["category_pressuar"]) == '1' or str(self.dict_data_well["category_h2s"]) == '1' \
                or self.dict_data_well["category_gf"] == '1':
            self.dict_data_well["kat_pvo"] = 1
        try:
            self.dict_data_well["template_depth"], self.dict_data_well["template_lenght"], \
            self.dict_data_well["template_depth_addition"], \
            self.dict_data_well["template_lenght_addition"] = json.loads(result[paragraph_row][11])
        except:
            self.dict_data_well["template_depth"] = result[paragraph_row][11]
        self.dict_data_well["skm_interval"] = json.loads(result[paragraph_row][12])

        self.dict_data_well["problem_with_ek_depth"] = result[paragraph_row][13]
        self.dict_data_well["problem_with_ek_diametr"] = result[paragraph_row][14]
        self.dict_data_well["dict_perforation_short"] = json.loads(result[paragraph_row][2])

        try:

            self.dict_data_well["ribbing_interval"] = json.loads(result[paragraph_row][15])
        except:
            pass

        definition_plast_work(self)
        return True

    def work_list(self, work_earlier):
        krs_begin = [[None, None,
                      f' Ранее проведенные работ: \n {work_earlier}',
                      None, None, None, None, None, None, None,
                      'Мастер КРС', None]]

        return krs_begin


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()

    window = DopPlanWindow(1, 1, 1)
    window.show()
    sys.exit(app.exec_())
