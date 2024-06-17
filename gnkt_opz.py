from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QMainWindow, QTabWidget, QLabel, QLineEdit, QComboBox, \
    QGridLayout, QWidget, QPushButton
from PyQt5 import QtWidgets

import well_data
from cdng import events_gnvp_frez
from krs import GnoWindow
from main import MyWindow
from work_py.acid_paker import CheckableComboBox, AcidPakerWindow
from gnkt_data import gnkt_data
from collections import namedtuple


class TabPage_gnkt(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)
        # self.gnkt_number_label = QLabel('Номер ГНКТ')
        # self.gnkt_number_combo = QComboBox(self)
        # self.gnkt_number_combo.addItems(['ГНКТ №2', 'ГНКТ №1'])

        self.roof_label = QLabel("кровля пласта", self)
        self.roof_edit = QLineEdit(self)
        self.roof_edit.setText(f'{well_data.perforation_roof}')
        self.roof_edit.setValidator(self.validator_float)

        self.sole_label = QLabel("подошва пласта", self)
        self.sole_edit = QLineEdit(self)
        self.sole_edit.setText(f'{well_data.perforation_sole}')
        self.sole_edit.setValidator(self.validator_float)
        plast_work = ['']
        plast_work.extend(well_data.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        # self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.need_rast_label = QLabel("необходимость растворителя", self)
        self.need_rast_combo = QComboBox(self)
        self.need_rast_combo.addItems(['нужно', 'не нужно'])

        self.volume_rast_label = QLabel("Объем растворителя", self)
        self.volume_rast_edit = QLineEdit(self)
        self.volume_rast_edit.setText('2')
        self.volume_rast_edit.setValidator(self.validator_int)

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_combo = QComboBox(self)
        self.svk_true_combo.addItems(['Нужно СКВ', 'без СКВ'])
        self.svk_true_combo.setCurrentIndex(1)
        self.svk_true_combo.setProperty('value', 'без СКВ')

        self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
        self.skv_acid_edit = QComboBox(self)
        self.skv_acid_edit.addItems(['HCl', 'HF'])
        self.skv_acid_edit.setCurrentIndex(0)
        self.skv_acid_edit.setProperty('value', 'HCl')

        self.skv_volume_label = QLabel("Объем СКВ", self)
        self.skv_volume_edit = QLineEdit(self)
        self.skv_volume_edit.setValidator(self.validator_float)
        self.skv_volume_edit.setText('1')
        self.skv_volume_edit.setClearButtonEnabled(True)

        self.skv_proc_label = QLabel("Концентрация СКВ", self)
        self.skv_proc_edit = QLineEdit(self)
        self.skv_proc_edit.setClearButtonEnabled(True)
        self.skv_proc_edit.setText('15')
        self.skv_proc_edit.setValidator(self.validator_int)

        self.acid_label = QLabel("необходимость кислотной обработки", self)
        self.acid_true_edit = QComboBox(self)
        self.acid_true_edit.addItems(['нужно', 'не нужно'])

        self.acid_label_type = QLabel("Вид кислотной обработки", self)
        self.acid_edit = QComboBox(self)
        self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acid_edit.setCurrentIndex(0)

        self.acid_volume_label = QLabel("Объем кислотной обработки", self)
        self.acid_volume_edit = QLineEdit(self)
        self.acid_volume_edit.setValidator(self.validator_float)
        self.acid_volume_edit.setText("10")
        self.acid_volume_edit.setClearButtonEnabled(True)

        self.acid_proc_label = QLabel("Концентрация кислоты", self)
        self.acid_proc_edit = QLineEdit(self)
        self.acid_proc_edit.setText('15')
        self.acid_proc_edit.setClearButtonEnabled(True)
        self.acid_proc_edit.setValidator(self.validator_int)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setText(f'{well_data.max_admissible_pressure._value}')
        self.pressure_edit.setValidator(self.validator_int)

        self.distance_pntzh_label = QLabel('Расстояние  до ПНТЖ', self)
        self.distance_pntzh_edit = QLineEdit(self)
        self.distance_pntzh_edit.setValidator(self.validator_int)

        self.grid = QGridLayout(self)
        # grid.addWidget(self.gnkt_number_label, 0, 0)
        # grid.addWidget(self.gnkt_number_combo, 1, 0)
        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.roof_label, 0, 2)
        self.grid.addWidget(self.roof_edit, 1, 2)
        self.grid.addWidget(self.sole_label, 0, 3)
        self.grid.addWidget(self.sole_edit, 1, 3)

        self.grid.addWidget(self.need_rast_label, 2, 0)
        self.grid.addWidget(self.need_rast_combo, 3, 0)
        self.grid.addWidget(self.volume_rast_label, 2, 1)
        self.grid.addWidget(self.volume_rast_edit, 3, 1)

        self.grid.addWidget(self.skv_true_label_type, 4, 0)
        self.grid.addWidget(self.svk_true_combo, 5, 0)
        self.grid.addWidget(self.skv_acid_label_type, 4, 1)
        self.grid.addWidget(self.skv_acid_edit, 5, 1)
        self.grid.addWidget(self.skv_volume_label, 4, 2)
        self.grid.addWidget(self.skv_volume_edit, 5, 2)
        self.grid.addWidget(self.skv_proc_label, 4, 3)
        self.grid.addWidget(self.skv_proc_edit, 5, 3)

        self.grid.addWidget(self.acid_label, 6, 0)
        self.grid.addWidget(self.acid_true_edit, 7, 0)

        self.grid.addWidget(self.acid_label_type, 6, 1)
        self.grid.addWidget(self.acid_edit, 7, 1)
        self.grid.addWidget(self.acid_volume_label, 6, 2)
        self.grid.addWidget(self.acid_volume_edit, 7, 2)
        self.grid.addWidget(self.acid_proc_label, 6, 3)
        self.grid.addWidget(self.acid_proc_edit, 7, 3)
        # grid.addWidget(self.acidOilProcLabel, 4, 4)
        # grid.addWidget(self.acidOilProcEdit, 5, 4)
        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.grid.addWidget(self.distance_pntzh_label, 8, 1, 1, 3)
        self.grid.addWidget(self.distance_pntzh_edit, 9, 1, 1, 3)

        self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)
        self.svk_true_combo.setCurrentIndex(0)
        self.svk_true_combo.setCurrentIndex(1)
        self.acid_edit.currentTextChanged.connect(self.update_sko_type)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

    def update_skv_edit(self, index):
        if index == 'Нужно СКВ':
            self.grid.addWidget(self.skv_acid_label_type, 4, 1)
            self.grid.addWidget(self.skv_acid_edit, 5, 1)
            self.grid.addWidget(self.skv_volume_label, 4, 2)
            self.grid.addWidget(self.skv_volume_edit, 5, 2)
            self.grid.addWidget(self.skv_proc_label, 4, 3)
            self.grid.addWidget(self.skv_proc_edit, 5, 3)
        else:
            self.skv_acid_label_type.setParent(None)
            self.skv_acid_edit.setParent(None)
            self.skv_volume_label.setParent(None)
            self.skv_volume_edit.setParent(None)
            self.skv_proc_label.setParent(None)
            self.skv_proc_edit.setParent(None)

    def update_plast_edit(self):

        dict_perforation = well_data.dict_perforation
        plasts = well_data.texts
        # print(f'пласты {plasts, len(well_data.texts), len(plasts), well_data.texts}')
        roof_plast = well_data.current_bottom
        sole_plast = 0
        for plast in well_data.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']
        self.roof_edit.setText(f'{roof_plast}')
        self.sole_edit.setText(f'{sole_plast}')

    def update_sko_type(self, type_sko):
        self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
        self.sko_vt_edit = QLineEdit(self)
        if type_sko == 'ВТ':
            self.grid.addWidget(self.sko_vt_label, 6, 6)
            self.grid.addWidget(self.sko_vt_edit, 7, 6)
        else:
            self.sko_vt_label.setParent(None)
            self.sko_vt_edit.setParent(None)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_gnkt(self), 'ГНКТ ОПЗ')


