import math
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTabWidget, QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, \
    QGridLayout, QPushButton, QBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QApplication

from open_pz import CreatePZ
from work_py.acid_paker import AcidPakerWindow
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.alone_oreration import kot_work
from PyQt5.QtGui import QDoubleValidator


class TabPage_SO_with(QWidget):
    def __init__(self, parent=None):
        from open_pz import CreatePZ
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
        # self.dictance_three_Edit.setValidator()

        self.roof_skm_label = QLabel("Кровля скреперования", self)
        self.roof_skm_line = QLineEdit(self)
        self.roof_skm_line.setValidator(validator)
        self.roof_skm_line.setClearButtonEnabled(True)

        self.sole_skm_label = QLabel("Кровля скреперования", self)
        self.sole_skm_line = QLineEdit(self)
        self.sole_skm_line.setClearButtonEnabled(True)
        self.sole_skm_line.setValidator(validator)



        self.grid = QGridLayout(self)
        if CreatePZ.column_additional is False or \
                (CreatePZ.column_additional and CreatePZ.current_bottom < CreatePZ.head_column_additional._value):
            self.template_select_list = ['ПСШ ЭК', 'ПСШ открытый ствол', 'ПСШ без хвоста']

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

        self.grid.addWidget(self.template_str_Label, 11, 1, 1, 8)
        self.grid.addWidget(self.template_str_Edit, 12, 1, 1, 8)

        self.grid.addWidget(self.skm_teml_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_Edit, 14, 1, 1, 8)

        if CreatePZ.column_additional is False or (CreatePZ.column_additional and
                                                   CreatePZ.head_column_additional._value >= CreatePZ.current_bottom):
            first_template, template_second = self.template_diam_ek()
        else:
            first_template, template_second = self.template_diam_additional_ek()

        self.grid.addWidget(self.roof_skm_label, 35, 2, 1, 3)
        self.grid.addWidget(self.roof_skm_line, 36, 2, 1, 3)

        self.grid.addWidget(self.sole_skm_label, 35, 5, 1, 3)
        self.grid.addWidget(self.sole_skm_line, 36, 5, 1, 3)

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))

        self.lenght_template_first_Edit.setText(str(2))


        #
        # dictance_template_first = int(CreatePZ.current_bottom - roof_plast + 5)
        # self.dictance_template_first_Edit.setText(str(dictance_template_first))
        # self.skm_Edit.setText(str(CreatePZ.column_diametr._value))
        # self.dictance_template_second_Edit.setText(str(10))

        self.template_first_Edit.textChanged.connect(self.update_template)
        self.dictance_three_Edit.textChanged.connect(self.update_template)
        self.lenght_template_second_Edit.textChanged.connect(self.update_template)
        self.template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_second_Edit.textChanged.connect(self.update_template)
        self.dictance_template_first_Edit.textChanged.connect(self.update_template)
        self.lenght_template_first_Edit.textChanged.connect(self.update_template)
        self.skm_Edit.textChanged.connect(self.update_template)

    def definition_pssh(self):
        from open_pz import CreatePZ

        if CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
                [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
            template_key = 'ПСШ ЭК'

        elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is True:
            template_key = 'ПСШ открытый ствол'

        elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
                [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is True:
            template_key = 'ПСШ без хвоста'

        # elif CreatePZ.column_additional is True and CreatePZ.head_column_additional._value > roof_skm:
        #     template_key = 'ПСШ Доп колонна СКМ в основной колонне'

        elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is False and all(
                [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
            template_key = 'ПСШ СКМ в доп колонне c хвостом'

        elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is True:
            template_key = 'ПСШ СКМ в доп колонне + открытый ствол'

        elif CreatePZ.column_additional is True and all(
                [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in
                 CreatePZ.plast_work]) is True and CreatePZ.open_trunk_well is False:
            template_key = 'ПСШ СКМ в доп колонне без хвоста'
        return template_key

        # self.sole_rir_Edit.setText()
        # listEnabel = [self.khovstLabel, self.khvostEdit, self.swabTruelabelType, self.swabTrueEditType,
        #               self.plastCombo, self.pakerEdit, self.paker2Edit,
        #               self.svkTrueEdit, self.QplastEdit, self.skvProcEdit, self.acidEdit, self.acidVolumeEdit,
        #               self.acidProcEdit]
        # for enable in listEnabel:
        #     enable.setEnabled(False)

    def update_template(self):
        from open_pz import CreatePZ
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
        nkt_diam = CreatePZ.nkt_diam

        roof_plast, roof_add_column_plast = self.definition_roof_not_raiding()

        if CreatePZ.column_additional or \
                (CreatePZ.head_column_additional._value >= CreatePZ.current_bottom and CreatePZ.column_additional is False):
            nkt_pod = '60мм' if CreatePZ.column_additional_diametr._value < 110 else '73мм со снятыми фасками'


        if first_template != '' and lenght_template_first != '' and \
                template_second != '' and lenght_template_second != '' and \
                skm != '' and dictance_template_first != '' and \
                dictance_template_second != '' and first_template != '':

            if self.template_Combo.currentText() == 'ПСШ ЭК':
                if dictance_template_second != '':
                    self.dictance_three_Edit.setParent(None)
                    self.dictance_three_Label.setParent(None)

                    template_str = f'перо + шаблон-{int(first_template)}мм L-{int(lenght_template_first)}м + НКТ{nkt_diam}м ' \
                                   f'{int(dictance_template_first)}м + СКМ-{skm} +  ' \
                                   f'НКТ{nkt_diam}м {int(dictance_template_second)}м + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '

                    CreatePZ.template_depth = int(CreatePZ.current_bottom - int(dictance_template_first) -
                                                  int(lenght_template_first)) - int(dictance_template_second)
                    CreatePZ.skm_depth = CreatePZ.template_depth + dictance_template_second
                    skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ без хвоста':
                if dictance_template_second != None:
                    template_str = f'перо + СКМ-{skm} + {dictance_template_second}м ' \
                                   f'НКТ{nkt_diam}м + шаблон-{template_second}мм L-{lenght_template_second}м '
                    CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - int(dictance_template_second))
                    CreatePZ.skm_depth = CreatePZ.template_depth + dictance_template_second
                    skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ открытый ствол':
                if dictance_template_second != None:
                    self.template_first_Edit.setText('фильтр направление')
                    template_str = f'фильтр-направление L {lenght_template_first}м + НКТ{nkt_diam}м {dictance_template_first}м ' \
                                   f'+ СКМ-{skm} + {dictance_template_second}м НКТ{nkt_diam}м + ' \
                                   f'шаблон-{template_second}мм L-{lenght_template_second}м '
                    CreatePZ.template_depth = int(CreatePZ.current_bottom - int(dictance_template_first) -
                                                  int(dictance_template_second) - int(lenght_template_first))
                    CreatePZ.skm_depth = CreatePZ.template_depth + dictance_template_second
                    skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ Доп колонна СКМ в основной колонне':
                if dictance_template_second != None:
                    template_str = f'обточная муфта  + ' \
                                   f'НКТ{nkt_pod}  + {dictance_template_first}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_template_second}м + НКТ{nkt_diam} {dictance_three}м + ' \
                                   f'СКМ-{skm} + шаблон-{template_second}мм L-{lenght_template_second}м '

                    CreatePZ.template_depth_addition = int(roof_add_column_plast - 5)

                    CreatePZ.template_depth = int(roof_add_column_plast - 5 -dictance_template_second - dictance_three)
                    CreatePZ.skm_depth = CreatePZ.template_depth + dictance_three
                # template_str = template_SKM_DP_EK
                skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                               f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне c хвостом':
                if dictance_template_second != None:
                    template_str = f'обточная муфта + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_three}м + ' \
                                   f'шаблон-{template_second}мм L-{lenght_template_second}м '
                    CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 2 -
                                                        int(dictance_template_first) - int(dictance_template_second) -
                                                        int(lenght_template_first) - int(dictance_three))
                    CreatePZ.template_depth_addition = math.ceil(roof_add_column_plast -
                                                                 5 - dictance_template_second)
                    CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне без хвоста':
                if dictance_three != "":
                    template_str = f'обточная муфта + СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second} + ' \
                                   f'шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                                   f'НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '

                    CreatePZ.template_depth = math.ceil(roof_add_column_plast - 5 - dictance_template_second - dictance_three)
                    CreatePZ.template_depth_addition = math.ceil(
                        CreatePZ.current_bottom - int(dictance_template_second))
                    CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second
                    skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'


            elif self.template_Combo.currentText() == 'ПСШ СКМ в доп колонне + открытый ствол':
                if dictance_template_second != None:
                    template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {dictance_template_first}м ' \
                                   f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                                   f'L-{lenght_template_first}м' \
                                   f' + НКТ{nkt_pod} {dictance_three}м + шаблон-{template_second}мм ' \
                                   f'L-{lenght_template_second}м '
                    CreatePZ.template_depth_addition = math.ceil(roof_add_column_plast -
                                                                 5 - dictance_template_second)

                    CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second

                    skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                                   f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'
            if dictance_template_second != "":
                self.template_str_Edit.setText(template_str)
                self.skm_teml_str_Edit.setText(skm_teml_str)

    def update_template_edit(self, index):
        from open_pz import CreatePZ

        nkt_diam = CreatePZ.nkt_diam
        if CreatePZ.column_additional is False or (CreatePZ.column_additional and
                                                   CreatePZ.head_column_additional._value >= CreatePZ.current_bottom):

            first_template, template_second = self.template_diam_ek()
            # print(f'диаметры шаблонов {first_template, template_second}')
        else:
            first_template, template_second = self.template_diam_additional_ek()
            # print(f'диаметры шаблонов {first_template, template_second}')

        self.template_first_Edit.setText(str(first_template))
        self.template_second_Edit.setText(str(template_second))
        self.skm_Edit.setText(str(CreatePZ.column_diametr._value))
        self.dictance_template_second_Edit.setText(str(10))

        roof_plast, roof_add_column_plast = self.definition_roof_not_raiding()
        dictance_template_first1 = int(CreatePZ.current_bottom - roof_plast + 5)
        self.dictance_template_first_Edit.setText(str(dictance_template_first1))

        lenght_template_first, lenght_template_second = self.definition_ECN_true(CreatePZ.dict_pump_ECN_h["posle"])
        self.lenght_template_first_Edit.setText(lenght_template_first)
        self.lenght_template_second_Edit.setText(str(lenght_template_second))

        first_template = self.template_first_Edit.text()
        template_second = int(self.template_second_Edit.text())
        lenght_template_first = int(self.lenght_template_first_Edit.text())

        dictance_template_first = int(self.dictance_template_first_Edit.text())

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

        if CreatePZ.column_additional or \
                (CreatePZ.head_column_additional._value >= CreatePZ.current_bottom and CreatePZ.column_additional is False):
            nkt_pod = '60мм' if CreatePZ.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

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
            CreatePZ.template_depth = int(CreatePZ.current_bottom - int(dictance_template_first1) -
                                          int(lenght_template_first)) - int(dictance_template_second)
            CreatePZ.skm_depth = CreatePZ.template_depth + dictance_template_second
            skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'



        elif index == 'ПСШ без хвоста':
            template_str = f'перо + СКМ-{skm} + {dictance_template_second}м ' \
                           f'НКТ{nkt_diam}м + шаблон-{template_second}мм L-{lenght_template_second}м '
            CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - int(dictance_template_second))
            CreatePZ.skm_depth = CreatePZ.current_bottom
            skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

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
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))
            self.dictance_template_second_Edit.setText(str(10))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            template_str = f'фильтр-направление + НКТ{nkt_diam}м {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + {dictance_template_second}м НКТ{nkt_diam}м + ' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '
            CreatePZ.template_depth = int(CreatePZ.current_bottom - dictance_template_first - dictance_template_second)
            CreatePZ.skm_depth = CreatePZ.template_depth + dictance_template_second

            skm_teml_str = f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

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
            dictance_template_first1 = int(CreatePZ.current_bottom - roof_add_column_plast + 5)

            # print(f'дистанци {dictance_template_first }')
            self.skm_Edit.setText(str(CreatePZ.column_diametr._value))
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))
            dictance_template_first = int(self.dictance_template_first_Edit.text())
            dictance_second1 = int(roof_add_column_plast - lenght_template_first - CreatePZ.head_column_additional._value - 5)
            self.dictance_template_second_Edit.setText(str(dictance_second1))
            dictance_template_second = int(self.dictance_template_second_Edit.text())
            self.lenght_template_second_Edit.setText(str(lenght_template_second))

            self.dictance_three_Edit.setText(str(roof_plast - CreatePZ.head_column_additional._value + 10))
            dictance_three_first = int(float(self.dictance_three_Edit.text()))

            template_str = f'обточная муфта  + ' \
                           f'НКТ{nkt_pod}  + {dictance_template_first}м + шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_template_second}м +'\
                           f'СКМ-{skm} + НКТ{nkt_diam} {dictance_three_first}м + шаблон-{template_second}мм L-{lenght_template_second}м '

            CreatePZ.template_depth_addition = int(CreatePZ.current_bottom - dictance_template_first)
            CreatePZ.template_depth = int(CreatePZ.current_bottom - dictance_template_first - lenght_template_first -
                                          dictance_template_second - dictance_three_first)
            CreatePZ.skm_depth = CreatePZ.template_depth + dictance_three_first
            # template_str = template_SKM_DP_EK
            skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'


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

            self.skm_Edit.setText(str(CreatePZ.column_additional_diametr._value))
            skm = str(self.skm_Edit.text())
            dictance_template_first1 = int(CreatePZ.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))
            dictance_template_first = int(self.dictance_template_first_Edit.text())

            dictance_three_first = int(roof_add_column_plast - CreatePZ.head_column_additional._value - int(
                self.lenght_template_first_Edit.text()) - 9)
            self.dictance_three_Edit.setText(str(dictance_three_first))
            dictance_template_three = int(self.dictance_three_Edit.text())
            template_str = f'обточная муфта + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                           f'L-{lenght_template_first}м + НКТ{nkt_pod} {dictance_three_first}м + ' \
                           f'шаблон-{template_second}мм L-{lenght_template_second}м '
            CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 2 -
                                                dictance_template_first - dictance_template_second -
                                                lenght_template_first - dictance_template_three)
            CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - 2 -
                                                         dictance_template_first - dictance_template_second)
            CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second

            skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

        elif index == 'ПСШ СКМ в доп колонне без хвоста':

            self.grid.addWidget(self.dictance_three_Label, 4, 7)
            self.grid.addWidget(self.dictance_three_Edit, 5, 7)

            dictance_template_first1 = 0
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))

            self.skm_Edit.setText(str(CreatePZ.column_additional_diametr._value))
            skm = str(self.skm_Edit.text())
            self.dictance_template_second_Edit.setText(str(10))
            dictance_template_second = int(self.dictance_template_second_Edit.text())

            dictance_three = int(
                CreatePZ.current_bottom - int(dictance_template_second) - CreatePZ.head_column_additional._value
                - int(lenght_template_first) + 4)
            self.dictance_three_Edit.setText(str(dictance_three))
            dictance_three_first = int(self.dictance_three_Edit.text())

            template_str = f'обточная муфта + СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second} + ' \
                           f'шаблон-{first_template}мм L-{lenght_template_first}м + ' \
                           f'НКТ{nkt_pod} {dictance_three_first}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '

            CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - dictance_template_second -
                                                lenght_template_first - dictance_three_first)
            CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - dictance_template_second)
            CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second
            skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'



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

            self.skm_Edit.setText(str(CreatePZ.column_additional_diametr._value))
            skm = str(self.skm_Edit.text())
            dictance_template_first1 = int(CreatePZ.current_bottom - roof_add_column_plast + 5)
            self.dictance_template_first_Edit.setText(str(dictance_template_first1))
            dictance_template_first = int(self.dictance_template_first_Edit.text())

            dictance_three_first = int(roof_add_column_plast - CreatePZ.head_column_additional._value - int(
                self.lenght_template_first_Edit.text()) - 9)
            self.dictance_three_Edit.setText(str(dictance_three_first))
            dictance_template_three = int(self.dictance_three_Edit.text())

            template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {dictance_template_first}м ' \
                           f'+ СКМ-{skm} + НКТ{nkt_pod} {dictance_template_second}м + шаблон-{first_template}мм ' \
                           f'L-{lenght_template_first}м' \
                           f' + НКТ{nkt_pod} {dictance_template_three}м + шаблон-{template_second}мм ' \
                           f'L-{lenght_template_second}м '
            CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 2 -
                                                dictance_template_first - dictance_template_second -
                                                lenght_template_first - dictance_template_three)
            CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - 2 -
                                                         dictance_template_first - dictance_template_second)
            CreatePZ.skm_depth = CreatePZ.template_depth_addition + dictance_template_second

            skm_teml_str = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                           f'шаблон-{template_second}мм до гл.{CreatePZ.template_depth}м'

        self.template_str_Edit.setText(template_str)
        self.skm_teml_str_Edit.setText(skm_teml_str)

        if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
            self.template_second_Edit.setText(str(126))

    def definition_ECN_true(self, depth_ecn):
        from open_pz import CreatePZ
        if CreatePZ.column_additional is False and CreatePZ.dict_pump_ECN["posle"] != 0:
            return "4", "30"
        elif CreatePZ.column_additional is True and CreatePZ.dict_pump_ECN["posle"] != 0 \
                and CreatePZ.column_additional_diametr._value < 170:
            if CreatePZ.dict_pump_ECN["posle"] != 0 and float(depth_ecn) < CreatePZ.head_column_additional._value:
                return "4", "30"

            elif CreatePZ.dict_pump_ECN["posle"] != 0 and float(depth_ecn) >= CreatePZ.head_column_additional._value:

                return "30", "4"
        else:
            return "4", "4"

            # print(f' ЭЦН длина" {CreatePZ.lift_ecn_can, CreatePZ.lift_ecn_can_addition, "ЭЦН" in str(CreatePZ.dict_pump["posle"][0]).upper()}')

    def definition_roof_not_raiding(self):
        from open_pz import CreatePZ
        dict_perforation = CreatePZ.dict_perforation
        plast_all = list(dict_perforation.keys())
        roof_plast = CreatePZ.current_bottom
        if CreatePZ.column_additional is False or (
                CreatePZ.column_additional and CreatePZ.head_column_additional._value >= CreatePZ.current_bottom):
            for plast in plast_all:
                roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
                # print(roof_plast < roof, roof_plast, roof)
                if roof_plast > roof:
                    if dict_perforation[plast]['отрайбировано'] and CreatePZ.open_trunk_well is False:
                        roof_add_column_plast = roof_plast
                    elif CreatePZ.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = CreatePZ.shoe_column._value
                        roof_add_column_plast = CreatePZ.current_bottom
                        break
                    else:
                        roof_plast = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
                        roof_add_column_plast = roof_plast
                        break
                    if roof_plast > CreatePZ.current_bottom:
                        roof_plast = CreatePZ.current_bottom
                else:
                    roof_add_column_plast = roof_plast


        elif CreatePZ.column_additional:
            for plast in plast_all:
                roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))

                if CreatePZ.head_column_additional._value <= roof:
                    if dict_perforation[plast]['отрайбировано'] and CreatePZ.open_trunk_well is False:
                        roof_add_column_plast = CreatePZ.current_bottom
                        roof_plast = CreatePZ.head_column_additional._value
                    elif CreatePZ.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_plast = CreatePZ.shoe_column._value
                        roof_add_column_plast =CreatePZ.current_bottom
                        break
                    else:
                        roof_add_column_plast = roof
                        roof_plast = CreatePZ.head_column_additional._value
                        break

                else:
                    if dict_perforation[plast]['отрайбировано']:

                        roof_add_column_plast = CreatePZ.current_bottom
                        roof_plast = CreatePZ.head_column_additional._value
                    elif CreatePZ.open_trunk_well is True and dict_perforation[plast]['отрайбировано']:
                        roof_add_column_plast = CreatePZ.shoe_column_additional._value
                        roof_plast = roof
                        break
                    else:
                        roof_add_column_plast = CreatePZ.current_bottom
                        roof_plast = roof
                        break

        return roof_plast, roof_add_column_plast

    def template_diam_ek(self):
        from open_pz import CreatePZ

        diam_internal_ek = CreatePZ.column_diametr._value - 2 * CreatePZ.column_wall_thickness._value

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
        return (template_first_diam, template_second_diam)

    def template_diam_additional_ek(self):  # Выбор диаметра шаблонов при наличии в скважине дополнительной колонны
        from open_pz import CreatePZ
        diam_internal_ek = CreatePZ.column_diametr._value - 2 * CreatePZ.column_wall_thickness._value
        diam_internal_ek_addition = float(CreatePZ.column_additional_diametr._value) - 2 * float(
            CreatePZ.column_additional_wall_thickness._value)

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
        if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
            template_second_diam = 126
        return (template_first_diam, template_second_diam)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_with(self), 'Выбор компоновки шаблонов')


