import json
import math
import data_list

from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTabWidget, QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, \
    QGridLayout, QPushButton, QBoxLayout, QApplication

from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.alone_oreration import kot_work
from PyQt5.QtGui import QDoubleValidator
from .template_work import TemplateKrs, TabPageSoWith
from main import MyMainWindow


class TabPageSo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        validator = QDoubleValidator(0.0, 80000.0, 2)

        self.template_labelType = QLabel("Вид компоновки шаблона", self)
        self.template_Combo = QComboBox(self)

        self.template_str_Label = QLabel("строчка с шаблонами", self)
        self.template_str_Edit = QLineEdit(self)

        self.skm_teml_str_Label = QLabel("глубины спуска шаблонов", self)
        self.skm_teml_str_Edit = QLineEdit(self)

        self.template_first_Label = QLabel("диаметр первого шаблона", self)
        self.template_first_Edit = QLineEdit(self)
        self.template_first_Edit.setValidator(validator)

        self.length_template_first_Label = QLabel("длина первого шаблона", self)
        self.length_template_first_Edit = QLineEdit(self)
        self.length_template_first_Edit.setValidator(validator)

        self.dictance_template_first_Label = QLabel("расстояние", self)
        self.dictance_template_first_Edit = QLineEdit(self)
        self.dictance_template_first_Edit.setValidator(validator)

        self.template_second_Label = QLabel("диаметр второго шаблона", self)
        self.template_second_Edit = QLineEdit(self)
        self.template_second_Edit.setValidator(validator)

        self.length_template_second_Label = QLabel("длина второго шаблона", self)
        self.length_template_second_Edit = QLineEdit(self)
        self.length_template_second_Edit.setValidator(validator)

        self.dictance_template_second_Label = QLabel("расстояние-2", self)
        self.dictance_template_second_Edit = QLineEdit(self)
        self.dictance_template_second_Edit.setValidator(validator)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')

        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        if self.data_well.current_bottom - self.data_well.perforation_roof <= 10 and \
                self.data_well.open_trunk_well is False and self.data_well.count_template != 0:
            self.privyazka_question_QCombo.setCurrentIndex(1)

        self.note_label = QLabel("Нужно ли добавлять примечание", self)
        self.note_question_qcombo = QComboBox(self)
        self.note_question_qcombo.addItems(['Нет', 'Да'])

        self.solvent_label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(validator)
        self.solvent_volume_edit.setText("2")

        self.solvent_question_label = QLabel("необходимость растворителя", self)
        self.solvent_question_combo = QComboBox(self)
        self.solvent_question_combo.addItems(['Нет', 'Да'])

        self.kot_label = QLabel("Нужно ли добавлять систему КОТ-50", self)
        self.kot_question_qcombo = QComboBox(self)

        self.kot_question_qcombo.addItems(['Нет', 'Да'])
        if self.data_well.plast_work:
            self.kot_question_qcombo.setCurrentIndex(1)

        self.template_Combo.currentTextChanged.connect(self.update_template_edit)

        if self.data_well.count_template == 0:
            self.note_question_qcombo.setCurrentIndex(1)
            self.solvent_question_combo.setCurrentIndex(1)

        self.grid = QGridLayout(self)
        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and self.data_well.current_bottom <
                 self.data_well.head_column_additional.get_value):
            first_template, template_second = TabPageSoWith.template_diam_ek(self)
            self.template_select_list = ['шаблон ЭК с хвостом', 'шаблон открытый ствол', 'шаблон без хвоста']

            self.template_Combo.addItems(self.template_select_list)
            template_key = self.definition_pssh()
            self.template_Combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_Combo, 2, 2, 2, 8)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.length_template_first_Label, 4, 3)
            self.grid.addWidget(self.length_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)

            self.grid.addWidget(self.template_second_Label, 4, 7)
            self.grid.addWidget(self.template_second_Edit, 5, 7)
            self.grid.addWidget(self.length_template_second_Label, 4, 8)
            self.grid.addWidget(self.length_template_second_Edit, 5, 8)
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)

        else:
            first_template, template_second = TabPageSoWith.template_diam_additional_ek(self)
            self.template_select_list = ['шаблон ДП с хвостом', 'шаблон ДП открытый ствол', 'шаблон ДП без хвоста']
            self.template_Combo.addItems(self.template_select_list)
            template_key = self.definition_pssh()

            self.template_Combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_Combo, 2, 2, 2, 8)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)

            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)

            self.grid.addWidget(self.length_template_first_Label, 4, 4)
            self.grid.addWidget(self.length_template_first_Edit, 5, 4)

            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.template_second_Label, 4, 6)
            self.grid.addWidget(self.template_second_Edit, 5, 6)
            self.grid.addWidget(self.length_template_second_Label, 4, 7)
            self.grid.addWidget(self.length_template_second_Edit, 5, 7)

        self.grid.addWidget(self.current_bottom_label, 8, 3)
        self.grid.addWidget(self.current_bottom_edit, 9, 3)

        self.grid.addWidget(self.solvent_question_label, 8, 4)
        self.grid.addWidget(self.solvent_question_combo, 9, 4)

        self.grid.addWidget(self.solvent_label, 8, 5)
        self.grid.addWidget(self.solvent_volume_edit, 9, 5)

        self.grid.addWidget(self.privyazka_question_Label, 8, 6)
        self.grid.addWidget(self.privyazka_question_QCombo, 9, 6)

        self.grid.addWidget(self.note_label, 8, 7)
        self.grid.addWidget(self.note_question_qcombo, 9, 7)

        self.grid.addWidget(self.kot_label, 8, 8)
        self.grid.addWidget(self.kot_question_qcombo, 9, 8)

        self.grid.addWidget(self.template_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.template_str_Edit, 14, 1, 1, 8)

        self.grid.addWidget(self.skm_teml_str_Label, 15, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_Edit, 16, 1, 1, 8)

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))

        self.length_template_first_Edit.setText(str(2))

        self.template_first_Edit.textChanged.connect(self.update_template)
        self.length_template_second_Edit.textChanged.connect(self.update_template)
        self.template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_first_Edit.textChanged.connect(self.update_template)
        self.length_template_first_Edit.textChanged.connect(self.update_template)
        self.kot_question_qcombo.currentTextChanged.connect(self.update_template)


    def definition_pssh(self):

        if self.data_well.column_additional is False and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is False or \
                (
                        self.data_well.column_additional is True and self.data_well.current_bottom <
                        self.data_well.head_column_additional.get_value and self.data_well.open_trunk_well is False):
            template_key = 'шаблон ЭК с хвостом'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is True:
            template_key = 'шаблон открытый ствол'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is True or \
                (self.data_well.column_additional is True and \
                 self.data_well.current_bottom < self.data_well.head_column_additional.get_value and \
                 self.data_well.open_trunk_well is False):
            template_key = 'шаблон без хвоста'


        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is False:
            template_key = 'шаблон ДП с хвостом'

        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is True:
            template_key = 'шаблон ДП открытый ствол'

        elif self.data_well.column_additional is True and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is True and self.data_well.open_trunk_well is False:
            template_key = 'шаблон ДП с хвостом'
        return template_key

    def update_template(self):
        first_template, length_template_first, template_second, dictance_template_first, dictance_template_second \
            = '', '', '', '', ''

        if self.template_first_Edit.text() != '':
            first_template = self.template_first_Edit.text()
        if self.length_template_first_Edit.text() != '':
            length_template_first = self.length_template_first_Edit.text()
        if self.template_second_Edit.text() != '':
            template_second = self.template_second_Edit.text()
        if self.length_template_second_Edit.text() != '':
            length_template_second = self.length_template_second_Edit.text()

        if self.dictance_template_first_Edit.text() != '':
            dictance_template_first = int(float(self.dictance_template_first_Edit.text()))
        else:
            dictance_template_first = ''
        if self.dictance_template_second_Edit.text() != '':
            dictance_template_second = int(float(self.dictance_template_second_Edit.text()))
        else:
            dictance_template_second = ''
        current_bottom = float(self.current_bottom_edit.text())
        roof_plast, roof_add_column_plast = TabPageSoWith.definition_roof_not_raiding(self, current_bottom)

        nkt_diam = self.data_well.nkt_diam

        if self.data_well.column_additional or \
                (self.data_well.head_column_additional.get_value >= self.data_well.current_bottom and
                 self.data_well.column_additional is False):
            nkt_pod = '60мм' if self.data_well.column_additional_diameter.get_value < 110 else '73мм со снятыми фасками'

        if first_template != '' and length_template_first != '' and \
                template_second != '' and length_template_second != '' and \
                dictance_template_first != '' and \
                dictance_template_second != '' and first_template != '':

            kot_str = ''
            if 'Ойл' in data_list.contractor and len(self.data_well.plast_work) != 0:
                kot_str = '+ КОТ-50'

            if self.template_Combo.currentText() == 'шаблон ЭК с хвостом':
                if dictance_template_second != '':
                    template_str = f'перо {kot_str} + шаблон-{int(first_template)}мм ' \
                                   f'L-{int(length_template_first)}м + НКТ{nkt_diam}м ' \
                                   f'{int(dictance_template_first)}м  + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}'

                    self.data_well.template_depth = int(
                        self.data_well.current_bottom - int(dictance_template_first) -
                        int(length_template_first))

                    skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'


            elif self.template_Combo.currentText() == 'шаблон без хвоста':
                if dictance_template_second is not None:
                    template_str = f'перо {kot_str} + шаблон-{template_second}мм L-{length_template_second}м '
                    self.data_well.template_depth = self.data_well.current_bottom
                    skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'



            elif self.template_Combo.currentText() == 'шаблон открытый ствол':
                if dictance_template_second is not None:
                    self.template_first_Edit.setText('фильтр направление')
                    template_str = f'фильтр-направление {kot_str} + НКТ{nkt_diam}м {dictance_template_first}м  ' \
                                   f'шаблон-{template_second}мм L-{length_template_second}м '
                    self.data_well.template_depth = int(
                        self.data_well.current_bottom - int(dictance_template_first))

                    skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

            elif self.template_Combo.currentText() == 'шаблон ДП с хвостом':
                if dictance_template_second is not None:
                    template_str = f'обточная муфта + {kot_str} НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ шаблон-{first_template}мм ' \
                                   f'L-{length_template_first}м + НКТ{nkt_pod} {dictance_template_second}м + ' \
                                   f'шаблон-{template_second}мм L-{length_template_second}м '
                    self.data_well.template_depth = math.ceil(self.data_well.current_bottom - 2 -
                                                                      int(dictance_template_first) - int(
                        dictance_template_second) -
                                                                      int(length_template_first))
                    self.data_well.template_depth_addition = math.ceil(
                        self.data_well.current_bottom - 2 -
                        int(dictance_template_first) - int(
                            dictance_template_second))

                    skm_teml_str = f'шаблон-{first_template}мм до гл.' \
                                   f'{self.data_well.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

            elif self.template_Combo.currentText() == 'шаблон ДП без хвоста':

                template_str = f'обточная муфта {kot_str} + ' \
                               f'шаблон-{first_template}мм L-{length_template_first}м + ' \
                               f'НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                               f'L-{length_template_second}м '

                self.data_well.template_depth = math.ceil(
                    self.data_well.current_bottom - int(dictance_template_second) -
                    int(length_template_first))
                self.data_well.template_depth_addition = math.ceil(
                    self.data_well.current_bottom)

                skm_teml_str = f'шаблон-{first_template}мм до гл.{self.data_well.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'


            elif self.template_Combo.currentText() == 'шаблон ДП открытый ствол':
                if dictance_template_second is not None:
                    template_str = f'фильтр направление L-2м {kot_str} + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'  + шаблон-{first_template}мм ' \
                                   f'L-{length_template_first}м' \
                                   f' + НКТ{nkt_pod} + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м '
                    self.data_well.template_depth = math.ceil(self.data_well.current_bottom - 2 -
                                                                      int(dictance_template_first) - int(
                        dictance_template_second) -
                                                                      int(length_template_first))
                    self.data_well.template_depth_addition = math.ceil(
                        self.data_well.current_bottom - 2 -
                        int(dictance_template_first) - int(
                            dictance_template_second))

                    skm_teml_str = f'шаблон-{first_template}мм до гл.' \
                                   f'{self.data_well.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'
            if dictance_template_second != "":
                self.template_str_Edit.setText(template_str)
                self.skm_teml_str_Edit.setText(skm_teml_str)

    def update_template_edit(self, index):

        template_str = ''
        skm_teml_str = ''
        kot_str = ''
        if 'Ойл' in data_list.contractor:
            kot_str = '+ КОТ'
        nkt_diam = self.data_well.nkt_diam
        if self.data_well.column_additional is False or (self.data_well.column_additional and
                                                                 self.data_well.head_column_additional.get_value >=
                                                                 self.data_well.current_bottom):

            first_template, template_second = TabPageSoWith.template_diam_ek(self)
            # print(f'диаметры шаблонов {first_template, template_second}')
        else:
            first_template, template_second = TabPageSoWith.template_diam_additional_ek(self)
            # print(f'диаметры шаблонов {first_template, template_second}')

        current_bottom = float(self.current_bottom_edit.text())

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))
        # self.skm_edit.setText(str(self.data_well.column_diameter.get_value))
        self.dictance_template_second_Edit.setText(str(10))

        roof_plast, roof_add_column_plast = TabPageSoWith.definition_roof_not_raiding(self, current_bottom)
        dictance_template_first = int(self.data_well.current_bottom - roof_plast + 5)
        # print(f'дистанция первая {dictance_template_first}')
        self.dictance_template_first_Edit.setText(str(dictance_template_first))

        length_template_first, length_template_second = (
            TabPageSoWith.definition_ecn_true(self, self.data_well.dict_pump_ecn_depth["posle"]))
        self.length_template_first_Edit.setText(length_template_first)
        self.length_template_second_Edit.setText(str(length_template_second))

        first_template = self.template_first_Edit.text()
        template_second = int(self.template_second_Edit.text())
        length_template_first = int(self.length_template_first_Edit.text())

        dictance_template_first = int(self.dictance_template_first_Edit.text())

        length_template_second = int(self.length_template_second_Edit.text())
        dictance_template_second = int(self.dictance_template_second_Edit.text())

        self.template_first_Label.setParent(None)
        self.template_first_Edit.setParent(None)
        self.length_template_first_Label.setParent(None)
        self.length_template_first_Edit.setParent(None)

        self.dictance_template_first_Label.setParent(None)
        self.dictance_template_first_Edit.setParent(None)
        self.dictance_template_second_Edit.setParent(None)

        if self.data_well.column_additional or \
                (
                        self.data_well.head_column_additional.get_value >= self.data_well.current_bottom and self.data_well.column_additional is False):
            nkt_pod = '60мм' if self.data_well.column_additional_diameter.get_value < 110 else '73мм со снятыми фасками'

        if index == 'шаблон ЭК с хвостом':
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.length_template_first_Label, 4, 3)
            self.grid.addWidget(self.length_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)

            template_str = f'перо {kot_str} + шаблон-{first_template}мм L-2м + НКТ{nkt_diam}мм ' \
                           f'{dictance_template_first}м ' \
                           f'+  НКТ{nkt_diam}мм + шаблон-{template_second}мм' \
                           f' L-{length_template_second}м '

            # print(f'строка шаблона {template_str}')
            self.data_well.template_depth = int(roof_plast - 5)
            skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'



        elif index == 'шаблон без хвоста':
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)
            self.dictance_template_first_Edit.setParent(None)
            self.dictance_template_first_Label.setParent(None)

            template_str = f'перо {kot_str} + шаблон-{template_second}мм L-{length_template_second}м '
            self.data_well.template_depth = self.data_well.current_bottom
            skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

        elif index == 'шаблон открытый ствол':

            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            # self.grid.addWidget(self.length_template_first_Label, 4, 3)
            # self.grid.addWidget(self.length_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)
            # self.grid.addWidget(self.length_template_second_Label, 4, 9)
            # self.grid.addWidget(self.length_template_second_Edit, 5, 9)

            self.template_first_Edit.setText('фильтр направление')
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            self.dictance_template_second_Edit.setText(str(10))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'фильтр-направление L-2 {kot_str}+ НКТ{nkt_diam}м {dictance_template_first}м +' \
                           f'шаблон-{template_second}мм L-{length_template_second}м '
            self.data_well.template_depth = int(roof_plast - 5)

            skm_teml_str = f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

        elif index == 'шаблон ДП с хвостом':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.length_template_first_Label, 4, 4)
            self.grid.addWidget(self.length_template_first_Edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.length_template_second_Label, 4, 8)
            self.grid.addWidget(self.length_template_second_Edit, 5, 8)

            dictance_template_first = int(self.data_well.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            dictance_template_second = int(
                roof_add_column_plast - self.data_well.head_column_additional.get_value - int(
                    self.length_template_first_Edit.text()) + 5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))

            template_str = f'обточная муфта {kot_str} + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f' + шаблон-{first_template}мм ' \
                           f'L-{length_template_first}м + НКТ{nkt_pod} {dictance_template_second}м + ' \
                           f'шаблон-{template_second}мм L-{length_template_second}м '
            self.data_well.template_depth = math.ceil(
                roof_add_column_plast - 5 - length_template_first - dictance_template_second)
            self.data_well.template_depth_addition = math.ceil(roof_add_column_plast - 5)

            skm_teml_str = f'шаблон-{first_template}мм до гл.{self.data_well.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

        elif index == 'шаблон ДП без хвоста':
            self.dictance_template_first_Edit.setParent(None)
            self.dictance_template_first_Label.setParent(None)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.length_template_first_Label, 4, 3)
            self.grid.addWidget(self.length_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 6)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 6)
            self.grid.addWidget(self.template_second_Label, 4, 7)
            self.grid.addWidget(self.template_second_Edit, 5, 7)
            self.grid.addWidget(self.length_template_second_Label, 4, 8)
            self.grid.addWidget(self.length_template_second_Edit, 5, 8)

            dictance_template_second = int(
                self.data_well.current_bottom - self.data_well.head_column_additional.get_value
                - int(length_template_first) + 5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'обточная муфта {kot_str} + шаблон-{first_template}мм L-{length_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                           f'L-{length_template_second}м '

            self.data_well.template_depth = math.ceil(
                self.data_well.current_bottom - dictance_template_second -
                length_template_first)
            self.data_well.template_depth_addition = math.ceil(self.data_well.current_bottom)

            skm_teml_str = f'шаблон-{first_template}мм до гл.{self.data_well.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'



        elif index == 'шаблон ДП открытый ствол':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.length_template_first_Label, 4, 4)
            self.grid.addWidget(self.length_template_first_Edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.length_template_second_Label, 4, 8)
            self.grid.addWidget(self.length_template_second_Edit, 5, 8)

            dictance_template_first = int(self.data_well.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            dictance_template_first = int(self.dictance_template_first_Edit.text())

            dictance_template_second = int(
                roof_add_column_plast - self.data_well.head_column_additional.get_value - int(
                    self.length_template_first_Edit.text()) + 5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))

            template_str = f'фильтр направление {kot_str}+ НКТ{nkt_pod} {dictance_template_first}м ' \
                           f' + шаблон-{first_template}мм L-{length_template_first}м' \
                           f' + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                           f'L-{length_template_second}м '
            self.data_well.template_depth = math.ceil(
                roof_add_column_plast - 5 - length_template_first - dictance_template_second)
            self.data_well.template_depth_addition = math.ceil(roof_add_column_plast - 5)

            skm_teml_str = f'шаблон-{first_template}мм до гл.{self.data_well.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{self.data_well.template_depth}м'

        self.template_str_Edit.setText(template_str)
        self.skm_teml_str_Edit.setText(skm_teml_str)

        if 'ПОМ' in str(self.data_well.paker_before["posle"]).upper() and \
                '122' in str(self.data_well.paker_before["posle"]):
            self.template_second_Edit.setText(str(126))

    def definition_ecn_true(self, depth_ecn):

        if self.data_well.column_additional is False and self.data_well.dict_pump_ecn["posle"] != 0:
            return "2", "30"
        elif self.data_well.column_additional is False and self.data_well.max_angle.get_value > 45:
            return "2", "10"
        elif self.data_well.column_additional is True and self.data_well.dict_pump_ecn["posle"] != 0:
            if self.data_well.dict_pump_ecn["posle"] != 0 and \
                    float(depth_ecn) < self.data_well.head_column_additional.get_value:
                return "2", "30"

            elif self.data_well.dict_pump_ecn["posle"] != 0 and \
                    float(depth_ecn) >= self.data_well.head_column_additional.get_value:
                return "30", "4"
            elif self.data_well.max_angle.get_value > 45:
                return "10", "4"
        else:
            return "2", "4"


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Выбор компоновки шаблонов')


