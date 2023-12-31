from PyQt5 import QtWidgets
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
        self.lineEditHolesMetr = QComboBox(self)
        self.lineEditHolesMetr.addItems(['6', '8', '10', '16', '18', '20', '30'])
        self.ComboBoxCharges.setProperty("value", '20')
        # self.lineEditHolesMetr.setClearButtonEnabled(True)

        # self.labelCountHoles = QLabel("Количество отверстий", self)
        # self.lineEditCountHoles = QLineEdit(self)
        # self.lineEditCountHoles.setClearButtonEnabled(True)

        self.labelIndexFormation = QLabel("Индекс пласта", self)
        self.lineEditIndexFormation = QLineEdit(self)
        self.lineEditIndexFormation.setClearButtonEnabled(True)

        self.labelDopInformation = QLabel("Доп информация", self)
        self.lineEditDopInformation = QLineEdit(self)
        self.lineEditDopInformation.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.labelType, 0, 0)
        grid.addWidget(self.labelType2, 0, 1)
        grid.addWidget(self.labelTypeCharges, 0, 2)
        grid.addWidget(self.labelHolesMetr, 0, 3)

        grid.addWidget(self.labelIndexFormation, 0, 4)
        grid.addWidget(self.labelDopInformation, 0, 5)
        grid.addWidget(self.lineEditType, 1, 0)
        grid.addWidget(self.lineEditType2, 1, 1)
        grid.addWidget(self.ComboBoxCharges, 1, 2)
        grid.addWidget(self.lineEditHolesMetr, 1, 3)
        grid.addWidget(self.lineEditIndexFormation, 1, 4)
        grid.addWidget(self.lineEditDopInformation, 1, 5)



        # grid.setRowStretch(4, 1)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Перфорация')

