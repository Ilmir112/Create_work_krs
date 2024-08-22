import json
import math
import well_data

from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTabWidget, QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, \
    QGridLayout, QPushButton, QBoxLayout
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.alone_oreration import kot_work
from PyQt5.QtGui import QDoubleValidator
from .template_work import TemplateKrs, TabPage_SO_with
from main import MyWindow

class TabPage_SO(QWidget):
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

        self.lenght_template_first_Label = QLabel("длина первого шаблона", self)
        self.lenght_template_first_Edit = QLineEdit(self)
        self.lenght_template_first_Edit.setValidator(validator)

        self.dictance_template_first_Label = QLabel("расстояние", self)
        self.dictance_template_first_Edit = QLineEdit(self)
        self.dictance_template_first_Edit.setValidator(validator)

        self.template_second_Label = QLabel("диаметр второго шаблона", self)
        self.template_second_Edit = QLineEdit(self)
        self.template_second_Edit.setValidator(validator)

        self.lenght_template_second_Label = QLabel("длина второго шаблона", self)
        self.lenght_template_second_Edit = QLineEdit(self)
        self.lenght_template_second_Edit.setValidator(validator)

        self.dictance_template_second_Label = QLabel("расстояние-2", self)
        self.dictance_template_second_Edit = QLineEdit(self)
        self.dictance_template_second_Edit.setValidator(validator)

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        if well_data.current_bottom - well_data.perforation_sole <= 10 and well_data.open_trunk_well is False and well_data.count_template != 0:
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

        self.template_Combo.currentTextChanged.connect(self.update_template_edit)

        if well_data.count_template == 0:
            self.note_question_QCombo.setCurrentIndex(1)
            self.solvent_question_QCombo.setCurrentIndex(1)


        self.grid = QGridLayout(self)
        if well_data.column_additional is False or \
                (well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value):
            first_template, template_second = TabPage_SO_with.template_diam_ek(self)
            self.template_select_list = ['шаблон ЭК с хвостом', 'шаблон открытый ствол', 'шаблон без хвоста']

            self.template_Combo.addItems(self.template_select_list)
            template_key = self.definition_pssh()
            self.template_Combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_Combo, 2, 2, 2, 8)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)

            self.grid.addWidget(self.template_second_Label, 4, 7)
            self.grid.addWidget(self.template_second_Edit, 5, 7)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 8)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 8)
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)

        else:
            first_template, template_second = TabPage_SO_with.template_diam_additional_ek(self)
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

            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)

            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.template_second_Label, 4, 6)
            self.grid.addWidget(self.template_second_Edit, 5, 6)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 7)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 7)

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

        self.grid.addWidget(self.template_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.template_str_Edit, 14, 1, 1, 8)

        self.grid.addWidget(self.skm_teml_str_Label, 15, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_Edit, 16, 1, 1, 8)

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))

        self.lenght_template_first_Edit.setText(str(2))

        self.template_first_Edit.textChanged.connect(self.update_template)
        self.lenght_template_second_Edit.textChanged.connect(self.update_template)
        self.template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_first_Edit.textChanged.connect(self.update_template)
        self.lenght_template_first_Edit.textChanged.connect(self.update_template)


    def definition_pssh(self):


        if well_data.column_additional is False and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is False or \
            (well_data.column_additional is True and well_data.current_bottom < well_data.head_column_additional._value and well_data.open_trunk_well is False):
            template_key = 'шаблон ЭК с хвостом'

        elif well_data.column_additional is False and well_data.open_trunk_well is True:
            template_key = 'шаблон открытый ствол'

        elif well_data.column_additional is False and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is True or \
               (well_data.column_additional is True and \
                well_data.current_bottom < well_data.head_column_additional._value and \
                well_data.open_trunk_well is False):
            template_key = 'шаблон без хвоста'

        # elif well_data.column_additional is True and well_data.head_column_additional._value > roof_skm:
        #     template_key = 'ПСШ Доп колонна СКМ в основной колонне'

        elif well_data.column_additional is True and well_data.open_trunk_well is False and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in well_data.plast_work]) is False:
            template_key = 'шаблон ДП с хвостом'

        elif well_data.column_additional is True and well_data.open_trunk_well is True:
            template_key = 'шаблон ДП открытый ствол'

        elif well_data.column_additional is True and all(
                [well_data.dict_perforation[plast]['отрайбировано'] for plast in
                 well_data.plast_work]) is True and well_data.open_trunk_well is False:
            template_key = 'шаблон ДП с хвоста'
        return template_key

        # self.sole_rir_Edit.setText()
        # listEnabel = [self.khovst_label, self.khvostEdit, self.swab_true_label_type, self.swab_true_edit_type,
        #               self.plastCombo, self.pakerEdit, self.paker2Edit,
        #               self.svkTrueEdit, self.QplastEdit, self.skvProcEdit, self.acidEdit, self.acidVolumeEdit,
        #               self.acidProcEdit]
        # for enable in listEnabel:
        #     enable.setEnabled(False)

    def update_template(self):
       
        if self.template_first_Edit.text() != '':
            first_template = self.template_first_Edit.text()
        if self.lenght_template_first_Edit.text() != '':
            lenght_template_first = self.lenght_template_first_Edit.text()
        if self.template_second_Edit.text() != '':
            template_second = self.template_second_Edit.text()
        if self.lenght_template_second_Edit.text() != '':
            lenght_template_second = self.lenght_template_second_Edit.text()

        if self.dictance_template_first_Edit.text() != '':
            dictance_template_first = int(float(self.dictance_template_first_Edit.text()))
        else:
            dictance_template_first = ''
        if self.dictance_template_second_Edit.text() != '':
            dictance_template_second = int(float(self.dictance_template_second_Edit.text()))
        else:
            dictance_template_second = ''
        current_bottom = float(self.current_bottom_edit.text())
        roof_plast, roof_add_column_plast = TabPage_SO_with.definition_roof_not_raiding(self, current_bottom)
        dictance_template_first = int(well_data.current_bottom - roof_plast + 5)

        nkt_diam = well_data.nkt_diam

        if well_data.column_additional or \
                (well_data.head_column_additional._value >= well_data.current_bottom and well_data.column_additional is False):
            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'


        if first_template != '' and lenght_template_first != '' and \
                template_second != '' and lenght_template_second != '' and \
                dictance_template_first != '' and \
                dictance_template_second != '' and first_template != '':

            kot_str = ''
            if float(well_data.static_level._value) > 700:
                kot_str = '+ КОТ'

            if self.template_Combo.currentText() == 'шаблон ЭК с хвостом':
                if dictance_template_second != '':

                    template_str = f'перо {kot_str} + шаблон-{int(first_template)}мм L-{int(lenght_template_first)}м + НКТ{nkt_diam}м ' \
                                   f'{int(dictance_template_first)}м  + шаблон-{template_second}мм L-{lenght_template_second}'

                    well_data.template_depth = int(well_data.current_bottom - int(dictance_template_first) -
                                                  int(lenght_template_first))

                    skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


            elif self.template_Combo.currentText() == 'шаблон без хвоста':
                if dictance_template_second != None:
                    template_str = f'перо {kot_str} + шаблон-{template_second}мм L-{lenght_template_second}м '
                    well_data.template_depth = well_data.current_bottom
                    skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'



            elif self.template_Combo.currentText() == 'шаблон открытый ствол':
                if dictance_template_second != None:
                    self.template_first_Edit.setText('фильтр направление')
                    template_str = f'фильтр-направление + НКТ{nkt_diam}м {dictance_template_first}м {kot_str} ' \
                                   f'шаблон-{template_second}мм L-{lenght_template_second}м '
                    well_data.template_depth = int(well_data.current_bottom - int(dictance_template_first))

                    skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

            elif self.template_Combo.currentText() == 'шаблон ДП с хвостом':
                if dictance_template_second != None:
                    template_str = f'обточная муфта + {kot_str} НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_template_second}м + ' \
                                   f'шаблон-{template_second}мм L-{lenght_template_second}м '
                    well_data.template_depth = math.ceil(well_data.current_bottom - 2 -
                                                        int(dictance_template_first) - int(dictance_template_second) -
                                                        int(lenght_template_first))
                    well_data.template_depth_addition = math.ceil(well_data.current_bottom - 2 -
                                                                 int(dictance_template_first) - int(
                        dictance_template_second))



                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

            elif self.template_Combo.currentText() == 'шаблон ДП без хвоста':

                template_str = f'обточная муфта {kot_str} + ' \
                               f'шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                               f'НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                               f'L-{lenght_template_second}м '

                well_data.template_depth = math.ceil(well_data.current_bottom - int(dictance_template_second) -
                                                    int(lenght_template_first))
                well_data.template_depth_addition = math.ceil(
                    well_data.current_bottom - int(dictance_template_second))


                skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'


            elif self.template_Combo.currentText() == 'шаблон ДП открытый ствол':
                if dictance_template_second != None:
                    template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f' {kot_str} + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м' \
                                   f' + НКТ{nkt_pod} + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '
                    well_data.template_depth = math.ceil(well_data.current_bottom - 2 -
                                                        int(dictance_template_first) - int(dictance_template_second) -
                                                        int(lenght_template_first))
                    well_data.template_depth_addition = math.ceil(well_data.current_bottom - 2 -
                                                                 int(dictance_template_first) - int(
                        dictance_template_second))


                    skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'
            if dictance_template_second != "":
                self.template_str_Edit.setText(template_str)
                self.skm_teml_str_Edit.setText(skm_teml_str)

    def update_template_edit(self, index):
       
        template_str = ''
        skm_teml_str = ''
        nkt_diam = well_data.nkt_diam
        if well_data.column_additional is False or (well_data.column_additional and
                                                   well_data.head_column_additional._value >= well_data.current_bottom):

            first_template, template_second = TabPage_SO_with.template_diam_ek(self)
            # print(f'диаметры шаблонов {first_template, template_second}')
        else:
            first_template, template_second = TabPage_SO_with.template_diam_additional_ek(self)
            # print(f'диаметры шаблонов {first_template, template_second}')

        current_bottom = float(self.current_bottom_edit.text())

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))
        # self.skm_Edit.setText(str(well_data.column_diametr._value))
        self.dictance_template_second_Edit.setText(str(10))

        roof_plast, roof_add_column_plast = TabPage_SO_with.definition_roof_not_raiding(self, current_bottom)
        dictance_template_first = int(well_data.current_bottom - roof_plast + 5)
        # print(f'дистанция первая {dictance_template_first}')
        self.dictance_template_first_Edit.setText(str(dictance_template_first))

        lenght_template_first, lenght_template_second = TabPage_SO_with.definition_ECN_true(self, well_data.dict_pump_ECN_h["posle"])
        self.lenght_template_first_Edit.setText(lenght_template_first)
        self.lenght_template_second_Edit.setText(str(lenght_template_second))

        first_template = self.template_first_Edit.text()
        template_second = int(self.template_second_Edit.text())
        lenght_template_first = int(self.lenght_template_first_Edit.text())

        dictance_template_first = int(self.dictance_template_first_Edit.text())

        lenght_template_second = int(self.lenght_template_second_Edit.text())
        dictance_template_second = int(self.dictance_template_second_Edit.text())


        self.template_first_Label.setParent(None)
        self.template_first_Edit.setParent(None)
        self.lenght_template_first_Label.setParent(None)
        self.lenght_template_first_Edit.setParent(None)

        self.dictance_template_first_Label.setParent(None)
        self.dictance_template_first_Edit.setParent(None)
        self.dictance_template_second_Edit.setParent(None)



        if well_data.column_additional or \
                (well_data.head_column_additional._value >= well_data.current_bottom and well_data.column_additional is False):
            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        if index == 'шаблон ЭК с хвостом':
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)

            template_str = f'перо + шаблон-{first_template}мм L-2м + НКТ{nkt_diam}мм ' \
                           f'{dictance_template_first}м ' \
                           f'+  НКТ{nkt_diam}мм + шаблон-{template_second}мм' \
                           f' L-{lenght_template_second}м '

            # print(f'строка шаблона {template_str}')
            well_data.template_depth = int(roof_plast - 5)
            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'



        elif index == 'шаблон без хвоста':
            self.dictance_template_second_Edit.setParent(None)
            self.dictance_template_second_Label.setParent(None)
            self.dictance_template_first_Edit.setParent(None)
            self.dictance_template_first_Label.setParent(None)

            template_str = f'перо + шаблон-{template_second}мм L-{lenght_template_second}м '
            well_data.template_depth = well_data.current_bottom
            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'шаблон открытый ствол':

            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            # self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            # self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_first_Label, 4, 4)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 4)
            # self.grid.addWidget(self.lenght_template_second_Label, 4, 9)
            # self.grid.addWidget(self.lenght_template_second_Edit, 5, 9)

            self.template_first_Edit.setText('фильтр направление')
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            self.dictance_template_second_Edit.setText(str(10))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'фильтр-направление L-2 + НКТ{nkt_diam}м {dictance_template_first}м +' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '
            well_data.template_depth = int(roof_plast - 5)

            skm_teml_str = f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'шаблон ДП с хвостом':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 8)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 8)


            dictance_template_first = int(well_data.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            dictance_template_second = int(roof_add_column_plast - well_data.head_column_additional._value - int(
                self.lenght_template_first_Edit.text())+5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))



            template_str = f'обточная муфта + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f' + шаблон-{first_template}мм ' \
                           f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_template_second}м + ' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '
            well_data.template_depth = math.ceil(roof_add_column_plast - 5 - lenght_template_first - dictance_template_second)
            well_data.template_depth_addition = math.ceil(roof_add_column_plast - 5)


            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        elif index == 'шаблон ДП без хвоста':
            self.dictance_template_first_Edit.setParent(None)
            self.dictance_template_first_Label.setParent(None)
            self.grid.addWidget(self.template_first_Label, 4, 2)
            self.grid.addWidget(self.template_first_Edit, 5, 2)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 3)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 3)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 6)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 6)
            self.grid.addWidget(self.template_second_Label, 4, 7)
            self.grid.addWidget(self.template_second_Edit, 5, 7)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 8)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 8)


            dictance_template_second = int(well_data.current_bottom - well_data.head_column_additional._value
                - int(lenght_template_first) + 5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'обточная муфта + шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '

            well_data.template_depth = math.ceil(well_data.current_bottom - dictance_template_second -
                                                lenght_template_first)
            well_data.template_depth_addition = math.ceil(well_data.current_bottom)

            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'



        elif index == 'шаблон ДП открытый ствол':

            self.grid.addWidget(self.dictance_template_first_Label, 4, 2)
            self.grid.addWidget(self.dictance_template_first_Edit, 5, 2)
            self.grid.addWidget(self.template_first_Label, 4, 3)
            self.grid.addWidget(self.template_first_Edit, 5, 3)
            self.grid.addWidget(self.lenght_template_first_Label, 4, 4)
            self.grid.addWidget(self.lenght_template_first_Edit, 5, 4)
            self.grid.addWidget(self.dictance_template_second_Label, 4, 5)
            self.grid.addWidget(self.dictance_template_second_Edit, 5, 5)
            self.grid.addWidget(self.lenght_template_second_Label, 4, 8)
            self.grid.addWidget(self.lenght_template_second_Edit, 5, 8)



            dictance_template_first = int(well_data.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first))
            dictance_template_first = int(self.dictance_template_first_Edit.text())

            dictance_template_second = int(roof_add_column_plast - well_data.head_column_additional._value - int(
                self.lenght_template_first_Edit.text()) + 5)
            self.dictance_template_second_Edit.setText(str(dictance_template_second))


            template_str = f'фильтр направление + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f' + шаблон-{first_template}мм L-{lenght_template_first}м' \
                           f' + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '
            well_data.template_depth = math.ceil(
                roof_add_column_plast - 5 - lenght_template_first - dictance_template_second)
            well_data.template_depth_addition = math.ceil(roof_add_column_plast - 5)


            skm_teml_str = f'шаблон-{first_template}мм до гл.{well_data.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{well_data.template_depth}м'

        self.template_str_Edit.setText(template_str)
        self.skm_teml_str_Edit.setText(skm_teml_str)

        if 'ПОМ' in str(well_data.paker_do["posle"]).upper() and '122' in str(well_data.paker_do["posle"]):
            self.template_second_Edit.setText(str(126))

    def definition_ECN_true(self, depth_ecn):
       
        if well_data.column_additional is False and well_data.dict_pump_ECN["posle"] != 0:
            return "2", "30"
        elif well_data.column_additional is False and well_data.max_angle._value > 45:
            return "2", "10"
        elif well_data.column_additional is True and well_data.dict_pump_ECN["posle"] != 0:
            if well_data.dict_pump_ECN["posle"] != 0 and float(depth_ecn) < well_data.head_column_additional._value:
                return "2", "30"

            elif well_data.dict_pump_ECN["posle"] != 0 and float(depth_ecn) >= well_data.head_column_additional._value:
                return "30", "4"
            elif well_data.max_angle._value > 45:
                return "10", "4"
        else:
            return "2", "4"

            # print(f' ЭЦН длина" {well_data.lift_ecn_can, well_data.lift_ecn_can_addition, "ЭЦН" in str(well_data.dict_pump["posle"][0]).upper()}')