class TemplateWithoutSkm(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)


        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.rir_paker = None
        self.paker_select = None
        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        distance_second = int(self.tabWidget.currentWidget().dictance_template_second_Edit.text())
        distance_first = int(self.tabWidget.currentWidget().dictance_template_first_Edit.text())
        template_str = str(self.tabWidget.currentWidget().template_str_Edit.text())
        template = str(self.tabWidget.currentWidget().template_Combo.currentText())
        template_length = int(float(self.tabWidget.currentWidget().length_template_second_Edit.text()))
        if self.data_well.column_additional:
            template_length_addition = int(float(self.tabWidget.currentWidget().length_template_first_Edit.text()))
        if self.data_well.column_additional is False or (
                self.data_well.column_additional is True and float(
            self.data_well.head_column_additional.get_value) >= self.data_well.current_bottom):
            template_diameter = int(self.tabWidget.currentWidget().template_second_Edit.text())
        else:
            template_diameter = int(self.tabWidget.currentWidget().template_first_Edit.text())
        # print(f'проблема ЭК {self.data_well.problem_with_ek_diameter}')
        if (template_diameter >= int(self.data_well.problem_with_ek_diameter) - 2
                and self.data_well.template_depth > int(self.data_well.problem_with_ek_depth)):
            QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if self.data_well.column_additional is False or \
                self.data_well.column_additional and \
                self.data_well.current_bottom < self.data_well.head_column_additional.get_value:
            if self.data_well.template_depth > self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
        else:
            if self.data_well.template_depth_addition > self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
            if self.data_well.template_depth >= self.data_well.head_column_additional.get_value:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже головы хвостовика')
                return
            # if self.template_Combo.currentText() == 'ПСШ Доп колонна СКМ в основной колонне' and\
            #         self.data_well.skm_depth >= self.data_well.head_column_additional.get_value:
            #     QMessageBox.warning(self, "ВНИМАНИЕ", 'СКМ спускается ниже головы хвостовика')
            #     return
        if distance_second < 0 or distance_first < 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Расстояние между шаблонами не корректно')
            return
        self.data_well.template_length = template_length
        if self.data_well.column_additional:
            self.data_well.template_length_addition = template_length_addition
        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            self.data_well.current_bottom = round(float(current_bottom), 1)

        self.update_template(self.data_well.insert_index)
        self.privyazka_question = self.tabWidget.currentWidget().privyazka_question_QCombo.currentText()
        if self.privyazka_question == 'Да':
            mes = QMessageBox.question(self, 'Привязка', 'ЗУМПФ меньше 10м. '
                                                         'Привязка нужна, корректно ли?')
            if mes == QMessageBox.StandardButton.No:
                return
        if self.data_well.head_column.get_value != 0:
            if self.data_well.column_conductor_length.get_value <= self.data_well.template_depth:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Нельзя спускать шаблон ниже глубины башмака кондуктора '
                                    f'{self.data_well.column_conductor_length.get_value}м')

        work_list = self.template_ek(template_str, template, template_diameter)

        self.populate_row(self.insert_index, work_list, self.table_widget)

        data_list.pause = False
        self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        self.data_well.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def update_template(self, index_plan):

        row_index = index_plan - self.data_well.count_row_well
        template_ek = json.dumps(
            [self.data_well.template_depth, self.data_well.template_length,
             self.data_well.template_depth_addition,
             self.data_well.template_length_addition])
        for index, data in enumerate(self.data_well.data_list):
            if index == index:
                template_ek_old = self.data_well.data_list[index][11]
            if row_index < index:
                if self.data_well.data_list[index][11] == template_ek_old:
                    self.data_well.data_list[index][11] = template_ek

    def template_ek(self, template_str, template, temlate_ek):

        solvent_question = self.tabWidget.currentWidget().solvent_question_combo.currentText()
        solvent_volume_edit = self.tabWidget.currentWidget().solvent_volume_edit.text()
        if solvent_volume_edit != '':
            solvent_volume_edit = round(float(solvent_volume_edit), 1)

        self.note_question_qcombo = self.tabWidget.currentWidget().note_question_qcombo.currentText()
        self.kot_question_qcombo = self.tabWidget.currentWidget().kot_question_qcombo.currentText()

        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round(float(current_bottom), 1)

        list_template_ek = [
            [f'Cпустить {template_str} на НКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{self.data_well.nkt_diam}мм  с замером,'
             f' шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom, 1.2)],
            [f'Нормализовать до глубины {current_bottom}м.',
             None, f'ПРИ НЕОБХОДИМОСТИ: \nНормализовать забой обратной промывкой тех жидкостью уд.весом '
                   f'{self.data_well.fluid_work} до глубины {current_bottom}м.', None, None, None, None, None,
             None, None,
             'Мастер КРС', None],
            [f'Обработка растворителем в V-{solvent_volume_edit}', None,
             f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
             f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3. При открытом '
             f'затрубном пространстве закачать в '
             f'трубное пространство растворитель в объеме {solvent_volume_edit}м3, продавить в '
             f'трубное пространство тех.жидкостью '
             f'в объеме {round(3 * float(current_bottom) / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [f'Промыть в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work} '
             f'при расходе жидкости 6-8 л/сек '
             f'в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. ПРИ '
             f'ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ,'
             f' ДОПУСТИМАЯ ОСЕВАЯ '
             f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', well_volume_norm(TemplateKrs.well_volume(self) * 1.5)],
            [
                f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. Определение '
                f'текущего забоя',
                None,
                f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. '
                f'Определение текущего забоя, при '
                f'необходимости повторная промывка.',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', 2.49],

        ]
        if abs(self.data_well.perforation_sole - current_bottom) > 10:
            list_template_ek.pop(-2)

        if self.kot_question_qcombo == 'Да' and self.data_well.count_template == 0:
            list_template_ek.insert(-1, ['опрессовать тНКТ на 150атм', None,
                                         f'Перед подъемом опрессовать тНКТ на давление 150атм. ',
                                         None, None, None, None, None, None, None,
                                         'Мастер КРС', 0.7])

        aa = 'КР11' in self.data_well.type_kr, self.data_well.type_kr
        if 'КР11' in self.data_well.type_kr:
            definition_q_list = [
                [f'Насыщение 5м3 определение Q при 80-120атм', None,
                 f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                 f' на приемистость в трех режимах при Р=80-120атм в '
                 f'присутствии представителя супервайзерской службы'
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                 f'с подтверждением за 2 часа до '
                 f'начала работ). ',
                 None, None, None, None, None, None, None,
                 'мастер КРС, УСРСиСТ', 0.17 + 0.2 + 0.2 + 0.2 + 0.15 + 0.52]]

            list_template_ek.extend(definition_q_list)

        list_template_ek.append([None, None,
                                 f'Поднять {template_str} на НКТ{self.data_well.nkt_diam}мм с глубины '
                                 f'{current_bottom}м с доливом скважины в '
                                 f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом '
                                 f'{self.data_well.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'Мастер КРС', liftingNKT_norm(current_bottom, 1.2)])

        notes_list = [
            [None, None,
             f'ПРИМЕЧАНИЕ №1: При не прохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного '
             f'двигателя с райбером d={temlate_ek + 1}мм, {temlate_ek - 1}мм, {temlate_ek - 3}мм, '
             f'{temlate_ek - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
             f'гл.{current_bottom}м с последующим СПО шаблона {temlate_ek}мм на ТНКТ под промывку '
             f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
             f'на ТНКТ с гл. {current_bottom}м вести с доливом скважины до устья т/ж '
             f'удел.весом {self.data_well.fluid_work} в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 ',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None],
            [None, None,
             f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с '
             f'долотом {temlate_ek};'
             f' {temlate_ek - 2}; {temlate_ek - 4}мм  фрезера-{temlate_ek}мм, райбера-{temlate_ek + 1}мм и '
             f'другого оборудования и '
             f'инструмента, (при необходимости  ловильного), при необходимости на СБТ для восстановления '
             f'проходимости ствола  '
             f'и забоя скважины с применением мех.ротора, до текущего забоя с последующей нормализацией до '
             f'планового '
             f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{current_bottom}м '
             f'вести с доливом '
             f'скважины до устья т/ж удел.весом {self.data_well.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС',
             None],
            [None, None,
             f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию '
             f'№2 произвести '
             f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.'
             f'{current_bottom}м вести с '
             f'доливом скважины до устья т/ж удел.весом с доливом c'
             f'скважины до устья т/ж удел.весом {self.data_well.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None],

            [None, None,
             f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 '
             f'до планового '
             f'текущего забоя. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке  '
             f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
             f'на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {self.data_well.fluid_work} в '
             f'объеме {round(current_bottom * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
            [None, None,
             f'Примечание №5: В случае необходимости по результатам восстановления проходимости '
             f'эксплуатационной колонны '
             f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
             f'проходимость. Подъем компоновки на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {self.data_well.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

        privyazka_nkt = [f'Привязка по ГК и ЛМ По привязному НКТ удостовериться в наличии текущего забоя', None,
                         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС'
                         f' {data_list.contractor}".'
                         f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                         f' По привязному НКТ удостовериться в наличии'
                         f'текущего забоя с плановым, Нормализовать забой обратной промывкой тех жидкостью '
                         f'уд.весом {self.data_well.fluid_work}   до глубины {current_bottom}м',
                         None, None, None, None, None, None, None, 'Мастер КРС', None, None]
        if self.privyazka_question == "Да":
            list_template_ek.insert(-1, privyazka_nkt)

        if self.data_well.gips_in_well is True and self.data_well.count_template == 0:
            # Добавление работ при наличии Гипсово-солевых отложений
            gips = TemplateKrs.pero(self)
            for row in gips[::-1]:
                list_template_ek.insert(0, row)

        if self.note_question_qcombo == "Да":
            list_template_ek = list_template_ek + notes_list
            self.data_well.count_template += 1
        else:
            list_template_ek = list_template_ek
        if solvent_question == 'Нет':
            list_template_ek.pop(1)
        else:
            self.calculate_chemistry('растворитель', solvent_volume_edit)
        if self.data_well.head_column.get_value != 0:
            self.data_well.current_bottom = current_bottom
        return list_template_ek

    def pero(self):
        from .rir import RirWindow
        from .drilling import Drill_window

        pero_list = RirWindow.pero_select(self, self.data_well.current_bottom)
        gips_pero_list = [
            [f'Спустить {pero_list}  на тНКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить {pero_list}  на тНКТ{self.data_well.nkt_diam}мм до глубины '
             f'{self.data_well.current_bottom}м '
             f'с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. '
             f'Опрессовать НКТ на 150атм. Вымыть шар. \n'
             f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [f'Промывка уд.весом {self.data_well.fluid_work_short} в объеме'
             f' {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work} '
             f'при расходе жидкости '
             f'6-8 л/сек в присутствии представителя Заказчика в объеме '
             f'{round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ '
             f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
             f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(self.data_well.current_bottom - 20, 1)}м. Тех отстой 2ч. '
             f'Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{self.data_well.nkt_diam}мм с глубины '
             f'{self.data_well.current_bottom}м с доливом скважины в '
             f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех.'
             f' жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             round(
                 self.data_well.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * self.data_well.current_bottom / 9.5 + 0.17 + 0.5,
                 2)],
            [None, None,
             f'В случае не до хождения пера до текущего забоя работы продолжить:',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             None]
        ]
        if self.data_well.gips_in_well is True:

            if self.data_well.dict_pump_shgn["do"] != 0:

                gips_pero_list = [gips_pero_list[-1]]
                from .drilling import Drill_window
                if self.raid_window is None:
                    self.raid_window = Drill_window(self.table_widget, self.insert_index)
                    # self.raid_window.setGeometry(200, 400, 300, 400)
                    self.raid_window.show()
                    self.pause_app()
                    drill_work_list = self.raid_window.add_work()
                    data_list.pause = True

                    self.raid_window = None
                else:
                    self.raid_window.close()  # Close window.
                    self.raid_window = None

                for row in drill_work_list:
                    gips_pero_list.append(row)
            else:
                if self.raid_window is None:
                    self.raid_window = Drill_window(self.table_widget, self.insert_index)
                    # self.raid_window.setGeometry(200, 400, 300, 400)
                    self.raid_window.show()
                    self.pause_app()
                    drill_work_list = self.raid_window.add_work()
                    data_list.pause = True

                    self.raid_window = None
                else:
                    self.raid_window.close()  # Close window.
                    self.raid_window = None
                for row in drill_work_list:
                    gips_pero_list.append(row)

        return gips_pero_list


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = TemplateWithoutSkm(22, 22)
    window.show()
    app.exec_()
