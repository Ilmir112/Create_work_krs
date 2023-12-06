from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from main import MyWindow
from open_pz import CreatePZ


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.swabTrueEditType.setCurrentIndex(1)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.khovstEdit = QLineEdit(self)
        self.khovstEdit.setClearButtonEnabled(True)

        self.pakerLabel = QLabel("глубина пакера", self)
        self.pakerEdit = QLineEdit(self)
        self.pakerEdit.setText(f"{self.ifNone(CreatePZ.perforation_roof-10)}")
        self.pakerEdit.setClearButtonEnabled(True)

        self.plastLabel = QLabel("Выбор пласта", self)
        self.plastCombo = QComboBox(self)
        self.plastCombo.addItems(CreatePZ.plast_work)
        self.plastCombo.setCurrentIndex(0)
        # self.ComboBoxGeophygist.setProperty("value", 'ГП')

        self.privyazkaTrueLabelType = QLabel("необходимость освоения", self)
        self.privyazkaTrueEdit = QComboBox(self)
        self.privyazkaTrueEdit.addItems(['Нужна привязка', 'без привязки'])
        self.privyazkaTrueEdit.setCurrentIndex(1)

        self.skvTrueLabelType = QLabel("необходимость кислотной ванны", self)
        self.svkTrueEdit = QComboBox(self)
        self.svkTrueEdit.addItems(['Нужно СКВ', 'без СКВ'])
        self.svkTrueEdit.setCurrentIndex(1)

        self.skvAcidLabelType = QLabel("Вид кислоты для СКВ", self)
        self.skvAcidEdit = QComboBox(self)
        self.skvAcidEdit.addItems(['HCl', 'HF'])
        self.skvAcidEdit.setCurrentIndex(0)

        self.skvVolumeLabel = QLabel("Объем СКВ", self)
        self.skvVolumeEdit = QLineEdit(self)
        self.skvVolumeEdit.setText('1')
        self.skvVolumeEdit.setClearButtonEnabled(True)

        self.QplastLabelType = QLabel("Нужно ли определять приемистоть до СКО", self)
        self.QplastEdit = QComboBox(self)
        self.QplastEdit.addItems(['ДА', 'НЕТ'])
        self.QplastEdit.setCurrentIndex(1)

        self.skvProcLabel = QLabel("Концентрация СКВ", self)
        self.skvProcEdit = QLineEdit(self)
        self.skvProcEdit.setClearButtonEnabled(True)
        self.skvProcEdit.setText('15')

        self.acidLabelType = QLabel("Вид кислотной обработки", self)
        self.acidEdit = QComboBox(self)
        self.acidEdit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acidEdit.setCurrentIndex(0)

        self.acidVolumeLabel = QLabel("Объем кислотной обработки", self)
        self.acidVolumeEdit = QLineEdit(self)
        self.acidVolumeEdit.setText("10")
        self.acidVolumeEdit.setClearButtonEnabled(True)

        self.acidProcLabel = QLabel("Концентрация кислоты", self)
        self.acidProcEdit = QLineEdit(self)
        self.acidProcEdit.setText('15')
        self.acidProcEdit.setClearButtonEnabled(True)

        self.acidOilProcLabel = QLabel("объем нефти", self)
        self.acidOilProcLabel.setText('5')
        self.acidOilProcEdit = QLineEdit(self)
        self.acidOilProcEdit.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.swabTruelabelType, 0, 0)
        grid.addWidget(self.swabTrueEditType, 1, 0)
        grid.addWidget(self.plastLabel, 0, 1)
        grid.addWidget(self.plastCombo, 1, 1)
        grid.addWidget(self.pakerLabel, 0, 2)
        grid.addWidget(self.pakerEdit, 1, 2)
        grid.addWidget(self.khovstLabel, 0, 3)
        grid.addWidget(self.khovstEdit, 1, 3)
        grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        grid.addWidget(self.privyazkaTrueEdit, 1, 4)

        grid.addWidget(self.skvTrueLabelType, 2, 0)
        grid.addWidget(self.svkTrueEdit, 3, 0)
        grid.addWidget(self.skvAcidLabelType, 2, 1)
        grid.addWidget(self.skvAcidEdit, 3, 1)
        grid.addWidget(self.skvVolumeLabel, 2, 2)
        grid.addWidget(self.skvVolumeEdit, 3, 2)
        grid.addWidget(self.skvProcLabel, 2, 3)
        grid.addWidget(self.skvProcEdit, 3, 3)

        grid.addWidget(self.acidLabelType, 4, 1)
        grid.addWidget(self.acidEdit, 5, 1)
        grid.addWidget(self.acidVolumeLabel, 4, 2)
        grid.addWidget(self.acidVolumeEdit, 5, 2)
        grid.addWidget(self.acidProcLabel, 4, 3)
        grid.addWidget(self.acidProcEdit, 5, 3)
        grid.addWidget(self.acidOilProcLabel, 4, 4)
        grid.addWidget(self.acidOilProcEdit, 5, 4)





class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Кислотная обработка на одном пакере')


