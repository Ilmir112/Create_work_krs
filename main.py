# -*- coding: utf-8 -*-
import json
import os
import shutil

import sys
import socket

import psutil

import win32com.client
import openpyxl
import re
import win32con
import property_excel.property_excel_pvr
import threading

import win32gui

from openpyxl.reader.excel import load_workbook
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, \
    QLineEdit, QFileDialog, QToolBar, QPushButton, QMessageBox, QInputDialog, QTabWidget, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from openpyxl.utils import get_column_letter

from openpyxl.workbook import Workbook
from openpyxl.styles import Alignment, Font

from block_name import region_select
from data_base.config_base import connect_to_database, CheckWellExistence, connection_to_database, WorkDatabaseWell
from log_files.log import logger, QPlainTextEditLogger

from openpyxl.drawing.image import Image

import well_data

from PyQt5.QtCore import QThread, pyqtSlot

from users.login_users import LoginWindow
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class UncaughtExceptions(QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    @pyqtSlot(object)
    def handleException(self, ex):
        try:
            logger.critical(f'{self.dict_data_well["well_number"]._value} {self.dict_data_well["well_area"]._value} Критическая ошибка: {ex}')
        except:
            logger.critical(f'{self.dict_data_well["well_number"]} {self.dict_data_well["well_area"]} Критическая ошибка: {ex}')


class ExcelWorker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def check_well_existence(self, well_number, deposit_area, region):

        check_true = True

        try:
            db = connection_to_database(well_data.DB_CLASSIFICATION)
            self.check_correct_well = CheckWellExistence(db)
            check_true, stop_app = self.check_correct_well.checking_well_database_without_juming(well_number, deposit_area, region)

        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f"Ошибка при проверке записи: {type(e).__name__}\n\n{str(e)}")

        # Завершение работы потока
        self.finished.emit()
        return check_true, stop_app

    def check_category(self, well_number, deposit_area, region):
        result = self.check_correct_well.check_category(well_number, deposit_area, region)
        return result


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.operation_window = None
        self.table_schema = None
        self.table_widget = None
        self.table_title = None
        self.data_window = None
        self.perforation_correct_window2 = None
        self.work_plan = None
        self.dict_data_well = {}

    @staticmethod
    def insert_image(ws, file, coordinate, width=200, height=180):
        # Загружаем изображение с помощью библиотеки Pillow

        img = openpyxl.drawing.image.Image(file)
        img.width = width
        img.height = height
        img.anchor = coordinate
        ws.add_image(img, coordinate)

    @staticmethod
    def set_modal_window(window):
        # Установка модальности окна
        window.setWindowModality(Qt.ApplicationModal)
        window.show()

    def read_excel_file(self):
        from find import FindIndexPZ
        from work_py.leakage_column import LeakageWindow
        from category_correct import CategoryWindow

        from find import WellNkt, WellPerforation, WellCondition, WellHistoryData, WellName, WellCategory, \
            WellFondData, WellSuckerRod, WellExpectedPickUp, WellData

        self.dict_category = {}
        # Запуск основного класса и всех дочерних классов в одной строке
        well_pz = FindIndexPZ(self.ws, self.work_plan)
        well_pz.dict_data_well["work_plan"] = self.work_plan
        data_well_dict = {}
        self.dict_data_well = WellName.read_well(
            well_pz, well_pz.cat_well_max._value, well_pz.data_pvr_min._value)
        
        well_pz.dict_data_well['region'] = region_select(well_pz.dict_data_well['cdng']._value)

        date_str2 = datetime.strptime('2024-09-19', '%Y-%m-%d')

        if self.work_plan == 'dop_plan':
            number_list = list(map(str, range(1, 50)))
            self.dict_data_well["number_dp"], ok = QInputDialog.getItem(self, 'Номер дополнительного плана работ',
                                                      'Введите номер дополнительного плана работ',
                                                      number_list, 0, False)

            db = connection_to_database(well_data.DB_WELL_DATA)
            data_well_base = WorkDatabaseWell(db, self.dict_data_well)

            data_well = data_well_base.check_in_database_well_data(self.dict_data_well["well_number"]._value,
                                                                   self.dict_data_well["well_area"]._value,
                                                                   f'ДП№{self.dict_data_well["number_dp"]}')

            if data_well:

                date_str1 = datetime.strptime(f'{data_well[1]}', '%Y-%m-%d')
                if date_str1 > date_str2:

                    change_work_work_plan = QMessageBox.question(self,
                                                                 'Наличие в базе данных',
                                                                 'Проверка показала что данные по скважине есть в'
                                                                 ' базе данных, '
                                                                 'загрузить с базы?')

                    if change_work_work_plan == QMessageBox.StandardButton.Yes:
                        self.dict_data_well["type_kr"] = data_well[2]
                        self.dict_data_well["work_plan"] = 'dop_plan_in_base'
                        self.dict_data_well["work_plan"] = 'dop_plan_in_base'
                        well_data.data_in_base = True
                        from work_py.dop_plan_py import DopPlanWindow
                        self.rir_window = DopPlanWindow(self.dict_data_well["ins_ind"], None, self.dict_data_well["work_plan"])
                        # self.rir_window.setGeometry(200, 400, 100, 200)
                        self.rir_window.show()
                        self.pause_app()
                        well_data.pause = True

                        return

        if well_data.data_well_is_True is False:
            WellNkt.read_well(
                well_pz, well_pz.pipes_ind._value, well_pz.condition_of_wells._value)
            WellHistoryData.read_well(
                well_pz, well_pz.data_pvr_max._value, well_pz.data_fond_min._value)
            WellCondition.read_well(
                well_pz, well_pz.condition_of_wells._value, well_pz.data_well_max._value)

            WellExpectedPickUp.read_well(
                well_pz, well_pz.data_x_min._value, well_pz.data_x_max._value)
            if self.work_plan not in ['application_pvr', 'application_gis']:
                WellSuckerRod.read_well(
                    well_pz, well_pz.sucker_rod_ind._value, well_pz.pipes_ind._value)

                WellFondData.read_well(
                    well_pz, well_pz.data_fond_min._value, well_pz.condition_of_wells._value)
            WellData.read_well(well_pz, well_pz.cat_well_max._value, well_pz.data_pvr_min._value)



            WellPerforation.read_well(well_pz, well_pz.data_pvr_min._value, well_pz.data_pvr_max._value + 1)

            self.dict_data_well = \
                WellCategory.read_well(well_pz, well_pz.cat_well_min._value, well_pz.data_well_min._value)


        # self.set_modal_window(self.well_data.data_window)

        # self.pause_app()
        # well_data.pause = True

            if self.dict_data_well["leakiness"] is True:
                if WellCondition.leakage_window is None:
                    WellCondition.leakage_window = LeakageWindow()
                    WellCondition.leakage_window.setWindowTitle("Геофизические исследования")
                    # WellCondition.leakage_window.setGeometry(200, 400, 300, 400)
                    WellCondition.leakage_window.show()

                    self.pause_app()
                    self.dict_data_well["dict_leakiness"] = WellCondition.leakage_window.add_work()
                    # print(f'словарь нарушений {self.dict_data_well["dict_leakiness"]}')
                    well_pz.pause = True
                    WellCondition.leakage_window = None  # Discard reference.


            if self.dict_data_well["emergency_well"] is True:
                emergency_quest = QMessageBox.question(self, 'Аварийные работы ',
                                                       'Программа определила что в скважине'
                                                       f' авария - {self.dict_data_well["emergency_count"]}, верно ли?')
                if emergency_quest == QMessageBox.StandardButton.Yes:
                    self.dict_data_well["emergency_well"] = True
                    self.dict_data_well["emergency_bottom"], ok = QInputDialog.getInt(self, 'Аварийный забой',
                                                                         'Введите глубину аварийного забоя',
                                                                         0, 0,
                                                                         int(self.dict_data_well[
                                                                                 "bottomhole_artificial"]._value))
                else:
                    self.dict_data_well["emergency_well"] = False
            if self.dict_data_well["problem_with_ek"] is True:
                problem_with_ek_quest = QMessageBox.question(self, 'ВНИМАНИЕ НЕПРОХОД ',
                                                             f'Программа определила что в скважине '
                                                             f'ссужение в ЭК -, верно ли?')
                if problem_with_ek_quest == QMessageBox.StandardButton.Yes:
                    self.dict_data_well["problem_with_ek"] = True
                    self.dict_data_well["problem_with_ek_depth"], ok = QInputDialog.getInt(self, 'Глубина сужения',
                                                                              "Введите глубину cсужения", 0, 0,
                                                                              int(self.dict_data_well[
                                                                                      "current_bottom"]))
                    self.dict_data_well["problem_with_ek_diametr"] = QInputDialog.getInt(self, 'диаметр внутренний cсужения',
                                                                            "ВВедите внутренний диаметр cсужения", 0,
                                                                            0,
                                                                            int(float(self.dict_data_well["current_bottom"])))[
                        0]
                else:
                    self.dict_data_well["problem_with_ek"] = False

            if self.dict_data_well["gips_in_well"] is True:
                gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                       'Программа определила что скважина осложнена гипсовыми отложениями '
                                                       'и требуется предварительно определить забой на НКТ, верно ли это?')

                if gips_true_quest == QMessageBox.StandardButton.Yes:
                    self.dict_data_well["gips_in_well"] = True
                else:
                    self.dict_data_well["gips_in_well"] = False

        if self.dict_data_well["inv_number"]._value == 'не корректно' or self.dict_data_well["inv_number"] is None:
            QMessageBox.warning(self, 'Инвентарный номер отсутствует',
                                'Необходимо уточнить наличие инвентарного номера')
            return

        return self.dict_data_well
    def open_read_excel_file_pz(self):
        from open_pz import CreatePZ
        from data_base.work_with_base import insert_data_new_excel_file
        from work_py.correct_plan import CorrectPlanWindow
        from work_py.dop_plan_py import DopPlanWindow
        from work_py.gnkt_grp import GnktOsvWindow
        from work_py.gnkt_frez import WorkWithGnkt

        if self.work_plan in ['krs', 'dop_plan', 'gnkt_opz', 'gnkt_after_grp', 'gnkt_bopz', 'gnkt_frez']:
            QMessageBox.information(self, 'ВНИМАНИЕ', 'Для корректного прочтения план заказа, план заказ должен быть '
                                                      'пересохранен в формат .xlsx (КНИГА EXCEL, '
                                                      'excel версия от 2010г и выше)')
            self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                                  "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            if self.fname:
                try:
                    self.read_pz(self.fname)
                    well_data.pause = True
                    
                    self.dict_data_well = self.read_excel_file()
                    read_pz = CreatePZ(self.dict_data_well, self.ws)
                    self.ws = read_pz.open_excel_file(self.ws, self.work_plan)
                except FileNotFoundError as f:
                    QMessageBox.warning(self, 'Ошибка', f'Ошибка при прочтении файла {f}')

            if self.work_plan in ['krs', 'dop_plan']:
                self.copy_pz(self.ws, self.table_widget, self.work_plan)
                if self.work_plan == 'dop_plan':
                    self.rir_window = DopPlanWindow(self.dict_data_well, self.table_widget)
                    self.set_modal_window(self.rir_window)
            elif self.work_plan in ['gnkt_opz', 'gnkt_after_grp', 'gnkt_bopz']:
                self.gnkt_data = GnktOsvWindow(self.ws,
                                               self.table_title, self.table_schema, self.table_widget,
                                               self.dict_data_well)
            elif self.work_plan == 'gnkt_frez':
                self.gnkt_data = WorkWithGnkt(self.ws, self.table_title, self.table_schema, self.table_widget, self.dict_data_well)


        elif self.work_plan in ['plan_change', 'dop_plan_in_base']:
            well_data.data_in_base = True
            if self.work_plan == 'plan_change':
                self.rir_window = CorrectPlanWindow(self.dict_data_well, self.table_widget)
            elif self.work_plan == 'dop_plan_in_base':
                self.rir_window = DopPlanWindow(self.dict_data_well, self.table_widget)

            self.rir_window.setGeometry(200, 400, 800, 200)
            self.rir_window.show()
            well_data.pause = True
            self.pause_app()

            self.ws = insert_data_new_excel_file(self, well_data.data, well_data.rowHeights, well_data.colWidth,
                                                 well_data.boundaries_dict)

            self.copy_pz(self.ws, self.table_widget, self.work_plan)
        self.pause_app()
        well_data.pause = True
        self.rir_window = None

        return self.ws

    def read_pz(self, fname):
        self.wb = load_workbook(fname, data_only=True)
        name_list = self.wb.sheetnames
        self.ws = self.wb.active

    def definition_filenames(self):
        if 'РН' in well_data.contractor:
            contractor = 'РН'
        elif 'Ойл' in well_data.contractor:
            contractor = 'Ойл'

        if self.work_plan in ['dop_plan', 'dop_plan_in_base']:
            string_work = f' ДП№ {self.dict_data_well["number_dp"]}'
        elif self.work_plan == 'krs':
            string_work = 'ПР'
        elif self.work_plan == 'plan_change':
            if self.dict_data_well["work_plan_change"] == 'krs':
                string_work = 'ПР изм'
            else:
                string_work = f'ДП№{self.dict_data_well["number_dp"]} изм '

        elif self.work_plan == 'gnkt_bopz':
            string_work = 'ГНКТ БОПЗ ВНС'
        elif self.work_plan == 'gnkt_opz':
            string_work = 'ГНКТ ОПЗ'
        elif self.work_plan == 'gnkt_after_grp':
            string_work = 'ГНКТ ОСВ ГРП'
        else:
            string_work = 'ГНКТ'

        filenames = f'{self.dict_data_well["well_number"]._value} {self.dict_data_well["well_area"]._value} ' \
                    f'{self.dict_data_well["type_kr"].split(" ")[0]} кат {self.dict_data_well["category_pressuar"]}' \
                    f' {string_work} {contractor}.xlsx'
        return filenames



    def save_to_gnkt(self):
        from gnkt_data.gnkt_data import insert_data_base_gnkt

        sheets = ["Титульник", 'СХЕМА', 'Ход работ']
        tables = [self.table_title, self.table_schema, self.table_widget]

        for i, sheet_name in enumerate(sheets):
            worksheet = self.gnkt_data.wb_gnkt[sheet_name]
            table = tables[i]

            work_list = []
            for row in range(table.rowCount()):
                row_lst = []
                # self.ins_ind_border += 1
                for column in range(table.columnCount()):

                    item = table.item(row, column)
                    if not item is None:

                        row_lst.append(item.text())
                        # print(item.text())
                    else:
                        row_lst.append("")
                work_list.append(row_lst)
            self.gnkt_data.count_row_height(worksheet, work_list, sheet_name)
        if "СХЕМЫ КНК_38,1" not in self.gnkt_data.wb_gnkt.sheetnames:
            # ws6 = self.gnkt_data.wb_gnkt.create_sheet(title="СХЕМЫ КНК_44,45")
            # self.insert_image(ws6, f'{well_data.path_image}imageFiles/schema_well/СХЕМЫ КНК_44,45.png', 'A1',
            #                   550, 900)

            ws7 = self.gnkt_data.wb_gnkt.create_sheet(title="СХЕМЫ КНК_38,1")
            self.insert_image(ws7, f'{well_data.path_image}imageFiles/schema_well/СХЕМЫ КНК_38,1.png', 'A1',
                              550, 900)

        # path = 'workiii'
        if 'Зуфаров' in well_data.user:
            path = 'D:\Documents\Desktop\ГТМ'
        else:
            path = ""
        filenames = self.definition_filenames()
        full_path = path + '/' + filenames
        gnkt_data = self.gnkt_data.data_gnkt

        insert_data_base_gnkt(self, well_data.contractor, filenames, gnkt_data.gnkt_number_combo,
                              int(gnkt_data.lenght_gnkt_edit),
                              float(gnkt_data.diametr_length),
                              float(gnkt_data.iznos_gnkt_edit) * 1.014,
                              int(gnkt_data.pipe_mileage_edit) + int(gnkt_data.current_bottom_edit * 1.1),
                              gnkt_data.pipe_fatigue, int(gnkt_data.pvo_number),
                              gnkt_data.previous_well_combo)

        if self.dict_data_well["bvo"] is True:
            ws5 = self.gnkt_data.wb_gnkt.create_sheet('Sheet1')
            ws5.title = "Схемы ПВО"
            ws5 = self.gnkt_data.wb_gnkt["Схемы ПВО"]
            self.gnkt_data.wb_gnkt.move_sheet(ws5, offset=-1)
            schema_list = self.check_pvo_schema(ws5, 2)

        if self.gnkt_data.wb_gnkt:
            self.save_file_dialog(self.gnkt_data.wb_gnkt, full_path)

            self.gnkt_data.wb_gnkt.close()
            print(f'Table data saved to Excel {full_path}')
        if self.wb:
            self.wb.close()



    @staticmethod
    def calculate_chemistry(type_chemistry, volume):
        if type_chemistry in ['HCl', 'Нефтекислотка']:
            well_data.DICT_VOLUME_CHEMISTRY['HCl'] += volume
        elif type_chemistry == 'HF':
            well_data.DICT_VOLUME_CHEMISTRY['HF'] += volume
        elif type_chemistry == 'ВТ':
            well_data.DICT_VOLUME_CHEMISTRY['ВТ СКО'] += volume
        elif type_chemistry == 'Противогипсовая обработка':
            well_data.DICT_VOLUME_CHEMISTRY['NaOH'] += volume
        elif type_chemistry == 'цемент':
            well_data.DICT_VOLUME_CHEMISTRY['цемент'] += volume
        elif type_chemistry == 'Глина':
            well_data.DICT_VOLUME_CHEMISTRY['Глина'] += volume
        elif type_chemistry == 'растворитель':
            well_data.DICT_VOLUME_CHEMISTRY['растворитель'] += volume
        elif type_chemistry == 'песок':
            well_data.DICT_VOLUME_CHEMISTRY['песок'] += volume
        elif type_chemistry == 'РПК':
            well_data.DICT_VOLUME_CHEMISTRY['РПК'] += 1
        elif type_chemistry == 'РИР 2С':
            well_data.DICT_VOLUME_CHEMISTRY['РИР 2С'] += 1
        elif type_chemistry == "РИР ОВП":
            well_data.DICT_VOLUME_CHEMISTRY["РИР ОВП"] += 1
        elif type_chemistry == 'гидрофабизатор':
            well_data.DICT_VOLUME_CHEMISTRY['гидрофабизатор'] += volume

    def save_file_dialog(self, wb2, full_path):
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save excel-file",
                                                       f"{full_path}", "Excel Files (*.xlsx)")
            if file_name:
                wb2.save(file_name)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка',
                                 f'файл под таким именем открыт, закройте его: {type(e).__name__}\n\n{str(e)}')
            return
        try:
            # Создаем объект Excel
            excel = win32com.client.Dispatch("Excel.Application")
            # Открываем файл
            workbook = excel.Workbooks.Open(file_name)
            # Выбираем активный лист
            worksheet = workbook.ActiveSheet

            # Назначаем область печати с колонок B до L
            worksheet.PageSetup.PrintArea = "B:L"

        except Exception as e:
            print(f"Ошибка при работе с Excel: {type(e).__name__}\n\n{str(e)}")

    @staticmethod
    def pause_app():
        asww = well_data.pause
        while well_data.pause is True:
            QtCore.QCoreApplication.instance().processEvents()



    def check_pvo_schema(self, ws5, ind):
        schema_pvo_set = set()
        for row in range(self.table_widget.rowCount()):
            if row > ind:
                for column in range(self.table_widget.columnCount()):
                    value = self.table_widget.item(row, column)
                    if value != None:
                        value = value.text()

                        if 'схеме №' in value or 'схемы №' in value or 'Схемы обвязки №' in value or 'схемы ПВО №' in value:
                            number_schema = value[value.index(' №') + 1:value.index(' №') + 4].replace(' ', '')

                            schema_pvo_set.add(number_schema)
        # print(f'схема ПВО {schema_pvo_set}')

        n = 0
        if schema_pvo_set:
            for schema in list(schema_pvo_set):
                coordinate = f'{get_column_letter(2)}{1 + n}'
                if 'Ойл' in well_data.contractor:
                    schema_path = f'{well_data.path_image}imageFiles/pvo/oil/схема {schema}.jpg'
                elif 'РН' in well_data.contractor:
                    schema_path = f'{well_data.path_image}imageFiles/pvo/rn/схема {schema}.png'
                try:
                    img = openpyxl.drawing.image.Image(schema_path)
                    img.width = 750
                    img.height = 530
                    img.anchor = coordinate
                    ws5.add_image(img, coordinate)
                    n += 29
                except FileNotFoundError as f:
                    QMessageBox.warning(self, 'Ошибка', f'Схему {schema} не удалось вставилось:\n {f}')
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


    def insert_data_in_database(self, row_number, row_max):

        dict_perforation_json = json.dumps(self.dict_data_well["dict_perforation"], default=str, ensure_ascii=False, indent=4)
        # print(self.dict_data_well["dict_leakiness"])
        leakage_json = json.dumps(self.dict_data_well["dict_leakiness"], default=str, ensure_ascii=False, indent=4)
        plast_all_json = json.dumps(self.dict_data_well["plast_all"])
        plast_work_json = json.dumps(self.dict_data_well['plast_work'])
        skm_list_json = json.dumps(self.dict_data_well["skm_interval"])
        raiding_list_json = json.dumps(self.dict_data_well["ribbing_interval"])
        number = json.dumps(str(self.dict_data_well["well_number"]._value) + self.dict_data_well["well_area"]._value, ensure_ascii=False,
                            indent=4)
        template_ek = json.dumps(
            [self.dict_data_well["template_depth"], self.dict_data_well["template_lenght"], self.dict_data_well["template_depth_addition"],
             self.dict_data_well["template_lenght_addition"]])

        # Подготовленные данные для вставки (пример)
        data_values = [row_max, self.dict_data_well["current_bottom"], dict_perforation_json, plast_all_json, plast_work_json,
                       leakage_json, self.dict_data_well["column_additional"], self.dict_data_well["fluid_work"],
                       self.dict_data_well["category_pressuar"], self.dict_data_well["category_h2s"], self.dict_data_well["category_gf"],
                       template_ek, skm_list_json,
                       self.dict_data_well["problem_with_ek_depth"], self.dict_data_well["problem_with_ek_diametr"], raiding_list_json]

        if len(self.dict_data_well["data_list"]) == 0:
            self.dict_data_well["data_list"].append(data_values)
        else:
            row_number = row_number - self.dict_data_well["count_row_well"]
            self.dict_data_well["data_list"].insert(row_number, data_values)

    def check_depth_in_skm_interval(self, depth):

        check_true = False
        check_ribbing = False

        for interval in self.dict_data_well["skm_interval"]:
            if float(interval[0]) <= float(depth) <= float(interval[1]):
                check_true = True
                return int(depth)

        for interval in self.dict_data_well["ribbing_interval"]:
            if float(interval[0]) <= float(depth) <= float(interval[1]):
                check_ribbing = True
        if check_true is False and check_ribbing is False:
            QMessageBox.warning(None, 'Проверка посадки пакера в интервал скреперования',
                                f'Проверка посадки показала, что пакер сажается не '
                                f'в интервал скреперования {self.dict_data_well["skm_interval"]}, и '
                                f'райбирования {self.dict_data_well["ribbing_interval"]} \n'
                                f'Нужно скорректировать интервалы скреперования ')
            return False
        if check_true is True and check_ribbing is False:
            false_question = QMessageBox.question(None, 'Проверка посадки пакера в интервал скреперования',
                                                  f'Проверка посадки показала, что пакер сажается не '
                                                  f'в интервал скреперования {self.dict_data_well["skm_interval"]}, '
                                                  f'но сажается в интервал райбирования '
                                                  f'райбирования {self.dict_data_well["ribbing_interval"]} \n'
                                                  f'Продолжить?')
            if false_question == QMessageBox.StandardButton.No:
                return False


    def true_set_paker(self, depth):

        check_true = False

        for plast in self.dict_data_well["plast_all"]:
            if len(self.dict_data_well["dict_perforation"][plast]['интервал']) >= 1:
                for interval in self.dict_data_well["dict_perforation"][plast]['интервал']:
                    if float(interval[0]) < depth < float(interval[1]):
                        check_true = False
                    else:
                        check_true = True
            elif len(self.dict_data_well["dict_perforation"][plast]['интервал']) == 0:
                check_true = True

        if check_true is False:
            QMessageBox.warning(None, 'Проверка посадки пакера в интервал перфорации',
                                f'Проверка посадки показала пакер сажается в интервал перфорации, '
                                f'необходимо изменить глубину посадки!!!')

        return check_true

    def populate_row(self, ins_ind, work_list, table_widget, work_plan='krs'):
        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 900), 200: (901, 1500)}
        index_setSpan = 0
        if work_plan == 'gnkt_frez':
            index_setSpan = 1
        row_max = table_widget.rowCount()
        # print(f'ДОП {work_plan}')

        for i, row_data in enumerate(work_list):
            row = ins_ind + i
            if work_plan not in ['application_pvr', 'gnkt_frez', 'gnkt_opz', 'gnkt_bopz', 'gnkt_after_grp', 'application_gis']:
                self.insert_data_in_database(row, row_max + i)

            table_widget.insertRow(row)

            if len(str(row_data)[1]) > 3 and work_plan in 'gnkt_frez':
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
        if 'gnkt' not in work_plan:
            for row in range(table_widget.rowCount()):
                if row >= self.dict_data_well["ins_ind2"]:
                    
                    # Добавляем нумерацию в первую колонку
                    item_number = QtWidgets.QTableWidgetItem(str(row - self.dict_data_well["ins_ind2"] + 1))  # Номер строки + 1
                    table_widget.setItem(row, 1, item_number)

    def check_true_depth_template(self, depth):
        check = True
        if self.dict_data_well["column_additional"]:

            if self.dict_data_well["template_depth_addition"] < depth and depth > self.dict_data_well["head_column_additional"]._value:
                check = False
                check_question = QMessageBox.question(
                    self,
                    'Проверка глубины пакера',
                    f'Проверка показало что пакер с глубиной {depth}м спускается ниже'
                    f' глубины  шаблонирования {self.dict_data_well["template_depth_addition"]}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True
            if self.dict_data_well["template_depth"] < depth and depth < self.dict_data_well["head_column_additional"]._value:
                check = False
                check_question = QMessageBox.question(
                    self,
                    'Проверка глубины пакера',
                    f'Проверка показало что пакер с глубиной {depth}м спускается ниже '
                    f'глубины шаблонирования {self.dict_data_well["template_depth"]}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True
        else:
            # print(f'глубина {self.dict_data_well["template_depth"], depth}')
            if self.dict_data_well["template_depth"] < depth:
                check = False
                check_question = QMessageBox.question(
                    self, 'Проверка глубины пакера', f'Проверка показало что пакер с глубиной {depth}м спускается ниже '
                                                     f'глубины шаблонирования {self.dict_data_well["template_depth"]}')
                if check_question == QMessageBox.StandardButton.Yes:
                    check = True

        return check

    def copy_pz(self, sheet, table_widget, work_plan='krs', count_col=12, list_page=1):
        from krs import GnoWindow

        rows = sheet.max_row
        merged_cells = sheet.merged_cells
        table_widget.setRowCount(rows)
        self.dict_data_well["count_row_well"] = table_widget.rowCount()

        if work_plan == 'plan_change':
            self.dict_data_well["count_row_well"] = self.dict_data_well["data_x_max"]._value

        border_styles = {}
        for row in sheet.iter_rows():
            for cell in row:
                border_styles[(cell.row, cell.column)] = cell.border

        table_widget.setColumnCount(count_col)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height is not None else 18
                           for i in range(sheet.max_row)]

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

                    item = QtWidgets.QTableWidgetItem(str(cell_value))
                    table_widget.setItem(row - 1, col - 1, item)

                    # Проверяем, является ли текущая ячейка объединенной
                    for merged_cell in merged_cells:
                        range_row = range(merged_cell.min_row, merged_cell.max_row + 1)
                        range_col = range(merged_cell.min_col, merged_cell.max_col + 1)
                        if row in range_row and col in range_col:
                            # Устанавливаем количество объединяемых строк и столбцов для текущей ячейки
                            table_widget.setSpan(row - 1, col - 1,
                                                 merged_cell.max_row - merged_cell.min_row + 1,
                                                 merged_cell.max_col - merged_cell.min_col + 1)

                else:
                    item = QTableWidgetItem("")

        if well_data.dop_work_list:
            self.populate_row(table_widget.rowCount(), well_data.dop_work_list, self.table_widget, self.work_plan)
        for row in range(table_widget.rowCount()):
            row_value_empty = True  # Флаг, указывающий, что все ячейки в строке пустые
            # Проход по всем колонкам в текущей строке
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                # Проверка, является ли содержимое ячейки пустым
                if item is not None and item.text() != "":
                    row_value_empty = False  # Если хотя бы одна ячейка не пустая, снимаем флаг
                    break
            # Если все ячейки в строке пустые, скрываем строку
            if row_value_empty:
                table_widget.setRowHidden(row, True)
            else:
                table_widget.setRowHidden(row, False)

        if work_plan == 'krs':
            self.work_window = GnoWindow(table_widget.rowCount(), self.table_widget, self.dict_data_well)
            self.set_modal_window(self.work_window)

            # self.work_window.setGeometry(100, 400, 200, 500)
            self.work_window.show()

            self.pause_app()
            well_data.pause = True
            self.work_window = None

        if work_plan in ['gnkt_frez'] and list_page == 2:
            colWidth = [2.28515625, 13.0, 4.5703125, 13.0, 13.0, 13.0, 5.7109375, 13.0, 13.0, 13.0, 4.7109375,
                        13.0, 5.140625, 13.0, 13.0, 13.0, 13.0, 13.0, 4.7109375, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0,
                        13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                        13.0, 13.0, 13.0, 5.42578125, 13.0, 4.5703125, 2.28515625, 10.28515625]
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(colWidth[column]))  # Здесь задайте требуемую ширину столбца
        elif work_plan in ['gnkt_after_grp', 'gnkt_opz', 'gnkt_after_grp', 'gnkt_bopz'] and list_page == 2:

            colWidth = property_excel.property_excel_pvr.colWidth_gnkt_osv
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(colWidth[column] * 9))  # Здесь задайте требуемую ширину столбца

        elif work_plan == 'application_pvr':
            from property_excel import property_excel_pvr
            for column in range(table_widget.columnCount()):
                table_widget.setColumnWidth(column, int(
                    property_excel_pvr.colWidth[column]))  # Здесь задайте требуемую ширину столбца
        well_data.pause = True