class TemplateKrs(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        print(f'дочерний класс TemplateKRS')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

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
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        self.buttonAddString = QPushButton('Добавить интервалы скреперования')
        self.buttonAddString.clicked.connect(self.addString)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

    def addRowTable(self):

        roof_skm = self.tabWidget.currentWidget().roof_skm_line.text().replace(',', '.')
        sole_skm = self.tabWidget.currentWidget().sole_skm_line.text().replace(',', '.')
        if not roof_skm or not sole_skm:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if CreatePZ.current_bottom < float(sole_skm):
            msg = QMessageBox.information(self, 'Внимание', f'глубина НЭК ниже глубины нахождения '
                                                            f'СКМ {CreatePZ.skm_depth}')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_skm))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_skm))

        self.tableWidget.setSortingEnabled(False)

    def addString(self):

        from work_py.advanted_file import skm_interval
        template = self.tabWidget.currentWidget().template_Combo.currentText()

        skm_interval = skm_interval(self, template)
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

        # except:
        #     mes = QMessageBox.warning(self, 'Ошибка', 'Данные введены не корректно')
        #     self.addString()

    def addWork(self):

        template_str = str(self.tabWidget.currentWidget().template_str_Edit.text())
        template_key = str(self.tabWidget.currentWidget().template_Combo.currentText())

        if CreatePZ.column_additional is False or (
                CreatePZ.column_additional is True and float(
            CreatePZ.head_column_additional._value) >= CreatePZ.current_bottom):
            template_diametr = int(self.tabWidget.currentWidget().template_second_Edit.text())
        else:
            template_diametr = int(self.tabWidget.currentWidget().template_first_Edit.text())
        # print(f'проблема ЭК {CreatePZ.problem_with_ek_diametr}')
        if (template_diametr >= int(CreatePZ.problem_with_ek_diametr._value) - 2
            and CreatePZ.template_depth > int(CreatePZ.problem_with_ek_depth)):
            mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'шаблон спускается ниже глубины не прохода')

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

        # skm_list = self.SkmColumn(skm_tuple)
        skm_list = sorted(skm_tuple, key = lambda x: x[0])
        work_template_list = self.template_ek(template_str, template_key, template_diametr, skm_list)

        CreatePZ.pause = False
        self.close()
        # print(f'в {work_template_list}')
        return work_template_list

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)


    def well_volume(self):
        from open_pz import CreatePZ

        if not CreatePZ.column_additional:

            volume_well = 3.14 * (CreatePZ.column_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000000 * (
                CreatePZ.current_bottom)
            return volume_well
        else:
            volume_well = (3.14 * (
                    CreatePZ.column_additional_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                   CreatePZ.current_bottom - float(CreatePZ.head_column_additional._value)) / 1000) + (
                                  3.14 * (
                                      CreatePZ.column_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                      CreatePZ.head_column_additional._value) / 1000)
            return volume_well



    def template_ek(self, template_str, template_key, template_diametr, skm_list):
        from open_pz import CreatePZ
        from work_py.advanted_file import raid

        skm_interval = raid(skm_list)

        list_template_ek = [
            [f'СПО  {template_str} на 'f'НКТ{CreatePZ.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{CreatePZ.nkt_diam}мм  с замером, шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1.2)],
            [f'Произвести скреперование э/к в интервале {skm_interval}м Допустить низ НКТ до гл. {CreatePZ.current_bottom}м',
             None,
             f'Произвести скреперование э/к в интервале {skm_interval}м обратной промывкой и проработкой 5 раз каждого '
             'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
             f'представителя Заказчика. Допустить низ НКТ до гл. {CreatePZ.current_bottom}м, шаблон '
             f'до глубины {CreatePZ.template_depth}м. Составить акт. \n'
             '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель УСРСиСТ', round(0.012 * 90 * 1.04 + 1.02 + 0.77, 2)],
            [f'Очистить колонну от АСПО растворителем - 2м3', None,
             f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
             f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
             f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
             f'в объеме {round(3 * CreatePZ.current_bottom / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [f'Промывка скважину уд.весом {CreatePZ.fluid_work_short} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе '
                f'жидкости 6-8 л/сек '
                f'в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ '
                f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure._value}АТМ, '
                f'ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', well_volume_norm(TemplateKrs.well_volume(self) * 1.5)],
            [None, None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None,
             None, None,
             'Мастер КРС', None],
            [f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч', None,
             f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {template_str} на НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1.2)]
        ]

        notes_list = [
            [None, None,
           f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={template_diametr}мм предусмотреть СПО забойного '
           f'двигателя с райбером d={template_diametr + 1}мм, {template_diametr - 1}мм, {template_diametr - 3}мм, '
           f'{template_diametr - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
           f'гл.{CreatePZ.current_bottom}м с последующим СПО шаблона {template_diametr}мм на ТНКТ под промывку '
           f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {template_diametr}мм) '
           f'на ТНКТ с гл. {CreatePZ.current_bottom}м вести с доливом скважины до устья т/ж '
           f'удел.весом {CreatePZ.fluid_work} в '
           f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 ',
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
           f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{CreatePZ.current_bottom}м '
           f'вести с доливом '
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме '
           f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
           None, None, None, None, None, None, None, 'Мастер КРС',
           None],
          [None, None,
           f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию '
           f'№2 произвести '
           f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.'
           f'{CreatePZ.current_bottom}м вести с '
           f'доливом скважины до устья т/ж удел.весом с доливом c'
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме '
           f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
           None, None, None, None, None, None, None, 'Мастер КРС', None],
          [None, None,
           f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 '
           f'до планового '
           f'текущего забоя обратной циркуляцией. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке '
           f'КОТ-50 произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
           f'на ТНКТ с гл.{CreatePZ.current_bottom}м'
           f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в '
           f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
           None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
          [None, None,
           f'Примечание №5: В случае необходимости по результатам восстановления проходимости '
           f'экплуатационной колонны '
           f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
           f'проходимость. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
           f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме '
           f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
           None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

        privyazka_nkt = [f'Привязка по ГК и ЛМ По привязому НКТ удостовериться в наличии текущего забоя', None,
                         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис".'
                         f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                         f' По привязому НКТ удостовериться в наличии '
                         f'текущего забоя с плановым, при необходимости нормализовать '
                         f'забой обратной промывкой тех жидкостью '
                         f'уд.весом {CreatePZ.fluid_work}   до глубины {CreatePZ.current_bottom}м',
                         None, None, None, None, None, None, None, 'Мастер КРС', None, None]
        if CreatePZ.current_bottom - CreatePZ.perforation_sole <= 10 and CreatePZ.open_trunk_well is False:
            privyazka_question = QMessageBox.question(self, 'Привязка оборудования',
                                                      f'зумпф составляет {int(CreatePZ.current_bottom - CreatePZ.perforation_sole)}м '
                                                      f'нужно ли привязывать компоновку?'
                                                      )
            if privyazka_question == QMessageBox.StandardButton.Yes:
                list_template_ek.insert(-1, privyazka_nkt)

        if float(CreatePZ.static_level._value) > 700:
            kot_question = QMessageBox.question(self, 'Низкий Статический уровень', 'Нужно ли произвести СПО '
                                                                                    'обратных клапанов перед ПСШ?')
            if kot_question == QMessageBox.StandardButton.Yes:
                # print(f'Нужно вставить коты')
                for row in kot_work(self, CreatePZ.current_bottom)[::-1]:
                    list_template_ek.insert(0, row)

        if CreatePZ.gipsInWell is True:  # Добавление работ при наличии Гипсово-солевых отложений
            gips = TemplateKrs.pero(self)
            for row in gips[::-1]:
                list_template_ek.insert(0, row)
        print(f'счет использования шаблн {CreatePZ.count_template}')
        if CreatePZ.count_template == 0:
            list_template_ek = list_template_ek + notes_list
        #     CreatePZ.count_template += 1
        # else:
        #     list_template_ek = list_template_ek
        #     list_template_ek.pop(2)

        return list_template_ek

    def pero(self):
        from work_py.rir import RirWindow
        from open_pz import CreatePZ
        from work_py.drilling import Drill_window

        pero_list = RirWindow.pero_select(self, CreatePZ.current_bottom)

        gipsPero_list = [
            [f'Спустить {pero_list}  на тНКТ{CreatePZ.nkt_diam}мм', None,
             f'Спустить {pero_list}  на тНКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м '
             f'с замером, шаблонированием шаблоном {CreatePZ.nkt_template}мм. Опрессовать НКТ на 150атм. Вымыть шар. \n'
             f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [
                f'Промывка уд.весом {CreatePZ.fluid_work_short} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости '
                f'6-8 л/сек в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ '
                f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure._value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
                f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             round(
                 CreatePZ.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * CreatePZ.current_bottom / 9.5 + 0.17 + 0.5,
                 2)],
            [None, None,
             f'В случае недохождения пера до текущего забоя работы продолжить:',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             None]
        ]
        if CreatePZ.gipsInWell is True:

            if CreatePZ.dict_pump_SHGN["do"] != 0:

                gipsPero_list = [gipsPero_list[-1]]
                from work_py.drilling import Drill_window
                drill_work_list = Drill_window.addWork()


                for row in drill_work_list:
                    gipsPero_list.append(row)
            else:
                if self.raid_window is None:
                    self.raid_window = Drill_window(self.table_widget, self.ins_ind)
                    self.raid_window.setGeometry(200, 400, 300, 400)
                    self.raid_window.show()
                    drill_work_list = self.raid_window.addWork()
                    self.raid_window = None
                else:
                    self.raid_window.close()  # Close window.
                    self.raid_window = None
                for row in drill_work_list:
                    gipsPero_list.append(row)

        return gipsPero_list


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = TemplateKrs()
    window.show()
    app.exec_()