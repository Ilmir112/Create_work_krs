import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

import main
from main import MyWindow


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labelTypeCharges = QLabel("вид исследования", self)
        self.ComboBoxCharges = QComboBox(self)
        self.ComboBoxCharges.addItems(['Гироскоп', 'АКЦ', 'АКЦ + СГДТ', 'СГДТ', 'ИНГК', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ'])
        self.ComboBoxCharges.setProperty("value", 'ГП')

        self.labelType = QLabel("Кровля записи", self)
        self.lineEditType = QLineEdit(self)
        self.lineEditType.setClearButtonEnabled(True)

        self.labelType2 = QLabel("Подошва записи", self)
        self.lineEditType2 = QLineEdit(self)
        self.lineEditType2.setClearButtonEnabled(True)


        self.labelDopInformation = QLabel("Доп информация", self)
        self.lineEditDopInformation = QLineEdit(self)
        self.lineEditDopInformation.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.labelTypeCharges, 0, 0)
        grid.addWidget(self.labelType, 0, 1)
        grid.addWidget(self.labelType2, 0, 2)
        grid.addWidget(self.labelDopInformation, 0, 3)

        grid.addWidget(self.ComboBoxCharges, 1, 0)
        grid.addWidget(self.lineEditType, 1, 1)
        grid.addWidget(self.lineEditType2, 1, 2)
        grid.addWidget(self.lineEditDopInformation, 1, 3)

        # grid.setRowStretch(4, 1)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Геофизические исследования')


class GeophysicWindow(MyWindow):

    def __init__(self, table_widget, ins_ind, parent=None):
        from open_pz import CreatePZ
        super(MyWindow, self).__init__(parent)
        self.current_bottom = CreatePZ.current_bottom
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind

        self.tabWidgetgis = TabWidget()
        self.tabWidgetgis = QTableWidget(0, 7)
        self.tabWidgetgis.setHorizontalHeaderLabels(
            ["Геофизические исследования", "Кровля записи", "Подошва записи", "доп информация"])
        for i in range(4):
            self.tabWidgetgis.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tabWidgetgis.setSortingEnabled(True)
        self.tabWidgetgis.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить исследования в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблицы')
        self.buttonDel.clicked.connect(self.delRowTable)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidgetgis, 0, 0, 1, 2)
        vbox.addWidget(self.tabWidgetgis, 1, 0, 1, 2)
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
        editType = self.tabWidgetgis.currentWidget().lineEditType.text()
        editType2 = self.tabWidgetgis.currentWidget().lineEditType2.text()
        researchGis = self.geophysicalSelect(self, str(self.tabWidgetgis.currentWidget().ComboBoxCharges.currentText()))

        dopInformation = self.tabWidgetgis.currentWidget().lineEditDopInformation.text()
        if not editType or not researchGis:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return

        self.tabWidgetgis.setSortingEnabled(False)
        rows = self.tabWidgetgis.rowCount()
        self.tabWidgetgis.insertRow(rows)
        self.tabWidgetgis.setItem(rows, 0, QTableWidgetItem(researchGis))
        self.tabWidgetgis.setItem(rows, 1, QTableWidgetItem(editType))
        self.tabWidgetgis.setItem(rows, 2, QTableWidgetItem(editType2))

        self.tabWidgetgis.setItem(rows, 3, QTableWidgetItem(dopInformation))
        self.tabWidgetgis.setSortingEnabled(True)
        # print(editType, spinYearOfIssue, editSerialNumber, editSpecifications)

    def addWork(self):
        from main import MyWindow
        from open_pz import CreatePZ
        rows = self.tabWidgetgis.rowCount()

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
             f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). '
             f'Передать по сводке уровня жидкости до перфорации и после перфорации.'
             f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации,'
             f' фотографии предоставить в ЦИТС Ойл-сервис',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 15, None, None]
            ]

        for row in range(rows):
            perf_list = [None, None]
            for col in range(0, 9):
                item = self.tabWidgetgis.item(row, col)
                if item:
                    value = item.text()
            perf_list.extend([None, None])
            geophysicalResearch.append(perf_list)

        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700)}
        # print(perf_list)
        for i, row_data in enumerate(geophysicalResearch):
            row = self.ins_ind + i
            self.table_widget.insertRow(row)
            lst = [1, 0, 2, len(geophysicalResearch) - 1]
            if float(CreatePZ.max_angle) >= 50:
                lst.extend([3, 4])
            if i in lst:  # Объединение ячеек по вертикале в столбце "отвественные и норма"
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
        self.table_widget.setSpan(1 + self.ins_ind, 10, len(geophysicalResearch) - 2, 1)
        self.table_widget.setSpan(1 + self.ins_ind, 11, len(geophysicalResearch) - 2, 1)

        self.table_widget.setRowHeight(self.ins_ind, 60)
        self.table_widget.setRowHeight(self.ins_ind + 1, 60)

        self.close()

    def delRowTable(self):
        row = self.tabWidgetgis.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tabWidgetgis.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet()
    window = GeophysicWindow()
    window.show()
    sys.exit(app.exec_())
