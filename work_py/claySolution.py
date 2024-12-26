from work_py.alone_oreration import volume_vn_ek, volume_vn_nkt, well_volume

from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton

import data_list
from work_py.calculate_work_parametrs import volume_calculate_roof_of_sole

from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion
from work_py.rir import RirWindow

from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPageSoClay(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.purpose_of_clay_label = QLabel("цель закачки глинистого раствора", self)
        self.purpose_of_clay_combo = QComboBox(self)
        self.purpose_of_clay_combo.addItems(['в колонне', 'сбитие приемистости'])

        self.current_bottom_label = QLabel("забой", self)
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setValidator(self.validator_float)
        self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')

        self.roof_clay_label = QLabel("кровля ГР", self)
        self.roof_clay_edit = QLineEdit(self)
        self.roof_clay_edit.setValidator(self.validator_float)

        self.roof_clay_edit.setText(f'{self.data_well.perforation_roof + 70}')
        self.roof_clay_edit.setClearButtonEnabled(True)

        self.sole_clay_LabelType = QLabel("Подошва ГР", self)
        self.sole_clay_edit = QLineEdit(self)
        self.sole_clay_edit.setText(f'{self.data_well.current_bottom}')
        self.sole_clay_edit.setValidator(self.validator_float)

        self.volume_clay_label = QLabel("Объем глинистого раствора", self)
        self.volume_clay_edit = QLineEdit(self)
        self.volume_clay_edit.setValidator(self.validator_float)

        self.rir_question_Label = QLabel("Нужно ли УЦМ производить на данной компоновке", self)
        self.rir_question_combo = QComboBox(self)
        self.rir_question_combo.addItems(['Нет', 'Да'])

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.purpose_of_clay_label, 2, 4)
        self.grid.addWidget(self.purpose_of_clay_combo, 3, 4)

        self.grid.addWidget(self.volume_clay_label, 4, 7)
        self.grid.addWidget(self.volume_clay_edit, 5, 7)

        self.roof_clay_edit.editingFinished.connect(self.update_roof)

        self.rir_question_combo.currentTextChanged.connect(self.update_rir)
        self.purpose_of_clay_combo.currentIndexChanged.connect(self.update_purpose_of_clay)

        self.purpose_of_clay_combo.setCurrentIndex(1)
        # self.purpose_of_clay_combo.setCurrentIndex(0)

    def update_purpose_of_clay(self, index):

        if index == 0:
            self.grid.addWidget(self.roof_clay_label, 4, 4)
            self.grid.addWidget(self.roof_clay_edit, 5, 4)
            self.grid.addWidget(self.sole_clay_LabelType, 4, 5)
            self.grid.addWidget(self.sole_clay_edit, 5, 5)

            self.grid.addWidget(self.rir_question_Label, 6, 3)
            self.grid.addWidget(self.rir_question_combo, 7, 3)

            self.current_bottom_label.setParent(None)
            self.current_bottom_edit.setParent(None)
        else:
            self.volume_clay_edit.setText(f'{5}')
            self.roof_clay_label.setParent(None)
            self.roof_clay_edit.setParent(None)
            self.sole_clay_LabelType.setParent(None)
            self.sole_clay_edit.setParent(None)

            self.rir_question_Label.setParent(None)
            self.rir_question_combo.setParent(None)

            self.grid.addWidget(self.current_bottom_label, 6, 4)
            self.grid.addWidget(self.current_bottom_edit, 7, 4)

    def update_roof(self):
        roof_clay = self.roof_clay_edit.text()
        sole_clay = self.sole_clay_edit.text()
        if roof_clay != '' and sole_clay != '':
            volume_calculate = volume_calculate_roof_of_sole(self.data_well, roof_clay, sole_clay)
            self.volume_clay_edit.setText(str(volume_calculate))

        if self.rir_question_combo.currentText() == 'Да':
            self.sole_rir_edit.setText(f'{float(roof_clay)}')
            self.roof_rir_edit.setText(f'{float(roof_clay) - 50}')

    def update_rir(self, index):
        if index == "Нет":
            self.roof_rir_label.setParent(None)
            self.roof_rir_edit.setParent(None)
            self.sole_rir_LabelType.setParent(None)
            self.sole_rir_edit.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
        else:
            self.roof_rir_label = QLabel("Плановая кровля РИР", self)
            self.roof_rir_edit = QLineEdit(self)


            self.roof_rir_edit.setText(f'{self.data_well.current_bottom - 50}')
            self.roof_rir_edit.setClearButtonEnabled(True)

            self.sole_rir_LabelType = QLabel("Подошва РИР", self)
            self.sole_rir_edit = QLineEdit(self)
            self.sole_rir_edit.editingFinished.connect(self.update_volume_cement)
            self.roof_rir_edit.editingFinished.connect(self.update_volume_cement)
            self.sole_rir_edit.setText(f'{self.data_well.current_bottom}')
            self.sole_rir_edit.setClearButtonEnabled(True)
            self.cement_volume_label = QLabel('Объем цемента')
            self.cement_volume_line = QLineEdit(self)

            self.info_rir_label = QLabel('Цель РИР')
            self.info_rir_edit = QLineEdit(self)

            self.grid.addWidget(self.roof_rir_label, 6, 4)
            self.grid.addWidget(self.roof_rir_edit, 7, 4)
            self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
            self.grid.addWidget(self.sole_rir_edit, 7, 5)
            self.grid.addWidget(self.cement_volume_label, 6, 6)
            self.grid.addWidget(self.cement_volume_line, 7, 6)
            self.grid.addWidget(self.info_rir_label, 6, 7)
            self.grid.addWidget(self.info_rir_edit, 7, 7)

    def update_volume_cement(self):
        roof_rir = self.roof_rir_edit.text()
        sole_rir = self.sole_rir_edit.text()
        if roof_rir != '' and sole_rir != '':
            self.cement_volume_line.setText(
                f'{round(volume_calculate_roof_of_sole(self.data_well, roof_rir, sole_rir), 1)}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoClay(parent), 'отсыпка')


class ClayWindow(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)
        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        self.roof_rir_edit, self.sole_rir_edit, self.volume_cement = '', '', ''

    def add_work(self):
        self.current_widget = self.tabWidget.currentWidget()
        self.purpose_of_clay = self.current_widget.purpose_of_clay_combo.currentText()

        self.strategies = {
            'сбитие приемистости': ClaySolutionForRir(self),
            'в колонне': ClaySolutionForEk(self)
        }

        strategy = self.strategies.get(self.purpose_of_clay)
        if strategy:
            work_list = strategy.add_work_clay()
            self.populate_row(self.insert_index, work_list, self.table_widget)
            data_list.pause = False
            self.close()

    def clay_solution_q(self, current_bottom_edit, volume_clay_edit):
        if self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                current_bottom_edit > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: current_bottom_edit - self.data_well.head_column_additional.get_value}
        else:
            dict_nkt = {73: current_bottom_edit}
        glin_list = [
            [f'СПО пера до глубины {current_bottom_edit}м. Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, current_bottom_edit)} на тНКТ{self.data_well.nkt_diam}мм '
             f'до '
             f'глубины {current_bottom_edit}м с замером, шаблонированием '
             f'шаблоном {self.data_well.nkt_template}мм. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom_edit, 1)],
            [None, None,
             f'По результатам определения приёмистости выполнить следующие работы: \n'
             f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке глинистого раствора '
             f'(по согласованию с ГС и ПТО {data_list.contractor} и заказчика). \n'
             f'В случае приёмистости менее 480 м3/сут при Р=100атм и более 120м3/сут при Р=100атм приступить '
             f'к выполнению РИР',
             None, None, None, None, None, None, None,
             'мастер КРС, заказчик', None],
            [None, None,
             f'Объём глинистого р-ра скорректировать на устье на основании тех.возможности. \n'
             f'Приготовить глинистый раствор в объёме 5м3 (расчет на 1 м3 - сухой глинопорошок массой 0,3т + '
             f'вода у=1,00г/см3 в объёме 0,9м3) плотностью у=1,24г/см3',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Закачка глины для сбития приемистости', None,
             f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме '
             f'{volume_clay_edit}м3 + тех. воду '
             f'в объёме {round(volume_vn_nkt(dict_nkt) - volume_clay_edit, 1)}м3. Закрыть затруб. '
             f'Продавить в НКТ тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более '
             f'{self.data_well.max_admissible_pressure.get_value}атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [f'Коагуляция 4 часа', None,
             f'Коагуляция 4 часа (на основании конечного давления при продавке. '
             f'В случае конечного давления менее 50атм, согласовать объем глинистого раствора с '
             f'Заказчиком и продолжить приготовление следующего объема глинистого объема).',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Определить приёмистость по НКТ при Р=100атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.35],
            [None, None,
             f'В случае необходимости выполнить работы по закачке глинистого раствора, с корректировкой '
             f'по объёму раствора.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью '
             f'в объеме не менее {well_volume(self, volume_vn_nkt(dict_nkt))}м3 с расходом жидкости не менее 8 л/с.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(24)],
            [None, None,
             f'Опрессовать НКТ на 200атм. Вымыть шар. Поднять перо на тНКТ{self.data_well.nkt_diam}мм '
             f'с глубины '
             f'{current_bottom_edit}м с доливом скважины в объеме '
             f'{round(current_bottom_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
             f'уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(current_bottom_edit, 1)]
        ]

        if volume_vn_nkt(dict_nkt) <= 5:
            glin_list[3] = [
                None, None,
                f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                f'Продавить в НКТ остаток глинистого раствора в объеме '
                f'{round(volume_clay_edit - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более '
                f'{self.data_well.max_admissible_pressure.get_value}атм.',
                None, None, None, None, None, None, None,
                'мастер КРС', 0.5]
        self.calculate_chemistry('глина', volume_clay_edit)
        return glin_list

    def clay_solution_def(self, rir_roof, rir_sole, rir_question_combo,
                          roof_rir_edit=0, sole_rir_edit=0, volume_cement=0):

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])
        volume_clay = round(volume_vn_ek(self, rir_sole) * (rir_sole - rir_roof) / 1000, 1)

        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                rir_sole > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: self.data_well.head_column_additional.get_value - rir_sole}
        else:
            dict_nkt = {73: rir_sole}

        pero_list = [
            [f'СПО {RirWindow.pero_select(self, rir_sole)}  на тНКТ{nkt_diam}мм до {rir_sole}м', None,
             f'Спустить {RirWindow.pero_select(self, rir_sole)} на тНКТ{nkt_diam}мм до глубины {rir_sole}м с '
             f'замером, шаблонированием '
             f'шаблоном {self.data_well.nkt_template}мм. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(rir_sole, 1)],
            [f'закачку глинистого раствора в интервале {rir_sole}-{rir_roof}м в объеме {volume_clay}м3 '
             f'({round(volume_clay * 0.45, 2)}т'
             f' сухого порошка)', None,
             f'Произвести закачку глинистого раствора в объеме {volume_clay}м3 '
             f'удельным весом не менее 1,24г/см3 в интервале {rir_roof}-{rir_sole}м.\n'
             f'- Приготовить и закачать в глинистый раствор уд.весом не менее 1,24г/см3 в объеме {volume_clay}м3 '
             f'({round(volume_clay * 0.45, 2)}т'
             f' сухого порошка) с добавлением ингибитора коррозии {round(volume_clay * 11, 1)}гр с '
             f'удельной дозировкой 11гр/м3 .\n'
             f'-Продавить тех жидкостью  в объеме {volume_vn_nkt(dict_nkt, rir_roof, rir_sole)}м3.',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5]]

        self.calculate_chemistry('глина', volume_clay * 0.45)

        self.data_well.current_bottom = rir_roof

        if rir_question_combo == 'Нет':
            pero_list.append([None, None,
                              f'Поднять перо на тНКТ{nkt_diam}мм с глубины {rir_sole}м с доливом скважины в объеме '
                              f'{round(rir_sole * 1.3 / 1000, 1)}м3 тех. жидкостью '
                              f'уд.весом {self.data_well.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(rir_roof, 1)])
        else:
            pero_list.append([None, None,
                              f'Поднять перо на тНКТ{nkt_diam}мм до глубины {rir_roof}м с доливом скважины в объеме'
                              f' {round((rir_sole - self.roof_clay) * 1.3 / 1000, 1)}м3 тех. жидкостью '
                              f'уд.весом {self.data_well.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(float(rir_sole) - float(self.roof_clay), 1)])
            if (self.data_well.plast_work) != 0 or rir_sole > self.data_well.perforation_roof:
                rir_work_list = RirWindow.rir_with_pero_gl(self, 'Не нужно', '', roof_rir_edit, sole_rir_edit,
                                                           volume_cement)
                pero_list.extend(rir_work_list[1:])
            else:
                rir_work_list = RirWindow.rir_with_pero_gl(self, 'Не нужно', '', roof_rir_edit, sole_rir_edit,
                                                           volume_cement)
                pero_list.extend(rir_work_list[-10:])
        return pero_list


class ClayWork:
    def __init__(self, parent=None):
        self.data_well = parent.data_well
        self.calculate_chemistry = parent.calculate_chemistry
        self.sole_rir = None
        self.roof_rir = None
        self.rir_question = None
        self.sole_clay = None
        self.roof_clay = None
        self.volume_clay = None
        self.current_bottom = None

    def add_work_clay(self):
        NotImplementedError('Не выбран метод реализации, метод должен быть переопределен')


class ClaySolutionForRir(ClayWork):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def add_work_clay(self):
        self.current_bottom = float(self.parent.current_widget.current_bottom_edit.text())
        self.volume_clay = float(self.parent.current_widget.volume_clay_edit.text())
        if self.current_bottom == '' and self.volume_clay == '':
            QMessageBox(self.parent, 'Ошибка', 'Не введены все значения')
            return
        work_list = self.clay_solution_q()
        return work_list

    def clay_solution_q(self):
        if (self.data_well.column_additional is True and
                self.data_well.column_additional_diameter.get_value < 110 and \
                self.current_bottom > self.data_well.head_column_additional.get_value):
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: self.current_bottom - self.data_well.head_column_additional.get_value}
        else:
            dict_nkt = {73: self.current_bottom}
        glin_list = [
            # [f'СПО пера до глубины {self.current_bottom}м. Опрессовать НКТ на 200атм', None,
            #  f'Спустить {RirWindow.pero_select(self, self.current_bottom)} на '
            #  f'тНКТ{self.data_well.nkt_diam}мм до '
            #  f'глубины {self.current_bottom}м с замером, шаблонированием '
            #  f'шаблоном {self.data_well.nkt_template}мм. \n'
            #  f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
            #  None, None, None, None, None, None, None,
            #  'мастер КРС', descentNKT_norm(self.current_bottom, 1)],
            [None, None,
             f'По результатам определения приёмистости выполнить следующие работы: \n'
             f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке глинистого раствора '
             f'(по согласованию с ГС и ПТО {data_list.contractor} и заказчика). \n'
             f'В случае приёмистости менее 480 м3/сут при Р=100атм и более 120м3/сут при Р=100атм приступить '
             f'к выполнению РИР',
             None, None, None, None, None, None, None,
             'мастер КРС, заказчик', None],
            [None, None,
             f'Объём глинистого р-ра скорректировать на устье на основании тех.возможности. \n'
             f'Приготовить глинистый раствор в объёме 5м3 (расчет на 1 м3 - сухой глинопорошок массой 0,3т + '
             f'вода у=1,00г/см3 в объёме 0,9м3) плотностью у=1,24г/см3',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Закачка глины для сбития приемистости', None,
             f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме '
             f'{self.volume_clay}м3 + тех. воду '
             f'в объёме {round(volume_vn_nkt(dict_nkt) - self.volume_clay, 1)}м3. Закрыть затруб. '
             f'Продавить в НКТ тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более '
             f'{self.data_well.max_admissible_pressure.get_value}атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [f'Коагуляция 4 часа', None,
             f'Коагуляция 4 часа (на основании конечного давления при продавке. '
             f'В случае конечного давления менее 50атм, согласовать объем глинистого раствора с '
             f'Заказчиком и продолжить приготовление следующего объема глинистого объема).',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Определить приёмистость по НКТ при Р=100атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.35],
            [None, None,
             f'В случае необходимости выполнить работы по закачке глинистого раствора, с корректировкой '
             f'по объёму раствора.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью '
             f'в объеме не менее {well_volume(self, volume_vn_nkt(dict_nkt))}м3 с расходом жидкости не менее 8 л/с.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(24)],
            # [None, None,
            #  f'Опрессовать НКТ на 200атм. Вымыть шар. Поднять перо на тНКТ{self.data_well.nkt_diam}мм '
            #  f'с глубины {self.current_bottom}м с доливом скважины в объеме '
            #  f'{round(self.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью '
            #  f'уд.весом {self.data_well.fluid_work}',
            #  None, None, None, None, None, None, None,
            #  'мастер КРС', liftingNKT_norm(self.current_bottom, 1)]
        ]

        if volume_vn_nkt(dict_nkt) <= 5:
            glin_list[3] = [
                None, None,
                f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                f'Продавить в НКТ остаток глинистого раствора в объеме '
                f'{round(self.volume_clay - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более '
                f'{self.data_well.max_admissible_pressure.get_value}атм.',
                None, None, None, None, None, None, None,
                'мастер КРС', 0.5]
        self.calculate_chemistry('глина', self.volume_clay)
        return glin_list


class ClaySolutionForEk(ClayWork):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

    def add_work_clay(self):
        self.roof_clay = int(float(self.parent.current_widget.roof_clay_edit.text()))
        self.sole_clay = int(float(self.parent.current_widget.sole_clay_edit.text()))
        self.rir_question = str(self.parent.current_widget.rir_question_combo.currentText())

        if self.rir_question == 'Да':
            self.roof_rir = int(float(self.parent.current_widget.roof_rir_edit.text()))
            self.sole_rir = int(float(self.parent.current_widget.sole_rir_edit.text()))
            self.volume_cement = self.parent.current_widget.cement_volume_line.text().replace(',', '.')
            self.info_rir_edit = self.parent.current_widget.info_rir_edit.text()
            if self.volume_cement != '':
                self.volume_cement = round(float(self.volume_cement), 1)
            elif self.volume_cement == '' and self.rir_question == "Да":
                QMessageBox.question(self.parent, 'Вопрос', f'Не указан объем цемента')
                return
        if self.roof_clay > self.sole_clay:
            QMessageBox.warning(self.parent, 'Ошибка', 'Не корректные интервалы ')
            return

        work_list = self.clay_solution_def()
        return work_list

    def clay_solution_def(self):
        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])

        volume_clay = round(volume_calculate_roof_of_sole(self.data_well, self.roof_clay, self.sole_clay), 1)

        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                self.sole_clay > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: self.data_well.head_column_additional.get_value - self.sole_clay}
        else:
            dict_nkt = {73: self.sole_clay}

        pero_list = [
            [f'СПО {RirWindow.pero_select(self, self.sole_clay)}  на тНКТ{nkt_diam}мм до {self.sole_clay}м', None,
             f'Спустить {RirWindow.pero_select(self, self.sole_clay)} на тНКТ{nkt_diam}мм до глубины {self.sole_clay}м '
             f'с замером, шаблонированием '
             f'шаблоном {self.data_well.nkt_template}мм. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.sole_clay, 1)],
            [f'закачку глинистого раствора в интервале {self.sole_clay}-{self.roof_clay}м в объеме {volume_clay}м3 '
             f'({round(volume_clay * 0.45, 2)}т'
             f' сухого порошка)', None,
             f'Произвести закачку глинистого раствора в объеме {volume_clay}м3 '
             f'удельным весом не менее 1,24г/см3 в интервале {self.roof_clay}-{self.sole_clay}м.\n'
             f'- Приготовить и закачать в глинистый раствор уд.весом не менее 1,24г/см3 в объеме {volume_clay}м3 '
             f'({round(volume_clay * 0.45, 2)}т'
             f' сухого порошка) с добавлением ингибитора коррозии {round(volume_clay * 11, 1)}гр с '
             f'удельной дозировкой 11гр/м3 .\n'
             f'-Продавить тех жидкостью  в объеме {volume_vn_nkt(dict_nkt, self.roof_clay, self.sole_clay)}м3.',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5]]

        self.parent.calculate_chemistry('глина', volume_clay * 0.45)

        self.data_well.current_bottom = self.roof_clay

        if self.rir_question == 'Нет':
            pero_list.append([None, None,
                              f'Поднять перо на тНКТ{nkt_diam}мм с глубины {self.sole_clay}м с доливом'
                              f' скважины в объеме '
                              f'{round(self.sole_clay * 1.3 / 1000, 1)}м3 тех. жидкостью '
                              f'уд.весом {self.data_well.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(self.roof_clay, 1)])
        else:
            pero_list.append([None, None,
                              f'Поднять перо на тНКТ{nkt_diam}мм до глубины {self.roof_clay}м с доливом '
                              f'скважины в объеме'
                              f' {round((self.sole_clay - self.roof_clay) * 1.3 / 1000, 1)}м3 тех. жидкостью '
                              f'уд.весом {self.data_well.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(float(self.sole_clay) - float(self.roof_clay), 1)])
            rir_work_list = RirWindow.rir_with_pero_gl(self, 'Не нужно', '', self.roof_rir, self.sole_rir,
                                                       self.volume_cement, self.info_rir_edit)
            if (self.data_well.plast_work) != 0 or self.sole_clay > self.data_well.perforation_roof:

                pero_list.extend(rir_work_list[1:])
            else:

                pero_list.extend(rir_work_list[-10:])
        return pero_list
