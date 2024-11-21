from PyQt5 import Qt
from PyQt5.QtGui import QDoubleValidator

import data_list
from main import MyMainWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QTabWidget, QPushButton, QHeaderView, QTableWidget, QTableWidgetItem

from work_py.alone_oreration import privyazka_nkt
from .parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from .rationingKRS import descentNKT_norm, liftingNKT_norm


class TabPageSo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__()

        self.dict_data_well = parent

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
        self.need_privyazka_q_combo = QComboBox()
        self.need_privyazka_q_combo.addItems(['Нет', 'Да'])

        if len(self.dict_data_well['plast_work']) != 0:
            pakerDepth = self.dict_data_well["perforation_roof"] - 20
        else:
            # print(self.dict_data_well["dict_perforation"])
            if self.dict_data_well["dict_leakiness"]:
                aaaaa = self.dict_data_well["dict_leakiness"]['НЭК']['интервал']
                pakerDepth = min([float(nek.split('-')[0]) - 10
                                       for nek in self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()])
        try:
            self.paker_depth_edit.setText(str(int(pakerDepth)))
        except:
            pass


        self.paker_depth_zumpf_Label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator)

        self.pressure_zumph_question_Label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressure_zumph_question_QCombo = QComboBox(self)
        self.pressure_zumph_question_QCombo.currentTextChanged.connect(self.update_paker_need)

        self.pressure_zumph_question_QCombo.addItems(['Нет', 'Да'])

        self.grid_layout = QGridLayout(self)

        self.grid_layout.addWidget(self.diametr_paker_labelType, 3, 1)
        self.grid_layout.addWidget(self.diametr_paker_edit, 4, 1)

        self.grid_layout.addWidget(self.paker_khost_Label, 3, 2)
        self.grid_layout.addWidget(self.paker_khost_edit, 4, 2)

        self.grid_layout.addWidget(self.paker_depth_Label, 3, 3)
        self.grid_layout.addWidget(self.paker_depth_edit, 4, 3)

        self.grid_layout.addWidget(self.pressure_zumph_question_Label, 3, 5)
        self.grid_layout.addWidget(self.pressure_zumph_question_QCombo, 4, 5)

        self.grid_layout.addWidget(self.need_privyazka_Label, 3, 4)
        self.grid_layout.addWidget(self.need_privyazka_q_combo, 4, 4)

    def update_paker_need(self, index):
        if index == 'Да':
            if len(self.dict_data_well['plast_work']) != 0:
                paker_depth_zumpf = int(self.dict_data_well["perforation_roof"] + 10)
            else:
                if self.dict_data_well["dict_leakiness"]:
                    paker_depth_zumpf = int(max([float(nek.split('-')[0])+10
                                           for nek in self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()]))

            self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid_layout.addWidget(self.paker_depth_zumpf_Label, 3, 6)
            self.grid_layout.addWidget(self.paker_depth_zumpf_edit, 4, 6)
        elif index == 'Нет':
            self.paker_depth_zumpf_Label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)

    def update_paker(self):
        paker_depth = self.paker_depth_edit.text()
        if paker_depth != '':
            if self.dict_data_well["open_trunk_well"] is True:

                paker_khost = self.dict_data_well["current_bottom"] - int(paker_depth)
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{self.paker_diametr_select(int(paker_depth))}')
            else:
                paker_khost = 10
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{self.paker_diametr_select(int(paker_depth))}')
            need_count = 0
            for plast in self.dict_data_well["plast_all"]:
                for roof, sole in self.dict_data_well["dict_perforation"][plast]['интервал']:
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth))< 10:
                        need_count += 1
            if self.dict_data_well["dict_leakiness"]:
                a = self.dict_data_well["dict_leakiness"]
                for interval in self.dict_data_well["dict_leakiness"]['НЭК']['интервал']:
                    roof, sole = interval.split('-')
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth)) < 10:
                        need_count += 1

            if need_count == 0:
                self.need_privyazka_q_combo.setCurrentIndex(0)
            else:
                self.need_privyazka_q_combo.setCurrentIndex(1)


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

        if self.dict_data_well["column_additional"] is False or (
                self.dict_data_well["column_additional"] is True and int(depth_landing) <= self.dict_data_well["head_column_additional"]._value):
            diam_internal_ek = self.dict_data_well["column_diametr"]._value - 2 * self.dict_data_well["column_wall_thickness"]._value
        else:
            diam_internal_ek = self.dict_data_well["column_additional_diametr"]._value - \
                               2 * self.dict_data_well["column_additional_wall_thickness"]._value

        for diam, diam_internal_paker in paker_diam_dict.items():
            if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                paker_diametr = diam

        return paker_diametr


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Опрессовка')