class MyWindow(MyMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.login_window = None
        self.operation_window = None
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
        self.resize(1400, 800)
        # self.setWindowState(Qt.WindowFullScreen)
        # self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        self.perforation_correct_window2 = None
        self.ws = None
        self.ins_ind = None
        self.perforation_list = []
        self.dict_perforation_project = {}

        self.ins_ind_border = None
        self.work_plan = 0
        self.table_widget = None
        self.table_pvr = None

        threading.Timer(2.0, self.close_splash).start()

        self.log_widget = QPlainTextEditLogger(self)
        logger.addHandler(self.log_widget)
        self.setCentralWidget(self.log_widget.widget)

        # Обработка критических ошибок
        self.excepthook = UncaughtExceptions()
        self.excepthook._exception_caught.connect(self.excepthook.handleException)

        # # Запускаем обработчик исключений в отдельном потоке
        self.thread = QThread()
        self.excepthook.moveToThread(self.thread)
        # self.thread.started.connect(self.excepthook.handleException)
        self.thread.start()

    def insert_data_in_chemistry(self):


        if self.dict_data_well["work_plan"] in ['dop_plan', 'dop_plan_in_base']:
            string_work = f' ДП№ {self.dict_data_well["number_dp"]}'
        elif self.dict_data_well["work_plan"] == 'krs':
            string_work = 'ПР'
        elif self.dict_data_well["work_plan"] == 'plan_change':
            if self.dict_data_well["work_plan_change"] == 'krs':
                string_work = 'ПР изм'
            else:
                string_work = f'ДП№{self.dict_data_well["number_dp"]} изм '

        elif self.dict_data_well["work_plan"] == 'gnkt_bopz':
            string_work = 'ГНКТ БОПЗ ВНС'
        elif self.dict_data_well["work_plan"] == 'gnkt_opz':
            string_work = 'ГНКТ ОПЗ'
        elif self.dict_data_well["work_plan"] == 'gnkt_after_grp':
            string_work = 'ГНКТ ОСВ ГРП'
        else:
            string_work = 'ГНКТ'

        date_today = datetime.now()
        data_work = (self.dict_data_well["well_number"]._value,
                     self.dict_data_well["well_area"]._value,
                     self.dict_data_well["region"],
                     well_data.costumer,
                     well_data.contractor,
                     string_work,
                     self.dict_data_well["type_kr"].split(" ")[0],
                     date_today,
                     well_data.DICT_VOLUME_CHEMISTRY['цемент'],
                     well_data.DICT_VOLUME_CHEMISTRY['HCl'],
                     well_data.DICT_VOLUME_CHEMISTRY['HF'],
                     well_data.DICT_VOLUME_CHEMISTRY['NaOH'],
                     well_data.DICT_VOLUME_CHEMISTRY['ВТ СКО'],
                     well_data.DICT_VOLUME_CHEMISTRY['Глина'],
                     well_data.DICT_VOLUME_CHEMISTRY['песок'],
                     well_data.DICT_VOLUME_CHEMISTRY['РПК'],
                     well_data.DICT_VOLUME_CHEMISTRY['РПП'],
                     well_data.DICT_VOLUME_CHEMISTRY["извлекаемый пакер"],
                     well_data.DICT_VOLUME_CHEMISTRY["ЕЛАН"],
                     well_data.DICT_VOLUME_CHEMISTRY['растворитель'],
                     well_data.DICT_VOLUME_CHEMISTRY["РИР 2С"],
                     well_data.DICT_VOLUME_CHEMISTRY["РИР ОВП"],
                     well_data.DICT_VOLUME_CHEMISTRY['гидрофабизатор'],
                     round(self.dict_data_well["norm_of_time"], 1),
                     self.dict_data_well["fluid"]
                     )

        query = f"INSERT INTO chemistry " \
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                f"%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        from data_base.work_with_base import Classifier_well
        Classifier_well.insert_database('well_data', data_work, query)

    @staticmethod
    def check_process():
        count_zima = 0
        for proc in psutil.process_iter():
            if proc.name() == 'ZIMA.exe':
                count_zima += count_zima
        if count_zima > 1:
            return True  # Процесс найден

        return False  # Процесс не найден

    @staticmethod
    def close_process():
        for proc in psutil.process_iter():
            if proc.name() == 'ZIMA.exe':
                proc.terminate()  # Принудительное завершение

    @staticmethod
    def show_confirmation():
        reply = QMessageBox.question(None, 'Закрыть Zima?',
                                     'Приложение Zima.exe работает. Вы хотите Перезапустить его?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            MyWindow.close_process()

    @staticmethod
    def check_connection(host, port=5432):
        """Проверяет соединение с удаленным хостом по указанному порту."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # Устанавливаем таймаут 2 секунды
            sock.connect((host, port))
            sock.close()
            return True
        except socket.error:
            return False

    # Остальная часть кода...

    def initUI(self):

        self.setWindowTitle("ZIMA")
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

        self.correctNEKButton = QPushButton("Скорректировать НЭК")
        self.correctNEKButton.clicked.connect(self.correctNEK)
        self.toolbar.addWidget(self.correctNEKButton)

        self.correct_curator_Button = QPushButton("Скорректировать куратора")
        self.correct_curator_Button.clicked.connect(self.correct_curator)
        self.toolbar.addWidget(self.correct_curator_Button)

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
        self.create_KRS_change = self.create_file.addAction('Корректировка плана КРС', self.action_clicked)
        self.create_KRS_DP = self.create_file.addAction('Дополнительный план КРС', self.action_clicked)
        self.create_KRS_DP_in_base = self.create_file.addAction('Дополнительный план КРС из базы', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_gnkt_opz = self.create_GNKT.addAction(' ГНКТ ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('ГНКТ Фрезерование', self.action_clicked)
        self.create_GNKT_GRP = self.create_GNKT.addAction('Освоение после ГРП', self.action_clicked)
        self.create_GNKT_BOPZ = self.create_GNKT.addAction('БОПЗ ГНКТ', self.action_clicked)
        self.create_PRS = self.create_file.addAction('План ПРС', self.action_clicked)
        # self.open_file = self.fileMenu.addAction('Открыть', self.action_clicked)
        # self.save_file = self.fileMenu.addAction('Сохранить', self.action_clicked)
        # self.save_file_as = self.fileMenu.addAction('Сохранить как', self.action_clicked)

        self.class_well = self.classifierMenu.addMenu('&ООО Башнефть-Добыча')
        self.costumer_class_well = self.class_well.addMenu('Классификатор')
        self.costumer_select = self.class_well.addMenu('Перечень скважин без глушения')

        self.class_well_TGM = self.costumer_class_well.addMenu('&Туймазинский регион')
        self.class_well_TGM_open = self.class_well_TGM.addAction('&открыть перечень', self.action_clicked)

        self.class_well_IGM = self.costumer_class_well.addMenu('&Ишимбайский регион')

        self.class_well_IGM_open = self.class_well_IGM.addAction('&открыть перечень', self.action_clicked)

        self.class_well_CHGM = self.costumer_class_well.addMenu('&Чекмагушевский регион')
        self.class_well_CHGM_open = self.class_well_CHGM.addAction('&открыть перечень', self.action_clicked)

        self.class_well_KGM = self.costumer_class_well.addMenu('&Краснохолмский регион')
        self.class_well_KGM_open = self.class_well_KGM.addAction('&открыть перечень', self.action_clicked)

        self.class_well_AGM = self.costumer_class_well.addMenu('&Арланский регион')
        self.class_well_AGM_open = self.class_well_AGM.addAction('&открыть перечень', self.action_clicked)

        self.without_jamming_TGM = self.costumer_select.addMenu('&Туймазинский регион')
        self.without_jamming_TGM_open = self.without_jamming_TGM.addAction('&открыть перечень', self.action_clicked)

        self.without_jamming_IGM = self.costumer_select.addMenu('&Ишимбайский регион')
        self.without_jamming_IGM_open = self.without_jamming_IGM.addAction('&открыть перечень', self.action_clicked)

        self.without_jamming_CHGM = self.costumer_select.addMenu('&Чекмагушевский регион')
        self.without_jamming_CHGM_open = self.without_jamming_CHGM.addAction('&открыть перечень', self.action_clicked)

        self.without_jamming_KGM = self.costumer_select.addMenu('&Краснохолмский регион')
        self.without_jamming_KGM_open = self.without_jamming_KGM.addAction('&открыть перечень', self.action_clicked)

        self.without_jamming_AGM = self.costumer_select.addMenu('&Арланский регион')
        self.without_jamming_AGM_open = self.without_jamming_AGM.addAction('&открыть перечень', self.action_clicked)

        asd = well_data.user[1]
        if 'Зуфаров' in well_data.user[1] and 'И' in well_data.user[1] and 'М' in well_data.user[1]:
            self.class_well_TGM_reload = self.class_well_TGM.addAction('&обновить', self.action_clicked)
            self.class_well_IGM_reload = self.class_well_IGM.addAction('&обновить', self.action_clicked)
            self.class_well_CHGM_reload = self.class_well_CHGM.addAction('&обновить', self.action_clicked)
            self.class_well_KGM_reload = self.class_well_KGM.addAction('&обновить', self.action_clicked)
            self.class_well_AGM_reload = self.class_well_AGM.addAction('&обновить', self.action_clicked)
            self.without_jamming_TGM_reload = self.without_jamming_TGM.addAction('&обновить', self.action_clicked)
            self.without_jamming_IGM_reload = self.without_jamming_IGM.addAction('&обновить', self.action_clicked)
            self.without_jamming_CHGM_reload = self.without_jamming_CHGM.addAction('&обновить', self.action_clicked)
            self.without_jamming_KGM_reload = self.without_jamming_KGM.addAction('&обновить', self.action_clicked)
            self.without_jamming_AGM_reload = self.without_jamming_AGM.addAction('&обновить', self.action_clicked)

        self.signatories_Bnd = self.signatories.addAction('&БашНефть-Добыча', self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        from data_correct_position_people import CorrectSignaturesWindow

        action = self.sender()

        if action == self.create_KRS and self.table_widget == None:
            self.work_plan = 'krs'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()

        elif action == self.create_KRS_DP and self.table_widget == None:
            self.work_plan = 'dop_plan'
            self.dict_data_well["work_plan"] = 'dop_plan'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()
        elif action == self.create_KRS_DP_in_base and self.table_widget == None:
            self.work_plan = 'dop_plan_in_base'
            self.dict_data_well["work_plan"] = 'dop_plan_in_base'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()

        elif action == self.create_KRS_change and self.table_widget == None:
            self.work_plan = 'plan_change'
            self.dict_data_well["work_plan"] = 'plan_change'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()

        elif action == self.create_gnkt_opz and self.table_widget == None:
            self.work_plan = 'gnkt_opz'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()


        elif action == self.create_GNKT_GRP and self.table_widget == None:
            self.work_plan = 'gnkt_after_grp'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()



        elif action == self.create_GNKT_BOPZ and self.table_widget == None:
            self.work_plan = 'gnkt_bopz'
            self.dict_data_well["bvo"] = True
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()



        elif action == self.create_GNKT_frez and self.table_widget == None:
            self.work_plan = 'gnkt_frez'
            self.tableWidgetOpen(self.work_plan)
            self.ws = self.open_read_excel_file_pz()




        elif action == self.signatories_Bnd:
            if self.signatures_window is None:
                self.signatures_window = CorrectSignaturesWindow()
                self.signatures_window.setWindowTitle("Подписанты")
                # self.signatures_window.setGeometry(200, 400, 300, 400)
                self.signatures_window.show()
            else:
                self.signatures_window.close()
                self.signatures_window = None


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
                self.open_gis_application(self.fname)
        elif action == self.application_geophysical:
            pass

        elif 'Зуфаров' in well_data.user[1] and 'И' in well_data.user[1] and 'М' in well_data.user[1]:

            if action == self.class_well_TGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_class_well(costumer, 'ТГМ')
            elif action == self.class_well_CHGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_class_well(costumer, 'ЧГМ')
            elif action == self.class_well_KGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_class_well(costumer, 'КГМ')
            elif action == self.class_well_AGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_class_well(costumer, 'АГМ')
            elif action == self.without_jamming_TGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_without_damping(costumer, 'ТГМ')
            elif action == self.without_jamming_CHGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_without_damping(costumer, 'ЧГМ')
            elif action == self.without_jamming_KGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_without_damping(costumer, 'КГМ')
            elif action == self.without_jamming_AGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_without_damping(costumer, 'АГМ')
            elif action == self.without_jamming_IGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_without_damping(costumer, 'ИГМ')

            elif action == self.class_well_IGM_reload:
                costumer = 'ООО Башнефть-добыча'
                self.reload_class_well(costumer, 'ИГМ')

        else:
            mes = QMessageBox.question(self, 'Информация', 'Необходимо закрыть текущий проект, закрыть?')
            if mes == QMessageBox.StandardButton.Yes:
                self.close_file()

    def reload_class_well(self, costumer, region):
        from data_base.work_with_base import Classifier_well
        self.fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                              "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if self.fname:
            try:
                Classifier_well.export_to_database_class_well(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    def close_splash(self):
        splash_hwnd = win32gui.FindWindow(None, "Splash Screen")  # При необходимости измените название окна
        if splash_hwnd:
            win32gui.PostMessage(splash_hwnd, win32con.WM_CLOSE, 0, 0)

    def open_without_damping(self, costumer, region):
        from data_base.work_with_base import Classifier_well

        if self.new_window is None:

            self.new_window = Classifier_well(costumer, region, 'damping')
            self.new_window.setWindowTitle("Перечень скважин без глушения")
            # self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def open_pvr_application(self, fname):
        from open_pz import CreatePZ
        from application_pvr import PvrApplication
        if fname:
            # try:
            self.read_pz(fname)
            well_data.pause = True
            read_pz = CreatePZ(self.wb, self.ws)
            sheet = read_pz.open_excel_file(self.ws, self.work_plan)
            self.rir_window = PvrApplication(self.table_pvr)
            self.rir_window.show()

            self.pause_app()
            well_data.pause = False

    def open_gis_application(self, fname):
        from open_pz import CreatePZ
        from application_gis import GisApplication
        if fname:
            # try:
            self.read_pz(fname)
            well_data.pause = True
            read_pz = CreatePZ(self.wb, self.ws)
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
            # self.new_window.setGeometry(200, 400, 300, 400)
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
                Classifier_well.export_to_sqlite_without_juming(self, self.fname, costumer, region)

            except FileNotFoundError:
                print('Файл не найден')

    def tableWidgetOpenNormir(self, work_plan):

        if self.table_widget is None:
            # Создание объекта TabWidget
            self.tabWidget = QTabWidget()
            self.table_widget = QTableWidget()

            self.table_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_widget.customContextMenuRequested.connect(self.openContextMenuNormir)
            self.setCentralWidget(self.tabWidget)
            self.model = self.table_widget.model()

            # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
            # Указанная строка и столбец - это ячейка, которая была нажата.
            self.table_widget.cellPressed[int, int].connect(self.clickedRowColumn)
            self.tabWidget.addTab(self.table_widget, 'Нормирование')

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
            if work_plan in ['gnkt_frez', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz']:
                self.table_title = QTableWidget()
                self.tabWidget.addTab(self.table_title, 'Титульник')
                self.table_schema = QTableWidget()
                self.tabWidget.addTab(self.table_schema, 'Схема скважины')
                self.tabWidget.addTab(self.table_widget, 'Ход работ')

            else:
                self.tabWidget.addTab(self.table_widget, 'Ход работ')

    def save_to_excel(self):
        if self.work_plan in ['gnkt_frez', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz']:
            self.save_to_gnkt()
        else:
            self.save_to_krs()

    def save_to_krs(self):
        from open_pz import CreatePZ
        from work_py.alone_oreration import is_number
        from data_base.work_with_base import excel_in_json
        from work_py.advanted_file import count_row_height

        if not self.table_widget is None:
            wb2 = Workbook()
            ws2 = wb2.get_sheet_by_name('Sheet')
            ws2.title = "План работ"

            ins_ind = self.dict_data_well["ins_ind2"]

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

            merged_cells_dict = {}
            # print(f' индекс объ {ins_ind}')
            for row in merged_cells:
                if row[0] >= ins_ind - 1:
                    merged_cells_dict.setdefault(row[0], []).append(row[1])
            plan_short = ''
            self.dict_data_well["norm_of_time"] = 0

            for i in range(1, len(work_list)):  # нумерация работ
                if i >= ins_ind + 1:
                    if is_number(work_list[i][11]) is True:
                        self.dict_data_well["norm_of_time"] += round(float(str(work_list[i][11]).replace(',', '.')), 1)
                    if work_list[i][0]:
                        plan_short += f'п.{work_list[i][1]} {work_list[i][0]} \n'

            count_row_height(self, wb2, self.ws, ws2, work_list, merged_cells_dict, ins_ind)

            self.dict_data_well["itog_ind_min"] = ins_ind
            self.dict_data_well["itog_ind_max"] = len(work_list)
            # print(f' длина {len(work_list)}')
            CreatePZ.add_itog(self, ws2, self.table_widget.rowCount() + 1, self.work_plan)

            # try:
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
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Зуфаров.png', coordinate)
                    elif 'М.К.Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 1}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Алиев махир.png', coordinate)
                    elif 'З.К. Алиев' in str(value):
                        coordinate = f'{get_column_letter(col - 1)}{row_ind - 1}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/Алиев Заур.png', coordinate)
                        break
                    elif 'Расчет жидкости глушения производится согласно МУ' in str(value):
                        coordinate = f'{get_column_letter(6)}{row_ind + 1}'
                        self.insert_image(ws2, f'{well_data.path_image}imageFiles/schema_well/формула.png', coordinate,
                                          330, 130)
                        break
            if self.work_plan in ['krs', 'plan_change']:
                self.create_short_plan(wb2, plan_short)
            #
            if self.work_plan not in ['dop_plan_in_base']:
                if 'Ойл' in well_data.contractor:
                    self.insert_image(ws2, f'{well_data.path_image}imageFiles/Хасаншин.png', 'H1')
                    self.insert_image(ws2, f'{well_data.path_image}imageFiles/Шамигулов.png', 'H4')

            excel_data_dict = excel_in_json(self, ws2)
            db = connection_to_database(well_data.DB_WELL_DATA)
            data_well_base = WorkDatabaseWell(db, self.dict_data_well)
            data_well_base.insert_in_database_well_data(self.dict_data_well["well_number"]._value, self.dict_data_well["well_area"]._value,
                                                        well_data.contractor, well_data.costumer,
                self.dict_data_well["data_well_dict"], excel_data_dict, self.work_plan)


            data_well_base.insert_data_in_chemistry()


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
            # print(f'Пользоватль{well_data.user}')
            if 'Зуфаров' in well_data.user[1]:
                path = 'D:/Documents/Desktop/ГТМ'
            else:
                path = ""

            filenames = self.definition_filenames()
            full_path = path + "/" + filenames

            if self.dict_data_well["bvo"] and self.work_plan != 'dop_plan':
                ws5 = wb2.create_sheet('Sheet1')
                ws5.title = "Схемы ПВО"
                ws5 = wb2["Схемы ПВО"]
                wb2.move_sheet(ws5, offset=-1)
                schema_list = self.check_pvo_schema(ws5, ins_ind + 2)

            # Перед сохранением установите режим расчета
            wb2.calculation.calcMode = "auto"

            if wb2:
                wb2.close()
                self.save_file_dialog(wb2, full_path)

                # wb2.save(full_path)
                print(f'Table data saved to Excel {full_path}')

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
        rgd_without_paker_action = QAction("РГД по колонне", self)
        rgd_menu.addAction(rgd_without_paker_action)
        rgd_without_paker_action.triggered.connect(self.rgd_without_paker_action)

        po_action = QAction("прихватоопределить", self)
        geophysical.addAction(po_action)
        po_action.triggered.connect(self.poNewWindow)

        rgd_with_paker_action = QAction("РГД с пакером", self)
        rgd_menu.addAction(rgd_with_paker_action)
        rgd_with_paker_action.triggered.connect(self.rgd_with_paker_action)

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

        kompressVoronka_action = QAction("Замер Рпл", self)
        geophysical.addAction(kompressVoronka_action)
        kompressVoronka_action.triggered.connect(self.pressuar_gis)

        del_menu = context_menu.addMenu('удаление строки')
        emptyString_action = QAction("добавить пустую строку", self)
        del_menu.addAction(emptyString_action)
        emptyString_action.triggered.connect(self.emptyString)

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

        sgm_work = QAction("СГМ", self)
        template_menu.addAction(sgm_work)
        sgm_work.triggered.connect(self.sgm_work)

        template_pero = QAction("проходимость по перу", self)
        template_menu.addAction(template_pero)
        template_pero.triggered.connect(self.template_pero)

        paker_aspo = QAction("очистка колонны от АСПО с пакером и заглушкой", self)
        template_menu.addAction(paker_aspo)
        paker_aspo.triggered.connect(self.paker_clear_aspo)

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
        emergency_sticking_action.triggered.connect(self.lar_po_action)

        emergency_print_work_action = QAction("СПО печати", self)
        emergency_menu.addAction(emergency_print_work_action)
        emergency_print_work_action.triggered.connect(self.emergency_print_work_action)

        lar_sbt_action = QAction("ловильные работы", self)
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
        grp_with_paker_action = QAction('ГРП с одним пакером')
        grp_menu.addAction(grp_with_paker_action)
        grp_with_paker_action.triggered.connect(self.grp_with_paker)

        grp_with_gpp_action = QAction('ГРП с ГПП')
        grp_menu.addAction(grp_with_gpp_action)
        grp_with_gpp_action.triggered.connect(self.grp_with_gpp)

        alone_menu = action_menu.addMenu('одиночные операции')

        mkp_action = QAction('Ревизия МКП')
        alone_menu.addAction(mkp_action)
        mkp_action.triggered.connect(self.mkp_revision)

        block_pack_action = QAction('Блок пачка')
        alone_menu.addAction(block_pack_action)
        block_pack_action.triggered.connect(self.block_pack)

        tubing_pressure_testing_action = QAction('Опрессовка поинтервальная НКТ')
        alone_menu.addAction(tubing_pressure_testing_action)
        tubing_pressure_testing_action.triggered.connect(self.tubing_pressure_testing)

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

        pakerIzvlek_action = QAction('извлекаемый пакер')
        rir_menu.addAction(pakerIzvlek_action)
        pakerIzvlek_action.triggered.connect(self.pakerIzvlek_action)

        rir_action = QAction('РИР')
        rir_menu.addAction(rir_action)
        rir_action.triggered.connect(self.rir_action)

        claySolision_action = QAction('Глинистый раствор в ЭК')
        rir_menu.addAction(claySolision_action)
        claySolision_action.triggered.connect(self.claySolision)

        gno_menu = action_menu.addAction('Спуск фондового оборудования')
        gno_menu.triggered.connect(self.gno_bottom)

        context_menu.exec_(self.mapToGlobal(position))

    def clickedRowColumn(self, r, c):

        self.ins_ind = r + 1
        self.dict_data_well["ins_ind"] = r + 1
        # print(r, self.dict_data_well["count_row_well"])
        if r > self.dict_data_well["count_row_well"] and 'gnkt' not in self.work_plan:
            data = self.read_clicked_mouse_data(r)

    def close_file(self):
        from find import ProtectedIsNonNone, ProtectedIsDigit

        temp_folder = r'C:\Windows\Temp'

        try:
            if 'Зуфаров' in well_data.user:
                for filename in os.listdir(temp_folder):
                    file_path = os.path.join(temp_folder, filename)
                    # Удаляем только файлы, а не директории
                    if os.path.isfile(file_path):
                        os.remove(file_path)

        except Exception as e:
            QMessageBox.critical(window, "Ошибка", f"Не удалось очистить папку с временными файлами: {e}")

        if not self.table_widget is None:
            self.table_widget.clear()
            self.table_widget.resizeColumnsToContents()
            self.table_widget = None
            self.tabWidget = None
            self.dict_data_well["stabilizator_true"] = False
            self.dict_data_well["column_head_m"] = ''
            self.dict_data_well["date_drilling_cancel"] = ''
            self.dict_data_well["date_drilling_run"] = ''
            self.dict_data_well["wellhead_fittings"] = ''
            self.dict_data_well["dict_perforation_short"] = {}
            self.dict_data_well['plast_work_short'] = []
            self.table_widget = None
            self.dict_data_well["norm_of_time"] = 0
            self.dict_data_well["gips_in_well"] = False
            self.dict_data_well["grp_plan"] = False
            self.dict_data_well["bottom"] = 0
            well_data.nkt_opressTrue = False
            self.dict_data_well["bottomhole_drill"] = ProtectedIsNonNone(0)
            self.dict_data_well["open_trunk_well"] = False
            self.dict_data_well["norm_of_time"] = 0
            well_data.lift_ecn_can = False
            well_data.pause = True
            self.dict_data_well["check_data_in_pz"] = []
            well_data.sucker_rod_none = True
            self.dict_data_well["curator"] = '0'
            well_data.lift_ecn_can_addition = False
            well_data.column_passability = False
            self.dict_data_well["column_additional_passability"] = False
            self.dict_data_well["template_depth"] = 0

            self.dict_data_well["gnkt_length"] = 0
            well_data.diametr_length = 0
            self.dict_data_well["iznos"] = 0
            well_data.pipe_mileage = 0
            well_data.pipe_fatigue = 0
            well_data.pvo = 0
            well_data.previous_well = 0
            well_data.b_plan = 0
            well_data.pipes_ind = ProtectedIsDigit(0)
            well_data.sucker_rod_ind = ProtectedIsDigit(0)
            self.dict_data_well["expected_Q"] = 0
            self.dict_data_well["expected_P"] = 0
            well_data.plast_select = ''
            self.dict_data_well["dict_perforation"] = {}
            self.dict_data_well["dict_perforation_project"] = {}
            self.dict_data_well["itog_ind_min"] = 0
            self.dict_data_well["kat_pvo"] = 2
            self.dict_data_well["gaz_f_pr"] = []
            well_data.paker_layout = 0
            self.dict_data_well["cat_P_P"] = []
            self.dict_data_well["ribbing_interval"] = []
            self.dict_data_well["column_direction_diametr"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_direction_wall_thickness"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_direction_lenght"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_conductor_diametr"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_conductor_wall_thickness"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_conductor_lenght"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_additional_diametr"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_additional_wall_thickness"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["head_column_additional"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["shoe_column_additional"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_diametr"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["column_wall_thickness"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["shoe_column"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["bottomhole_artificial"] = ProtectedIsNonNone(5000)
            self.dict_data_well["max_expected_pressure"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["head_column_additional"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["leakiness_count"] = 0
            self.dict_data_well["bur_rastvor"] = ''
            well_data.data, well_data.rowHeights, well_data.colWidth, well_data.boundaries_dict = '', '', '', ''
            well_data.data_in_base = False
            self.dict_data_well["well_volume_in_PZ"] = []
            self.dict_data_well["expected_Pick_up"] = {}
            self.dict_data_well["current_bottom"] = 0
            self.dict_data_well["emergency_bottom"] = self.dict_data_well["current_bottom"]
            self.dict_data_well["fluid_work"] = 0
            self.dict_data_well["groove_diameter"] = ''
            self.dict_data_well["static_level"] = ProtectedIsNonNone('не корректно')
            self.dict_data_well["dinamic_level"] = ProtectedIsNonNone('не корректно')
            well_data.work_perforations_approved = False
            self.dict_data_well["dict_leakiness"] = {}
            self.dict_data_well["leakiness"] = False
            self.dict_data_well["emergency_well"] = False
            
            self.dict_data_well["emergency_count"] = 0
            well_data.DICT_VOLUME_CHEMISTRY = {'пункт': [], 'цемент': 0.0, 'HCl': 0.0, 'HF': 0.0, 'NaOH': 0.0,
                                               'ВТ СКО': 0.0,
                                               'Глина': 0.0, 'растворитель': 0.0, 'уд.вес': 0.0,
                                               'песок': 0.0, 'РПК': 0.0, 'РПП': 0.0, "извлекаемый пакер": 0.0,
                                               "ЕЛАН": 0.0,
                                               'РИР 2С': 0.0, 'РИР ОВП': 0.0, 'гидрофабизатор': 0.0}
            self.dict_data_well["skm_interval"] = []
            well_data.work_perforations = []
            well_data.work_perforations_dict = {}
            self.dict_data_well["paker_do"] = {"do": 0, "posle": 0}
            self.dict_data_well["column_additional"] = False
            self.dict_data_well["well_number"] = ProtectedIsNonNone('')
            self.dict_data_well["well_area"] = ProtectedIsNonNone('')
            well_data.values = []
            well_data.dop_work_list = None
            self.dict_data_well["depth_fond_paker_do"] = {"do": 0, "posle": 0}
            self.dict_data_well["paker2_do"] = {"do": 0, "posle": 0}
            self.dict_data_well["depth_fond_paker2_do"] = {"do": 0, "posle": 0}
            self.dict_data_well["perforation_roof"] = 50000
            self.dict_data_well["data_x_min"] = 0
            self.dict_data_well["perforation_roof"] = 0
            self.dict_data_well["dict_pump_SHGN"] = {"do": '0', "posle": '0'}
            self.dict_data_well["dict_pump_ECN"] = {"do": '0', "posle": '0'}
            self.dict_data_well["dict_pump_SHGN_h"] = {"do": '0', "posle": '0'}
            self.dict_data_well["dict_pump_ECN_h"] = {"do": '0', "posle": '0'}
            well_data.dict_pump = {"do": '0', "posle": '0'}
            self.dict_data_well["leakiness_interval"] = []
            well_data.dict_pump_h = {"do": 0, "posle": 0}
            self.dict_data_well["ins_ind"] = 0
            self.dict_data_well["ins_ind2"] = 0
            self.dict_data_well["image_data"] = []
            self.dict_data_well["current_bottom2"] = 5000
            well_data.len_razdel_1 = 0
            self.dict_data_well["count_template"] = 0
            well_data.data_well_is_True = False
            self.dict_data_well["cat_P_1"] = []
            well_data.countAcid = 0
            self.dict_data_well["first_pressure"] = ProtectedIsDigit(0)
            well_data.swabTypeComboIndex = 1
            well_data.swab_true_edit_type = 1
            self.dict_data_well["data_x_max"] = ProtectedIsDigit(0)
            self.dict_data_well["drilling_interval"] = []
            self.dict_data_well["max_angle"] = 0
            well_data.pakerTwoSKO = False
            well_data.privyazkaSKO = 0
            self.dict_data_well["h2s_pr"] = []
            self.dict_data_well["cat_h2s_list"] = []
            self.dict_data_well["dict_perforation_short"] = {}
            self.dict_data_well["h2s_mg"] = []
            well_data.lift_key = 0
            self.dict_data_well["max_admissible_pressure"] = ProtectedIsNonNone(0)
            self.dict_data_well["region"] = ''
            self.dict_data_well["for_paker_list"] = False
            self.dict_data_well["dict_nkt"] = {}
            self.dict_data_well["dict_nkt_po"] = {}
            self.dict_data_well["data_well_max"] = ProtectedIsNonNone(0)
            well_data.data_pvr_max = ProtectedIsNonNone(0)
            self.dict_data_well["dict_sucker_rod"] = {}
            self.dict_data_well["dict_sucker_rod_po"] = {}
            self.dict_data_well["row_expected"] = []
            well_data.rowHeights = []
            self.dict_data_well["plast_project"] = []
            self.dict_data_well['plast_work'] = []
            self.dict_data_well["leakiness_count"] = 0
            self.dict_data_well['plast_all'] = []
            well_data.condition_of_wells = ProtectedIsNonNone(0)
            self.dict_data_well["cat_well_min"] = ProtectedIsNonNone(0)
            self.dict_data_well["bvo"] = False
            self.dict_data_well["old_version"] = False
            self.dict_data_well["image_list"] = []
            self.dict_data_well["problem_with_ek"] = False
            self.dict_data_well["problem_with_ek_depth"] = self.dict_data_well["current_bottom"]
            self.dict_data_well["problem_with_ek_diametr"] = 220
            path = f"{well_data.path_image}/imageFiles/image_work"[1:]
            try:
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if path in file_path:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
            except:
                pass

            QMessageBox.information(self, 'Обновление', 'Данные обнулены')

    def on_finished(self):
        print("Работа с файлом Excel завершена.")

    def tubing_pressure_testing(self):
        from work_py.tubing_pressuar_testing import TubingPressuarWindow

        if self.operation_window is None:
            self.operation_window = TubingPressuarWindow(self.dict_data_well, self.table_widget)
            self.operation_window.setGeometry(50, 50, 900, 500)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def read_clicked_mouse_data(self, row):
        from work_py.advanted_file import definition_plast_work
        from data_correct import DataWindow

        row = row - self.dict_data_well["count_row_well"]
        # print(self.dict_data_well["column_diametr"]._value)
        data = self.dict_data_well["data_list"]

        self.dict_data_well["current_bottom"] = data[row][1]
        self.dict_data_well["dict_perforation"] = json.loads(data[row][2])
        self.dict_data_well['plast_all'] = json.loads(data[row][3])
        self.dict_data_well['plast_work'] = json.loads(data[row][4])
        self.dict_data_well["dict_leakiness"] = json.loads(data[row][5])
        aaaaaaa = self.dict_data_well["dict_leakiness"]
        self.dict_data_well["column_additional"] = data[row][6]

        self.dict_data_well["fluid_work"] = data[row][7]
        self.dict_data_well["template_depth"], self.dict_data_well["template_lenght"], self.dict_data_well["template_depth_addition"], self.dict_data_well["template_lenght_addition"] = json.loads(
            data[row][11])
        self.dict_data_well["skm_interval"] = json.loads(data[row][12])

        self.dict_data_well["problem_with_ek_depth"] = data[row][13]
        self.dict_data_well["problem_with_ek_diametr"] = data[row][14]


        DataWindow.definition_open_trunk_well(self)

        definition_plast_work(self)
        try:
            self.dict_data_well["ribbing_interval"] = json.loads(data[row][15])

        except:
            pass

        # print(self.dict_data_well["skm_interval"])

    def frezering_port_action(self):
        from work_py.drilling import Drill_window
        drilling_work_list = Drill_window.frezer_ports(self)
        self.populate_row(self.ins_ind, drilling_work_list, self.table_widget)



    def drilling_action_nkt(self):
        if self.operation_window is None:
            from work_py.drilling import Drill_window
            self.operation_window = Drill_window(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def magnet_action(self):

        from work_py.emergency_magnit import EmergencyMagnit
        if self.operation_window is None:
            self.operation_window = EmergencyMagnit(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 300, 400)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

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
        from work_py.emergency_lar import EmergencyLarWork
        if self.operation_window is None:
            self.operation_window = EmergencyLarWork(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 300, 400)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def lar_po_action(self):
        from work_py.emergency_po import EmergencyPo
        if self.operation_window is None:
            self.operation_window = EmergencyPo(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 300, 400)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def emergency_print_work_action(self):
        from work_py.emergency_printing import EmergencyPrintWork
        if self.operation_window is None:
            self.operation_window = EmergencyPrintWork(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 300, 400)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def rgd_without_paker_action(self):
        from work_py.rgdVcht import rgd_without_paker
        rgd_without_paker_list = rgd_without_paker(self)
        self.populate_row(self.ins_ind, rgd_without_paker_list, self.table_widget)

    def rgd_with_paker_action(self):
        from work_py.rgdVcht import rgd_with_paker
        rgd_with_paker_list = rgd_with_paker(self)
        self.populate_row(self.ins_ind, rgd_with_paker_list, self.table_widget)

    def pressuar_gis(self):
        from work_py.alone_oreration import pressuar_gis

        pressuar_gis_list = pressuar_gis(self)
        self.populate_row(self.ins_ind, pressuar_gis_list, self.table_widget)

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
        from work_py.acids import GonsWindow

        if self.operation_window is None:
            self.operation_window = GonsWindow(self.dict_data_well, self.table_widget, self.dict_data_well)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def pakerIzvlek_action(self):
        from work_py.izv_paker import PakerIzvlek
        if self.operation_window is None:
            self.operation_window = PakerIzvlek(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def pvo_cat1(self):
        from work_py.alone_oreration import pvo_cat1
        pvo_cat1_work_list = pvo_cat1(self)
        self.populate_row(self.ins_ind, pvo_cat1_work_list, self.table_widget)

    def fluid_change_action(self):
        from work_py.change_fluid import Change_fluid_Window

        if self.operation_window is None:
            self.operation_window = Change_fluid_Window(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 100, 200)
            self.operation_window.show()
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def claySolision(self):
        from work_py.claySolution import ClayWindow
        if self.operation_window is None:
            well_data.countAcid = 0
            self.operation_window = ClayWindow(self.dict_data_well, self.table_widget)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def rir_action(self):
        from work_py.rir import RirWindow

        if self.operation_window is None:
            well_data.countAcid = 0
            self.operation_window = RirWindow(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 300, 400)

            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def grp_with_paker(self):
        from work_py.grp import GrpWindow

        if self.operation_window is None:
            self.operation_window = GrpWindow(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 500, 500)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def grp_with_gpp(self):
        from work_py.gpp import GppWindow

        if self.operation_window is None:
            self.operation_window = GppWindow(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 500, 500)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def filling_sand(self):
        from work_py.sand_filling import SandWindow

        if self.operation_window is None:
            self.operation_window = SandWindow(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 500, 500)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def washing_sand(self):
        from work_py.sand_filling import SandWindow

        print('Вставился отсыпка песком')
        washing_work_list = SandWindow.sandWashing(self)
        self.populate_row(self.ins_ind, washing_work_list, self.table_widget)

    def deleteString(self):
        selected_ranges = self.table_widget.selectedRanges()
        selected_rows = []
        if self.ins_ind > self.dict_data_well["count_row_well"]:
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
                self.dict_data_well["data_list"].pop(row - self.dict_data_well["count_row_well"])

    def emptyString(self):
        if self.ins_ind > self.dict_data_well["count_row_well"]:
            ryber_work_list = [[None, None, None, None, None, None, None, None, None, None, None, None]]
            self.populate_row(self.ins_ind, ryber_work_list, self.table_widget)

    def vp_action(self):
        from work_py.vp_cm import VpWindow

        if self.operation_window is None:
            self.operation_window = VpWindow(self.dict_data_well, self.table_widget)
            # self.operation_window.setGeometry(200, 400, 500, 500)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def swibbing_with_paker(self):
        from work_py.swabbing import SwabWindow

        if self.operation_window is None:
            self.operation_window = SwabWindow(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def kompress_with_voronka(self):
        from work_py.kompress import KompressWindow

        if self.operation_window is None:
            self.operation_window = KompressWindow(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def ryber_add(self):
        from work_py.raiding import Raid

        if self.operation_window is None:
            self.operation_window = Raid(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def gnkt_after_grp(self):
        from gnkt_after_grp import gnkt_work
        gnkt_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, gnkt_work_list, self.table_widget)

    def gno_bottom(self):
        from work_py.descent_gno import GnoDescentWindow

        if self.operation_window is None:
            self.operation_window = GnoDescentWindow(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def pressureTest(self):
        from work_py.opressovka import OpressovkaEK

        if self.operation_window is None:
            self.operation_window = OpressovkaEK(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def block_pack(self):
        from work_py.block_pack_work import BlockPackWindow

        self.operation_window = BlockPackWindow(self.dict_data_well, self.table_widget)
        self.set_modal_window(self.operation_window)
        self.pause_app()
        well_data.pause = True
        self.operation_window = None

    def template_pero(self):
        from work_py.pero_work import PeroWindow

        self.operation_window = PeroWindow(self.dict_data_well, self.table_widget)
        self.set_modal_window(self.operation_window)
        self.pause_app()
        well_data.pause = True
        self.operation_window = None

    def template_with_skm(self):
        from work_py.template_work import TemplateKrs

        if self.operation_window is None:
            self.operation_window = TemplateKrs(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def sgm_work(self):
        from work_py.sgm_work import TemplateKrs

        if self.operation_window is None:
            self.operation_window = TemplateKrs(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def paker_clear_aspo(self):
        from work_py.opressovka_aspo import PakerAspo

        if self.operation_window is None:
            self.operation_window = PakerAspo(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def template_without_skm(self):
        from work_py.template_without_skm import Template_without_skm

        if self.operation_window is None:
            self.operation_window = Template_without_skm(self.dict_data_well, self.table_widget)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None
        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None

    def acidPakerNewWindow(self):
        from work_py.acid_paker import AcidPakerWindow

        if self.acid_windowPaker is None:

            self.acid_windowPaker = AcidPakerWindow(self.dict_data_well, self.table_widget)
            self.acid_windowPaker.setGeometry(50, 50, 900, 500)
            self.set_modal_window(self.acid_windowPaker)
            self.pause_app()
            well_data.pause = True

        else:
            self.acid_windowPaker.close()  # Close window.
            self.acid_windowPaker = None

    def GeophysicalNewWindow(self):
        from work_py.geophysic import GeophysicWindow

        if self.operation_window is None:
            self.operation_window = GeophysicWindow(self.dict_data_well, self.table_widget)
            self.operation_window.setWindowTitle("Геофизические исследования")
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True
            self.operation_window = None  # Discard reference.


        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None  # Discard reference.

    def correctPVR(self):
        from perforation_correct import PerforationCorrect

        self.dict_data_well["current_bottom"], ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                              'Введите забой до которого нужно нормализовать')
        if self.perforation_correct_window2 is None:
            self.perforation_correct_window2 = PerforationCorrect(self.dict_data_well)
            self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
            self.set_modal_window(self.perforation_correct_window2)
            self.pause_app()
            well_data.pause = True
            self.perforation_correct_window2 = None

        else:
            self.perforation_correct_window2.close()
            self.perforation_correct_window2 = None

        self.dict_data_well["data_list"][-1][1] = self.dict_data_well["current_bottom"]

        self.dict_data_well["data_list"][-1][2] = json.dumps(self.dict_data_well["dict_perforation"], default=str, ensure_ascii=False, indent=4)

    def correct_curator(self):
        from work_py.curators import SelectCurator

        if self.new_window is None:
            self.new_window = SelectCurator()
            # WellCondition.leakage_window.setGeometry(200, 400, 300, 400)
            self.set_modal_window(self.new_window)
            self.pause_app()
            well_data.pause = True
            self.new_window = None  # Discard reference.
        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def correctNEK(self):
        from find import WellCondition
        from work_py.leakage_column import LeakageWindow

        if WellCondition.leakage_window is None:
            WellCondition.leakage_window = LeakageWindow()
            WellCondition.leakage_window.setWindowTitle("Корректировка негерметичности")
            # WellCondition.leakage_window.setGeometry(200, 400, 300, 400)
            self.set_modal_window(WellCondition.leakage_window)

            self.pause_app()
            self.dict_data_well["dict_leakiness"] = WellCondition.leakage_window.add_work()
            # print(f'словарь нарушений {self.dict_data_well["dict_leakiness"]}')
            well_data.pause = True
            WellCondition.leakage_window = None  # Discard reference.


        else:
            WellCondition.leakage_window.close()  # Close window.
            WellCondition.leakage_window = None  # Discard reference.
        self.dict_data_well["data_list"][-1][5] = json.dumps(self.dict_data_well["dict_leakiness"], default=str, ensure_ascii=False, indent=4)

    def correctData(self):
        from data_correct import DataWindow

        if self.correct_window is None:

            self.correct_window = DataWindow()
            self.correct_window.setWindowTitle("Окно корректировки")
            # self.correct_window.setGeometry(100, 400, 300, 400)
            self.set_modal_window(self.correct_window)
            self.pause_app()
            well_data.pause = True
            self.correct_window = None

        else:
            self.correct_window.close()  # Close window.
            self.correct_window = None  # Discard reference.

    def poNewWindow(self):
        from work_py.emergencyWork import emergencyECN

        template_pero_list = emergencyECN(self)
        self.populate_row(self.ins_ind, template_pero_list, self.table_widget)

    def perforationNewWindow(self):
        from work_py.perforation import PerforationWindow

        if len(self.dict_data_well["cat_P_1"]) > 1:
            if self.dict_data_well["cat_P_1"][1] == 1 and self.dict_data_well["kat_pvo"] != 1:
                msc = QMessageBox.information(self, 'Внимание', 'Не произведен монтаж первой категории')
                return

        if self.operation_window is None:

            self.operation_window = PerforationWindow(self.dict_data_well, self.table_widget)
            self.operation_window.setWindowTitle("Перфорация")
            # self.new_window.setGeometry(200, 400, 300, 400)
            self.set_modal_window(self.operation_window)
            self.pause_app()
            well_data.pause = True

        else:
            self.operation_window.close()  # Close window.
            self.operation_window = None  # Discard reference.

    def insertPerf(self):
        self.populate_row(self.ins_ind, self.perforation_list)

    def create_short_plan(self, wb2, plan_short):
        from work_py.descent_gno import TabPage_Gno

        ws4 = wb2.create_sheet('Sheet1')
        ws4.title = "Краткое содержание плана работ"
        ws4 = wb2["Краткое содержание плана работ"]

        for row in range(15):
            ws4.insert_rows(ws4.max_row)
        ws4.cell(row=1, column=1).value = self.dict_data_well["well_number"]._value
        ws4.cell(row=2, column=1).value = self.dict_data_well["well_area"]._value

        if self.dict_data_well["dict_pump_SHGN"]["do"] != 0 and self.dict_data_well["dict_pump_ECN"]["do"] == 0 and \
                self.dict_data_well["paker_do"]["do"] == 0:
            ws4.cell(row=3,
                     column=1).value = f'{self.dict_data_well["dict_pump_SHGN"]["do"]} -на гл. {self.dict_data_well["dict_pump_SHGN_h"]["do"]}м'
        elif self.dict_data_well["dict_pump_SHGN"]["do"] == 0 and self.dict_data_well["dict_pump_ECN"]["do"] != 0 and \
                self.dict_data_well["paker_do"]["do"] == 0:
            ws4.cell(row=3,
                     column=1).value = f'{self.dict_data_well["dict_pump_ECN"]["do"]} -на гл. {self.dict_data_well["dict_pump_ECN_h"]["do"]}м'
        elif self.dict_data_well["dict_pump_SHGN"]["do"] == 0 and self.dict_data_well["dict_pump_ECN"]["do"] != 0 and \
                self.dict_data_well["paker_do"]["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{self.dict_data_well["dict_pump_ECN"]["do"]} -на гл. {self.dict_data_well["dict_pump_ECN_h"]["do"]}м \n' \
                                       f'{self.dict_data_well["paker_do"]["do"]} на {self.dict_data_well["depth_fond_paker_do"]["do"]}м'
        elif self.dict_data_well["dict_pump_SHGN"]["do"] != 0 and self.dict_data_well["dict_pump_ECN"]["do"] == 0 and \
                self.dict_data_well["paker_do"]["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{self.dict_data_well["dict_pump_SHGN"]["do"]} -на гл. {self.dict_data_well["dict_pump_SHGN_h"]["do"]}м \n' \
                                       f'{self.dict_data_well["paker_do"]["do"]} на {self.dict_data_well["depth_fond_paker_do"]["do"]}м'
        elif self.dict_data_well["dict_pump_SHGN"]["do"] == 0 and self.dict_data_well["dict_pump_ECN"]["do"] == 0 and \
                self.dict_data_well["paker_do"]["do"] != 0:
            ws4.cell(row=3, column=1).value = f'{self.dict_data_well["paker_do"]["do"]} на {self.dict_data_well["depth_fond_paker_do"]["do"]}м'
        elif self.dict_data_well["dict_pump_SHGN"]["do"] == 0 and self.dict_data_well["dict_pump_ECN"]["do"] == 0 and \
                self.dict_data_well["paker_do"]["do"] == 0:
            ws4.cell(row=3, column=1).value = " "
        elif self.dict_data_well["dict_pump_SHGN"]["do"] != 0 and self.dict_data_well["dict_pump_ECN"]["do"] != 0 and \
                self.dict_data_well["paker_do"]["do"] != 0:
            ws4.cell(row=3,
                     column=1).value = f'{self.dict_data_well["dict_pump_SHGN"]["do"]} -на гл. {self.dict_data_well["dict_pump_SHGN_h"]["do"]}м \n' \
                                       f'{self.dict_data_well["dict_pump_ECN"]["do"]} -на гл. {self.dict_data_well["dict_pump_ECN_h"]["do"]}м \n' \
                                       f'{self.dict_data_well["paker_do"]["do"]} на {self.dict_data_well["depth_fond_paker_do"]["do"]}м '
        plast_str = ''
        pressur_set = set()
        # print(f'После {self.dict_data_well["dict_perforation_short"]}')
        for plast in list(self.dict_data_well["dict_perforation_short"].keys()):
            if self.dict_data_well["dict_perforation_short"][plast][
                'отключение'] is False and plast in self.dict_data_well["dict_perforation_short"]:
                for interval in self.dict_data_well["dict_perforation_short"][plast]["интервал"]:
                    plast_str += f'{plast[:4]}: {interval[0]}- {interval[1]} \n'
            elif self.dict_data_well["dict_perforation_short"][plast]['отключение'] and plast in self.dict_data_well["dict_perforation_short"]:
                for interval in self.dict_data_well["dict_perforation_short"][plast]["интервал"]:
                    plast_str += f'{plast[:4]} :{interval[0]}- {interval[1]} (изол)\n'
            try:
                a = self.dict_data_well["dict_perforation_short"]
                filter_list_pressuar = list(
                    filter(lambda x: type(x) in [int, float],
                           list(self.dict_data_well["dict_perforation_short"][plast]["давление"])))
                # print(f'фильтр -{filter_list_pressuar}')
                if filter_list_pressuar:
                    pressur_set.add(f'{plast[:4]} - {filter_list_pressuar}')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка вставки давления в краткое описание {e}')

        ws4.cell(row=6, column=1).value = f'НКТ: \n {TabPage_Gno.gno_nkt_opening(self.dict_data_well["dict_nkt"])}'
        ws4.cell(row=7, column=1).value = f'Рпл: \n {" ".join(list(pressur_set))}атм'
        # ws4.cell(row=8, column=1).value = f'ЖГС = {self.dict_data_well["fluid_work_short"]}г/см3'
        ws4.cell(row=9,
                 column=1).value = f'Нст- {self.dict_data_well["static_level"]._value}м / Ндин - {self.dict_data_well["dinamic_level"]._value}м'
        if self.dict_data_well["curator"] == 'ОР':
            ws4.cell(row=10, column=1).value = f'Ожид {self.dict_data_well["expected_Q"]}м3/сут при Р-{self.dict_data_well["expected_P"]}м3/сут'
        else:
            ws4.cell(row=10, column=1).value = f'Qн {self.dict_data_well["Qoil"]}т Qж- {self.dict_data_well["Qwater"]}м3/сут'
        ws4.cell(row=11, column=1).value = f'макс угол {self.dict_data_well["max_angle"]._value} на {self.dict_data_well["max_angle_H"]._value}'
        ws4.cell(row=1, column=2).value = self.dict_data_well["cdng"]._value
        try:
            try:
                category_pressuar = self.dict_data_well["dict_category"][self.dict_data_well['plast_work_short'][0]]["по давлению"].category
            except:
                category_pressuar = self.dict_data_well["category_pressuar2"]
            try:
                category_h2s = self.dict_data_well["dict_category"][self.dict_data_well['plast_work_short'][0]]["по сероводороду"].category
            except:
                category_h2s = self.dict_data_well["category_h2s_2"]
            try:
                gaz_f_pr = self.dict_data_well["gaz_f_pr"][0]
            except:
                gaz_f_pr = self.dict_data_well["gaz_f_pr_2"]

            ws4.cell(row=2, column=3).value = \
                f'Рпл - {category_pressuar},' \
                f' H2S -{category_h2s},' \
                f' газ факт -{gaz_f_pr}т/м3'
        except Exception as e:
            QMessageBox.warning(self, 'ОШИБКА',
                                f"Программа не смогла вставить данные в краткое содержание значения по "
                                f"Рпл {type(e).__name__}\n\n{str(e)}")
        column_well = f'{self.dict_data_well["column_diametr"]._value}х{self.dict_data_well["column_wall_thickness"]._value} в ' \
                      f'инт 0 - {self.dict_data_well["shoe_column"]._value}м ' \
            if self.dict_data_well["column_additional"] is False else \
            f'{self.dict_data_well["column_diametr"]._value} х {self.dict_data_well["column_wall_thickness"]._value} \n' \
            f'0 - {self.dict_data_well["shoe_column"]._value}м/\n{self.dict_data_well["column_additional_diametr"]._value}' \
            f' х {self.dict_data_well["column_additional_wall_thickness"]._value} в инт ' \
            f'{self.dict_data_well["head_column_additional"]._value}-{self.dict_data_well["head_column_additional"]._value}м'
        ws4.cell(row=1, column=7).value = column_well
        ws4.cell(row=4, column=7).value = f'Пробур забой {self.dict_data_well["bottomhole_drill"]._value}м'
        ws4.cell(row=5, column=7).value = f'Исскус забой {self.dict_data_well["bottomhole_artificial"]._value}м'
        ws4.cell(row=6, column=7).value = f'Тек забой {self.dict_data_well["bottom"]}м'

        ws4.cell(row=7, column=7).value = plast_str
        ws4.cell(row=11, column=7).value = f'Рмакс {self.dict_data_well["max_admissible_pressure"]._value}атм'
        ws4.cell(row=3, column=2).value = plan_short
        nek_str = 'НЭК '
        if len(self.dict_data_well["leakiness_interval"]) != 0:

            for nek in self.dict_data_well["leakiness_interval"]:
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
                        new_value = QtWidgets.QTableWidgetItem(
                            f'Установить подъёмный агрегат на устье не менее 60т. '
                            f'Пусковой комиссией составить акт готовности подьемного '
                            f'агрегата и бригады для проведения ремонта скважины.')
                        table_widget.setItem(row, column, new_value)

    def check_str_isdigit(self, string):

        # Паттерн для проверки: допустимы только цифры, точка и запятая
        pattern = r'^[\d.,]+$'

        # Проверка строки на соответствие паттерну
        if re.match(pattern, string):
            return True
        else:
            return False

    @staticmethod
    def delete_files():
        zip_path = os.path.dirname(os.path.abspath(__file__)) + '/ZIMA.zip'
        print(zip_path)
        destination_path = os.path.dirname(os.path.abspath(__file__)) + '/ZimaUpdate'
        a = os.path.exists(destination_path)
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)  # Удаляет папку ZimaUpdate
        if os.path.exists(zip_path):
            os.remove(zip_path)  # Удаляет файл Zima.zip


if __name__ == "__main__":
    # app3 = QApplication(sys.argv)

    app = QApplication(sys.argv)
    #  MyMainWindow.delete_files()

    if MyWindow.check_process():
        MyWindow.show_confirmation()



    # if well_data.connect_in_base:
    #     app2 = UpdateChecker()
    #     app2.check_version()
    #     if app2.window_close == True:
    #         MyWindow.set_modal_window(None, app2)
    #         well_data.pause = True
    #         self.pause_app()
    #         well_data.pause = False
    #         app2.close()dow = MyWindow()


    try:
        well_data.connect_in_base = connect_to_database('krs2')

        login_window = LoginWindow()
        login_window.setWindowModality(Qt.ApplicationModal)

        login_window.show()
        MyMainWindow.pause_app()
        well_data.pause = False
    except Exception as e:
        QMessageBox.warning(None, 'КРИТИЧЕСКАЯ ОШИБКА',
                            f'Критическая ошибка, смотри в лог {type(e).__name__}\n\n{str(e)}')

    window = MyWindow()
    window.show()


    sys.exit(app.exec_())