import datetime

import data_list
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget, QPushButton
from work_py.alone_oreration import volume_vn_ek, well_volume, volume_vn_nkt
from work_py.change_fluid import Change_fluid_Window
from work_py.opressovka import OpressovkaEK

from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.acid_paker import CheckableComboBox


class TabPageSoRir(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.paker_need_labelType = QLabel("необходимость спо пакера \nдля опрессовки ЭК и определения Q", self)
        self.paker_need_combo = QComboBox(self)
        self.paker_need_combo.addItems(['Нужно СПО', 'без СПО'])

        if self.difference_date_days(self.data_well.date_commissioning) < 365.25 * 20 and \
                self.difference_date_days(self.data_well.result_pressure_date) < 365 * 3 and \
                len(self.data_well.leakiness_interval) == 0:
            self.paker_need_combo.setCurrentIndex(1)

        self.rir_type_Label = QLabel("Вид РИР", self)
        self.rir_type_combo = QComboBox(self)
        self.rir_type_combo.addItems(['', 'РИР на пере', 'УЦМ в глухой колонне',
                                      'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП', 'РИР ОВП с пакером',
                                      'РПП Силами ККТ', 'РИР с РПП + ЦМ'])
        plast_work = ['']
        plast_work.extend(self.data_well.plast_work)

        if len(self.data_well.dict_leakiness) != 0:
            for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
                plast_work.append(f'НЭК {nek}')

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.setStyleSheet("QComboBox { width: 200px; }")
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.roof_rir_label = QLabel("Плановая кровля РИР", self)

        self.roof_rir_edit = QLineEdit(self)
        self.roof_rir_edit.setValidator(self.validator_int)
        # self.roof_rir_edit.setText()
        self.roof_rir_edit.setClearButtonEnabled(True)

        self.sole_rir_LabelType = QLabel("Подошва РИР", self)

        self.sole_rir_edit = QLineEdit(self)
        self.sole_rir_edit.setValidator(self.validator_int)
        self.sole_rir_edit.setClearButtonEnabled(True)

        self.cement_volume_label = QLabel('Объем цемента')
        self.cement_volume_line = QLineEdit(self)

        self.paker_need_combo.currentTextChanged.connect(self.update_paker_need_ek)

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])
        if len(self.data_well.plast_work) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressure_new_label = QLabel('Ожидаемое давление', self)
        self.pressure_new_edit = QLineEdit(self)
        self.pressure_new_edit.setValidator(self.validator_int)

        if len(self.data_well.plast_project) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(self.data_well.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)

        # self.grid = QGridLayout(self)
        self.view_paker_work()

        self.grid.addWidget(self.paker_need_labelType, 4, 1)
        self.grid.addWidget(self.paker_need_combo, 5, 1)

        self.grid.addWidget(self.rir_type_Label, 4, 2)
        self.grid.addWidget(self.rir_type_combo, 5, 2)
        self.grid.addWidget(self.plast_label, 4, 3)
        self.grid.addWidget(self.plast_combo, 5, 3)
        self.grid.addWidget(self.roof_rir_label, 4, 4)
        self.grid.addWidget(self.roof_rir_edit, 5, 4)
        self.grid.addWidget(self.sole_rir_LabelType, 4, 5)
        self.grid.addWidget(self.sole_rir_edit, 5, 5)

        self.grid.addWidget(self.diameter_paker_label_type, 1, 1)
        self.grid.addWidget(self.diameter_paker_edit, 2, 1)

        self.grid.addWidget(self.paker_khost_label, 1, 2)
        self.grid.addWidget(self.paker_khost_edit, 2, 2)

        self.grid.addWidget(self.paker_depth_label, 1, 3)
        self.grid.addWidget(self.paker_depth_edit, 2, 3)

        # self.grid.addWidget(self.pressure_zumpf_question_label, 1, 4)
        # self.grid.addWidget(self.pressure_zumpf_question_combo, 2, 4)
        #
        # self.grid.addWidget(self.need_privyazka_Label, 1, 6)
        # self.grid.addWidget(self.need_privyazka_q_combo, 2, 6)

        self.grid.addWidget(self.need_change_zgs_label, 9, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

        self.grid.addWidget(self.plast_new_label, 9, 3)
        self.grid.addWidget(self.plast_new_combo, 10, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.grid.addWidget(self.pressure_new_label, 9, 5)
        self.grid.addWidget(self.pressure_new_edit, 10, 5)

        self.cement_volume_line.setValidator(self.validator_float)

        self.grid.addWidget(self.cement_volume_label, 4, 6)
        self.grid.addWidget(self.cement_volume_line, 5, 6)

        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)
        self.need_change_zgs_combo.setCurrentIndex(1)
        self.rir_type_combo.currentTextChanged.connect(self.update_rir_type)

        # self.paker_depth_edit.textChanged.connect(self.update_depth_paker)
        self.roof_rir_edit.textChanged.connect(self.update_volume_cement)
        self.sole_rir_edit.textChanged.connect(self.update_volume_cement)

        self.paker_need_combo.setCurrentIndex(1)
        self.paker_need_combo.setCurrentIndex(0)

    def update_change_fluid(self, index):
        if index == 'Да':
            category_h2s_list_plan = list(
                map(int, [self.data_well.dict_category[plast]['по сероводороду'].category for plast in
                          self.data_well.plast_project if self.data_well.dict_category.get(plast) and
                          self.data_well.dict_category[plast]['отключение'] == 'планируемый']))

            if len(category_h2s_list_plan) != 0:
                plast = self.data_well.plast_project[0]
                self.pressure_new_edit.setText(f'{self.data_well.dict_category[plast]["по давлению"].data_pressure}')
            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressure_new_label, 9, 5)
            self.grid.addWidget(self.pressure_new_edit, 10, 5)
        else:
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressure_new_label.setParent(None)
            self.pressure_new_edit.setParent(None)

    def update_depth_paker(self):

        self.view_paker_work()

        paker_depth = self.paker_depth_edit.text()
        if paker_depth != '':
            self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(float(paker_depth)))}')

        if self.data_well.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = self.data_well.current_bottom - int(paker_depth)
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')

    def update_rir_type(self, index):
        if index in ['РИР с пакером с 2С', 'РИР ОВП с пакером']:
            self.need_change_zgs_label.setParent(None)
            self.need_change_zgs_combo.setParent(None)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressure_new_label.setParent(None)
            self.pressure_new_edit.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
            self.paker_depth_edit.setText(f'{self.data_well.perforation_roof - 30}')
            self.roof_rir_edit.setText(f'{self.data_well.perforation_roof - 30}')
            self.sole_rir_edit.setText(f'{self.data_well.current_bottom}')
        elif index in ['РИР с РПК', 'РИР с РПП', 'РПП Силами ККТ']:
            self.need_change_zgs_label.setParent(None)
            self.need_change_zgs_combo.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressure_new_label.setParent(None)
            self.pressure_new_edit.setParent(None)
            self.paker_depth_edit.setText(f'{self.data_well.perforation_roof - 30}')
            self.roof_rir_edit.setText(f'{self.data_well.perforation_roof - 10}')
            if index == 'РИР с РПП':
                self.sole_rir_edit.setText(f'{self.roof_rir_edit.text()}')
                self.paker_depth_edit.setText(f'{self.data_well.perforation_roof - 30}')
            elif index == 'РИР с РПК':
                self.sole_rir_edit.setText(f'{self.data_well.perforation_roof - 10}')
                self.paker_depth_edit.setText(f'{self.data_well.perforation_roof - 10}')
        elif index in ['РИР на пере',
                       'УЦМ в глухой колонне',
                       'РИР с РПП + ЦМ']:  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            self.grid.addWidget(self.cement_volume_label, 4, 6)
            self.grid.addWidget(self.cement_volume_line, 5, 6)

            self.grid.addWidget(self.need_change_zgs_label, 9, 2)
            self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressure_new_label, 9, 5)
            self.grid.addWidget(self.pressure_new_edit, 10, 5)
            self.roof_rir_edit.setText(f'{self.data_well.perforation_roof - 50}')
            self.sole_rir_edit.setText(f'{self.data_well.current_bottom}')
            self.paker_depth_edit.setText(f'{self.data_well.perforation_roof - 30}')

    def update_volume_cement(self):
        if self.roof_rir_edit.text() != '' and self.sole_rir_edit.text() != '':
            volume_cement = round(volume_vn_ek(self, float(self.roof_rir_edit.text())) * (
                    float(self.sole_rir_edit.text()) - float(self.roof_rir_edit.text())) / 1000, 1)
            self.cement_volume_line.setText(f'{min([2, volume_cement])}')

    def update_paker_need_ek(self, index):
        if index == 'Нужно СПО':
            self.grid.addWidget(self.diameter_paker_label_type, 1, 1)
            self.grid.addWidget(self.diameter_paker_edit, 2, 1)

            self.grid.addWidget(self.paker_khost_label, 1, 2)
            self.grid.addWidget(self.paker_khost_edit, 2, 2)

            self.grid.addWidget(self.paker_depth_label, 1, 3)
            self.grid.addWidget(self.paker_depth_edit, 2, 3)

            self.grid.addWidget(self.pressure_zumpf_question_label, 1, 4)
            self.grid.addWidget(self.pressure_zumpf_question_combo, 2, 4)
            if self.pressure_zumpf_question_combo.currentText() == 'Да':
                self.paker_depth_zumpf_edit.setText(f'{self.data_well.perforation_sole + 10}')
        else:
            self.diameter_paker_label_type.setParent(None)
            self.diameter_paker_edit.setParent(None)
            self.paker_khost_label.setParent(None)
            self.paker_khost_edit.setParent(None)
            self.paker_depth_label.setParent(None)
            self.paker_depth_edit.setParent(None)
            try:
                self.pressure_zumpf_question_label.setParent(None)
                self.pressure_zumpf_question_combo.setParent(None)

                self.paker_depth_zumpf_label.setParent(None)
                self.paker_depth_zumpf_edit.setParent(None)
            except Exception:
                pass

    def update_plast_edit(self):

        dict_perforation = self.data_well.dict_perforation

        plasts = data_list.texts

        roof_plast = self.data_well.current_bottom
        sole_plast = 0
        for plast_sel in plasts:
            for plast in self.data_well.plast_work:
                if plast_sel == plast:
                    try:
                        if roof_plast >= dict_perforation[plast]['кровля']:
                            roof_plast = dict_perforation[plast]['кровля']
                        if sole_plast <= dict_perforation[plast]['подошва']:
                            sole_plast = dict_perforation[plast]['подошва']
                    except Exception:
                        pass

            if len(self.data_well.dict_leakiness):
                for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):

                    if nek in plast_sel:
                        if roof_plast >= float(nek.split('-')[0]):
                            roof_plast = float(nek.split('-')[0])
                            # print(f' кровля {roof_plast}')
                        if sole_plast <= float(nek.split('-')[1]):
                            sole_plast = float(nek.split('-')[1])
                        # print(nek, roof_plast, sole_plast)
        self.roof_rir_edit.setText(f"{int(roof_plast - 30)}")
        self.paker_depth_edit.setText(f"{int(roof_plast - 20)}")
        if sole_plast + 20 > self.data_well.current_bottom:
            self.sole_rir_edit.setText(f'{self.data_well.current_bottom}')
        else:
            self.sole_rir_edit.setText(f"{sole_plast + 20}")


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoRir(parent), 'Ремонтно-Изоляционные работы')


