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
from work_py.advanted_file import merge_overlapping_intervals, definition_plast_work
from main import MyMainWindow
from .dop_plan_py import DopPlanWindow




class TabPageDp(QWidget):
    def __init__(self, work_plan, tableWidget, old_index):
        super().__init__()
        self.validator_int = QIntValidator(0, 8000)

        self.tableWidget = tableWidget
        self.old_index = old_index

        self.work_plan = work_plan

        self.well_number_label = QLabel('номер скважины')
        self.well_number_edit = QLineEdit(self)
        # self.well_number_edit.setValidator(self.validator_int)

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
            self.well_data_label = QLabel('файл excel')
            self.well_data_in_base_combo = QComboBox()
            self.well_data_in_base_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

            self.grid.addWidget(self.well_data_label, 2, 6)
            self.grid.addWidget(self.well_data_in_base_combo, 3, 6)

            self.well_data_in_base_combo.currentIndexChanged.connect(self.update_area)

    def update_area(self):

        table_in_base_combo = self.well_data_in_base_combo.currentText()
        well_area = table_in_base_combo.split(" ")[1]
        self.well_area_edit.setText(well_area)
        self.well_number_edit.setText(table_in_base_combo.split(" ")[0])



    def update_well(self):
        from .dop_plan_py import TabPageDp

        if well_data.data_in_base:

            well_list =TabPageDp.check_in_database_well_data(self, self.well_number_edit.text())

            if well_list:
                self.well_data_in_base_combo.clear()
                self.well_data_in_base_combo.addItems(well_list)


class TabWidget(QTabWidget):
    def __init__(self, work_plan, tableWidget=0, old_index=0):
        super().__init__()
        self.addTab(TabPageDp(work_plan, tableWidget, old_index), 'Корректировка плана работ')


