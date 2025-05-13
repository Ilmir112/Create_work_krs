from PyQt5.QtGui import QDoubleValidator

import data_list

from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QPushButton, QHeaderView, QTableWidget, QTableWidgetItem


from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm


class TabPageSo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.validator = QDoubleValidator(0.0, 80000.0, 2)
        self.view_paker_work()


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Опрессовка')


class OpressovkaEK(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.tableWidget = QTableWidget(0, 1)
        self.tableWidget.setHorizontalHeaderLabels(
            ["посадка пакера"])
        for i in range(1):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work)
        self.buttonadd_string = QPushButton('Поинтервальная опрессовка')
        self.buttonadd_string.clicked.connect(self.add_string)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)

        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonadd_string, 3, 1)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def add_row_table(self):

        self.current_widget = self.tab_widget.currentWidget()

        paker_khost = int(float(self.current_widget.paker_khost_edit.text()))
        paker_depth = int(float(self.current_widget.paker_depth_edit.text()))
        pressure_zumpf_combo = self.current_widget.pressure_zumpf_question_combo.currentText()
        if not paker_khost or not paker_depth:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return

        if pressure_zumpf_combo == 'Да':
            paker_depth_zumpf = self.current_widget.paker_depth_zumpf_edit.text()
            if paker_depth_zumpf != '':
                paker_depth_zumpf = int(float(paker_depth_zumpf))
            if self.check_true_depth_template(paker_depth_zumpf) is False:
                return
            if self.check_depth_paker_in_perforation(paker_depth_zumpf) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth_zumpf) is False:
                return

        else:
            paker_depth_zumpf = 0

        if int(paker_khost) + int(paker_depth) > self.data_well.current_bottom and pressure_zumpf_combo == 'Нет' \
                or int(paker_khost) + int(
            paker_depth_zumpf) > self.data_well.current_bottom and pressure_zumpf_combo == 'Да':
            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                             f'ниже текущего забоя')
            return
        if self.check_true_depth_template(paker_depth) is False:
            return
        if self.check_depth_paker_in_perforation(paker_depth) is False:
            return
        if self.check_depth_in_skm_interval(paker_depth) is False:
            return
        item_roof = self.find_item_in_table(int(paker_depth))

        if item_roof is None:
            rows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rows)
            # self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(paker_depth)))

            self.tableWidget.setSortingEnabled(False)

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def add_work(self):
        rows = self.tableWidget.rowCount()
        paker_khost = int(float(self.tab_widget.currentWidget().paker_khost_edit.text()))
        diameter_paker = int(float(self.tab_widget.currentWidget().diameter_paker_edit.text()))
        pressure_zumpf_question_combo = self.tab_widget.currentWidget().pressure_zumpf_question_combo.currentText()
        if pressure_zumpf_question_combo == 'Да':
            paker_depth_zumpf = int(float(self.tab_widget.currentWidget().paker_depth_zumpf_edit.text()))
            if paker_khost + paker_depth_zumpf >= self.data_well.current_bottom:
                QMessageBox.warning(self, 'ОШИБКА', 'Длина хвостовика и пакера ниже текущего забоя')
                return
        else:
            paker_depth_zumpf = 0

        self.need_privyazka_q_combo = self.tab_widget.currentWidget().need_privyazka_q_combo.currentText()

        if rows == 0:
            QMessageBox.warning(self, 'ОШИБКА', 'Нужно добавить интервалы')
            return
        elif rows == 1:
            for row in range(rows):
                paker_depth = self.tableWidget.item(row, 0)
                paker_depth = int(float(paker_depth.text()))

            work_list = self.paker_list(diameter_paker, paker_khost, paker_depth,
                                                pressure_zumpf_question_combo, paker_depth_zumpf)
        else:
            depth_paker_list = []
            for row in range(rows):

                paker_depth = float(self.tableWidget.item(row, 0).text().replace(',', '.'))
                depth_paker_list.append(int(float(paker_depth)))

                if int(paker_khost) + int(paker_depth) > self.data_well.current_bottom and pressure_zumpf_question_combo == 'Нет' \
                        or int(paker_khost) + int(paker_depth_zumpf) > self.data_well.current_bottom and pressure_zumpf_question_combo == 'Да':
                    QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                     f'ниже текущего забоя')
                    return

                if self.check_true_depth_template(paker_depth) is False:
                    return
                if self.check_depth_paker_in_perforation(paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth) is False:
                    return

            work_list = self.interval_pressure_testing(paker_khost, diameter_paker,
                                                               depth_paker_list, pressure_zumpf_question_combo,
                                                               paker_depth_zumpf)

        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    # Добавление строк с опрессовкой ЭК


    def paker_list(self, paker_diameter, paker_khost, paker_depth, pressure_zumpf_question, paker_depth_zumpf=0):

        paker_select, paker_short, nkt_opress_list = self.select_combo_paker(paker_khost, paker_depth,
                                                                                     paker_diameter)

        if pressure_zumpf_question == 'Да':
            paker_list = [
                [f'СПО {paker_short} до глубины {paker_depth_zumpf}', None,
                 f'Спустить {paker_select} на НКТ{self.data_well.nkt_diam}мм до глубины {paker_depth_zumpf}м,'
                 f' воронкой до {paker_depth_zumpf + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth_zumpf, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм в течение 30 минут в присутствии '
                 f'представителя заказчика, '
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
                 f'Поднять {paker_select} на НКТ{self.data_well.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', lifting_nkt_norm(paker_depth, 1.2)]]

        else:
            paker_list = [
                [f'СПо {paker_short} до глубины {paker_depth}м', None,
                 f'Спустить {paker_select} на НКТ{self.data_well.nkt_diam}мм до глубины {paker_depth}м, '
                 f'воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. {nkt_opress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
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
                 f'Поднять {paker_select} на НКТ{self.data_well.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', lifting_nkt_norm(paker_depth, 1.2)]]

        if self.need_privyazka_q_combo == "Да":
            paker_list.insert(1, self.privyazka_nkt()[0])

        return paker_list

    def add_string(self):
        paker_depth = int(float(self.tab_widget.currentWidget().paker_depth_edit.text()))
        if len(self.data_well.dict_leakiness) != 0:
            dict_leakinest_keys = sorted(list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()),
                                         key=lambda x: x[0],
                                         reverse=False)

            leakness_list = [float(dict_leakinest_keys[0].split('-')[0]) - 10]

            for nek in list(dict_leakinest_keys):
                nek_bur = float(nek.split('-')[1]) + 10
                leakness_list.append(nek_bur)

                leakness_list.append(paker_depth)
        else:
            leakness_list = [paker_depth]

        for plast in self.data_well.plast_all:
            leakness_list.append(self.data_well.dict_perforation[plast]['кровля'] - 10)
            leakness_list.append(self.data_well.dict_perforation[plast]['подошва'] + 10)
        rows = self.tableWidget.rowCount()
        current_bottom = self.data_well.current_bottom
        # print(drilling_interval)
        for sole in sorted(leakness_list):
            if paker_depth >= sole and self.find_item_in_table(int(sole)) is None and current_bottom > sole:
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(sole))))
        self.tableWidget.setSortingEnabled(False)
        # self.tableWidget.sortItems(1)

    def interval_pressure_testing(self, paker_khost, diameter_paker, depth_paker_list,
                                  pressure_zumpf_question, paker_depth_zumpf=0):
        paker_depth = sorted(depth_paker_list)[0]
        paker_select, paker_short, nkt_opress_list = self.select_combo_paker(paker_khost, paker_depth,
                                                                                     diameter_paker)

        paker_list = [
            [f'Спо {paker_short} до глубины {paker_depth}м', None,
             f'Спустить {paker_select} на НКТ{self.data_well.nkt_diam}мм до глубины {paker_depth}м, '
             f'воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. {nkt_opress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
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
        if self.data_well.dict_leakiness:
            dict_leakinest_keys = sorted(list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()),
                                         key=lambda x: float(x[0]),
                                         reverse=False)
        else:
            dict_leakinest_keys = []
        plasts_keys = []

        depth_paker_list = sorted(depth_paker_list)
        for ind_nek, pakerNEK in enumerate(depth_paker_list):
            if paker_depth != pakerNEK:
                for plast in self.data_well.plast_all:
                    if f'{self.data_well.dict_perforation[plast]["кровля"]}-{self.data_well.dict_perforation[plast]["подошва"]}' not in plasts_keys:
                        plasts_keys.append(
                            f'{self.data_well.dict_perforation[plast]["кровля"]}-{self.data_well.dict_perforation[plast]["подошва"]}')

                    nek_count = ''
                    for nek in plasts_keys:
                        if f'инт. {nek}' not in nek_count:
                            if int(float(nek.split('-')[0])) < pakerNEK:
                                nek_count += f'инт. {nek}, '
                for nek in dict_leakinest_keys:
                    if f'НЭК {nek}' not in nek_count:
                        if int(float(nek.split('-')[0])) < pakerNEK:
                            nek_count += f'НЭК {nek}, '

                pressureNEK_list = [
                    [f'При герметичности колонны:  Допустить пакер до глубины {pakerNEK}м', None,
                     f'При герметичности колонны:  Допустить пакер до глубины {pakerNEK}м',
                     None, None, None, None, None, None, None,
                     'мастер КРС', descentNKT_norm(pakerNEK - paker_depth, 1.2)],
                    [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
                     OpressovkaEK.testing_pressure(self, paker_depth)[0],
                     None, None, None, None, None, None, None,
                     'мастер КРС', 0.77],
                    [f'Насыщение 5м3. Определение Q при Р-{self.data_well.max_admissible_pressure.get_value}', None,
                     f'ПРИ НЕГЕРМЕТИЧНОСТИ: \nПроизвести насыщение скважины в объеме 5м3 по '
                     f'затрубному пространству. Определить приемистость '
                     f'{nek_count} при Р-{self.data_well.max_admissible_pressure.get_value}'
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
                if pakerNEK == depth_paker_list[-1]:
                    pressureNEK_list[2] = [
                        None, None,
                        f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК '
                        f'для определения интервала '
                        f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                        f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                        f'Определить приемистость НЭК.',
                        None, None, None, None, None, None, None,
                        'мастер КРС', None]

                for row in pressureNEK_list:
                    paker_list.append(row)
                paker_depth = pakerNEK

        if pressure_zumpf_question == "Да":
            zumpf_list = [
                [f'Допустить пакер до глубины {paker_depth_zumpf}м', None,
                 f'Допустить пакер до глубины {paker_depth_zumpf}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.77],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм в течение 30 минут в присутствии представителя заказчика, '
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
                 f'Поднять {paker_select} на НКТ{self.data_well.nkt_diam} c глубины '
                 f'{paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                 f'{self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', lifting_nkt_norm(paker_depth, 1.2)]
            ]
        else:
            zumpf_list = [[None, None,
                           f'Поднять {paker_select} на НКТ{self.data_well.nkt_diam} c глубины '
                           f'{paker_depth}м с доливом скважины в '
                           f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                           f'{self.data_well.fluid_work}',
                           None, None, None, None, None, None, None,
                           'мастер КРС', lifting_nkt_norm(paker_depth, 1.2)]
                          ]
        for row in zumpf_list:
            paker_list.append(row)

        if self.need_privyazka_q_combo == "Да":
            paker_list.insert(1, self.privyazka_nkt()[0])

        return paker_list

    def nkt_opress(self):
        if self.data_well.nkt_opress_true is False:
            self.data_well.nkt_opress_true is True
            return 'НКТ + репер', ''
        else:
            return 'НКТ + репер', ''

    # функция проверки спуска пакера выше прошаблонированной колонны
    def check_for_template_paker(self, depth):

        check_true = False
        # print(f' глубина шаблона {self.data_well.template_depth}, посадка пакера {depth}')
        while check_true is False:
            if depth < float(
                    self.data_well.head_column_additional.get_value) and depth <= self.data_well.template_depth and self.data_well.column_additional:
                check_true = True
            elif depth > float(
                    self.data_well.head_column_additional.get_value) and depth <= self.data_well.template_depth_addition and self.data_well.column_additional:
                check_true = True
            elif depth <= self.data_well.template_depth and self.data_well.column_additional is False:
                check_true = True

            if check_true is False:
                false_template = QMessageBox.question(None, 'Проверка глубины пакера',
                                                      f'Проверка показала посадка пакера {depth}м '
                                                      f'опускается ниже глубины шаблонирования ЭК '
                                                      f'{self.data_well.template_depth}м'
                                                      f'изменить глубину ?')

        return check_true


