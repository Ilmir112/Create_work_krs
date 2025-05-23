import json
import math
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, \
    QGridLayout, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QApplication

import data_list
from PyQt5.QtCore import Qt

from work_py.opressovka import OpressovkaEK
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm, well_volume_norm
from PyQt5.QtGui import QDoubleValidator
from work_py.calculate_work_parametrs import volume_work


class TabPageSoWith(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.template_labelType = QLabel("Вид компоновки ПСШ", self)
        self.template_combo = QComboBox(self)

        self.template_str_Label = QLabel("строчка с шаблонами", self)
        self.template_str_edit = QLineEdit(self)

        self.skm_teml_str_Label = QLabel("глубины спуска шаблонов", self)
        self.skm_teml_str_edit = QLineEdit(self)

        self.template_first_Label = QLabel("диаметр первого шаблона", self)
        self.template_first_edit = QLineEdit(self)
        self.template_first_edit.setValidator(self.validator_int)

        self.length_template_first_Label = QLabel("длина первого шаблона", self)
        self.length_template_first_edit = QLineEdit(self)
        self.length_template_first_edit.setValidator(self.validator_int)

        self.dictance_template_first_Label = QLabel("расстояние", self)
        self.dictance_template_first_edit = QLineEdit(self)
        self.dictance_template_first_edit.setValidator(self.validator_int)

        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        if parent:
            if self.data_well.current_bottom - self.data_well.perforation_roof <= 10 \
                    and self.data_well.open_trunk_well is False and self.data_well.count_template != 0:
                self.privyazka_question_QCombo.setCurrentIndex(1)

        self.note_label = QLabel("Нужно ли добавлять примечание", self)
        self.note_question_qcombo = QComboBox(self)
        self.note_question_qcombo.addItems(['Нет', 'Да'])

        self.kot_label = QLabel("Нужно ли добавлять систему КОТ-50", self)
        self.kot_question_qcombo = QComboBox(self)

        self.kot_question_qcombo.addItems(['Нет', 'Да'])

        self.solvent_label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(self.validator_int)
        self.solvent_volume_edit.setText("2")

        self.solvent_question_label = QLabel("необходимость растворителя", self)
        self.solvent_question_combo = QComboBox(self)
        self.solvent_question_combo.addItems(['Нет', 'Да'])

        if parent:
            if self.data_well.count_template == 0:
                self.note_question_qcombo.setCurrentIndex(1)
                self.solvent_question_combo.setCurrentIndex(1)

        self.skm_label = QLabel("диаметр СКМ", self)
        self.skm_edit = QLineEdit(self)
        self.skm_edit.setValidator(self.validator_int)

        self.dictance_template_second_Label = QLabel("расстояние", self)
        self.dictance_template_second_edit = QLineEdit(self)
        self.dictance_template_second_edit.setValidator(self.validator_int)

        self.template_second_Label = QLabel("диаметр второго шаблона", self)
        self.template_second_edit = QLineEdit(self)
        self.template_second_edit.setValidator(self.validator_int)

        self.length_template_second_Label = QLabel("длина второго шаблона", self)
        self.length_template_second_edit = QLineEdit(self)
        self.length_template_second_edit.setValidator(self.validator_int)

        self.dictance_three_Label = QLabel("третья", self)
        self.dictance_three_edit = QLineEdit(self)
        self.dictance_three_edit.setValidator(self.validator_int)

        self.roof_skm_label = QLabel("Кровля скреперования", self)
        self.roof_skm_line = QLineEdit(self)
        self.roof_skm_line.setValidator(self.validator_int)
        self.roof_skm_line.setClearButtonEnabled(True)

        self.sole_skm_label = QLabel("Подошва скреперования", self)
        self.sole_skm_line = QLineEdit(self)
        self.sole_skm_line.setClearButtonEnabled(True)
        self.sole_skm_line.setValidator(self.validator_int)

        self.skm_type_label = QLabel("Тип скрепера", self)
        self.skm_type_combo = QComboBox(self)
        self.skm_type_combo.addItems(['СКМ', 'СГМ'])

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        if parent:
            self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')

        # self.grid = QGridLayout(self)
        self.template_combo.currentTextChanged.connect(self.update_template_edit)
        if parent:
            self.definition_template_work(float(self.current_bottom_edit.text()))

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

        self.grid.addWidget(self.template_str_Label, 11, 1, 1, 8)
        self.grid.addWidget(self.template_str_edit, 12, 1, 1, 8)

        self.grid.addWidget(self.skm_teml_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_edit, 14, 1, 1, 8)
        if parent:
            if self.data_well.column_additional is False or \
                    (self.data_well.column_additional and
                     self.data_well.head_column_additional.get_value >= self.data_well.current_bottom):
                first_template, template_second = self.template_diam_ek()
            else:
                first_template, template_second = self.template_diam_additional_ek()

        self.grid.addWidget(self.roof_skm_label, 35, 2, 1, 3)
        self.grid.addWidget(self.roof_skm_line, 36, 2, 1, 3)

        self.grid.addWidget(self.sole_skm_label, 35, 5, 1, 3)
        self.grid.addWidget(self.sole_skm_line, 36, 5, 1, 3)

        self.template_first_edit.setText(str(first_template))
        self.template_second_edit.setText(str(template_second))

        self.length_template_first_edit.setText(str(4))

        self.dictance_template_first_edit.editingFinished.connect(self.update_template)
        self.template_first_edit.editingFinished.connect(self.update_template)
        self.length_template_first_edit.editingFinished.connect(self.update_template)
        self.dictance_template_second_edit.editingFinished.connect(self.update_template)
        self.skm_edit.editingFinished.connect(self.update_template)
        self.dictance_three_edit.editingFinished.connect(self.update_template)
        self.template_second_edit.editingFinished.connect(self.update_template)
        self.length_template_second_edit.editingFinished.connect(self.update_template)
        self.current_bottom_edit.editingFinished.connect(self.update_template)
        self.skm_type_combo.currentTextChanged.connect(self.update_template)
        self.kot_question_qcombo.currentTextChanged.connect(self.update_template)
        if self.data_well:
            if self.data_well.plast_work and 'Ойл' in data_list.contractor and \
                    'открытый ствол' not in self.template_combo.currentText():
                self.kot_question_qcombo.setCurrentIndex(1)
            else:
                self.kot_question_qcombo.setCurrentIndex(0)

    def definition_template_work(self, current_bottom):
        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and current_bottom < self.data_well.head_column_additional.get_value):
            self.template_select_list = ['', 'ПСШ ЭК', 'ПСШ открытый ствол', 'ПСШ без хвоста', 'ПСШ + пакер']

            self.template_combo.addItems(self.template_select_list)

            template_key = self.definition_pssh(current_bottom)
            self.template_combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_combo, 2, 2, 2, 8)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_edit, 5, 2)
            self.grid.addWidget(self.length_template_first_Label, 4, 3)
            self.grid.addWidget(self.length_template_first_edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_edit, 5, 4)
            self.grid.addWidget(self.skm_label, 4, 5)
            self.grid.addWidget(self.skm_edit, 5, 5)
            self.grid.addWidget(self.skm_type_label, 4, 6)
            self.grid.addWidget(self.skm_type_combo, 5, 6)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 7)
            self.grid.addWidget(self.dictance_template_second_edit, 5, 7)
            self.grid.addWidget(self.template_second_Label, 4, 8)
            self.grid.addWidget(self.template_second_edit, 5, 8)
            self.grid.addWidget(self.length_template_second_Label, 4, 9)
            self.grid.addWidget(self.length_template_second_edit, 5, 9)
            self.grid.addWidget(self.dictance_three_Label, 4, 10)
            self.grid.addWidget(self.dictance_three_edit, 5, 10)

        else:
            self.template_select_list = ['', 'ПСШ Доп колонна СКМ в основной колонне',
                                         'ПСШ СКМ в доп колонне + открытый ствол',
                                         'ПСШ СКМ в доп колонне c хвостом',
                                         'ПСШ СКМ в доп колонне без хвоста']

            self.template_combo.addItems(self.template_select_list)
            template_key = self.definition_pssh(current_bottom)
            # print(template_key)
            self.template_combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_combo, 2, 2, 2, 8)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_edit, 5, 2)

            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_edit, 5, 3)

            self.grid.addWidget(self.length_template_first_Label, 4, 4)
            self.grid.addWidget(self.length_template_first_edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_edit, 5, 5)
            self.grid.addWidget(self.skm_label, 4, 6)
            self.grid.addWidget(self.skm_edit, 5, 6)
            self.grid.addWidget(self.skm_type_label, 4, 7)
            self.grid.addWidget(self.skm_type_combo, 5, 7)
            self.grid.addWidget(self.dictance_three_Label, 4, 8)
            self.grid.addWidget(self.dictance_three_edit, 5, 8)
            self.grid.addWidget(self.template_second_Label, 4, 9)
            self.grid.addWidget(self.template_second_edit, 5, 9)
            self.grid.addWidget(self.length_template_second_Label, 4, 10)
            self.grid.addWidget(self.length_template_second_edit, 5, 10)

    def definition_pssh(self, current_bottom):
        if (self.data_well.column_additional is False or \
            (self.data_well.column_additional and
             self.data_well.current_bottom < self.data_well.head_column_additional.get_value)) \
                and self.data_well.open_trunk_well is False and \
                ((self.difference_date_days(self.data_well.date_commissioning.get_value) / 365 < 20 and \
                  self.data_well.category_h2s == "3") or (
                         self.difference_date_days(self.data_well.date_commissioning.get_value) / 365 < 10 \
                         and self.data_well.category_h2s != "3")):
            template_key = 'ПСШ + пакер'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is False or \
                (self.data_well.column_additional is True and self.data_well.open_trunk_well is False and all(
                    [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                     self.data_well.plast_work]) is False and \
                 current_bottom <= self.data_well.head_column_additional.get_value):
            template_key = 'ПСШ ЭК'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is True or \
                (self.data_well.column_additional is True and self.data_well.open_trunk_well is True and \
                 current_bottom <= self.data_well.head_column_additional.get_value and self.data_well.open_trunk_well):
            template_key = 'ПСШ открытый ствол'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is True or \
                (self.data_well.column_additional is True and self.data_well.open_trunk_well is False and all(
                    [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                     self.data_well.plast_work]) is True and \
                 current_bottom <= self.data_well.head_column_additional.get_value):
            template_key = 'ПСШ без хвоста'

        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is False and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is False:
            template_key = 'ПСШ СКМ в доп колонне c хвостом'

        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is True:
            template_key = 'ПСШ СКМ в доп колонне + открытый ствол'

        elif self.data_well.column_additional is True and all(
                [self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                 self.data_well.plast_work]) is True and self.data_well.open_trunk_well is False:
            template_key = 'ПСШ СКМ в доп колонне без хвоста'
        return template_key

    def update_template(self):
        skm_type = self.skm_type_combo.currentText()

        if self.current_bottom_edit.text() != '':
            current_bottom = round(float(self.current_bottom_edit.text()), 1)

        self.roof_plast, self.roof_add_column_plast = self.definition_roof_not_raiding(current_bottom)
        dictance_template_first = int(current_bottom - self.roof_plast + 5)
        if int(float(self.dictance_template_first_edit.text())) == dictance_template_first:
            self.dictance_template_first_edit.setText(str(int(dictance_template_first)))
        else:
            dictance_template_first = int(float(self.dictance_template_first_edit.text()))

        if self.template_first_edit.text() != '':
            first_template = self.template_first_edit.text()
        if self.length_template_first_edit.text() != '':
            length_template_first = int(float(self.length_template_first_edit.text()))
        if self.template_second_edit.text() != '':
            template_second = self.template_second_edit.text()
        if self.length_template_second_edit.text() != '':
            length_template_second = self.length_template_second_edit.text()
        if self.skm_edit.text() != '':
            skm = self.skm_edit.text()

        else:
            dictance_template_first = ''
        if self.dictance_template_second_edit.text() != '':
            dictance_template_second = int(float(self.dictance_template_second_edit.text()))
        else:
            dictance_template_second = ''
        if self.dictance_three_edit.text() != '':
            dictance_three = int(float(self.dictance_three_edit.text()))
        else:
            dictance_three = ''
        nkt_diam = self.data_well.nkt_diam
        valve = ''
        if self.kot_question_qcombo.currentText() == 'Да':
            kot_str = '+ КОТ-50'
            valve = "+ СК "
        else:
            kot_str = ''

        if self.data_well.column_additional or \
                (
                        self.data_well.head_column_additional.get_value >= current_bottom and self.data_well.column_additional is False):
            nkt_pod = '60мм' if self.data_well.column_additional_diameter.get_value < 110 else '73мм со снятыми фасками'

        if first_template != '' and length_template_first != '' and \
                template_second != '' and length_template_second != '' and \
                skm != '' and dictance_template_first != '' and \
                dictance_template_second != '' and first_template != '':
            template_str = ''
            if self.template_combo.currentText() == 'ПСШ ЭК':
                # if dictance_template_second != '':
                self.dictance_three_edit.setParent(None)
                self.dictance_three_Label.setParent(None)
                if first_template != 'фильтр направление':
                    template_str = f'перо {kot_str} + шаблон-{int(first_template)}мм L-{int(length_template_first)}м + ' \
                                   f'НКТ{nkt_diam}мм ' \
                                   f'{int(dictance_template_first)}м + {skm_type}-{skm} {valve}+  ' \
                                   f'НКТ{nkt_diam}мм {int(dictance_template_second)}м + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м '

                    self.template_depth = int(
                        current_bottom - int(dictance_template_first) - int(length_template_first)) - int(
                        dictance_template_second)

                    self.data_well.skm_depth = self.template_depth + dictance_template_second
                    skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'
            if self.template_combo.currentText() == 'ПСШ + пакер':
                # if dictance_template_second != '':
                # self.dictance_three_edit.setParent(None)
                # self.dictance_three_Label.setParent(None)
                if first_template != 'фильтр направление':
                    template_str = f'перо {kot_str} + шаблон-{int(first_template)}мм L-{int(length_template_first)}м + ' \
                                   f'НКТ{nkt_diam}мм ' \
                                   f'{int(dictance_template_first)}м + {skm_type}-{skm} {valve}+  ' \
                                   f'НКТ{nkt_diam}мм {int(dictance_template_second)}м + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м + НКТ{nkt_diam}мм L-{self.dictance_three_edit.text()}м + пакер ' \
                                   f'ПРОЯМО-{self.diameter_paker_edit.text()}мм (либо аналог) '

                    self.template_depth = int(
                        current_bottom - int(dictance_template_first) - int(length_template_first)) - int(
                        dictance_template_second)
                    self.paker_depth = self.template_depth - int(self.dictance_three_edit.text())

                    self.data_well.skm_depth = self.template_depth + dictance_template_second
                    skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'

            elif self.template_combo.currentText() == 'ПСШ без хвоста':
                if self.data_well.current_bottom - self.data_well.perforation_roof < 15:
                    self.dictance_template_second_edit.setText('1')
                    dictance_template_second = self.dictance_template_second_edit.text()
                # if dictance_template_second is not None:
                template_str = f'перо {kot_str}+ {skm_type}-{skm} {valve}+ НКТ{nkt_diam}мм {dictance_template_second:.0f}м ' \
                               f' + шаблон-{template_second}мм L-{length_template_second}м '
                self.template_depth = math.ceil(current_bottom - int(dictance_template_second))
                self.data_well.skm_depth = self.template_depth + int(dictance_template_second)
                skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

            elif self.template_combo.currentText() == 'ПСШ открытый ствол':

                # if dictance_template_second is not None:
                self.template_first_edit.setText('фильтр направление')
                template_str = f'фильтр-направление L {length_template_first}м {kot_str} + НКТ{nkt_diam}мм ' \
                               f'{dictance_template_first:.0f}м ' \
                               f'+ {skm_type}-{skm} {valve}+  НКТ{nkt_diam}мм {dictance_template_second:.0f}м + ' \
                               f'шаблон-{template_second}мм L-{length_template_second}м '
                self.template_depth = int(current_bottom - int(dictance_template_first) -
                                                    int(dictance_template_second) - int(length_template_first))

                self.data_well.skm_depth = self.template_depth + dictance_template_second
                skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

            elif self.template_combo.currentText() == 'ПСШ Доп колонна СКМ в основной колонне':
                if dictance_template_second != '' and dictance_template_first != '' and dictance_three != '':
                    template_str = f'обточная муфта {kot_str} + ' \
                                   f'НКТ{nkt_pod}  + {dictance_template_first:.0f}м + шаблон-{first_template}мм ' \
                                   f'L-{length_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_template_second:.0f}м + НКТ{nkt_diam} {dictance_three}м + ' \
                                   f'{skm_type}-{skm} {valve}+ шаблон-{template_second}мм L-{length_template_second}м '

                    self.template_depth_addition = current_bottom - int(dictance_template_first)

                    self.template_depth = int(float(current_bottom - int(dictance_template_first) - \
                                                              int(dictance_template_second) - int(
                        dictance_three)))
                    self.data_well.skm_depth = self.template_depth + dictance_three
                    # template_str = template_SKM_DP_EK
                    skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                                   f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'


            elif self.template_combo.currentText() == 'ПСШ СКМ в доп колонне c хвостом':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                        length_template_first != '' and first_template != '' and template_second != '' \
                        and length_template_second != '':
                    template_str = f'обточная муфта {kot_str}+ НКТ{nkt_pod} {dictance_template_first:.0f}м ' \
                                   f'+ {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f}м  +' \
                                   f' шаблон-{first_template}мм ' \
                                   f'L-{length_template_first}м + НКТ{nkt_pod} {dictance_three}м + ' \
                                   f'шаблон-{template_second}мм L-{length_template_second}м '

                    self.template_depth = int(current_bottom) - int(dictance_template_first) - \
                                                    int(dictance_template_second) - int(dictance_three) - \
                                                    int(length_template_first)

                    self.template_depth_addition = int(current_bottom) - int(
                        dictance_template_first) - \
                                                             int(dictance_template_second)

                    self.data_well.skm_depth = self.template_depth_addition + int(
                        dictance_template_second)

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                                   f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'

            elif self.template_combo.currentText() == 'ПСШ СКМ в доп колонне без хвоста':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                        length_template_first != '' and first_template != '' and template_second != '' \
                        and length_template_second != '':
                    template_str = f'обточная муфта {kot_str} + {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f} + ' \
                                   f' шаблон-{first_template}мм L-{length_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м '
                    self.template_depth_addition = current_bottom - int(dictance_template_second)

                    self.template_depth = int(
                        current_bottom - dictance_template_second - dictance_three - length_template_first)

                    self.data_well.skm_depth = current_bottom

                    skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'


            elif self.template_combo.currentText() == 'ПСШ СКМ в доп колонне + открытый ствол':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                        length_template_first != '' and first_template != '' and template_second != '' \
                        and length_template_second != '':
                    template_str = f'фильтр направление L-2м {kot_str} + НКТ{nkt_pod} {dictance_template_first:.0f}м ' \
                                   f'+ {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f}м + ' \
                                   f' шаблон-{first_template}мм ' \
                                   f'L-{length_template_first}м' \
                                   f' + НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м '
                    # if dictance_three and dictance_template_second and dictance_template_first and length_template_first:
                    self.template_depth_addition = int(current_bottom) - int(
                        dictance_template_first) - int(dictance_template_second)

                    self.template_depth = int(current_bottom) - int(dictance_template_first) - \
                                                    int(dictance_template_second) - int(dictance_three) - \
                                                    int(length_template_first)

                    self.data_well.skm_depth = self.template_depth_addition + int(
                        dictance_template_second)

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                                   f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м'
            if dictance_template_second != '' and dictance_template_first != '' and \
                    length_template_first != '' and first_template != '' and template_second != '' \
                    and length_template_second != '' and template_str != '':
                self.template_str_edit.setText(template_str)
                self.skm_teml_str_edit.setText(skm_teml_str)

    def update_template_edit(self, index):
        current_bottom = float(self.current_bottom_edit.text())
        if index != '':

            self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
            self.diameter_paker_edit = QLineEdit(self)

            if self.kot_question_qcombo.currentText() == 'Да':
                kot_str = '+ КОТ-50'
                valve = '+ СК'
            else:
                kot_str = ''
                valve = ''

            skm_type = self.skm_type_combo.currentText()

            nkt_diam = self.data_well.nkt_diam
            # print(self.data_well.column_additional, self.data_well.head_column_additional.get_value, current_bottom)
            if self.data_well.column_additional is False or (self.data_well.column_additional and
                                                             self.data_well.head_column_additional.get_value >= current_bottom):
                first_template, template_second = self.template_diam_ek()
                # print(f'диаметры шаблонов {first_template, template_second}')
            else:
                first_template, template_second = self.template_diam_additional_ek()
                # print(f'диаметры шаблонов {first_template, template_second}')

            if 'ПОМ' in str(self.data_well.paker_before["after"]).upper() and '122' in str(
                    self.data_well.paker_before["after"]):
                self.template_second_edit.setText(str(126))

            self.template_first_edit.setText(str(int(first_template)))
            self.template_second_edit.setText(str(int(template_second)))
            self.skm_edit.setText(str(self.data_well.column_diameter.get_value))
            self.dictance_template_second_edit.setText(str(1))

            self.roof_plast, self.roof_add_column_plast = self.definition_roof_not_raiding(current_bottom)
            dictance_template_first = float(current_bottom - self.roof_plast + 5)
            self.dictance_template_first_edit.setText(str(int(dictance_template_first)))

            length_template_first, length_template_second = self.definition_ecn_true(
                self.data_well.dict_pump_ecn_depth["after"])
            self.length_template_first_edit.setText(length_template_first)
            self.length_template_second_edit.setText(str(length_template_second))

            first_template = self.template_first_edit.text()
            template_second = int(self.template_second_edit.text())
            length_template_first = int(self.length_template_first_edit.text())

            length_template_second = int(self.length_template_second_edit.text())
            dictance_template_second = int(self.dictance_template_second_edit.text())
            skm = self.skm_edit.text()

            self.template_first_Label.setParent(None)
            self.template_first_edit.setParent(None)
            self.length_template_first_Label.setParent(None)
            self.length_template_first_edit.setParent(None)
            self.dictance_three_edit.setParent(None)
            self.dictance_three_edit.setParent(None)
            self.dictance_template_first_Label.setParent(None)
            self.dictance_template_first_edit.setParent(None)
            self.dictance_three_Label.setParent(None)
            self.dictance_three_edit.setParent(None)

            if self.data_well.column_additional or \
                    (self.data_well.head_column_additional.get_value >= current_bottom and \
                     self.data_well.column_additional is False):
                nkt_pod = '60мм' if self.data_well.column_additional_diameter.get_value < 110 else '73мм со снятыми фасками'

            if index == 'ПСШ ЭК':
                template_str = f'перо {kot_str} + шаблон-{first_template}мм L-{length_template_first}м + ' \
                               f'НКТ{nkt_diam}мм ' \
                               f'{dictance_template_first:.0f}м + {skm_type}-{skm} {valve}+ ' \
                               f'НКТ{nkt_diam}мм {dictance_template_second:.0f}м  +  шаблон-{template_second}мм ' \
                               f'L-{length_template_second}м '

                # print(f'строка шаблона {template_str}')
                self.template_depth = int(current_bottom - dictance_template_first -
                                                    length_template_first - dictance_template_second)
                self.data_well.skm_depth = self.template_depth + dictance_template_second
                skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

                self.grid.addWidget(self.template_first_Label, 4, 2)
                self.grid.addWidget(self.template_first_edit, 5, 2)
                self.grid.addWidget(self.length_template_first_Label, 4, 3)
                self.grid.addWidget(self.length_template_first_edit, 5, 3)
                self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 9)
                self.grid.addWidget(self.length_template_second_edit, 5, 9)


            elif index == 'ПСШ без хвоста':
                template_str = f'перо {kot_str} + {skm_type}-{skm} {valve}+ {dictance_template_second:.0f}м ' \
                               f'НКТ{nkt_diam}м + шаблон-{template_second}мм L-{length_template_second}м '
                self.template_depth = math.ceil(current_bottom - int(dictance_template_second))
                self.data_well.skm_depth = current_bottom
                skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

            elif index == 'ПСШ открытый ствол':

                # self.grid.addWidget(self.template_first_Label, 4, 2)
                # self.grid.addWidget(self.template_first_edit, 5, 2)

                self.template_first_edit.setText('фильтр направление')
                self.dictance_template_first_edit.setText(str(int(dictance_template_first)))
                self.dictance_template_second_edit.setText(str(1))
                dictance_template_first = int(float(self.dictance_template_first_edit.text()))
                dictance_template_second = int(float(self.dictance_template_second_edit.text()))

                template_str = f'фильтр-направление {kot_str} + НКТ{nkt_diam}мм {dictance_template_first:.0f}м ' \
                               f'+ {skm_type}-{skm} {valve}+ {dictance_template_second:.0f}м НКТ{nkt_diam}мм + ' \
                               f'шаблон-{template_second}мм L-{length_template_second}м '
                self.template_depth = int(float(
                    current_bottom - dictance_template_first - dictance_template_second))
                self.data_well.skm_depth = self.template_depth + dictance_template_second

                skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

                self.grid.addWidget(self.length_template_first_Label, 4, 3)
                self.grid.addWidget(self.length_template_first_edit, 5, 3)
                self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 9)
                self.grid.addWidget(self.length_template_second_edit, 5, 9)

            elif index == 'ПСШ Доп колонна СКМ в основной колонне':

                self.length_template_first_edit.setText(str(length_template_first))
                length_template_first = int(float(self.length_template_first_edit.text()))
                dictance_template_first1 = int(float(current_bottom - self.roof_add_column_plast + 5))

                self.skm_edit.setText(str(self.data_well.column_diameter.get_value))
                self.dictance_template_first_edit.setText(str(int(dictance_template_first1)))
                dictance_template_first = int(float(self.dictance_template_first_edit.text()))
                dictance_template_second = int(float(current_bottom - dictance_template_first1 - \
                                                     length_template_first - self.data_well.head_column_additional.get_value + 5))
                self.dictance_template_second_edit.setText(str(int(float(dictance_template_second))))

                self.length_template_second_edit.setText(str(length_template_second))

                dictance_template_three = round(current_bottom - dictance_template_first - \
                                                int(dictance_template_second) - length_template_first - self.roof_plast + 10,
                                                0)
                self.dictance_three_edit.setText(str(dictance_template_three))

                template_str = f'обточная муфта {kot_str} + ' \
                               f'НКТ{nkt_pod} + {dictance_template_first:.0f}м + шаблон-{first_template}мм ' \
                               f'L-{length_template_first}м + ' \
                               f'НКТ{nkt_pod} {dictance_template_second:.0f}м +' \
                               f'{skm_type}-{skm} {valve}+ НКТ{nkt_diam} {dictance_template_three}м + ' \
                               f' шаблон-{template_second}мм L-{length_template_second}м '

                self.template_depth_addition = int(float(current_bottom - dictance_template_first))
                self.template_depth = int(float(
                    current_bottom - dictance_template_first - length_template_first -
                    dictance_template_second - dictance_template_three))
                self.data_well.skm_depth = self.template_depth + dictance_template_three
                # template_str = template_SKM_DP_EK
                skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

                self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 2)
                self.grid.addWidget(self.template_first_Label, 4, 3)
                self.grid.addWidget(self.template_first_edit, 5, 3)
                self.grid.addWidget(self.length_template_first_Label, 4, 4)
                self.grid.addWidget(self.length_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 11)
                self.grid.addWidget(self.length_template_second_edit, 5, 11)
                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)


            elif index == 'ПСШ СКМ в доп колонне c хвостом':

                skm = str(self.data_well.column_additional_diameter.get_value)
                self.skm_edit.setText(skm)

                dictance_template_first = int(float(current_bottom - self.roof_add_column_plast + 5))
                self.dictance_template_first_edit.setText(str(int(dictance_template_first)))

                dictance_template_three = round((current_bottom - dictance_template_first - \
                                                 int(dictance_template_second) - length_template_first) - self.roof_plast + 10,
                                                0)

                self.dictance_three_edit.setText(str(dictance_template_three))

                template_str = f'обточная муфта {kot_str} + НКТ{nkt_pod} {dictance_template_first:.0f}м ' \
                               f'+ {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f}м + шаблон-{first_template}мм ' \
                               f'L-{length_template_first}м + НКТ{nkt_pod} {dictance_template_three}м + ' \
                               f'шаблон-{template_second}мм L-{length_template_second}м '

                self.template_depth = math.ceil(current_bottom -
                                                          dictance_template_first - dictance_template_second -
                                                          length_template_first - dictance_template_three)

                self.template_depth_addition = math.ceil(current_bottom - dictance_template_first -
                                                                   dictance_template_second)

                self.data_well.skm_depth = self.template_depth_addition + dictance_template_second

                skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

                self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 2)
                self.grid.addWidget(self.template_first_Label, 4, 3)
                self.grid.addWidget(self.template_first_edit, 5, 3)
                self.grid.addWidget(self.length_template_first_Label, 4, 4)
                self.grid.addWidget(self.length_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 11)
                self.grid.addWidget(self.length_template_second_edit, 5, 11)
                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)

            elif index == 'ПСШ СКМ в доп колонне без хвоста':

                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)

                dictance_template_first = 0
                self.dictance_template_first_edit.setText(str(int(dictance_template_first)))

                skm = str(self.data_well.column_additional_diameter.get_value)
                self.skm_edit.setText(skm)
                dictance_template_second = 10
                self.dictance_template_second_edit.setText(str(int(float(dictance_template_second))))

                dictance_template_three = round((current_bottom - dictance_template_first - \
                                                 dictance_template_second - length_template_first) - self.roof_plast + 10,
                                                0)

                self.dictance_three_edit.setText(str(dictance_template_three))

                template_str = f'обточная муфта {kot_str} + {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f} + ' \
                               f'шаблон-{first_template}мм L-{length_template_first}м + ' \
                               f'НКТ{nkt_pod} {dictance_template_three}м + шаблон-{template_second}мм ' \
                               f'L-{length_template_second}м '

                self.template_depth = math.ceil(current_bottom - dictance_template_second -
                                                          length_template_first - dictance_template_three)
                self.template_depth_addition = math.ceil(current_bottom - dictance_template_second)
                self.data_well.skm_depth = self.template_depth_addition + dictance_template_second
                skm_teml_str = f'до глубины {self.data_well.skm_depth}м,' \
                               f' шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'

                self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 2)
                self.grid.addWidget(self.template_first_Label, 4, 3)
                self.grid.addWidget(self.template_first_edit, 5, 3)
                self.grid.addWidget(self.length_template_first_Label, 4, 4)
                self.grid.addWidget(self.length_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 11)
                self.grid.addWidget(self.length_template_second_edit, 5, 11)
                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)

            elif index == 'ПСШ СКМ в доп колонне + открытый ствол':
                skm = str(self.data_well.column_additional_diameter.get_value)
                self.skm_edit.setText(skm)

                dictance_template_first = int(float(current_bottom - self.roof_add_column_plast + 5))
                self.dictance_template_first_edit.setText(str(int(dictance_template_first)))

                dictance_template_three = round((current_bottom - dictance_template_first - \
                                                 dictance_template_second - length_template_first) - self.roof_plast + 10,
                                                0)
                self.dictance_three_edit.setText(str(dictance_template_three))

                template_str = f'фильтр направление L-2м {kot_str} + НКТ{nkt_pod} {dictance_template_first:.0f}м ' \
                               f'+ {skm_type}-{skm} {valve}+ НКТ{nkt_pod} {dictance_template_second:.0f}м + ' \
                               f'шаблон-{first_template}мм ' \
                               f'L-{length_template_first}м' \
                               f' + НКТ{nkt_pod} {dictance_template_three}м + шаблон-{template_second}мм ' \
                               f'L-{length_template_second}м '

                self.template_depth = math.ceil(current_bottom -
                                                          dictance_template_first - dictance_template_second -
                                                          length_template_first - dictance_template_three)
                self.template_depth_addition = math.ceil(current_bottom -
                                                                   dictance_template_first - dictance_template_second)
                self.data_well.skm_depth = self.template_depth_addition + dictance_template_second

                skm_teml_str = f'шаблон-{first_template}мм до гл.{self.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{self.template_depth}м'
                self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 2)
                self.grid.addWidget(self.template_first_Label, 4, 3)
                self.grid.addWidget(self.template_first_edit, 5, 3)
                self.grid.addWidget(self.length_template_first_Label, 4, 4)
                self.grid.addWidget(self.length_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 11)
                self.grid.addWidget(self.length_template_second_edit, 5, 11)
                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)

            if index == 'ПСШ + пакер':
                template_depth = int(current_bottom - dictance_template_first -
                                     length_template_first - dictance_template_second)
                diameter_paker = int(float(self.paker_diameter_select(template_depth)))

                self.diameter_paker_edit.setText(str(diameter_paker))

                self.grid.addWidget(self.template_first_Label, 4, 2)
                self.grid.addWidget(self.template_first_edit, 5, 2)
                self.grid.addWidget(self.length_template_first_Label, 4, 3)
                self.grid.addWidget(self.length_template_first_edit, 5, 3)
                self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
                self.grid.addWidget(self.dictance_template_first_edit, 5, 4)
                self.grid.addWidget(self.length_template_second_Label, 4, 9)
                self.grid.addWidget(self.length_template_second_edit, 5, 9)
                self.grid.addWidget(self.dictance_three_Label, 4, 10)
                self.grid.addWidget(self.dictance_three_edit, 5, 10)
                self.grid.addWidget(self.diameter_paker_label_type, 4, 11)
                self.grid.addWidget(self.diameter_paker_edit, 5, 11)
                if diameter_paker != '':
                    template_str = f'перо {kot_str} + шаблон-{first_template}мм L-{length_template_first}м + ' \
                                   f'НКТ{nkt_diam}мм ' \
                                   f'{dictance_template_first:.0f}м + {skm_type}-{skm} {valve}+ ' \
                                   f'НКТ{nkt_diam}мм {dictance_template_second:.0f}м + шаблон-{template_second}мм ' \
                                   f'L-{length_template_second}м + НКТ{nkt_diam}мм L-{20}м + пакер ПРОЯМО-{diameter_paker}'

                    # print(f'строка шаблона {template_str}')
                    self.template_depth = template_depth
                    self.dictance_three_edit.setText(str(20))
                    self.paker_depth = self.template_depth - float(self.dictance_three_edit.text())
                    self.data_well.skm_depth = self.template_depth + dictance_template_second
                    skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м, ' \
                                   f'шаблон-{template_second}мм до гл.{self.template_depth}м,' \
                                   f' пакер до глубины {int(self.paker_depth)}м'
                self.dictance_three_edit.textChanged.connect(self.update_paker_depth)

            else:
                # self.dictance_three_Label.setParent(None)
                # self.dictance_three_edit.setParent(None)
                self.diameter_paker_label_type.setParent(None)
                self.diameter_paker_edit.setParent(None)

            self.template_str_edit.setText(template_str)
            self.skm_teml_str_edit.setText(skm_teml_str)

    def update_paker_depth(self, text):
        if text:
            paker_diameter = int(float(self.paker_diameter_select(self.template_depth)))
            self.diameter_paker_edit.setText(str(paker_diameter))

    def definition_ecn_true(self, depth_ecn):

        if self.data_well.column_additional is False and self.data_well.dict_pump_ecn["after"] != 0 and \
                self.data_well.column_diameter.get_value > 168:
            return "4", "4"
        elif self.data_well.column_additional is False and self.data_well.dict_pump_ecn["after"] != 0:
            return "4", "30"
        elif self.data_well.column_additional is False and self.data_well.max_angle.get_value > 45:
            return "4", "10"
        elif self.data_well.column_additional is True and self.data_well.dict_pump_ecn["after"] != 0 \
                and self.data_well.column_additional_diameter.get_value < 170:
            if self.data_well.dict_pump_ecn["after"] != 0 and float(
                    depth_ecn) < self.data_well.head_column_additional.get_value and \
                    self.data_well.column_diameter.get_value > 168:
                return "4", "4"
            elif self.data_well.dict_pump_ecn["after"] != 0 and \
                    float(depth_ecn) < self.data_well.head_column_additional.get_value:
                return "4", "30"
            elif self.data_well.dict_pump_ecn["after"] != 0 and \
                    float(depth_ecn) >= self.data_well.head_column_additional.get_value:
                return "30", "4"

        elif self.data_well.max_angle.get_value > 45 and self.data_well.current_bottom > \
                self.data_well.head_column_additional.get_value:
            return "10", "4"
        elif self.data_well.max_angle.get_value > 45 and self.data_well.current_bottom < \
                self.data_well.head_column_additional.get_value:
            return "4", "10"
        else:
            return "4", "4"

            # print(f' ЭЦН длина" {data_list.lift_ecn_can, data_list.lift_ecn_can_addition, "ЭЦН" in str(data_list.dict_pump["after"][0]).upper()}')

    def definition_roof_not_raiding(self, current_bottom):

        dict_perforation = self.data_well.dict_perforation
        plast_all = list(dict_perforation.keys())
        roof_plast = current_bottom
        roof_add_column_plast = current_bottom
        if self.data_well.column_additional is False or (
                self.data_well.column_additional and self.data_well.head_column_additional.get_value >= current_bottom):
            for plast in plast_all:
                roof = min(list(map(lambda x: float(x[0]), list(dict_perforation[plast]['интервал']))))

                if roof_plast > roof and roof < current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and self.data_well.open_trunk_well is False:
                        roof_add_column_plast = roof_plast
                    elif self.data_well.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = self.data_well.shoe_column.get_value
                        roof_add_column_plast = current_bottom

                    else:
                        roof_plast = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
                        roof_add_column_plast = roof
                else:
                    roof_add_column_plast = roof_plast
        elif self.data_well.column_additional:
            for plast in plast_all:
                roof_plast_in = dict_perforation[plast]['кровля']

                if self.data_well.head_column_additional.get_value <= roof_plast_in and roof_plast_in < current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and self.data_well.open_trunk_well is False:
                        roof_add_column_plast = current_bottom
                    elif self.data_well.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_add_column_plast = current_bottom
                    else:
                        roof_add_column_plast = roof_plast_in
                        break
            for plast in plast_all:
                roof_plast_in = dict_perforation[plast]['кровля']
                roof_plast = self.data_well.head_column_additional.get_value
                if self.data_well.head_column_additional.get_value > roof_plast_in and roof_plast_in < current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and self.data_well.open_trunk_well is False:
                        roof_plast = self.data_well.head_column_additional.get_value
                    elif self.data_well.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = self.data_well.shoe_column.get_value
                    else:
                        roof_plast = roof_plast_in
                        break

        return float(roof_plast), float(roof_add_column_plast)

    def template_diam_ek(self):

        diam_internal_ek = self.data_well.column_diameter.get_value - 2 * self.data_well.column_wall_thickness.get_value

        template_first_diam_dict = {
            80: (88, 97),
            89: (97.1, 102),
            92: (102.1, 120),
            112: (120.1, 121.9),
            114: (122, 133),
            118: (144, 221)
        }
        template_second_diam_dict = {
            84: (88, 92),
            90: (92.1, 97),
            94: (97.1, 102),
            102: (102.1, 109),
            106: (109, 115),
            114: (118, 120),
            116: (120.1, 121.9),
            118: (122, 123.9),
            120: (124, 127.9),
            124: (128, 133),
            140: (144, 148),
            144: (148.1, 154),
            152: (154.1, 164),
            164: (166, 176),
            190: (190.6, 203.6),
            210: (215, 221)
        }
        # определение диаметра шаблонов первого и второго
        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_second_diam = diam
        for diam, diam_internal in template_first_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_first_diam = diam
        if 'ПОМ' in str(self.data_well.paker_before["after"]).upper() and '122' in str(
                self.data_well.paker_before["after"]):
            template_second_diam = 126
        return (template_first_diam, template_second_diam)

    def template_diam_additional_ek(self):  # Выбор диаметра шаблонов при наличии в скважине дополнительной колонны

        diam_internal_ek = self.data_well.column_diameter.get_value - 2 * self.data_well.column_wall_thickness.get_value
        diam_internal_ek_addition = float(self.data_well.column_additional_diameter.get_value) - 2 * float(
            self.data_well.column_additional_wall_thickness.get_value)

        template_second_diam_dict = {
            82: (84, 88),
            84: (88, 92),
            90: (92.1, 96),
            94: (96.1, 102),
            102: (102.1, 109),
            106: (109, 115),
            114: (118, 120),
            116: (120.1, 121.9),
            118: (122, 123.9),
            120: (124, 127.9),
            124: (128, 133),
            140: (144, 148),
            144: (148.1, 154),
            152: (154.1, 164),
            164: (166, 176),
            190: (190.6, 203.6),
            210: (215, 221)
        }

        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_second_diam = diam
                break
        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1]:
                # print(diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1], diam_internal[0],diam_internal_ek_addition,diam_internal[1])
                template_first_diam = diam
                break
        if 'ПОМ' in str(self.data_well.paker_before["after"]).upper() and '122' in str(
                self.data_well.paker_before["after"]):
            template_second_diam = 126

        if self.data_well.column_additional_diameter == '114':
            template_first_diam = '94'
        try:
            return (template_first_diam, template_second_diam)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка ', f'Ошибка  определения диаметра шаблонов {e}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addTab(TabPageSoWith(parent), 'Выбор компоновки шаблонов')


