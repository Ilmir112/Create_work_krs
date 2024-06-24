from PyQt5.QtGui import QDoubleValidator

import well_data
from main import MyWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QTabWidget, QPushButton

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


        self.pakerDepthZumpf_Label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.pakerDepthZumpf_edit = QLineEdit(self)
        self.pakerDepthZumpf_edit.setValidator(self.validator)

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
                pakerDepthZumpf = int(well_data.perforation_sole + 10)
            else:
                if well_data.leakiness:
                    pakerDepthZumpf = int(max([float(nek.split('-')[0])+10
                                           for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()]))

                    self.pakerDepthZumpf_edit.setText(f'{pakerDepthZumpf}')

            self.grid_layout.addWidget(self.pakerDepthZumpf_Label, 3, 6)
            self.grid_layout.addWidget(self.pakerDepthZumpf_edit, 4, 6)
        elif index == 'Нет':
            self.pakerDepthZumpf_Label.setParent(None)
            self.pakerDepthZumpf_edit.setParent(None)

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
                for roof, sole in well_data.dict_leakiness['НЭК']['интервал']:
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth)) < 10:
                        need_count += 1

            if need_count == 0:
                self.need_privyazka_QCombo.setCurrentIndex(0)
            else:
                self.need_privyazka_QCombo.setCurrentIndex(1)


    def paker_diametr_select(self, depth_landing):
        paker_diam_dict = {
            82: (88, 92),
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

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)


    def add_work(self):

        pressureZUMPF_question = self.tabWidget.currentWidget().pressureZUMPF_question_QCombo.currentText()

        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        self.need_privyazka_QCombo = self.tabWidget.currentWidget().need_privyazka_QCombo.currentText()
        try:
            pakerDepthZumpf = int(float(self.tabWidget.currentWidget().pakerDepthZumpf_edit.text()))
            if MyWindow.check_true_depth_template(self, paker_depth) is False:
                return
            if MyWindow.true_set_Paker(self, paker_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
                return


        except:
            pakerDepthZumpf = 0

        if int(paker_khost) + int(paker_depth) > well_data.current_bottom and pressureZUMPF_question == 'Нет' \
                or int(paker_khost) + int(pakerDepthZumpf) > well_data.current_bottom and pressureZUMPF_question == 'Да':
            mes = QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        if MyWindow.check_true_depth_template(self, paker_depth) is False:
            return
        if MyWindow.true_set_Paker(self, paker_depth) is False:
            return
        if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
            return


        work_list = OpressovkaEK.paker_list(self, diametr_paker, paker_khost, paker_depth, pakerDepthZumpf,
                                            pressureZUMPF_question)
        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    # Добавление строк с опрессовкой ЭК
    def paker_list(self, paker_diametr, paker_khost, paker_depth, pakerDepthZumpf, pressureZUMPF_question):

        if well_data.column_additional is False or well_data.column_additional is True \
                and paker_depth < well_data.head_column_additional._value:

            paker_select = f'воронку + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм +' \
                           f' {OpressovkaEK.nktOpress(self)[0]}'
            paker_short = f'в-у + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                          f' пакер ПРО-ЯМО-{paker_diametr}мм  +' \
                          f' {OpressovkaEK.nktOpress(self)[0]}'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr}мм ' \
                           f'(либо аналог)  ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм  + {OpressovkaEK.nktOpress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'в-у + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{paker_diametr}мм ' \
                          f' + {OpressovkaEK.nktOpress(self)[0]} ' \
                          f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм  + {OpressovkaEK.nktOpress(self)[0]}' \
                           f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'в-у + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{paker_diametr}мм + {OpressovkaEK.nktOpress(self)[0]}' \
                          f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                          f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'

        nktOpress_list = OpressovkaEK.nktOpress(self)

        if pressureZUMPF_question == 'Да':
            paker_list = [
                [f'СПО {paker_short} до глубины {pakerDepthZumpf}', None,
                 f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {pakerDepthZumpf}м,'
                 f' воронкой до {pakerDepthZumpf + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nktOpress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(pakerDepthZumpf, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {pakerDepthZumpf} - {well_data.current_bottom}м на '
                 f'Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {pakerDepthZumpf} - {well_data.current_bottom}м на '
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
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nktOpress_list[1]} '
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

        if len(well_data.dict_leakiness) != 0:
            dict_leakinest_keys = sorted(list(well_data.dict_leakiness['НЭК']['интервал'].keys()), key=lambda x: x[0], reverse=True)
            if int(dict_leakinest_keys[0][0]) < paker_depth:

                NEK_question = QMessageBox.question(self, 'Поинтервальная опрессовка НЭК',
                                                    'Нужна ли поинтервальная опрессовка НЭК?')
                if NEK_question == QMessageBox.StandardButton.Yes:

                    pakerNEK, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                       'Введите глубину посадки пакера для под НЭК',
                                                       int(float(dict_leakinest_keys[0].split('-')[0])) - 10, 0,
                                                       int(well_data.current_bottom))

                    nek1 = "-".join(map(str, list(dict_leakinest_keys)))
                    paker_list = [
                        [f'СПО {paker_short} до глубины {pakerNEK}', None,
                         f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {pakerNEK}м, воронкой '
                         f'до {pakerNEK + paker_khost}м'
                         f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nktOpress_list[1]}'
                         f' {("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
                         f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО'
                         f' КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                         None, None, None, None, None, None, None,
                         'мастер КРС', descentNKT_norm(pakerNEK, 1.2)],
                        [f'Посадить пакер на глубине {pakerNEK}м', None, f'Посадить пакер на глубине {pakerNEK}м',
                         None, None, None, None, None, None, None,
                         'мастер КРС', 0.4],
                        [f'Опрессовать ЭК в инт {pakerNEK}-0м на '
                         f'Р={well_data.max_admissible_pressure._value}атм', None,
                         f'Опрессовать эксплуатационную колонну в интервале {pakerNEK}-0м на '
                         f'Р={well_data.max_admissible_pressure._value}атм'
                         f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
                         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                         f'часа до начала работ)',
                         None, None, None, None, None, None, None,
                         'мастер КРС, предст. заказчика', 0.67],
                        [None, None,
                         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения '
                         f'интервала негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, '
                         f'ВЧТ с целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                         f'Определить приемистость НЭК.',
                         None, None, None, None, None, None, None,
                         'мастер КРС', None],
                        [f'Опрессовать  в инт 0-{int(dict_leakinest_keys[0][1]) + 10}м на '
                         f'Р={well_data.max_admissible_pressure._value}атм.', None,
                         f'Допустить пакер до глубины {pakerNEK + 20}м. '
                         f'Опрессовать эксплуатационную колонну в интервале {pakerNEK + 20}-0м на '
                         f'Р={well_data.max_admissible_pressure._value}атм'
                         f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
                         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                         f'часа до начала работ)',
                         None, None, None, None, None, None, None,
                         'мастер КРС, предст. заказчика', 0.67],
                        [f'Определение Q при Р-{well_data.max_admissible_pressure._value}атм',
                         None,
                         f'ПРИ НЕГЕРМЕТИЧНОСТИ: \nПроизвести насыщение скважины в объеме 5м3 по затрубному пространству. '
                         f'Определить приемистость '
                         f'НЭК {nek1}м при Р-{well_data.max_admissible_pressure._value}атм по '
                         f'затрубному пространству'
                         f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                         f'после закачки, объем согласовать с подрядчиком по РИР).',
                         None, None, None, None, None, None, None,
                         'мастер КРС', 1.5],
                        [f'срыв пакера 30мин', None,
                         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в'
                         f' течении 30мин и с выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                         None, None, None, None, None, None, None,
                         'мастер КРС', 0.7],
                    ]
                    ind_nek = 1
                    while len(dict_leakinest_keys) - ind_nek != 0:
                        # print('запуск While')
                        if paker_depth > int(dict_leakinest_keys[ind_nek][1]) + 10:
                            pakerNEK1, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                                'Введите глубину посадки пакера для под НЭК',
                                                                int(dict_leakinest_keys[ind_nek][1]) + 10, 0,
                                                                int(well_data.current_bottom))
                            pressureNEK_list = [
                                [f'При герметичности колонны:  Допустить'
                                 f' пакер до глубины {pakerNEK1}м', None,
                                 f'При герметичности колонны:  Допустить'
                                 f' пакер до глубины {pakerNEK1}м',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', descentNKT_norm(pakerNEK1 - pakerNEK, 1.2)],
                                [f'Опрессовать в '
                                 f'инт 0-{pakerNEK1}м на Р={well_data.max_admissible_pressure._value}атм',
                                 None,
                                 f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в '
                                 f'интервале 0-{pakerNEK1}м на Р={well_data.max_admissible_pressure._value}атм'
                                 f' в течение 30 минут в присутствии представителя заказчика, составить акт.',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', 0.77],
                                [f'Насыщение 5м3. Определение Q при Р-{well_data.max_admissible_pressure._value}', None,
                                 f'ПРИ НЕГЕРМЕТИЧНОСТИ: \nПроизвести насыщение скважины в объеме 5м3 по '
                                 f'затрубному пространству. Определить приемистость '
                                 f'НЭК {dict_leakinest_keys[ind_nek]} при Р-{well_data.max_admissible_pressure._value}'
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
                            ind_nek += 1
                            pakerNEK = pakerNEK1
                        else:
                            ind_nek += 1
                            pakerNEK = pakerNEK1

                    if len(dict_leakinest_keys) - ind_nek == 0:
                        pressureNEK_list = [
                            [f'При герметичности:  Допустить пакер до '
                                 f'глубины {paker_depth}м', None,
                                 f'При герметичности колонны:  Допустить пакер до '
                                 f'глубины {paker_depth}м',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', 0.4],
                                [f'Опрессовать '
                                 f'в инт {paker_depth}-0м на Р={well_data.max_admissible_pressure._value}атм',
                                 None,
                                 f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну '
                                 f'в интервале {paker_depth}-0м на Р={well_data.max_admissible_pressure._value}атм'
                                 f' в течение 30 минут в присутствии представителя заказчика, составить акт.',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', 0.77],
                                [f'срыв пакера 30мин', None,
                                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса '
                                 f'НКТ в течении 30мин и с '
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
                        for row in pressureNEK_list:
                            paker_list.append(row)

        if self.need_privyazka_QCombo == "Да":
            paker_list.insert(1, privyazkaNKT(self)[0])

        return paker_list

    def nktOpress(self):

        if well_data.nktOpressTrue is False:
            well_data.nktOpressTrue is True
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












