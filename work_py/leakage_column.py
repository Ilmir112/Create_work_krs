from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator

import well_data
from main import MyMainWindow


class TabPage_SO_leakage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.validator = QDoubleValidator(0, 8000, 1)

        self.roof_leakage_label = QLabel("Кровля", self)
        self.roof_leakage_line = QLineEdit(self)
        self.roof_leakage_line.setClearButtonEnabled(True)
        self.roof_leakage_line.setValidator(self.validator)

        self.sole_leakage_label = QLabel("Подошва", self)
        self.sole_leakage_line = QLineEdit(self)
        self.sole_leakage_line.setClearButtonEnabled(True)
        self.sole_leakage_line.setValidator(self.validator)

        self.insulation_label = QLabel("Изоляция", self)
        self.insulation_combo = QComboBox(self)
        self.insulation_combo.addItems(
            ['не изолирован', 'изолирован'])

        grid = QGridLayout(self)
        grid.addWidget(self.roof_leakage_label, 0, 0)
        grid.addWidget(self.sole_leakage_label, 0, 1)
        grid.addWidget(self.insulation_label, 0, 2)

        grid.addWidget(self.roof_leakage_line, 1, 0)
        grid.addWidget(self.sole_leakage_line, 1, 1)
        grid.addWidget(self.insulation_combo, 1, 2)





class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_leakage(self), 'Негерметичность')

class LeakageWindow(MyMainWindow):

    def __init__(self, parent=None):

        super(LeakageWindow, self).__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "изоляция"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddString = QPushButton('Добавить строкой')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

        if len(well_data.dict_leakiness) != 0:

            ffa = well_data.dict_leakiness['НЭК']
            for nek in well_data.dict_leakiness['НЭК']['интервал']:
                rows = self.tableWidget.rowCount()

                roof_leakage, sole_leakage_line = nek.split('-')
                self.tableWidget.insertRow(rows)
                insulation_combo1 = QComboBox(self)
                insulation_combo1.addItems(['не изолирован', 'изолирован'])
                if well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение']:
                    insulation_combo1.setCurrentIndex(1)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_leakage))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_leakage_line))
                self.tableWidget.setCellWidget(rows, 2, insulation_combo1)

                self.tableWidget.sortItems(0)


    def add_row_table(self):

        roof_leakage = self.tabWidget.currentWidget().roof_leakage_line.text().replace(',', '.')
        sole_leakage_line = self.tabWidget.currentWidget().sole_leakage_line.text().replace(',', '.')
        insulation_combo1 = QComboBox(self)
        insulation_combo1.addItems(['не изолирован', 'изолирован'])
        index_insulation = self.tabWidget.currentWidget().insulation_combo.currentIndex()
        # print(index_insulation)
        insulation_combo1.setCurrentIndex(index_insulation)
        if float(roof_leakage) > float(sole_leakage_line):
            QMessageBox.information(self, 'Внимание', 'Кровля больше подошвы')
            return
        if not roof_leakage or not sole_leakage_line:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        # ada = float(well_data.bottomhole_artificial._value)
        # if float(well_data.bottomhole_artificial._value) <= float(sole_leakage_line):
        #     QMessageBox.information(self, 'Внимание', 'глубина НЭК ниже искусственного забоя')
        #     return

        rows = 0
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_leakage))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_leakage_line))
        self.tableWidget.setCellWidget(rows, 2, insulation_combo1)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.sortItems(0)

    def addString(self):
       
        try:
            leakiness_column, ok = QInputDialog.getText(self, 'Нарушение колонны',
                                                        'Введите нарушение колонны через тире')

            dict_leakiness = self.get_leakiness(leakiness_column)


            return dict_leakiness
        except:
            QMessageBox.warning(self, 'Ошибка', 'Данные введены не корректно')
            LeakageWindow.addString(self)


    def get_leakiness(self, leakiness_column):

        leakiness_column.replace('м', '').strip()
        # print(leakiness_column)
        rows = 0
        for leakiness in leakiness_column.replace('м', '').replace(' ', '').split(','):


            roof_leakage = str(min(map(float, leakiness.split('-'))))
            sole_leakage = str(max(map(float, leakiness.split('-'))))
            insulation_combo = QComboBox(self)
            insulation_combo.addItems(['не изолирован', 'изолирован'])
            if roof_leakage != sole_leakage:
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_leakage))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_leakage))
                self.tableWidget.setCellWidget(rows, 2, insulation_combo)
            self.tableWidget.setSortingEnabled(False)
            self.tableWidget.sortItems(0)


    def add_work(self):
       
        rows = self.tableWidget.rowCount()
        dict_leakiness = {}
        for row in range(rows):
            roof_leakage = self.tableWidget.item(row, 0)
            sole_leakage = self.tableWidget.item(row, 1)
            insulation_leakage = self.tableWidget.cellWidget(row, 2)
            if roof_leakage and sole_leakage:
                roof = round(float(roof_leakage.text()), 1)
                sole = round(float(sole_leakage.text()), 1)
                insulation = insulation_leakage.currentText()

                dict_leakiness.setdefault(
                    'НЭК', {}).setdefault('интервал', {}).setdefault((f"{roof}-{sole}"), {}).setdefault('отключение', False)
                if insulation == 'изолирован':
                   dict_leakiness['НЭК']['интервал'][f"{roof}-{sole}"]['отключение'] = True
                dict_leakiness.setdefault(
                    'НЭК', {}).setdefault('интервал', {}).setdefault((f"{roof}-{sole}"), {}).setdefault(
                    'Прошаблонировано', False)
                dict_leakiness.setdefault(
                    'НЭК', {}).setdefault('интервал', {}).setdefault((f"{roof}-{sole}"), {}).setdefault(
                    'отрайбировано', False)
        # well_data.dict_leakiness = dict_leakiness
        # print(dict_leakiness)

        well_data.pause = False
        self.close()
        return dict_leakiness

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = LeakageWindow()
    window.show()
    sys.exit(app.exec_())