class CorrectPlanWindow(MyMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, ws=None, parent=None):

        super(CorrectPlanWindow, self).__init__()
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

    # def read_excel_in_base(self, number_well, area_well, work_plan):
    #     if well_data.connect_in_base:
    #         conn = psycopg2.connect(**well_data.postgres_params_data_well)
    #         cursor = conn.cursor()
    #
    #
    #         cursor.execute("SELECT excel_json FROM wells WHERE well_number = %s AND area_well = %s "
    #                        "AND contractor = %s AND costumer = %s AND work_plan = %s",
    #                        (str(number_well), area_well, well_data.contractor, well_data.costumer, work_plan))
    #
    #         data_well = cursor.fetchall()
    #
    #         if cursor:
    #             cursor.close()
    #         if conn:
    #             conn.close()
    #
    #     else:
    #         db_path = connect_to_db('well_data.db', 'data_base_well/')
    #
    #         conn = sqlite3.connect(f'{db_path}')
    #         cursor = conn.cursor()
    #
    #         cursor.execute("SELECT excel_json FROM wells WHERE well_number = ? AND area_well = ? "
    #                        "AND contractor = ? AND costumer = ?",
    #                        (str(number_well), area_well, well_data.contractor, well_data.costumer))
    #         data_well = cursor.fetchall()
    #         if cursor:
    #             cursor.close()
    #         if conn:
    #             conn.close()
    #     try:
    #         dict_well = json.loads(data_well[len(data_well) - 1][0])
    #         data = dict_well['data']
    #         rowHeights = dict_well['rowHeights']
    #         colWidth = dict_well['colWidth']
    #         boundaries_dict = dict_well['merged_cells']
    #
    #     except Exception as e:
    #         QMessageBox.warning(self, 'Ошибка', f'Введены не все параметры {type(e).__name__}\n\n{str(e)}')
    #         return
    #
    #     return data, rowHeights, colWidth, boundaries_dict

    def add_work(self):
        from data_base.work_with_base import check_in_database_well_data, insert_data_well_dop_plan, round_cell
        from work_py.dop_plan_py import DopPlanWindow

        from well_data import ProtectedIsNonNone

        well_number = self.tabWidget.currentWidget().well_number_edit.text()
        well_area = self.tabWidget.currentWidget().well_area_edit.text()

        if well_data.data_in_base:
            data_well_data_in_base_combo, data_table_in_base_combo = '', ''

            well_data_in_base_combo = self.tabWidget.currentWidget().well_data_in_base_combo.currentText()

            if ' от' in well_data_in_base_combo:
                data_well_data_in_base_combo = well_data_in_base_combo.split(' ')[-1]
                well_data_in_base = well_data_in_base_combo.split(' ')[3]
                if 'ДП' in well_data_in_base:
                    well_data.number_dp = ''.join(filter(str.isdigit, well_data_in_base))
                    well_data.work_plan_change = 'dop_plan'
                else:
                    well_data.work_plan_change = 'krs'

            data_well = check_in_database_well_data(well_number, well_area, well_data_in_base)

            if data_well:
                well_data.type_kr = data_well[2]

                if data_well[3]:
                    well_data.dict_category = json.loads(data_well[3])
                    aaaa = well_data.dict_category
                insert_data_well_dop_plan(data_well[0])

            DopPlanWindow.work_with_excel(self, well_number, well_area, well_data_in_base, well_data.type_kr)

            well_data.data, well_data.rowHeights, well_data.colWidth, well_data.boundaries_dict = \
                DopPlanWindow.change_pvr_in_bottom(self, self.data, self.rowHeights, self.colWidth,
                                                   self.boundaries_dict)

            DopPlanWindow.extraction_data(self, well_data_in_base_combo)
            if well_area != '' and well_area != '':
                well_data.well_number, well_data.well_area = \
                    ProtectedIsNonNone(well_number), ProtectedIsNonNone(well_area)

            well_data.pause = False
            self.close()
    # @staticmethod
    # def delete_data(number_well, area_well, work_plan):
    #     if well_data.connect_in_base:
    #         try:
    #             conn = psycopg2.connect(**well_data.postgres_params_data_well)
    #             cursor = conn.cursor()
    #
    #             cursor.execute("""
    #             DELETE FROM wells
    #             WHERE well_number = %s AND area_well = %s AND contractor = %s AND costumer = %s AND work_plan= %s """,
    #                            (str(number_well), area_well, well_data.contractor, well_data.costumer, work_plan)
    #                            )
    #
    #             conn.commit()
    #             cursor.close()
    #             conn.close()
    #
    #         except psycopg2.Error as e:
    #             # Выведите сообщение об ошибке
    #             QMessageBox.warning(None, 'Ошибка',
    #                                       f'Ошибка удаления {type(e).__name__}\n\n{str(e)}')
    #     else:
    #         try:
    #             db_path = connect_to_db('well_data.db', 'data_base_well/')
    #
    #             conn = sqlite3.connect(f'{db_path}')
    #             cursor = conn.cursor()
    #
    #             cursor.execute("DELETE FROM wells  WHERE well_number = ? AND area_well = ? "
    #                            "AND contractor = ? AND costumer = ? AND work_plan=?",
    #                            (str(number_well._value), area_well._value, well_data.contractor, well_data.costumer,
    #                             work_plan))
    #
    #             conn.commit()
    #             cursor.close()
    #             conn.close()
    #
    #         except sqlite3.Error as e:
    #             # Выведите сообщение об ошибке
    #             QMessageBox.warning(None, 'Ошибка',
    #                                       f'Ошибка удаления {type(e).__name__}\n\n{str(e)}')
    @staticmethod
    def add_work_excel(ws2, work_list, ind_ins):
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

        well_data.fluid_work_short = well_data.fluid_work_short

    def work_list(self, work_earlier):
        krs_begin = [[None, None,
                      f' Ранее проведенные работ: \n {work_earlier}',
                      None, None, None, None, None, None, None,
                      'Мастер КРС', None]]

        return krs_begin
