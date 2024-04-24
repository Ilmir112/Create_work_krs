import json
import os
import sqlite3
import sys
import win32com.client
import openpyxl
import re

from PyQt5.QtGui import QColor
from openpyxl.reader.excel import load_workbook

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, \
    QLineEdit, QFileDialog, QToolBar, QPushButton, QMessageBox, QInputDialog, QTabWidget, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from openpyxl.utils import get_column_letter
from PyQt5.QtCore import Qt
from openpyxl.workbook import Workbook
from openpyxl.styles import Border, Side, Alignment, Font

import property_excel.property_excel_pvr
from work_py.advanted_file import count_row_height, definition_plast_work, raid, remove_overlapping_intervals

from openpyxl.drawing.image import Image

import well_data
from H2S import calc_h2s
from PyQt5.QtCore import QThread, pyqtSignal
from data_correct_position_people import CorrectSignaturesWindow
from work_py.dop_plan_py import DopPlanWindow
from work_py.drilling import Drill_window
from users.login_users import LoginWindow


class ExcelWorker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def check_well_existence(self, well_number, deposit_area, region):

        # Подключение к базе данных SQLite
        conn = sqlite3.connect('data_base/database_without_juming.db')
        cursor = conn.cursor()
        current_year = datetime.now().year
        month = datetime.now().month
        # print(f'месяц {month}')
        if 1 <= month < 4:
            date_string = datetime(current_year, 1, 1).strftime('%d.%m.%Y')
            print(f'Корректная таблица перечня без глушения от {date_string}')
        elif 4 <= month < 7:
            date_string = datetime(current_year, 4, 1).strftime('%d.%m.%Y')
            print(f'Корректная таблица перечня без глушения от {date_string}')
        elif 7 <= month < 10:
            date_string = datetime(current_year, 7, 1).strftime('%d.%m.%Y')
            print(f'Корректная таблица перечня без глушения от {date_string}')
        elif 10 >= month <= 12:
            date_string = datetime(current_year, 10, 1).strftime('%d.%m.%Y')
            print(f'Корректная таблица перечня без глушения от {date_string}')
        print(f' регион {region}')

        if region == 'КГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM КГМ WHERE today =?", (date_string,))
            print(f' база данных открыта')
            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(self, 'Некорректная дата перечня',
                                          f'Необходимо обновить перечень скважин без '
                                          f'глушения на текущий квартал {region}')
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT * FROM КГМ WHERE well_number=? AND deposit_area=?", (well_number, deposit_area))
            result = cursor.fetchone()
            # Закрытие соединения с базой данных
            conn.close()
            print(f' база данных закрыта')

            # Если запись найдена, возвращается True, в противном случае возвращается False
            if result:

                mes = QMessageBox.information(None, 'перечень без глушения',
                                              f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                                              f'в перечне от  {region}')

                check_true = True
            else:
                check_true = False

        if region == 'ЧГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM ЧГМ WHERE today =?", (date_string,))
            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(self, 'Некорректная дата перечня',
                                          f'Необходимо обновить перечень скважин без глушения на текущий квартал {region}')
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT * FROM ЧГМ WHERE well_number=? AND deposit_area=?", (well_number, deposit_area))
            result = cursor.fetchone()
            # Закрытие соединения с базой данных
            conn.close()

            # Если запись найдена, возвращается True, в противном случае возвращается False
            if result:
                date_reload = result[2]
                mes = QMessageBox.information(self, 'перечень без глушения',
                                              f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                                              f'в перечне от {date_reload} {region}')
                check_true = True
            else:
                check_true = False

        if region == 'ТГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM ТГМ WHERE today =?", (date_string,))
            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(self, 'Некорректная дата перечня',
                                          'Необходимо обновить перечень скважин без глушения на текущий квартал')

            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT * FROM ТГМ WHERE well_number=? AND deposit_area=?", (well_number, deposit_area))
            result = cursor.fetchone()

            # Закрытие соединения с базой данных
            conn.close()
            # Если запись найдена, возвращается True, в противном случае возвращается False
            if result:
                date_reload = result[2]
                # mes = QMessageBox.information(self, 'перечень без глушения',
                #                               f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                #                               f'в перечне от {date_reload} {region}')
                check_true = True
            else:
                check_true = False

        if region == 'ИГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM ИГМ WHERE today =?", (date_string,))

            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(None, 'Некорректная дата перечня',
                                          'Необходимо обновить перечень скважин без глушения на текущий квартал')
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT * FROM ИГМ WHERE well_number=? AND deposit_area=?", (well_number, deposit_area))
            result = cursor.fetchone()
            # Закрытие соединения с базой данных
            conn.close()

            # Если запись найдена, возвращается True, в противном случае возвращается False
            if result:
                date_reload = result[2]
                mes = QMessageBox.information(None, 'перечень без глушения',
                                              f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                                              f'в перечне от {date_reload} {region}')

                check_true = True
            else:
                check_true = False

        if region == 'АГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM АГМ WHERE today =?", (date_string,))
            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(self, 'Некорректная дата перечня',
                                          'Необходимо обновить перечень скважин без глушения на текущий квартал')
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT * FROM АГМ WHERE well_number=? AND deposit_area=?", (well_number, deposit_area))
            result = cursor.fetchone()
            # Закрытие соединения с базой данных
            conn.close()

            # Если запись найдена, возвращается True, в противном случае возвращается False
            if result:
                date_reload = result[2]
                mes = QMessageBox.information(None, 'перечень без глушения',
                                              f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                                              f'в перечне от {date_reload} {region}')

                check_true = True
            else:
                check_true = False

        # Завершение работы потока
        self.finished.emit()
        return check_true

    def check_category(self, well_number, deposit_area, region):
        # Подключение к базе данных SQLite
        conn = sqlite3.connect('data_base/database_without_juming.db')
        cursor = conn.cursor()
        # print(well_number._value, deposit_area._value, region)
        # Подключение к базе данных SQLite)

        if region == 'КГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM КГМ_классификатор "
                           f"WHERE well_number = ? and deposit_area = ?", (well_number._value, deposit_area._value))

        elif region == 'АГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM АГМ_классификатор "
                           f"WHERE well_number = ? and deposit_area = ?", (well_number._value, deposit_area._value))

        elif region == 'ИГМ':
            print(f'ркатг')
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM ИГМ_классификатор "
                           f"WHERE well_number = ? and deposit_area = ?", (well_number._value, deposit_area._value))

        elif region == 'ТГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM ТГМ_классификатор "
                           f"WHERE well_number = ? and deposit_area = ?", (well_number._value, deposit_area._value))

        elif region == 'ЧГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT categoty_pressure, categoty_h2s, categoty_gf, today FROM ЧГМ_классификатор "
                           f"WHERE well_number = ? and deposit_area = ?", (well_number._value, deposit_area._value))

        result = cursor.fetchone()
        # print(result)
        # Закрытие соединения с базой данных
        conn.close()
        # # Завершение работы потока
        # ExcelWorker.finished.emit()
        return result


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.login_window = None
        self.new_window = None
        self.raid_window = None
        self.leakage_window = None
        self.correct_window = None
        self.acid_windowPaker = None
        self.work_window = None
        self.signatures_window = None
        self.acid_windowPaker2 = None
        self.rir_window = None
        self.data_window = None
        self.filter_widgets = []
        self.table_class = None
        self.table_juming = None

        self.perforation_correct_window2 = None
        self.ws = None
        self.ins_ind = None
        self.perforation_list = []
        self.dict_perforation_project = {}

        self.ins_ind_border = None
        self.work_plan = 0
        self.table_widget = None
        self.table_pvr = None

        if self.login_window == None:
            self.login_window = LoginWindow()
            self.login_window.show()
            self.pause_app()
            well_data.pause = False

    def initUI(self):

        self.setWindowTitle("Main Window")
        self.setGeometry(200, 100, 800, 800)

        self.createMenuBar()
        self.le = QLineEdit()

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.saveFileButton = QPushButton("Сохранить проект")
        self.saveFileButton.clicked.connect(self.save_to_excel)
        self.toolbar.addWidget(self.saveFileButton)

        self.correctDataButton = QPushButton("Скорректировать данные")
        self.correctDataButton.clicked.connect(self.correctData)
        self.toolbar.addWidget(self.correctDataButton)

        self.correctPVRButton = QPushButton("Скорректировать работающие ПВР")
        self.correctPVRButton.clicked.connect(self.correctPVR)
        self.toolbar.addWidget(self.correctPVRButton)

        self.closeFileButton = QPushButton("Закрыть проект")
        self.closeFileButton.clicked.connect(self.close_file)
        self.toolbar.addWidget(self.closeFileButton)

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.fileMenu = QMenu('&Файл', self)
        self.application_geophysical = QMenu('&Заявка на ГИС', self)
        self.classifierMenu = QMenu('&Классификатор', self)
        self.signatories = QMenu('&Подписанты ', self)
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.application_geophysical)
        self.menuBar.addMenu(self.classifierMenu)
        self.menuBar.addMenu(self.signatories)

        self.application_pvr = self.application_geophysical.addAction('Заявка на ПВР', self.action_clicked)
        self.application_gis = self.application_geophysical.addAction('Заявка на ГИС', self.action_clicked)

        self.create_file = self.fileMenu.addMenu('&Создать')
        self.create_KRS = self.create_file.addAction('План КРС', self.action_clicked)
        self.create_KRS_DP = self.create_file.addAction('Дополнительный план', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_GNKT_OPZ = self.create_GNKT.addAction(' ГНКТ ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('ГНКТ Фрезерование', self.action_clicked)
        self.create_GNKT_GRP = self.create_GNKT.addAction('Освоение после ГРП', self.action_clicked)
        self.create_PRS = self.create_file.addAction('План ПРС', self.action_clicked)
        self.open_file = self.fileMenu.addAction('Открыть', self.action_clicked)
        self.save_file = self.fileMenu.addAction('Сохранить', self.action_clicked)
        self.save_file_as = self.fileMenu.addAction('Сохранить как', self.action_clicked)

        self.class_well = self.classifierMenu.addMenu('&ООО Башнефть-Добыча')
        self.costumer_class_well = self.class_well.addMenu('Классификатор')
        self.costumer_select = self.class_well.addMenu('Перечень скважин без глушения')

        self.class_well_TGM = self.costumer_class_well.addMenu('&Туймазинский регион')
        self.class_well_TGM_open = self.class_well_TGM.addAction('&открыть перечень', self.action_clicked)
        self.class_well_TGM_reload = self.class_well_TGM.addAction('&обновить', self.action_clicked)

        self.class_well_IGM = self.costumer_class_well.addMenu('&Ишимбайский регион')
        self.class_well_IGM_open = self.class_well_IGM.addAction('&открыть перечень', self.action_clicked)
        self.class_well_IGM_reload = self.class_well_IGM.addAction('&обновить', self.action_clicked)

        self.class_well_CHGM = self.costumer_class_well.addMenu('&Чекмагушевский регион')
        self.class_well_CHGM_open = self.class_well_CHGM.addAction('&открыть перечень', self.action_clicked)
        self.class_well_CHGM_reload = self.class_well_CHGM.addAction('&обновить', self.action_clicked)

        self.class_well_KGM = self.costumer_class_well.addMenu('&Краснохолмский регион')
        self.class_well_KGM_open = self.class_well_KGM.addAction('&открыть перечень', self.action_clicked)
        self.class_well_KGM_reload = self.class_well_KGM.addAction('&обновить', self.action_clicked)

        self.class_well_AGM = self.costumer_class_well.addMenu('&Арланский регион')
        self.class_well_AGM_open = self.class_well_AGM.addAction('&открыть перечень', self.action_clicked)
        self.class_well_AGM_reload = self.class_well_AGM.addAction('&обновить', self.action_clicked)

        self.without_jamming_TGM = self.costumer_select.addMenu('&Туймазинский регион')
        self.without_jamming_TGM_open = self.without_jamming_TGM.addAction('&открыть перечень', self.action_clicked)
        self.without_jamming_TGM_reload = self.without_jamming_TGM.addAction('&обновить', self.action_clicked)

        self.without_jamming_IGM = self.costumer_select.addMenu('&Ишимбайский регион')
        self.without_jamming_IGM_open = self.without_jamming_IGM.addAction('&открыть перечень', self.action_clicked)
        self.without_jamming_IGM_reload = self.without_jamming_IGM.addAction('&обновить', self.action_clicked)

        self.without_jamming_CHGM = self.costumer_select.addMenu('&Чекмагушевский регион')
        self.without_jamming_CHGM_open = self.without_jamming_CHGM.addAction('&открыть перечень', self.action_clicked)
        self.without_jamming_CHGM_reload = self.without_jamming_CHGM.addAction('&обновить', self.action_clicked)

        self.without_jamming_KGM = self.costumer_select.addMenu('&Краснохолмский регион')
        self.without_jamming_KGM_open = self.without_jamming_KGM.addAction('&открыть перечень', self.action_clicked)
        self.without_jamming_KGM_reload = self.without_jamming_KGM.addAction('&обновить', self.action_clicked)

        self.without_jamming_AGM = self.costumer_select.addMenu('&Арланский регион')
        self.without_jamming_AGM_open = self.without_jamming_AGM.addAction('&открыть перечень', self.action_clicked)
        self.without_jamming_AGM_reload = self.without_jamming_AGM.addAction('&обновить', self.action_clicked)

        self.signatories_Bnd = self.signatories.addAction('&БашНефть-Добыча', self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        from open_pz import CreatePZ
        from work_py.gnkt_frez import Work_with_gnkt
        from work_py.gnkt_grp import GnktOsvWindow
        from application_pvr import PvrApplication
        action = self.sender()
        if action == self.create_KRS:
            self.work_plan = 'krs'
            self.tableWidgetOpen(self.work_plan)
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.copy_pz(sheet, self.table_widget, self.work_plan)

                except FileNotFoundError:
                    print('Файл не найден')
        elif action == self.create_KRS_DP:
            self.work_plan = 'dop_plan'
            self.tableWidgetOpen(self.work_plan)
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.copy_pz(sheet, self.table_widget, self.work_plan)

                except FileNotFoundError:
                    print('Файл не найден')

        elif action == self.create_GNKT_OPZ:
            self.work_plan = 'gnkt_opz'

            self.tableWidgetOpen(self.work_plan)

            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.rir_window = GnktOsvWindow(self.ws,
                                                    self.table_title, self.table_schema, self.table_widget, self.work_plan)

                    self.pause_app()
                    well_data.pause = True
                    # self.copy_pz(sheet)

                except FileNotFoundError:
                    print('Файл не найден')

        elif action == self.create_GNKT_GRP:
            self.work_plan = 'gnkt_after_grp'
            self.tableWidgetOpen(self.work_plan)

            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)
                    self.rir_window = GnktOsvWindow(self.ws,
                                                    self.table_title, self.table_schema, self.table_widget,
                                                    self.work_plan)

                    self.pause_app()
                    well_data.pause = True
                    # self.copy_pz(sheet)

                except FileNotFoundError:
                    print('Файл не найден')

        elif action == self.create_GNKT_frez:
            self.work_plan = 'gnkt_frez'
            self.tableWidgetOpen(self.work_plan)

            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.rir_window = Work_with_gnkt(self.ws, self.table_title, self.table_schema, self.table_widget)

                    self.pause_app()
                    well_data.pause = True
                    # self.copy_pz(sheet)

                except FileNotFoundError:
                    print('Файл не найден')

                # if action == self.save_file:
                #     open_pz.open_excel_file().wb.save("test_unmerge.xlsx")


        elif action == self.save_file:
            self.save_to_excel

        elif action == self.save_file_as:
            self.saveFileDialog(self.wb2)

        elif action == self.signatories_Bnd:
            if self.signatures_window is None:
                self.signatures_window = CorrectSignaturesWindow()
                self.signatures_window.setWindowTitle("Подписанты")
                self.signatures_window.setGeometry(200, 400, 300, 400)
                self.signatures_window.show()

        elif action == self.without_jamming_TGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_without_damping(costumer, 'ТГМ')
        elif action == self.without_jamming_IGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_without_damping(costumer, 'ИГМ')
        elif action == self.without_jamming_CHGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_without_damping(costumer, 'ЧГМ')
        elif action == self.without_jamming_KGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_without_damping(costumer, 'КГМ')
        elif action == self.without_jamming_AGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_without_damping(costumer, 'АГМ')

        elif action == self.without_jamming_TGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_without_damping(costumer, 'ТГМ')
        elif action == self.without_jamming_IGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_without_damping(costumer, 'ИГМ')
        elif action == self.without_jamming_CHGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_without_damping(costumer, 'ЧГМ')
        elif action == self.without_jamming_KGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_without_damping(costumer, 'КГМ')
        elif action == self.without_jamming_AGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_without_damping(costumer, 'АГМ')


        elif action == self.class_well_TGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_class_well(costumer, 'ТГМ')

        elif action == self.class_well_IGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_class_well(costumer, 'ИГМ')
        elif action == self.class_well_CHGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_class_well(costumer, 'ЧГМ')
        elif action == self.class_well_KGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_class_well(costumer, 'КГМ')
        elif action == self.class_well_AGM_reload:
            costumer = 'ООО Башнефть-добыча'
            self.reload_class_well(costumer, 'АГМ')

        elif action == self.class_well_TGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_class_well(costumer, 'ТГМ')
        elif action == self.class_well_IGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_class_well(costumer, 'ИГМ')
        elif action == self.class_well_CHGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_class_well(costumer, 'ЧГМ')
        elif action == self.class_well_KGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_class_well(costumer, 'КГМ')
        elif action == self.class_well_AGM_open:
            costumer = 'ООО Башнефть-добыча'
            self.open_class_well(costumer, 'АГМ')
        elif action == self.application_pvr:
            self.work_plan = 'application_pvr'
            # self.tableWidgetOpenPvr()
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                self.open_pvr_application(self.fname)
        elif action == self.application_gis:
            self.work_plan = 'application_gis'
            # self.tableWidgetOpenPvr()
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                self.open_pvr_application(self.fname)


        elif action == self.application_geophysical:
            pass

    def reload_class_well(self, costumer, region):
        from data_base.work_with_base import Classifier_well
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                              "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if self.fname:
            try:
                copy = Classifier_well.export_to_sqlite_class_well(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    def open_without_damping(self, costumer, region):
        from data_base.work_with_base import Classifier_well

        if self.new_window is None:

            self.new_window = Classifier_well(costumer, region, 'damping')
            self.new_window.setWindowTitle("Перечень скважин без глушения")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def open_pvr_application(self, fname):
        from open_pz import CreatePZ
        from application_gis import GisApplication
        if fname:
            # try:
            self.read_pz(fname)
            well_data.pause = True
            read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
            sheet = read_pz.open_excel_file(self.ws, self.work_plan)
            self.rir_window = GisApplication(self.table_pvr)
            self.rir_window.show()

            self.pause_app()
            well_data.pause = False
            # except:
            #     pass

    def open_class_well(self, costumer, region):
        from data_base.work_with_base import Classifier_well
        if self.new_window is None:

            self.new_window = Classifier_well(costumer, region, 'classifier_well')
            self.new_window.setWindowTitle("Классификатор")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def reload_without_damping(self, costumer, region):
        from data_base.work_with_base import Classifier_well
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                              "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if self.fname:
            try:
                copy = Classifier_well.export_to_sqlite_without_juming(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    def tableWidgetOpenPvr(self):

        if self.table_pvr is None:
            # Создание объекта TabWidget
            self.tabWidget = QTabWidget()
            self.table_pvr = QTableWidget()

            self.table_pvr.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_pvr.customContextMenuRequested.connect(self.openContextMenu)
            self.setCentralWidget(self.tabWidget)
            self.model = self.table_pvr.model()

            # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
            # Указанная строка и столбец - это ячейка, которая была нажата.
            self.table_pvr.cellPressed[int, int].connect(self.clickedRowColumn)

            if self.work_plan == 'application_pvr':
                self.tabWidget.addTab(self.table_pvr, 'заявка на ПВР')

    def tableWidgetOpen(self, work_plan='krs'):

        if self.table_widget is None:

            # Создание объекта TabWidget
            self.tabWidget = QTabWidget()
            self.table_widget = QTableWidget()
            self.table_pvr = QTableWidget()

            self.table_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_widget.customContextMenuRequested.connect(self.openContextMenu)
            self.setCentralWidget(self.tabWidget)
            self.model = self.table_widget.model()

            # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
            # Указанная строка и столбец - это ячейка, которая была нажата.
            self.table_widget.cellPressed[int, int].connect(self.clickedRowColumn)
            if work_plan in ['gnkt_frez', 'gnkt_after_grp', 'gnkt_opz']:
                self.table_title = QTableWidget()
                self.tabWidget.addTab(self.table_title, 'Титульник')
                self.table_schema = QTableWidget()
                self.tabWidget.addTab(self.table_schema, 'Схема скважины')
                self.tabWidget.addTab(self.table_widget, 'Ход работ')

            else:
                self.tabWidget.addTab(self.table_widget, 'Ход работ')

    def saveFileDialog(self, wb2, full_path):
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save excel-file",
                                                      f"{full_path}", "Excel Files (*.xlsx)")
            if fileName:
                wb2.save(full_path)
            # Создаем объект Excel
            excel = win32com.client.Dispatch("Excel.Application")
        except:
            mes = QMessageBox.critical(self, 'Ошибка', 'файл под таким именем открыт, закройте его')
        try:
            # Открываем файл
            workbook = excel.Workbooks.Open(full_path)
            # Выбираем активный лист
            worksheet = workbook.ActiveSheet

            # Назначаем область печати с колонок B до L
            worksheet.PageSetup.PrintArea = "B:L"

        except Exception as e:
            print(f"Ошибка при работе с Excel: {e}")

    def save_to_excel(self):
        from work_py.gnkt_frez import Work_with_gnkt
        from work_py.gnkt_grp import GnktOsvWindow

        if self.work_plan in ['gnkt_frez']:
            Work_with_gnkt.save_to_gnkt(self)
        elif self.work_plan in ['gnkt_after_grp', 'gnkt_opz']:
            GnktOsvWindow.save_to_gnkt(self)
        else:
            self.save_to_krs()

    def save_to_krs(self):
        from open_pz import CreatePZ
        from work_py.alone_oreration import is_number
        from data_base.work_with_base import create_database_well_db

        if not self.table_widget is None:
            wb2 = Workbook()
            ws2 = wb2.get_sheet_by_name('Sheet')
            ws2.title = "План работ"

            ins_ind = self.ins_ind_border

            merged_cells = []  # Список индексов объединения ячеек

            work_list = []
            for row in range(self.table_widget.rowCount()):
                row_lst = []
                # self.ins_ind_border += 1
                for column in range(self.table_widget.columnCount()):
                    if self.table_widget.rowSpan(row, column) > 1 or self.table_widget.columnSpan(row, column) > 1:
                        merged_cells.append((row, column))
                    item = self.table_widget.item(row, column)
                    if not item is None:
                        if 'Нормы времени' in item.text():
                            ins_ind = row
                        if self.check_str_isdigit(item.text()):
                            row_lst.append(item.text().replace(',', '.'))
                        else:
                            row_lst.append(item.text())

                    else:
                        row_lst.append("")

                work_list.append(row_lst)
            create_database_well_db(self.work_plan, well_data.number_dp)
            merged_cells_dict = {}
            # print(f' индекс объ {ins_ind}')
            for row in merged_cells:
                if row[0] >= ins_ind - 1:
                    merged_cells_dict.setdefault(row[0], []).append(row[1])
            plan_short = ''

            for i in range(1, len(work_list)):  # нумерация работ

                if i >= ins_ind + 1:
                    work_list[i][1] = i - ins_ind
                    if is_number(work_list[i][11]) is True:
                        well_data.normOfTime += float(str(work_list[i][11]).replace(',', '.'))
                    if work_list[i][0]:
                        plan_short += f'п.{work_list[i][1]} {work_list[i][0]} \n'

            count_row_height(self.ws, ws2, work_list, merged_cells_dict, ins_ind)
            # print(f'3 - {ws2.max_row}')
            well_data.itog_ind_min = self.ins_ind_border
            well_data.itog_ind_max = len(work_list)
            # print(f' длина {len(work_list)}')
            CreatePZ.add_itog(self, ws2, self.table_widget.rowCount() + 1, self.work_plan)
            # print(f'45- {ws2.max_row}')
            for row_ind, row in enumerate(ws2.iter_rows(values_only=True)):

                if 15 < row_ind < 100:
                    if all(cell in [None, ''] for cell in row) \
                            and ('Интервалы темпа' not in str(ws2.cell(row=row_ind, column=2).value) \
                                 and 'Замечания к эксплуатационному периоду' not in str(
                                ws2.cell(row=row_ind, column=2).value) \
                                 and 'Замечания к эксплуатационному периоду' not in str(
                                ws2.cell(row=row_ind - 2, column=2).value)):
                        # print(row_ind, ('Интервалы темпа' not in str(ws2.cell(row=row_ind, column=2).value)),
                        #       str(ws2.cell(row=row_ind, column=2).value))
                        ws2.row_dimensions[row_ind + 1].hidden = True
                for col, value in enumerate(row):
                    if 'Зуфаров' in str(value):
                        coordinate = f'{get_column_letter(col - 2)}{row_ind - 2}'
                        self.insert_image(ws2, 'imageFiles/Зуфаров.png', coordinate)
                    elif 'М.К.Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 1}'
                        self.insert_image(ws2, 'imageFiles/Алиев махир.png', coordinate)
                    elif 'З.К. Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 1}'
                        self.insert_image(ws2, 'imageFiles/Алиев Заур.png', coordinate)
                        break
            if self.work_plan != 'dop_plan':
                self.create_short_plan(wb2, plan_short)

            # print(f'9 - {ws2.max_row}')
            if self.work_plan != 'dop_plan':
                self.insert_image(ws2, 'imageFiles/Хасаншин.png', 'H1')
                self.insert_image(ws2, 'imageFiles/Шамигулов.png', 'H4')

                cat_h2s_list = well_data.dict_category[well_data.plast_work_short[0]]['по сероводороду'].category
                h2s_mg = well_data.dict_category[well_data.plast_work_short[0]]['по сероводороду'].data_mg_l
                h2s_pr = well_data.dict_category[well_data.plast_work_short[0]]['по сероводороду'].data_procent

                if cat_h2s_list in [1, 2] and self.work_plan != 'dop_plan':
                    ws3 = wb2.create_sheet('Sheet1')
                    ws3.title = "Расчет необходимого количества поглотителя H2S"
                    ws3 = wb2["Расчет необходимого количества поглотителя H2S"]
                    calc_h2s(ws3, h2s_pr, h2s_mg)
                else:
                    print(f'Расчет поглотителя сероводорода не требуется')

            ws2.print_area = f'B1:L{self.table_widget.rowCount() + 45}'
            ws2.page_setup.fitToPage = True
            ws2.page_setup.fitToHeight = False
            ws2.page_setup.fitToWidth = True
            ws2.print_options.horizontalCentered = True
            # зададим размер листа
            ws2.page_setup.paperSize = ws2.PAPERSIZE_A4
            # содержимое по ширине страницы
            ws2.sheet_properties.pageSetUpPr.fitToPage = True
            ws2.page_setup.fitToHeight = False

            # path = 'workiii'
            path = 'D:\Documents\Desktop\ГТМ'
            if self.work_plan == 'dop_plan':
                string_work = f' № {well_data.number_dp}'
            elif self.work_plan == 'krs':
                string_work = 'ПР'
            else:
                string_work = 'ГНКТ'

            filenames = f"{well_data.well_number._value} {well_data.well_area._value} кат {int(well_data.cat_P_1[0])} " \
                        f"{string_work}.xlsx"
            full_path = path + "/" + filenames
            # print(f'10 - {ws2.max_row}')
            # print(wb2.path)
            # print(f' кате {well_data.cat_P_1}')
            if well_data.bvo and self.work_plan != 'dop_plan':
                ws5 = wb2.create_sheet('Sheet1')
                ws5.title = "Схемы ПВО"
                ws5 = wb2["Схемы ПВО"]
                wb2.move_sheet(ws5, offset=-1)
                schema_list = self.check_pvo_schema(ws5, ins_ind + 2)

            if wb2:
                wb2.close()
                self.saveFileDialog(wb2, full_path)
                # wb2.save(full_path)
                print(f"Table data saved to Excel {full_path} {well_data.number_dp}")
            if self.wb:
                self.wb.close()

    def close_file(self):
        from find import ProtectedIsNonNone
        from find import ProtectedIsDigit

        if not self.table_widget is None:
            column_head_m = ''
            date_drilling_cancel = ''
            date_drilling_run = ''
            wellhead_fittings = ''
            well_data.dict_perforation_short = {}
            well_data.plast_work_short = []
            self.table_widget.close()
            self.table_widget = None
            well_data.normOfTime = 0
            well_data.gipsInWell = False
            well_data.grp_plan = False
            well_data.nktOpressTrue = False
            well_data.bottomhole_drill = ProtectedIsNonNone(0)
            well_data.open_trunk_well = False
            well_data.normOfTime = 0
            well_data.lift_ecn_can = False
            well_data.pause = True
            well_data.sucker_rod_none = True
            well_data.curator = '0'
            well_data.lift_ecn_can_addition = False
            well_data.column_passability = False
            well_data.column_additional_passability = False
            well_data.template_depth = 0

            well_data.b_plan = 0
            well_data.pipes_ind = ProtectedIsDigit(0)
            well_data.sucker_rod_ind = ProtectedIsDigit(0)
            well_data.expected_Q = 0
            well_data.expected_P = 0
            well_data.plast_select = ''
            well_data.dict_perforation = {}
            well_data.dict_perforation_project = {}
            well_data.itog_ind_min = 0
            well_data.kat_pvo = 2
            well_data.gaz_f_pr = []
            well_data.paker_layout = 0
            well_data.cat_P_P = []
            well_data.column_direction_diametr = ProtectedIsNonNone('не корректно')
            well_data.column_direction_wall_thickness = ProtectedIsNonNone('не корректно')
            well_data.column_direction_lenght = ProtectedIsNonNone('не корректно')
            well_data.column_conductor_diametr = ProtectedIsNonNone('не корректно')
            well_data.column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
            well_data.column_conductor_lenght = ProtectedIsNonNone('не корректно')
            well_data.column_additional_diametr = ProtectedIsNonNone('не корректно')
            well_data.column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
            well_data.head_column_additional = ProtectedIsNonNone('не корректно')
            well_data.shoe_column_additional = ProtectedIsNonNone('не корректно')
            well_data.column_diametr = ProtectedIsNonNone('не корректно')
            well_data.column_wall_thickness = ProtectedIsNonNone('не корректно')
            well_data.shoe_column = ProtectedIsNonNone('не корректно')
            well_data.bottomhole_artificial = ProtectedIsNonNone('не корректно')
            well_data.max_expected_pressure = ProtectedIsNonNone('не корректно')
            well_data.head_column_additional = ProtectedIsNonNone('не корректно')
            well_data.leakiness_Count = 0
            well_data.data_in_base = False
            well_data.well_volume_in_PZ = []
            well_data.expected_pick_up = {}
            well_data.current_bottom = 0
            well_data.fluid_work = 0
            well_data.static_level = ProtectedIsNonNone('не корректно')
            well_data.dinamic_level = ProtectedIsNonNone('не корректно')
            well_data.work_perforations_approved = False
            well_data.dict_leakiness = {}
            well_data.leakiness = False
            well_data.emergency_well = False
            well_data.emergency_count = 0
            well_data.skm_interval = []
            well_data.work_perforations = []
            well_data.work_perforations_dict = {}
            well_data.paker_do = {"do": 0, "posle": 0}
            well_data.column_additional = False
            well_data.well_number = None
            well_data.well_area = None
            well_data.values = []
            well_data.depth_fond_paker_do = {"do": 0, "posle": 0}
            well_data.paker2_do = {"do": 0, "posle": 0}
            well_data.depth_fond_paker2_do = {"do": 0, "posle": 0}
            well_data.perforation_roof = 50000
            well_data.data_x_min = 0
            well_data.perforation_sole = 0
            well_data.dict_pump_SHGN = {"do": '0', "posle": '0'}
            well_data.dict_pump_ECN = {"do": '0', "posle": '0'}
            well_data.dict_pump_SHGN_h = {"do": '0', "posle": '0'}
            well_data.dict_pump_ECN_h = {"do": '0', "posle": '0'}
            well_data.dict_pump = {"do": '0', "posle": '0'}
            well_data.leakiness_interval = []
            well_data.dict_pump_h = {"do": 0, "posle": 0}
            well_data.ins_ind = 0
            well_data.len_razdel_1 = 0
            well_data.count_template = 0
            well_data.cat_P_1 = []
            well_data.countAcid = 0
            well_data.swabTypeComboIndex = 1
            well_data.swab_true_edit_type = 1
            well_data.data_x_max = 0
            well_data.drilling_interval = []
            well_data.max_angle = 0
            well_data.pakerTwoSKO = False
            well_data.privyazkaSKO = 0
            well_data.h2s_pr = []
            well_data.cat_h2s_list = []
            well_data.h2s_mg = []
            well_data.lift_key = 0
            well_data.max_admissible_pressure = ProtectedIsNonNone(0)
            well_data.region = ''
            well_data.dict_nkt = {}
            well_data.dict_nkt_po = {}
            well_data.data_well_max = 0
            well_data.data_pvr_max = 0
            well_data.dict_sucker_rod = {}
            well_data.dict_sucker_rod_po = {}
            well_data.row_expected = []
            well_data.rowHeights = []
            well_data.plast_project = []
            well_data.plast_work = []
            well_data.plast_all = []
            well_data.condition_of_wells = 0
            well_data.cat_well_min = 0
            well_data.bvo = False
            well_data.old_version = False
            well_data.image_list = []
            well_data.problemWithEk = False
            well_data.problemWithEk_depth = well_data.current_bottom
            well_data.problemWithEk_diametr = 220
            path = "imageFiles/image_work"
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        print("Closing current file")

    def on_finished(self):
        print("Работа с файлом Excel завершена.")

    def insert_image(self, ws, file, coordinate, width=200, height=180):
        # Загружаем изображение с помощью библиотеки Pillow

        img = openpyxl.drawing.image.Image(file)
        img.width = width
        img.height = height
        img.anchor = coordinate
        ws.add_image(img, coordinate)

    def openContextMenu(self, position):

        context_menu = QMenu(self)

        action_menu = context_menu.addMenu("вид работ")
        geophysical = action_menu.addMenu("Геофизические работы")

        perforation_action = QAction("Перфорация", self)
        geophysical.addAction(perforation_action)
        perforation_action.triggered.connect(self.perforationNewWindow)

        geophysical_action = QAction("Геофизические исследования", self)
        geophysical.addAction(geophysical_action)
        geophysical_action.triggered.connect(self.GeophysicalNewWindow)

        rgd_menu = geophysical.addMenu("РГД")
        rgdWithoutPaker_action = QAction("РГД по колонне", self)
        rgd_menu.addAction(rgdWithoutPaker_action)
        rgdWithoutPaker_action.triggered.connect(self.rgdWithoutPaker_action)

        rgdWithPaker_action = QAction("РГД с пакером", self)
        rgd_menu.addAction(rgdWithPaker_action)
        rgdWithPaker_action.triggered.connect(self.rgdWithPaker_action)

        privyazka_action = QAction("Привязка НКТ", self)
        geophysical.addAction(privyazka_action)
        privyazka_action.triggered.connect(self.privyazkaNKT)

        definitionBottomGKLM_action = QAction("Отбивка забоя по ЭК", self)
        geophysical.addAction(definitionBottomGKLM_action)
        definitionBottomGKLM_action.triggered.connect(self.definitionBottomGKLM)

        vp_action = QAction("Установка ВП", self)
        geophysical.addAction(vp_action)
        vp_action.triggered.connect(self.vp_action)

        swibbing_action = QAction("Свабирование", self)
        geophysical.addAction(swibbing_action)
        swibbing_action.triggered.connect(self.swibbing_with_paker)

        kompressVoronka_action = QAction("Освоение компрессором с воронкой", self)
        geophysical.addAction(kompressVoronka_action)
        kompressVoronka_action.triggered.connect(self.kompress_with_voronka)

        del_menu = context_menu.addMenu('удаление строки')
        emptyString_action = QAction("добавить пустую строку", self)
        del_menu.addAction(emptyString_action)
        emptyString_action.triggered.connect(self.emptyString)

        # gnkt_menu = context_menu.addMenu("ГНКТ")
        # gnkt_opz_action = QAction("ГНКТ ОПЗ", self)
        # gnkt_menu.addAction(gnkt_opz_action)
        # gnkt_opz_action.triggered.connect(self.gnkt_opz)
        #
        # gnkt_opz_action = QAction("ГНКТ Освоение после ГРП", self)
        # gnkt_menu.addAction(gnkt_opz_action)
        # gnkt_opz_action.triggered.connect(self.gnkt_after_grp)

        deleteString_action = QAction("Удалить строку", self)
        del_menu.addAction(deleteString_action)
        deleteString_action.triggered.connect(self.deleteString)

        opressovka_action = QAction("Опрессовка колонны", self)
        action_menu.addAction(opressovka_action)
        opressovka_action.triggered.connect(self.pressureTest)

        template_with_skm = QAction("шаблон c СКМ", self)
        template_menu = action_menu.addMenu('Шаблоны')
        template_menu.addAction(template_with_skm)
        template_with_skm.triggered.connect(self.template_with_skm)

        template_pero = QAction("проходимость по перу", self)

        template_menu.addAction(template_pero)
        template_pero.triggered.connect(self.template_pero)

        ryber_action = QAction("Райбирование", self)
        action_menu.addAction(ryber_action)
        ryber_action.triggered.connect(self.ryber_add)

        drilling_menu = action_menu.addMenu('Бурение')

        drilling_action_nkt = QAction("бурение на НКТ", self)
        drilling_menu.addAction(drilling_action_nkt)
        drilling_action_nkt.triggered.connect(self.drilling_action_nkt)

        frezering_port_action = QAction("Фрезерование портов", self)
        drilling_menu.addAction(frezering_port_action)
        frezering_port_action.triggered.connect(self.frezering_port_action)

        template_without_skm = QAction("шаблон без СКМ", self)
        template_menu.addAction(template_without_skm)
        template_without_skm.triggered.connect(self.template_without_skm)

        emergency_menu = action_menu.addMenu('Аварийные работы')

        magnet_action = QAction("магнит", self)
        emergency_menu.addAction(magnet_action)
        magnet_action.triggered.connect(self.magnet_action)

        hook_action = QAction("Удочка-крючок", self)
        emergency_menu.addAction(hook_action)
        hook_action.triggered.connect(self.hook_action)

        emergency_sticking_action = QAction("Прихваченное оборудование", self)
        emergency_menu.addAction(emergency_sticking_action)
        emergency_sticking_action.triggered.connect(self.emergency_sticking_action)

        larNKT_action = QAction("печать + ЛАР на НКТ", self)
        emergency_menu.addAction(larNKT_action)
        larNKT_action.triggered.connect(self.larNKT_action)

        lar_sbt_action = QAction("ЛАР на СБТ правое", self)
        emergency_menu.addAction(lar_sbt_action)
        lar_sbt_action.triggered.connect(self.lar_sbt_action)

        lapel_tubing_action = QAction("Отворот на СБТ левое", self)
        emergency_menu.addAction(lapel_tubing_action)
        lapel_tubing_action.triggered.connect(self.lapel_tubing_func)

        acid_menu = action_menu.addMenu('Кислотная обработка')
        acid_action1paker = QAction("Кислотная обработка", self)
        acid_menu.addAction(acid_action1paker)
        acid_action1paker.triggered.connect(self.acidPakerNewWindow)

        acid_action_gons = QAction("ГОНС", self)
        acid_menu.addAction(acid_action_gons)
        acid_action_gons.triggered.connect(self.acid_action_gons)

        sand_menu = action_menu.addMenu('песчанный мост')
        filling_action = QAction('Отсыпка песком')
        sand_menu.addAction(filling_action)
        filling_action.triggered.connect(self.filling_sand)

        washing_action = QAction('вымыв песка')
        sand_menu.addAction(washing_action)
        washing_action.triggered.connect(self.washing_sand)

        grp_menu = action_menu.addMenu('ГРП')
        grpWithPaker_action = QAction('ГРП с одним пакером')
        grp_menu.addAction(grpWithPaker_action)
        grpWithPaker_action.triggered.connect(self.grpWithPaker)

        grpWithGpp_action = QAction('ГРП с ГПП')
        grp_menu.addAction(grpWithGpp_action)
        grpWithGpp_action.triggered.connect(self.grpWithGpp)

        alone_menu = action_menu.addMenu('одиночные операции')

        mkp_action = QAction('Ревизия МКП')
        alone_menu.addAction(mkp_action)
        mkp_action.triggered.connect(self.mkp_revision)

        konte_action = QAction('Канатные технологии')
        alone_menu.addAction(konte_action)
        konte_action.triggered.connect(self.konte_action)

        definition_Q_action = QAction("Определение приемитости по НКТ", self)
        alone_menu.addAction(definition_Q_action)
        definition_Q_action.triggered.connect(self.definition_Q)

        definition_Q_NEK_action = QAction("Определение приемитости по затрубу", self)
        alone_menu.addAction(definition_Q_NEK_action)
        definition_Q_NEK_action.triggered.connect(self.definition_Q_nek)

        kot_action = QAction('Система обратных клапанов')
        alone_menu.addAction(kot_action)
        kot_action.triggered.connect(self.kot_work)

        fluid_change_action = QAction('Изменение удельного веса')
        alone_menu.addAction(fluid_change_action)
        fluid_change_action.triggered.connect(self.fluid_change_action)

        pvo_cat1_action = QAction('Монтаж первой категории')
        alone_menu.addAction(pvo_cat1_action)
        pvo_cat1_action.triggered.connect(self.pvo_cat1)

        rir_menu = action_menu.addMenu('РИР')

        pakerIzvlek_menu = rir_menu.addMenu('извлекаемый пакер')
        pakerIzvlek_action = QAction('Установка пакера')
        pakerIzvlek_menu.addAction(pakerIzvlek_action)
        pakerIzvlek_action.triggered.connect(self.pakerIzvlek_action)

        izvlek_action = QAction('извлечение')
        pakerIzvlek_menu.addAction(izvlek_action)
        izvlek_action.triggered.connect(self.izvlek_action)

        rir_action = QAction('РИР')
        rir_menu.addAction(rir_action)
        rir_action.triggered.connect(self.rirAction)

        claySolision_action = QAction('Глинистый раствор в ЭК')
        rir_menu.addAction(claySolision_action)
        claySolision_action.triggered.connect(self.claySolision)

        gno_menu = action_menu.addAction('Спуск фондового оборудования')
        gno_menu.triggered.connect(self.gno_bottom)

        context_menu.exec_(self.mapToGlobal(position))

    def clickedRowColumn(self, r, c):

        self.ins_ind = r + 1
        well_data.ins_ind = r + 1
        if r > well_data.count_row_well and self.work_plan == 'krs':
            data = self.read_clicked_mouse_data(r)

    def read_clicked_mouse_data(self, row):

        row = row - well_data.count_row_well

        for index, data in enumerate(well_data.data_list):
            if index == row:
                well_data.current_bottom = data[1]
                well_data.dict_perforation = json.loads(data[2])
                # print(f' строка {well_data.dict_perforation}')

                well_data.plast_all = json.loads(data[3])
                well_data.plast_work = json.loads(data[4])
                well_data.dict_leakiness = json.loads(data[5])
                well_data.column_additional = data[6]
                well_data.fluid_work = data[7]
                well_data.template_depth = int(data[11])
                well_data.skm_interval = json.loads(data[12])
                well_data.problemWithEk_depth = data[13]
                well_data.problemWithEk_diametr = data[14]

    @staticmethod
    def pause_app():
        while well_data.pause is True:
            QtCore.QCoreApplication.instance().processEvents()

    def frezering_port_action(self):
        from work_py.drilling import Drill_window
        drilling_work_list = Drill_window.frezer_ports(self)
        self.populate_row(self.ins_ind, drilling_work_list, self.table_widget)

    def drilling_action_nkt(self):
        if self.raid_window is None:
            self.raid_window = Drill_window(well_data.ins_ind, self.table_widget)
            self.raid_window.setGeometry(200, 400, 300, 400)
            self.raid_window.show()
            self.pause_app()
            well_data.pause = True
            self.raid_window = None
        else:
            self.raid_window.close()  # Close window.
            self.raid_window = None

    def magnet_action(self):
        from work_py.emergencyWork import magnetWork
        magnet_work_list = magnetWork(self)
        self.populate_row(self.ins_ind, magnet_work_list, self.table_widget)

    def emergency_sticking_action(self):
        from work_py.emergencyWork import emergency_sticking
        emergency_sticking_list = emergency_sticking(self)
        self.populate_row(self.ins_ind, emergency_sticking_list, self.table_widget)

    def hook_action(self):
        from work_py.emergencyWork import emergency_hook
        hook_work_list = emergency_hook(self)
        self.populate_row(self.ins_ind, hook_work_list, self.table_widget)

    def lapel_tubing_func(self):
        from work_py.emergencyWork import lapel_tubing
        emergency_sbt_list = lapel_tubing(self)
        self.populate_row(self.ins_ind, emergency_sbt_list, self.table_widget)

    def lar_sbt_action(self):
        from work_py.emergencyWork import emergence_sbt
        emergency_sbt_list = emergence_sbt(self)
        self.populate_row(self.ins_ind, emergency_sbt_list, self.table_widget)

    def larNKT_action(self):
        from work_py.emergencyWork import emergencyNKT
        emergencyNKT_list = emergencyNKT(self)
        self.populate_row(self.ins_ind, emergencyNKT_list, self.table_widget)

    def rgdWithoutPaker_action(self):
        from work_py.rgdVcht import rgdWithoutPaker
        rgdWithoutPaker_list = rgdWithoutPaker(self)
        self.populate_row(self.ins_ind, rgdWithoutPaker_list, self.table_widget)

    def rgdWithPaker_action(self):
        from work_py.rgdVcht import rgdWithPaker
        rgdWithPaker_list = rgdWithPaker(self)
        self.populate_row(self.ins_ind, rgdWithPaker_list, self.table_widget)

    def definitionBottomGKLM(self):
        from work_py.alone_oreration import definitionBottomGKLM
        definitionBottomGKLM_list = definitionBottomGKLM(self)
        self.populate_row(self.ins_ind, definitionBottomGKLM_list, self.table_widget)

    def privyazkaNKT(self):
        from work_py.alone_oreration import privyazkaNKT
        privyazkaNKT_list = privyazkaNKT(self)
        self.populate_row(self.ins_ind, privyazkaNKT_list, self.table_widget)

    def definition_Q(self):
        from work_py.alone_oreration import definition_Q
        definition_Q_list = definition_Q(self)
        self.populate_row(self.ins_ind, definition_Q_list, self.table_widget)

    def definition_Q_nek(self):
        from work_py.alone_oreration import definition_Q_nek
        definition_Q_list = definition_Q_nek(self)
        self.populate_row(self.ins_ind, definition_Q_list, self.table_widget)

    def kot_work(self):
        from work_py.alone_oreration import kot_work

        kot_work_list = kot_work(self, well_data.current_bottom)
        self.populate_row(self.ins_ind, kot_work_list, self.table_widget)

    def konte_action(self):
        from work_py.alone_oreration import konte
        konte_work_list = konte(self)
        self.populate_row(self.ins_ind, konte_work_list, self.table_widget)

    def mkp_revision(self):
        from work_py.mkp import mkp_revision
        mkp_work_list = mkp_revision(self)
        self.populate_row(self.ins_ind, mkp_work_list, self.table_widget)

    def acid_action_gons(self):
        from work_py.acids import acidGons
        acidGons_work_list = acidGons(self)
        self.populate_row(self.ins_ind, acidGons_work_list, self.table_widget)

    def izvlek_action(self):
        from work_py.rir import RirWindow
        izvlech_paker_work_list = RirWindow.izvlech_paker(self)
        self.populate_row(self.ins_ind, izvlech_paker_work_list, self.table_widget)

    def pakerIzvlek_action(self):
        from work_py.rir import RirWindow
        rir_izvelPaker_work_list = RirWindow.rir_izvelPaker(self)
        self.populate_row(self.ins_ind, rir_izvelPaker_work_list, self.table_widget)

    def read_pz(self, fname):
        self.wb = load_workbook(fname, data_only=True)
        name_list = self.wb.sheetnames
        old_index = 1
        self.ws = self.wb.active

        for sheet in name_list:
            if sheet in self.wb.sheetnames and (sheet != 'наряд-заказ КРС' or sheet != 'План работ'):
                self.wb.remove(self.wb[sheet])

    def pvo_cat1(self):
        from work_py.alone_oreration import pvo_cat1
        pvo_cat1_work_list = pvo_cat1(self)
        self.populate_row(self.ins_ind, pvo_cat1_work_list, self.table_widget)

    def fluid_change_action(self):
        from work_py.change_fluid import Change_fluid_Window

        if self.rir_window is None:
            self.rir_window = Change_fluid_Window(well_data.ins_ind, self.table_widget)
            # self.rir_window.setGeometry(200, 400, 100, 200)
            self.rir_window.show()
            self.pause_app()
            well_data.pause = True
            self.rir_window = None
        else:
            self.rir_window.close()  # Close window.
            self.rir_window = None

    def claySolision(self):
        from work_py.claySolution import ClayWindow
        if self.rir_window is None:
            well_data.countAcid = 0
            self.rir_window = ClayWindow(well_data.ins_ind, self.table_widget)
            # self.rir_window.setGeometry(200, 400, 100, 200)
            self.rir_window.show()
            self.pause_app()
            well_data.pause = True
            self.rir_window = None
        else:
            self.rir_window.close()  # Close window.
            self.rir_window = None

    def rirAction(self):
        from work_py.rir import RirWindow

        if self.rir_window is None:
            well_data.countAcid = 0
            self.rir_window = RirWindow(well_data.ins_ind, self.table_widget)
            # self.rir_window.setGeometry(200, 400, 300, 400)
            self.rir_window.show()
            self.pause_app()
            well_data.pause = True
            self.rir_window = None
        else:
            self.rir_window.close()  # Close window.
            self.rir_window = None

    def grpWithPaker(self):
        from work_py.grp import Grp_window

        if self.work_window is None:
            self.work_window = Grp_window(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def grpWithGpp(self):
        from work_py.gpp import Gpp_window

        if self.work_window is None:
            self.work_window = Gpp_window(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def filling_sand(self):
        from work_py.sand_filling import SandWindow

        if self.work_window is None:
            self.work_window = SandWindow(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def washing_sand(self):
        from work_py.sand_filling import SandWindow

        print('Вставился отсыпка песком')
        washing_work_list = SandWindow.sandWashing(self)
        self.populate_row(self.ins_ind, washing_work_list, self.table_widget)

    def deleteString(self):
        selected_ranges = self.table_widget.selectedRanges()
        selected_rows = []
        if self.ins_ind > well_data.count_row_well:
            # Получение индексов выбранных строк
            for selected_range in selected_ranges:
                top_row = selected_range.topRow()
                bottom_row = selected_range.bottomRow()

                for row in range(top_row, bottom_row + 1):
                    if row not in selected_rows:
                        selected_rows.append(row)

            # Удаление выбранных строк в обратном порядке
            selected_rows.sort(reverse=True)
            # print(selected_rows)
            for row in selected_rows:
                print(row - well_data.count_row_well, well_data.data_list)
                self.table_widget.removeRow(row)
                well_data.data_list.pop(row - well_data.count_row_well)

    def emptyString(self):
        if self.ins_ind > well_data.count_row_well:
            ryber_work_list = [[None, None, None, None, None, None, None, None, None, None, None, None]]
            self.populate_row(self.ins_ind, ryber_work_list, self.table_widget)

    def vp_action(self):
        from work_py.vp_cm import VpWindow

        if self.work_window is None:
            self.work_window = VpWindow(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None

    def swibbing_with_paker(self):
        from work_py.swabbing import Swab_Window

        if self.work_window is None:
            self.work_window = Swab_Window(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def kompress_with_voronka(self):
        from work_py.kompress import Kompress_Window

        if self.work_window is None:
            self.work_window = Kompress_Window(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 300, 400)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def ryber_add(self):
        from work_py.raiding import Raid

        if self.work_window is None:
            self.work_window = Raid(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 300, 400)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def gnkt_after_grp(self):
        from gnkt_after_grp import gnkt_work
        gnkt_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, gnkt_work_list, self.table_widget)

    def gnkt_opz(self):
        from gnkt_opz import GnktOpz

        if self.work_window is None:
            self.work_window = GnktOpz(well_data.ins_ind, self.table_widget)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def gno_bottom(self):
        from work_py.descent_gno import GnoDescentWindow

        if self.work_window is None:
            self.work_window = GnoDescentWindow(well_data.ins_ind, self.table_widget)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def pressureTest(self):
        from work_py.opressovka import OpressovkaEK

        if self.work_window is None:
            self.work_window = OpressovkaEK(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 300, 400)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def template_pero(self):
        from work_py.template_work import TemplateKrs

        template_pero_list = TemplateKrs.pero(self)
        self.populate_row(self.ins_ind, template_pero_list, self.table_widget)

    def template_with_skm(self):
        from work_py.template_work import TemplateKrs

        if self.work_window is None:
            self.work_window = TemplateKrs(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def template_without_skm(self):
        from work_py.template_without_skm import Template_without_skm

        if self.work_window is None:
            self.work_window = Template_without_skm(well_data.ins_ind, self.table_widget)
            # self.work_window.setGeometry(200, 400, 500, 500)
            self.work_window.show()
            self.pause_app()
            well_data.pause = True
            self.work_window = None
        else:
            self.work_window.close()  # Close window.
            self.work_window = None

    def populate_row(self, ins_ind, work_list, table_widget, work_plan='krs'):
        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 1500)}
        index_setSpan = 0
        if work_plan == 'gnkt_frez':
            index_setSpan = 1
        row_max = table_widget.rowCount()
        print(f'ДОП {work_plan}')

        for i, row_data in enumerate(work_list):

            row = ins_ind + i
            if work_plan not in ['application_pvr', 'gnkt_frez', 'gnkt_opz', 'gnkt_after_grp', 'application_gis']:
                MyWindow.insert_data_in_database(self, row, row_max + i)

            table_widget.insertRow(row)

            if len(str(row_data[1])) > 3 and work_plan in 'gnkt_frez':
                table_widget.setSpan(i + ins_ind, 1, 1, 12)

            else:
                table_widget.setSpan(i + ins_ind, 2, 1, 8 + index_setSpan)
            for column, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | Qt.ItemIsEditable)

                if not data is None:
                    table_widget.setItem(row, column, item)

                else:
                    table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                table_widget.setRowHeight(row, int(text_width))

    def create_database_well(self, work_plan):

        well_data.number_dict = []

    def insert_data_in_database(self, row_number, row_max):

        dict_perforation_json = json.dumps(well_data.dict_perforation, default=str, ensure_ascii=False, indent=4)
        print(well_data.dict_leakiness)
        leakage_json = json.dumps(well_data.dict_leakiness, default=str, ensure_ascii=False, indent=4)
        plast_all_json = json.dumps(well_data.plast_all)
        plast_work_json = json.dumps(well_data.plast_work)
        skm_list_json = json.dumps(well_data.skm_interval)
        number = json.dumps(well_data.well_number._value + well_data.well_area._value, ensure_ascii=False, indent=4)

        # Подготовленные данные для вставки (пример)
        data_values = (row_max, well_data.current_bottom, dict_perforation_json, plast_all_json, plast_work_json,
                       leakage_json, well_data.column_additional, well_data.fluid_work,
                       well_data.category_pressuar, well_data.category_h2s, well_data.category_gf,
                       well_data.template_depth, skm_list_json,
                       well_data.problemWithEk_depth, well_data.problemWithEk_diametr)

        if len(well_data.data_list) == 0:
            well_data.data_list.append(data_values)
        else:
            row_number = row_number - well_data.count_row_well
            well_data.data_list.insert(row_number, data_values)

    def acidPakerNewWindow(self):
        from work_py.acid_paker import AcidPakerWindow

        if self.acid_windowPaker is None:

            self.acid_windowPaker = AcidPakerWindow(self.ins_ind, self.table_widget)

            # self.acid_windowPaker.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker.show()
            self.pause_app()
            well_data.pause = True

        else:
            self.acid_windowPaker.close()  # Close window.
            self.acid_windowPaker = None

    def check_pvo_schema(self, ws5, ind):
        schema_pvo_set = set()
        for row in range(self.table_widget.rowCount()):
            if row > ind:
                for column in range(self.table_widget.columnCount()):
                    value = self.table_widget.item(row, column)
                    if value != None:
                        value = value.text()

                        if 'схеме №' in value or 'схемы №' in value:
                            number_schema = value[value.index(' №') + 1:value.index(' №') + 4].replace(' ', '')
                            if '1' in number_schema:
                                number_schema = "2"
                            schema_pvo_set.add(number_schema)
        # print(f'схема ПВО {schema_pvo_set}')

        n = 0
        for schema in list(schema_pvo_set):
            coordinate = f'{get_column_letter(2)}{1 + n}'
            schema_path = f'imageFiles/pvo/oil/схема {schema}.jpg'
            img = openpyxl.drawing.image.Image(schema_path)
            img.width = 750
            img.height = 530
            img.anchor = coordinate
            ws5.add_image(img, coordinate)
            n += 29
        ws5.print_area = f'B1:M{n}'
        ws5.page_setup.fitToPage = True
        ws5.page_setup.fitToHeight = False
        ws5.page_setup.fitToWidth = True
        ws5.print_options.horizontalCentered = True
        # зададим размер листа
        ws5.page_setup.paperSize = ws5.PAPERSIZE_A4
        # содержимое по ширине страницы
        ws5.sheet_properties.pageSetUpPr.fitToPage = True
        ws5.page_setup.fitToHeight = False
        # Переместите второй лист перед первым

        return list(schema_pvo_set)

    def GeophysicalNewWindow(self):
        from work_py.geophysic import GeophysicWindow

        if self.new_window is None:
            self.new_window = GeophysicWindow(self.table_widget, self.ins_ind)
            self.new_window.setWindowTitle("Геофизические исследования")
            # self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()
            self.pause_app()
            well_data.pause = True
            self.new_window = None  # Discard reference.


        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def correctPVR(self):
        from perforation_correct import PerforationCorrect

        well_data.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                              'Введите забой до которого нужно нормализовать')
        if self.perforation_correct_window2 is None:
            self.perforation_correct_window2 = PerforationCorrect(self)
            self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
            # self.perforation_correct_window2.setGeometry(200, 400, 100, 400)

            self.perforation_correct_window2.show()
            self.pause_app()
            well_data.pause = True
            self.perforation_correct_window2 = None

        else:
            self.perforation_correct_window2.close()
            self.perforation_correct_window2 = None

    def correctData(self):
        from data_correct import DataWindow

        if self.correct_window is None:

            self.correct_window = DataWindow()
            self.correct_window.setWindowTitle("Окно корректировки")
            # self.correct_window.setGeometry(100, 400, 300, 400)
            self.correct_window.show()
            self.pause_app()
            well_data.pause = True
            self.correct_window = None

        else:
            self.correct_window.close()  # Close window.
            self.correct_window = None  # Discard reference.

    def perforationNewWindow(self):
        from work_py.perforation import PerforationWindow

        if len(well_data.cat_P_1) > 1:
            if well_data.cat_P_1[1] == 1 and well_data.kat_pvo != 1:
                msc = QMessageBox.information(self, 'Внимание', 'Не произведен монтаж первой категории')
                return

        if self.new_window is None:

            self.new_window = PerforationWindow(self.table_widget, self.ins_ind)
            self.new_window.setWindowTitle("Перфорация")
            # self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()
            self.pause_app()
            well_data.pause = True

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def insertPerf(self):
        self.populate_row(self.ins_ind, self.perforation_list)

    def copy_pz(self, sheet, table_widget, work_plan='krs', count_col=12, list_page=1):
        from krs import GnoWindow

        rows = sheet.max_row
        merged_cells = sheet.merged_cells
        table_widget.setRowCount(rows)
        well_data.count_row_well = table_widget.rowCount()

        border_styles = {}
        for row in sheet.iter_rows():
            for cell in row:
                border_styles[(cell.row, cell.column)] = cell.border

        table_widget.setColumnCount(count_col)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height is not None else 18
                           for i in range(sheet.max_row)]
        if work_plan not in ['application_pvr', 'gnkt_frez', 'gnkt_after_grp', 'gnkt_opz']:
            self.populate_row(table_widget.rowCount(), [
                [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
                [None, None, 'Наименование работ', None, None, None, None, None, None, None, 'Ответственный',
                 'Нормы времени \n мин/час.']], self.table_widget, self.work_plan)

        for row in range(1, rows + 2):
            if row > 1 and row < rows - 1:
                table_widget.setRowHeight(row, int(rowHeights_exit[row]))
            for col in range(1, count_col + 1):

                if not sheet.cell(row=row, column=col).value is None:
                    if isinstance(sheet.cell(row=row, column=col).value, float) and row > 25:
                        cell_value = str(round(sheet.cell(row=row, column=col).value, 2))
                    elif isinstance(sheet.cell(row=row, column=col).value, datetime):
                        cell_value = sheet.cell(row=row, column=col).value.strftime('%d.%m.%Y')
                    else:
                        cell_value = str(sheet.cell(row=row, column=col).value)
                        # print(cell_value)

                    # cell = sheet[f'{get_column_letter(col + 1)}{row + 1}']
                    # cell_style = cell._style

                    item = QtWidgets.QTableWidgetItem(str(cell_value))
                    # item.setData(10, cell_style)
                    # item.setData(10, cell_style)

                    table_widget.setItem(row - 1, col - 1, item)
                    # Проверяем, является ли текущая ячейка объединенной
                    for merged_cell in merged_cells:
                        if row in range(merged_cell.min_row, merged_cell.max_row + 1) and \
                                col in range(merged_cell.min_col, merged_cell.max_col + 1):
                            # Устанавливаем количество объединяемых строк и столбцов для текущей ячейки
                            table_widget.setSpan(row - 1, col - 1,
                                                 merged_cell.max_row - merged_cell.min_row + 1,
                                                 merged_cell.max_col - merged_cell.min_col + 1)
                else:
                    item = QTableWidgetItem("")
                # border = sheet.cell(row=row, column=col).border
                # if border.top.style is not None:
                #     item.setFlags(item.flags() ^ 0x00100000)  # Убираем рамку из ячейки
                # table_widget.setItem(row - 1, col - 1, item)

                # # Установка стилей и границ ячеек, используя openpyxl
                # cell = sheet.cell(row=row + 1, column=col + 1)
                # if cell.border:
                #     top_border = cell.border.top.style
                #     bottom_border = cell.border.bottom.style
                #     left_border = cell.border.left.style
                #     right_border = cell.border.right.style
                #
                # # if right_border:
                #
                #     # Установка стилей для правых границ ячеек
                #     if table_widget.item(row, col):
                #         border_style = cell.data(Qt.UserRole)
                #         if border_style:
                #             cell.setStyleSheet("border-right: 1px solid black;")

                # if not left_border is None:
                #     # Установка стилей для правых границ ячеек
                #     item.setData(Qt.UserRole, "border-left: 1px solid black;")
                # if not bottom_border is  None:
                #     # Установка стилей для правых границ ячеек
                #     item.setData(Qt.UserRole, "border-bottom: 1px solid black;")
                # if not top_border is  None:
                #     # Установка стилей для правых границ ячеек
                #     item.setData(Qt.UserRole, "border-top: 1px solid black;")

                # table_widget.setStyleSheet(f"QTableWidget::item {top_border}: 1px ; padding: 2px; ")
        if work_plan == 'krs':
            if self.work_window is None:
                self.work_window = GnoWindow(table_widget.rowCount(), self.table_widget, self.work_plan)

                # self.work_window.setGeometry(100, 400, 200, 500)
                self.work_window.show()

                self.pause_app()
                well_data.pause = True
                self.work_window = None
            else:
                self.work_window.close()  # Close window.
                self.work_window = None

        elif work_plan == 'dop_plan':

            self.rir_window = DopPlanWindow(well_data.ins_ind, self.table_widget, work_plan)
            # self.rir_window.setGeometry(200, 400, 100, 200)
            self.rir_window.show()
            self.pause_app()
            well_data.pause = True
            self.rir_window = None

        if work_plan in ['gnkt_frez'] and list_page == 2:
            colWidth = [2.28515625, 13.0, 4.5703125, 13.0, 13.0, 13.0, 5.7109375, 13.0, 13.0, 13.0, 4.7109375,
                        13.0, 5.140625, 13.0, 13.0, 13.0, 13.0, 13.0, 4.7109375, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0,
                        13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0, 13.0, 13.0, 5.42578125, 13.0, 4.5703125, 2.28515625, 10.28515625]
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(colWidth[column]))  # Здесь задайте требуемую ширину столбца
        elif work_plan in ['gnkt_after_grp', 'gnkt_opz'] and list_page == 2:

            colWidth = property_excel.property_excel_pvr.colWidth_gnkt_osv
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(colWidth[column] * 9))  # Здесь задайте требуемую ширину столбца

        elif work_plan == 'application_pvr':
            from property_excel import property_excel_pvr
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(
                    property_excel_pvr.colWidth[column]))  # Здесь задайте требуемую ширину столбца

    def create_short_plan(self, wb2, plan_short):
        from work_py.descent_gno import TabPage_Gno

        ws4 = wb2.create_sheet('Sheet1')
        ws4.title = "Краткое содержание плана работ"
        ws4 = wb2["Краткое содержание плана работ"]

        for row in range(15):
            ws4.insert_rows(ws4.max_row)
        ws4.cell(row=1, column=1).value = well_data.well_number._value
        ws4.cell(row=2, column=1).value = well_data.well_area._value

        if well_data.dict_pump_SHGN["do"] != 0 and well_data.dict_pump_ECN["do"] == 0 and \
                well_data.paker_do["do"] == 0:
            ws4.cell(row=3,
                     column=1).value = f'{well_data.dict_pump_SHGN["do"]} -на гл. {well_data.dict_pump_SHGN_h["do"]}м'
        elif well_data.dict_pump_SHGN["do"] == 0 and well_data.dict_pump_ECN["do"] != 0 and \
                well_data.paker_do["do"] == 0:
            ws4.cell(row=3,
                     column=1).value = f'{well_data.dict_pump_ECN["do"]} -на гл. {well_data.dict_pump_ECN_h["do"]}м'
        elif well_data.dict_pump_SHGN["do"] == 0 and well_data.dict_pump_ECN["do"] != 0 and \
                well_data.paker_do["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{well_data.dict_pump_ECN["do"]} -на гл. {well_data.dict_pump_ECN_h["do"]}м \n' \
                                       f'{well_data.paker_do["do"]} на {well_data.depth_fond_paker_do["do"]}м'
        elif well_data.dict_pump_SHGN["do"] != 0 and well_data.dict_pump_ECN["do"] == 0 and \
                well_data.paker_do["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{well_data.dict_pump_SHGN["do"]} -на гл. {well_data.dict_pump_SHGN_h["do"]}м \n' \
                                       f'{well_data.paker_do["do"]} на {well_data.depth_fond_paker_do["do"]}м'
        elif well_data.dict_pump_SHGN["do"] == 0 and well_data.dict_pump_ECN["do"] == 0 and \
                well_data.paker_do["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{well_data.paker_do["do"]} на {well_data.depth_fond_paker_do["do"]}м'
        elif well_data.dict_pump_SHGN["do"] == 0 and well_data.dict_pump_ECN["do"] == 0 and \
                well_data.paker_do["do"] == 0:
            ws4.cell(row=3, column=1).value = " "
        elif well_data.dict_pump_SHGN["do"] != 0 and well_data.dict_pump_ECN["do"] != 0 and \
                well_data.paker_do["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{well_data.dict_pump_SHGN["do"]} -на гл. {well_data.dict_pump_SHGN_h["do"]}м \n' \
                                       f'{well_data.dict_pump_ECN["do"]} -на гл. {well_data.dict_pump_ECN_h["do"]}м \n' \
                                       f'{well_data.paker_do["do"]} на {well_data.depth_fond_paker_do["do"]}м '
        plast_str = ''
        pressur_set = set()
        # print(f'После {well_data.dict_perforation_short}')
        for plast in list(well_data.dict_perforation_short.keys()):
            if well_data.dict_perforation_short[plast][
                'отключение'] is False and plast in well_data.dict_perforation_short:
                for interval in well_data.dict_perforation_short[plast]["интервал"]:
                    plast_str += f'{plast[:4]}: {interval[0]}- {interval[1]} \n'
            elif well_data.dict_perforation_short[plast]['отключение'] and plast in well_data.dict_perforation_short:
                for interval in well_data.dict_perforation_short[plast]["интервал"]:
                    plast_str += f'{plast[:4]} :{interval[0]}- {interval[1]} (изол)\n'

            filter_list_pressuar = list(
                filter(lambda x: type(x) in [int, float], list(well_data.dict_perforation_short[plast]["давление"])))
            # print(f'фильтр -{filter_list_pressuar}')
            if filter_list_pressuar:
                pressur_set.add(f'{plast[:4]} - {filter_list_pressuar}')

        ws4.cell(row=6, column=1).value = f'НКТ: \n {TabPage_Gno.gno_nkt_opening(well_data.dict_nkt)}'
        ws4.cell(row=7, column=1).value = f'Рпл: \n {" ".join(list(pressur_set))}атм'
        # ws4.cell(row=8, column=1).value = f'ЖГС = {well_data.fluid_work_short}г/см3'
        ws4.cell(row=9,
                 column=1).value = f'Нст- {well_data.static_level._value}м / Ндин - {well_data.dinamic_level._value}м'
        if well_data.curator == 'ОР':
            ws4.cell(row=10, column=1).value = f'Ожид {well_data.expected_Q}м3/сут при Р-{well_data.expected_P}м3/сут'
        else:
            ws4.cell(row=10, column=1).value = f'Qн {well_data.Qoil}т Qж- {well_data.Qwater}м3/сут'
        ws4.cell(row=11, column=1).value = f'макс угол {well_data.max_angle._value} на {well_data.max_angle_H._value}'
        ws4.cell(row=1, column=2).value = well_data.cdng._value
        ws4.cell(row=2, column=3).value = \
            f'Рпл - {well_data.dict_category[well_data.plast_work_short[0]]["по давлению"].category},' \
            f' H2S -{well_data.dict_category[well_data.plast_work_short[0]]["по сероводороду"].category},' \
            f' газ факт -{well_data.gaz_f_pr[0]}т/м3'
        column_well = f'{well_data.column_diametr._value}х{well_data.column_wall_thickness._value} в инт 0 - {well_data.shoe_column._value}м ' \
            if well_data.column_additional is False else f'{well_data.column_diametr._value} х {well_data.column_wall_thickness._value} \n' \
                                                         f'0 - {well_data.shoe_column._value}м/\n{well_data.column_additional_diametr._value}' \
                                                         f' х {well_data.column_additional_wall_thickness._value} в инт ' \
                                                         f'{well_data.head_column_additional._value}-{well_data.head_column_additional._value}м'
        ws4.cell(row=1, column=7).value = column_well
        ws4.cell(row=4, column=7).value = f'Пробур забой {well_data.bottomhole_drill._value}м'
        ws4.cell(row=5, column=7).value = f'Исскус забой {well_data.bottomhole_artificial._value}м'
        ws4.cell(row=6, column=7).value = f'Тек забой {well_data.bottom}м'

        ws4.cell(row=7, column=7).value = plast_str
        ws4.cell(row=11, column=7).value = f'Рмакс {well_data.max_admissible_pressure._value}атм'
        ws4.cell(row=3, column=2).value = plan_short
        nek_str = 'НЭК '
        if len(well_data.leakiness_interval) != 0:

            for nek in well_data.leakiness_interval:
                nek_str += f'{nek.split("-")[0]}-{nek.split("-")[1]} \n'

        ws4.cell(row=3, column=7).value = nek_str

        ws4.insert_rows(1, 2)
        ws4.insert_cols(1, 2)
        ws4.cell(row=2, column=3).value = 'Краткое содержание плана работ'
        ws4.cell(row=2, column=3).font = Font(name='Arial', size=16, bold=True)

        # объединение ячеек
        ws4.merge_cells(start_row=2, start_column=3, end_row=2, end_column=9)  # Объединение оглавления
        ws4.merge_cells(start_row=5, start_column=3, end_row=7, end_column=3)  # Объединение строк ГНО
        ws4.merge_cells(start_row=4, start_column=5, end_row=4, end_column=6)  # объединение по класси
        ws4.merge_cells(start_row=3, start_column=9, end_row=4, end_column=9)  # Объединение строк данных по колонну
        ws4.merge_cells(start_row=9, start_column=9, end_row=12, end_column=9)
        ws4.merge_cells(start_row=5, start_column=4, end_row=13, end_column=8)

        for row_ind in range(3, 15):
            ws4.row_dimensions[row_ind].height = 80
            for col in range(3, 10):
                if row_ind == 3:
                    ws4.column_dimensions[get_column_letter(col)].width = 20

                ws4.cell(row=row_ind, column=col).border = well_data.thin_border
                ws4.cell(row=row_ind, column=col).font = Font(name='Arial', size=13, bold=False)
                ws4.cell(row=row_ind, column=col).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')
        ws4.cell(row=5, column=4).font = Font(name='Arial', size=11, bold=False)
        ws4.hide = True
        ws4.page_setup.fitToPage = True
        ws4.page_setup.fitToHeight = False

        ws4.page_setup.fitToWidth = True
        ws4.print_area = 'C2:I14'

    def check_gpp_upa(self, table_widget):
        for row in range(table_widget.rowCount()):
            for column in range(table_widget.columnCount()):
                value = self.table_widget.item(row, column)
                if value != None:
                    value = value.text()
                    if 'Установить подъёмный агрегат на устье не менее 40т' in value:
                        new_value = QtWidgets.QTableWidgetItem(f'Установить подъёмный агрегат на устье не менее 60т. '
                                                               f'Пусковой комиссией составить акт готовности подьемного '
                                                               f'агрегата и бригады для проведения ремонта скважины.')
                        table_widget.setItem(row, column, new_value)

    def check_true_depth_template(self, depth):
        check = True
        if well_data.column_additional:

            if well_data.template_depth_addition < depth and depth > well_data.head_column_additional._value:
                check = False
                check_question = QMessageBox.question(self, 'Проверка глубины пакера',
                                                      f'Проверка показало что пакер с глубиной {depth}м спускается ниже '
                                                      f'глубины  {well_data.template_depth_addition}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True
            if well_data.template_depth < depth and depth < well_data.head_column_additional._value:
                check = False
                check_question = QMessageBox.question(self, 'Проверка глубины пакера',
                                                      f'Проверка показало что пакер с глубиной {depth}м спускается ниже '
                                                      f'глубины  {well_data.template_depth}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True
        else:
            # print(f'глубина {well_data.template_depth, depth}')
            if well_data.template_depth < depth:
                check = False
                check_question = QMessageBox.question(self, 'Проверка глубины пакера',
                                                      f'Проверка показало что пакер с глубиной {depth}м спускается ниже '
                                                      f'глубины  {well_data.template_depth}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True

        return check

    def true_set_Paker(self, depth):

        check_true = False


        for plast in well_data.plast_all:
            if len(well_data.dict_perforation[plast]['интервал']) >= 1:
                for interval in well_data.dict_perforation[plast]['интервал']:
                    if interval[0] < depth < interval[1]:
                        check_true = False
                    else:
                        check_true = True
            elif len(well_data.dict_perforation[plast]['интервал']) == 0:
                check_true = True

        if check_true is False:
            paker_warning = QMessageBox.warning(None, 'Проверка посадки пакера в интервал перфорации',
                                                f'Проверка посадки показала пакер сажается в интервал перфорации, '
                                                f'необходимо изменить глубину посадки!!!')

        return check_true

    def check_str_isdigit(self, string):

        # Паттерн для проверки: допустимы только цифры, точка и запятая
        pattern = r'^[\d.,]+$'

        # Проверка строки на соответствие паттерну
        if re.match(pattern, string):
            return True
        else:
            return False

    def check_depth_in_skm_interval(self, depth):
        check_true = False

        if any([interval[0] <= depth <= interval[1] for interval in well_data.skm_interval]):
            check_true = True
            return int(depth)
        else:
            false_question = QMessageBox.question(None, 'Проверка посадки пакера в интервал скреперования',
                                                  f'Проверка посадки показала, что пакер сажается не '
                                                  f'в интервал скреперования, '
                                                  f'Проигнорировать ошибку?')
            if false_question == QMessageBox.StandardButton.Yes:
                return True
            else:
                kroly_skm = depth - 20
                pod_skm = depth + 20
                skm = (kroly_skm, pod_skm)
                perforating_intervals = []

                skm_question = QMessageBox.question(None, 'Скреперование',
                                                    f'добавить интервал скреперования {skm}')
                if skm_question == QMessageBox.StandardButton.Yes:
                    well_data.skm_interval.append(skm)
                    well_data.skm_interval = sorted(well_data.skm_interval, key=lambda x: x[0])
                    raid_str = raid(remove_overlapping_intervals(perforating_intervals, well_data.skm_interval))
                    # print(f'скреперование {well_data.skm_interval}')
                    for row in range(self.table_widget.rowCount()):
                        for column in range(self.table_widget.columnCount()):
                            value = self.table_widget.item(row, column)
                            if value != None:
                                value = value.text()
                                if 'Произвести скреперование' in value:
                                    ind_value = value.split(' ')
                                    ind_min = ind_value.index('интервале') + 1
                                    ind_max = ind_value.index('обратной')
                                    new_value = QtWidgets.QTableWidgetItem(f'{" ".join(ind_value[:ind_min])} '
                                                                           f'{raid_str}м {" ".join(ind_value[ind_max:])}')

                                    self.table_widget.setItem(row, column, new_value)
                    return True
                else:
                    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