class GnktOpz(QMainWindow):
    def __init__(self, table_widget, gnkt_number_combo, fluid_edit, parent=None):

        super(GnktOpz, self).__init__(parent=None)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.work_plan = 'gnkt_opz'
        self.paker_select = None
        self.gnkt_number_combo = gnkt_number_combo
        self.fluid_edit = fluid_edit

        self.table_widget = table_widget
        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        roof_plast = float(self.tabWidget.currentWidget().roof_edit.text())
        sole_plast = float(self.tabWidget.currentWidget().sole_edit.text())
        need_rast_combo = str(self.tabWidget.currentWidget().need_rast_combo.currentText())
        volume_rast_edit = float(self.tabWidget.currentWidget().volume_rast_edit.text())
        acid_true_edit = str(self.tabWidget.currentWidget().acid_true_edit.currentText())
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        skv_volume_edit = float(self.tabWidget.currentWidget().skv_volume_edit.text().replace(',', '.'))
        skv_proc_edit = int(self.tabWidget.currentWidget().skv_proc_edit.text().replace(',', '.'))
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        svk_true_combo = str(self.tabWidget.currentWidget().svk_true_combo.currentText())
        skv_acid_edit = str(self.tabWidget.currentWidget().skv_acid_edit.currentText())
        self.distance = self.tabWidget.currentWidget().distance_pntzh_edit.text()
        if self.distance == '':
            mes = QMessageBox.critical(self, "Ошибка", "Нужно указать расстояние до ПНТЖ")
            return
        if acid_edit == 'ВТ':
            self.vt = self.tabWidget.currentWidget().sko_vt_edit.text()
            if self.vt == '':
                mes = QMessageBox.critical(self, "Ошибка", "Нужно расписать объемы и вид кислоты")
                return

        work_list = self.gnkt_work(roof_plast, sole_plast, need_rast_combo, volume_rast_edit, acid_true_edit,
                                   acid_edit, skv_volume_edit, skv_proc_edit, acid_volume_edit, acid_proc_edit,
                                   pressure_edit,
                                   plast_combo, svk_true_combo, skv_acid_edit, self.gnkt_number_combo, self.fluid_edit)

        well_data.pause = False
        self.close()
        return work_list

    def gnkt_work(self, roof_plast, sole_plast, need_rast_combo, volume_rast_edit, acid_true_edit,
                  acid_edit, skv_volume_edit, skv_proc_edit, acid_volume_edit, acid_proc_edit, pressure_edit,
                  plast_combo, svk_true_combo, skv_acid_edit, gnkt_number_combo, fluid_work_insert):

        block_gnvp_list = events_gnvp_frez(self, self.distance, float(fluid_work_insert))

        if gnkt_number_combo == 'ГНКТ №2':
            gnkt_number = gnkt_data.gnkt_2
        elif gnkt_number_combo == 'ГНКТ №1':
            gnkt_number = gnkt_data.gnkt_1

        V_gntk = round(gnkt_number.gnkt_length * 0.74 / 1000, 1)

        if acid_true_edit == "нужно":
            acid_true_quest = True
        else:
            acid_true_quest = False

        fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(self, fluid_work_insert)

        if need_rast_combo == 'нужно':
            volume_rast_edit = volume_rast_edit

        if acid_edit == 'HCl':
            acid_24 = round(acid_volume_edit * acid_proc_edit / 24 * 1.118, 1)
            acid_sel = f'Произвести  солянокислотную обработку {plast_combo} в объеме {acid_volume_edit}м3 ' \
                       f' ({acid_edit} - {acid_proc_edit} %) силами/' \
                       f' Крезол НС с протяжкой БДТ вдоль интервалов перфорации {roof_plast}-{sole_plast}м ' \
                       f'(снизу вверх) в ' \
                       f'присутствии представителя Заказчика с составлением акта, не превышая давления' \
                       f' закачки не более Р={well_data.max_admissible_pressure._value}атм.\n' \
                       f' (для приготовления соляной кислоты в объеме {acid_volume_edit}м3 - ' \
                       f'{acid_proc_edit}% необходимо замешать {acid_24}т HCL 24% и пресной воды ' \
                       f'{round(acid_volume_edit - acid_24, 1)}м3)'
            acid_sel_short = f'СКО пласта {plast_combo}  в объеме  {acid_volume_edit}м3  ' \
                             f'({acid_edit} - {acid_proc_edit} %)'
        elif acid_edit == 'ВТ':

            acid_sel = f'Произвести кислотную обработку пласта {plast_combo} {self.vt}  силами Крезол ' \
                       f'НС с протяжкой БДТ вдоль интервалов перфорации {roof_plast}-' \
                       f'{sole_plast}м (снизу вверх) в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более ' \
                       f'Р = {well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'{self.vt} пласта {plast_combo}  в объеме ' \
                             f'{acid_volume_edit}м3  ({acid_edit} - {acid_proc_edit} %)'
        elif acid_edit == 'HF':
            acid_sel = f'Произвести глинокислотную обработку пласта {plast_combo} в объеме ' \
                       f'{acid_volume_edit}м3 ' \
                       f'(концентрация в смеси HF 3% / HCl 13%) силами Крезол ' \
                       f'НС с протяжкой БДТ вдоль интервалов перфорации {roof_plast}-' \
                       f'{sole_plast}м (снизу вверх) в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более ' \
                       f'Р={well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'ГКО пласта {plast_combo}  в объеме  {acid_volume_edit}м3'

        paker_opr = [f'Опрессовать пакер на {well_data.max_admissible_pressure._value}атм',
                     5, f'Опрессовать пакер на {well_data.max_admissible_pressure._value}атм с выдержкой 30 мин с '
                        f'оформлением соответствующего акта в присутствии ' \
                        f'представителя представителя ЦДНГ',
                     None, None, None, None, None, None, None,
                     'Мастер ГНКТ, предст. Заказчика', 1]
        if well_data.depth_fond_paker_do["do"] == 0:
            depth_fond_paker_do = sum(list(well_data.dict_nkt.values()))
            # print(depth_fond_paker_do)
            if depth_fond_paker_do >= well_data.current_bottom:
                depth_fond_paker_do, ok = QInputDialog.getDouble(self, 'глубина НКТ',
                                                                 'Введите Глубины башмака НКТ', 500,
                                                                 0, well_data.current_bottom)
        else:
            depth_fond_paker_do = well_data.depth_fond_paker_do["do"]

        gnkt_opz = [
            [None, 'Порядок работы', None, None, None, None, None, None, None, None, None, None],
            [None, None, 'Наименование работ', None, None, None, None, None, None, None,
             'Ответственный', 'Нормы'],
            [None, 1, 'ВНИМАНИЕ: Перед спуском и вовремя проведения СПО бурильщикам и мастеру производить осмотр '
                      'ГНКТ на наличие '
                      '"меток" на г/трубы, установленных запрещённым способом.\nПри обнаружении - доложить руководству'
                      ' ООО "Ойл-Сервис" '
                      'по согласованию произвести отрезание ГНКТ выше "метки" с составлением АКТа и указанием метража '
                      'отрезанного участка ГНКТ. '
                      'Установку меток на г/трубе производить ТОЛЬКО безопасным способом - (краской, лентой фум, '
                      'шкемарём, и тд.) '
                      'КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ устанавливать "метки" опасным способом - вальцевателем (труборезом) или '
                      'другим инструментом - '
                      'который причиняет механические повреждения на теле г/трубы и может привести к снижению прочностных '
                      'характеристик ГНКТ. '
                      'Запросить у Заказчика внутренние диаметры спущенной компоновки для исключения заклинивания низа'
                      ' компоновки',
             None, None, None, None, None, None, None,
             'Мастер КРС,бурильщик', None],
            [None, 1, 'Провести приемку скважины в ремонт у Заказчика с составлением акта. Переезд бригады КРС '
                      'на скважину. '
                      'Подготовительные работы к КРС. Расставить технику и оборудование.Составить Акт .',
             None, None, None, None, None, None, None, 'Мастер КРС, представитель Заказчика', 'расчет нормы на '
                                                                                              'переезд '],
            [None, 1, 'Провести инструктаж по предупреждению ГНВП и ОФ при КРС, а также по плану ликвидации '
                      'аварий при '
                      'производстве работ с записью в журнале (инструктаж, в обязательном порядке, проводить '
                      'с обеими вахтами бригады).',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 3,
             'Мастеру бригады - запретить бурильщикам оставлять устье скважины незагерметизированным независимо '
             'от продолжительности перерывов в работе.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 4, 'Проводить замеры газовоздушной среды согласно утвержденного графика',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 6,
             'Провести работы по монтажу колтюбинговой установки'
             ' в соответствии с технологической инструкцией, федеральных норм и правила в области промышленной '
             'безопасности «Правила безопасности в нефтяной и газовой промышленности»  РОСТЕХНАДЗОР '
             'Приказ №1 от 15.12.2020г и РД 153-39-023-97.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 7,
             'Все операции при производстве выполнять в соответствии с технологической инструкцией, '
             'федеральных норм и правила в области промышленной безопасности "Правила безопасности в '
             'нефтяной и газовой промышленности" '
             'от 15.12.2020г и РД 153-39-023-97.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 8,
             f'Произвести монтаж колтюбингового оборудования согласно утверждённой схемы №5 от 14.10.2021г '
             f'("Обвязки устья '
             f'при глушении скважин, после проведения гидроразрыва пласта и работы на скважинах ППД с оборудованием'
             f' койлтюбинговых установок на месторождениях ООО "Башнефть-Добыча") перевентором ППК 80х35 '
             f'(4-х секционный превентор БП 80-70.00.00.000 (700атм)) № {gnkt_number.pvo} и инжектором ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 3.5],
            [None, 9, 'Пусковой комиссии в составе мастера и членов бригады согласно положения от 2015г.'
                      '"Положение о проведении пусковой комиссии при ТКРС" произвести проверку готовности бригады '
                      'для ремонта скважины с последующим составлением акта.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 0.5],
            [None, 10, f'Перед началом опрессовки принять все требуемые меры безопасности. Подготовиться к опрессовке.'
                       f' Удостовериться в том, рабочая зона вокруг линий высокого давления обозначена знаками '
                       f'безопосности.'
                       f' Запустить систему регистрации СОРП. Оповестить всех людей на кустовой площадке о проведении '
                       f'опрессовки.'
                       f' Опрессовать все нагнетательные линии на {min(225, well_data.max_admissible_pressure._value * 1.5)}атм. '
                       f'Опрессовать  выкидную линию '
                       f'от устья скважины до желобной ёмкости на '
                       f'{min(225, round(well_data.max_admissible_pressure._value * 1.5, 1))}атм c выдержкой 30мин'
                       f'(надёжно закрепить, оборудовать дроссельными задвижками)',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 'факт'],
            [None, 11, f'При закрытой центральной задвижке фондовой арматуры. Опрессовать превентор, глухие и трубные  '
                       f'плашки на '
                       f'устье скважины на Р={well_data.max_admissible_pressure._value}атм с выдержкой 30 мин (опрессовку ПВО '
                       f'зафиксировать'
                       f' в вахтовом журнале). Оформить соответствующий акт в присутствии представителя Башкирского '
                       f'военизированного '
                       f'отряда с выдачей разрешения на дальнейшее проведение работ (вызов представителя БВО по '
                       f'телефонограмме за 24 '
                       f'часа). Провести учебно-тренировочное занятие по сигналу "Выброс" с записью в журнале.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 0.47],
            [None, 12,
             f'Произвести спуск БДТ + насадка 5 каналов до {well_data.current_bottom}м (забой) с промывкой скважины '
             f'мин.водой уд.веса {fluid_work} с фиксацией давления промывки, расход жидкости не менее 200л\\мин, объем '
             f'промывки не менее 1 цикла  со скоростью 5м/мин. Убедиться в наличии свободного прохода КНК-2 (при '
             f'прохождении насадкой лубрикаторной задвижки, пакера, воронки скорость спуска минимальная 2м/мин). При '
             f'посадке ГНКТ в колонне НКТ произвести закачку (на циркуляции) растворителя в объёме 0,2 м3 в ГНКТ. '
             f'Произвести продавку (на циркуляции) растворителя АСПО до башмака ГНКТ мин.водой уд.вес {fluid_work} '
             f'в объёме 2,0м3. Закрыть Кран на тройнике устьевого оборудования. '
             f'{"Стоянка на реакции 2 часа." if well_data.region != "ТГМ" and acid_sel != "HF" else "без реагирования"}'
             f' Промывка колонны '
             f'НКТ - не менее1 цикла. Составить Акт. Промывка подвески ФНКТ по согласованию ПТО и ЦДНГ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', 2.04],
            [f'Промыть НКТ и скважину с гл.{well_data.current_bottom}м',
             13, f'Промыть НКТ и скважину с гл.{well_data.current_bottom}м мин.водой уд.веса {fluid_work}  в 1 цикл'
                 f' с добавлением 1т растворителя с составлением соответствующего акта. При появлении затяжек или '
                 f'посадок при спуско-подъемных операциях произвести интенсивную промывку '
                 f'осложненного участка скважины. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представит. Заказчика', 0.84],
            [f'обработку НКТ {volume_rast_edit}м3 растворителя',
             14, f'Произвести  обработку НКТ {volume_rast_edit}м3 растворителя в присутствии'
                 f' представителя Заказчика при открытом'
                 f' малом затрубном пространстве на циркуляции. Произвести продавку растворителя АСПО до '
                 f'башмака ГНКТ '
                 f'мин.водой уд.вес {fluid_work} в объёме 2,2м3 не превышая давления закачки не более  '
                 f'Р={well_data.max_admissible_pressure._value}атм. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.92],
            [None, 15,
             f'Приподнять БДТ до {int(depth_fond_paker_do) - 20}м. Произвести круговую циркуляцию растворителя в '
             f'течении 2часов. Составить Акт',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 2.06],

            [None, 22, f'Спустить БДТ до забоя. Промыть скважину от продуктов реакции кислоты мин.водой  {fluid_work}  '
                       f'с составлением'
                       f'соответствующего акта. \n ПРИ ПОЯВЛЕНИИ ЗАТЯЖЕК ИЛИ ПОСАДОК ПРИ СПУСКО-ПОДЪЕМНЫХ ОПЕРАЦИЯХ '
                       f'ПРОИЗВЕСТИ '
                       f'ИНТЕНСИВНУЮ ПРОМЫВКУ ОСЛОЖНЕННОГО УЧАСТКА СКВАЖИНЫ ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 0.93],
            [f'гидросвабирование в инт {roof_plast}-'
             f'{sole_plast}м при Рзак={well_data.max_admissible_pressure._value}атм',
             23, f'Произвести гидросвабирование пласта в интервале {roof_plast}-'
                 f'{sole_plast}м (закрыть затруб, произвести задавку в пласт '
                 f'жидкости при не более Рзак={well_data.max_admissible_pressure._value}атм при установленном '
                 f'герметичном пакере. '
                 f'Операции по задавке и изливу произвести 3-4 раза в зависимости от приёмистости). ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1],
            [f'Исследовать скважину на приёмистость при Рзак={well_data.expected_P}атм',
             24, f'Исследовать скважину на приёмистость при Рзак={well_data.expected_P}атм с составлением акта в '
                 f' в присутствии представителя ЦДНГ с составлением соответствующего акта (для вызова представителя '
                 f'давать телефонограмму в ЦДНГ). Определение приёмистости производить после насыщения пласта не менее 6м3 или '
                 f'при установившемся давлении закачки, но не более 1 часов. При недостижении запланированной приёмистости '
                 f'{well_data.expected_Q}м3/сут при Р= {well_data.expected_P}атм дальнейшие работы производить '
                 f'по согласованию с Заказчиком. Составить Акт ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.4],
            [None,
             25, f'Вызвать телефонограммой представителя Заказчика для замера приёмистости  при '
                 f'Рзак={well_data.expected_P}атм прибором "Панаметрикс".Перед запуском скважины '
                 f'произвести сброс жидкости с водовода в объёме 3-5м3 в ЕДК в зависимости от наличия нефтяной эмульсии на '
                 f'выходе в технологическую емкость для предупреждения повторной кольматации ПЗП шламом с водовода и '
                 f'произвести замер приемистости переносным прибором после насыщения скважины в течении 1-2 часа от КНС. '
                 f'При недостижении запланированной приёмистости дальнейшие работы производить по согласованию с  Заказчиком. '
                 f'Составить Акт ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика УСРСиСТ', 1.4],
            [None, 26,
             f'Поднять БДТ до устья с промывкой скважины мин.водой {fluid_work} . Составить Акт. Согласовать с '
             f'Заказчиком утилизацию жидкости в коллектор.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 1.56],
            [None, 27, 'Произвести демонтаж колтюбингового оборудования и линии обвязки желобной системы.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 2.25],
            [None, 28, 'Запустить скважину под закачку. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 29, 'Сдать территорию скважину представителю Заказчика. Составить Акт.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', None],
        ]

        opz = [
            ['Допустить БДТ до забоя. Промыть скважину ',
             16, f'Допустить БДТ до забоя. Промыть скважину  мин.водой уд.веса {fluid_work}  с составлением '
                 f'соответствующего акта. При отсутствии циркуляции дальнейшие промывки исключить. Определить '
                 f'приемистость пласта в трубное пространство при давлении не более '
                 f'{well_data.max_admissible_pressure._value}атм'
                 f'  (перед определением приемистости произвести закачку тех.воды не менее 6м3 или при установившемся '
                 f'давлении закачки, но не более 1 часа). Установить БДТ на гл.{well_data.current_bottom}м.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.33],
            [acid_sel_short,
             17, acid_sel,
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, подрядчик по ОПЗ', 2],
            [None,
             18, f'Закачку {V_gntk}м3 кислоты производить при открытом малом затрубном пространстве на '
                 f'циркуляции. Закачку оставшейся '
                 f'кислоты в объеме {round(acid_volume_edit - V_gntk, 1)}м3 производить при закрытом затрубном '
                 f'пространстве. Составить Акт.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 2.88],
            [None, 19, f'Продавить кислоту в пласт мин.водой уд.веса {fluid_work} в объёме 3м3 при давлении не более '
                       f'{well_data.max_admissible_pressure._value}атм. Составить Акт',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 1.11],
            [None, 20,
             f'Приподнять БДТ на {int(depth_fond_paker_do) - 20}м. Стоянка на реакции 2 часа. В СЛУЧАЕ ОТСУТСТВИЯ ДАВЛЕНИЯ '
             f'ПРОДАВКИ ПРИ СКО, РАБОТЫ ПРОИЗВОДИМ БЕЗ РЕАГИРОВАНИЯ.СОСТАВИТЬ АКТ)',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 3.06],
            ['разрядку скважины для извлечения продуктов',
             21, 'Произвести разрядку скважины для извлечения продуктов реакции кислоты в объёме не менее объёма '
                 'закаченной кислоты + объём малого затрубного пространства (из расчета 1,88л на 1 м пространства между '
                 '73мм колонной НКТ и БДТ;'
                 ' 0,46л между 60мм НКТ и БДТ; 3,38л между 89мм НКТ и БДТ) + 3м3. Разрядку производить до чистой промывочной '
                 'жидкости (без признаков продуктов реакции кислоты), но не более 2 часов. Зафиксировать избыточное давление '
                 'на устье скважины, объём и описание скважинной жидкости на выходе с отражением их в акте, суточном рапорте '
                 'работы бригад. Составить Акт.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 1]]
        n = 17
        if well_data.depth_fond_paker_do['do'] != 0:  # вставка строк при наличии пакера
            gnkt_opz.insert(7, paker_opr)
            n += 1

        if acid_true_quest:  # Вставка строк при необходимости ОПЗ
            for i in opz:
                gnkt_opz.insert(n, i)
                n += 1

        for row in block_gnvp_list[::-1]:
            gnkt_opz.insert(0, row)

        number_punkt = 1
        for i in range(3, len(gnkt_opz)):  # нумерация работ
            if len(str(gnkt_opz[i][1])) <= 3 and gnkt_opz[i][1] != '№':
                gnkt_opz[i][1] = number_punkt
                number_punkt += 1
            else:
                number_punkt = 1

        return gnkt_opz


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    # window = GnktOpz()
    # window.show()
    sys.exit(app.exec_())