class RirWindow(WindowUnion):
    work_rir_window = None

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.rir_type_combo = None
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

    def rir_kkt(self, paker_need_combo, plast_combo, roof_rir_edit, pressure_zumpf_question,
                diameter_paker=122, paker_khost=0, paker_depth=0):
        rir_list = self.need_paker(paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                   paker_depth, pressure_zumpf_question, True)
        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True
        else:
            rir_rpk_plast_true = False
        rir_work_list = [
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 24 часов сутки через ЦИТС {data_list.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером  '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. ',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [f'установка ККТ на {roof_rir_edit}м', None,
             f'Произвести установку глухого пакера  для изоляции {plast_combo} по технологическому плану '
             f'подрядчика по РИР силами подрядчика по РИР '
             f'с установкой пакера  на глубине {roof_rir_edit}м',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
            [f'{self.need_opressovki(rir_rpk_plast_true)}', None,
             f'{self.need_opressovki(rir_rpk_plast_true)} '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
             f'подтверждением за 2 часа до начала работ) ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ  с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None]
        ]

        rir_list.extend(rir_work_list)

        self.data_well.current_bottom = roof_rir_edit
        self.perf_new(roof_rir_edit, roof_rir_edit + 1)

        return rir_list

    def rir_rpp(self, paker_need_combo, plast_combo,
                roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                diameter_paker=122, paker_khost=0, paker_depth=0):

        rir_list = self.need_paker(paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                   paker_depth, pressure_zumpf_question, True)

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True
        else:
            rir_rpk_plast_true = False

        rir_work_list = [
            [f'СПО РПП до глубины {sole_rir_edit}м', None,
             f'Спустить пакер глухой {self.rpk_nkt(sole_rir_edit)}  на тНКТ{self.data_well.nkt_diam}мм '
             f'до глубины {sole_rir_edit}м '
             f'с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии '
             f'представителя РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sole_rir_edit, 1.2)],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером  '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'опрессовать НКТ на 200атм', None,
             f'При наличии циркуляции опрессовать НКТ на 200атм '
             f'в присутствии подрядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.5 + 0.6],
            [f'установка РПП на {sole_rir_edit}м', None,
             f'Произвести установку глухого пакера  для изоляции {plast_combo} по технологическому плану '
             f'с установкой пакера  на глубине {sole_rir_edit}м',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],

            [f'{self.need_opressovki(rir_rpk_plast_true)}',
             None,
             f'{self.need_opressovki(rir_rpk_plast_true)} '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
             f'подтверждением за 2 часа до начала работ) ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Поднять стыковочное устройство с глубины {roof_rir_edit}м с доливом скважины в объеме '
             f'{round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work} ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1.2)]]

        for row in rir_work_list:
            rir_list.append(row)

        self.data_well.current_bottom = roof_rir_edit
        self.perf_new(roof_rir_edit, roof_rir_edit + 1)
        self.data_well.for_paker_list = None
        # print(f'текущий забой {self.data_well.current_bottom}')
        return rir_list

    def rir_rpp_cm(self, paker_need_combo, plast_combo,
                   roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo='Нет', plast_new_combo='',
                   fluid_new_edit='', pressure_new_edit='', pressure_zumpf_question='Не нужно',
                   diameter_paker=122, paker_khost=0, paker_depth=0):
        work_list = self.rir_rpp(paker_need_combo, plast_combo,
                                 roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                                 diameter_paker, paker_khost, paker_depth)

        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                sole_rir_edit > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: sole_rir_edit - self.data_well.head_column_additional.get_value}
        else:
            dict_nkt = {73: sole_rir_edit}

        volume_in_nkt, volume_in_ek = RirWindow.calc_buffer(self, roof_rir_edit, sole_rir_edit, dict_nkt)

        rir_list = [
            [f'УЦМ в инт {roof_rir_edit}-{sole_rir_edit}м', None,
             f'Произвести цементную заливку с целью изоляции пласта {plast_combo}  в интервале '
             f'{roof_rir_edit}-{sole_rir_edit}м в присутствии '
             f'представителя УСРС и СТ',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None,
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
             f' (сухой цемент {round(volume_cement / 1.25, 1)}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме {volume_in_ek}м3,'
             f' цементный раствор в '
             f'объеме {volume_cement}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме {volume_in_nkt}м3, тех. жидкостью  в объёме '
             f'{round(volume_vn_nkt(dict_nkt, roof_rir_edit, sole_rir_edit) - volume_in_nkt, 1)}м3. '
             f'Уравновешивание цементного раствора',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Приподнять перо до гл.{roof_rir_edit}м. Закрыть трубное пространство. '
             f'Продавить по затрубному пространству '
             f'тех.жидкостью  при давлении не более {self.data_well.max_admissible_pressure.get_value}атм '
             f'(до получения технологического СТОП).',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
             f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом '
             f'{self.data_well.fluid_work} '
             f'(Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)]]

        for row in rir_list:
            work_list.insert(-1, row)

        ozc_list = [
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [None, None,
             f'Спустить перо с замером и шаблонированием НКТ до кровли цементного моста '
             f'(плановый на гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
             f'телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67]]
        work_list.extend(ozc_list)
        if need_change_zgs_combo == "Да":
            for row in Change_fluid_Window.fluid_change(self, plast_new_combo, fluid_new_edit,
                                                        pressure_new_edit):
                work_list.append(row)
            work_list.append([
                None, None,
                f'Поднять перо на тНКТ с глубины {roof_rir_edit}м с доливом скважины в '
                f'объеме {round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью уд.весом {self.data_well.fluid_work}',
                None, None, None, None, None, None, None,
                'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        else:
            work_list.append([
                None, None,
                f'Поднять перо на тНКТ с глубины {roof_rir_edit}м с доливом скважины в объеме '
                f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                f'уд.весом {self.data_well.fluid_work}',
                None, None, None, None, None, None, None,
                'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        return work_list

    def rir_rpk(self, paker_need_combo, plast_combo,
                roof_rir_edit, sole_rir_edit, pressure_zumpf_question='Не нужно',
                diameter_paker=122, paker_khost=0, paker_depth=0):

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        rir_rpk_plast_true = False
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True

        rir_list = self.need_paker(paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                   paker_depth, pressure_zumpf_question, rir_rpk_plast_true)

        if rir_rpk_plast_true:
            rir_q_list = [
                [f'посадить пакер на глубину {roof_rir_edit}м', None,
                 f'посадить пакер на глубину {roof_rir_edit}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1],
                [f'Насыщение 5м3. Определить приемистость {plast_combo} при Р=80-100атм',
                 None,
                 f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast_combo} при Р=80-100атм '
                 f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                 f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                 f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                 f'приемистости по технологическому плану',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.35]]
            for row in rir_q_list:
                rir_list.insert(-1, row)
        else:

            if self.rir_type_combo not in ['РИР с РПП']:
                rir_q_list = [
                    [f'Насыщение 5м3. Определить Q {plast_combo} при Р=80-100атм',
                     None,
                     f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast_combo} '
                     f'при Р=80-100атм '
                     f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                     f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                     f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с '
                     f'целью увеличения '
                     f'приемистости по технологическому плану',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 1.35]]
                for row in rir_q_list[::-1]:
                    rir_list.insert(-1, row)

        rir_work_list = [
            [f'СПО пакера РПК до глубины {roof_rir_edit}м', None,
             f'Спустить   пакера РПК {self.rpk_nkt(roof_rir_edit)}  на тНКТ{self.data_well.nkt_diam}мм до '
             f'глубины {roof_rir_edit}м с '
             f'замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя '
             f'РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(roof_rir_edit, 1.2)],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'опрессовать НКТ на 200атм', None,
             f'При наличии циркуляции опрессовать НКТ на 200атм '
             f'в присутствии подрядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [f'РИР {plast_combo} с установкой пакера РПК на глубине {roof_rir_edit}м ', None,
             f'Произвести РИР {plast_combo} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
             f'с установкой пакера РПК на глубине {roof_rir_edit}м',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [
                f'{self.need_opressovki(rir_rpk_plast_true)}',
                None,
                f'{self.need_opressovki(rir_rpk_plast_true)} '
                f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                f'подтверждением за 2 часа '
                f'до начала работ) ',
                None, None, None, None, None, None, None,
                'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Во время ОЗЦ поднять стыковочное устройство с глубины {roof_rir_edit}м с доливом скважины в объеме '
             f'{round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work} ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1)]]
        for row in rir_work_list:
            rir_list.append(row)
        self.perf_new(roof_rir_edit, self.data_well.current_bottom)
        self.data_well.current_bottom = roof_rir_edit
        self.data_well.for_paker_list = None
        return rir_list

    def need_opressovki(self, rir_rpk_plast_true):
        need_opress = ''
        if rir_rpk_plast_true is False:
            need_opress = f'Опрессовать эксплуатационную колонну на' \
                          f' Р={self.data_well.max_admissible_pressure.get_value}атм в присутствии представителя' \
                          f' заказчика'
        return need_opress

    def perf_new(self, roof_rir, sole_rir):

        for plast in self.data_well.plast_all:
            for interval in list((self.data_well.dict_perforation[plast]['интервал'])):
                if roof_rir <= interval[0] <= sole_rir:
                    self.data_well.dict_perforation[plast]['отключение'] = True
                if self.data_well.dict_perforation[plast]['отключение'] is False:
                    if interval[0] < self.data_well.perforation_roof:
                        self.data_well.perforation_roof = interval[0]
                    elif interval[1] > self.data_well.perforation_roof:
                        self.data_well.perforation_roof = interval[1]

        self.data_well.plast_work = []
        for plast in self.data_well.plast_all:
            if self.data_well.dict_perforation[plast]['отключение'] is False:
                self.data_well.plast_work.append(plast)

        if len(self.data_well.dict_leakiness) != 0:
            for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
                # print(roof_rir, float(nek.split('-')[0]), sole_rir)
                if roof_rir <= float(nek.split('-')[0]) <= sole_rir:
                    self.data_well.dict_leakiness['НЭК']['интервал'][nek]['отключение'] = True
            # print(f"при {self.data_well.dict_leakiness['НЭК']['интервал'][nek]['отключение']}")
        if self.data_well.column_additional:
            if self.data_well.current_bottom <= self.data_well.shoe_column_additional.get_value:
                self.data_well.open_trunk_well = False
        else:
            if self.data_well.current_bottom <= self.data_well.shoe_column.get_value:
                self.data_well.open_trunk_well = False

    def rpk_nkt(self, paker_depth):

        from work_py.opressovka import OpressovkaEK
        self.data_well.nkt_opress_true = False

        if self.data_well.column_additional is False or self.data_well.column_additional is True and \
                paker_depth < self.data_well.head_column_additional.get_value:
            rpk_nkt_select = f' для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                             f'{self.data_well.column_wall_thickness.get_value}мм ' \
                             f'+ {OpressovkaEK.nkt_opress(self)[0]} + НКТ + репер'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            rpk_nkt_select = f' для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                             f'{self.data_well.column_additional_wall_thickness.get_value}мм  +' \
                             f' {OpressovkaEK.nkt_opress(self)[0]} ' \
                             f'+ НКТ60мм + репер + НКТ60мм L- ' \
                             f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            rpk_nkt_select = f' для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                             f'{self.data_well.column_additional_wall_thickness.get_value}мм  + ' \
                             f'{OpressovkaEK.nkt_opress(self)[0]}' \
                             f'+ НКТ + репер + НКТ{self.data_well.nkt_diam}мм со снятыми фасками L- ' \
                             f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '

        return rpk_nkt_select

    def rir_with_pero_gl(self, paker_need_combo, plast_combo,
                         roof_rir_edit, sole_rir_edit, volume_cement, info_rir_edit='',
                         need_change_zgs_combo='Нет', plast_new_combo='',
                         fluid_new_edit='', pressure_new_edit='', pressure_zumpf_question='Не нужно',
                         diameter_paker=122, paker_khost=0, paker_depth=0):

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])

        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                sole_rir_edit > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: sole_rir_edit - self.data_well.head_column_additional.get_value}
        else:
            dict_nkt = {73: sole_rir_edit}

        volume_in_nkt, volume_in_ek = RirWindow.calc_buffer(self, roof_rir_edit, sole_rir_edit, dict_nkt)
        self.ozc_str_short, self.ozc_str, self.time_ozc = self.calculate_time_ozc(roof_rir_edit)
        uzm_pero_list = [
            [f' СПО пера до глубины {sole_rir_edit}м Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, sole_rir_edit)}  на тНКТ{nkt_diam}м до глубины {sole_rir_edit}м с '
             f'замером, шаблонированием '
             f'шаблоном {self.data_well.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sole_rir_edit, 1)],
            [f'УЦМ в интервале {roof_rir_edit}-{sole_rir_edit}м ({info_rir_edit})', None,
             f'Произвести установку  цементного моста в интервале {roof_rir_edit}-{sole_rir_edit}м {info_rir_edit} '
             f'в присутствии представителя УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None,
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
             f' (сухой цемент {round(volume_cement / 1.25, 1)}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме {volume_in_ek}м3, цементный '
             f'раствор в объеме {volume_cement}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме {volume_in_nkt}м3, тех. жидкостью  в '
             f'объёме {round(volume_vn_nkt(dict_nkt, roof_rir_edit, sole_rir_edit) - volume_in_nkt, 1)}м3. '
             f'Уравновешивание цементного раствора',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Приподнять перо до гл.{roof_rir_edit}м. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
             f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом '
             f'{self.data_well.fluid_work} (Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)],
            [None, None,
             f'Поднять перо на безопасную зону до гл. {roof_rir_edit - 300 if roof_rir_edit - 300 > 0 else 0}м '
             f'с доливом скважины '
             f'в объеме 0,3м3 тех. жидкостью '
             f'уд.весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на '
             f'гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
             f'телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать на Р={self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с'
             f' подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67],
        ]

        self.calculate_chemistry('цемент', volume_cement)
        if 'КР11' in self.data_well.type_kr and self.data_well.perforation_roof > roof_rir_edit:
            self.data_well.fluid_work = '1.18г/см3'
            uzm_pero_list.append([
                f'{self.data_well.fluid_work} в объеме '
                f'{well_volume(self, roof_rir_edit)}м3, обработанным ингибитором коррозии',
                None,
                f'В интервале {roof_rir_edit}-30м заполнить ствол скважины тех. жидкостью уд.в.'
                f' {self.data_well.fluid_work} в объеме '
                f'{well_volume(self, roof_rir_edit)}м3, обработанным ингибитором коррозии '
                f'{well_volume(self, roof_rir_edit) * 11}гр с удельной дозировкой 11гр/м3 ',
                None, None, None, None, None, None, None,
                'мастер КРС', 0.67])
        RirWindow.perf_new(self, roof_rir_edit, sole_rir_edit)
        # print(plast_combo)
        if self.data_well.head_column.get_value == 0:
            if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
                uzm_pero_list.pop(-1)
        else:
            if self.data_well.column_conductor_length.get_value > roof_rir_edit:
                uzm_pero_list.pop(-1)

        if need_change_zgs_combo == "Да":
            for row in Change_fluid_Window.fluid_change(self, plast_new_combo, fluid_new_edit,
                                                        pressure_new_edit):
                uzm_pero_list.append(row)
            uzm_pero_list.append([
                None, None,
                f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в '
                f'объеме '
                f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                f'уд.весом {self.data_well.fluid_work}',
                None, None, None, None, None, None, None,
                'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        else:
            uzm_pero_list.append([
                None, None,
                f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в объеме '
                f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                f'уд.весом {self.data_well.fluid_work}',
                None, None, None, None, None, None, None,
                'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        self.data_well.for_paker_list = None
        return uzm_pero_list

    def rir_with_pero(self, paker_need_combo, plast_combo,
                      roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo='Нет', plast_new_combo='',
                      fluid_new_edit='', pressure_new_edit='', pressure_zumpf_question='Не нужно',
                      diameter_paker=122, paker_khost=0, paker_depth=0):
        from .claySolution import ClayWindow

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])

        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                sole_rir_edit > self.data_well.head_column_additional.get_value:
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: sole_rir_edit - self.data_well.head_column_additional.get_value}
        else:
            dict_nkt = {73: sole_rir_edit}
        rir_list = RirWindow.need_paker(self, paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                        paker_depth, pressure_zumpf_question)

        volume_in_nkt, volume_in_ek = RirWindow.calc_buffer(self, roof_rir_edit, sole_rir_edit, dict_nkt)

        if paker_need_combo == "Нужно СПО":
            glin_list = [
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
                 f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме 5м3 + тех. воду '
                 f'в объёме {round(volume_vn_nkt(dict_nkt) - 5, 1)}м3. Закрыть затруб. '
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
                 f'в объеме не менее {well_volume(self, volume_vn_nkt(dict_nkt))}м3 с '
                 f'расходом жидкости не менее 8 л/с.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', well_volume_norm(24)]
            ]

            if volume_vn_nkt(dict_nkt) <= 5:
                glin_list[2] = [
                    None, None,
                    f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                    f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                    f'Продавить в НКТ остаток глинистого раствора в объеме '
                    f'{round(5 - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                    f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более '
                    f'{self.data_well.max_admissible_pressure.get_value}атм.',
                    None, None, None, None, None, None, None,
                    'мастер КРС', 0.5]

            for row in glin_list:
                rir_list.insert(-3, row)
            self.calculate_chemistry('глина', 5)
        else:
            rir_list = []

        rirPero_list = [
            [f'СПО пера до глубины {sole_rir_edit}м. Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, sole_rir_edit)}  на тНКТ{nkt_diam}м до глубины {sole_rir_edit}м '
             f'с замером, шаблонированием '
             f'шаблоном {self.data_well.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sole_rir_edit, 1)],
            [f'УЦМ в инт {roof_rir_edit}-{sole_rir_edit}м',
             None,
             f'Произвести цементную заливку с целью изоляции пласта {plast_combo}  в интервале '
             f'{roof_rir_edit}-{sole_rir_edit}м в присутствии '
             f'представителя УСРС и СТ',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None,
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
             f' (сухой цемент {round(volume_cement / 1.25, 1)}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме {volume_in_ek}м3,'
             f' цементный раствор в '
             f'объеме {volume_cement}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме {volume_in_nkt}м3, тех. жидкостью  в объёме '
             f'{round(volume_vn_nkt(dict_nkt, roof_rir_edit, sole_rir_edit) - volume_in_nkt, 1)}м3. '
             f'Уравновешивание цементного раствора',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Приподнять перо до гл.{roof_rir_edit}м. Закрыть трубное пространство. '
             f'Продавить по затрубному пространству '
             f'тех.жидкостью  при давлении не более {self.data_well.max_admissible_pressure.get_value}атм '
             f'(до получения технологического СТОП).',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
             f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом '
             f'{self.data_well.fluid_work} '
             f'(Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)],
            [None, None,
             f'Поднять перо на безопасную зону до гл.{roof_rir_edit - 300 if roof_rir_edit - 300 > 0 else 0}м с доливом '
             f'скважины в объеме 0,3м3 тех. жидкостью '
             f'уд.весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
             f'(плановый на гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
             f'телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67]
        ]
        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            rirPero_list.pop(-1)

        if paker_need_combo != "Нужно СПО":
            work_list_clay = ClayWindow.clay_solution_q(self, sole_rir_edit, 5)[1:-2]
            for row in work_list_clay[::-1]:
                rirPero_list.insert(1, row)

        if 'КР11' in self.data_well.type_kr and self.data_well.perforation_roof > roof_rir_edit:
            self.data_well.fluid_work = '1.18г/см3'
            rirPero_list.append([
                f'{self.data_well.fluid_work} в объеме '
                f'{well_volume(self, roof_rir_edit)}м3, обработанным ингибитором коррозии',
                None,
                f"В интервале {roof_rir_edit}-30м заполнить ствол скважины тех. жидкостью уд.в. 1,18г\см3 в объеме "
                f"{well_volume(self, roof_rir_edit)}м3, обработанным ингибитором коррозии "
                f"{well_volume(self, roof_rir_edit) * 11}гр с удельной дозировкой 11гр/м3 ",
                None, None, None, None, None, None, None,
                'мастер КРС', 0.67])

        for row in rirPero_list:
            rir_list.append(row)
        RirWindow.perf_new(self, roof_rir_edit, self.data_well.current_bottom)
        self.data_well.current_bottom = roof_rir_edit

        self.calculate_chemistry('цемент', volume_cement)

        if need_change_zgs_combo == "Да":
            for row in Change_fluid_Window.fluid_change(self, plast_new_combo, fluid_new_edit,
                                                        pressure_new_edit):
                rir_list.append(row)

        rir_list.append(
            [None, None,
             f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в объеме '
             f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
             f'уд.весом {self.data_well.fluid_work}', None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        self.data_well.for_paker_list = None
        return rir_list

    def pero_select(self, sole_rir_edit, pero_combo_combo='перо'):

        if self.data_well.column_additional is False or self.data_well.column_additional is True \
                and sole_rir_edit < self.data_well.head_column_additional.get_value:
            pero_select = f'{pero_combo_combo} + НКТ{self.data_well.nkt_diam} 20м + репер'

        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 \
                and sole_rir_edit > self.data_well.head_column_additional.get_value:
            pero_select = f'{pero_combo_combo} + НКТ60мм 20м + репер + НКТ60мм L- ' \
                          f'{round(sole_rir_edit - self.data_well.head_column_additional.get_value, 1)}м'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110 \
                and sole_rir_edit > self.data_well.head_column_additional.get_value:
            pero_select = f'{pero_combo_combo} + НКТ{self.data_well.nkt_diam}мм со снятыми фасками 20м + ' \
                          f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками' \
                          f' L- {sole_rir_edit - self.data_well.head_column_additional.get_value}м'
        return pero_select

    def need_paker(self, paker_need_combo, plast_combo, diameter_paker, paker_khost,
                   paker_depth, pressure_zumpf_question, rir_rpk_plast_true=False):

        from work_py.opressovka import OpressovkaEK

        try:
            paker_depth_zumpf = int(float(self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()))
        except Exception:
            paker_depth_zumpf = 0
        if paker_need_combo == 'Нужно СПО':

            rir_list = OpressovkaEK.paker_list(self, diameter_paker, paker_khost, paker_depth,
                                               pressure_zumpf_question, paker_depth_zumpf)
            if rir_rpk_plast_true is False:
                rir_q_list = [
                    f'насыщение 5м3. Определить Q {plast_combo} при Р=80-100атм. СКВ', None,
                    f'Произвести насыщение скважины в объеме 5м3. Определить приемистость '
                    f'{plast_combo} при Р=80-100атм '
                    f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                    f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
                    f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью'
                    f' увеличения '
                    f'приемистости по технологическому плану',
                    None, None, None, None, None, None, None,
                    'мастер КРС', 1.77]
                rir_list.insert(-3, rir_q_list)
        else:
            rir_list = []

        return rir_list

    def rir_paker(self, paker_need_combo, plast_combo,
                  roof_rir_edit, sole_rir_edit, pressure_zumpf_question='Не нужно',
                  diameter_paker=122, paker_khost=0, paker_depth=0):

        rir_list = self.need_paker(paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                   paker_depth, pressure_zumpf_question)

        rir_paker_list = [
            [f'РИР c пакером {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м',
             None,
             f'Произвести РИР {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м по '
             f'технологическому плану'
             f' подрядчика по РИР силами подрядчика по РИР '
             f'Перед спуском технологического пакера произвести испытание гидроякоря в присутствии '
             f'представителя '
             f'РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [f'Определение кровли', None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
             f'(плановый на '
             f'гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [f'Опрессовать на Р={self.data_well.max_admissible_pressure.get_value}атм', None,
             f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии '
             f'представителя заказчика '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до начала '
             f'работ) В случае негерметичности цементного моста дальнейшие работы согласовать с'
             f' Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Поднять компоновку РИР на тНКТ{self.data_well.nkt_diam}мм с глубины {roof_rir_edit}м '
             f'с доливом скважины в объеме '
             f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1.2)]
        ]
        RirWindow.perf_new(self, roof_rir_edit, sole_rir_edit)
        self.data_well.current_bottom = roof_rir_edit
        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            rir_paker_list.pop(-2)

        for row in rir_paker_list:
            rir_list.append(row)

        self.data_well.for_paker_list = None
        return rir_list

    def rir_paker_ovp(self, paker_need_combo, plast_combo,
                      roof_rir_edit, sole_rir_edit, pressure_zumpf_question='Не нужно',
                      diameter_paker=122, paker_khost=0, paker_depth=0):

        rir_list = self.need_paker(paker_need_combo, plast_combo, diameter_paker, paker_khost,
                                   paker_depth, pressure_zumpf_question)

        rir_paker_list = [
            [f'РИР c пакером пласта {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м',
             None,
             f'Произвести РИР ОВП пласта {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м по '
             f'технологическому плану'
             f' подрядчика по РИР силами подрядчика по РИР '
             f'Перед спуском технологического пакера произвести испытание гидроякоря в присутствии '
             f'представителя '
             f'РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
            [self.ozc_str_short, None,
             self.ozc_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', self.time_ozc],
            [f'Определение кровли', None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
             f'(плановый на '
             f'гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [f'Опрессовать на Р={self.data_well.max_admissible_pressure.get_value}атм', None,
             f'Опрессовать цементный мост на Р={self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии '
             f'представителя заказчика '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до начала '
             f'работ) В случае негерметичности цементного моста дальнейшие работы согласовать с'
             f' Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Поднять компоновку РИР на тНКТ{self.data_well.nkt_diam}мм с глубины {roof_rir_edit}м '
             f'с доливом скважины в объеме '
             f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1.2)]
        ]

        self.data_well.current_bottom = roof_rir_edit
        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            rir_paker_list.pop(-2)

        for row in rir_paker_list:
            rir_list.append(row)

        self.data_well.for_paker_list = None
        return rir_list

    def add_work(self):
        try:
            current_widget = self.tabWidget.currentWidget()
            plast_combo = str(current_widget.plast_combo.combo_box.currentText())
            self.rir_type_combo = str(current_widget.rir_type_combo.currentText())
            self.need_privyazka_q_combo = current_widget.need_privyazka_q_combo.currentText()
            roof_rir_edit = current_widget.roof_rir_edit.text().replace(',', '.')
            if roof_rir_edit != '':
                roof_rir_edit = int(float(roof_rir_edit))
            sole_rir_edit = current_widget.sole_rir_edit.text().replace(',', '.')
            if sole_rir_edit != '':
                sole_rir_edit = int(float(sole_rir_edit))

            if sole_rir_edit > self.data_well.current_bottom:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Подошва ЦМ ниже текущего забоя - {self.data_well.current_bottom}м')
                return
            paker_need_combo = current_widget.paker_need_combo.currentText()

            if paker_need_combo == 'без СПО':
                difference_date_well = self.difference_date_days(self.data_well.date_commissioning)
                difference_date_pressuar = self.difference_date_days(self.data_well.result_pressure_date)
                if difference_date_well > 365.25 * 20:
                    mes = QMessageBox.question(self, 'Критерии',
                                               f'Скважина в эксплуатации более {difference_date_well / 365:.0f}лет '
                                               f'Согласно технологических мероприятий по сокращению продолжительности'
                                               ' ТКРС от 31 мая 2025г, СПО пакера не нужно только при ПВЛГ и '
                                               'скважины с периодом эксплуатации более 20 лет')

                if difference_date_pressuar < 365 * 3:
                    mes = QMessageBox.question(self, 'Критерии',
                                               f'Последняя опрессовка ЭК более {difference_date_pressuar / 365:.0f}лет '
                                               f'Согласно технологических мероприятий по сокращению продолжительности'
                                               f' ТКРС от 31 мая 2025г, СПО пакера не нужно только при ПВЛГ и '
                                               f'(Отсутствие исследований по герметичности Э/К в течении последних 3 лет')

                if len(self.data_well.leakiness_interval) != 0:
                    mes = QMessageBox.question(self, 'Критерии', 'В скважине имеется НЭК, РИР без СПО пакер'
                                                                 ' не желателен')

                if mes == QMessageBox.StandardButton.No:
                    return

            pressure_zumpf_question = current_widget.pressure_zumpf_question_combo.currentText()
            need_change_zgs_combo = current_widget.need_change_zgs_combo.currentText()
            volume_cement = current_widget.cement_volume_line.text().replace(',', '.')
            if volume_cement != '':
                volume_cement = round(float(volume_cement), 1)
            if len(self.data_well.plast_project) != 0:
                plast_new_combo = current_widget.plast_new_combo.currentText()
            else:
                plast_new_combo = current_widget.plast_new_combo.text()
            fluid_new_edit = current_widget.fluid_new_edit.text().replace(',', '.')
            pressure_new_edit = current_widget.pressure_new_edit.text()
        except Exception as e :
            QMessageBox.warning(self, 'ОШИБКА', f'Введены не все данные {e}')

        self.ozc_str_short, self.ozc_str, self.time_ozc = self.calculate_time_ozc(roof_rir_edit)

        if paker_need_combo == 'Нужно СПО':
            diameter_paker = int(float(current_widget.diameter_paker_edit.text()))
            paker_khost = int(float(current_widget.paker_khost_edit.text()))
            paker_depth = int(float(current_widget.paker_depth_edit.text()))
            if self.check_true_depth_template(paker_depth) is False:
                return
            if self.true_set_paker(paker_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth) is False:
                return
            if pressure_zumpf_question == 'Да':
                if paker_depth + paker_khost > self.data_well.current_bottom:
                    mes = QMessageBox.critical(self, 'Ошибка', 'Компоновка ниже текущего забоя')
                    return

        else:
            diameter_paker = 122
            paker_khost = 10
            paker_depth = 1000

        if self.rir_type_combo == 'РИР на пере':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']
            if (plast_new_combo == '' or fluid_new_edit == '' or pressure_new_edit == '') and \
                    need_change_zgs_combo == 'Да':
                mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return

            work_list = self.rir_with_pero(paker_need_combo, plast_combo,
                                           roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo,
                                           plast_new_combo,
                                           fluid_new_edit, pressure_new_edit, pressure_zumpf_question,
                                           diameter_paker, paker_khost, paker_depth)

        elif self.rir_type_combo == 'УЦМ в глухой колонне':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']
            if (plast_new_combo == '' or fluid_new_edit == '' or pressure_new_edit == '') and \
                    need_change_zgs_combo == 'Да':
                QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return
            if paker_need_combo == 'Да':
                if self.check_true_depth_template(paker_depth) is False:
                    return
                if self.true_set_paker(paker_depth) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth) is False:
                    return
            info_rir_edit = ''

            work_list = self.rir_with_pero_gl(
                paker_need_combo, plast_combo, roof_rir_edit, sole_rir_edit, volume_cement, info_rir_edit,
                need_change_zgs_combo, plast_new_combo, fluid_new_edit, pressure_new_edit, pressure_zumpf_question,
                diameter_paker, paker_khost, paker_depth)



        elif self.rir_type_combo in ['РИР с пакером с 2С']:
            # print(paker_need_combo, plast_combo, roof_rir_edit, sole_rir_edit)
            work_list = self.rir_paker(paker_need_combo, plast_combo,
                                       roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                                       diameter_paker, paker_khost, paker_depth)
            self.calculate_chemistry('РИР 2С', 1)

        elif self.rir_type_combo in ['РИР ОВП с пакером']:
            # print(paker_need_combo, plast_combo, roof_rir_edit, sole_rir_edit)
            work_list = self.rir_paker_ovp(paker_need_combo, plast_combo,
                                           roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                                           diameter_paker, paker_khost, paker_depth)
            self.calculate_chemistry('РИР ОВП', 1)

        elif self.rir_type_combo == 'РИР с РПК':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpk(paker_need_combo, plast_combo,
                                     roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                                     diameter_paker, paker_khost, paker_depth)
            self.calculate_chemistry('РПК', 1)

        elif self.rir_type_combo == 'РИР с РПП':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpp(paker_need_combo, plast_combo,
                                     roof_rir_edit, sole_rir_edit, pressure_zumpf_question,
                                     diameter_paker, paker_khost, paker_depth)
            self.calculate_chemistry('РПП', volume_cement)

        elif self.rir_type_combo == 'РПП Силами ККТ':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_kkt(paker_need_combo, plast_combo,
                                     roof_rir_edit, pressure_zumpf_question,
                                     diameter_paker, paker_khost, paker_depth)

        elif self.rir_type_combo == 'РИР с РПП + ЦМ':
            work_list = self.rir_rpp_cm(paker_need_combo, plast_combo, roof_rir_edit, sole_rir_edit, volume_cement,
                                        need_change_zgs_combo, plast_new_combo, fluid_new_edit, pressure_new_edit,
                                        pressure_zumpf_question, diameter_paker, paker_khost, paker_depth)

        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()

    def calc_buffer(self, roof, sole, dict_nkt):
        volume_in_nkt = round(100 * volume_vn_nkt(dict_nkt, roof, sole) / 1000, 1)
        nkt = min(list(map(int, dict_nkt.keys()))) / 100
        volume_out_nkt = nkt ** 2 * 3.14 / 4 / 100
        volume_ek = volume_vn_ek(self, sole) / 1000
        volume_in_ek = round(100 * volume_ek - volume_out_nkt, 1)
        return volume_in_nkt, volume_in_ek

    def rir_izvelPaker(self):

        paker_izv_paker, ok = QInputDialog.getInt(None, 'Глубина извлекаемого пакера',
                                                  'Введите глубину установки извлекаемого пакера ',
                                                  int(self.data_well.perforation_roof - 50), 0,
                                                  int(self.data_well.bottom_hole_drill.get_value))

        data_list.paker_izv_paker = paker_izv_paker
        rir_list = [[f'СПО пакера извлекаемый до глубины {paker_izv_paker}м',
                     None,
                     f'Спустить  пакера извлекаемый компании НЕОИНТЕХ +НКТ 20м + реперный патрубок 2м на тНКТ до'
                     f' глубины {paker_izv_paker}м с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм.'
                     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                     None, None, None, None, None, None, None,
                     'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(paker_izv_paker, 1.2)],
                    [f'Привязка', None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
                     f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
                     None, None, None, None, None, None, None,
                     'Мастер КРС, подрядчик по ГИС', 4],
                    [None, None,
                     f'Произвести установку извлекаемого пакера на глубине {paker_izv_paker}м по технологическому '
                     f'плану работ плана '
                     f'подрядчика.',
                     None, None, None, None, None, None, None,
                     'Мастер КРС, подрядчик по ГИС', 4]]

        sand_question = QMessageBox.question(None, 'Отсыпка', 'Нужна ли отсыпка головы пакера?')
        if sand_question == QMessageBox.StandardButton.Yes:

            filling_list = [
                [None, None,
                 f'Поднять ИУГ до глубины {paker_izv_paker - 120}м с доливом тех жидкости в '
                 f'объеме  {round(120 * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4],
                [f'отсыпка в инт. {paker_izv_paker - 20} - {paker_izv_paker}  в объеме'
                 f' {round(well_volume(self, paker_izv_paker) / paker_izv_paker * 1000 * (20), 0)}л',
                 None, f'Произвести отсыпку кварцевым песком в инт. {paker_izv_paker - 20} - {paker_izv_paker} '
                       f' в объеме {round(well_volume(self, paker_izv_paker) / paker_izv_paker * 1000 * (20), 0)}л '
                       f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 3.5],
                [f'Ожидание 4 часа.', None, f'Ожидание оседания песка 4 часа.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 4],
                [None, None,
                 f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста (плановый забой - '
                 f'{paker_izv_paker - 20}м).'
                 f' Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в '
                 f'песчаный мост).',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.2],
                [None, None,
                 f'В случае если кровля песчаного моста на гл.{paker_izv_paker - 20}м дальнейшие работы продолжить'
                 f' дальше по плану'
                 f'В случае пеcчаного моста ниже гл.{paker_izv_paker - 20}м работы повторить с корректировкой объема и '
                 f'технологических глубин.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять ИУГ с глубины {paker_izv_paker - 20}м с доливом тех '
                 f'жидкости в объеме  {round(paker_izv_paker * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4]]

            for row in filling_list:
                rir_list.append(row)
            self.data_well.current_bottom_second = paker_izv_paker
            self.data_well.current_bottom = paker_izv_paker - 20
        else:
            rir_list.append([None, None,
                             f'Поднять ИУГ c глубины {paker_izv_paker}м с доливом тех жидкости в объеме '
                             f'{round(paker_izv_paker * 1.12 / 1000, 1)}м3 уд.весом {self.data_well.fluid_work}',
                             None, None, None, None, None, None, None,
                             'Мастер КРС, подрядчик по ГИС', 4])
            self.data_well.current_bottom_second = self.data_well.current_bottom
            self.data_well.current_bottom = paker_izv_paker
        self.data_well.for_paker_list = None
        return rir_list

    def izvlech_paker(self):

        rir_list = [
            [f'СПО {RirWindow.pero_select(self, self.data_well.current_bottom).replace("перо", "перо-110мм")} до '
             f'глубины {round(self.data_well.current_bottom, 0)}м', None,
             f'Спустить  {RirWindow.pero_select(self, self.data_well.current_bottom).replace("перо", "перо-110мм")} '
             f'на НКТ{self.data_well.nkt_diam}мм до '
             f'глубины {round(self.data_well.current_bottom, 0)}м с замером, шаблонированием шаблоном '
             f'{self.data_well.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(self.data_well.current_bottom, 1)],
            [f'Вымыв песка до гл.{data_list.paker_izv_paker - 10}',
             None,
             f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной промывкой '
             f'по круговой циркуляции '
             f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{data_list.paker_izv_paker - 10}м. \n'
             f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Поднять {RirWindow.pero_select(self, self.data_well.current_bottom)} НКТ{self.data_well.nkt_diam}мм с глубины '
             f'{data_list.paker_izv_paker - 10}м с доливом '
             f'скважины'
             f' в объеме {round((data_list.paker_izv_paker - 10) * 1.12 / 1000, 1)}м3 тех. '
             f'жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(data_list.paker_izv_paker - 10, 1)]]

        emer_list = [
            [f'СПО лов. инст до до Н= {self.data_well.current_bottom}', None,
             f'Спустить с замером ловильный инструмент на НКТ до Н= {self.data_well.current_bottom}м с замером. ',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(self.data_well.current_bottom, 1)],
            [f'Вымыв песка до {data_list.paker_izv_paker}м. Извлечение пакера', None,
             f'Произвести нормализацию (вымыв кварцевого песка) на ловильном инструменте до глубины '
             f'{data_list.paker_izv_paker}м обратной '
             f'промывкой уд.весом {self.data_well.fluid_work} \n'
             f'Произвести  ловильный работы при представителе заказчика на глубине {data_list.paker_izv_paker}м.',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(data_list.paker_izv_paker, 1)],
            [None, None,
             f'Расходить и поднять компоновку НКТ{self.data_well.nkt_diam}мм с глубины {data_list.paker_izv_paker}м с '
             f'доливом скважины в объеме {round(data_list.paker_izv_paker * 1.12 / 1000, 1)}м3 тех. жидкостью '
             f'уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(data_list.paker_izv_paker, 1)]]
        for row in emer_list:
            rir_list.append(row)

        self.data_well.current_bottom, ok = QInputDialog.getInt(None, 'Глубина забоя',
                                                                'Введите глубину текущего забоя после извлечения',
                                                                int(self.data_well.current_bottom), 0,
                                                                int(self.data_well.bottom_hole_drill.get_value))
        self.data_well.for_paker_list = None
        return rir_list
