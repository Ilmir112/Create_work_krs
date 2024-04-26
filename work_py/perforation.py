from PyQt5 import QtWidgets
from PyQt5.Qt import *

import well_data
from main import MyWindow
from .advanted_file import definition_plast_work


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


class PerforationWindow(QMainWindow):

    def __init__(self, table_widget, ins_ind, parent=None):

        super(QMainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        # self.dict_perforation = well_data.dict_perforation
        self.dict_perforation_project = well_data.dict_perforation_project
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.",
             "Количество отверстий", "Вскрываемые пласты", "доп информация"])
        for i in range(7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить интервалы перфорации в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить интервалы перфорации в таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddProject = QPushButton('Добавить проектные интервалы перфорации')
        self.buttonAddProject.clicked.connect(self.addPerfProject)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddProject, 3, 1)

    def addPerfProject(self):



        self.tableWidget.setSortingEnabled(False)
        # print(f' проект {self.dict_perforation_project}')
        # print(f' текущий ПВР {self.dict_perforation}')
        rows = self.tableWidget.rowCount()

        # print(f'проект {well_data.dict_perforation_project}')
        if len(well_data.dict_perforation_project) != 0:
            for plast, data in well_data.dict_perforation_project.items():
                for i in data['интервал']:
                    if well_data.grp_plan:
                        chargePM_GP = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                                          'кол-во отверстий на 1 п.м. зарядов ГП', 20, 5,
                                                          50)[0]
                        chargePM_BO = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                                          'кол-во отверстий на 1 п.м. зарядов БО', 20, 5,
                                                          50)[0]

                        count_charge = int((max(i) - min(i)) * chargePM_GP)
                        # Вставка интервалов зарядов ГП
                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[0]))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM_GP)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

                        # Вставка интервалов зарядов БО
                        count_charge = int((max(i) - min(i)) * chargePM_BO)
                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[1]))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM_BO)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

                    else:

                        chargePM = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                                       'кол-во отверстий на 1 п.м.', 20, 5,
                                                       50)[0]
                        # print(i[1], well_data.current_bottom)


                        # Вставка интервалов зарядов ГП без ГРП
                        count_charge = int((max(i) - min(i)) * chargePM)

                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[0]))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

        else:
            for plast, data in well_data.dict_perforation.items():

                if plast in well_data.plast_work:
                    for i in data['интервал']:
                        if i[1] <= well_data.current_bottom:
                            if well_data.grp_plan:
                                # Вставка интервалов зарядов ГП
                                count_charge = int((max(i) - min(i)) * chargePM_GP)

                                self.tableWidget.insertRow(rows)
                                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                                self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[0]))
                                self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM_GP)))
                                self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))
                                self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                                self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

                                # Вставка интервалов зарядов БО
                                count_charge = int((max(i) - min(i)) * chargePM_BO)
                                self.tableWidget.insertRow(rows)
                                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                                self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[1]))
                                self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM_BO)))
                                self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                                self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                                self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))
                            else:
                                count_charge = int((max(i) - min(i)) * chargePM)
                                # print(i)
                                # print(str(min(i)))
                                self.tableWidget.insertRow(rows)
                                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                                self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[0]))
                                self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM)))
                                self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                                self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                                self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))
        self.tableWidget.setSortingEnabled(True)

    def charge(self, pvr):

        charge_diam_dict = {73: (0, 110), 89: (111, 135), 102: (136, 160), 114: (160, 250)}

        if well_data.column_additional is False or (
                well_data.column_additional is True and pvr < well_data.head_column_additional._value):
            diam_internal_ek = well_data.column_diametr._value
        else:
            diam_internal_ek = well_data.column_additional_diametr._value

        for diam, diam_internal_paker in charge_diam_dict.items():
            if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                zar = 25 if diam == 73 else 32
                return f'{diam} ПП{zar}ГП', f'{diam} ПП{zar}БО'

    def addRowTable(self):

        editType = self.tabWidget.currentWidget().lineEditType.text().replace(',', '.')
        editType2 = self.tabWidget.currentWidget().lineEditType2.text().replace(',', '.')
        chargesx = str(self.tabWidget.currentWidget().ComboBoxCharges.currentText())
        editHolesMetr = self.tabWidget.currentWidget().lineEditHolesMetr.currentText()
        editIndexFormation = self.tabWidget.currentWidget().lineEditIndexFormation.text()
        dopInformation = self.tabWidget.currentWidget().lineEditDopInformation.text()
        if not editType or not editType2 or not chargesx or not editIndexFormation:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if float(editType2.replace(',', '.')) >= float(well_data.current_bottom):
            msg = QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
            return

        chargesx = self.charge(int(float(editType2)))[0][:-2] + chargesx

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(editType))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(editType2))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(chargesx))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(editHolesMetr))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(int((float(editType2) - float(
            editType)) * int(editHolesMetr)))))
        self.tableWidget.setItem(rows, 5, QTableWidgetItem(editIndexFormation))
        self.tableWidget.setItem(rows, 6, QTableWidgetItem(dopInformation))
        self.tableWidget.setSortingEnabled(True)
        # print(editType, spinYearOfIssue, editSerialNumber, editSpecifications)

    def geophysicalSelect(self, geophysic):
        return geophysic
    def add_work(self):

        rows = self.tableWidget.rowCount()
        if len(well_data.cat_P_1) > 1:
            well_data.category_pressuar = well_data.cat_P_1[1]
            well_data.category_h2s = well_data.cat_h2s_list[1]
            well_data.category_gf = well_data.cat_gaz_f_pr[1]
            kateg2 = [1 if str(well_data.cat_P_1[1]) == '1' or str(well_data.cat_h2s_list[1]) == '1' else 2][0]

            if well_data.kat_pvo < kateg2:
                well_data.kat_pvo = kateg2

        perforation = [[None, None,
                        f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через '
                        f'ЦИТС "Ойл-сервис". '
                        f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                        f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г',
                        None, None, None, None, None, None, None,
                        'Мастер КРС', None, None, None],
                       [None, None,
                        f'Долить скважину до устья тех жидкостью уд.весом {well_data.fluid_work}. '
                        f'Установить ПВО по схеме №8а утвержденной '
                        f'главным инженером ООО "Ойл-сервис" от 14.10.2021г. Опрессовать  плашки  '
                        f'ПВО (на давление опрессовки ЭК, но '
                        f'не ниже максимального ожидаемого давления на устье) '
                        f'{well_data.max_admissible_pressure._value}атм, по невозможности на давление поглощения, но '
                        f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). '
                        f'Передать по сводке уровня жидкости до перфорации и после перфорации.'
                        f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения '
                        f'перфорации,'
                        f' фотографии предоставить в ЦИТС Ойл-сервис',
                        None, None, None, None, None, None, None,
                        'Мастер КРС, подрядчик по ГИС', 1.2, None],
                       [''.join(["ГИС (Перфорация на кабеле ЗАДАЧА 2.9.1)" if float(well_data.max_angle._value) <= 50
                                 else "ГИС ( Трубная Перфорация ЗАДАЧА 2.9.2)"]), None,
                        ''.join(["ГИС (Перфорация на кабеле ЗАДАЧА 2.9.1)" if float(well_data.max_angle._value) <= 50
                                 else "ГИС ( Трубная Перфорация ЗАДАЧА 2.9.2)"]), None, None, None, None,
                        None, None, None, 'подрядчик по ГИС', None],
                       [None, None, "Кровля", "-", "Подошва", "Тип заряда", "отв на 1 п.м.", "Кол-во отв",
                        "пласт", "Доп.данные", 'подрядчик по ГИС', None]
                       ]

        for row in range(rows):
            item = self.tableWidget.item(row, 1)
            if item:
                value = item.text()
                # print(f'dff{value}')
                if float(value) >= well_data.current_bottom:
                    msg = QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
                    return
        for row in range(rows):
            perf_list = []
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.", "Количество отверстий",
             "Вскрываемые пласты", "доп информация"]
            roof = self.tableWidget.item(row, 0).text()
            sool = self.tableWidget.item(row, 1).text()
            type_charge = self.tableWidget.item(row, 2).text()
            count_otv = self.tableWidget.item(row, 3).text()
            count_charge = self.tableWidget.item(row, 4).text()
            plast = self.tableWidget.item(row, 5).text()
            dop_information = self.tableWidget.item(row, 6).text()

            pvr_str = f'ПВР {plast} {roof}-{sool}м {count_otv}отв/м'

            perf_list.extend(
                [pvr_str, None, roof, '-', sool, type_charge, count_otv, count_charge, plast, dop_information,
                 'подрядчик по ГИС', round(float(sool) - float(roof)) * 1.5, 1])

            well_data.dict_perforation.setdefault(plast, {}).setdefault('интервал', []).append(
                (float(perf_list[2]), float(perf_list[4])))
            well_data.dict_perforation[plast]['отрайбировано'] = False
            well_data.dict_perforation[plast]['отключение'] = False
            well_data.dict_perforation[plast]['Прошаблонировано'] = False
            well_data.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
            well_data.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
            # print(f' перфорация после добавления {well_data.dict_perforation}')
            well_data.dict_perforation[plast]['интервал'] = list(
                set(map(tuple, well_data.dict_perforation[plast]['интервал'])))

            perforation.append(perf_list)

        perforation.append([None, None, ''.join(["Произвести контрольную запись ЛМ;ТМ. Составить АКТ на "
                                                 "перфорацию." if float(well_data.max_angle._value) <= 50 else ""
                                                                                                               f"Подъем последних 5-ти НКТ{well_data.nkt_diam}мм и демонтаж перфоратора "
                                                                                                               f"производить в присутствии ответственного "
                                                                                                               f"представителя подрядчика по ГИС» (руководителя взрывных"
                                                                                                               f" работ или взрывника)."]),
                            None, None, None, None, None, None, None,
                            'Подрядчик по ГИС', 2])
        # print([well_data.dict_perforation[plast] for plast in well_data.plast_work])
        pipe_perforation = [
            [f'монтаж трубного перфоратора', None,
             f'Произвести монтаж трубного перфоратора + 2шт/20м НКТ + реперный '
             f'патрубок L=2м до намеченного интервала перфорации '
             f'(с шаблонировкой НКТ{well_data.nkt_diam}мм шаблоном {well_data.nkt_template}мм. '
             f'Спуск компоновки производить  со скоростью не более 0,30 м/с, не допуская резких ударов и вращения.'
             f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации, '
             f'фотографии предоставить в ЦИТС Ойл-сервис, передать по сводке уровня '
             f'жидкости до перфорации и после перфорации) '
             f'(При СПО первых десяти НКТ на спайдере дополнительно '
             f'устанавливать элеватор ЭХЛ).',
             None, None, None, None, None, None, None,
             'Подрядчик по ГИС, мастер КРС', None, None],
            [None, None, 'Произвести ГИС привязку трубного перфоратора по ГК, ЛМ.',
             None, None, None, None, None, None, None,
             'Подрядчик по ГИС', None, None]]
        if float(well_data.max_angle._value) >= 50:
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
                lst = [0, 1, 2, len(perforation) - 1]
                row_max = self.table_widget.rowCount()
                definition_plast_work(self)
                MyWindow.insert_data_in_database(self, row, row_max)
                if float(well_data.max_angle._value) >= 50:
                    lst.extend([3, 4])
                if i in lst:  # Объединение ячеек по вертикале в столбце "отвественные и норма"
                    self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
                for column, data in enumerate(row_data):

                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(str(text)) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(float(text_width)))
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
    window = PerforationWindow()
    window.show()
    sys.exit(app.exec_())
