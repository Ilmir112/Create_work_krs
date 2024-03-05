import os
import sqlite3
import sys
import win32com.client
import openpyxl
from openpyxl.reader.excel import load_workbook

from collections import namedtuple

import krs
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, \
    QLineEdit, QFileDialog, QToolBar, QPushButton, QMessageBox, QInputDialog, QTabWidget
from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from openpyxl.utils import get_column_letter
from PyQt5.QtCore import Qt
from openpyxl.workbook import Workbook
from openpyxl.styles import Border, Side, Alignment, Font

from openpyxl.drawing.image import Image

from H2S import calc_H2S
from PyQt5.QtCore import QThread, pyqtSignal
from data_correct_position_people import CorrectSignaturesWindow
from data_base.work_with_base import Classifier_well



class ExcelWorker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()


    def check_well_existence(self, well_number, deposit_area, region):
        # print(f'jghfjlt {well_number, deposit_area, region}')


        # Подключение к базе данных SQLite
        conn = sqlite3.connect('data_base/database_without_juming.db')
        cursor = conn.cursor()
        current_year = datetime.now().year
        month = datetime.now().month
        print(f'месяц {month}')
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
                mes = QMessageBox.information(self, 'перечень без глушения',
                                              f'Скважина состоит в перечне скважин без глушения на текущий квартал, '
                                              f'в перечне от {date_reload} {region}')
                check_true = True
            else:
                check_true = False

        if region == 'ИГМ':
            # Проверка наличия записи в базе данных
            cursor.execute(f"SELECT *  FROM ИГМ WHERE today =?", (date_string,))

            result = cursor.fetchone()
            if result is None:
                mes = QMessageBox.warning(self, 'Некорректная дата перечня',
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


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.new_window = None
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
        # self.table_widget = table_widget
        self.ins_ind_border = None
        self.work_plan = 0

    def initUI(self):

        self.setWindowTitle("Main Window")
        self.setGeometry(200, 100, 800, 800)

        self.table_widget = None

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
        self.classifierMenu = QMenu('&Классификатор', self)
        self.signatories = QMenu('&Подписанты ', self)
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.classifierMenu)
        self.menuBar.addMenu(self.signatories)

        self.create_file = self.fileMenu.addMenu('&Создать')
        self.create_KRS = self.create_file.addAction('План КРС', self.action_clicked)
        self.create_KRS_DP = self.create_file.addAction('Дополнительный план', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_GNKT_OPZ = self.create_GNKT.addAction('ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('Фрезерование', self.action_clicked)
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
        action = self.sender()
        if action == self.create_KRS:
            self.work_plan = 'krs'
            self.tableWidgetOpen(self.work_plan)
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                try:
                    self.read_pz(self.fname)
                    CreatePZ.pause = True
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
                    CreatePZ.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.copy_pz(sheet, self.table_widget, self.work_plan)

                except FileNotFoundError:
                    print('Файл не найден')

        elif action == self.create_GNKT_OPZ:
            self.work_plan = 'gnkt_opz'
            self.tableWidgetOpen(self.work_plan)

            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',"Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            if self.fname:
                try:
                    self.read_pz(self.fname)
                    CreatePZ.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    print(f' ГНКТ {self.work_plan}')
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)
                    self.copy_pz(sheet, self.table_widget, self.work_plan)


                except FileNotFoundError:
                    print('Файл не найден')

                # if action == self.save_file:
                #     open_pz.open_excel_file().wb.save("test_unmerge.xlsx")

        elif action == self.create_GNKT_frez:
            self.work_plan = 'gnkt_frez'
            self.tableWidgetOpen(self.work_plan)

            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            if self.fname:
                try:
                    self.read_pz(self.fname)
                    CreatePZ.pause = True
                    read_pz = CreatePZ(self.wb, self.ws, self.data_window, self.perforation_correct_window2)
                    sheet = read_pz.open_excel_file(self.ws, self.work_plan)

                    self.rir_window = Work_with_gnkt(self.ws, self.tabWidget,
                                                     self.table_title, self.table_schema, self.table_widget,)

                    CreatePZ.pause_app(self)
                    CreatePZ.pause = True
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
                print('Подписанты')
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

    def reload_class_well(self, costumer, region):
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                              "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if self.fname:
            try:
                copy = Classifier_well.export_to_sqlite_class_well(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    def open_without_damping(self, costumer, region):

        if self.new_window is None:

            self.new_window = Classifier_well(costumer, region, 'damping')
            self.new_window.setWindowTitle("Перечень скважин без глушения")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def open_class_well(self, costumer, region):
        if self.new_window is None:

            self.new_window = Classifier_well(costumer, region, 'classifier_well')
            self.new_window.setWindowTitle("Классификатор")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def reload_without_damping(self, costumer, region):

        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                              "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if self.fname:
            try:
                copy = Classifier_well.export_to_sqlite_without_juming(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    # def tableDampingWidgetOpen(self):
    #     if self.table_juming is None:
    #         self.table_juming = QTableWidget()
    #
    #         self.table_juming.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
    #         self.table_juming.customContextMenuRequested.connect(self.openContextMenu)
    #         self.setCentralWidget(self.table_juming)
    #         self.model = self.table_juming.model()
    #
    #         # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
    #         # Указанная строка и столбец - это ячейка, которая была нажата.
    #         self.table_juming.cellPressed[int, int].connect(self.clickedRowColumn)

    # def tableClassifisierOpen(self):
    #     if self.table_class is None:
    #         self.new_window = Classifier_well()
    #         self.new_window.setWindowTitle("Классификатор")
    #         self.new_window.setGeometry(200, 400, 300, 400)
    #         self.new_window.show()





    def tableWidgetOpen(self, work_plan = 'krs'):

        if self.table_widget is None:

            # Создание объекта TabWidget
            self.tabWidget = QTabWidget()

            self.table_widget = QTableWidget()

            self.table_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_widget.customContextMenuRequested.connect(self.openContextMenu)
            self.setCentralWidget(self.tabWidget)
            self.model = self.table_widget.model()

            # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
            # Указанная строка и столбец - это ячейка, которая была нажата.
            self.table_widget.cellPressed[int, int].connect(self.clickedRowColumn)
            if work_plan == 'gnkt_frez':
                self.table_title = QTableWidget()
                self.tabWidget.addTab(self.table_title, 'Титульник')
                self.table_schema = QTableWidget()
                self.tabWidget.addTab(self.table_schema , 'Схема скважины')


            self.tabWidget.addTab(self.table_widget, 'Ход работ')


    def saveFileDialog(self, wb2, full_path):
        from open_pz import CreatePZ
        fileName, _ = QFileDialog.getSaveFileName(self, "Save excel-file",
                                                  f"{full_path}", "Excel Files (*.xlsx)")
        if fileName:
            wb2.save(full_path)
        # Создаем объект Excel
        excel = win32com.client.Dispatch("Excel.Application")

        # Открываем файл
        workbook = excel.Workbooks.Open(full_path)

        # Отображаем Excel
        excel.Visible = True

    def save_to_excel(self):
        from work_py.gnkt_frez import Work_with_gnkt

        if self.work_plan != 'gnkt_frez':
            self.save_to_krs()
        else:
            Work_with_gnkt.save_to_gnkt(self)



    def save_to_krs(self):
        from open_pz import CreatePZ
        if not self.table_widget is None:
            wb2 = Workbook()
            ws2 = wb2.get_sheet_by_name('Sheet')
            ws2.title = "План работ"
            # print(f'открытие wb2')

            ins_ind = self.ins_ind_border

            # print(f'открытие wb2 - {ins_ind}')

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
                        row_lst.append(item.text())
                        # print(item.text())
                    else:
                        row_lst.append("")

                work_list.append(row_lst)

            merged_cells_dict = {}
            # print(f' индекс объ {ins_ind}')
            for row in merged_cells:
                if row[0] >= ins_ind - 1:
                    merged_cells_dict.setdefault(row[0], []).append(row[1])
            plan_short = ''

            for i in range(2, len(work_list)):  # нумерация работ
                if i >= ins_ind + 2:
                    work_list[i][1] = i - 1 - ins_ind
                    if krs.is_number(work_list[i][11]) == True:
                        CreatePZ.normOfTime += float(str(work_list[i][11]).replace(',', '.'))
                    if work_list[i][0]:
                        plan_short += f'п.{work_list[i][1]} {work_list[i][0]} \n'

            # print(f'Нормы времени - {CreatePZ.normOfTime}')
            # print(f'строки {ins_ind}')
            CreatePZ.count_row_height(self.ws, ws2, work_list, merged_cells_dict, ins_ind)
            # print(f'3 - {ws2.max_row}')
            CreatePZ.itog_ind_min = self.ins_ind_border
            CreatePZ.itog_ind_max = len(work_list)
            # print(f' длина {len(work_list)}')
            CreatePZ.addItog(self, ws2, self.table_widget.rowCount() + 1, self.work_plan)
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

            self.create_short_plan(wb2, plan_short)

            # print(f'9 - {ws2.max_row}')
            if self.work_plan != 'dop_plan':
                self.insert_image(ws2, 'imageFiles/Хасаншин.png', 'H1')
                self.insert_image(ws2, 'imageFiles/Шамигулов.png', 'H4')

                cat_H2S_list = CreatePZ.dict_category[CreatePZ.plast_work[0]]['по сероводороду'].category
                H2S_mg = CreatePZ.dict_category[CreatePZ.plast_work[0]]['по сероводороду'].data_mg_l
                H2S_pr = CreatePZ.dict_category[CreatePZ.plast_work[0]]['по сероводороду'].data_procent

                if cat_H2S_list  in [1, 2] and self.work_plan != 'dop_plan':
                    ws3 = wb2.create_sheet('Sheet1')
                    ws3.title = "Расчет необходимого количества поглотителя H2S"
                    ws3 = wb2["Расчет необходимого количества поглотителя H2S"]
                    calc_H2S(ws3, H2S_pr, H2S_mg)
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
            filenames = f"{CreatePZ.well_number._value} {CreatePZ.well_area._value} кат {CreatePZ.cat_P_1} {self.work_plan}.xlsx"
            full_path = path + '/' + filenames
            # print(f'10 - {ws2.max_row}')
            # print(wb2.path)
            # print(f' кате {CreatePZ.cat_P_1}')
            if CreatePZ.bvo:
                ws5 = wb2.create_sheet('Sheet1')
                ws5.title = "Схемы ПВО"
                ws5 = wb2["Схемы ПВО"]
                wb2.move_sheet(ws5, offset=-1)
                schema_list = self.check_pvo_schema(ws5, ins_ind + 2)

            if wb2:
                wb2.close()
                self.saveFileDialog(wb2, full_path)
                # wb2.save(full_path)
                print(f"Table data saved to Excel {full_path} {CreatePZ.number_dp}")
            if self.wb:
                self.wb.close()

    def close_file(self):
        from find import ProtectedIsNonNone
        from open_pz import CreatePZ
        if not self.table_widget is None:
            self.table_widget.close()
            self.table_widget = None
            CreatePZ.normOfTime = 0
            CreatePZ.gipsInWell = False
            CreatePZ.grpPlan = False
            CreatePZ.nktOpressTrue = False
            CreatePZ.bottomhole_drill = 0
            CreatePZ.open_trunk_well = False
            CreatePZ.normOfTime = 0
            CreatePZ.lift_ecn_can = False
            CreatePZ.pause = True
            CreatePZ.curator = '0'
            CreatePZ.lift_ecn_can_addition = False
            CreatePZ.column_passability = False
            CreatePZ.column_additional_passability = False
            CreatePZ.template_depth = 0

            CreatePZ.b_plan = 0
            CreatePZ.pipes_ind = 0
            CreatePZ.sucker_rod_ind = 0
            CreatePZ.expected_Q = 0
            CreatePZ.expected_P = 0
            CreatePZ.plast_select = ''
            CreatePZ.dict_perforation = {}
            CreatePZ.dict_perforation_project = {}
            CreatePZ.itog_ind_min = 0
            CreatePZ.kat_pvo = 2
            CreatePZ.gaz_f_pr = []
            CreatePZ.paker_layout = 0
            CreatePZ.cat_P_P = []
            CreatePZ.column_direction_diametr = ProtectedIsNonNone('отсут')
            CreatePZ.column_direction_wall_thickness = ProtectedIsNonNone('отсут')
            CreatePZ.column_direction_lenght = ProtectedIsNonNone('отсут')
            CreatePZ.column_conductor_diametr = ProtectedIsNonNone('отсут')
            CreatePZ.column_conductor_wall_thickness = ProtectedIsNonNone('отсут')
            CreatePZ.column_conductor_lenght = ProtectedIsNonNone('отсут')
            CreatePZ.column_additional_diametr = ProtectedIsNonNone('отсут')
            CreatePZ.column_additional_wall_thickness = ProtectedIsNonNone('отсут')
            CreatePZ.head_column_additional = ProtectedIsNonNone('отсут')
            CreatePZ.shoe_column_additional = ProtectedIsNonNone('отсут')
            CreatePZ.column_diametr = ProtectedIsNonNone('отсут')
            CreatePZ.column_wall_thickness = ProtectedIsNonNone('отсут')
            CreatePZ.shoe_column = ProtectedIsNonNone('отсут')
            CreatePZ.column_additional_diametr = 0
            CreatePZ.column_additional_wall_thickness = 0
            CreatePZ.shoe_column_additional = 0
            CreatePZ.column_diametr = 0
            CreatePZ.column_wall_thickness = 0
            CreatePZ.shoe_column = 0
            CreatePZ.bottomhole_artificial = 0
            CreatePZ.max_expected_pressure = 0
            CreatePZ.head_column_additional = 0
            CreatePZ.leakiness_Count = 0
            CreatePZ.expected_pick_up = {}
            CreatePZ.current_bottom = 0
            CreatePZ.fluid_work = 0
            CreatePZ.static_level = 0
            CreatePZ.dinamic_level = 0
            CreatePZ.work_perforations_approved = False
            CreatePZ.dict_leakiness = {}
            CreatePZ.leakiness = False
            CreatePZ.emergency_well = False
            CreatePZ.emergency_count = 0
            CreatePZ.skm_interval = []
            CreatePZ.work_perforations = []
            CreatePZ.work_perforations_dict = {}
            CreatePZ.paker_do = {"do": 0, "posle": 0}
            CreatePZ.column_additional = False
            CreatePZ.well_number = None
            CreatePZ.well_area = None
            CreatePZ.values = []
            CreatePZ. H_F_paker_do = {"do": 0, "posle": 0}
            CreatePZ.paker2_do = {"do": 0, "posle": 0}
            CreatePZ.H_F_paker2_do = {"do": 0, "posle": 0}
            CreatePZ.perforation_roof = 50000
            CreatePZ.data_x_min = 0
            CreatePZ.perforation_sole = 0
            CreatePZ.dict_pump_SHGN = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_ECN = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_SHGN_h = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_ECN_h = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump = {"do": '0', "posle": '0'}
            CreatePZ.leakiness_interval = []
            CreatePZ.dict_pump_h = {"do": 0, "posle": 0}
            CreatePZ.ins_ind = 0
            CreatePZ.len_razdel_1 = 0
            CreatePZ.count_template = 0
            CreatePZ.cat_P_1 = []
            CreatePZ.countAcid = 0
            CreatePZ.swabTypeComboIndex = 1
            CreatePZ.swabTrueEditType = 1
            CreatePZ.data_x_max = 0
            CreatePZ.drilling_interval = []
            CreatePZ.max_angle = 0
            CreatePZ.pakerTwoSKO = False
            CreatePZ.privyazkaSKO = 0
            CreatePZ.H2S_pr = []
            CreatePZ.cat_H2S_list = []
            CreatePZ.H2S_mg = []
            CreatePZ.lift_key = 0
            CreatePZ.max_admissible_pressure = 0
            CreatePZ.region = ''
            CreatePZ.dict_nkt = {}
            CreatePZ.dict_nkt_po = {}
            CreatePZ.data_well_max = 0
            CreatePZ.data_pvr_max = 0
            CreatePZ.dict_sucker_rod = {}
            CreatePZ.dict_sucker_rod_po = {}
            CreatePZ.row_expected = []
            CreatePZ.rowHeights = []
            CreatePZ.plast_project = []
            CreatePZ.plast_work = []
            CreatePZ.plast_all = []
            CreatePZ.condition_of_wells = 0
            CreatePZ.cat_well_min = 0
            CreatePZ.bvo = False
            CreatePZ.old_version = False
            CreatePZ.image_list = []
            CreatePZ.problem_with_ek = False
            CreatePZ.problem_with_ek_depth = CreatePZ.current_bottom
            CreatePZ.problem_with_ek_diametr = CreatePZ.column_diametr
            path = "imageFiles/image_work"
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)


        print("Closing current file")

    def on_finished(self):
        print("Работа с файлом Excel завершена.")
    def insert_image(self, ws, file, coordinate, width = 200, height = 180):
        # Загружаем изображение с помощью библиотеки Pillow
        print(f'vtcnj {file}')
        img = openpyxl.drawing.image.Image(file)
        img.width = width
        img.height = height
        img.anchor = coordinate
        ws.add_image(img, coordinate)

    def openContextMenu(self, position):
        from open_pz import CreatePZ


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

        czh_action = QAction("Установка цементными желонками", self)
        geophysical.addAction(czh_action)
        czh_action.triggered.connect(self.czh_action)

        swibbing_action = QAction("Свабирование со пакером", self)
        geophysical.addAction(swibbing_action)
        swibbing_action.triggered.connect(self.swibbing_with_paker)

        swibbing2_action = QAction("Свабирование с двумя пакерами", self)
        geophysical.addAction(swibbing2_action)
        swibbing2_action.triggered.connect(self.swibbing2_with_paker)

        swabbing_opy_action = QAction("ГИС ОПУ", self)
        geophysical.addAction(swabbing_opy_action)
        swabbing_opy_action.triggered.connect(self.swabbing_opy)

        swibbingVoronka_action = QAction("Свабирование со воронкой", self)
        geophysical.addAction(swibbingVoronka_action)
        swibbingVoronka_action.triggered.connect(self.swibbing_with_voronka)

        kompressVoronka_action = QAction("Освоение компрессором с воронкой", self)
        geophysical.addAction(kompressVoronka_action)
        kompressVoronka_action.triggered.connect(self.kompress_with_voronka)

        del_menu = context_menu.addMenu('удаление строки')
        emptyString_action = QAction("добавить пустую строку", self)
        del_menu.addAction(emptyString_action)
        emptyString_action.triggered.connect(self.emptyString)

        gnkt_menu = context_menu.addMenu("ГНКТ")
        gnkt_opz_action = QAction("ГНКТ ОПЗ", self)
        gnkt_menu.addAction(gnkt_opz_action)
        gnkt_opz_action.triggered.connect(self.gnkt_opz)

        gnkt_opz_action = QAction("ГНКТ Освоение после ГРП", self)
        gnkt_menu.addAction(gnkt_opz_action)
        gnkt_opz_action.triggered.connect(self.gnkt_after_grp)

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
        ryber_action.triggered.connect(self.ryberAdd)

        drilling_menu = action_menu.addMenu('Бурение')

        drilling_action_nkt = QAction("бурение на НКТ", self)
        drilling_menu.addAction(drilling_action_nkt)
        drilling_action_nkt.triggered.connect(self.drilling_action_nkt)

        frezering_port_action = QAction("Фрезерование портов", self)
        drilling_menu.addAction(frezering_port_action)
        frezering_port_action.triggered.connect(self.frezering_port_action)

        drilling_SBT_action = QAction("бурение на СБТ", self)
        drilling_menu.addAction(drilling_SBT_action)
        drilling_SBT_action.triggered.connect(self.drilling_SBT_action)

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
        acid_action1paker = QAction("окно на одном пакере", self)
        acid_menu.addAction(acid_action1paker)
        acid_action1paker.triggered.connect(self.acidPakerNewWindow)

        acid_action2paker = QAction("окно на двух пакерах", self)
        acid_menu.addAction(acid_action2paker)
        acid_action2paker.triggered.connect(self.acid2PakerNewWindow)



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
        from open_pz import CreatePZ
        self.ins_ind = r + 1
        CreatePZ.ins_ind = r + 1
        # print(f' выбранная строка {self.ins_ind}')

    def drilling_SBT_action(self):
        from work_py.drilling import drilling_sbt
        drilling_work_list = drilling_sbt(self)
        self.populate_row(self.ins_ind, drilling_work_list, self.table_widget)

    def frezering_port_action(self):
        from work_py.drilling import frezer_ports
        drilling_work_list = frezer_ports(self)
        self.populate_row(self.ins_ind, drilling_work_list, self.table_widget)
    def drilling_action_nkt(self):
        from work_py.drilling import drilling_nkt
        drilling_work_list = drilling_nkt(self)
        self.populate_row(self.ins_ind, drilling_work_list, self.table_widget)

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
        kot_work_list = kot_work(self)
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
        from work_py.alone_oreration import fluid_change
        fluid_change_work_list = fluid_change(self)
        self.populate_row(self.ins_ind, fluid_change_work_list, self.table_widget)
    def claySolision(self):
        from work_py.claySolution import claySolutionDef
        rirRpp_work_list = claySolutionDef(self)
        self.populate_row(self.ins_ind, rirRpp_work_list, self.table_widget)
    def rirAction(self):
        from work_py.rir import RirWindow

        from open_pz import CreatePZ
        print(f' окно СКО ')
        # CreatePZ.pause = False
        if self.rir_window is None:
            CreatePZ.countAcid = 0
            print(f' окно2 СКО ')
            self.rir_window = RirWindow(self.table_widget, CreatePZ.ins_ind)
            self.rir_window.setGeometry(200, 400, 300, 400)
            self.rir_window.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.rir_window = None
        else:
            self.rir_window.close()  # Close window.
            self.rir_window is None

    def grpWithPaker(self):
        from work_py.grp import grpPaker

        print('Вставился ГРП с пакером')
        grpPaker_work_list = grpPaker(self)
        self.populate_row(self.ins_ind, grpPaker_work_list, self.table_widget)

    def grpWithGpp(self):
        from work_py.grp import grpGpp

        print('Вставился ГРП с ГПП')
        grpGpp_work_list = grpGpp(self)
        self.populate_row(self.ins_ind, grpGpp_work_list, self.table_widget)

    def filling_sand(self):
        from work_py.sand_filling import sandFilling

        print('Вставился отсыпка песком')
        filling_work_list = sandFilling(self)
        self.populate_row(self.ins_ind, filling_work_list, self.table_widget)

    def washing_sand(self):
        from work_py.sand_filling import sandWashing

        print('Вставился отсыпка песком')
        washing_work_list = sandWashing(self)
        self.populate_row(self.ins_ind, washing_work_list, self.table_widget)

    def deleteString(self):
        selected_ranges = self.table_widget.selectedRanges()
        selected_rows = []

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
            self.table_widget.removeRow(row)

    def emptyString(self):
        ryber_work_list = [[None, None, None, None, None, None, None, None, None, None, None, None]]
        self.populate_row(self.ins_ind, ryber_work_list, self.table_widget)

    def vp_action(self):
        from work_py.vp_cm import vp

        print('Вставился ВП')
        vp_work_list = vp(self)
        self.populate_row(self.ins_ind, vp_work_list, self.table_widget)

    def czh_action(self):
        from work_py.vp_cm import czh

        print('Вставился ВП')
        vp_work_list = czh(self)
        self.populate_row(self.ins_ind, vp_work_list, self.table_widget)

    def swibbing_with_paker(self):
        from work_py.swabbing import swabbing_with_paker

        print('Вставился Сваб с пакером')
        swab_work_list = swabbing_with_paker(self, 10, 1)
        self.populate_row(self.ins_ind, swab_work_list, self.table_widget)

    def swibbing2_with_paker(self):
        from work_py.swabbing import swabbing_with_2paker

        print('Вставился Сваб с пакером')
        swab_work_list = swabbing_with_2paker(self)
        self.populate_row(self.ins_ind, swab_work_list, self.table_widget)

    def swabbing_opy(self):
        from work_py.swabbing import swabbing_opy

        print('Вставился ОПУ')
        swabbing_opy_list = swabbing_opy(self)
        self.populate_row(self.ins_ind, swabbing_opy_list, self.table_widget)

    def kompress_with_voronka(self):
        from work_py.kompress import kompress

        print('Вставился компрессор с воронкой')
        kompress_work_list = kompress(self)
        self.populate_row(self.ins_ind, kompress_work_list, self.table_widget)

    def swibbing_with_voronka(self):

        from work_py.swabbing import swabbing_with_voronka

        print('Вставился Сваб с воронкой')
        swab_work_list = swabbing_with_voronka(self)
        self.populate_row(self.ins_ind, swab_work_list, self.table_widget)

    def ryberAdd(self):
        from work_py.raiding import Raid

        print('Вставился райбер')
        ryber_work_list = Raid.raidingColumn(self)
        self.populate_row(self.ins_ind, ryber_work_list, self.table_widget)

    def gnkt_after_grp(self):
        from gnkt_after_grp import gnkt_work
        gnkt_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, gnkt_work_list, self.table_widget)

    def gnkt_opz(self):
        from gnkt_opz import gnkt_work

        print('Вставился ГНКТ')
        ryber_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, ryber_work_list, self.table_widget)

    def gno_bottom(self):
        from work_py.descent_gno import gno_down

        print('Вставился ГНО')
        gno_work_list = gno_down(self)
        self.populate_row(self.ins_ind, gno_work_list, self.table_widget)

    def acid_action_1paker(self):
        from work_py.acids_work import acid_work
        from open_pz import CreatePZ
        if len(CreatePZ.plast_work) == 0:
            msc = QMessageBox.information(self, 'Внимание', 'Отсутствуют рабочие интервалы перфорации')
            return
        CreatePZ.paker_layout = 1
        print('Вставился кислотная обработка на одном пакере ')
        acid_work_list = acid_work(self)
        if acid_work_list != None:
            self.populate_row(self.ins_ind, acid_work_list, self.table_widget)

    def acid_action_2paker(self):
        from work_py.acids import acid_work
        from open_pz import CreatePZ

        if len(CreatePZ.plast_work) == 0:
            msc = QMessageBox.information(self, 'Внимание', 'Отсутствуют рабочие интервалы перфорации')
            return
        CreatePZ.paker_layout = 2
        print('Вставился кислотная обработка на двух пакере ')
        acid_work_list = acid_work(self)
        if acid_work_list != None:
            self.populate_row(self.ins_ind, acid_work_list, self.table_widget)

    def pressureTest(self):
        from work_py.opressovka import OpressovkaEK
        from open_pz import CreatePZ


        if self.work_window is None:
            self.work_window = OpressovkaEK(self.table_widget, self.ins_ind)
            self.work_window.setGeometry(200, 400, 300, 400)
            self.work_window.show()
            CreatePZ.pause_app(self)
            work_list = OpressovkaEK.addRowTable()
            # print(work_list)
            CreatePZ.pause = True
            self.populate_row(self, CreatePZ.ins_ind, work_list)
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
        from open_pz import CreatePZ
        print(f' окно СКО ')

        if self.acid_windowPaker2 is None:
            self.acid_windowPaker2 = TemplateKrs(self.table_widget, CreatePZ.ins_ind)
            self.acid_windowPaker2.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker2.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.acid_windowPaker2 = None
        else:
            self.acid_windowPaker2.close()  # Close window.
            self.acid_windowPaker2 = None

    def template_without_skm(self):
        from work_py.template_work import TemplateKrs
        from open_pz import CreatePZ

        template_ek_list = TemplateKrs.template_ek_without_skm(self)
        # print()
        # print(f'индекс {self.ins_ind, len(template_ek_list)}')
        self.populate_row(self.ins_ind, template_ek_list, self.table_widget)
        CreatePZ.ins_ind += len(template_ek_list) + 1

    def populate_row(self, ins_ind, work_list, table_widget):
        # print(type(table_widget))
        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 1500)}
        index_setSpan = 0
        if self.work_plan == 'gnkt_frez':
            index_setSpan = 1

        for i, row_data in enumerate(work_list):
            row = ins_ind + i
            self.table_widget.insertRow(row)
            # print(f'при Х{row_data}')
            if len(str(row_data[1])) > 3 and self.work_plan == 'gnkt_frez':
                self.table_widget.setSpan(i + ins_ind, 1, 1, 12)
            else:
                self.table_widget.setSpan(i + ins_ind, 2, 1, 8 + index_setSpan)
            for column, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                # widget = QtWidgets.QLabel(str())
                # widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')

                # self.table_widget.setCellWidget(row, column, widget)

                if not data is None:
                   self.table_widget.setItem(row, column, item)

                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if not data is None:
                        text = data
                        # print(text)
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))


        print(f'закончено')

        # self.table_widget.setEditTriggers(QTableWidget.AnyKeyPressed)
        # self.table_widget.resizeColumnsToContents()
        # self.table_widget.resizeRowsToContents()

    def acid2PakerNewWindow(self):
        from work_py.acid_2paker import AcidPakerWindow
        from open_pz import CreatePZ
        print(f' окно СКО ')


        if self.acid_windowPaker2 is None:
            CreatePZ.countAcid = 0
            print(f' окно2 СКО ')
            self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, 0)
            self.acid_windowPaker2.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker2.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.acid_windowPaker2 = None
            self.reply2_acid()
        else:
            self.acid_windowPaker2.close()  # Close window.
            self.acid_windowPaker2 = None

    def acidPakerNewWindow(self):
        from work_py.acid_paker import AcidPakerWindow
        from open_pz import CreatePZ
        print(f' окно СКО ')

        if self.acid_windowPaker is None:
            CreatePZ.countAcid = 0
            print(f' окно2 СКО ')
            self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, 0)
            self.acid_windowPaker.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            CreatePZ.countAcid = 0
            self.acid_windowPaker = None
            self.reply_acid()
        else:
            self.acid_windowPaker.close()  # Close window.
            self.acid_windowPaker = None

    def reply2_acid(self):
        from open_pz import CreatePZ
        from work_py.acid_2paker import AcidPakerWindow

        acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                               'Нужно ли планировать кислоту на следующий объет?')

        if acid_true_quest == QMessageBox.StandardButton.Yes:
            if self.acid_windowPaker2 is None:
                CreatePZ.countAcid = 1
                print(f' окно2 СКО ')
                self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker2.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker2.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker2 = None
                self.reply2_acid()
            else:
                self.acid_windowPaker2.close()  # Close window.
                self.acid_windowPaker2 = None
        else:
            if self.acid_windowPaker2 is None:
                CreatePZ.countAcid = 2
                print(f' окно2 СКО ')
                self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker2.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker2.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker2 = None
            else:
                self.acid_windowPaker2.close()  # Close window.
                self.acid_windowPaker2 = None
    def check_pvo_schema(self, ws5, ind):
        schema_pvo_set = set()
        for row in range(self.table_widget.rowCount()):
            if row > ind:
                for column in range(self.table_widget.columnCount()):
                    value = self.table_widget.item(row, column)
                    if value != None:
                        value = value.text()
                        if 'схеме №' in value or 'схемы №' in value:
                            schema_pvo_set.add(value[value.index(' №')+1:value.index(' №')+4].replace(' ', ''))
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
    def reply_acid(self):
        from open_pz import CreatePZ
        from work_py.acid_paker import AcidPakerWindow

        acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                               'Нужно ли планировать кислоту на следующий объет?')
        if acid_true_quest == QMessageBox.StandardButton.Yes:
            if self.acid_windowPaker is None:
                CreatePZ.countAcid = 1
                print(f' окно2 СКО ')
                self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker = None
                self.reply_acid()
        else:
            if self.acid_windowPaker is None:
                CreatePZ.countAcid = 2
                print(f' окно2 СКО ')
                self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker = None

    def GeophysicalNewWindow(self):
        from work_py.geophysic import GeophysicWindow

        if self.new_window is None:
            self.new_window = GeophysicWindow(self.table_widget, self.ins_ind)
            self.new_window.setWindowTitle("Геофизические исследования")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def correctPVR(self):
        from perforation_correct import PerforationCorrect
        from open_pz import CreatePZ
        plast_work = set()
        CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                             'Введите забой до которого нужно нормализовать')
        for plast, value in CreatePZ.dict_perforation.items():
            for interval in value['интервал']:
                if CreatePZ.current_bottom >= interval[0]:
                    perf_work_quest = QMessageBox.question(self, 'Добавление работающих интервалов перфорации',
                                                           f'Является ли данный интервал {CreatePZ.dict_perforation[plast]["интервал"]} работающим?')
                    if perf_work_quest == QMessageBox.StandardButton.No:
                        CreatePZ.dict_perforation[plast]['отключение'] = True
                    else:
                        plast_work.add(plast)
                        CreatePZ.dict_perforation[plast]['отключение'] = False
                elif CreatePZ.perforation_roof <= interval[0] and CreatePZ.dict_perforation[plast][
                    "отключение"] == False:
                    CreatePZ.perforation_roof = interval[0]
                elif CreatePZ.perforation_sole >= interval[1] and CreatePZ.dict_perforation[plast][
                    "отключение"] == False:
                    CreatePZ.perforation_sole = interval[1]
                # elif CreatePZ.perforation_roof_all <= interval[0]:
                #     CreatePZ.perforation_roof_all = interval[0]
                break

        if self.perforation_correct_window2 is None:
            self.perforation_correct_window2 = PerforationCorrect(self)
            self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
            self.perforation_correct_window2.setGeometry(200, 400, 100, 400)

            self.perforation_correct_window2.show()

            # CreatePZ.pause_app(self)
            # CreatePZ.pause = True
            self.perforation_correct_window2 = None

    def correctData(self):
        from data_correct import DataWindow
        from open_pz import CreatePZ

        if self.new_window is None:

            self.new_window = DataWindow()
            self.new_window.setWindowTitle("Окно корректировки")
            self.new_window.setGeometry(100, 400, 300, 400)
            self.new_window.show()
            CreatePZ.pause = True

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def perforationNewWindow(self):
        from work_py.perforation import PerforationWindow
        from open_pz import CreatePZ

        if len(CreatePZ.cat_P_1) > 1:
            if CreatePZ.cat_P_1[1] == 1 and CreatePZ.kat_pvo != 1:
                msc = QMessageBox.information(self, 'Внимание', 'Не произведен монтаж первой категории')
                return

        if self.new_window is None:

            self.new_window = PerforationWindow(self.table_widget, self.ins_ind)
            self.new_window.setWindowTitle("Перфорация")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def insertPerf(self):

        self.populate_row(self.ins_ind, self.perforation_list)

    def copy_pz(self, sheet, table_widget, work_plan = 'krs', count_col = 12, list_page = 1):

        from krs import work_krs
        rows = sheet.max_row
        merged_cells = sheet.merged_cells

        table_widget.setRowCount(rows)

        border_styles = {}
        for row in self.ws.iter_rows():
            for cell in row:
                border_styles[(cell.row, cell.column)] = cell.border

        table_widget.setColumnCount(count_col)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height is not None else 18
                           for i in range(sheet.max_row)]
        # print(rowHeights_exit)
        # print(f' Объединенны {merged_cells}')
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
                    cell = sheet[f'{get_column_letter(col + 1)}{row + 1}']
                    cell_style = cell._style

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


        # # Чтение стилей границ и применение к QTableWidget
        # for row in self.ws.iter_rows():
        #     for cell in row:
        #         cell_widget = table_widget.itemAt(cell.row - 1, cell.column - 1)
        #         if cell_widget:
        #             border = cell.border
        #             border_style = f"{border.left.style},{border.right.style},{border.top.style},{border.bottom.style}"
        #             print(border_style)
        #             cell_widget.horizontalHeader().setStyleSheet(f"border-style: {border_style};")

        if work_plan == 'krs':
            self.populate_row(table_widget.rowCount(), work_krs(self, self.work_plan), self.table_widget)
        
        if work_plan == 'gnkt_frez' and list_page == 2:
            colWidth = [2.28515625, 13.0, 4.5703125, 13.0, 13.0, 13.0, 5.7109375, 13.0, 13.0, 13.0, 4.7109375,
                        13.0, 5.140625, 13.0, 13.0, 13.0, 13.0, 13.0, 4.7109375, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0,
                        13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0, 13.0, 13.0, 5.42578125, 13.0, 4.5703125, 2.28515625, 10.28515625]
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(colWidth[column]))  # Здесь задайте требуемую ширину столбца



        # elif self.work_plan == 'gnkt-opz':
        #     from open_pz import CreatePZ
        #     # print(CreatePZ.gnkt_work1)
        #     # self.populate_row(self.table_widget.rowCount(), CreatePZ.gnkt_work1)


    def create_short_plan(self, wb2, plan_short):
        from open_pz import CreatePZ
        from work_py.descent_gno import gno_nkt_opening
        ws4 = wb2.create_sheet('Sheet1')
        ws4.title = "Краткое содержание плана работ"
        ws4 = wb2["Краткое содержание плана работ"]

        for row in range(15):
            ws4.insert_rows(ws4.max_row)
        ws4.cell(row= 1, column=1).value = CreatePZ.well_number._value
        ws4.cell(row=2, column=1).value = CreatePZ.well_area._value

        if CreatePZ.dict_pump_SHGN["do"] != 0 and CreatePZ.dict_pump_ECN["do"] == 0 and\
                CreatePZ.paker_do["do"] == 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.dict_pump_SHGN["do"]} -на гл. {CreatePZ.dict_pump_SHGN_h["do"]}м'
        elif CreatePZ.dict_pump_SHGN["do"] == 0 and CreatePZ.dict_pump_ECN["do"] != 0 and\
                CreatePZ.paker_do["do"] == 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.dict_pump_ECN["do"]} -на гл. {CreatePZ.dict_pump_ECN_h["do"]}м'
        elif CreatePZ.dict_pump_SHGN["do"] == 0 and CreatePZ.dict_pump_ECN["do"] != 0 and\
                CreatePZ.paker_do["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.dict_pump_ECN["do"]} -на гл. {CreatePZ.dict_pump_ECN_h["do"]}м \n' \
                                              f'{CreatePZ.paker_do["do"]} на {CreatePZ.H_F_paker_do["do"]}м'
        elif CreatePZ.dict_pump_SHGN["do"] != 0 and  CreatePZ.dict_pump_ECN["do"] == 0 and\
                CreatePZ.paker_do["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.dict_pump_SHGN["do"]} -на гл. {CreatePZ.dict_pump_SHGN_h["do"]}м \n' \
                                              f'{CreatePZ.paker_do["do"]} на {CreatePZ.H_F_paker_do["do"]}м'
        elif CreatePZ.dict_pump_SHGN["do"] == 0 and CreatePZ.dict_pump_ECN["do"] == 0 and\
                CreatePZ.paker_do["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.paker_do["do"]} на {CreatePZ.H_F_paker_do["do"]}м'
        elif CreatePZ.dict_pump_SHGN["do"] == 0 and CreatePZ.dict_pump_ECN["do"] == 0 and\
                CreatePZ.paker_do["do"] == 0:
            ws4.cell(row=3, column=1).value = " "
        elif CreatePZ.dict_pump_SHGN["do"] != 0 and CreatePZ.dict_pump_ECN["do"] != 0 and\
                CreatePZ.paker_do["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{CreatePZ.dict_pump_SHGN["do"]} -на гл. {CreatePZ.dict_pump_SHGN_h["do"]}м \n' \
                                              f'{CreatePZ.dict_pump_ECN["do"]} -на гл. {CreatePZ.dict_pump_ECN_h["do"]}м \n' \
                                              f'{CreatePZ.paker_do["do"]} на {CreatePZ.H_F_paker_do["do"]}м ' \


        plast_str = ''
        pressur_set = set()
        # print(f'После {CreatePZ.dict_perforation_short}')
        for plast in list(CreatePZ.dict_perforation_short.keys()):
            if CreatePZ.dict_perforation_short[plast]['отключение'] is False and plast in CreatePZ.dict_perforation_short:
                for interval in CreatePZ.dict_perforation_short[plast]["интервал"]:
                    plast_str += f'{plast[:4]}: {interval[0]}- {interval[1]} \n'
            elif CreatePZ.dict_perforation_short[plast]['отключение'] and plast in CreatePZ.dict_perforation_short:
                for interval in CreatePZ.dict_perforation_short[plast]["интервал"]:
                    plast_str += f'{plast[:4]} :{interval[0]}- {interval[1]} (изол)\n'

            filter_list_pressuar = list(
                filter(lambda x: type(x) in [int, float], list(CreatePZ.dict_perforation_short[plast]["давление"])))
            # print(f'фильтр -{filter_list_pressuar}')
            if filter_list_pressuar:
                pressur_set.add(f'{plast[:4]} - {filter_list_pressuar}')

        ws4.cell(row=6, column=1).value = f'НКТ: \n {gno_nkt_opening(CreatePZ.dict_nkt)}'
        ws4.cell(row=7, column=1).value = f'Рпл: \n {" ".join(list(pressur_set))}атм'
        # ws4.cell(row=8, column=1).value = f'ЖГС = {CreatePZ.fluid_work_short}г/см3'
        ws4.cell(row=9, column=1).value = f'Нст- {CreatePZ.static_level}м / Ндин - {CreatePZ.dinamic_level}м'
        if CreatePZ.curator == 'ОР':
            ws4.cell(row=10, column=1).value = f'Ожид {CreatePZ.expected_Q}м3/сут при Р-{CreatePZ.expected_P}м3/сут'
        else:
            ws4.cell(row=10, column=1).value = f'Qн {CreatePZ.Qoil}т Qж- {CreatePZ.Qwater}м3/сут'
        ws4.cell(row=11, column=1).value = f'макс угол {CreatePZ.max_angle} на {CreatePZ.max_angle_H._value}'
        ws4.cell(row=1, column=2).value = CreatePZ.cdng._value
        ws4.cell(row=2, column=3).value = \
            f'Рпл - {CreatePZ.dict_category[CreatePZ.plast_work[0]]["по давлению"].category},' \
              f' H2S -{CreatePZ.dict_category[CreatePZ.plast_work[0]]["по сероводороду"].category},' \
              f' газ факт -{CreatePZ.gaz_f_pr[0]}т/м3'
        column_well = f'{CreatePZ.column_diametr}х{CreatePZ.column_wall_thickness} в инт 0 - {CreatePZ.shoe_column}м ' \
            if CreatePZ.column_additional is False else f'{CreatePZ.column_diametr} х {CreatePZ.column_wall_thickness} \n' \
                                               f'0 - {CreatePZ.shoe_column}м/\n{CreatePZ.column_additional_diametr}' \
                                               f' х {CreatePZ.column_additional_wall_thickness} в инт ' \
                                                f'{CreatePZ.head_column_additional}-{CreatePZ.shoe_column_additional}м'
        ws4.cell(row=1, column=7).value = column_well
        ws4.cell(row=4, column=7).value = f'Пробур забой {CreatePZ.bottomhole_drill}м'
        ws4.cell(row=5, column=7).value = f'Исскус забой {CreatePZ.bottomhole_artificial}м'
        ws4.cell(row=6, column=7).value = f'Тек забой {CreatePZ.bottom}м'


        ws4.cell(row=7, column=7).value = plast_str
        ws4.cell(row=11, column=7).value = f'Рмакс {CreatePZ.max_admissible_pressure}атм'
        ws4.cell(row=3, column=2).value = plan_short
        nek_str = 'НЭК '
        if len(CreatePZ.leakiness_interval) != 0:

            for nek in CreatePZ.leakiness_interval:
                nek_str += f'{nek[0]}-{nek[1]} \n'

        ws4.cell(row=3, column=7).value = nek_str

        ws4.insert_rows(1, 2)
        ws4.insert_cols(1, 2)
        ws4.cell(row=2, column=3).value = 'Краткое содержание плана работ'
        ws4.cell(row=2, column=3).font = Font(name='Arial', size=16, bold=True)

        #объединение ячеек
        ws4.merge_cells(start_row=2, start_column=3, end_row=2, end_column=9) # Объединение оглавления
        ws4.merge_cells(start_row=5, start_column=3, end_row=7, end_column=3) # Объединение строк ГНО
        ws4.merge_cells(start_row=4, start_column=5, end_row=4, end_column=6) # объединение по класси
        ws4.merge_cells(start_row=3, start_column=9, end_row=4, end_column=9) # Объединение строк данных по колонну
        ws4.merge_cells(start_row=9, start_column=9, end_row=12, end_column=9)
        ws4.merge_cells(start_row=5, start_column=4, end_row=13, end_column=8)


        for row_ind in range(3, 15):
            ws4.row_dimensions[row_ind].height = 80
            for col in range(3, 10):
                if row_ind == 3:
                    ws4.column_dimensions[get_column_letter(col)].width = 20

                ws4.cell(row=row_ind, column=col).border = CreatePZ.thin_border
                ws4.cell(row=row_ind, column=col).font = Font(name='Arial', size=13, bold=False)
                ws4.cell(row=row_ind, column=col).alignment = Alignment(wrap_text=True, horizontal='left',
                                                               vertical='center')
        ws4.cell(row=5, column=4).font = Font(name='Arial', size=11, bold=False)
        ws4.hide = True
        ws4.page_setup.fitToPage = True
        ws4.page_setup.fitToHeight = False

        ws4.page_setup.fitToWidth = True
        ws4.print_area = 'C2:I14'

    def check_gpp_upa(self):
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                value = self.table_widget.item(row, column)
                if value != None:
                    value = value.text()
                    if 'Установить подъёмный агрегат на устье не менее 40т' in value:
                        new_value = QtWidgets.QTableWidgetItem(f'Установить подъёмный агрегат на устье не менее 60т. '
                                                               f'Пусковой комиссией составить акт готовности подьемного '
                                                               f'агрегата и бригады для проведения ремонта скважины.')

                        self.table_widget.setItem(row, column, new_value)

    def true_set_Paker(self, depth):
        from open_pz import CreatePZ
        from work_py.advanted_file import raid, remove_overlapping_intervals
        from work_py.opressovka import OpressovkaEK

        a = False

        while a is False:
            for plast in CreatePZ.plast_all:
                if len(CreatePZ.dict_perforation[plast]['интервал']) >= 1:
                    for interval in CreatePZ.dict_perforation[plast]['интервал']:
                        if interval[0] < depth < interval[1]:
                            a = False
                        else:
                            a = True
                elif len(CreatePZ.dict_perforation[plast]['интервал']) == 0:
                    a = True


            if a is False:
                paker_warning = QMessageBox.warning(None, 'Проверка посадки пакера в интервал перфорации',
                                                    f'Проверка посадки показала пакер сажается в интервал перфорации, '
                                                    f'необходимо изменить глубину посадки!!!')
                # print(f'проверка {a}')
                depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                'Введите глубину посадки пакера для опрессовки колонны',
                                                int(CreatePZ.perforation_roof - 20), 0,
                                                int(CreatePZ.current_bottom))


        check_for_template = OpressovkaEK.check_for_template_paker(self, depth)
        if check_for_template[1]:
            depth = check_for_template[0]

            if any([interval[0] <= depth <= interval[1] for interval in CreatePZ.skm_interval]):
                return int(depth)
            else:
                false_question = QMessageBox.question(None, 'Проверка посадки пакера в интервал скреперования',
                                                     f'Проверка посадки показала пакер сажается не в интервал скреперования, '
                                                     f'Посадить ли пакер?')
                if false_question == QMessageBox.StandardButton.Yes:
                    return int(depth)
                else:
                    skm_question = QMessageBox.question(None, 'Скреперование',
                                                          f'добавить интервал скреперования {depth - 20} - {depth + 20}')
                    if skm_question == QMessageBox.StandardButton.Yes:

                        CreatePZ.skm_interval.append((depth - 20, depth + 20))
                        perforating_intervals = []
                        for plast in CreatePZ.plast_all:
                            for interval in CreatePZ.dict_perforation[plast]['интервал']:
                                perforating_intervals.append(list(interval))
                        # print(f'интервалы ПВР {perforating_intervals, CreatePZ.skm_interval}')
                        raid_str = raid(remove_overlapping_intervals(perforating_intervals))
                        for row in range(self.table_widget.rowCount()):
                            for column in range(self.table_widget.columnCount()):
                                value = self.table_widget.item(row, column)
                                if value != None:
                                    value = value.text()
                                    if 'Произвести скреперование' in value:
                                        ind_value = value.split(' ')
                                        ind_min = ind_value.index('интервале')+1
                                        ind_max = ind_value.index('обратной')

                                        new_value = QtWidgets.QTableWidgetItem(f'{" ".join(ind_value[:ind_min])} '
                                                                               f'{raid_str}м {" ".join(ind_value[ind_max:])}')

                                        self.table_widget.setItem(row, column, new_value)
                        return int(depth)
                    else:
                        return int(depth)
        else:
            return int(depth)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
