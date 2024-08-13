from PyQt5 import Qt
from PyQt5.QtGui import QDoubleValidator

import well_data
from main import MyWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QTabWidget, QPushButton, QHeaderView, QTableWidget, QTableWidgetItem

from work_py.alone_oreration import privyazkaNKT
from .rationingKRS import descentNKT_norm, liftingNKT_norm


class TabPage_SO(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.validator = QDoubleValidator(0.0, 80000.0, 2)

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)

        self.paker_khost_Label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator)

        self.paker_depth_Label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator)
        self.paker_depth_edit.textChanged.connect(self.update_paker)

        self.need_privyazka_Label = QLabel("Привязка оборудования", self)
        self.need_privyazka_QCombo = QComboBox()
        self.need_privyazka_QCombo.addItems(['Нет', 'Да'])

        if len(well_data.plast_work) != 0:
            pakerDepth = well_data.perforation_roof - 20
        else:
            # print(well_data.dict_perforation)
            if well_data.leakiness:
                pakerDepth = min([well_data.dict_leakiness['НЭК']['интервал'][nek][0] - 10
                                       for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()])
        try:
            self.paker_depth_edit.setText(str(int(pakerDepth)))
        except:
            pass


        self.paker_depth_zumpf_Label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator)

        self.pressureZUMPF_question_Label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressureZUMPF_question_QCombo = QComboBox(self)
        self.pressureZUMPF_question_QCombo.currentTextChanged.connect(self.update_paker_need)

        self.pressureZUMPF_question_QCombo.addItems(['Нет', 'Да'])

        self.grid_layout = QGridLayout(self)

        self.grid_layout.addWidget(self.diametr_paker_labelType, 3, 1)
        self.grid_layout.addWidget(self.diametr_paker_edit, 4, 1)

        self.grid_layout.addWidget(self.paker_khost_Label, 3, 2)
        self.grid_layout.addWidget(self.paker_khost_edit, 4, 2)

        self.grid_layout.addWidget(self.paker_depth_Label, 3, 3)
        self.grid_layout.addWidget(self.paker_depth_edit, 4, 3)

        self.grid_layout.addWidget(self.pressureZUMPF_question_Label, 3, 5)
        self.grid_layout.addWidget(self.pressureZUMPF_question_QCombo, 4, 5)

        self.grid_layout.addWidget(self.need_privyazka_Label, 3, 4)
        self.grid_layout.addWidget(self.need_privyazka_QCombo, 4, 4)

    def update_paker_need(self, index):
        if index == 'Да':
            if len(well_data.plast_work) != 0:
                paker_depth_zumpf = int(well_data.perforation_sole + 10)
            else:
                if well_data.leakiness:
                    paker_depth_zumpf = int(max([float(nek.split('-')[0])+10
                                           for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()]))

                    self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid_layout.addWidget(self.paker_depth_zumpf_Label, 3, 6)
            self.grid_layout.addWidget(self.paker_depth_zumpf_edit, 4, 6)
        elif index == 'Нет':
            self.paker_depth_zumpf_Label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)

    def update_paker(self):
        paker_depth = self.paker_depth_edit.text()
        if paker_depth != '':
            if well_data.open_trunk_well is True:

                paker_khost = well_data.current_bottom - int(paker_depth)
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{self.paker_diametr_select(int(paker_depth))}')
            else:
                paker_khost = 10
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{self.paker_diametr_select(int(paker_depth))}')
            need_count = 0
            for plast in well_data.plast_all:
                for roof, sole in well_data.dict_perforation[plast]['интервал']:
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth))< 10:
                        need_count += 1
            if well_data.leakiness:
                a = well_data.dict_leakiness
                for interval in well_data.dict_leakiness['НЭК']['интервал']:
                    roof, sole = interval.split('-')
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth)) < 10:
                        need_count += 1

            if need_count == 0:
                self.need_privyazka_QCombo.setCurrentIndex(0)
            else:
                self.need_privyazka_QCombo.setCurrentIndex(1)


    def paker_diametr_select(self, depth_landing):
        paker_diam_dict = {
            82: (84, 92),
            88: (92.1, 97),
            92: (97.1, 102),
            100: (102.1, 109),
            104: (109, 115),
            112: (118, 120),
            114: (120.1, 121.9),
            116: (122, 123.9),
            118: (124, 127.9),
            122: (128, 133),
            136: (144, 148),
            142: (148.1, 154),
            145: (154.1, 164),
            158: (166, 176),
            182: (190.6, 203.6),
            204: (215, 221)
        }

        if well_data.column_additional is False or (
                well_data.column_additional is True and int(depth_landing) <= well_data.head_column_additional._value):
            diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
        else:
            diam_internal_ek = well_data.column_additional_diametr._value - \
                               2 * well_data.column_additional_wall_thickness._value

        for diam, diam_internal_paker in paker_diam_dict.items():
            if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                paker_diametr = diam

        return paker_diametr


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Опрессовка')


