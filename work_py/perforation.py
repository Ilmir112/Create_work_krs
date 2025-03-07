from PyQt5 import QtWidgets
from PyQt5.Qt import *

import data_list
from work_py.acid_paker import CheckableComboBox
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from work_py.swabbing import SwabWindow


class TabPageSo(TabPageUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__(parent)

        self.labelType = QLabel("Кровля  перфорации", self)
        self.lineedit_type = QLineEdit(self)
        self.lineedit_type.setClearButtonEnabled(True)
        self.tableWidget = tableWidget

        self.labelType2 = QLabel("Подошва  перфорации", self)
        self.lineedit_type2 = QLineEdit(self)
        self.lineedit_type2.setClearButtonEnabled(True)

        self.labelTypeCharges = QLabel("Тип зарядов", self)
        self.ComboBoxCharges = QComboBox(self)
        self.ComboBoxCharges.addItems(['ГП', 'БО'])

        self.ComboBoxCharges.setProperty("value", 'ГП')

        self.labelHolesMetr = QLabel("отверстий на 1п.м", self)
        self.lineEditHolesMetr = QComboBox(self)
        self.lineEditHolesMetr.addItems(['6', '8', '10', '16', '18', '20', '30'])
        self.lineEditHolesMetr.setCurrentIndex(3)

        self.labelIndexFormation = QLabel("Индекс пласта", self)
        self.lineEditIndexFormation = QLineEdit(self)
        self.lineEditIndexFormation.setClearButtonEnabled(True)



        self.label_type_perforation = QLabel("Тип перфорации", self)
        TabPageSo.combobox_type_perforation = QComboBox(self)
        TabPageSo.combobox_type_perforation.addItems(['ПВР на кабеле', 'Трубная перфорация', 'Трубная перфорация на депрессии'])

        self.labelDopInformation = QLabel("Доп информация", self)
        self.lineEditDopInformation = QLineEdit(self)
        self.lineEditDopInformation.setClearButtonEnabled(True)

        # self.grid = QGridLayout(self)
        self.grid.addWidget(self.labelType, 0, 0)
        self.grid.addWidget(self.labelType2, 0, 1)
        self.grid.addWidget(self.labelTypeCharges, 0, 2)
        self.grid.addWidget(self.labelHolesMetr, 0, 3)

        self.grid.addWidget(self.labelIndexFormation, 0, 4)
        self.grid.addWidget(self.labelDopInformation, 0, 5)
        self.grid.addWidget(self.lineedit_type, 1, 0)
        self.grid.addWidget(self.lineedit_type2, 1, 1)
        self.grid.addWidget(self.ComboBoxCharges, 1, 2)
        self.grid.addWidget(self.lineEditHolesMetr, 1, 3)
        self.grid.addWidget(self.lineEditIndexFormation, 1, 4)
        self.grid.addWidget(self.lineEditDopInformation, 1, 5)
        self.grid.addWidget(self.label_type_perforation, 0, 6)
        self.grid.addWidget(TabPageSo.combobox_type_perforation, 1, 6)

        TabPageSo.combobox_type_perforation.currentTextChanged.connect(self.update_combobox_type_perforation)

    def update_combobox_type_perforation(self, index):
        if self.tableWidget.rowCount() == 0 and index in ['Трубная перфорация', 'Трубная перфорация на депрессии']:
            QMessageBox.warning(self, 'Ошибка', 'Сначало нужно добавить все плановые интервалы перфорации')
            TabPageSo.combobox_type_perforation.setCurrentIndex(0)
            return
        if index in ['Трубная перфорация', 'Трубная перфорация на депрессии']:
            self.question_need_paker_label = QLabel('Внедрять пакер в компоновку?')
            self.question_need_paker_combo = QComboBox(self)
            self.question_need_paker_combo.addItems(['Нет', 'Да'])

            self.grid.addWidget(self.question_need_paker_label, 0, 7)
            self.grid.addWidget(self.question_need_paker_combo, 1, 7)
            self.question_need_paker_combo.currentTextChanged.connect(self.update_need_paker)

            self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
            self.svk_true_combo = QComboBox(self)
            self.svk_true_combo.addItems(['без СКВ', 'Нужно СКВ', ])

            self.sko_true_label_type = QLabel("необходимость СКО", self)
            self.sko_true_combo = QComboBox(self)
            self.sko_true_combo.addItems(['Нет', 'Да'])

            self.swab_true_label_type = QLabel("необходимость освоения", self)
            self.swab_true_edit_type = QComboBox(self)

            self.swab_true_edit_type.addItems(['без освоения', 'Нужно освоение'])
            self.grid.addWidget(self.swab_true_label_type, 12, 0)
            self.grid.addWidget(self.swab_true_edit_type, 13, 0)

            self.grid.addWidget(self.sko_true_label_type, 6, 0)
            self.grid.addWidget(self.sko_true_combo, 7, 0)
            self.grid.addWidget(self.skv_true_label_type, 4, 0)
            self.grid.addWidget(self.svk_true_combo, 5, 0)

            self.sko_true_combo.currentTextChanged.connect(self.update_sko_true)

            self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)
            self.swab_true_edit_type.currentTextChanged.connect(self.update_need_swab)

        else:
            self.question_need_paker_label.setParent(None)
            self.question_need_paker_combo.setParent(None)
            self.question_need_paker_combo.setParent(None)
            self.skv_true_label_type.setParent(None)
            self.svk_true_combo.setParent(None)

            self.sko_true_label_type.setParent(None)
            self.sko_true_combo.setParent(None)

            self.swab_true_label_type.setParent(None)
            self.swab_true_edit_type.setParent(None)

    def update_need_paker(self, index):
        self.paker_label = QLabel("глубина пакера", self)
        self.paker_depth_edit = QLineEdit(self)
        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        if index == 'Нет':
            self.paker_label.setParent(None)
            self.paker_depth_edit.setParent(None)
            self.diameter_paker_label_type.setParent(None)
            self.diameter_paker_edit.setParent(None)
        else:

            self.grid.addWidget(self.paker_label, 0, 8)
            self.grid.addWidget(self.paker_depth_edit, 1, 8)
            self.grid.addWidget(self.diameter_paker_label_type, 0, 9)
            self.grid.addWidget(self.diameter_paker_edit, 1, 9)

            self.tableWidget.min_roof = min(
                [float(self.tableWidget.item(row, 0).text()) for row in range(self.tableWidget.rowCount())])

            if self.data_well.column_additional is False or \
                    (
                            self.data_well.column_additional and self.data_well.head_column_additional.get_value > self.data_well.current_bottom):
                self.paker_depth_edit.setText(str(int(self.tableWidget.min_roof) - 20))
            else:
                self.paker_depth_edit.setText(str(float(self.data_well.head_column_additional.get_value) - 20))

            self.paker_depth_edit.textChanged.connect(self.update_paker_depth_edit)

    def update_paker_depth_edit(self):
        paker_depth_edit = self.paker_depth_edit.text()
        if paker_depth_edit:
            paker_diameter = int(float(self.paker_diameter_select(paker_depth_edit)))
            self.diameter_paker_edit.setText(str(paker_diameter))

    def select_type_perforation(self, sole):
        if len(self.data_well.angle_data) == 0 and self.data_well.max_angle.get_value < 50:
            TabPageSo.combobox_type_perforation.setCurrentIndex(0)
        elif len(self.data_well.angle_data) == 0 and self.data_well.max_angle.get_value >= 50:
            TabPageSo.combobox_type_perforation.setCurrentIndex(1)
        elif len(self.data_well.angle_data) != 0:
            if sole != '':
                angle_list = [(depth, angle) for depth, angle, curvature in self.data_well.angle_data
                              if abs(float(depth) - float(sole)) <= 10]
                depth_max = max([float(str(depth).replace(',', '.')) for depth, angle in angle_list])
                angle_depth = max([float(str(angle).replace(',', '.')) for depth, angle in angle_list])

                if angle_depth < 50:
                    TabPageSo.combobox_type_perforation.setCurrentIndex(0)
                    return ''
                else:
                    TabPageSo.combobox_type_perforation.setCurrentIndex(1)
                    return f'На глубине {depth_max}м угол {angle_depth}'


