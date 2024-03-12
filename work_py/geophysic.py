from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

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
        self.ComboBoxGeophygist.addItems(
            ['Гироскоп', 'АКЦ', 'АКЦ + СГДТ', 'СГДТ', 'ИНГК', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ'])
        self.ComboBoxGeophygist.currentTextChanged.connect(self.geophygist_data)

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

    def geophygist_data(self):
        from open_pz import CreatePZ
        if self.ComboBoxGeophygist.currentText() in ['Гироскоп', 'АКЦ', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ']:
            self.lineEditType.setText('0')
            self.lineEditType2.setText(f'{CreatePZ.current_bottom}')



class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Перфорация')


class GeophysicWindow(MyWindow):

    def __init__(self, table_widget, ins_ind, parent=None):

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
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)

    def geophysicalSelect(self, geophysic):

        return geophysic

    def addRowTable(self):
        from open_pz import CreatePZ

        editType = self.tabWidget.currentWidget().lineEditType.text().replace(',', '.')
        editType2 = self.tabWidget.currentWidget().lineEditType2.text().replace(',', '.')
        researchGis = self.geophysicalSelect(str(self.tabWidget.currentWidget().ComboBoxGeophygist.currentText()))

        dopInformation = self.tabWidget.currentWidget().lineEditDopInformation.text()
        if not editType or not editType2 or not researchGis:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if CreatePZ.current_bottom < float(editType2):
            msg = QMessageBox.information(self, 'Внимание', 'глубина исследований ниже текущего забоя')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(researchGis))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(editType2))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(dopInformation))
        self.tableWidget.setSortingEnabled(True)
    def geophysic_sel(self, geophysic, editType, editType2):
        from open_pz import CreatePZ
        if geophysic == 'АКЦ':
            research = f'ЗАДАЧА 2.7.1 Определение состояния цементного камня (АКЦ, АК-сканирование) в интервале {editType}-{editType2}м. '
            research_short = f'АКЦ в интервале {editType}-{editType2}м.'
        elif geophysic == 'СГДТ':
            research = f'ЗАДАЧА 2.7.2 Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале {editType}-{editType2}м.'
            research_short = f'СГДТ в интервале {editType}-{editType2}м.'
        elif geophysic == 'АКЦ + СГДТ':
            research = f'ЗАДАЧА 2.7.3  Определение состояния цементного камня (АКЦ, АК-сканирование). в интервале {editType}-{editType2}м,' \
                       f'Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале 0 - {CreatePZ.perforation_roof - 20} '
            research_short = f'АКЦ в интервале {editType}-{editType2}м.' \
                             f'СГДТ в интервале 0 - {CreatePZ.perforation_roof - 20}'



        elif geophysic == 'ИНГК':
            research = f'ЗАДАЧА 2.4.3 Определение текущей нефтенасыщенности по данным интегрального импульсного нейтронного' \
                       f'каротажа пласта  в интервале {editType}-{editType2}м. '
            research_short = f'ИНГК в интервале {editType}-{editType2}м.'

        elif geophysic == 'Гироскоп':
            research = f'ЗАДАЧА 2.7.4. Определение траектории ствола скважины гироскопическим инклинометром ' \
                       f'в интервале {editType}-{editType2}м. '
            research_short = f'Гироскоп в интервале {editType}-{editType2}м.'
        elif geophysic == 'РК':
            research = f'ЗАДАЧА 2.4.1 РК в интервале {editType}-{editType2}м. '
            research_short = f'РК в интервале {editType}-{editType2}м.'
        elif geophysic == 'ЭМДС':
            research = f' ЗАДАЧА 2.6.11. Определение интервалов дефектов и толщины колонн и НКТ с ' \
                       f'использованием электромагнитной дефектоскопии  и толщинометрии в ' \
                       f'интервале {editType}-{editType2}м.'
            research_short = f'ЭМДС в интервале {editType}-{editType2}м.'
        elif geophysic == 'ПТС':
            research = f'ЗАДАЧА 2.6.10 Профилимер в интервале {editType}-{editType2}м.'
            research_short = f'ПТС в интервале {editType}-{editType2}м.'

        elif geophysic == 'ГК и ЛМ':
            research = f'Произвести записи ГК и ЛМ интервале {editType}-{editType2}м. '
            research_short = f'ГК и ЛМ в интервале {editType}-{editType2}м.'

        return research, research_short

    def if_None_gis(self, value):

        if isinstance(value, int) or isinstance(value, float):
            return int(value)

        elif str(value).replace('.','').replace(',','').isdigit():
            if str(round(float(value.replace(',','.')), 1))[-1] == 0:
                return int(float(value.replace(',','.')))
        else:
            return 0
    def addWork(self):

        from open_pz import CreatePZ

        rows = self.tableWidget.rowCount()
        geophysicalResearch = [
            [" ", None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                         f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером оТ 14.10.2021г',
             None, None, None, None, None, None, None,
             'Мастер КРС', ' '],
            [' ', None,
             f'Долить скважину до устья тех жидкостью уд.весом {CreatePZ.fluid_work} .Установить ПВО по схеме №8а утвержденной '
             f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  ПВО (на давление опрессовки ЭК, но '
             f'не ниже максимального ожидаемого давления на устье) {CreatePZ.max_expected_pressure._value}атм, по невозможности на давление поглощения, но '
             f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2]
        ]

        for row in range(rows):
            researchGis_list = []

            item = self.tableWidget.item(row, 0)
            edit1 = self.tableWidget.item(row, 1)
            edit2 = self.tableWidget.item(row, 2)
            if item and edit1 and edit2:
                value = item.text()
                edit1_1 = edit1.text()
                edit2_1 = edit2.text()
                geo_sel = self.geophysic_sel(value, edit1_1, edit2_1)
                # print(f'геофои {geo_sel}')
                researchGis_list.extend([geo_sel[1], None, geo_sel[0], None, None, None, None, None, None, None, 'подряд по ГИС', 4])



            geophysicalResearch.append(researchGis_list)
        # print(geophysicalResearch)

        ori = QMessageBox.question(self, 'ОРИ', 'Нужна ли интерпретация?')
        if ori == QMessageBox.StandardButton.Yes:
            geophysicalResearch.append([f'ОРИ', None,
                                        f'Интерпретация данных ГИС, согласовать с ПТО и Ведущим инженером ЦДНГ опрессовку фНКТ ',
                                        None, None, None, None, None, None, None,
                                        'Мастер КРС, подрядчик по ГИС', 8])


        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700)}
        # print(researchGis_list)
        for i, row_data in enumerate(geophysicalResearch):
            row = self.ins_ind + i
            self.table_widget.insertRow(row)
            # lst = [1, 0, 2, len(geophysicalResearch)-1]
            # if float(CreatePZ.max_angle._value) >= 50:
            #     lst.extend([3, 4])
            # Объединение ячеек по горизонтали в столбце "отвественные и норма"
            self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):

                self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

                if column == 0 or column == 2 or column == 10 or column == 11 or column == 12:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(str(text)) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))
                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

        self.table_widget.setRowHeight(self.ins_ind, 60)
        self.table_widget.setRowHeight(self.ins_ind + 1, 60)

        self.close()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet()
    window = GeophysicWindow()
    window.show()
    sys.exit(app.exec_())