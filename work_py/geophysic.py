import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

import main
from main import MyWindow


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.labelType = QLabel("Кровля записи", self)
        self.lineEditType = QLineEdit(self)
        self.lineEditType.setClearButtonEnabled(True)

        self.labelType2 = QLabel("Подошва записи", self)
        self.lineEditType2 = QLineEdit(self)
        self.lineEditType2.setClearButtonEnabled(True)

        self.labelGeores = QLabel("вид исследования", self)
        self.ComboBoxGeophygist = QComboBox(self)
        self.ComboBoxGeophygist.addItems(['Гироскоп', 'АКЦ', 'АКЦ + СГДТ', 'СГДТ', 'ИНГК', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ'])
        self.ComboBoxGeophygist.setProperty("value", 'ГП')


        self.labelDopInformation = QLabel("Доп информация", self)
        self.lineEditDopInformation = QLineEdit(self)
        self.lineEditDopInformation.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.labelGeores, 0, 0)
        grid.addWidget(self.labelType, 0, 1)
        grid.addWidget(self.labelType2, 0, 2)
        grid.addWidget(self.labelDopInformation, 0, 3)

        grid.addWidget(self.ComboBoxGeophygist, 1, 0)
        grid.addWidget(self.lineEditType, 1, 1)
        grid.addWidget(self.lineEditType2, 1, 2)
        grid.addWidget(self.lineEditDopInformation, 1, 3)




class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Перфорация')

class GeophysicWindow(MyWindow):


    def __init__(self, table_widget, ins_ind, parent=None):
        from open_pz import CreatePZ
        super(MyWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind

        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 4)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Геофизические исследования", "Кровля записи", "Подошва записи", "доп информация"])
        for i in range(4):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.delRowTable)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)



        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)

    def geophysicalSelect(self, geophysic, editType, editType2):

        if geophysic == 'АКЦ':
            research = f'ЗАДАЧА 2.7.1 Определение состояния цементного камня (АКЦ, АК-сканирование) в интервале {editType}-{editType2}м. '
        elif geophysic == 'СГДТ':
            research = f'ЗАДАЧА 2.7.2 Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале {editType}-{editType2}м.'
        elif geophysic == 'АКЦ + СГДТ':
            research = f'ЗАДАЧА 2.7.3  Определение состояния цементного камня (АКЦ, АК-сканирование). в интервале {editType}-{editType2}м,' \
                       f'Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале 0 - 20м выше интервала перфорации '

            ['АКЦ', 'АКЦ + СГДТ', 'СГДТ', 'ИНГК', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ']
        elif geophysic == 'ИНГК':
            research = f'ЗАДАЧА 2.4.3 Определение текущей нефтенасыщенности по данным интегрального импульсного нейтронного' \
                       f'каротажа пласта  в интервале {editType}-{editType2}м. '
        elif geophysic == 'Гироскоп':
            research = f'ЗАДАЧА 2.7.4. Определение траектории ствола скважины гироскопическим инклинометром в интервале {editType}-{editType2}м. '
        elif geophysic == 'РК':
            research = f'ЗАДАЧА 2.4.1 РК в интервале {editType}-{editType2}м. '
        elif geophysic == 'ЭМДС':
            research = f' ЗАДАЧА 2.6.11.  Определение интервалов дефектов и толщины колонн и НКТ с ' \
                       f'использованием электромагнитной дефектоскопии  и толщинометрии  в интервале в интервале {editType}-{editType2}м.'
        elif geophysic == 'ПТС':
            research = f'ЗАДАЧА 2.6.10 Профилимер в интервале {editType}-{editType2}м.'
        elif geophysic == 'ГК и ЛМ':
            research = f'Произвести записи ГК и ЛМ интервале {editType}-{editType2}м. '
        return research


    def addRowTable(self):

        editType = self.tabWidget.currentWidget().lineEditType.text()
        editType2 = self.tabWidget.currentWidget().lineEditType2.text()
        researchGis= self.geophysicalSelect(str(self.tabWidget.currentWidget().ComboBoxGeophygist.currentText()), editType, editType2)


        dopInformation = self.tabWidget.currentWidget().lineEditDopInformation.text()
        if not editType or not editType2 or not researchGis:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return






        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(researchGis))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(editType2))


        self.tableWidget.setItem(rows, 3, QTableWidgetItem(dopInformation))
        self.tableWidget.setSortingEnabled(True)


    def addWork(self):
        from main import MyWindow
        from open_pz import CreatePZ
        rows = self.tableWidget.rowCount()

        geophysicalResearch = [
            [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                         f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером от  14.10.2021г',
             None, None, None, None, None, None, None,
             'Мастер КРС', None, None, None],
            [None, None,
             f'Долить скважину до устья тех жидкостью уд.весом {CreatePZ.fluid_work} .Установить ПВО по схеме №8а утвержденной '
             f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  ПВО (на давление опрессовки ЭК, но '
             f'не ниже максимального ожидаемого давления на устье) {CreatePZ.max_admissible_pressure}атм, по невозможности на давление поглощения, но '
             f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2]
        ]

        for row in range(rows):
            researchGis_list = [None, None]
            for col in range(0, 9):
                item = self.tableWidget.item(row, col)
                if item:
                    if col == 0:
                        value = item.text()
                        researchGis_list.append(value)



            researchGis_list.extend([None, None, None, None, None, None, None, 'подр по ГИС', 4])
            geophysicalResearch.append(researchGis_list)
            print(geophysicalResearch)









        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700)}
        # print(researchGis_list)
        for i, row_data in enumerate(geophysicalResearch):
            row = self.ins_ind + i
            self.table_widget.insertRow(row)
            # lst = [1, 0, 2, len(geophysicalResearch)-1]
            # if float(CreatePZ.max_angle) >= 50:
            #     lst.extend([3, 4])
             # Объединение ячеек по горизонтали в столбце "отвественные и норма"
            self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):

                widget = QtWidgets.QLabel(str())
                if column != 25:
                    widget.setStyleSheet("""QLabel { 
                                                        border: 1px solid black;
                                                        font-size: 12px; 
                                                        font-family: Arial;
                                                    }
                                                    """)
                    self.table_widget.setCellWidget(row, column, widget)
                self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

                if column == 2 or column == 10:
                    if data != None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))
        # self.table_widget.setSpan(1 + self.ins_ind, 10, len(geophysicalResearch) - 2, 1)
        # self.table_widget.setSpan(1 + self.ins_ind, 11, len(geophysicalResearch) - 2, 1)



        self.table_widget.setRowHeight(self.ins_ind, 60)
        self.table_widget.setRowHeight(self.ins_ind + 1, 60)


        self.close()



    def delRowTable(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet()
    window =  GeophysicWindow()
    window.show()
    sys.exit(app.exec_())