class TabWidget(TabWidgetUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__()
        self.addTab(TabPageSo(tableWidget, parent), 'Перфорация')


class PerforationWindow(WindowUnion):
    def __init__(self, data_well=None, table_widget=None, parent=None):
        super().__init__(data_well)
        if self.data_well:
            self.insert_index = data_well.insert_index
            # self.dict_perforation = self.data_well.dict_perforation
            self.dict_perforation_project = self.data_well.dict_perforation_project

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.tableWidget = QTableWidget(0, 7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.",
             "Количество отверстий", "Вскрываемые пласты", "доп информация"])
        for i in range(7):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tab_widget = TabWidget(self.tableWidget, self.data_well)

        self.buttonAdd = QPushButton('Добавить интервалы перфорации в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить интервалы перфорации в таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddProject = QPushButton('Добавить проектные интервалы перфорации')
        self.buttonAddProject.clicked.connect(self.addPerfProject)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddProject, 3, 1)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def addPerfProject(self):

        if self.data_well.grp_plan:
            chargePM_GP = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                              'кол-во отверстий на 1 п.м. зарядов ГП', 20, 5,
                                              50)[0]
            chargePM_BO = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                              'кол-во отверстий на 1 п.м. зарядов БО', 10, 5,
                                              50)[0]
        else:
            chargePM = QInputDialog.getInt(self, 'кол-во отверстий на 1 п.м.',
                                           'кол-во отверстий на 1 п.м.', 16, 5,
                                           50)[0]

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        if len(self.data_well.dict_perforation_project) != 0:

            for plast, data in self.data_well.dict_perforation_project.items():
                a = data['интервал']
                for i in data['интервал']:
                    TabPageSo.select_type_perforation(self, i[1])
                    if self.data_well.grp_plan:
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
                        if count_charge < 0 or count_charge > 500:
                            QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
                            return
                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[1]))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM_BO)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

                    else:
                        # Вставка интервалов зарядов ГП без ГРП
                        count_charge = int((max(i) - min(i)) * chargePM)
                        if count_charge < 0 or count_charge > 500:
                            QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
                            return

                        self.tableWidget.insertRow(rows)
                        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(min(i))))
                        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(max(i))))
                        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.charge(max(i))[0]))
                        self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(chargePM)))
                        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_charge)))

                        self.tableWidget.setItem(rows, 5, QTableWidgetItem(plast))
                        self.tableWidget.setItem(rows, 6, QTableWidgetItem(' '))

        else:
            for plast, data in self.data_well.dict_perforation.items():

                if plast in self.data_well.plast_work:
                    for i in data['интервал']:
                        TabPageSo.select_type_perforation(self, i[1])
                        if i[1] <= self.data_well.current_bottom:
                            if self.data_well.grp_plan:
                                # Вставка интервалов зарядов ГП
                                count_charge = int((max(i) - min(i)) * chargePM_GP)
                                if count_charge < 0 or count_charge > 500:
                                    QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
                                    return

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
                                if count_charge < 0 or count_charge > 500:
                                    QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
                                    return
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

        if self.data_well.column_additional is False or (
                self.data_well.column_additional is True and pvr < self.data_well.head_column_additional.get_value):
            diam_internal_ek = self.data_well.column_diameter.get_value
        else:
            diam_internal_ek = self.data_well.column_additional_diameter.get_value

        for diam, diam_internal_paker in charge_diam_dict.items():
            if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                zar = 25 if diam == 73 else 32
                return f'{diam} ПП{zar}ГП', f'{diam} ПП{zar}БО'

    def add_row_table(self):
        self.current_widget = self.tab_widget.currentWidget()

        edit_type = self.current_widget.lineedit_type.text().replace(',', '.')
        edit_type2 = self.current_widget.lineedit_type2.text().replace(',', '.')
        chargesx = str(self.current_widget.ComboBoxCharges.currentText())
        editHolesMetr = self.current_widget.lineEditHolesMetr.currentText()
        editIndexFormation = self.current_widget.lineEditIndexFormation.text()
        dopInformation = self.current_widget.lineEditDopInformation.text()
        if not edit_type or not edit_type2 or not chargesx or not editIndexFormation:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if float(edit_type2.replace(',', '.')) >= float(self.data_well.current_bottom):
            QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
            return
        self.plast_combo = editIndexFormation
        chargesx = self.charge(int(float(edit_type2)))[0][:-2] + chargesx
        count_otv = int((float(edit_type2) - float(edit_type)) * int(editHolesMetr))
        if count_otv < 0:
            QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
            return
        TabPageSo.select_type_perforation(self, edit_type2)
        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(edit_type))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(edit_type2))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(chargesx))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(editHolesMetr))
        self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(count_otv)))
        self.tableWidget.setItem(rows, 5, QTableWidgetItem(editIndexFormation))
        self.tableWidget.setItem(rows, 6, QTableWidgetItem(dopInformation))
        self.tableWidget.setSortingEnabled(True)
        # print(edit_type, spinYearOfIssue, editSerialNumber, editSpecifications)

    def add_work(self):
        self.current_widget = self.tab_widget.currentWidget()
        rows = self.tableWidget.rowCount()
        self.type_perforation = self.current_widget.combobox_type_perforation.currentText()
        if len(self.data_well.category_pressure_list) > 1:
            self.data_well.category_pressure = self.data_well.category_pressure_list[1]

            self.data_well.category_h2s = self.data_well.category_h2s_list[1]
            self.data_well.category_gas_factor = self.data_well.category_gaz_factor_percent[1]
            kateg2 = [1 if str(self.data_well.category_pressure_list[1]) == '1' or
                           str(self.data_well.category_h2s_list[1]) == '1' else 2][0]

            if self.data_well.category_pvo < kateg2:
                self.data_well.category_pvo = kateg2

        if 'Ойл' in data_list.contractor:
            shema_str = 'a'
        elif 'РН' in data_list.contractor:
            if self.type_perforation == 'ПВР на кабеле':
                shema_str = 'a'
            else:
                shema_str = 'б'
        angle_text = ''
        if self.data_well.angle_data:
            if self.data_well.max_angle.get_value > 45:
                max_depth_pvr = max([float(self.tableWidget.item(row, 1).text()) for row in range(rows)])
                tuple_angle = self.calculate_angle(max_depth_pvr, self.data_well.angle_data)
                angle_text = tuple_angle[2]

        perforation = [
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через '
             f'ЦИТС {data_list.contractor}". '
             f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
             f'Произвести  монтаж ГИС согласно схемы  №8{shema_str} утвержденной главным инженером от '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
             None, None, None, None, None, None, None,
             'Мастер КРС', None, None, None],
            [None, None,
             f'Долить скважину до устья тех жидкостью уд.весом {self.data_well.fluid_work}. '
             f'Опрессовать плашки ПВО (на давление опрессовки ЭК, но '
             f'не ниже максимального ожидаемого давления на устье) '
             f'{self.data_well.max_admissible_pressure.get_value}атм, по невозможности на давление поглощения, но '
             f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). '
             f'Передать по сводке уровня жидкости до перфорации и после перфорации.'
             f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения '
             f'перфорации,'
             f' фотографии предоставить в ЦИТС {data_list.contractor}',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2, None],
            [f"ГИС (Перфорация на кабеле ЗАДАЧА 2.9.1)", None,
             f"ГИС (Перфорация на кабеле ЗАДАЧА 2.9.1) \n{angle_text}", None, None, None, None,
             None, None, None, 'подрядчик по ГИС', None],
            [None, None, "Кровля", "-", "Подошва", "Тип заряда", "отв на 1 п.м.", "Кол-во отв",
             "пласт", "Доп.данные", 'подрядчик по ГИС', None]
        ]
        if self.type_perforation in ['Трубная перфорация', 'Трубная перфорация на депрессии']:
            self.tableWidget.min_roof = min(
                [float(self.tableWidget.item(row, 0).text()) for row in range(self.tableWidget.rowCount())])

            self.swab_true_edit_type = self.current_widget.swab_true_edit_type.currentText()
            if self.swab_true_edit_type == "Нужно освоение":
                read_swab = self.read_update_need_swab(self.current_widget)
                if read_swab is False:
                    return

            self.svk_true_combo = self.current_widget.svk_true_combo.currentText()
            if self.svk_true_combo == 'Нужно СКВ':
                read_skv = self.read_update_skv(self.current_widget)
                if read_skv is False:
                    return

            self.sko_true_combo = str(self.current_widget.sko_true_combo.currentText())
            if self.sko_true_combo == "Да":
                read_sko = self.read_sko_need(self.current_widget)
                if read_sko is False:
                    return

                self.expected_pickup = self.current_widget.expected_pickup_edit.text()
                self.expected_pressure = self.current_widget.expected_pressure_edit.text()
                if self.expected_pressure not in [None, 'None', '', '-', 'атм']:
                    self.expected_pressure = int(float(self.expected_pressure))
                self.pressure_three = self.current_widget.pressure_three_edit.text()

            self.question_need_paker_combo = self.current_widget.question_need_paker_combo.currentText()
            if self.question_need_paker_combo == 'Да':
                self.paker_depth = self.current_widget.paker_depth_edit.text()
                self.diameter_paker = self.current_widget.diameter_paker_edit.text()
                self.current_widget.question_need_paker_combo.currentText()
                if self.paker_depth == '' or self.diameter_paker == '':
                    QMessageBox.warning(self, 'Ошибка', 'Не введены данные по пакеру')
                    return
                else:
                    self.paker_depth = int(self.paker_depth)
                    self.diameter_paker = int(float(self.diameter_paker))
                    self.paker_khost = int(self.tableWidget.min_roof - self.paker_depth)

                if self.check_true_depth_template(self.paker_depth) is False:
                    return
                if self.true_set_paker(self.paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(self.paker_depth) is False:
                    return

                self.nkt_diam, self.nkt_pod, self.nkt_template = self.select_diameter_nkt(self.paker_depth,
                                                                                          self.swab_true_edit_type)
                if self.data_well.column_additional is False or \
                        (self.data_well.column_additional and \
                         self.data_well.head_column_additional.get_value > self.data_well.current_bottom):
                    self.dict_nkt = {self.nkt_diam: float(self.tableWidget.min_roof)}
                else:
                    self.dict_nkt = {
                        self.nkt_diam: round(self.data_well.head_column_additional.get_value, 0),
                        self.nkt_pod: round(
                            float(self.tableWidget.min_roof) - self.data_well.head_column_additional.get_value, 0)}
            else:
                self.paker_layout_combo = 'воронка'


            perforation[2] = [f"ГИС ( Трубная Перфорация ЗАДАЧА 2.9.2)", None,
                              f"ГИС ( Трубная Перфорация ЗАДАЧА 2.9.2). \n{angle_text}", None, None, None, None,
                              None, None, None, 'подрядчик по ГИС', None]

        for row in range(rows):
            item = self.tableWidget.item(row, 1)
            if item:
                value = item.text()
                # print(f'dff{value}')
                if float(value) >= self.data_well.current_bottom:
                    QMessageBox.information(self, 'Внимание', 'Подошва интервала перфорации ниже текущего забоя')
                    return
            perf_list = []
            ["Кровля перфорации", "Подошва Перфорации", "Тип заряда", "отв на 1 п.м.", "Количество отверстий",
             "Вскрываемые пласты", "доп информация"]
            roof = self.tableWidget.item(row, 0).text().replace(',', '.')
            sool = self.tableWidget.item(row, 1).text().replace(',', '.')

            type_charge = self.tableWidget.item(row, 2).text()
            count_otv = self.tableWidget.item(row, 3).text()
            if count_otv != '':
                count_charge = float(count_otv)
                if 0 > count_charge or count_charge > 500:
                    QMessageBox.warning(self, 'НЕКОРРЕКТНО', 'ОБЪЕМ зарядов некорректен')
                    return
            count_charge = self.tableWidget.item(row, 4).text()
            plast = self.tableWidget.item(row, 5).text()
            dop_information = self.tableWidget.item(row, 6).text()

            pvr_str = f'ПВР {plast} {roof}-{sool}м {count_otv}отв/м'
            if 'c.' not in plast or 'спец' not in plast:
                if float(roof) < float(self.data_well.level_cement_column.get_value) and \
                        self.data_well.column_additional is False:
                    QMessageBox.warning(self, 'Ошибка', f'Уровень цемента за колонной '
                                                        f'{self.data_well.level_cement_column.get_value}м ниже '
                                                        f'кровли ПВР {roof}м,'
                                                        f'Нужно согласовать дополнительно корректность ПВР')
            perf_list.extend(
                [pvr_str, None, roof, '-', sool, type_charge, count_otv, count_charge, plast, dop_information,
                 'подрядчик по ГИС', round(float(sool) - float(roof)) * 1.5, 1])

            self.data_well.dict_perforation.setdefault(plast, {}).setdefault('интервал', []).append(
                (float(perf_list[2]), float(perf_list[4])))
            self.data_well.dict_perforation[plast]['отрайбировано'] = False
            self.data_well.dict_perforation[plast]['отключение'] = False
            self.data_well.dict_perforation[plast]['Прошаблонировано'] = False
            self.data_well.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
            self.data_well.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
            # print(f' перфорация после добавления {self.data_well.dict_perforation}')
            self.data_well.dict_perforation[plast]['интервал'] = list(
                set(map(tuple, self.data_well.dict_perforation[plast]['интервал'])))

            perforation.append(perf_list)

        # print([self.data_well.dict_perforation[plast] for plast in self.data_well.plast_work])

        if self.type_perforation in ['Трубная перфорация', 'Трубная перфорация на депрессии']:

            pipe_perforation = [
                [f'монтаж трубного перфоратора', None,
                 f'Произвести монтаж трубного перфоратора + 2шт/20м НКТ + реперный '
                 f'патрубок L=2м до намеченного интервала перфорации '
                 f'(с шаблонировкой НКТ{self.data_well.nkt_diam}мм шаблоном {self.data_well.nkt_template}мм. '
                 f'Спуск компоновки производить  со скоростью не более 0,30 м/с, не допуская резких ударов и вращения.'
                 f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации, '
                 f'фотографии предоставить в ЦИТС {data_list.contractor}, передать по сводке уровня '
                 f'жидкости до перфорации и после перфорации) '
                 f'(При СПО первых десяти НКТ на спайдере дополнительно '
                 f'устанавливать элеватор ЭХЛ). ',
                 None, None, None, None, None, None, None,
                 'Подрядчик по ГИС, мастер КРС', None, None],
                [None, None, 'Произвести ГИС привязку трубного перфоратора по ГК, ЛМ.',
                 None, None, None, None, None, None, None,
                 'Подрядчик по ГИС', None, None]]

            if self.question_need_paker_combo == 'Да':
                self.paker_layout_combo = 'однопакерная'

                pipe_perforation = [[
                    f'монтаж трубного перфоратора + ПАКЕР', None,
                    f'Произвести монтаж трубного перфоратора + НКТ {self.tableWidget.min_roof - self.paker_depth} '
                    f'НКТ + пакер-{self.diameter_paker}мм + '
                    f'НКТ 20м + реперный '
                    f'патрубок L=2м до намеченного интервала перфорации '
                    f'(с шаблонировкой НКТ{self.data_well.nkt_diam}мм шаблоном {self.data_well.nkt_template}мм. '
                    f'Спуск компоновки производить  со скоростью не более 0,30 м/с, не допуская резких ударов '
                    f'и вращения.'
                    f'(Произвести фотографию перфоратора в заряженном состоянии, и после проведения перфорации, '
                    f'фотографии предоставить в ЦИТС {data_list.contractor}, передать по сводке уровня '
                    f'жидкости до перфорации и после перфорации) '
                    f'(При СПО первых десяти НКТ на спайдере дополнительно '
                    f'устанавливать элеватор ЭХЛ). ',
                    None, None, None, None, None, None, None,
                    'Подрядчик по ГИС, мастер КРС', None, None]]


                mes = QMessageBox.question(self, 'пакер при трубной перфорации',
                                           'Внедрять ли пакер в компоновку с трубным перфоратором?')
                if mes == QMessageBox.No:
                    return

            if self.type_perforation in ['Трубная перфорация на депрессии']:
                if 'Ойл' in data_list.contractor:
                    schema_swab = '8'
                elif 'РН' in data_list.contractor:
                    schema_swab = '7'
                pipe_perforation.extend([[None, None,
                 f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной главным инженером '
                 f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г.'
                 f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
                 f'давление на устье {self.data_well.max_admissible_pressure.get_value}атм,'
                 f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
                 f'практическое обучение вахт по '
                 f'сигналу "выброс" с записью в журнале проведения учебных тревог',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 1.3],
                 ['Понижение ', None, 'Произвести максимальное понижение уровня в скважине (дополнительно согласовать '
                                      'с заказчиком глубину понижению уровня)',
                  None, None, None, None, None, None, None, 'подрядчика по ГИС', 30]])

            for i in range(len(pipe_perforation)):
                if i == 0:
                    perforation.insert(i + 1, pipe_perforation[i])
                else:
                    perforation.insert(i + 2, pipe_perforation[i])

            if self.svk_true_combo == 'Нужно СКВ':
                perforation.extend(self.skv_acid_work())
            if self.sko_true_combo == 'Да':
                self.plast_combo = plast
                perforation.extend(self.acid_work())
            if self.swab_true_edit_type == 'Нужно освоение':
                self.depth_gauge = ''
                if self.question_need_paker_combo:
                    swab_work_list = SwabWindow.swabbing_with_paker(self)
                else:
                    swab_work_list = SwabWindow.swabbing_with_voronka(self)

                perforation.extend(swab_work_list[1:])
        end_list = "Произвести контрольную запись ЛМ;ТМ. Составить АКТ на перфорацию."\
            if self.type_perforation not in ['Трубная перфорация','Трубная перфорация на депрессии'] \
            else f'Подъем последних 5-ти НКТ{self.data_well.nkt_diam}мм и демонтаж перфоратора ' \
                 f'производить в присутствии ответственного ' \
                 f'представителя подрядчика по ГИС» (руководителя взрывных' \
                 f' работ или взрывника).'

        perforation.append([None, None, end_list,
                            None, None, None, None, None, None, None,
                            'Подрядчик по ГИС', 2])

        if len(perforation) < 6:
            QMessageBox.information(self, 'Внимание', 'Не добавлены интервалы перфорации!!!')
        else:
            self.populate_row(self.insert_index, perforation, self.table_widget)
            data_list.pause = False
            self.close()


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
    window = PerforationWindow()
    window.show()
    sys.exit(app.exec_())