class OpressovkaEK(WindowUnion):
    def __init__(self, dict_data_well, table_widget, parent=None):
        super().__init__()

        self.dict_data_well = dict_data_well
        self.ins_ind = dict_data_well['ins_ind']
        self.tabWidget = TabWidget(self.dict_data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

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

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия
    def add_row_table(self):

        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        pressureZUMPF_combo = self.tabWidget.currentWidget().pressure_zumph_question_QCombo.currentText()
        if not paker_khost or not paker_depth:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return


        if pressureZUMPF_combo == 'Да':
            paker_depth_zumpf = self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()
            if paker_depth_zumpf != '':
                paker_depth_zumpf = int(float(paker_depth_zumpf))
            if self.check_true_depth_template(paker_depth_zumpf) is False:
                return
            if self.true_set_paker( paker_depth_zumpf) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth_zumpf) is False:
                return

        else:
            paker_depth_zumpf = 0

        if int(paker_khost) + int(paker_depth) > self.dict_data_well["current_bottom"] and pressureZUMPF_combo == 'Нет' \
                or int(paker_khost) + int(
            paker_depth_zumpf) > self.dict_data_well["current_bottom"] and pressureZUMPF_combo == 'Да':
            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        if self.check_true_depth_template(paker_depth) is False:
            return
        if self.true_set_paker(paker_depth) is False:
            return
        if self.check_depth_in_skm_interval(paker_depth) is False:
            return


        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(paker_khost)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_depth)))


        self.tableWidget.setSortingEnabled(False)
    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)
    def add_work(self):
        rows = self.tableWidget.rowCount()
        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        pressure_zumph_question_QCombo = self.tabWidget.currentWidget().pressure_zumph_question_QCombo.currentText()
        if pressure_zumph_question_QCombo == 'Да':
            paker_depth_zumpf = int(float(self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()))
            if paker_khost + paker_depth_zumpf >= self.dict_data_well["current_bottom"]:
                QMessageBox.warning(self, 'ОШИБКА', 'Длина хвостовика и пакера ниже текущего забоя')
                return

        else:
            paker_depth_zumpf = 0
        self.need_privyazka_q_combo = self.tabWidget.currentWidget().need_privyazka_q_combo.currentText()

        if rows == 0:
            QMessageBox.warning(self, 'ОШИБКА', 'Нужно добавить интервалы')
            return
        elif rows == 1:
            for row in range(rows):
                paker_depth = self.tableWidget.item(row, 1)
                paker_depth = int(float(paker_depth.text()))


            work_list = OpressovkaEK.paker_list(self, diametr_paker, paker_khost, paker_depth,
                                            pressure_zumph_question_QCombo, paker_depth_zumpf)
        else:
            depth_paker_list = []
            for row in range(rows):
                paker_depth = self.tableWidget.item(row, 1)
                depth_paker_list.append(int(float(paker_depth.text())))
                pressure_zumph_question = self.tableWidget.item(row, 2)
            work_list = OpressovkaEK.interval_pressure_testing(self, paker_khost, diametr_paker, depth_paker_list, pressure_zumph_question, paker_depth_zumpf)

        self.populate_row(self.ins_ind, work_list, self.table_widget)
        data_list.pause = False
        self.close()

    # Добавление строк с опрессовкой ЭК
    def select_combo_paker(self, paker_khost, paker_depth, paker_diametr):
        if self.dict_data_well["column_additional"] is False or self.dict_data_well["column_additional"] is True \
                and paker_depth < self.dict_data_well["head_column_additional"]._value:

            paker_select = f'воронку + НКТ{self.dict_data_well["nkt_diam"]}мм {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {self.dict_data_well["column_diametr"]._value}мм х {self.dict_data_well["column_wall_thickness"]._value}мм +' \
                           f' {OpressovkaEK.nkt_opress(self)[0]}'
            paker_short = f'в-у + НКТ{self.dict_data_well["nkt_diam"]}мм {paker_khost}м +' \
                          f' пакер ПРО-ЯМО-{paker_diametr}мм  +' \
                          f' {OpressovkaEK.nkt_opress(self)[0]}'
        elif self.dict_data_well["column_additional"] is True and self.dict_data_well["column_additional_diametr"]._value < 110 and \
                paker_depth > self.dict_data_well["head_column_additional"]._value:
            paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr}мм ' \
                           f'(либо аналог)  ' \
                           f'для ЭК {self.dict_data_well["column_additional_diametr"]._value}мм х ' \
                           f'{self.dict_data_well["column_additional_wall_thickness"]._value}мм  + {OpressovkaEK.nkt_opress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth - self.dict_data_well["head_column_additional"]._value, 0)}м'
            paker_short = f'в-у + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{paker_diametr}мм ' \
                          f' + {OpressovkaEK.nkt_opress(self)[0]} ' \
                          f'+ НКТ60мм L- {round(paker_depth - self.dict_data_well["head_column_additional"]._value, 0)}м'
        elif self.dict_data_well["column_additional"] is True and self.dict_data_well["column_additional_diametr"]._value > 110 and \
                paker_depth > self.dict_data_well["head_column_additional"]._value:
            paker_select = f'воронку + НКТ{self.dict_data_well["nkt_diam"]}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {self.dict_data_well["column_additional_diametr"]._value}мм х ' \
                           f'{self.dict_data_well["column_additional_wall_thickness"]._value}мм  + {OpressovkaEK.nkt_opress(self)[0]}' \
                           f'+ НКТ{self.dict_data_well["nkt_diam"]}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - self.dict_data_well["head_column_additional"]._value, 0)}м'
            paker_short = f'в-у + НКТ{self.dict_data_well["nkt_diam"]}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{paker_diametr}мм + {OpressovkaEK.nkt_opress(self)[0]}' \
                          f'+ НКТ{self.dict_data_well["nkt_diam"]}мм со снятыми фасками L- ' \
                          f'{round(paker_depth - self.dict_data_well["head_column_additional"]._value, 0)}м'

        nkt_opress_list = OpressovkaEK.nkt_opress(self)
        return paker_select, paker_short, nkt_opress_list

    def paker_list(self, paker_diametr, paker_khost, paker_depth, pressure_zumph_question, paker_depth_zumpf = 0):

        paker_select, paker_short, nkt_opress_list = OpressovkaEK.select_combo_paker(self, paker_khost, paker_depth, paker_diametr)

        if pressure_zumph_question == 'Да':
            paker_list = [
                [f'СПО {paker_short} до глубины {paker_depth_zumpf}', None,
                 f'Спустить {paker_select} на НКТ{self.dict_data_well["nkt_diam"]}мм до глубины {paker_depth_zumpf}м,'
                 f' воронкой до {paker_depth_zumpf + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if self.dict_data_well["column_additional"] is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth_zumpf, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.dict_data_well["current_bottom"]}м на '
                 f'Р={self.dict_data_well["max_admissible_pressure"]._value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {self.dict_data_well["current_bottom"]}м на '
                 f'Р={self.dict_data_well["max_admissible_pressure"]._value}атм в течение 30 минут в присутствии представителя заказчика, '
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
                 f'Поднять {paker_select} на НКТ{self.dict_data_well["nkt_diam"]}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {self.dict_data_well["fluid_work"]}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]

        else:
            paker_list = [
                [f'СПо {paker_short} до глубины {paker_depth}м', None,
                 f'Спустить {paker_select} на НКТ{self.dict_data_well["nkt_diam"]}мм до глубины {paker_depth}м, '
                 f'воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if self.dict_data_well["column_additional"] is False else "")} '
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
                 f'Поднять {paker_select} на НКТ{self.dict_data_well["nkt_diam"]}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {self.dict_data_well["fluid_work"]}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]

        if self.need_privyazka_q_combo == "Да":
            paker_list.insert(1, privyazka_nkt(self)[0])

        return paker_list

    def addString(self):
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        if len(self.dict_data_well["dict_leakiness"]) != 0:
            dict_leakinest_keys = sorted(list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()), key=lambda x: x[0],
                                         reverse=False)

            leakness_list = [float(dict_leakinest_keys[0].split('-')[0]) - 10]

            for nek in list(dict_leakinest_keys):
                nek_bur = float(nek.split('-')[1]) + 10
                leakness_list.append(nek_bur)

                leakness_list.append(paker_depth)
        else:
            leakness_list = [paker_depth]
        for plast in self.dict_data_well["plast_all"]:
            leakness_list.append(self.dict_data_well["dict_perforation"][plast]['кровля'] -10)
            leakness_list.append(self.dict_data_well["dict_perforation"][plast]['подошва'] + 10)
        rows = self.tableWidget.rowCount()
        current_bottom = self.dict_data_well["current_bottom"]
        # print(drilling_interval)
        for sole in sorted(leakness_list):
            if paker_depth > sole:
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(''))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(1)

    def interval_pressure_testing(self, paker_khost, diametr_paker, depth_paker_list,
                                  pressure_zumph_question, paker_depth_zumpf = 0):
        paker_depth = sorted(depth_paker_list)[0]
        paker_select, paker_short, nkt_opress_list = OpressovkaEK.select_combo_paker(self, paker_khost, paker_depth, diametr_paker)

        paker_list = [
            [f'Спо {paker_short} до глубины {paker_depth}м', None,
             f'Спустить {paker_select} на НКТ{self.dict_data_well["nkt_diam"]}мм до глубины {paker_depth}м, '
             f'воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. {nkt_opress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if self.dict_data_well["column_additional"] is False else "")} '
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
        if self.dict_data_well["dict_leakiness"]:
            dict_leakinest_keys = sorted(list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()), key=lambda x: float(x[0]),
                                         reverse=False)
        else:
            dict_leakinest_keys = []

        for plast in self.dict_data_well["plast_all"]:
            dict_leakinest_keys.append(f'{self.dict_data_well["dict_perforation"][plast]["кровля"]}-{self.dict_data_well["dict_perforation"][plast]["подошва"]}')

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
                [f'Опрессовать в инт 0-{pakerNEK}м на Р={self.dict_data_well["max_admissible_pressure"]._value}атм', None,
                 f'{nkt_opress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в '
                 f'интервале {pakerNEK}-0м на Р={self.dict_data_well["max_admissible_pressure"]._value}атм'
                 f' в течение 30 минут в присутствии представителя заказчика, составить акт.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'Насыщение 5м3. Определение Q при Р-{self.dict_data_well["max_admissible_pressure"]._value}', None,
                 f'ПРИ НЕГЕРМЕТИЧНОСТИ: \nПроизвести насыщение скважины в объеме 5м3 по '
                 f'затрубному пространству. Определить приемистость '
                 f'НЭК {nek_count[:-2]} при Р-{self.dict_data_well["max_admissible_pressure"]._value}'
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

        if pressure_zumph_question == "Да":
            zumpf_list = [
                [f'Допустить пакер до глубины {paker_depth_zumpf}м', None,
                 f'Допустить пакер до глубины {paker_depth_zumpf}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.dict_data_well["current_bottom"]}м на '
                 f'Р={self.dict_data_well["max_admissible_pressure"]._value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {self.dict_data_well["current_bottom"]}м на '
                 f'Р={self.dict_data_well["max_admissible_pressure"]._value}атм в течение 30 минут в присутствии представителя заказчика, '
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
                 f'Поднять {paker_select} на НКТ{self.dict_data_well["nkt_diam"]} c глубины '
                 f'{paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                 f'{self.dict_data_well["fluid_work"]}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]
            ]
        else:
            zumpf_list = [[None, None,
             f'Поднять {paker_select} на НКТ{self.dict_data_well["nkt_diam"]} c глубины '
             f'{paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
             f'{self.dict_data_well["fluid_work"]}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]
            ]
        for row in zumpf_list:
            paker_list.append(row)

        if self.need_privyazka_q_combo == "Да":
            paker_list.insert(1, privyazka_nkt(self)[0])

        return paker_list





    def nkt_opress(self):

        if self.dict_data_well["nkt_opress_true"] is False:
            self.dict_data_well["nkt_opress_true"] is True
            return 'НКТ + опрессовочное седло', 'Опрессовать НКТ на 200атм. Вымыть шар'
        else:
            return 'НКТ', ''

    # функция проверки спуска пакера выше прошаблонированной колонны
    def check_for_template_paker(self, depth):

        check_true = False
        # print(f' глубина шаблона {self.dict_data_well["template_depth"]}, посадка пакера {depth}')
        while check_true is False:
            if depth < float(
                    self.dict_data_well["head_column_additional"]._value) and depth <= self.dict_data_well["template_depth"] and self.dict_data_well["column_additional"]:
                check_true = True
            elif depth > float(
                    self.dict_data_well["head_column_additional"]._value) and depth <= self.dict_data_well["template_depth_addition"] and self.dict_data_well["column_additional"]:
                check_true = True
            elif depth <= self.dict_data_well["template_depth"] and self.dict_data_well["column_additional"] is False:
                check_true = True

            if check_true is False:

                false_template = QMessageBox.question(None, 'Проверка глубины пакера',
                                                      f'Проверка показала посадка пакера {depth}м '
                                                      f'опускается ниже глубины шаблонирования ЭК '
                                                      f'{self.dict_data_well["template_depth"]}м'
                                                      f'изменить глубину ?')

        return check_true

    def testing_pressure(self, depth):


        interval_list = []

        for plast in self.dict_data_well["plast_all"]:
            if self.dict_data_well["dict_perforation"][plast]['отключение'] is False:
                for interval in self.dict_data_well["dict_perforation"][plast]['интервал']:
                    if interval[0] < self.dict_data_well["current_bottom"]:
                        interval_list.append(interval)

        if self.dict_data_well["leakiness"] is True:
            for nek in self.dict_data_well["dict_leakiness"]['НЭК']['интервал']:
                if self.dict_data_well["dict_leakiness"]['НЭК']['интервал'][nek]['отключение'] is False and float(nek.split('-')[0]) < depth:
                    interval_list.append(list(map(float, nek.split('-'))))

        if any([float(interval[1]) < float(depth) for interval in interval_list]):
            check_true = True
            testing_pressure_str = f'Закачкой тех жидкости в затрубное пространство при Р=' \
                                   f'{self.dict_data_well["max_admissible_pressure"]._value}атм' \
                                   f' удостоверить в отсутствии выхода тех жидкости и герметичности пакера, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Закачкой в затруб при Р=' \
                                     f'{self.dict_data_well["max_admissible_pressure"]._value}атм' \
                                     f' удостоверить в герметичности пакера'
        else:
            check_true = False
            testing_pressure_str = f'Опрессовать эксплуатационную колонну в интервале {depth}-0м на ' \
                                   f'Р={self.dict_data_well["max_admissible_pressure"]._value}атм' \
                                   f' в течение 30 минут в присутствии представителя заказчика, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Опрессовать в {depth}-0м на Р={self.dict_data_well["max_admissible_pressure"]._value}атм'

        return testing_pressure_str, testing_pressure_short, check_true












