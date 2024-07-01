import math
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTabWidget, QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, \
    QGridLayout, QPushButton, QBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QApplication

import well_data
from PyQt5.QtCore import Qt

from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.alone_oreration import kot_work
from PyQt5.QtGui import QDoubleValidator
from main import MyWindow


class TabPage_SO_with(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        validator = QDoubleValidator(0.0, 80000.0, 2)

        self.template_labelType = QLabel("Вид компоновки ПСШ", self)
        self.template_Combo = QComboBox(self)

        self.template_Combo.currentTextChanged.connect(self.update_template_edit)

        self.template_str_Label = QLabel("строчка с шаблонами", self)
        self.template_str_Edit = QLineEdit(self)

        self.skm_teml_str_Label = QLabel("глубины спуска шаблонов", self)
        self.skm_teml_str_Edit = QLineEdit(self)

        self.template_first_Label = QLabel("диаметр первого шаблона", self)
        self.template_first_Edit = QLineEdit(self)
        self.template_first_Edit.setValidator(validator)

        self.lenght_template_first_Label = QLabel("длина первого шаблона", self)
        self.lenght_template_first_Edit = QLineEdit(self)
        self.lenght_template_first_Edit.setValidator(validator)

        self.dictance_template_first_Label = QLabel("расстояние", self)
        self.dictance_template_first_Edit = QLineEdit(self)
        self.dictance_template_first_Edit.setValidator(validator)



        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        if well_data.current_bottom - well_data.perforation_sole <= 10 and well_data.open_trunk_well is False:
            self.privyazka_question_QCombo.setCurrentIndex(1)

        self.note_Label = QLabel("Нужно ли добавлять примечание", self)
        self.note_question_QCombo = QComboBox(self)
        self.note_question_QCombo.addItems(['Нет', 'Да'])

        self.solvent_Label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(validator)
        self.solvent_volume_edit.setText("2")

        self.solvent_question_Label = QLabel("необходимость растворителя", self)
        self.solvent_question_QCombo = QComboBox(self)
        self.solvent_question_QCombo.addItems(['Нет', 'Да'])

        if well_data.count_template == 0:
            self.note_question_QCombo.setCurrentIndex(1)
            self.solvent_question_QCombo.setCurrentIndex(1)

        self.skm_Label = QLabel("диаметр СКМ", self)
        self.skm_Edit = QLineEdit(self)
        self.skm_Edit.setValidator(validator)

        self.dictance_template_second_Label = QLabel("расстояние", self)
        self.dictance_template_second_Edit = QLineEdit(self)
        self.dictance_template_second_Edit.setValidator(validator)

        self.template_second_Label = QLabel("диаметр второго шаблона", self)
        self.template_second_Edit = QLineEdit(self)
        self.template_second_Edit.setValidator(validator)

        self.lenght_template_second_Label = QLabel("длина второго шаблона", self)
        self.lenght_template_second_Edit = QLineEdit(self)
        self.lenght_template_second_Edit.setValidator(validator)

        self.dictance_three_Label = QLabel("третья", self)
        self.dictance_three_Edit = QLineEdit(self)
        self.dictance_three_Edit.setValidator(validator)

        self.roof_skm_label = QLabel("Кровля скреперования", self)
        self.roof_skm_line = QLineEdit(self)
        self.roof_skm_line.setValidator(validator)
        self.roof_skm_line.setClearButtonEnabled(True)

        self.sole_skm_label = QLabel("Кровля скреперования", self)
        self.sole_skm_line = QLineEdit(self)
        self.sole_skm_line.setClearButtonEnabled(True)
        self.sole_skm_line.setValidator(validator)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')


        self.grid = QGridLayout(self)
        if well_data.column_additional is False or \
                (well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value):
            self.template_select_list = ['ПСШ ЭК', 'ПСШ открытый ствол', 'ПСШ без хвоста']

            self.template_Combo.addItems(self.template_select_list)

            template_key = self.definition_pssh()
            # print(self.template_select_list, template_key)
            self.template_Combo.setCurrentIndex(self.template_select_list.index(template_key))


            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_Combo, 2, 2, 2, 8)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)
            self.grid.addWidget(self.skm_Label, 4, 5)
            self.grid.addWidget(self.skm_Edit, 5, 5)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 6)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 6)
            self.grid.addWidget(self.template_second_Label, 4, 7)
            self.grid.addWidget(self.template_second_Edit, 5, 7)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 8)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 8)
            self.grid.addWidget(self.dictance_three_Label, 4, 9)
            self.grid.addWidget(self.dictance_three_Edit, 5, 9)

        else:
            self.template_select_list = ['ПСШ Доп колонна СКМ в основной колонне', 'ПСШ СКМ в доп колонне c хвостом',
                                         'ПСШ СКМ в доп колонне + открытый ствол', 'ПСШ СКМ в доп колонне без хвоста']
            self.template_Combo.addItems(self.template_select_list)
            template_key = self.definition_pssh()
            # print(template_key)
            self.template_Combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_Combo, 2, 2, 2, 8)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)

            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)

            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.skm_Label, 4, 6)
            self.grid.addWidget(self.skm_Edit, 5, 6)
            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)
            self.grid.addWidget(self.template_second_Label, 4, 8)
            self.grid.addWidget(self.template_second_Edit, 5, 8)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)

        self.grid.addWidget(self.current_bottom_label, 8, 3)
        self.grid.addWidget(self.current_bottom_edit, 9, 3)

        self.grid.addWidget(self.solvent_question_Label, 8, 4)
        self.grid.addWidget(self.solvent_question_QCombo, 9, 4)

        self.grid.addWidget(self.solvent_Label, 8, 5)
        self.grid.addWidget(self.solvent_volume_edit, 9, 5)

        self.grid.addWidget(self.privyazka_question_Label, 8, 6)
        self.grid.addWidget(self.privyazka_question_QCombo, 9, 6)

        self.grid.addWidget(self.note_Label, 8, 7)
        self.grid.addWidget(self.note_question_QCombo, 9, 7)

        self.grid.addWidget(self.template_str_Label, 11, 1, 1, 8)
        self.grid.addWidget(self.template_str_Edit, 12, 1, 1, 8)

        self.grid.addWidget(self.skm_teml_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_Edit, 14, 1, 1, 8)

        if well_data.column_additional is False or (well_data.column_additional and
                                                    well_data.head_column_additional._value >= well_data.current_bottom):
            first_template, template_second = self.template_diam_ek()
        else:
            first_template, template_second = self.template_diam_additional_ek()

        self.grid.addWidget(self.roof_skm_label, 35, 2, 1, 3)
        self.grid.addWidget(self.roof_skm_line, 36, 2, 1, 3)

        self.grid.addWidget(self.sole_skm_label, 35, 5, 1, 3)
        self.grid.addWidget(self.sole_skm_line, 36, 5, 1, 3)

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))

        self.lenght_template_first_Edit.setText(str(4))

        self.dictance_template_first_Edit.textChanged.connect(self.update_template)
        self.template_first_Edit.textChanged.connect(self.update_template)
        self.lenght_template_first_Edit.textChanged.connect(self.update_template)
        self.dictance_template_second_Edit.textChanged.connect(self.update_template)
        self.skm_Edit.textChanged.connect(self.update_template)
        self.dictance_three_Edit.textChanged.connect(self.update_template)
        self.template_second_Edit.textChanged.connect(self.update_template)
        self.lenght_template_second_Edit.textChanged.connect(self.update_template)
        self.current_bottom_edit.textChanged.connect(self.update_template)
        self.current_bottom_edit.textChanged.connect(self.update_template)



    def definition_pssh(self):
        # print(well_data.plast_work)
        #
        # print(list(well_data.dict_perforation.keys()))
        # print(well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work)

        if well_data.column_additional is False and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is False or \
                (well_data.column_additional is True and well_data.open_trunk_well is False and all(
            [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is False and \
                 well_data.current_bottom <= well_data.head_column_additional._value):
            template_key = 'ПСШ ЭК'

        elif well_data.column_additional is False and well_data.open_trunk_well is True or \
                ( well_data.column_additional is True and well_data.open_trunk_well is True and \
                  well_data.current_bottom <= well_data.head_column_additional._value and well_data.open_trunk_well):
            template_key = 'ПСШ открытый ствол'

        elif well_data.column_additional is False and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is True or \
                (well_data.column_additional is True and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is True and \
                 well_data.current_bottom <= well_data.head_column_additional._value):
            template_key = 'ПСШ без хвоста'

        elif well_data.column_additional is True and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is False:
            template_key = 'ПСШ СКМ в доп колонне c хвостом'

        elif well_data.column_additional is True and well_data.open_trunk_well is True:
            template_key = 'ПСШ СКМ в доп колонне + открытый ствол'

        elif well_data.column_additional is True and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in
                 well_data.plast_work]) is True and well_data.open_trunk_well is False:
            template_key = 'ПСШ СКМ в доп колонне без хвоста'
        return template_key


    def update_template(self):
        if self.current_bottom_edit.text() != '':
            well_data.current_bottom = round(float(self.current_bottom_edit.text()), 1)

        if self.template_first_Edit.text() != '':
                first_template = self.template_first_Edit.text()
        if self.lenght_template_first_Edit.text() != '':
            lenght_template_first = self.lenght_template_first_Edit.text()
        if self.template_second_Edit.text() != '':
            template_second = self.template_second_Edit.text()
        if self.lenght_template_second_Edit.text() != '':
            lenght_template_second = self.lenght_template_second_Edit.text()
        if self.skm_Edit.text() != '':
            skm = self.skm_Edit.text()
        if self.dictance_template_first_Edit.text() != '':
            dictance_template_first = int(float(self.dictance_template_first_Edit.text()))
        else:
            dictance_template_first = ''
        if self.dictance_template_second_Edit.text() != '':
            dictance_template_second = int(float(self.dictance_template_second_Edit.text()))
        else:
            dictance_template_second = ''
        if self.dictance_three_Edit.text() != '':
            dictance_three = int(float(self.dictance_three_Edit.text()))
        else:
            dictance_three = ''
        nkt_diam = well_data.nkt_diam

        if well_data.column_additional or \
                (well_data.head_column_additional._value >= well_data.current_bottom and well_data.column_additional is False):
            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        if first_template != '' and lenght_template_first != '' and \
                template_second != '' and lenght_template_second != '' and \
                skm != '' and dictance_template_first != '' and \
                dictance_template_second != '' and first_template != '':

            if self.template_Combo.currentText() == 'ПСШ ЭК':
                # if dictance_template_second != '':
                self.dictance_three_Edit.setParent(None)
                self.dictance_three_Label.setParent(None)

                template_str = f'перо + шаблон-{int(first_template)}мм L-{int(lenght_template_first)}м + НКТ{nkt_diam}м ' \
                               f'{int(dictance_template_first)}м + СКМ-{skm} +  ' \
                               f'НКТ{nkt_diam}м {int(dictance_template_second)}м + шаблон-{template_second}мм ' \
                               f'L-{lenght_template_second}м '

                well_data.template_depth = int(well_data.current_bottom - int(dictance_template_first) -
                                               int(lenght_template_first)) - int(dictance_template_second)
                well_data.skm_depth = well_data.template_depth + dictance_template_second
                skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ без хвоста':
                # if dictance_template_second != None:
                template_str = f'перо + СКМ-{skm} + {dictance_template_second}м ' \
                               f'НКТ{nkt_diam}м + шаблон-{template_second}мм L-{lenght_template_second}м '
                well_data.template_depth = math.ceil(well_data.current_bottom - int(dictance_template_second))
                well_data.skm_depth = well_data.template_depth + dictance_template_second
                skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ открытый ствол':
                # if dictance_template_second != None:
                self.template_first_Edit.setText('фильтр направление')
                template_str = f'фильтр-направление L {lenght_template_first}м + НКТ{nkt_diam}м {dictance_template_first}м ' \
                               f'+ СКМ-{skm} + {dictance_template_second}м НКТ{nkt_diam}м + ' \
                               f'шаблон-{template_second}мм L-{lenght_template_second}м '
                well_data.template_depth = int(well_data.current_bottom - int(dictance_template_first) -
                                               int(dictance_template_second) - int(lenght_template_first))
                well_data.skm_depth = well_data.template_depth + dictance_template_second
                skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ Доп колонна СКМ в основной колонне':
                if dictance_template_second != '' and  dictance_template_first != '' and dictance_three != '':
                    template_str = f'обточная муфта  + ' \
                                   f'НКТ{nkt_pod}  + {dictance_template_first}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_template_second}м + НКТ{nkt_diam} {dictance_three}м + ' \
                                   f'СКМ-{skm} + шаблон-{template_second}мм L-{lenght_template_second}м '

                    well_data.template_depth_addition = well_data.current_bottom - int(dictance_template_first)

                    well_data.template_depth = well_data.current_bottom - int(dictance_template_first) - \
                                               int(dictance_template_second) - int(dictance_three)
                    well_data.skm_depth = well_data.template_depth + dictance_three
                    # template_str = template_SKM_DP_EK
                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне c хвостом':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                    lenght_template_first != '' and first_template != '' and template_second != '' \
                        and lenght_template_second != '':
                    template_str = f'обточная муфта + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_three}м + ' \
                                   f'шаблон-{template_second}мм L-{lenght_template_second}м '



                    well_data.template_depth = well_data.current_bottom - int(dictance_template_first) - \
                                               int(dictance_template_second) - int(dictance_three) - \
                                               int(lenght_template_first)
                    well_data.template_depth_addition = well_data.current_bottom - int(dictance_template_first) - \
                                                        int(dictance_template_second)
                    well_data.skm_depth = well_data.template_depth_addition + int(dictance_template_second)

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне без хвоста':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                        lenght_template_first != '' and first_template != '' and template_second != '' \
                        and lenght_template_second != '':

                    template_str = f'обточная муфта + СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second} + ' \
                                   f'шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '
                    well_data.template_depth_addition = well_data.current_bottom - int(dictance_template_second)

                    well_data.template_depth = well_data.current_bottom - int(dictance_template_second) - \
                                               int(dictance_three) - int(lenght_template_first)
                    well_data.skm_depth = well_data.template_depth + int(dictance_three)

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне + открытый ствол':
                if dictance_three != '' and dictance_template_second != '' and dictance_template_first != '' and \
                        lenght_template_first != '' and first_template != '' and template_second != '' \
                        and lenght_template_second != '':
                    template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м' \
                                   f' + НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '
                    # if dictance_three and dictance_template_second and dictance_template_first and lenght_template_first:
                    well_data.template_depth_addition = well_data.current_bottom - int(dictance_template_first) - \
                                                        int(dictance_template_second)

                    well_data.template_depth = well_data.current_bottom - int(dictance_template_first) - \
                                               int(dictance_template_second) - int(dictance_three) - \
                                               int(lenght_template_first)
                    well_data.skm_depth = well_data.template_depth_addition + int(dictance_template_second)

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'
            if dictance_template_second != '' and dictance_template_first != '' and \
                    lenght_template_first != '' and first_template != '' and template_second != '' \
                    and lenght_template_second != '':

                self.template_str_Edit.setText(template_str)
                self.skm_teml_str_Edit.setText(skm_teml_str)

    def update_template_edit(self, index):

        nkt_diam = well_data.nkt_diam
        # print(well_data.column_additional, well_data.head_column_additional._value, well_data.current_bottom)
        if well_data.column_additional is False or (well_data.column_additional and
                                                    well_data.head_column_additional._value >= well_data.current_bottom):
            first_template, template_second = self.template_diam_ek()
            # print(f'диаметры шаблонов {first_template, template_second}')
        else:
            first_template, template_second = self.template_diam_additional_ek()
            # print(f'диаметры шаблонов {first_template, template_second}')

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))
        self.skm_Edit.setText(str(well_data.column_diametr._value))
        self.dictance_template_second_Edit.setText(str(10))

        roof_plast, roof_add_column_plast = self.definition_roof_not_raiding()

        # print(f'кровля отрайби интерва {roof_plast, roof_add_column_plast}')
        dictance_template_first = int(well_data.current_bottom - roof_plast + 5)
        self.dictance_template_first_Edit.setText(str(dictance_template_first))

        lenght_template_first, lenght_template_second = self.definition_ECN_true(well_data.dict_pump_ECN_h["posle"])
        self.lenght_template_first_Edit.setText(lenght_template_first)
        self.lenght_template_second_Edit.setText(str(lenght_template_second))

        first_template = self.template_first_Edit.text()
        template_second = int(self.template_second_Edit.text())
        lenght_template_first = int(self.lenght_template_first_Edit.text())

        lenght_template_second = int(self.lenght_template_second_Edit.text())
        dictance_template_second = int(self.dictance_template_second_Edit.text())
        skm = self.skm_Edit.text()

        self.template_first_Label.setParent(None)
        self.template_first_Edit.setParent(None)
        self.lenght_template_first_Label.setParent(None)
        self.lenght_template_first_Edit.setParent(None)
        self.dictance_three_Edit.setParent(None)
        self.dictance_three_Edit.setParent(None)
        self.dictance_template_first_Label.setParent(None)
        self.dictance_template_first_Edit.setParent(None)
        self.dictance_three_Label.setParent(None)
        self.dictance_three_Edit.setParent(None)

        if well_data.column_additional or \
                (well_data.head_column_additional._value >= well_data.current_bottom and \
                 well_data.column_additional is False):
            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        if index == 'ПСШ ЭК':
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)

            template_str = f'перо + шаблон-{first_template}мм L-{lenght_template_first}м + НКТ{nkt_diam}м ' \
                           f'{dictance_template_first}м + СКМ-{skm} +  ' \
                           f'НКТ{nkt_diam}м {dictance_template_second}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '

            # print(f'строка шаблона {template_str}')
            well_data.template_depth = int(well_data.current_bottom - int(dictance_template_first) -
                                           int(lenght_template_first)) - int(dictance_template_second)
            well_data.skm_depth = well_data.template_depth + dictance_template_second
            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'



        elif index == 'ПСШ без хвоста':
            template_str = f'перо + СКМ-{skm} + {dictance_template_second}м ' \
                           f'НКТ{nkt_diam}м + шаблон-{template_second}мм L-{lenght_template_second}м '
            well_data.template_depth = math.ceil(well_data.current_bottom - int(dictance_template_second))
            well_data.skm_depth = well_data.current_bottom
            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'ПСШ открытый ствол':

            # self.grid.addWidget(self.template_first_Label, 4, 2)
            # self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)

            self.template_first_Edit.setText('фильтр направление')
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            self.dictance_template_second_Edit.setText(str(10))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'фильтр-направление + НКТ{nkt_diam}м {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + {dictance_template_second}м НКТ{nkt_diam}м + ' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '
            well_data.template_depth = int(
                well_data.current_bottom - dictance_template_first - dictance_template_second)
            well_data.skm_depth = well_data.template_depth + dictance_template_second

            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'ПСШ Доп колонна СКМ в основной колонне':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)
            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)

            self.lenght_template_first_Edit.setText(str(lenght_template_first))
            lenght_template_first = int(self.lenght_template_first_Edit.text())
            dictance_template_first1 = int(well_data.current_bottom - roof_add_column_plast + 5)

            # print(f'дистанци {dictance_template_first }')
            self.skm_Edit.setText(str(well_data.column_diametr._value))
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_template_second = int(well_data.current_bottom - dictance_template_first1 - \
                               lenght_template_first - well_data.head_column_additional._value +5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))

            self.lenght_template_second_Edit.setText(str(lenght_template_second))

            dictance_template_three = round(well_data.current_bottom - dictance_template_first - \
                                       int(dictance_template_second) - lenght_template_first - roof_plast + 10, 0)
            self.dictance_three_Edit.setText(str(dictance_template_three))


            template_str = f'обточная муфта  + ' \
                           f'НКТ{nkt_pod}  + {dictance_template_first}м + шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_template_second}м +' \
                           f'СКМ-{skm} + НКТ{nkt_diam} {dictance_template_three}м + шаблон-{template_second}мм L-{lenght_template_second}м '

            well_data.template_depth_addition = int(well_data.current_bottom - dictance_template_first)
            well_data.template_depth = int(well_data.current_bottom - dictance_template_first - lenght_template_first -
                                           dictance_template_second - dictance_template_three)
            well_data.skm_depth = well_data.template_depth + dictance_template_three
            # template_str = template_SKM_DP_EK
            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


        elif index == 'ПСШ СКМ в доп колонне c хвостом':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)
            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)

            skm = str(well_data.column_additional_diametr._value)
            self.skm_Edit.setText(skm)

            dictance_template_first = int(well_data.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))

            dictance_template_three = round((well_data.current_bottom - dictance_template_first - \
                                      int(dictance_template_second) - lenght_template_first) - roof_plast + 10, 0)

            self.dictance_three_Edit.setText(str(dictance_template_three))

            template_str = f'обточная муфта + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                           f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_template_three}м + ' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '

            well_data.template_depth = math.ceil(well_data.current_bottom -
                                                 dictance_template_first - dictance_template_second -
                                                 lenght_template_first - dictance_template_three)

            well_data.template_depth_addition = math.ceil(well_data.current_bottom - dictance_template_first -
                                                          dictance_template_second)

            well_data.skm_depth = well_data.template_depth_addition + dictance_template_second

            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'ПСШ СКМ в доп колонне без хвоста':

            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)

            dictance_template_first = 0
            self.dictance_template_first_Edit.setText(str(dictance_template_first))

            skm = str(well_data.column_additional_diametr._value)
            self.skm_Edit.setText(skm)
            dictance_template_second = 10
            self.dictance_template_second_Edit.setText(str(dictance_template_second))

            dictance_template_three = round((well_data.current_bottom - dictance_template_first - \
                                       int(dictance_template_second) - lenght_template_first) - roof_plast + 10, 0)

            self.dictance_three_Edit.setText(str(dictance_template_three))


            template_str = f'обточная муфта + СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second} + ' \
                           f'шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_template_three}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '

            well_data.template_depth = math.ceil(well_data.current_bottom - dictance_template_second -
                                                 lenght_template_first - dictance_template_three)
            well_data.template_depth_addition = math.ceil(well_data.current_bottom - dictance_template_second)
            well_data.skm_depth = well_data.template_depth_addition + dictance_template_second
            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'



        elif index == 'ПСШ СКМ в доп колонне + открытый ствол':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)
            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)

            skm = str(well_data.column_additional_diametr._value)
            self.skm_Edit.setText(skm)

            dictance_template_first = int(well_data.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))

            dictance_template_three = round((well_data.current_bottom - dictance_template_first - \
                                       int(dictance_template_second) - lenght_template_first) - roof_plast + 10, 0)
            self.dictance_three_Edit.setText(str(dictance_template_three))


            template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                           f'L-{lenght_template_first}м' \
                           f' + НКТ{nkt_pod} {dictance_template_three}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '

            well_data.template_depth = math.ceil(well_data.current_bottom -
                                                 dictance_template_first - dictance_template_second -
                                                 lenght_template_first - dictance_template_three)
            well_data.template_depth_addition = math.ceil(well_data.current_bottom -
                                                          dictance_template_first - dictance_template_second)
            well_data.skm_depth = well_data.template_depth_addition + dictance_template_second

            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        self.template_str_Edit.setText(template_str)
        self.skm_teml_str_Edit.setText(skm_teml_str)

        if 'ПОМ' in str(well_data.paker_do["posle"]).upper() and '122' in str(well_data.paker_do["posle"]):
            self.template_second_Edit.setText(str(126))

    def definition_ECN_true(self, depth_ecn):

        if well_data.column_additional is False and well_data.dict_pump_ECN["posle"] != 0 and \
                well_data.column_diametr._value > 168:
            return "4", "4"

        elif well_data.column_additional is False and well_data.dict_pump_ECN["posle"] != 0:
            return "4", "30"
        elif well_data.column_additional is True and well_data.dict_pump_ECN["posle"] != 0 \
                and well_data.column_additional_diametr._value < 170:
            if well_data.dict_pump_ECN["posle"] != 0 and float(depth_ecn) < well_data.head_column_additional._value and \
                    well_data.column_diametr._value > 168:
                return "4", "4"
            elif well_data.dict_pump_ECN["posle"] != 0 and float(depth_ecn) < well_data.head_column_additional._value:
                return "4", "30"

            elif well_data.dict_pump_ECN["posle"] != 0 and float(depth_ecn) >= well_data.head_column_additional._value:

                return "30", "4"
        else:
            return "4", "4"

            # print(f' ЭЦН длина" {well_data.lift_ecn_can, well_data.lift_ecn_can_addition, "ЭЦН" in str(well_data.dict_pump["posle"][0]).upper()}')

    def definition_roof_not_raiding(self):

        dict_perforation = well_data.dict_perforation
        plast_all = list(dict_perforation.keys())
        roof_plast = well_data.current_bottom
        roof_add_column_plast = well_data.head_column_additional._value
        if well_data.column_additional is False or (
                well_data.column_additional and well_data.head_column_additional._value >= well_data.current_bottom):
            for plast in plast_all:
                roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))

                if roof_plast > roof and roof < well_data.current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and well_data.open_trunk_well is False:
                        roof_add_column_plast = roof_plast
                    elif well_data.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = well_data.shoe_column._value
                        roof_add_column_plast = well_data.current_bottom

                    else:
                        roof_plast = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
                        roof_add_column_plast = roof


                else:
                    roof_add_column_plast = roof_plast


        elif well_data.column_additional:
            for plast in plast_all:
                roof_plast_in = dict_perforation[plast]['кровля']

                if well_data.head_column_additional._value <= roof_plast_in and roof_plast_in < well_data.current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and well_data.open_trunk_well is False:
                        roof_add_column_plast = well_data.current_bottom
                    elif well_data.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_add_column_plast = well_data.current_bottom
                    else:
                        roof_add_column_plast = roof_plast_in
                        break
            for plast in plast_all:
                roof_plast_in = dict_perforation[plast]['кровля']
                roof_plast = well_data.head_column_additional._value
                if well_data.head_column_additional._value > roof_plast_in and roof_plast_in < well_data.current_bottom:
                    if dict_perforation[plast]['отрайбировано'] and well_data.open_trunk_well is False:
                        roof_plast = well_data.head_column_additional._value
                    elif well_data.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = well_data.shoe_column._value
                    else:
                        roof_plast = roof_plast_in
                        break

        return roof_plast, roof_add_column_plast

    def template_diam_ek(self):

        diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value

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
        # определение диаметра  шаблонов первого и второго
        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_second_diam = diam
        for diam, diam_internal in template_first_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_first_diam = diam
        if 'ПОМ' in str(well_data.paker_do["posle"]).upper() and '122' in str(well_data.paker_do["posle"]):
            template_second_diam = 126
        return (template_first_diam, template_second_diam)

    def template_diam_additional_ek(self):  # Выбор диаметра шаблонов при наличии в скважине дополнительной колонны

        diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
        diam_internal_ek_addition = float(well_data.column_additional_diametr._value) - 2 * float(
            well_data.column_additional_wall_thickness._value)

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

        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
                template_second_diam = diam
        for diam, diam_internal in template_second_diam_dict.items():
            if diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1]:
                # print(diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1], diam_internal[0],diam_internal_ek_addition,diam_internal[1])
                template_first_diam = diam
        if 'ПОМ' in str(well_data.paker_do["posle"]).upper() and '122' in str(well_data.paker_do["posle"]):
            template_second_diam = 126
        return (template_first_diam, template_second_diam)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_with(self), 'Выбор компоновки шаблонов')


