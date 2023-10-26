import sys
import openpyxl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QWidget, QLineEdit
from PyQt5 import QtCore, QtWidgets, QtGui
from openpyxl.workbook import Workbook

import krs
import work_py.opressovka



class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()
        self.new_window = None
        self.ws = None
        self.ins_ind = None
        self.perforation_list = []
        self.dict_perforation_project = {}
        self.dict_work_pervorations = {}
        self.ins_ind_border = None
    def initUI(self):
        from work_py.mouse import TableWidget
        self.setWindowTitle("Main Window")
        self.setGeometry(500, 500, 600, 600)

        self.table_widget = TableWidget()
        self.table_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.openContextMenu)
        self.setCentralWidget(self.table_widget)
        self.createMenuBar()
        self.le = QLineEdit()
        self.model = self.table_widget.model()
        # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
        # Указанная строка и столбец - это ячейка, которая была нажата.
        self.table_widget.cellPressed[int, int].connect(self.clickedRowColumn)

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.fileMenu = QMenu('&Файл', self)
        self.classifierMenu = QMenu('&Классификатор', self)
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.classifierMenu)

        self.create_file = self.fileMenu.addMenu('&Создать')
        self.create_KRS = self.create_file.addAction('План КРС', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_GNKT_OPZ = self.create_GNKT.addAction('ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('Фрезерование', self.action_clicked)
        self.create_GNKT_GRP = self.create_GNKT.addAction('Освоение после ГРП', self.action_clicked)
        self.create_PRS = self.create_file.addAction('План ПРС', self.action_clicked)
        self.open_file = self.fileMenu.addAction('Открыть', self.action_clicked)
        self.save_file = self.fileMenu.addAction('Сохранить', self.action_clicked)
        self.save_file_as = self.fileMenu.addAction('Сохранить как', self.action_clicked)

        class_well = self.classifierMenu.addAction('&классификатор')
        list_without_jamming = self.classifierMenu.addAction('&Перечень без глушения')

    @QtCore.pyqtSlot()
    def action_clicked(self):
        from open_pz import CreatePZ
        action = self.sender()
        if action == self.create_KRS:
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                work_plan = 'krs'
                sheet = CreatePZ.open_excel_file(self, self.fname[0], work_plan)

                self.copy_pz(sheet)

            except FileNotFoundError:
                print('Файл не найден')

        elif action == self.create_GNKT_OPZ:
            print('кнопка нажата')
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                work_plan = 'gnkt_opz'
                sheet = CreatePZ.open_excel_file(self, self.fname[0], work_plan)
                self.copy_pz(sheet)

            except FileNotFoundError:
                print('Файл не найден')

            # if action == self.save_file:
            #     open_pz.open_excel_file().wb.save("test_unmerge.xlsx")
        elif action == self.save_file:

            self.save_to_excel(self.wb, self.ws)

        elif action == self.save_file_as:
            self.saveFileDialog()

    def save_to_excel(self, wb, ws):
        from open_pz import CreatePZ
        # print(f'граница {self.ins_ind_border}')
        ins_ind =  self.ins_ind_border

        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):

                item = self.table_widget.item(row, column)
                if item is not None:
                    if item.text() == 'ИТОГО:':
                        ins_int_border_bottom = row

        # ws.insert_rows(self.ins_ind_border, self.table_widget.rowCount()-self.ins_ind_border)
        work_list = []
        for row in range(self.table_widget.rowCount()):
            if row >= self.ins_ind_border:
                row_lst = []
                self.ins_ind_border += 1
                # ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=12)
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)
                    if item is not None:
                        row_lst.append(item.text())

                    #     ws.cell(row=row + 1, column=column + 1).value = item.text()
                work_list.append(row_lst)

        # print(ins_ind)
        # print(self.table_widget.rowCount())

        for i in range(2, len(work_list)):  # нумерация работ

            work_list[i][1] = i - 1
            if self.is_number(work_list[i][11]) == True:

                CreatePZ.normOfTime += float(work_list[i][11])

        print(f' норма {CreatePZ.normOfTime}')

        CreatePZ.count_row_height(ws, work_list, ins_ind)
        itog_ind_min = CreatePZ.itog_ind_min + len(work_list)
        CreatePZ.addItog(self, ws, self.table_widget.rowCount()+1, ins_ind + itog_ind_min)

        ws.print_area = f'B1:L{self.table_widget.rowCount()+45}'
        # ws.page_setup.fitToPage = True
        ws.page_setup.fitToHeight = False
        ws.page_setup.fitToWidth = True
        ws.print_options.horizontalCentered = True
        wb.save(f"{ CreatePZ.well_number} { CreatePZ.well_area} { CreatePZ.cat_P_1} категории.xlsx")

        print("Table data saved to Excel")

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False
    def openContextMenu(self, position):
        from open_pz import CreatePZ
        from work_py.template_work import template_ek_without_skm, template_ek

        context_menu = QMenu(self)

        action_menu = context_menu.addMenu("вид работ")
        # pervoration_ins = action_menu.addMenu("окно перфорации")
        perforation_action = QAction("Перфорация", self)
        action_menu.addAction(perforation_action)
        perforation_action.triggered.connect(self.openNewWindow)


        opressovka_action = QAction("Опрессовка колонны", self)
        action_menu.addAction(opressovka_action)
        opressovka_action.triggered.connect(self.pressureTest)

        template_with_skm = QAction("шаблон c СКМ", self)
        template_menu = action_menu.addMenu('Шаблоны')
        template_menu.addAction(template_with_skm)
        template_with_skm.triggered.connect(self.template_with_skm)

        ryber_action = QAction("Райбирование", self)
        action_menu.addAction(ryber_action)
        ryber_action.triggered.connect(self.ryberAdd)

        template_without_skm = QAction("шаблон без СКМ", self)
        template_menu.addAction(template_without_skm)
        template_without_skm.triggered.connect(self.template_without_skm)


        acid_menu = action_menu.addMenu('Кислотная обработка')

        acid_action_1paker = QAction("на одном пакере", self)
        acid_menu.addAction(acid_action_1paker)
        acid_action_1paker.triggered.connect(self.acid_action_1paker)

        gno_menu = action_menu.addMenu('Спуск фондового оборудования')
        gno_action = QAction('пакер')
        gno_menu.addAction(gno_action)
        gno_action.triggered.connect(self.gno_bottom)


        context_menu.exec_(self.mapToGlobal(position))

    def clickedRowColumn(self, r, c):
        from open_pz import CreatePZ
        self.ins_ind = r+1
        CreatePZ.ins_ind = r+1
        print(f' выбранная строка {self.ins_ind}')

    def ryberAdd(self):
        from work_py.raiding import raidingColumn

        print('Вставился райбер')
        ryber_work_list = raidingColumn(self)
        self.populate_row(self.ins_ind, ryber_work_list)
    def gno_bottom(self):
        from work_py.descent_gno import gno_down

        print('Вставился ГНО')
        gno_work_list = gno_down(self)
        self.populate_row(self.ins_ind, gno_work_list)

    def acid_action_1paker(self):
        from work_py.acids_work import acid_work
        print('Вставился кислотная обработка на одном пакере ')
        acid_work_list = acid_work(self)
        self.populate_row(self.ins_ind, acid_work_list)

    def pressureTest(self):
        from work_py.opressovka import paker_list

        print('Вставился опрессовка пакером')
        pressure_work1 = paker_list(self)
        print(f'индекс {self.ins_ind, len(pressure_work1)}')
        self.populate_row(self.ins_ind, pressure_work1)


    def template_with_skm(self):
        from work_py.template_work import template_ek
        from open_pz import CreatePZ
        template_ek_list = template_ek(self)
        print(f'индекс {self.ins_ind, len(template_ek_list)}')
        self.populate_row(self.ins_ind,  template_ek_list)
        CreatePZ.ins_ind += len(template_ek_list) + 1

    def template_without_skm(self):
        from work_py.template_work import template_ek_without_skm
        from open_pz import CreatePZ

        template_ek_list = template_ek_without_skm(self)
        print()
        print(f'индекс {self.ins_ind, len(template_ek_list)}')
        self.populate_row(self.ins_ind,  template_ek_list)
        CreatePZ.ins_ind += len(template_ek_list) + 1


    def populate_row(self, ins_ind, work_list):

        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500), 120: (501, 600), 140: (601, 700)}

        for i, row_data in enumerate(work_list):
            row = ins_ind + i
            self.table_widget.insertRow(row)
            self.table_widget.setSpan(i + ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):
                # item = QtWidgets.QTableWidgetItem(data)
                widget = QtWidgets.QLabel(str())
                widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')
                self.table_widget.setCellWidget(row, column, widget)
                if data != None:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if data != None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))

        # self.table_widget.resizeColumnsToContents()
        # self.table_widget.resizeRowsToContents()



    def openNewWindow(self):
        from work_py.perforation import PervorationWindow
        from open_pz import CreatePZ
        if self.new_window is None:
            print(f' проект перфорации {self.dict_perforation_project}')
            self.new_window = PervorationWindow(self.table_widget, self.ins_ind, self.dict_work_pervorations, self.dict_perforation_project)
            self.new_window.setWindowTitle("New Window")
            self.new_window.setGeometry(200, 200, 300, 200)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def insertPerf(self):

        self.populate_row(self.ins_ind, self.perforation_list)

    def copy_pz(self, sheet):
        from open_pz import CreatePZ
        rows = sheet.max_row
        merged_cells = sheet.merged_cells

        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(12)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height != None else 18 for
                           i in range(sheet.max_row)]

        for row in range(1, rows + 1):
            if row > 1 and row < rows - 1:
                self.table_widget.setRowHeight(row, int(rowHeights_exit[row]))
            for col in range(1, 12 + 1):
                if sheet.cell(row=row, column=col).value != None:
                    cell_value = str(sheet.cell(row=row, column=col).value)
                    item = QtWidgets.QTableWidgetItem(str(cell_value))
                    self.table_widget.setItem(row - 1, col - 1, item)
                    # Проверяем, является ли текущая ячейка объединенной
                    for merged_cell in merged_cells:
                        if row in range(merged_cell.min_row, merged_cell.max_row + 1) and \
                                col in range(merged_cell.min_col, merged_cell.max_col + 1):
                            # Устанавливаем количество объединяемых строк и столбцов для текущей ячейки
                            self.table_widget.setSpan(row - 1, col - 1,
                                                      merged_cell.max_row - merged_cell.min_row + 1,
                                                      merged_cell.max_col - merged_cell.min_col + 1)
        self.populate_row(self.table_widget.rowCount(), krs.work_krs(self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())