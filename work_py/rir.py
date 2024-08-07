import well_data
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget, QPushButton, \
    QMainWindow, QTabWidget
from work_py.alone_oreration import volume_vn_ek, well_volume, volume_vn_nkt
from .change_fluid import Change_fluid_Window
from .opressovka import OpressovkaEK, TabPage_SO

from main import MyWindow
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from .acid_paker import CheckableComboBox


class TabPage_SO_rir(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.paker_need_labelType = QLabel("необходимость спо пакера \nдля опрессовки ЭК и определения Q", self)
        self.paker_need_Combo = QComboBox(self)
        self.paker_need_Combo.addItems(['Нужно СПО', 'без СПО'])

        self.rir_type_Label = QLabel("Вид РИР", self)
        self.rir_type_Combo = QComboBox(self)
        self.rir_type_Combo.addItems(['', 'РИР на пере', 'УЦМ в глухой колонне',
                                      'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП'])
        plast_work = ['']
        plast_work.extend(well_data.plast_work)

        if well_data.leakiness:
            for nek in list(well_data.dict_leakiness['НЭК']['интервал'].keys()):
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

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)
        self.diametr_paker_edit.setValidator(self.validator_int)

        self.paker_khost_Label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator_int)
        self.paker_khost_edit.setText('10')

        self.paker_depth_Label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator_int)
        # self.paker_depth_edit.textChanged.connect(self.update_plast_edit)

        self.cement_volume_label = QLabel('Объем цемента')
        self.cement_volume_line = QLineEdit(self)

        if len(well_data.plast_work) != 0:
            pakerDepth = well_data.perforation_sole - 20
            if pakerDepth != '':
                self.paker_depth_edit.setText(str(int(pakerDepth)))
        else:
            if well_data.leakiness:
                pakerDepth = min([float(nek.split('-')[0]) - 10
                                  for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()])

        self.paker_depth_zumpf_Label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator_int)

        self.pressureZUMPF_question_Label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressureZUMPF_question_QCombo = QComboBox(self)
        self.pressureZUMPF_question_QCombo.addItems(['Нет', 'Да'])
        self.paker_need_Combo.currentTextChanged.connect(self.update_paker)

        self.pressureZUMPF_question_QCombo.currentTextChanged.connect(self.update_pakerZUMPF)

        self.need_privyazka_Label = QLabel("Привязка оборудования", self)
        self.need_privyazka_QCombo = QComboBox()
        self.need_privyazka_QCombo.addItems(['Нет', 'Да'])

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])
        if len(well_data.plast_work) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator_int)

        if len(well_data.plast_project) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(well_data.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.paker_need_labelType, 4, 1)
        self.grid.addWidget(self.paker_need_Combo, 5, 1)

        self.grid.addWidget(self.rir_type_Label, 4, 2)
        self.grid.addWidget(self.rir_type_Combo, 5, 2)
        self.grid.addWidget(self.plast_label, 4, 3)
        self.grid.addWidget(self.plast_combo, 5, 3)
        self.grid.addWidget(self.roof_rir_label, 4, 4)
        self.grid.addWidget(self.roof_rir_edit, 5, 4)
        self.grid.addWidget(self.sole_rir_LabelType, 4, 5)
        self.grid.addWidget(self.sole_rir_edit, 5, 5)

        self.grid.addWidget(self.diametr_paker_labelType, 1, 1)
        self.grid.addWidget(self.diametr_paker_edit, 2, 1)

        self.grid.addWidget(self.paker_khost_Label, 1, 2)
        self.grid.addWidget(self.paker_khost_edit, 2, 2)

        self.grid.addWidget(self.paker_depth_Label, 1, 3)
        self.grid.addWidget(self.paker_depth_edit, 2, 3)

        self.grid.addWidget(self.pressureZUMPF_question_Label, 1, 4)
        self.grid.addWidget(self.pressureZUMPF_question_QCombo, 2, 4)

        self.grid.addWidget(self.need_privyazka_Label, 1, 6)
        self.grid.addWidget(self.need_privyazka_QCombo, 2, 6)

        self.grid.addWidget(self.need_change_zgs_label, 9, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

        self.grid.addWidget(self.plast_new_label, 9, 3)
        self.grid.addWidget(self.plast_new_combo, 10, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.grid.addWidget(self.pressuar_new_label, 9, 5)
        self.grid.addWidget(self.pressuar_new_edit, 10, 5)

        self.cement_volume_line.setValidator(self.validator_float)

        self.grid.addWidget(self.cement_volume_label, 4, 6)
        self.grid.addWidget(self.cement_volume_line, 5, 6)

        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)
        self.need_change_zgs_combo.setCurrentIndex(1)
        self.rir_type_Combo.currentTextChanged.connect(self.update_rir_type)

        self.paker_depth_edit.textChanged.connect(self.update_depth_paker)
        self.roof_rir_edit.textChanged.connect(self.update_volume_cement)
        self.sole_rir_edit.textChanged.connect(self.update_volume_cement)

        self.paker_need_Combo.setCurrentIndex(1)
        self.paker_need_Combo.setCurrentIndex(0)

    def update_change_fluid(self, index):
        if index == 'Да':

            cat_h2s_list_plan = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                               well_data.plast_project if well_data.dict_category.get(plast) and
                                               well_data.dict_category[plast]['отключение'] == 'планируемый']))

            if len(cat_h2s_list_plan) != 0:
                plast = well_data.plast_project[0]
                self.pressuar_new_edit.setText(f'{well_data.dict_category[plast]["по давлению"].data_pressuar}')
            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressuar_new_label, 9, 5)
            self.grid.addWidget(self.pressuar_new_edit, 10, 5)
        else:
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)

    def update_pakerZUMPF(self, index):
        from .opressovka import TabPage_SO

        if index == 'Да':
            if len(well_data.plast_work) != 0:
                paker_depth_zumpf = well_data.perforation_sole + 10
            else:
                if well_data.leakiness:
                    paker_depth_zumpf = max([float(nek.split('-')[0]) + 10
                                           for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()])
            self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid.addWidget(self.paker_depth_zumpf_Label, 1, 5)
            self.grid.addWidget(self.paker_depth_zumpf_edit, 2, 5)
        elif index == 'Нет':
            self.paker_depth_zumpf_Label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)

        if well_data.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = well_data.current_bottom - int(paker_depth)
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 10
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(float(paker_depth)))}')

    def update_depth_paker(self):
        from work_py.opressovka import TabPage_SO
        paker_depth = self.paker_depth_edit.text()
        if paker_depth != '':
            self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(float(paker_depth)))}')

    def update_rir_type(self, index):
        if index in 'РИР с пакером с 2С':
            self.need_change_zgs_label.setParent(None)
            self.need_change_zgs_combo.setParent(None)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
            self.paker_depth_edit.setText(f'{well_data.perforation_roof - 30}')
            self.roof_rir_edit.setText(f'{well_data.perforation_roof - 30}')
            self.sole_rir_edit.setText(f'{well_data.current_bottom}')
        elif index == 'РИР с РПК' or index == 'РИР с РПП':
            self.need_change_zgs_label.setParent(None)
            self.need_change_zgs_combo.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)
            self.paker_depth_edit.setText(f'{well_data.perforation_roof - 30}')
            self.roof_rir_edit.setText(f'{well_data.perforation_roof - 10}')
            if index == 'РИР с РПП':
                self.sole_rir_edit.setText(f'{self.roof_rir_edit.text()}')
                self.paker_depth_edit.setText(f'{well_data.perforation_roof - 30}')
            elif index == 'РИР с РПК':
                self.sole_rir_edit.setText(f'{well_data.perforation_roof - 10}')
                self.paker_depth_edit.setText(f'{well_data.perforation_roof - 10}')
        elif index in ['РИР на пере',
                       'УЦМ в глухой колонне']:  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            self.grid.addWidget(self.cement_volume_label, 4, 6)
            self.grid.addWidget(self.cement_volume_line, 5, 6)

            self.grid.addWidget(self.need_change_zgs_label, 9, 2)
            self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressuar_new_label, 9, 5)
            self.grid.addWidget(self.pressuar_new_edit, 10, 5)
            self.roof_rir_edit.setText(f'{well_data.perforation_roof - 50}')
            self.sole_rir_edit.setText(f'{well_data.current_bottom}')
            self.paker_depth_edit.setText(f'{well_data.perforation_roof - 30}')

    def update_volume_cement(self):
        if self.roof_rir_edit.text() != '' and self.sole_rir_edit.text() != '':
            self.cement_volume_line.setText(
                f'{round(volume_vn_ek(float(self.roof_rir_edit.text())) * (float(self.sole_rir_edit.text()) - float(self.roof_rir_edit.text())) / 1000, 1)}')

    def update_paker(self, index):

        if index == 'Нужно СПО':
            self.grid.addWidget(self.diametr_paker_labelType, 1, 1)
            self.grid.addWidget(self.diametr_paker_edit, 2, 1)

            self.grid.addWidget(self.paker_khost_Label, 1, 2)
            self.grid.addWidget(self.paker_khost_edit, 2, 2)

            self.grid.addWidget(self.paker_depth_Label, 1, 3)
            self.grid.addWidget(self.paker_depth_edit, 2, 3)

            self.grid.addWidget(self.pressureZUMPF_question_Label, 1, 4)
            self.grid.addWidget(self.pressureZUMPF_question_QCombo, 2, 4)
            # if self.pressureZUMPF_question_QCombo.currentText() == 'Да':
            #     self.paker_depth_zumpf_edit.setText(f'{sole_plast + 20}')
        else:
            self.diametr_paker_labelType.setParent(None)
            self.diametr_paker_edit.setParent(None)
            self.paker_khost_Label.setParent(None)
            self.paker_khost_edit.setParent(None)
            self.paker_depth_Label.setParent(None)
            self.paker_depth_edit.setParent(None)
            try:
                self.pressureZUMPF_question_Label.setParent(None)
                self.pressureZUMPF_question_QCombo.setParent(None)

                self.paker_depth_zumpf_Label.setParent(None)
                self.paker_depth_zumpf_edit.setParent(None)
            except:
                pass

    def update_plast_edit(self):

        dict_perforation = well_data.dict_perforation

        plasts = well_data.texts

        roof_plast = well_data.current_bottom
        sole_plast = 0
        for plast_sel in plasts:
            for plast in well_data.plast_work:
                if plast_sel == plast:
                    try:
                        if roof_plast >= dict_perforation[plast]['кровля']:
                            roof_plast = dict_perforation[plast]['кровля']
                        if sole_plast <= dict_perforation[plast]['подошва']:
                            sole_plast = dict_perforation[plast]['подошва']
                    except:
                        pass

            if well_data.leakiness:
                for nek in list(well_data.dict_leakiness['НЭК']['интервал'].keys()):

                    if nek in plast_sel:
                        if roof_plast >= float(nek.split('-')[0]):
                            roof_plast = float(nek.split('-')[0])
                            # print(f' кровля {roof_plast}')
                        if sole_plast <= float(nek.split('-')[1]):
                            sole_plast = float(nek.split('-')[1])
                        # print(nek, roof_plast, sole_plast)
        self.roof_rir_edit.setText(f"{int(roof_plast - 30)}")
        self.paker_depth_edit.setText(f"{int(roof_plast - 20)}")
        if sole_plast + 20 > well_data.current_bottom:
            self.sole_rir_edit.setText(f"{well_data.current_bottom}")
        else:
            self.sole_rir_edit.setText(f"{sole_plast + 20}")


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_rir(self), 'Ремонтно-Изоляционные работы')


