import sys
import openpyxl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QWidget, QLineEdit
from PyQt5 import QtCore, QtWidgets, QtGui

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

        elif action == self.save_file_as:
            self.saveFileDialog()


    def openContextMenu(self, position):
        from open_pz import CreatePZ
        from work_py.template_work import template_ek_without_skm

        context_menu = QMenu(self)

        action_menu = context_menu.addMenu("вид работ")
        pervoration_ins = action_menu.addMenu("окно перфорации")
        perforation_action = QAction("Перфорация", self)
        pervoration_ins.addAction(perforation_action)
        perforation_action.triggered.connect(self.openNewWindow)
        perforation_action1 = QAction("добавление в план", self)
        pervoration_ins.addAction(perforation_action1)
        perforation_action1.triggered.connect(self.insertPerf)

        opressovka_action = QAction("Опрессовка колонны", self)
        action_menu.addAction(opressovka_action)
        opressovka_action.triggered.connect(self.pressureTest)

        template_action = QAction("шаблоны", self)
        action_menu.addAction(template_action)
        opressovka_action.triggered.connect(template_ek_without_skm)



        context_menu.exec_(self.mapToGlobal(position))

    def clickedRowColumn(self, r, c):
        from open_pz import CreatePZ
        self.ins_ind = r


    def pressureTest(self):
        from work_py.opressovka import paker_list
        from open_pz import CreatePZ

        pressure_work1 = paker_list(1000, 10)
        print(f'индекс {self.ins_ind, len(pressure_work1)}')
        self.populate_row(self.ins_ind, pressure_work1)
        CreatePZ.ins_ind += len(pressure_work1) + 1

    def populate_row(self, ins_ind, work_list):

        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500), 120: (501, 600), 140: (601, 700)}

        for i, row_data in enumerate(work_list):
            row = ins_ind + i
            self.table_widget.insertRow(row)
            self.table_widget.setSpan(i+ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):
                # item = QtWidgets.QTableWidgetItem(data)
                widget = QtWidgets.QLabel(str( ))
                widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')
                self.table_widget.setCellWidget(row, column, widget)
                self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
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
        cols = 13
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height != None else 18 for
                           i in range(sheet.max_row)]

        for row in range(1, rows + 1):
            if row > 1 and row < rows - 1:
                self.table_widget.setRowHeight(row, int(rowHeights_exit[row]))
            for col in range(1, cols + 1):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())