class OpressovkaEK(QMainWindow):
    def __init__(self, ins_ind, table_widget, forRirTrue=False, parent=None):
        super().__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        # self.paker_select = None
        self.forRirTrue = forRirTrue

        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["хвост", "посадка пакера"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work)
        self.buttonAddString = QPushButton('Поинтервальная опрессовка')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)

        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

    def add_row_table(self):

        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        pressureZUMPF_combo = self.tabWidget.currentWidget().pressureZUMPF_question_QCombo.currentText()
        if not paker_khost or not paker_depth:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return


        if pressureZUMPF_combo == 'Да':
            paker_depth_zumpf = self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()
            if paker_depth_zumpf != '':
                paker_depth_zumpf = int(float(paker_depth_zumpf))
            if MyWindow.check_true_depth_template(self, paker_depth_zumpf) is False:
                return
            if MyWindow.true_set_Paker(self, paker_depth_zumpf) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker_depth_zumpf) is False:
                return

        else:
            paker_depth_zumpf = 0

        if int(paker_khost) + int(paker_depth) > well_data.current_bottom and pressureZUMPF_combo == 'Нет' \
                or int(paker_khost) + int(
            paker_depth_zumpf) > well_data.current_bottom and pressureZUMPF_combo == 'Да':
            mes = QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        if MyWindow.check_true_depth_template(self, paker_depth) is False:
            return
        if MyWindow.true_set_Paker(self, paker_depth) is False:
            return
        if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
            return


        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(paker_khost)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_depth)))


        self.tableWidget.setSortingEnabled(False)
    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)
    def add_work(self):
        rows = self.tableWidget.rowCount()
        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        pressureZUMPF_question_QCombo = self.tabWidget.currentWidget().pressureZUMPF_question_QCombo.currentText()
        if pressureZUMPF_question_QCombo == 'Да':
            paker_depth_zumpf = int(float(self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()))
        else:
            paker_depth_zumpf = 0
        self.need_privyazka_QCombo = self.tabWidget.currentWidget().need_privyazka_QCombo.currentText()

        if rows == 0:
            mes = QMessageBox.warning(self, 'ОШИБКА', 'Нужно добавить интервалы')
            return
        elif rows == 1:
            for row in range(rows):

                paker_depth = self.tableWidget.item(row, 1)
                paker_depth = int(float(paker_depth.text()))



            work_list = OpressovkaEK.paker_list(self, diametr_paker, paker_khost, paker_depth,
                                            pressureZUMPF_question_QCombo, paker_depth_zumpf)
        else:
            depth_paker_list = []
            for row in range(rows):
                paker_depth = self.tableWidget.item(row, 1)
                depth_paker_list.append(int(float(paker_depth.text())))
                pressureZUMPF_question = self.tableWidget.item(row, 2)
            work_list = OpressovkaEK.interval_pressure_testing(self, paker_khost, diametr_paker, depth_paker_list, pressureZUMPF_question, paker_depth_zumpf)

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    # Добавление строк с опрессовкой ЭК
    def select_combo_paker(self, paker_khost, paker_depth, paker_diametr):
        if well_data.column_additional is False or well_data.column_additional is True \
                and paker_depth < well_data.head_column_additional._value:

            paker_select = f'воронку + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм +' \
                           f' {OpressovkaEK.nkt_opress(self)[0]}'
            paker_short = f'в-у + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                          f' пакер ПРО-ЯМО-{paker_diametr}мм  +' \
                          f' {OpressovkaEK.nkt_opress(self)[0]}'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr}мм ' \
                           f'(либо аналог)  ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм  + {OpressovkaEK.nkt_opress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'в-у + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{paker_diametr}мм ' \
                          f' + {OpressovkaEK.nkt_opress(self)[0]} ' \
                          f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм  + {OpressovkaEK.nkt_opress(self)[0]}' \
                           f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'в-у + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{paker_diametr}мм + {OpressovkaEK.nkt_opress(self)[0]}' \
                          f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                          f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'

        nkt_opress_list = OpressovkaEK.nkt_opress(self)
        return paker_select, paker_short, nkt_opress_list

    def paker_list(self, paker_diametr, paker_khost, paker_depth, pressureZUMPF_question, paker_depth_zumpf = 0):

        paker_select, paker_short, nkt_opress_list = OpressovkaEK.select_combo_paker(self, paker_khost, paker_depth, paker_diametr)

        if pressureZUMPF_question == 'Да':
            paker_list = [
                [f'СПО {paker_short} до глубины {paker_depth_zumpf}', None,
                 f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {paker_depth_zumpf}м,'
                 f' воронкой до {paker_depth_zumpf + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth_zumpf, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {well_data.current_bottom}м на '
                 f'Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {well_data.current_bottom}м на '
                 f'Р={well_data.max_admissible_pressure._value}атм в течение 30 минут в присутствии представителя заказчика, '
                 f'составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'срыв пакера 30мин + 1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [f'Приподнять и посадить пакер на глубине {paker_depth}м',
                 None, f'Приподнять и посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
                 OpressovkaEK.testing_pressure(self, paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.67],
                [f'срыв пакера 30мин + 1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять {paker_select} на НКТ{well_data.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]

        else:
            paker_list = [
                [f'СПо {paker_short} до глубины {paker_depth}м', None,
                 f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {paker_depth}м, '
                 f'воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [None, None, f'Посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1],
                 None, OpressovkaEK.testing_pressure(self, paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.67],
                [f'cрыв пакера 30мин +1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять {paker_select} на НКТ{well_data.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]

        if self.need_privyazka_QCombo == "Да":
            paker_list.insert(1, privyazkaNKT(self)[0])

        return paker_list

    def addString(self):
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        if len(well_data.dict_leakiness) != 0:
            dict_leakinest_keys = sorted(list(well_data.dict_leakiness['НЭК']['интервал'].keys()), key=lambda x: x[0],
                                         reverse=False)

            leakness_list = [float(dict_leakinest_keys[0].split('-')[0]) - 10]

            for nek in list(dict_leakinest_keys):
                nek_bur = float(nek.split('-')[1]) + 10
                leakness_list.append(nek_bur)

                leakness_list.append(paker_depth)
        else:
            leakness_list = [paker_depth]
        for plast in well_data.plast_all:
            leakness_list.append(well_data.dict_perforation[plast]['кровля'] -10)
            leakness_list.append(well_data.dict_perforation[plast]['подошва'] + 10)
        rows = self.tableWidget.rowCount()
        current_bottom = well_data.current_bottom
        # print(drilling_interval)
        for sole in sorted(leakness_list):
            if paker_depth > sole:
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(''))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(1)

    def interval_pressure_testing(self, paker_khost, diametr_paker, depth_paker_list,
                                  pressureZUMPF_question, paker_depth_zumpf = 0):
        paker_depth = sorted(depth_paker_list)[0]
        paker_select, paker_short, nkt_opress_list = OpressovkaEK.select_combo_paker(self, paker_khost, paker_depth, diametr_paker)

        paker_list = [
            [f'Спо {paker_short} до глубины {paker_depth}м', None,
             f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {paker_depth}м, '
             f'воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nkt_opress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
             f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [None, None, f'Посадить пакер на глубине {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [OpressovkaEK.testing_pressure(self, paker_depth)[1],
             None, OpressovkaEK.testing_pressure(self, paker_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [f'cрыв пакера 30мин +1ч', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None]
        ]
        if well_data.leakiness:
            dict_leakinest_keys = sorted(list(well_data.dict_leakiness['НЭК']['интервал'].keys()), key=lambda x: float(x[0]),
                                         reverse=False)
        else:
            dict_leakinest_keys = []

        for plast in well_data.plast_all:
            dict_leakinest_keys.append(f'{well_data.dict_perforation[plast]["кровля"]}-{well_data.dict_perforation[plast]["подошва"]}')

        for ind_nek, pakerNEK in enumerate(depth_paker_list[1:]):
            nek_count = ''
            for nek in dict_leakinest_keys:
                if int(float(nek.split('-')[0])) < pakerNEK:
                    nek_count += f'{nek}, '
            for nek in dict_leakinest_keys:
                if int(float(nek.split('-')[0])) < pakerNEK:
                    nek_count += f'{nek}, '

            pressureNEK_list = [
                [f'При герметичности колонны:  Допустить пакер до глубины {paker_depth}м', None,
                 f'При герметичности колонны:  Допустить пакер до глубины {pakerNEK}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(pakerNEK -paker_depth, 1.2)],
                [f'Опрессовать в инт 0-{pakerNEK}м на Р={well_data.max_admissible_pressure._value}атм', None,
                 f'{nkt_opress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в '
                 f'интервале {pakerNEK}-0м на Р={well_data.max_admissible_pressure._value}атм'
                 f' в течение 30 минут в присутствии представителя заказчика, составить акт.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'Насыщение 5м3. Определение Q при Р-{well_data.max_admissible_pressure._value}', None,
                 f'ПРИ НЕГЕРМЕТИЧНОСТИ: \nПроизвести насыщение скважины в объеме 5м3 по '
                 f'затрубному пространству. Определить приемистость '
                 f'НЭК {nek_count[:-2]} при Р-{well_data.max_admissible_pressure._value}'
                 f'атм по затрубному пространству'
                 f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль '
                 f'за отдачей жидкости '
                 f'после закачки, объем согласовать с подрядчиком по РИР).',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.5],
                [f'срыв пакера 30мин', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса '
                 f'НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7]]

            for row in pressureNEK_list:
                paker_list.append(row)
            paker_depth = pakerNEK

        if pressureZUMPF_question == "Да":
            zumpf_list = [
                [f'Допустить пакер до глубины {paker_depth_zumpf}м', None,
                 f'Допустить пакер до глубины {paker_depth_zumpf}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {well_data.current_bottom}м на '
                 f'Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {well_data.current_bottom}м на '
                 f'Р={well_data.max_admissible_pressure._value}атм в течение 30 минут в присутствии представителя заказчика, '
                 f'составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'срыв пакера 30мин + 1ч', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'Поднять {paker_select} на НКТ{well_data.nkt_diam} c глубины '
                 f'{paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                 f'{well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]
            ]
        else:
            zumpf_list = [[None, None,
             f'Поднять {paker_select} на НКТ{well_data.nkt_diam} c глубины '
             f'{paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
             f'{well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]
            ]
        for row in zumpf_list:
            paker_list.append(row)

        if self.need_privyazka_QCombo == "Да":
            paker_list.insert(1, privyazkaNKT(self)[0])

        return paker_list





    def nkt_opress(self):

        if well_data.nkt_opressTrue is False:
            well_data.nkt_opressTrue is True
            return 'НКТ + опрессовочное седло', 'Опрессовать НКТ на 200атм. Вымыть шар'
        else:
            return 'НКТ', ''

    # функция проверки спуска пакера выше прошаблонированной колонны
    def check_for_template_paker(self, depth):

        check_true = False
        # print(f' глубина шаблона {well_data.template_depth}, посадка пакера {depth}')
        while check_true is False:
            if depth < float(
                    well_data.head_column_additional._value) and depth <= well_data.template_depth and well_data.column_additional:
                check_true = True
            elif depth > float(
                    well_data.head_column_additional._value) and depth <= well_data.template_depth_addition and well_data.column_additional:
                check_true = True
            elif depth <= well_data.template_depth and well_data.column_additional is False:
                check_true = True

            if check_true is False:

                false_template = QMessageBox.question(None, 'Проверка глубины пакера',
                                                      f'Проверка показала посадка пакера {depth}м '
                                                      f'опускается ниже глубины шаблонирования ЭК '
                                                      f'{well_data.template_depth}м'
                                                      f'изменить глубину ?')

        return check_true

    def testing_pressure(self, depth):


        interval_list = []

        for plast in well_data.plast_all:
            if well_data.dict_perforation[plast]['отключение'] is False:
                for interval in well_data.dict_perforation[plast]['интервал']:
                    if interval[0] < well_data.current_bottom:
                        interval_list.append(interval)

        if well_data.leakiness is True:
            for nek in well_data.dict_leakiness['НЭК']['интервал']:
                if well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение'] is False and float(nek.split('-')[0]) < depth:
                    interval_list.append(list(map(float, nek.split('-'))))

        if any([float(interval[1]) < float(depth) for interval in interval_list]):
            check_true = True
            testing_pressure_str = f'Закачкой тех жидкости в затрубное пространство при Р=' \
                                   f'{well_data.max_admissible_pressure._value}атм' \
                                   f' удостоверить в отсутствии выхода тех жидкости и герметичности пакера, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Закачкой в затруб при Р=' \
                                     f'{well_data.max_admissible_pressure._value}атм' \
                                     f' удостоверить в герметичности пакера'
        else:
            check_true = False
            testing_pressure_str = f'Опрессовать эксплуатационную колонну в интервале {depth}-0м на ' \
                                   f'Р={well_data.max_admissible_pressure._value}атм' \
                                   f' в течение 30 минут в присутствии представителя заказчика, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Опрессовать в {depth}-0м на Р={well_data.max_admissible_pressure._value}атм'

        return testing_pressure_str, testing_pressure_short, check_true












