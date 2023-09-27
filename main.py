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
        self.save_file_as = self.fileMenu.addAction('Сохранить как', self.action_clicked)



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

        elif action == self.create_GNKT_OPZ:
            print('кнопка нажата')
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                work_plan = 'gnkt_opz'
                sheet = open_pz.CreatePZ.open_excel_file(self, self.fname[0], work_plan)
                self.copy_pz(sheet)


            except FileNotFoundError:
                print('Файл не найден')

            # if action == self.save_file:
            #     open_pz.open_excel_file().wb.save("test_unmerge.xlsx")

        elif action == self.save_file_as:
            self.saveFileDialog()

    def saveFileDialog(self):

        fname, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
        if fname:
            print(fname)

    def copy_pz(self, sheet):
        from open_pz import CreatePZ
        rows = sheet.max_row
        merged_cells = sheet.merged_cells
        cols = 13
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height != None else 18 for i in range(sheet.max_row)]


        for row in range(1, rows + 1):
            if row > 1 and row < rows -1:
                self.table_widget.setRowHeight(row, int(rowHeights_exit[row]))
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
        # self.table_widget.resizeColumnsToContents()



def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()
