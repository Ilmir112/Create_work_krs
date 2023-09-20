import openpyxl
import sys

from openpyxl.utils import get_column_letter

import open_pz
# import plan.py
from PyQt5.QtWidgets import QTextEdit
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QMenuBar, QFileDialog,QLineEdit

class MyWindow(QMainWindow):
    fname = ''

    def __init__(self, parent = None, *args, **kwargs):
        super(MyWindow, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle('Создание')
        self.setGeometry(500, 450, 550, 400)
        self.table_widget = QtWidgets.QTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.createMenuBar()
        self.le = QLineEdit()
        # self.line_edit = QtWidgets.QLineEdit(self)

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.fileMenu = QMenu('&Файл', self)
        self.classifierMenu = QMenu('&Классификатор', self)
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.classifierMenu)

        self.create_file =self.fileMenu.addMenu('&Создать')
        self.create_KRS = self.create_file.addAction('План КРС', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_GNKT_OPZ = self.create_GNKT.addAction('ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('Фрезерование', self.action_clicked)
        self.create_GNKT_GRP = self.create_GNKT.addAction('Освоение после ГРП', self.action_clicked)
        self.create_PRS = self.create_file.addAction('План ПРС', self.action_clicked)
        self.open_file = self.fileMenu.addAction('Открыть', self.action_clicked )
        self.save_file = self.fileMenu.addAction('Сохранить', self.action_clicked)
        self.save_file = self.fileMenu.addAction('Сохранить как', self.action_clicked)


        class_well = self.classifierMenu.addAction('&классификатор')
        list_without_jamming = self.classifierMenu.addAction('&Перечень без глушения')



    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        if action == self.create_KRS:
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
        "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                work_plan= 'krs'
                sheet = open_pz.CreatePZ.open_excel_file(self, self.fname[0], work_plan)
                self.copy_pz(sheet)

            except FileNotFoundError:
                print('Файл не найден')

        if action == self.create_GNKT_OPZ:
            print('кнопка нажата')
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                work_plan = 'gnkt_opz'
                sheet = open_pz.CreatePZ.open_excel_file(self, self.fname[0], work_plan)
                self.copy_pz(sheet)
                # # for c in sheet.iter_cols():
                #     print(sheet.column_dimensions[get_column_letter(c)].width)
                # columnWidths = [sheet.column_dimensions[get_column_letter(c + 1)].width for c in sheet.iter_cols()]
                #
                #
                # self.copyColumnWidths(self.table_widget, columnWidths)

            except FileNotFoundError:
                print('Файл не найден')

            if action == self.save_file:
                open_pz.open_excel_file().wb.save("test_unmerge.xlsx")

    # def copyColumnWidths(tableWidget, columnWidths):
    #     for column in range(tableWidget.columnCount()):
    #         tableWidget.setColumnWidth(column, columnWidths[column])

    # def open_dialog(self):
    #     current_text = self.line_edit.text()
    #     title = 'Введите новое значение'
    #     label = 'Текущее значение: {}'.format(current_text)
    #     ok_button = 'OK'
    #     cancel_button = 'Cancel'
    #
    #     reply = QtWidgets.QInputDialog.getText(self, title, label, 'New Value')
    #     if reply:
    #         self.line_edit.setText(reply)
    def copy_pz(self, sheet):
        rows = sheet.max_row
        merged_cells = sheet.merged_cells
        cols = 13
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                if sheet.cell(row=row, column=col).value != None:
                    cell_value = str(sheet.cell(row=row, column=col).value)
                    item = QtWidgets.QTableWidgetItem(cell_value)
                    self.table_widget.setItem(row - 1, col - 1, item)
                    # Проверяем, является ли текущая ячейка объединенной
                    for merged_cell in merged_cells:
                        if row in range(merged_cell.min_row, merged_cell.max_row + 1) and \
                                col in range(merged_cell.min_col, merged_cell.max_col + 1):
                            # Устанавливаем количество объединяемых строк и столбцов для текущей ячейки
                            self.table_widget.setSpan(row - 1, col - 1,
                                                      merged_cell.max_row - merged_cell.min_row + 1,
                                                      merged_cell.max_col - merged_cell.min_col + 1)
        self.table_widget.resizeColumnsToContents()


def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()