class TemplateKrs(QMainWindow):

    def __init__(self, ins_ind, table_widget, parent=None):
        super().__init__()
        # print(f'дочерний класс TemplateKRS')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget

        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "необходимость Cкреперования"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddString = QPushButton('Добавить интервалы скреперования')
        self.buttonAddString.clicked.connect(self.addString)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)


    def addRowTable(self):
        roof_skm = self.tabWidget.currentWidget().roof_skm_line.text()
        sole_skm = self.tabWidget.currentWidget().sole_skm_line.text()
        if roof_skm != '':
            roof_skm = int(float(roof_skm))
        if sole_skm != '':
            roof_skm = int(float(sole_skm))
        template_key = self.tabWidget.currentWidget().template_Combo.currentText()

        if not roof_skm or not sole_skm:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if well_data.current_bottom < float(sole_skm):
            msg = QMessageBox.information(self, 'Внимание', f'глубина забоя выше глубины нахождения '
                                                            f'СКМ {well_data.skm_depth}')
            return

        if template_key in ['ПСШ СКМ в доп колонне c хвостом',
                            'ПСШ СКМ в доп колонне + открытый ствол', 'ПСШ СКМ в доп колонне без хвоста'] \
                and (roof_skm < well_data.head_column_additional._value or
                     sole_skm < well_data.head_column_additional._value):
            mes = QMessageBox.warning(self, 'Ошибка',
                                      f'кровля скреперования выше головы '
                                      f'хвостовика {well_data.head_column_additional._value}')
            return

        elif template_key == 'ПСШ Доп колонна СКМ в основной колонне' and \
                (sole_skm > well_data.head_column_additional._value or
                 roof_skm >well_data.head_column_additional._value):
            mes = QMessageBox.warning(self, 'Ошибка',
                                      f'подошва скреперования ниже головы '
                                      f'хвостовика {well_data.head_column_additional._value}')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(roof_skm)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(f'{sole_skm}'))

        self.tableWidget.setSortingEnabled(False)

    def addString(self):
        from .advanted_file import skm_interval

        template_key = str(self.tabWidget.currentWidget().template_Combo.currentText())
        skm_interval = skm_interval(self, template_key)

        if len(skm_interval) == 0:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Интервалы перфорации не отрайбированы,'
                                      'данная компоновка не позволяет скреперовать посадку пакера')
            return
        rows = self.tableWidget.rowCount()

        for roof, sole in skm_interval:
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
            self.tableWidget.setSortingEnabled(False)
    def add_work(self):

        template_str = str(self.tabWidget.currentWidget().template_str_Edit.text())
        template_key = str(self.tabWidget.currentWidget().template_Combo.currentText())
        distance_second = int(float(self.tabWidget.currentWidget().dictance_template_second_Edit.text()))
        distance_first = int(self.tabWidget.currentWidget().dictance_template_first_Edit.text())


        if well_data.column_additional is False or (
                well_data.column_additional is True and float(
            well_data.head_column_additional._value) >= well_data.current_bottom):
            template_diametr = int(self.tabWidget.currentWidget().template_second_Edit.text())
        else:
            template_diametr = int(self.tabWidget.currentWidget().template_first_Edit.text())
        # print(well_data.problemWithEk_diametr)
        if (template_diametr >= int(well_data.problemWithEk_diametr) - 2
                and well_data.template_depth > float(well_data.problemWithEk_depth)):
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if (template_diametr >= int(well_data.problemWithEk_diametr) - 2
            and well_data.template_depth > int(well_data.problemWithEk_depth)):
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if well_data.column_additional is False or \
                well_data.column_additional and well_data.current_bottom <= well_data.head_column_additional._value:
            if well_data.template_depth >= well_data.current_bottom:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
        else:
            if well_data.template_depth_addition >= well_data.current_bottom:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
            if well_data.template_depth >= well_data.head_column_additional._value:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже головы хвостовика')
                return
            if template_key == 'ПСШ Доп колонна СКМ в основной колонне' and\
                    well_data.skm_depth >= well_data.head_column_additional._value:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'СКМ спускается ниже головы хвостовика')
                return
        if distance_second < 0 or distance_first < 0:
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Расстояние между шаблонами не корректно')
            return

        skm_tuple = []
        rows = self.tableWidget.rowCount()
        if rows == 0:
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы скреперования')
            return
        for row in range(rows):
            roof_skm = self.tableWidget.item(row, 0)
            sole_skm = self.tableWidget.item(row, 1)
            if roof_skm and sole_skm:
                roof = int(roof_skm.text())
                sole = int(sole_skm.text())
                skm_tuple.append((roof, sole))

        well_data.skm_interval.extend(skm_tuple)
        # print(f'интервалы СКМ {well_data.skm_interval}')
        skm_list = sorted(skm_tuple, key=lambda x: x[0])

        work_template_list = self.template_ek(template_str, template_diametr, skm_list)

        MyWindow.populate_row(self, self.ins_ind, work_template_list, self.table_widget)
        well_data.pause = False
        self.close()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def well_volume(self):
        if not well_data.column_additional:

            volume_well = 3.14 * (
                        well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000000 * (
                              well_data.current_bottom)
            return volume_well
        else:
            volume_well = (3.14 * (
                    well_data.column_additional_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                   well_data.current_bottom - float(
                               well_data.head_column_additional._value)) / 1000) + (
                                  3.14 * (
                                  well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                      well_data.head_column_additional._value) / 1000)
            return volume_well

    def template_ek(self, template_str, template_diametr, skm_list):

        from .advanted_file import raid
        # print(f'внут {skm_list}')
        skm_interval = raid(skm_list)

        solvent_question = self.tabWidget.currentWidget().solvent_question_QCombo.currentText()
        solvent_volume_edit = self.tabWidget.currentWidget().solvent_volume_edit.text()
        if solvent_volume_edit != '':
            solvent_volume_edit = round(float(solvent_volume_edit), 1)
        privyazka_question = self.tabWidget.currentWidget().privyazka_question_QCombo.currentText()
        note_question_QCombo = self.tabWidget.currentWidget().note_question_QCombo.currentText()

        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round(float(current_bottom), 1)

        list_template_ek = [
            [f'СПО  {template_str} на 'f'НКТ{well_data.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{well_data.nkt_diam}мм  с замером, шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom, 1.2)],
            [f'Произвести скреперование в интервале {skm_interval}м Допустить низ НКТ до гл. {current_bottom}м',
            None,
            f'Произвести скреперование э/к в интервале {skm_interval}м обратной промывкой и проработкой 5 раз каждого '
            'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
            f'представителя Заказчика. Допустить низ НКТ до гл. {current_bottom}м, шаблон '
            f'до глубины {well_data.template_depth}м. Составить акт. \n'
            '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ). ',
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
            [f'Промывка скважину уд.весом {well_data.fluid_work} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
            None,
            f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  при расходе '
            f'жидкости 6-8 л/сек '
            f'в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ '
            f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {well_data.max_admissible_pressure._value}АТМ, '
            f'ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
            None, None, None, None, None, None, None,
            'Мастер КРС, представитель ЦДНГ', well_volume_norm(TemplateKrs.well_volume(self) * 1.5)],
            [None, None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{well_data.fluid_work} до глубины {current_bottom}м.', None, None, None, None,
             None, None, None,
             'Мастер КРС', None],
            [f'Приподнять до глубины {round(float(current_bottom)- 20, 1)}м. Тех отстой 2ч', None,
             f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {template_str} на НКТ{well_data.nkt_diam}мм с глубины {current_bottom}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(float(current_bottom), 1.2)]
        ]

        notes_list = [
            [None, None,
             f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={template_diametr}мм предусмотреть СПО забойного '
             f'двигателя с райбером d={template_diametr + 1}мм, {template_diametr - 1}мм, {template_diametr - 3}мм, '
             f'{template_diametr - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
             f'гл.{well_data.current_bottom}м с последующим СПО шаблона {template_diametr}мм на ТНКТ под промывку '
             f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {template_diametr}мм) '
             f'на ТНКТ с гл. {current_bottom}м вести с доливом скважины до устья т/ж '
             f'удел.весом {well_data.fluid_work} в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 ',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None],
            [None, None,
             f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с '
             f'долотом {template_diametr};'
             f' {template_diametr - 2}; {template_diametr - 4}мм  фрезера-{template_diametr}мм, '
             f'райбера-{template_diametr + 1}мм и другого оборудования и '
             f'инструмента, (при необходимости  ловильного), при необходимости на СБТ для восстановления '
             f'проходимости ствола  '
             f'и забоя скважины с применением мех.ротора, до текущего забоя с последующей нормализацией до '
             f'планового '
             f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{current_bottom}м '
             f'вести с доливом '
             f'скважины до устья т/ж удел.весом {well_data.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС',
             None],
            [None, None,
             f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию '
             f'№2 произвести '
             f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.'
             f'{current_bottom}м вести с '
             f'доливом скважины до устья т/ж удел.весом с доливом c'
             f'скважины до устья т/ж удел.весом {well_data.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None],
            [None, None,
             f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 '
             f'до планового '
             f'текущего забоя обратной циркуляцией. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке '
             f'КОТ-50 произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
             f'на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {well_data.fluid_work} в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
            [None, None,
             f'Примечание №5: В случае необходимости по результатам восстановления проходимости '
             f'экплуатационной колонны '
             f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
             f'проходимость. Подъем компоновки на ТНКТ с гл.{current_bottom}м'
             f' вести с доливом скважины до устья т/ж удел.весом {well_data.fluid_work} в объеме '
             f'{round(float(current_bottom) * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

        privyazka_nkt = [f'Привязка по ГК и ЛМ По привязому НКТ удостовериться в наличии текущего забоя', None,
                         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}.'
                         f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                         f' По привязому НКТ удостовериться в наличии '
                         f'текущего забоя с плановым, при необходимости нормализовать '
                         f'забой обратной промывкой тех жидкостью '
                         f'уд.весом {well_data.fluid_work}   до глубины {well_data.current_bottom}м',
                         None, None, None, None, None, None, None, 'Мастер КРС', None, None]


        if privyazka_question == "Да":
            list_template_ek.insert(-1, privyazka_nkt)

        if float(well_data.static_level._value) > 700:
            kot_question = QMessageBox.question(self, 'Низкий Статический уровень', 'Нужно ли произвести СПО '
                                                                                    'обратных клапанов перед ПСШ?')
            if kot_question == QMessageBox.StandardButton.Yes:
                # print(f'Нужно вставить коты')
                for row in kot_work(self, current_bottom)[::-1]:
                    list_template_ek.insert(0, row)

        if well_data.gipsInWell is True:  # Добавление работ при наличии Гипсово-солевых отложений
            gips = TemplateKrs.pero(self)
            for row in gips[::-1]:
                list_template_ek.insert(0, row)
        # print(f'счет использования шаблн {well_data.count_template}')
        if note_question_QCombo == "Да":
            list_template_ek = list_template_ek + notes_list
            well_data.count_template += 1
        else:
            list_template_ek = list_template_ek

        if solvent_question == 'Нет':
            list_template_ek.pop(2)

        well_data.current_bottom = current_bottom

        return list_template_ek

    def pero(self):
        from .rir import RirWindow
        from .drilling import Drill_window, TabPage_SO_drill

        pero_list = RirWindow.pero_select(self, well_data.current_bottom)

        gipsPero_list = [
            [f'Спустить {pero_list}  на тНКТ{well_data.nkt_diam}мм', None,
             f'Спустить {pero_list}  на тНКТ{well_data.nkt_diam}мм до глубины {well_data.current_bottom}м '
             f'с замером, шаблонированием шаблоном {well_data.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [
            f'Промывка уд.весом {well_data.fluid_work_short} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
            None,
            f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work} при расходе жидкости '
            f'6-8 л/сек в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. '
            f'ПРИ ПРОМЫВКЕ НЕ '
            f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {well_data.max_admissible_pressure._value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
            f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
            None, None, None, None, None, None, None,
            'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(well_data.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{well_data.nkt_diam}мм с глубины {well_data.current_bottom}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             round(
                 well_data.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * well_data.current_bottom / 9.5 + 0.17 + 0.5,
                 2)],
            [None, None,
             f'В случае недохождения пера до текущего забоя работы продолжить:',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             None]
        ]
        if well_data.gipsInWell is True:
            template_diametr = TabPage_SO_drill.drillingBit_diam_select(self, well_data.current_bottom)

            if well_data.column_diametr._value > 127 or (well_data.column_additional and \
                    well_data.column_additional_diametr > 127):
                downhole_motor = 'Д-106'
            else:
                downhole_motor = 'Д-76'

            if well_data.dict_pump_SHGN["do"] != 0 and well_data.paker_do["do"] == 0:
                gipsPero_list = [gipsPero_list[-1]]
                drill_list = Drill_window.drilling_nkt(self, [(well_data.current_bottom, 'гипсовых отложениий')],
                                                       'долото', template_diametr, downhole_motor )
                for row in drill_list:
                    gipsPero_list.append(row)
            else:
                drill_list = Drill_window.drilling_nkt(self, [(well_data.current_bottom, 'гипсовых отложениий')],
                                                       'долото', template_diametr, downhole_motor )

                for row in drill_list:
                    gipsPero_list.append(row)

        return gipsPero_list

    @staticmethod
    def calc_combo_nkt(type_nkt, current):
        if well_data.column_additional is False or \
            well_data.column_additional and well_data.current_bottom <= well_data.head_column_additional._value:
            if type_nkt == 'СБТ':
                nkt_string = ''
            else:
                nkt_string = f' + НКТ{well_data.nkt_diam} 20м + репер'
        else:
            if well_data.column_additional_diametr._value > 110:
                if type_nkt == 'СБТ':
                    nkt_type = {type_nkt: '2" 7/8'}
                else:
                    nkt_type = {type_nkt: '73'}
            else:
                if type_nkt == 'СБТ':
                    nkt_type = {type_nkt: '2" 3/8'}
                elif 110 < well_data.column_additional_diametr._value < 125:
                    nkt_type = {type_nkt: '73 c обточными муфтами'}
                else:
                    nkt_type = {type_nkt: '60'}

            if type_nkt == 'СБТ':
                nkt_string = f'{type_nkt}{nkt_type[type_nkt]}  ' \
                             f'{round(well_data.head_column_additional._value - current, 0)}м '
            else:
                nkt_string = f'{type_nkt}{nkt_type[type_nkt]} 20м + репер + {type_nkt}{nkt_type[type_nkt]} ' \
                             f'{round(well_data.head_column_additional._value - current - 20, 0)}м '
        return nkt_string

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = TemplateKrs()
    window.show()
    app.exec_()