class TemplateKrs(WindowUnion):

    def __init__(self, data_well=None, table_widget=None, parent=None):
        super().__init__(data_well)
        if data_well:
            self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.table_widget = table_widget

        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "необходимость Cкреперования"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonadd_string = QPushButton('Добавить интервалы скреперования')
        self.buttonadd_string.clicked.connect(self.add_string)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonadd_string, 3, 1)

        self.current_widget = self.tab_widget.currentWidget()

    def add_row_table(self):
        roof_skm = self.current_widget.roof_skm_line.text()
        sole_skm = self.current_widget.sole_skm_line.text()
        if roof_skm != '':
            roof_skm = int(float(roof_skm))
        if sole_skm != '':
            sole_skm = int(float(sole_skm))
            if sole_skm > self.data_well.skm_depth:
                QMessageBox.information(self, 'Внимание',
                                        f'Глубина СКМ на {self.data_well.skm_depth}м не позволяет скреперовать в '
                                        f'{roof_skm}-{sole_skm}м')
                return
        template_key = self.current_widget.template_combo.currentText()

        if not roof_skm or not sole_skm:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if self.data_well.current_bottom < float(sole_skm):
            QMessageBox.information(self, 'Внимание', f'глубина забоя выше глубины нахождения '
                                                      f'СКМ {self.data_well.skm_depth}')
            return

        if template_key in ['ПСШ СКМ в доп колонне c хвостом',
                            'ПСШ СКМ в доп колонне + открытый ствол', 'ПСШ СКМ в доп колонне без хвоста'] \
                and (roof_skm < self.data_well.head_column_additional.get_value or
                     sole_skm < self.data_well.head_column_additional.get_value):
            QMessageBox.warning(self, 'Ошибка',
                                f'кровля скреперования выше головы '
                                f'хвостовика {self.data_well.head_column_additional.get_value}')
            return

        elif template_key == 'ПСШ Доп колонна СКМ в основной колонне' and \
                (sole_skm > self.data_well.head_column_additional.get_value or
                 roof_skm > self.data_well.head_column_additional.get_value):
            QMessageBox.warning(self, 'Ошибка',
                                f'подошва скреперования ниже головы '
                                f'хвостовика {self.data_well.head_column_additional.get_value}')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(roof_skm)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(f'{sole_skm}'))

        self.tableWidget.setSortingEnabled(False)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        data_list.pause = False
        event.accept()  # Принимаем событие закрытия

    def add_string(self):
        from work_py.advanted_file import skm_interval

        template_key = str(self.current_widget.template_combo.currentText())
        skm_interval = skm_interval(self, template_key)

        if len(skm_interval) == 0:
            QMessageBox.warning(self, 'Ошибка', 'данная компоновка не позволяет скреперовать посадку пакера')
            return

        for roof, sole in skm_interval:
            # Проверяем, что roof и sole еще не присутствуют в таблице
            item_roof = self.find_item_in_table(int(roof))
            item_sole = self.find_item_in_table(int(roof))

            if item_roof is None and item_sole is None:
                rows = self.tableWidget.rowCount()  # Получаем текущее количество строк
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
                self.tableWidget.setSortingEnabled(False)

    def add_work(self):

        template_str = str(self.current_widget.template_str_edit.text())
        self.template_key = str(self.current_widget.template_combo.currentText())
        self.roof_plast = self.current_widget.roof_plast
        self.roof_add_column_plast = self.current_widget.roof_add_column_plast
        self.kot_question_qcombo = self.current_widget.kot_question_qcombo.currentText()
        self.template_depth = self.tab_widget.currentWidget().template_depth
        if self.data_well.column_additional and \
                self.data_well.head_column_additional.get_value < self.data_well.current_bottom:
            self.template_depth_addition = self.tab_widget.currentWidget().template_depth_addition
        if self.kot_question_qcombo == 'Нет':
            mes = QMessageBox.question(self, 'КОТ', 'Согласно мероприятий по сокращению продолжительности '
                                                    'ТКРС от 31.01.2025 п.20 '
                                                    'при первичном СПО ПСШ необходимо использовать в компоновке систему '
                                                    'КОТ за исключением необходимости прямой или '
                                                    'комбинированной промывки, продолжить?')
            if mes == QMessageBox.StandardButton.No:
                return
        if self.kot_question_qcombo == 'Да' and 'открытый' in self.template_key:
            mes = QMessageBox.question(self, 'КОТ', 'Необходимо уточнить необходимость применения системы КОТ в '
                                                    'открытом стволе, продолжить?')
            if mes == QMessageBox.StandardButton.No:
                return

        if self.template_key == 'ПСШ + пакер':
            if self.data_well.gips_in_well:
                QMessageBox.warning(self, 'ПСШ + пакер', 'Нельзя спускать ПСШ в осложненный фонд')
                return

            difference_date_well = self.difference_date_days(self.data_well.date_commissioning.get_value)
            if difference_date_well > 365.25 * 20 and self.data_well.category_h2s == "3":
                mes = QMessageBox.question(self, 'Критерии',
                                           f'Скважина в эксплуатации более {difference_date_well / 365:.0f}лет '
                                           f'Согласно технологических мероприятий по сокращению продолжительности'
                                           f' ТКРС от 31.01.2025г, Объединение ПСШ + пакер не возможно при '
                                           f'эксплуатации скважины с периодом более 20 лет при отсутствии сероводорода '
                                           f'в скважине. \n Продолжить?')
                if mes == QMessageBox.StandardButton.No:
                    return
            if difference_date_well > 365.25 * 10 and self.data_well.category_h2s != "3":
                mes = QMessageBox.question(self, 'Критерии',
                                           f'Скважина в эксплуатации более {difference_date_well / 365:.0f}лет '
                                           f'Согласно технологических мероприятий по сокращению продолжительности'
                                           f' ТКРС от 31.01.2025г, Объединение ПСШ + пакер не возможно'
                                           f' с периодом эксплуатации более 10 лет и наличии сероводород'
                                           f'\n Продолжить?')
                if mes == QMessageBox.StandardButton.No:
                    return
            mes = QMessageBox.question(self, 'ПСШ + пакер',
                                       f'в скважину спускается ПСШ + пакер\n Продолжить?')
            if mes == QMessageBox.StandardButton.No:
                return

        distance_second = int(float(self.current_widget.dictance_template_second_edit.text()))
        distance_first = int(self.current_widget.dictance_template_first_edit.text())
        template_length = int(float(self.current_widget.length_template_second_edit.text()))

        if self.data_well.column_additional:
            self.template_length_addition = int(float(self.current_widget.length_template_first_edit.text()))

        # if self.data_well.skm_depth > self.data_well.perforation_roof:
        #     question = QMessageBox.question(self, 'Проверка глубины СКМ',
        #                                     f'Согласно указания главного инженера СКМ (на глубине '
        #                                     f'{self.data_well.skm_depth}м) не должен '
        #                                     f'спускаться ниже кровли перфорации {self.data_well.perforation_roof}м,'
        #                                     ' если даже интервал перфорации отрайбирован, Каждый спуск ниже кровли '
        #                                     'ИП должен '
        #                                     'быть согласован с заказчиком письменной телефонограммой, продолжить?')
        #     if question == QMessageBox.StandardButton.No:
        #         return
        if self.roof_plast < self.template_depth:
            mes = QMessageBox.question(self, 'Ошибка', f'Глубина спуска шаблона-{self.template_depth}м '
                                                       f'ниже кровли не отрайбированного ИП ({self.roof_plast}м), '
                                                       f'продолжить?')
            if mes == QMessageBox.StandardButton.No:
                return

        if self.data_well.column_additional is False or \
                (self.data_well.column_additional is True and
                 float(self.data_well.head_column_additional.get_value) >= self.data_well.current_bottom):
            template_diameter = int(self.current_widget.template_second_edit.text())
        else:
            template_diameter = int(self.current_widget.template_first_edit.text())
            if self.roof_add_column_plast < self.template_depth_addition:
                mes = QMessageBox.question(self, 'Ошибка',
                                           f'Глубина спуска шаблона-{self.template_depth_addition}м '
                                           f'ниже кровли не отрайбированного ИП'
                                           f' ({self.roof_add_column_plast}м), продолжить?')
                if mes == QMessageBox.StandardButton.No:
                    return

        # print(self.data_well.problem_with_ek_diameter)
        if (template_diameter >= int(self.data_well.problem_with_ek_diameter) - 2
                and self.template_depth > float(self.data_well.problem_with_ek_depth)):
            QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if (template_diameter >= int(self.data_well.problem_with_ek_diameter) - 2
                and self.template_depth > int(self.data_well.problem_with_ek_depth)):
            QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if self.data_well.column_additional is False or \
                self.data_well.column_additional and self.data_well.current_bottom <= \
                self.data_well.head_column_additional.get_value:
            if self.template_depth >= self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return

        else:
            self.data_well.template_length_addition = self.template_length_addition
            if self.template_depth_addition >= self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
            if self.template_depth >= self.data_well.head_column_additional.get_value:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже головы хвостовика')
                return
            if self.template_key == 'ПСШ Доп колонна СКМ в основной колонне' and \
                    self.data_well.skm_depth >= self.data_well.head_column_additional.get_value:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'СКМ спускается ниже головы хвостовика')
                return
        if distance_second < 0 or distance_first < 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Расстояние между шаблонами не корректно')
            return

        skm_tuple = []
        rows = self.tableWidget.rowCount()
        if rows == 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы скреперования')
            return
        for row in range(rows):
            roof_skm = self.tableWidget.item(row, 0)
            sole_skm = self.tableWidget.item(row, 1)
            if roof_skm and sole_skm:
                roof = int(roof_skm.text())
                sole = int(sole_skm.text())
                skm_tuple.append((roof, sole))

        # print(f'интервалы СКМ {self.data_well.skm_interval}')
        skm_list = sorted(skm_tuple, key=lambda x: x[0])
        self.data_well.template_length = template_length



        self.privyazka_question = self.current_widget.privyazka_question_QCombo.currentText()
        if self.privyazka_question == 'Да':
            mes = QMessageBox.question(self, 'Привязка', 'ЗУМПФ меньше 10м. '
                                                         'Нужна привязка, корректно ли?')
            if mes == QMessageBox.StandardButton.No:
                return
        work_template_list = self.template_ek(template_str, template_diameter, skm_list)
        if skm_tuple not in self.data_well.skm_interval:
            self.data_well.skm_interval.extend(skm_list)
        if work_template_list:

            if self.template_depth > self.data_well.template_depth:
                self.data_well.template_depth = self.template_depth
            if self.data_well.column_additional and \
                    self.data_well.head_column_additional.get_value < self.data_well.current_bottom:
                if self.template_depth_addition > self.data_well.template_depth_addition:
                    self.data_well.template_depth_addition = self.template_depth_addition
                    self.data_well.template_length_addition = self.template_length_addition

            self.update_skm_interval(self.data_well.insert_index, skm_list)

            self.populate_row(self.insert_index, work_template_list, self.table_widget)
            data_list.pause = False
            self.close()
            self.close_modal_forcefully()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def template_ek(self, template_str, template_diameter, skm_list):
        from work_py.advanted_file import raid

        skm_interval = raid(skm_list)

        solvent_question = self.current_widget.solvent_question_combo.currentText()
        solvent_volume_edit = self.current_widget.solvent_volume_edit.text()
        if solvent_volume_edit != '':
            solvent_volume_edit = round(float(solvent_volume_edit), 1)

        self.note_question_qcombo = self.current_widget.note_question_qcombo.currentText()
        self.kot_question_qcombo = self.current_widget.kot_question_qcombo.currentText()
        if self.kot_question_qcombo == 'Да':
            mes = QMessageBox.question(self, 'вопрос', 'В компоновке будет использоваться система обратных клапанов,'
                                                       ' продолжить?')
            if mes == QMessageBox.StandardButton.No:
                return

        current_bottom = self.current_widget.current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round(float(current_bottom), 1)

        list_template_ek = [
            [f'СПО  {template_str} на 'f'НКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{self.data_well.nkt_diam}мм  с замером, шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'(при не до хождении до нужного интервала допускается посадка инструмента не более 2т)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom, 1.2)],
            [None, None, f'Нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{self.data_well.fluid_work} до глубины {current_bottom}м.', None, None, None, None,
             None, None, None,
             'Мастер КРС', None],
            [f'Произвести скреперование в интервале {skm_interval}м Допустить низ НКТ до гл. {current_bottom}м',
             None,
             f'Произвести скреперование э/к в интервале {skm_interval}м обратной промывкой и проработкой 5 раз каждого '
             'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
             f'представителя Заказчика. Допустить низ НКТ до гл. {current_bottom}м, шаблон '
             f'до глубины {self.template_depth}м. Составить акт. \n'
             '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
             '2 часа до начала работ). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель УСРСиСТ', round(0.012 * 90 * 1.04 + 1.02 + 0.77, 2)],
            [f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3', None,
             f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
             f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3. При открытом затрубном '
             f'пространстве закачать в '
             f'трубное пространство растворитель в объеме {solvent_volume_edit}м3, продавить в трубное '
             f'пространство тех.жидкостью '
             f'в объеме {round(3 * float(current_bottom) / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [
                f'Промывка скважину уд.весом {self.data_well.fluid_work} в объеме {volume_work(self.data_well) * 1.5:.1f}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work}  при расходе '
                f'жидкости 6-8 л/сек '
                f'в присутствии представителя Заказчика в объеме {volume_work(self.data_well) * 1.5:.1f}м3 ПРИ ПРОМЫВКЕ НЕ '
                f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, '
                f'ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', well_volume_norm(volume_work(self.data_well) * 1.5)],
            [f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч', None,
             f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {template_str} на НКТ{self.data_well.nkt_diam}мм с глубины {current_bottom}м с доливом скважины в '
             f'объеме {round(current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС', lifting_nkt_norm(float(current_bottom), 1.2)]
        ]
        if self.template_key == 'ПСШ + пакер':
            list_template_ek.insert(
                0, [f'СОГЛАСОТЬ РАЗДЕЛЕНИЕ ПСШ+ПАКЕР', None,
                    f'ПРИ НАЛИЧИИ АСПО НА ФНКТ НЕОБХОДИМО СОГЛАСОВАТЬ С С ОТКРС БНД и ПТО ПРОИЗВЕСТИ СПО "ПСШ+ПАКЕР" '
                    f'в 2 СПО. РАЗДЕЛЕНИЕ ТОЛЬКО ПОСЛЕ ПИСЬМЕННОГО СОГЛАСОВАНИЯ и ОФОРМЛЕНИЯ '
                    f'ДОПОЛНИТЕЛЬНОГО ПЛАНА РАБОТ',
                    None, None, None, None, None, None, None,
                    'мастер КРС', None])
            paker_depth = self.current_widget.paker_depth
            paker_list = [
                [f'Посадить пакер на глубине {paker_depth}м', None, f'Посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.5],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
                 OpressovkaEK.testing_pressure(self, paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.83 + 0.58],
                [f'срыв 30мин', None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести '
                 f'ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
            for row in paker_list:
                list_template_ek.insert(-2, row)

        if abs(self.data_well.perforation_sole - current_bottom) > 10:
            list_template_ek.pop(-2)

        if self.kot_question_qcombo == 'Да' and self.data_well.count_template == 0:
            list_template_ek.insert(-1, ['опрессовать тНКТ на 150атм', None,
                                         f'Перед подъемом опрессовать тНКТ на давление 150атм. ',
                                         None, None, None, None, None, None, None,
                                         'Мастер КРС', 0.7])

        notes_list = [
            [None, None,
             f'ПРИМЕЧАНИЕ №1: При не прохождении шаблона d={template_diameter}мм предусмотреть СПО забойного '
             f'двигателя с райбером d={template_diameter + 1}мм, {template_diameter - 1}мм, {template_diameter - 3}мм, '
             f'{template_diameter - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
             f'гл.{self.data_well.current_bottom}м с последующим СПО шаблона {template_diameter}мм на ТНКТ под промывку '
             f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {template_diameter}мм) '
             f'на ТНКТ с гл. {current_bottom}м вести с доливом скважины до устья т/ж '
             f'удел.весом {self.data_well.fluid_work} в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 ',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None],
            [None, None,
             f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с '
             f'долотом {template_diameter};'
             f' {template_diameter - 2}; {template_diameter - 4}мм  фрезера-{template_diameter}мм, '
             f'райбера-{template_diameter + 1}мм и другого оборудования и '
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
             f'текущего забоя обратной циркуляцией. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке '
             f'КОТ-50 произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
             f'на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {self.data_well.fluid_work} в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
            [None, None,
             f'Примечание №5: В случае необходимости по результатам восстановления проходимости '
             f'эксплуатационной колонны '
             f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
             f'проходимость. Подъем компоновки на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {self.data_well.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

        cable_type_text = ''
        angle_text = ''

        if self.privyazka_question == "Да":
            if self.data_well.angle_data:
                if self.data_well.max_angle.get_value > 50:
                    tuple_angle = self.calculate_angle(self.data_well.current_bottom, self.data_well.angle_data)
                    if float(tuple_angle[0]) >= self.data_well.max_angle_depth.get_value:
                        cable_type_text = ' СОГЛАСОВАТЬ ЖЕСТКИЙ КАБЕЛЬ'
                        angle_text = angle_text[1]

            privyazka_nkt = [f'Привязка по ГК и ЛМ по привязому НКТ удостовериться в наличии текущего забоя', None,
                             f'Вызвать геофизическую партию.{cable_type_text} {angle_text}. '
                             f'Заявку оформить за 16 часов сутки через'
                             f' РИТС {data_list.contractor}.'
                             f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                             f' По привязому НКТ удостовериться в наличии '
                             f'текущего забоя с плановым, Нормализовать '
                             f'забой обратной промывкой тех жидкостью '
                             f'уд.весом {self.data_well.fluid_work}   до глубины {self.data_well.current_bottom}м',
                             None, None, None, None, None, None, None, 'Мастер КРС', 4, None]

            list_template_ek.insert(-1, privyazka_nkt)



        if self.data_well.gips_in_well is True and self.data_well.count_template == 0:
            gips = TemplateKrs.pero(self)
            for row in gips[::-1]:
                list_template_ek.insert(0, row)
        if self.note_question_qcombo == "Да":
            list_template_ek = list_template_ek + notes_list
            self.data_well.count_template += 1
        else:
            list_template_ek = list_template_ek

        if solvent_question == 'Нет':
            list_template_ek.pop(3)
        else:
            self.calculate_chemistry('растворитель', solvent_volume_edit)

        self.data_well.current_bottom = current_bottom

        return list_template_ek

    def update_skm_interval(self, index_plan, skm_list):

        row_index = index_plan - self.data_well.count_row_well
        template_ek = json.dumps(
            [self.data_well.template_depth, self.data_well.template_length,
             self.data_well.template_depth_addition,
             self.data_well.template_length_addition])
        for index, data in enumerate(self.data_well.data_list):
            if index == index:
                old_skm_2 = json.loads(self.data_well.data_list[index][12])
                template_ek_2 = self.data_well.data_list[index][11]
            if row_index < index:
                old_skm = json.loads(self.data_well.data_list[index][12])
                old_skm.extend(skm_list)
                self.data_well.data_list[index][12] = json.dumps(old_skm)
                if self.data_well.data_list[index][11] == template_ek_2:
                    self.data_well.data_list[index][11] = template_ek

    def pero(self):
        from work_py.rir import RirWindow
        from work_py.drilling import DrillWindow, TabPageSoDrill

        pero_list = RirWindow.pero_select(self, self.data_well.current_bottom, 'перо + КОТ')
        if self.data_well.gips_in_well:
            gips_str = f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
        else:
            gips_str = ''
        gips_pero_list = [
            [f'Спустить {pero_list}  на тНКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить {pero_list}  на тНКТ{self.data_well.nkt_diam}мм до глубины {self.data_well.current_bottom}м '
             f'с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. '
             f' {gips_str} \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None, f'ПРИ НЕОБХОДИМОСТИ: \n Нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{self.data_well.fluid_work} до глубины {self.data_well.current_bottom}м.',
             None, None, None, None,
             None, None, None,
             'Мастер КРС', None],
            [f'Промывка уд.весом {self.data_well.fluid_work_short} в объеме '
             f'{volume_work(self.data_well) * 1.5:.1f}м3 ',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work} '
             f'при расходе жидкости '
             f'6-8 л/сек в присутствии представителя Заказчика в объеме '
             f'{volume_work(self.data_well) * 1.5:.1f}м3. '
             f'ПРИ ПРОМЫВКЕ НЕ '
             f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
             f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(self.data_well.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение'
             f' текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{self.data_well.nkt_diam}мм с глубины {self.data_well.current_bottom}м с доливом '
             f'скважины в '
             f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом '
             f'{self.data_well.fluid_work}',
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
            template_diameter = TabPageSoDrill.drilling_bit_diam_select(self, self.data_well.current_bottom)

            if self.data_well.column_diameter.get_value > 127 or (self.data_well.column_additional and \
                                                                  self.data_well.column_additional_diameter > 127):
                downhole_motor = 'Д-106'
            else:
                downhole_motor = 'Д-76'
            self.cutter_calibrator = ''

            if self.data_well.dict_pump_shgn["before"] != 0 and self.data_well.paker_before["before"] == 0:
                gips_pero_list = [gips_pero_list[-1]]
                drill_list = DrillWindow.drilling_nkt(self,
                                                      [(self.data_well.current_bottom, 'гипсовых отложений')],
                                                      'долото', template_diameter, downhole_motor)
                for row in drill_list:
                    gips_pero_list.append(row)
            else:
                drill_list = DrillWindow.drilling_nkt(self,
                                                      [(self.data_well.current_bottom, 'гипсовых отложений')],
                                                      'долото', template_diameter, downhole_motor)

                for row in drill_list:
                    gips_pero_list.append(row)

        return gips_pero_list

    def calc_combo_nkt(self, type_nkt, current):
        if self.data_well.column_additional is False or \
                self.data_well.column_additional and \
                self.data_well.current_bottom <= self.data_well.head_column_additional.get_value:
            if type_nkt == 'СБТ':
                nkt_string = ''
            else:
                nkt_string = f' + НКТ{self.data_well.nkt_diam} 20м + репер'
        else:
            if self.data_well.column_additional_diameter.get_value > 110:
                if type_nkt == 'СБТ':
                    nkt_type = {type_nkt: '2" 7/8'}
                else:
                    nkt_type = {type_nkt: '73'}
            else:
                if type_nkt == 'СБТ':
                    nkt_type = {type_nkt: '2" 3/8'}
                elif 110 < self.data_well.column_additional_diameter.get_value < 125:
                    nkt_type = {type_nkt: '73 c обточными муфтами'}
                else:
                    nkt_type = {type_nkt: '60'}

            if type_nkt == 'СБТ':
                nkt_string = f'{type_nkt}{nkt_type[type_nkt]}  ' \
                             f'{round(self.data_well.head_column_additional.get_value - current, 0)}м '
            else:
                nkt_string = f'{type_nkt}{nkt_type[type_nkt]} 20м + репер + {type_nkt}{nkt_type[type_nkt]} ' \
                             f'{round(self.data_well.head_column_additional.get_value - current - 20, 0)}м '
        return nkt_string


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = TemplateKrs()
    window.show()
    app.exec_()
