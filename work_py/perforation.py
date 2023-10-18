import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from main import MyWindow


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.labelType = QLabel("Кровля  перфорации", self)
        self.lineEditType = QLineEdit(self)
        self.lineEditType.setClearButtonEnabled(True)

        self.labelType2 = QLabel("Подошва  перфорации", self)
        self.lineEditType2 = QLineEdit(self)
        self.lineEditType2.setClearButtonEnabled(True)

        self.labelTypeCharges = QLabel("Тип зарядов", self)
        self.ComboBoxCharges = QComboBox(self)
        self.ComboBoxCharges.addItems(['ГП', 'БО'])
        # self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        # self.spinBox.setMinimum(1917)
        # self.spinBox.setMaximum(2060)
        self.ComboBoxCharges.setProperty("value", 'ГП')

        self.labelHolesMetr = QLabel("отверстий на 1п.м", self)
        self.lineEditHolesMetr = QLineEdit(self)
        self.lineEditHolesMetr.setClearButtonEnabled(True)

        # self.labelCountHoles = QLabel("Количество отверстий", self)
        # self.lineEditCountHoles = QLineEdit(self)
        # self.lineEditCountHoles.setClearButtonEnabled(True)

        self.labelIndexFormation = QLabel("Индекс пласта", self)
        self.lineEditIndexFormation = QLineEdit(self)
        self.lineEditIndexFormation.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.labelType, 0, 0)
        grid.addWidget(self.labelType2, 0, 1)
        grid.addWidget(self.labelTypeCharges, 0, 2)
        grid.addWidget(self.labelHolesMetr, 0, 3)

        grid.addWidget(self.labelIndexFormation, 0, 4)
        grid.addWidget(self.lineEditType, 1, 0)
        grid.addWidget(self.lineEditType2, 1, 1)
        grid.addWidget(self.ComboBoxCharges, 1, 2)
        grid.addWidget(self.lineEditHolesMetr, 1, 3)
        grid.addWidget(self.lineEditIndexFormation, 1, 4)



        # grid.setRowStretch(4, 1)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Перфорация')

class PervorationWindow(MyWindow):
    # from open_pz import CreatePZ
    perforation_list = []
    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.", "Количество отверстий", "Вскрываемые пласты"])
        for i in range(6):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить интервалы перфорации в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить интервалы перфорации в таблице')
        self.buttonDel.clicked.connect(self.delRowTable)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)

    def addRowTable(self):
        editType = self.tabWidget.currentWidget().lineEditType.text()
        editType2 = self.tabWidget.currentWidget().lineEditType2.text()
        chargesx= str(self.tabWidget.currentWidget().ComboBoxCharges.currentText())
        editHolesMetr = self.tabWidget.currentWidget().lineEditHolesMetr.text()
        editIndexFormation = self.tabWidget.currentWidget().lineEditIndexFormation.text()
        if not editType or not editType2 or not chargesx or not editHolesMetr or not editIndexFormation:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(editType))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType2))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(chargesx))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(editHolesMetr))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(int((float(editType2)-float(editType))*float(editHolesMetr)))))
        self.tableWidget.setItem(rows, 5, QTableWidgetItem(editIndexFormation))
        self.tableWidget.setSortingEnabled(True)
        # print(editType, spinYearOfIssue, editSerialNumber, editSpecifications)

    def addWork(self):
        from main import MyWindow
        from open_pz import CreatePZ
        rows = self.tableWidget.rowCount()

        interval = [["Кровля перфорации", "-", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.", "Количество отверстий",
                      "Вскрываемые пласты"]]

        perforation = [[None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                                     f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                                     f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером от  14.10.2021г',
                         None, None, None, None, None, None, None,
                          'Мастер КРС', None, None],
                       [None, None, f'Долить скважину до устья тех жидкостью уд.весом 1,26г/см3 ОШИБКА .Установить ПВО по схеме №8а утвержденной '
                                     f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  ПВО (на давление опрессовки ЭК, но '
                                     f'не ниже максимального ожидаемого давления на устье) 80атм, по невозможности на давление поглощения, но '
                                     f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                         None, None, None, None, None, None, None,
                          'Мастер КРС, подрядчик по ГИС', 15, None]]


        for row in range(rows):
            perf_list = [None, None]
            for col in range(0, 6):
                item = self.tableWidget.item(row, col)

                if item:
                    value = item.text()
                    if col == 1:
                        perf_list.append("-")
                    else:
                        perf_list.append(value)

            perf_list.insert(5, None)
            perf_list.append(None)
            perf_list.append(None)
            perforation.append(perf_list)

        perforation.append([None, None, 'Произвести контрольную запись ЛМ;ТМ. Составить АКТ на перфорацию.',
                         None, None, None, None, None, None, None,
                          'Подрядчик по ГИС', None, None])
        print(CreatePZ.ins_ind)

        MyWindow.perforation_list = perforation

        self.close()
        acid_true_quest = QMessageBox.question(self, 'вставить данные?')
        if acid_true_quest == QMessageBox.StandardButton.Yes:
            acid_true_quest = True
        else:
            acid_true_quest = False
    def delRowTable(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)



qss = """
QLabel {
    font: 8pt "MS Shell Dlg 2";
}
QLineEdit {
    font: 12pt "Arial";
}
QSpinBox {
    font: 12pt "Arial";
}
"""

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qss)
    window = PervorationWindow()
    window.show()
    sys.exit(app.exec_())