class RirWindow(QMainWindow):
    work_rir_window = None

    def __init__(self, ins_ind, table_widget, parent=None):

        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def rir_rpp(self, paker_need_Combo, plast_combo,
                roof_rir_edit, sole_rir_edit, pressureZUMPF_question,
                diametr_paker=122, paker_khost=0, paker_depth=0):

        rir_list = self.need_paker(paker_need_Combo, plast_combo, diametr_paker, paker_khost,
                                   paker_depth, pressureZUMPF_question, True)

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True
        else:
            rir_rpk_plast_true = False

        rir_work_list = [
            [f'СПО РПП до глубины {roof_rir_edit}м', None,
             f'Спустить пакер глухой {self.rpk_nkt(roof_rir_edit)}  на тНКТ{well_data.nkt_diam}мм '
             f'до глубины {roof_rir_edit}м '
             f'с замером, шаблонированием шаблоном {well_data.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии '
             f'представителя РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(roof_rir_edit, 1.2)],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером  '
             f'{well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'опрессовать НКТ на 200атм', None,
             f'При наличии циркуляции опрессовать НКТ на 200атм '
             f'в присутствии порядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.5 + 0.6],
            [f'установка РПП на {roof_rir_edit}м', None,
             f'Произвести установку глухого пакера  для изоляции {plast_combo} по технологическому плану '
             f'подрядчика по РИР силами подрядчика по РИР '
             f'с установкой пакера  на глубине {roof_rir_edit}м',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],

            [
                f'{"".join([f"Опрессовать на Р={well_data.max_admissible_pressure._value}атм" if rir_rpk_plast_true is False else ""])}',
                None,
                f'{"".join([f"Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика" if rir_rpk_plast_true is False else ""])} '
                f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                f'подтверждением за 2 часа до начала работ) ',
                None, None, None, None, None, None, None,
                'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Поднять стыковочное устройство с глубины {roof_rir_edit}м с доливом скважины в объеме '
             f'{round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work} ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1.2)]]

        for row in rir_work_list:
            rir_list.append(row)

        well_data.current_bottom = roof_rir_edit
        self.perf_new(roof_rir_edit, roof_rir_edit + 1)
        well_data.forPaker_list = None
        # print(f'текущий забой {well_data.current_bottom}')
        return rir_list

    def rir_rpk(self, paker_need_Combo, plast_combo,
                roof_rir_edit, sole_rir_edit, pressureZUMPF_question='Не нужно',
                diametr_paker=122, paker_khost=0, paker_depth=0):

        rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
        rir_rpk_plast_true = False
        if rir_rpk_question == QMessageBox.StandardButton.Yes:
            rir_rpk_plast_true = True

        rir_list = self.need_paker(paker_need_Combo, plast_combo, diametr_paker, paker_khost,
                                   paker_depth, pressureZUMPF_question, rir_rpk_plast_true)

        if rir_rpk_plast_true:
            rir_q_list = [
                [f'посадить пакер на глубину {roof_rir_edit}м'
                    , None,
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

            if self.rir_type_Combo not in ['РИР с РПП']:
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
             f'Спустить   пакера РПК {self.rpk_nkt(roof_rir_edit)}  на тНКТ{well_data.nkt_diam}мм до '
             f'глубины {roof_rir_edit}м с '
             f'замером, шаблонированием шаблоном {well_data.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя '
             f'РИР или УСРСиСТ.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(roof_rir_edit, 1.2)],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
             f'{well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'опрессовать НКТ на 200атм', None,
             f'При наличии циркуляции опрессовать НКТ на 200атм '
             f'в присутствии порядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [f'РИР {plast_combo} с установкой пакера РПК на глубине {roof_rir_edit}м ', None,
             f'Произвести РИР {plast_combo} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
             f'с установкой пакера РПК на глубине {roof_rir_edit}м',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
            [f'ОЗЦ 16-24 часа', None,
             f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
             f'технологического "СТОП" ОЗЦ без давления.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 16],
            [
                f'{"".join([f"Опрессовать на Р={well_data.max_admissible_pressure._value}атм" if rir_rpk_plast_true is False else ""])}',
                None,
                f'{"".join([f"Опрессовать цементный мост на Р={well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика" if rir_rpk_plast_true is False else ""])} '
                f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                f'подтверждением за 2 часа '
                f'до начала работ) ',
                None, None, None, None, None, None, None,
                'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
            [None, None,
             f'Во время ОЗЦ поднять стыковочное устройство с глубины {roof_rir_edit}м с доливом скважины в объеме '
             f'{round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work} ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1)]]
        for row in rir_work_list:
            rir_list.append(row)
        self.perf_new(roof_rir_edit, well_data.current_bottom)
        well_data.current_bottom = roof_rir_edit
        well_data.forPaker_list = None
        return rir_list

    def perf_new(self, roof_rir, sole_rir):

        for plast in well_data.plast_all:
            for interval in list((well_data.dict_perforation[plast]['интервал'])):
                if roof_rir <= interval[0] <= sole_rir:
                    well_data.dict_perforation[plast]['отключение'] = True
                if well_data.dict_perforation[plast]['отключение'] is False:
                    if interval[0] < well_data.perforation_roof:
                        well_data.perforation_roof = interval[0]
                    elif interval[1] > well_data.perforation_sole:
                        well_data.perforation_sole = interval[1]

        well_data.plast_work = []
        for plast in well_data.plast_all:
            if well_data.dict_perforation[plast]['отключение'] is False:
                well_data.plast_work.append(plast)

        if len(well_data.dict_leakiness) != 0:
            for nek in list(well_data.dict_leakiness['НЭК']['интервал'].keys()):
                # print(roof_rir, float(nek.split('-')[0]), sole_rir)
                if roof_rir <= float(nek.split('-')[0]) <= sole_rir:
                    well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение'] = True
            # print(f"при {well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение']}")
        if well_data.column_additional:
            if well_data.current_bottom <= well_data.shoe_column_additional._value:
                well_data.open_trunk_well = False
        else:
            if well_data.current_bottom <= well_data.shoe_column._value:
                well_data.open_trunk_well = False

    def rpk_nkt(self, paker_depth):

        from .opressovka import OpressovkaEK
        well_data.nkt_opressTrue = False

        if well_data.column_additional is False or well_data.column_additional is True and \
                paker_depth < well_data.head_column_additional._value:
            rpk_nkt_select = f' для ЭК {well_data.column_diametr._value}мм х ' \
                             f'{well_data.column_wall_thickness._value}мм ' \
                             f'+ {OpressovkaEK.nkt_opress(self)[0]} + НКТ + репер'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            rpk_nkt_select = f' для ЭК {well_data.column_additional_diametr._value}мм х ' \
                             f'{well_data.column_additional_wall_thickness._value}мм  +' \
                             f' {OpressovkaEK.nkt_opress(self)[0]} ' \
                             f'+ НКТ60мм + репер + НКТ60мм L- ' \
                             f'{round(paker_depth - well_data.head_column_additional._value, 0)}м '
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and\
                paker_depth > well_data.head_column_additional._value:
            rpk_nkt_select = f' для ЭК {well_data.column_additional_diametr._value}мм х ' \
                             f'{well_data.column_additional_wall_thickness._value}мм  + ' \
                             f'{OpressovkaEK.nkt_opress(self)[0]}' \
                             f'+ НКТ + репер + НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                             f'{round(paker_depth - well_data.head_column_additional._value, 0)}м '

        return rpk_nkt_select

    def rirWithPero_gl(self, paker_need_Combo, plast_combo,
                       roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo='Нет', plast_new_combo='',
                       fluid_new_edit='', pressuar_new_edit='', pressureZUMPF_question='Не нужно',
                       diametr_paker=122, paker_khost=0, paker_depth=0):

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])

        if well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                sole_rir_edit > well_data.head_column_additional._value:
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: sole_rir_edit - well_data.head_column_additional._value}
        else:
            dict_nkt = {73: sole_rir_edit}

        volume_in_nkt, volume_in_ek = RirWindow.calc_buffer(self, roof_rir_edit, sole_rir_edit, dict_nkt)

        uzmPero_list = [
            [f' СПО пера до глубины {sole_rir_edit}м Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, sole_rir_edit)}  на тНКТ{nkt_diam}м до глубины {sole_rir_edit}м с '
             f'замером, шаблонированием '
             f'шаблоном {well_data.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sole_rir_edit, 1)],
            [f'УЦМ в интервале {roof_rir_edit}-{sole_rir_edit}м', None,
             f'Произвести установку  цементного моста в интервале {roof_rir_edit}-{sole_rir_edit}м в присутствии '
             f'представителя УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None,
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {round(volume_cement / 1.25, 1)}м3'
             f' (сухой цемент {volume_cement}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме {volume_in_ek}м3, цементный '
             f'раствор в объеме {round(volume_cement / 1.25, 1)}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме {volume_in_nkt}м3, тех. жидкостью  в '
             f'объёме {round(volume_vn_nkt(dict_nkt) - volume_in_nkt, 1)}м3. '
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
             f'{well_data.fluid_work} (Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)],
            [None, None,
             f'Поднять перо на безопасную зону до гл. {roof_rir_edit - 300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
             f'уд.весом {well_data.fluid_work}.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [f'ОЗЦ - 23 час', None,
             f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
             f'ОЗЦ без давления.',
             None, None, None, None, None, None, None,
             'мастер КРС', 24],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на '
             f'гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
             f'телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать на Р={well_data.max_admissible_pressure._value}атм',
             None,
             f'Опрессовать цементный мост на Р={well_data.max_admissible_pressure._value}атм в '
             f'присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с'
             f' подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67],

        ]
        RirWindow.perf_new(self, roof_rir_edit, sole_rir_edit)
        # print(plast_combo)
        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            uzmPero_list.pop(-2)

        well_data.current_bottom = roof_rir_edit

        if need_change_zgs_combo == "Да":
            for row in Change_fluid_Window.fluid_change(self, plast_new_combo, fluid_new_edit,
                                                        pressuar_new_edit):
                uzmPero_list.insert(-1, row)
            uzmPero_list.append([None, None,
                                 f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в '
                                 f'объеме '
                                 f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                                 f'уд.весом {well_data.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        else:
            uzmPero_list.append([None, None,
                                 f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в объеме '
                                 f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                                 f'уд.весом {well_data.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        well_data.forPaker_list = None
        return uzmPero_list

    def rirWithPero(self, paker_need_Combo, plast_combo,
                    roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo='Нет', plast_new_combo='',
                    fluid_new_edit='', pressuar_new_edit='', pressureZUMPF_question='Не нужно',
                    diametr_paker=122, paker_khost=0, paker_depth=0):

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])

        if well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                sole_rir_edit > well_data.head_column_additional._value:
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: sole_rir_edit - well_data.head_column_additional._value}
        else:
            dict_nkt = {73: sole_rir_edit}
        rir_list = RirWindow.need_paker(self, paker_need_Combo, plast_combo, diametr_paker, paker_khost,
                                        paker_depth, pressureZUMPF_question)

        volume_in_nkt, volume_in_ek = RirWindow.calc_buffer(self, roof_rir_edit, sole_rir_edit, dict_nkt)

        if paker_need_Combo == "Нужно СПО":
            glin_list = [
                [None, None,
                 f'По результатам определения приёмистости выполнить следующие работы: \n'
                 f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке гдинистого раствора '
                 f'(по согласованию с ГС и ПТО {well_data.contractor} и заказчика). \n'
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
                 f'{well_data.max_admissible_pressure._value}атм.',
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
                 'мастер КРС', well_volume_norm(24)]
            ]

            if volume_vn_nkt(dict_nkt) <= 5:
                glin_list[2] = [None, None,
                                f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                                f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                                f'Продавить в НКТ остаток глинистого раствора в объеме '
                                f'{round(5 - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                                f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более {well_data.max_admissible_pressure._value}атм.',
                                None, None, None, None, None, None, None,
                                'мастер КРС', 0.5]

            for row in glin_list:
                rir_list.insert(-3, row)
        else:
            rir_list = []

        rirPero_list = [
            [f'СПО пера до глубины {sole_rir_edit}м. Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, sole_rir_edit)}  на тНКТ{nkt_diam}м до глубины {sole_rir_edit}м '
             f'с замером, шаблонированием '
             f'шаблоном {well_data.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
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
             f'Приготовить цементный раствор у=1,82г/см3 в объёме {round(volume_cement / 1.25, 1)}м3'
             f' (сухой цемент{round(volume_cement, 1)}т) ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме {volume_in_ek}м3,'
             f' цементный раствор в '
             f'объеме {round(volume_cement / 1.25, 1)}м3, '
             f'довести тех.жидкостью у=1,00г/см3 в объёме {volume_in_nkt}м3, тех. жидкостью  в объёме '
             f'{round(volume_vn_nkt(dict_nkt) - volume_in_nkt, 1)}м3. '
             f'Уравновешивание цементного раствора',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Приподнять перо до гл.{roof_rir_edit}м. Закрыть трубное простанство. '
             f'Продавить по затрубному пространству '
             f'тех.жидкостью  при давлении не более {well_data.max_admissible_pressure._value}атм '
             f'(до получения технологического СТОП).',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
             f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом '
             f'{well_data.fluid_work} '
             f'(Полуторакратный объем НКТ) '
             f'с расходом жидкости 8л/с (срезка) до чистой воды.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(16)],
            [None, None,
             f'Поднять перо на безопасную зону до гл. {roof_rir_edit - 300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
             f'уд.весом {well_data.fluid_work}.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [None, None,
             f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
             f'ОЗЦ без давления.',
             None, None, None, None, None, None, None,
             'мастер КРС', 24],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
             f'(плановый на гл. {roof_rir_edit}м'
             f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной '
             f'телефонограммой.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Опрессовать цементный мост на Р={well_data.max_admissible_pressure._value}атм',
             None,
             f'Опрессовать цементный мост на Р={well_data.max_admissible_pressure._value}атм в присутствии представителя '
             f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до '
             f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
             f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.67],
        ]

        for row in rirPero_list:
            rir_list.append(row)
        RirWindow.perf_new(self, roof_rir_edit, well_data.current_bottom)
        well_data.current_bottom = roof_rir_edit

        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            rir_list.pop(-1)

        if need_change_zgs_combo == "Да":
            for row in Change_fluid_Window.fluid_change(self, plast_new_combo, fluid_new_edit,
                                                        pressuar_new_edit):
                rir_list.insert(-1, row)

        rir_list.append([None, None,
                         f'Поднять перо на тНКТ{nkt_diam}м с глубины {roof_rir_edit}м с доливом скважины в объеме '
                         f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
                         f'уд.весом {well_data.fluid_work}',
                         None, None, None, None, None, None, None,
                         'мастер КРС', liftingNKT_norm(roof_rir_edit, 1)])
        well_data.forPaker_list = None
        return rir_list

    def pero_select(self, sole_rir_edit, pero_combo_QCombo='перо'):

        if well_data.column_additional is False or well_data.column_additional is True \
                and sole_rir_edit < well_data.head_column_additional._value:
            pero_select = f'{pero_combo_QCombo} + опрессовочное седло + НКТ{well_data.nkt_diam} 20м + репер'

        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 \
                and sole_rir_edit > well_data.head_column_additional._value:
            pero_select = f'{pero_combo_QCombo} + опрессовочное седло + НКТ60мм 20м + репер + НКТ60мм L- ' \
                          f'{round(sole_rir_edit - well_data.head_column_additional._value, 1)}м'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 \
                and sole_rir_edit > well_data.head_column_additional._value:
            pero_select = f'{pero_combo_QCombo} + опрессовочное седло + НКТ{well_data.nkt_diam}мм со снятыми фасками 20м + ' \
                          f'НКТ{well_data.nkt_diam}мм со снятыми фасками' \
                          f' L- {sole_rir_edit - well_data.head_column_additional._value}м'
        return pero_select

    def need_paker(self, paker_need_Combo, plast_combo, diametr_paker, paker_khost,
                   paker_depth, pressureZUMPF_question, rir_rpk_plast_true=False):

        from .opressovka import OpressovkaEK

        try:
            paker_depth_zumpf = int(float(self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()))
        except:
            paker_depth_zumpf = 0
        if paker_need_Combo == 'Нужно СПО':

            rir_list = OpressovkaEK.paker_list(self, diametr_paker, paker_khost, paker_depth,
                                               pressureZUMPF_question, paker_depth_zumpf)
            if rir_rpk_plast_true is False:
                rir_q_list = [
                    f'насыщение 5м3. Определить Q {plast_combo} при Р=80-100атм. СКВ', None,
                  f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast_combo} при Р=80-100атм '
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

    def rir_paker(self, paker_need_Combo, plast_combo,
                  roof_rir_edit, sole_rir_edit, pressureZUMPF_question='Не нужно',
                  diametr_paker=122, paker_khost=0, paker_depth=0):

        rir_list = self.need_paker(paker_need_Combo, plast_combo, diametr_paker, paker_khost,
                                   paker_depth, pressureZUMPF_question)

        rir_paker_list = [[f'РИР c пакером {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м',
                           None,
                           f'Произвести РИР {plast_combo} c плановой кровлей на глубине {roof_rir_edit}м по '
                           f'технологическому плану'
                           f' подрядчика по РИР силами подрядчика по РИР '
                           f'Перед спуском технологического пакера произвести испытание гидроякоря в присутсвии '
                           f'представителя '
                           f'РИР или УСРСиСТ.',
                           None, None, None, None, None, None, None,
                           'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
                          [f'ОЗЦ 16-24 часа', None,
                           f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
                           f'технологического "СТОП" ОЗЦ без давления.',
                           None, None, None, None, None, None, None,
                           'Мастер КРС, подрядчик РИР, УСРСиСТ', 24],
                          [f'Определение кровли', None,
                           f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста '
                           f'(плановый на '
                           f'гл. {roof_rir_edit}м'
                           f' с прямой промывкой и разгрузкой на забой 3т',
                           None, None, None, None, None, None, None,
                           'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
                          [f'Опрессовать на Р={well_data.max_admissible_pressure._value}атм', None,
                           f'Опрессовать цементный мост на Р={well_data.max_admissible_pressure._value}атм в '
                           f'присутствии '
                           f'представителя заказчика '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до начала '
                           f'работ) В случае негерметичности цементного моста дальнейшие работы согласовать с'
                           f' Заказчиком.',
                           None, None, None, None, None, None, None,
                           'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
                          [None, None,
                           f'Поднять компоновку РИР на тНКТ{well_data.nkt_diam}мм с глубины {roof_rir_edit}м '
                           f'с доливом скважины в объеме '
                           f'{round(roof_rir_edit * 1.12 / 1000, 1)}м3 тех. жидкостью уд.весом {well_data.fluid_work}',
                           None, None, None, None, None, None, None,
                           'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(roof_rir_edit, 1.2)]
                          ]
        RirWindow.perf_new(self, roof_rir_edit, sole_rir_edit)
        well_data.current_bottom = roof_rir_edit
        if OpressovkaEK.testing_pressure(self, roof_rir_edit)[2]:
            rir_paker_list.pop(-2)

        for row in rir_paker_list:
            rir_list.append(row)

        well_data.forPaker_list = None
        return rir_list

    def add_work(self):
        try:
            current_widget = self.tabWidget.currentWidget()
            plast_combo = str(current_widget.plast_combo.combo_box.currentText())
            self.rir_type_Combo = str(current_widget.rir_type_Combo.currentText())
            self.need_privyazka_QCombo = current_widget.need_privyazka_QCombo.currentText()
            roof_rir_edit = current_widget.roof_rir_edit.text().replace(',', '.')
            if roof_rir_edit != '':
                roof_rir_edit = int(float(roof_rir_edit))
            sole_rir_edit = current_widget.sole_rir_edit.text().replace(',', '.')
            if sole_rir_edit != '':
                sole_rir_edit = int(float(sole_rir_edit))

            if sole_rir_edit > well_data.current_bottom:
                QMessageBox.warning(self, 'Ошибка', f'Подошва ЦМ ниже текущего забоя - {well_data.current_bottom}м')
                return
            paker_need_Combo = current_widget.paker_need_Combo.currentText()
            pressureZUMPF_question = current_widget.pressureZUMPF_question_QCombo.currentText()
            need_change_zgs_combo = current_widget.need_change_zgs_combo.currentText()
            volume_cement = current_widget.cement_volume_line.text().replace(',', '.')
            if volume_cement != '':
                volume_cement = round(float(volume_cement), 1)
            if len(well_data.plast_project) != 0:
                plast_new_combo = current_widget.plast_new_combo.currentText()
            else:
                plast_new_combo = current_widget.plast_new_combo.text()
            fluid_new_edit = current_widget.fluid_new_edit.text()
            pressuar_new_edit = current_widget.pressuar_new_edit.text()
        except:
            mes = QMessageBox.warning(self, 'ОШИБКА', 'Введены не все данные')
        if paker_need_Combo == 'Нужно СПО':
            diametr_paker = int(float(current_widget.diametr_paker_edit.text()))
            paker_khost = int(float(current_widget.paker_khost_edit.text()))
            paker_depth = int(float(current_widget.paker_depth_edit.text()))
            if MyWindow.check_true_depth_template(self, paker_depth) is False:
                return
            if MyWindow.true_set_Paker(self, paker_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
                return
            if pressureZUMPF_question == 'Да':
                if paker_depth + paker_khost > well_data.current_bottom:
                    mes = QMessageBox.critical(self, 'Ошибка', 'Компоновка ниже текущего забоя')
                    return

        else:
            diametr_paker = 122
            paker_khost = 10
            paker_depth = 1000

        if self.rir_type_Combo == 'РИР на пере':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']
            if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == '') and \
                    need_change_zgs_combo == 'Да':
                mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return

            work_list = self.rirWithPero(paker_need_Combo, plast_combo,
                                         roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo,
                                         plast_new_combo,
                                         fluid_new_edit, pressuar_new_edit, pressureZUMPF_question,
                                         diametr_paker, paker_khost, paker_depth)
        elif self.rir_type_Combo == 'УЦМ в глухой колонне':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']
            if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == '') and \
                    need_change_zgs_combo == 'Да':
                mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return
            if need_change_zgs_combo == 'Да':
                if MyWindow.check_true_depth_template(self, paker_depth) is False:
                    return
                if MyWindow.true_set_Paker(self, paker_depth) is False:
                    return
                if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
                    return

            work_list = self.rirWithPero_gl(paker_need_Combo, plast_combo,
                                            roof_rir_edit, sole_rir_edit, volume_cement, need_change_zgs_combo,
                                            plast_new_combo,
                                            fluid_new_edit, pressuar_new_edit, pressureZUMPF_question,
                                            diametr_paker, paker_khost, paker_depth)


        elif self.rir_type_Combo == 'РИР с пакером с 2С':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']
            # print(paker_need_Combo, plast_combo, roof_rir_edit, sole_rir_edit)
            work_list = self.rir_paker(paker_need_Combo, plast_combo,
                                       roof_rir_edit, sole_rir_edit, pressureZUMPF_question,
                                       diametr_paker, paker_khost, paker_depth)

        elif self.rir_type_Combo == 'РИР с РПК':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpk(paker_need_Combo, plast_combo,
                                     roof_rir_edit, sole_rir_edit, pressureZUMPF_question,
                                     diametr_paker, paker_khost, paker_depth)

        elif self.rir_type_Combo == 'РИР с РПП':  # ['РИР на пере', 'РИР с пакером с 2С', 'РИР с РПК', 'РИР с РПП']

            work_list = self.rir_rpp(paker_need_Combo, plast_combo,
                                     roof_rir_edit, sole_rir_edit, pressureZUMPF_question,
                                     diametr_paker, paker_khost, paker_depth)

        MyWindow.populate_row(MyWindow, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def calc_buffer(self, roof, sole, dict_nkt):
        volume_in_nkt = round(100 * volume_vn_nkt(dict_nkt) / 1000, 1)
        nkt = min(list(map(int, dict_nkt.keys()))) / 100
        volume_out_nkt = nkt ** 2 * 3.14 / 4 / 100
        volume_ek = volume_vn_ek(sole) / 1000
        volume_in_ek = round(100 * volume_ek - volume_out_nkt, 1)
        return volume_in_nkt, volume_in_ek

    def rir_izvelPaker(self):

        paker_izv_paker, ok = QInputDialog.getInt(None, 'Глубина извлекаемого пакера',
                                                'Введите глубину установки извлекаемого пакера ',
                                                int(well_data.perforation_roof - 50), 0,
                                                int(well_data.bottomhole_drill._value))

        well_data.paker_izv_paker = paker_izv_paker
        rir_list = [[f'СПО пакера извлекаемый до глубины {paker_izv_paker}м',
                     None,
                     f'Спустить  пакера извлекаемый компании НЕОИНТЕХ +НКТ 20м + реперный патрубок 2м на тНКТ до'
                     f' глубины {paker_izv_paker}м с замером, шаблонированием шаблоном {well_data.nkt_template}мм.'
                     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                     None, None, None, None, None, None, None,
                     'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(paker_izv_paker, 1.2)],
                    [f'Привязка', None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {well_data.contractor}". '
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
                 f'объеме  {round(120 * 1.12 / 1000, 1)}м3 уд.весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4],
                [f'отсыпка в инт. {paker_izv_paker - 20} - {paker_izv_paker}  в объеме'
                 f' {round(well_volume(self, paker_izv_paker) / paker_izv_paker * 1000 * (20), 0)}л',
                 None, f'Произвести отсыпку кварцевым песком в инт. {paker_izv_paker - 20} - {paker_izv_paker} '
                       f' в объеме {round(well_volume(self, paker_izv_paker) / paker_izv_paker * 1000 * (20), 0)}л '
                       f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {well_data.fluid_work}',
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
                 f'В случае пеcчаного моста ниже гл.{paker_izv_paker - 20}м работы повторить с корректировкой обьема и '
                 f'технологических глубин.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять ИУГ с глубины {paker_izv_paker - 20}м с доливом тех '
                 f'жидкости в объеме  {round(paker_izv_paker * 1.12 / 1000, 1)}м3 уд.весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4]]

            for row in filling_list:
                rir_list.append(row)
            well_data.current_bottom2 = paker_izv_paker
            well_data.current_bottom = paker_izv_paker - 20
        else:
            rir_list.append([None, None,
                             f'Поднять ИУГ c глубины {paker_izv_paker}м с доливом тех жидкости в объеме '
                             f'{round(paker_izv_paker * 1.12 / 1000, 1)}м3 уд.весом {well_data.fluid_work}',
                             None, None, None, None, None, None, None,
                             'Мастер КРС, подрядчик по ГИС', 4])
            well_data.current_bottom2 = well_data.current_bottom
            well_data.current_bottom = paker_izv_paker
        well_data.forPaker_list = None
        return rir_list

    def izvlech_paker(self):

        rir_list = [
            [f'СПО {RirWindow.pero_select(self, well_data.current_bottom).replace("перо", "перо-110мм")} до '
             f'глубины {round(well_data.current_bottom, 0)}м', None,
             f'Спустить  {RirWindow.pero_select(self, well_data.current_bottom).replace("перо", "перо-110мм")} '
             f'на НКТ{well_data.nkt_diam}мм до '
             f'глубины {round(well_data.current_bottom, 0)}м с замером, шаблонированием шаблоном '
             f'{well_data.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(well_data.current_bottom, 1)],
            [f'Вымыв песка до гл.{well_data.paker_izv_paker - 10}',
             None,
             f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной промывкой '
             f'по круговой циркуляции '
             f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{well_data.paker_izv_paker - 10}м. \n'
             f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Поднять {RirWindow.pero_select(self, well_data.current_bottom)} НКТ{well_data.nkt_diam}мм с глубины '
             f'{well_data.paker_izv_paker - 10}м с доливом '
             f'скважины'
             f' в объеме {round((well_data.paker_izv_paker - 10) * 1.12 / 1000, 1)}м3 тех. '
             f'жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.paker_izv_paker - 10, 1)]]

        emer_list = [
            [f'СПО лов. инст до до Н= {well_data.current_bottom}', None,
              f'Спустить с замером ловильный инструмент на НКТ до Н= {well_data.current_bottom}м с замером. ',
              None, None, None, None, None, None, None,
              'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1)],
             [f'Вымыв песка до {well_data.paker_izv_paker}м. Извлечение пакера', None,
              f'Произвести нормализацию (вымыв кварцевого песка) на ловильном инструменте до глубины '
              f'{well_data.paker_izv_paker}м обратной '
              f'промывкой уд.весом {well_data.fluid_work} \n'
              f'Произвести  ловильный работы при представителе заказчика на глубине {well_data.paker_izv_paker}м.',
              None, None, None, None, None, None, None,
              'мастер КРС', liftingNKT_norm(well_data.paker_izv_paker, 1)],
             [None, None,
              f'Расходить и поднять компоновку НКТ{well_data.nkt_diam}мм с глубины {well_data.paker_izv_paker}м с '
              f'доливом скважины в объеме {round(well_data.paker_izv_paker * 1.12 / 1000, 1)}м3 тех. жидкостью '
              f'уд.весом {well_data.fluid_work}',
              None, None, None, None, None, None, None,
              'мастер КРС', liftingNKT_norm(well_data.paker_izv_paker, 1)]]
        for row in emer_list:
            rir_list.append(row)

        well_data.current_bottom, ok = QInputDialog.getInt(None, 'Глубина забоя',
                                                           'Введите глубину текущего забоя после извлечения',
                                                           int(well_data.current_bottom), 0,
                                                           int(well_data.bottomhole_drill._value))
        well_data.forPaker_list = None
        return rir_list