class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Выбор компоновки шаблонов')


class Template_without_skm(QMainWindow):
    def __init__(self,  ins_ind, table_widget):

        super(QMainWindow, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.rir_paker = None
        self.paker_select = None
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()

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
        template_lenght = int(float(self.tabWidget.currentWidget().lenght_template_second_Edit.text()))
        if well_data.column_additional:
            template_lenght_addition = int(float(self.tabWidget.currentWidget().lenght_template_first_Edit.text()))
        if well_data.column_additional is False or (
                well_data.column_additional is True and float(
            well_data.head_column_additional._value) >= well_data.current_bottom):
            template_diametr = int(self.tabWidget.currentWidget().template_second_Edit.text())
        else:
            template_diametr = int(self.tabWidget.currentWidget().template_first_Edit.text())
        # print(f'проблема ЭК {well_data.problemWithEk_diametr}')
        if (template_diametr >= int(well_data.problemWithEk_diametr) - 2
            and well_data.template_depth > int(well_data.problemWithEk_depth)):
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')
            return
        if well_data.column_additional is False or \
                well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value:
            if well_data.template_depth > well_data.current_bottom:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
        else:
            if well_data.template_depth_addition > well_data.current_bottom:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже текущего забоя')
                return
            if well_data.template_depth >= well_data.head_column_additional._value:
                mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже головы хвостовика')
                return
            # if self.template_Combo.currentText() == 'ПСШ Доп колонна СКМ в основной колонне' and\
            #         well_data.skm_depth >= well_data.head_column_additional._value:
            #     mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'СКМ спускается ниже головы хвостовика')
            #     return
        if distance_second < 0 or distance_first < 0:
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Расстояние между шаблонами не корректно')
            return
        well_data.template_lenght = template_lenght
        if well_data.column_additional:
            well_data.template_lenght_addition = template_lenght_addition
        current_bottom = self.tabWidget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            well_data.current_bottom = round(float(current_bottom), 1)

        self.update_template(well_data.ins_ind)
        work_list = self.template_ek(template_str, template, template_diametr)
        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def update_template(self, index_plan):

        row_index = index_plan - well_data.count_row_well
        template_ek = json.dumps(
            [well_data.template_depth, well_data.template_lenght, well_data.template_depth_addition,
             well_data.template_lenght_addition])
        for index, data in enumerate(well_data.data_list):
            if index == index:
                template_ek_old = well_data.data_list[index][11]
            if row_index < index:
                if well_data.data_list[index][11] == template_ek_old:
                    well_data.data_list[index][11] = template_ek
    def well_volume(self):
       
        # print(well_data.column_additional)
        if not well_data.column_additional:

            volume_well = 3.14 * (well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000000 * (
                well_data.current_bottom)
            return volume_well
        else:
            volume_well = (3.14 * (
                    well_data.column_additional_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                   well_data.current_bottom - float(well_data.head_column_additional._value)) / 1000) + (
                                  3.14 * (
                                      well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                      well_data.head_column_additional._value) / 1000)
            return volume_well

    def template_ek(self, template_str, template, temlate_ek):

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
            [f'Cпустить {template_str} на НКТ{well_data.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{well_data.nkt_diam}мм  с замером, шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom, 1.2)],

            [f'Обработка растворителем в V-{solvent_volume_edit}', None,
             f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
             f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3. При открытом затрубном пространстве закачать в '
             f'трубное пространство растворитель в объеме {solvent_volume_edit}м3, продавить в трубное пространство тех.жидкостью '
             f'в объеме {round(3 * float(current_bottom) / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [f'Нормализовать до глубины {current_bottom}м.',
             None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                   f'{well_data.fluid_work} до глубины {current_bottom}м.', None, None, None, None, None,
             None, None,
             'Мастер КРС', None],
            [f'Промыть в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  при расходе жидкости 6-8 л/сек '
             f'в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. ПРИ '
             f'ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {well_data.max_admissible_pressure._value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
             f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', well_volume_norm(TemplateKrs.well_volume(self) * 1.5)],
            [
            f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя',
            None,
            f'Приподнять до глубины {round(float(current_bottom) - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, при '
            f'необходимости повторная промывка.',
            None, None, None, None, None, None, None,
            'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {template_str} на НКТ{well_data.nkt_diam}мм с глубины {current_bottom}м с доливом скважины в '
             f'объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(current_bottom, 1.2)]
        ]
        if abs(well_data.perforation_sole - current_bottom) < 15:
            list_template_ek.pop(-2)

        notes_list = [
            [None, None,
               f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного '
               f'двигателя с райбером d={temlate_ek + 1}мм, {temlate_ek - 1}мм, {temlate_ek - 3}мм, '
               f'{temlate_ek - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
               f'гл.{current_bottom}м с последующим СПО шаблона {temlate_ek}мм на ТНКТ под промывку '
               f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
               f'на ТНКТ с гл. {current_bottom}м вести с доливом скважины до устья т/ж '
               f'удел.весом {well_data.fluid_work} в '
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
               f'текущего забоя. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке  '
               f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
               f'на ТНКТ с гл.{current_bottom}м'
               f' вести с доливом скважины до устья т/ж удел.весом {well_data.fluid_work} в '
               f'объеме {round(current_bottom * 1.12 / 1000, 1)}м3',
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
                         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}".'
                         f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                         f' По привязому НКТ удостовериться в наличии'
                         f'текущего забоя с плановым, при необходимости нормализовать забой обратной промывкой тех жидкостью '
                         f'уд.весом {well_data.fluid_work}   до глубины {current_bottom}м',
                         None, None, None, None, None, None, None, 'Мастер КРС', None, None]
        if privyazka_question == "Да":
            list_template_ek.insert(-1, privyazka_nkt)

        if float(well_data.static_level._value) > 700:
            kot_question = QMessageBox.question(self, 'Низкий Статический уровень', 'Нужно ли произвести СПО '
                                                                                    'обратных клапанов перед ПСШ?')
            if kot_question == QMessageBox.StandardButton.Yes:
                # print(f'Нужно вставить коты')
                for row in kot_work(self, well_data.current_bottom)[::-1]:
                    list_template_ek.insert(0, row)

        if well_data.gipsInWell is True and well_data.count_template == 0:
            # Добавление работ при наличии Гипсово-солевых отложений
            gips = TemplateKrs.pero(self)
            for row in gips[::-1]:
                list_template_ek.insert(0, row)

        if note_question_QCombo == "Да":
            list_template_ek = list_template_ek + notes_list
            well_data.count_template += 1
        else:
            list_template_ek = list_template_ek
        if solvent_question == 'Нет':
            list_template_ek.pop(1)

        well_data.current_bottom = current_bottom
        return list_template_ek

    def pero(self):
        from .rir import RirWindow
        from .drilling import Drill_window

        pero_list = RirWindow.pero_select(self, well_data.current_bottom)
        gipsPero_list = [
            [f'Спустить {pero_list}  на тНКТ{well_data.nkt_diam}мм', None,
             f'Спустить {pero_list}  на тНКТ{well_data.nkt_diam}мм до глубины {well_data.current_bottom}м '
             f'с замером, шаблонированием шаблоном {well_data.nkt_template}мм. Опрессовать НКТ на 150атм. Вымыть шар. \n'
             f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [
                f'Промывка уд.весом {well_data.fluid_work_short} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work} при расходе жидкости '
                f'6-8 л/сек в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ '
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

            if well_data.dict_pump_SHGN["do"] != 0:

                gipsPero_list = [gipsPero_list[-1]]
                from .drilling import Drill_window
                if self.raid_window is None:
                    self.raid_window = Drill_window(self.table_widget, self.ins_ind)
                    # self.raid_window.setGeometry(200, 400, 300, 400)
                    self.raid_window.show()
                    MyWindow.pause_app()
                    drill_work_list = self.raid_window.add_work()
                    well_data.pause = True

                    self.raid_window = None
                else:
                    self.raid_window.close()  # Close window.
                    self.raid_window = None

                for row in drill_work_list:
                    gipsPero_list.append(row)
            else:
                if self.raid_window is None:
                    self.raid_window = Drill_window(self.table_widget, self.ins_ind)
                    # self.raid_window.setGeometry(200, 400, 300, 400)
                    self.raid_window.show()
                    MyWindow.pause_app()
                    drill_work_list = self.raid_window.add_work()
                    well_data.pause = True

                    self.raid_window = None
                else:
                    self.raid_window.close()  # Close window.
                    self.raid_window = None
                for row in drill_work_list:
                    gipsPero_list.append(row)

        return gipsPero_list