class PerforationWindow(MyWindow):


    def __init__(self, table_widget, ins_ind, dict_perforation_project, parent=None):
        from open_pz import CreatePZ
        super(MyWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.dict_perforation = CreatePZ.dict_perforation
        self.dict_perforation_project = CreatePZ.dict_perforation_project
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.", "Количество отверстий", "Вскрываемые пласты", "доп информация"])
        for i in range(7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить интервалы перфорации в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить интервалы перфорации в таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        self.buttonAddProject = QPushButton('Добавить проектные интервалы перфорации')
        self.buttonAddProject.clicked.connect(self.addPerfProject)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)
        vbox.addWidget(self.buttonAddProject, 3, 1)





    def addPerfProject(self):
        from open_pz import CreatePZ

        chargePM = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                                      'кол-во отверстий на 1 п.м.', 20, 5,
                                                     50)[0]

        self.tableWidget.setSortingEnabled(False)
        # print(f' проект {self.dict_perforation_project}')
        # print(f' текущий ПВР {self.dict_perforation}')
        rows = self.tableWidget.rowCount()
        if len(self.dict_perforation_project) != 0:
            for plast, data in self.dict_perforation_project.items():
                for i in data['интервал']:
                    count_charge = int((max(i) - min(i)) * chargePM)

                    self.tableWidget.insertRow(rows)
                    self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                    self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                    self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))))
                    self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM)))
                    self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                    self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                    self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

        else:

            for plast, data in self.dict_perforation.items():
                print(plast)
                if plast in CreatePZ.plast_work:
                    for i in data['интервал']:
                        count_charge = int((max(i)-min(i))*chargePM)
                        # print(i)
                        # print(str(min(i)))
                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))
        self.tableWidget.setSortingEnabled(True)


    def charge(self, pvr):
        from open_pz import CreatePZ
        charge_diam_dict = {73: (0, 110), 89: (111, 135), 102: (136, 160), 114: (160, 250)}

        if CreatePZ.column_additional == False or (
                CreatePZ.column_additional == True and pvr < CreatePZ.head_column_additional):
            diam_internal_ek = CreatePZ.column_diametr
        else:
            diam_internal_ek = CreatePZ.column_additional_diametr

        for diam, diam_internal_paker in charge_diam_dict.items():
            if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                zar = [25 if diam == 73 else 32]
                return f'{diam} ПП{zar}ГП'

    def addRowTable(self):
        from open_pz import CreatePZ

        editType = self.tabWidget.currentWidget().lineEditType.text().replace(',', '.')
        editType2 = self.tabWidget.currentWidget().lineEditType2.text().replace(',', '.')
        chargesx= str(self.tabWidget.currentWidget().ComboBoxCharges.currentText())
        editHolesMetr = self.tabWidget.currentWidget().lineEditHolesMetr.currentText()
        editIndexFormation = self.tabWidget.currentWidget().lineEditIndexFormation.text()
        dopInformation = self.tabWidget.currentWidget().lineEditDopInformation.text()
        if not editType or not editType2 or not chargesx or not editIndexFormation:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if float(editType2.replace(',', '.')) >= float(CreatePZ.current_bottom):
            msg = QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(editType))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType2))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(chargesx))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(editHolesMetr))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(int((float(editType2)-float(editType))*int(editHolesMetr)))))
        self.tableWidget.setItem(rows, 5, QTableWidgetItem(editIndexFormation))
        self.tableWidget.setItem(rows, 6, QTableWidgetItem(dopInformation))
        self.tableWidget.setSortingEnabled(True)
        # print(editType, spinYearOfIssue, editSerialNumber, editSpecifications)

    def addWork(self):

        from open_pz import CreatePZ
        rows = self.tableWidget.rowCount()
        if len(CreatePZ.cat_P_1) > 1:
            kateg2 = [1 if str(CreatePZ.cat_P_1[1]) == '1' or str(CreatePZ.cat_H2S_list[1]) == '1' else 2][0]

            if CreatePZ.kat_pvo <  kateg2:
                CreatePZ.kat_pvo = kateg2

        perforation = [[None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                                     f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                                     f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером от  14.10.2021г',
                         None, None, None, None, None, None, None,
                          'Мастер КРС', None, None,  None],
                       [None, None, f'Долить скважину до устья тех жидкостью уд.весом {CreatePZ.fluid_work} .Установить ПВО по схеме №8а утвержденной '
                                     f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  ПВО (на давление опрессовки ЭК, но '
                                     f'не ниже максимального ожидаемого давления на устье) {CreatePZ.max_expected_pressure}атм, по невозможности на давление поглощения, но '
                                     f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). '
                                    f'Передать по сводке уровня жидкости до перфорации и после перфорации.'
                                    f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации,'
                                    f' фотографии предоставить в ЦИТС Ойл-сервис',
                         None, None, None, None, None, None, None,
                          'Мастер КРС, подрядчик по ГИС', 1.2, None],
                       [None, None, ''.join(["ГИС (Перфорация на кабеле ЗАДАЧА 2.9.1)" if float(CreatePZ.max_angle) <= 50 else "ГИС ( Трубная Перфорация ЗАДАЧА 2.9.2)"]), None, None, None, None,
                        None,None, None, 'подрядчик по ГИС',  None],
                       [None, None, "Кровля", "-", "Подошва", "Тип заряда", "отв на 1 п.м.", "Кол-во отв",
                      "пласт", "Доп.данные", 'подрядчик по ГИС', 2.5]
                       ]
        print(f'до {CreatePZ.plast_work}')
        for row in range(rows):
            item = self.tableWidget.item(row, 1)
            if item:
                value = item.text()
                print(f'dff{value}')
                if float(value) >= CreatePZ.current_bottom:
                    msg = QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
                    return
        for row in range(rows):
            perf_list = [None, None]
            for col in range(0, 9):
                item = self.tableWidget.item(row, col)
                if item:
                    value = item.text()
                    if col == 1:
                        perf_list.append("-")
                        perf_list.append(float(value))
                    elif col == 0:
                        perf_list.append(float(value))
                    elif col == 4:
                        perf_list.append(int(value))
                    else:
                        perf_list.append(value)

            # perf_list.insert(7, (round((float(perf_list[4]) - float(perf_list[2])) * int(perf_list[6]), 1)))
            perf_list.extend(['подрядчик по ГИС', round(perf_list[4]-perf_list[2]) * 1.8, 1])
            # print(perf_list)
            plast = perf_list[8]
            # print(f' раб ПВР {CreatePZ.plast_work, plast}')

            CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add(
                (float(perf_list[2]), float(perf_list[4])))
            CreatePZ.dict_perforation[plast]['отрайбировано'] = False
            CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)



            perforation.append(perf_list)

        perforation.append([None, None, ''.join(["Произвести контрольную запись ЛМ;ТМ. Составить АКТ на "
                                                 "перфорацию." if float(CreatePZ.max_angle) <= 50 else ""
                                               f"Подъем последних 5-ти НКТ{CreatePZ.nkt_diam}мм и демонтаж перфоратора производить в присутствии ответственного "
                                           f"представителя подрядчика по ГИС» (руководителя взрывных работ или взрывника)."]),
                         None, None, None, None, None, None, None,
                          'Подрядчик по ГИС', None, 2])
        print([CreatePZ.dict_perforation[plast] for plast in CreatePZ.plast_work])
        pipe_perforation = [
           [None, None, f'Произвести монтаж трубного перфоратора + 2шт/20м НКТ + реперный патрубок L=2м до намеченного интервала перфорации '
                        f'(с шаблонировкой НКТ{CreatePZ.nkt_diam}мм шаблоном.  Спуск компоновки производить  со скоростью не более 0,30 м/с, не допуская резких ударов и вращения.'
                        f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации, фотографии предоставить в ЦИТС Ойл-сервис, передать по сводке уровня '
                        f'жидкости до перфорации и после перфорации) '
                        f'(При СПО первых десяти НКТ на спайдере дополнительно '
                        f'устанавливать элеватор ЭХЛ).' ,
                 None, None, None, None, None, None, None,
                  'Подрядчик по ГИС, мастер КРС', None, None],
            [None, None, 'Произвести ГИС привязку трубного перфоратора по ГК, ЛМ.',
            None, None, None, None, None, None, None,
            'Подрядчик по ГИС', None, None]]
        if float(CreatePZ.max_angle) >= 50:
            for i in range(len(pipe_perforation)):
                perforation.insert(i + 1, pipe_perforation[i])

        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700)}
        # print(len(perforation))

        if len(perforation) < 6:
            msg = QMessageBox.information(self, 'Внимание', 'Не добавлены интервалы перфорации!!!')
        else:
            for i, row_data in enumerate(perforation):
                row = self.ins_ind + i
                self.table_widget.insertRow(row)
                lst = [0, 1, 2, len(perforation)-1]
                if float(CreatePZ.max_angle) >= 50:
                    lst.extend([3, 4])
                if i in lst: # Объединение ячеек по вертикале в столбце "отвественные и норма"
                    self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
                for column, data in enumerate(row_data):

                    # widget = QtWidgets.QLabel(str())
                    # if column != 25:
                    #     widget.setStyleSheet("""QLabel {
                    #                                         border: 1px solid black;
                    #                                         font-size: 12px;
                    #                                         font-family: Arial;
                    #                                     }
                    #                                     """)
                    #     self.table_widget.setCellWidget(row, column, widget)
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

                    # if column == 2 or column == 10 or column == 11:
                    if not data  is  None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(str(text)) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))
                    else:
                        self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))
            # self.table_widget.setSpan(1 + self.ins_ind, 10, len(perforation) - 2, 1)
            # self.table_widget.setSpan(1 + self.ins_ind, 11, len(perforation) - 2, 1)

            print(f'мин {CreatePZ.perforation_roof}, мак {CreatePZ.perforation_sole}')

            self.table_widget.setRowHeight(self.ins_ind, 60)
            self.table_widget.setRowHeight(self.ins_ind + 1, 60)

            CreatePZ.definition_plast_work(self)

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
    window = PerforationWindow()
    window.show()
    sys.exit(app.exec_())