class AcidPakerWindow(MyWindow):

    def __init__(self, table_widget, ins_ind, parent=None):

        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 2)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Ход работ", "ответственные", "нормы"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить данные в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить строку из таблице')
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
        pass
        # if geophysic == 'АКЦ':
    #         research = f'ЗАДАЧА 2.7.1 Определение состояния цементного камня (АКЦ, АК-сканирование) в интервале {editType}-{editType2}м. '
    #     elif geophysic == 'СГДТ':
    #         research = f'ЗАДАЧА 2.7.2 Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале {editType}-{editType2}м.'
    #     elif geophysic == 'АКЦ + СГДТ':
    #         research = f'ЗАДАЧА 2.7.3  Определение состояния цементного камня (АКЦ, АК-сканирование). в интервале {editType}-{editType2}м,' \
    #                    f'Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в интервале 0 - 20м выше интервала перфорации '
    #
    #
    #     elif geophysic == 'ИНГК':
    #         research = f'ЗАДАЧА 2.4.3 Определение текущей нефтенасыщенности по данным интегрального импульсного нейтронного' \
    #                    f'каротажа пласта  в интервале {editType}-{editType2}м. '
    #     elif geophysic == 'Гироскоп':
    #         research = f'ЗАДАЧА 2.7.4. Определение траектории ствола скважины гироскопическим инклинометром в интервале {editType}-{editType2}м. '
    #     elif geophysic == 'РК':
    #         research = f'ЗАДАЧА 2.4.1 РК в интервале {editType}-{editType2}м. '
    #     elif geophysic == 'ЭМДС':
    #         research = f' ЗАДАЧА 2.6.11.  Определение интервалов дефектов и толщины колонн и НКТ с ' \
    #                    f'использованием электромагнитной дефектоскопии  и толщинометрии  в интервале в интервале {editType}-{editType2}м.'
    #     elif geophysic == 'ПТС':
    #         research = f'ЗАДАЧА 2.6.10 Профилимер в интервале {editType}-{editType2}м.'
    #     elif geophysic == 'ГК и ЛМ':
    #         research = f'Произвести записи ГК и ЛМ интервале {editType}-{editType2}м. '
    #     return research
    #
    def addRowTable(self):
        pass
        # editType = self.tabWidget.currentWidget().lineEditType.text()
        # editType2 = self.tabWidget.currentWidget().lineEditType2.text()
        # researchGis = self.geophysicalSelect(str(self.tabWidget.currentWidget().ComboBoxGeophygist.currentText()),
        #                                      editType, editType2)
        # dopInformation = self.tabWidget.currentWidget().lineEditDopInformation.text()
        # if not editType or not editType2 or not researchGis:
        #     msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
        #     return
        #
        # self.tableWidget.setSortingEnabled(False)
        # rows = self.tableWidget.rowCount()
        # self.tableWidget.insertRow(rows)
        #
        # self.tableWidget.setItem(rows, 0, QTableWidgetItem(researchGis))
        # self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType))
        # self.tableWidget.setItem(rows, 2, QTableWidgetItem(editType2))
        # self.tableWidget.setItem(rows, 3, QTableWidgetItem(dopInformation))
        # self.tableWidget.setSortingEnabled(True)

    def addWork(self):
        pass
        from open_pz import CreatePZ

        # rows = self.tableWidget.rowCount()
        # geophysicalResearch = [
        #     [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
        #                  f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
        #                  f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером от  14.10.2021г',
        #      None, None, None, None, None, None, None,
        #      'Мастер КРС', None, None, None],
        #     [None, None,
        #      f'Долить скважину до устья тех жидкостью уд.весом {CreatePZ.fluid_work} .Установить ПВО по схеме №8а утвержденной '
        #      f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  ПВО (на давление опрессовки ЭК, но '
        #      f'не ниже максимального ожидаемого давления на устье) {CreatePZ.max_expected_pressure}атм, по невозможности на давление поглощения, но '
        #      f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). ',
        #      None, None, None, None, None, None, None,
        #      'Мастер КРС, подрядчик по ГИС', 1.2]
        # ]
        #
        # for row in range(rows):
        #     researchGis_list = [None, None]
        #     for col in range(0, 9):
        #         item = self.tableWidget.item(row, col)
        #         if item:
        #             if col == 0:
        #                 value = item.text()
        #                 researchGis_list.append(value)
        #
        #     researchGis_list.extend([None, None, None, None, None, None, None, 'подр по ГИС', 4])
        #     geophysicalResearch.append(researchGis_list)
        #
        # ori = QMessageBox.question(self, 'ОРИ', 'Нужна ли интерпретация?')
        # if ori == QMessageBox.StandardButton.Yes:
        #     geophysicalResearch.append([None, None,
        #                                 f'Интерпретация данных ГИС, согласовать с ПТО и Ведущим инженером ЦДНГ опрессовку фНКТ ',
        #                                 None, None, None, None, None, None, None,
        #                                 'Мастер КРС, подрядчик по ГИС', 8])
        # else:
        #     pass

        # text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
        #                    120: (501, 600), 140: (601, 700)}
        # # print(researchGis_list)
        # for i, row_data in enumerate(geophysicalResearch):
        #     row = self.ins_ind + i
        #     self.table_widget.insertRow(row)
        #     # lst = [1, 0, 2, len(geophysicalResearch)-1]
        #     # if float(CreatePZ.max_angle) >= 50:
        #     #     lst.extend([3, 4])
        #     # Объединение ячеек по горизонтали в столбце "отвественные и норма"
        #     self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
        #     for column, data in enumerate(row_data):
        #
        #         self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
        #
        #         if column == 2 or column == 10:
        #             if not data is None:
        #                 text = data
        #                 for key, value in text_width_dict.items():
        #                     if value[0] <= len(text) <= value[1]:
        #                         text_width = key
        #                         self.table_widget.setRowHeight(row, int(text_width))
        #             else:
        #                 self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))
        #
        # self.table_widget.setRowHeight(self.ins_ind, 60)
        # self.table_widget.setRowHeight(self.ins_ind + 1, 60)
        #
        # self.close()

    def delRowTable(self):
        pass
    #     row = self.tableWidget.currentRow()
    #     if row == -1:
    #         msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
    #         return
    #     self.tableWidget.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = AcidPakerWindow()
    window.show()
    sys.exit(app.exec_())