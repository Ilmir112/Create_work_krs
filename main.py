import openpyxl
import sys
import open_pz
# import plan.py
from PyQt5.QtWidgets import QTextEdit
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QMenuBar, QFileDialog

class MyWindow(QMainWindow):


    def __init__(self, parent = None):
        super(MyWindow, self).__init__(parent)
        self.setWindowTitle('Создание')
        self.setGeometry(300, 250, 350, 200)
        self.table_widget = QtWidgets.QTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.createMenuBar()
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
            #self.fname ='6147.xlsx'


            try:

                sheet = open_pz.open_excel_file(self, self.fname[0])
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
                                    self.table_widget.setSpan(row - 1, col - 1, merged_cell.max_row - merged_cell.min_row + 1,
                                                       merged_cell.max_col - merged_cell.min_col + 1)
                # self.table_widget.setHorizontalHeaderLabels(
                #     [str(sheet.cell(row=1, column=col).value) for col in range(1, cols + 1)])
                # self.table_widget.setVerticalHeaderLabels(
                #     [str(sheet.cell(row=row, column=1).value) for row in range(1, rows + 1)])
                self.table_widget.resizeColumnsToContents()

            except FileNotFoundError:
                print('Файл не найден')

            if action == self.save_file:
                open_pz.open_excel_file().wb.save("test_unmerge.xlsx")


def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()
