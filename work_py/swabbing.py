from collections import namedtuple

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, \
    QLineEdit, QGridLayout, \
    QPushButton, QApplication, QTableWidget, QTableWidgetItem

import data_list
from H2S import calv_h2s

from work_py.alone_oreration import well_volume

from work_py.change_fluid import Change_fluid_Window

from work_py.alone_oreration import need_h2s
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from work_py.template_work import TabPageSoWith
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPageSoSwab(TabPageUnion):
    def __init__(self, tableWidget, parent=None):
        from work_py.acid_paker import CheckableComboBox
        super().__init__(parent)
        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0.87, 1.65, 2)
        self.swab_true_label_type = QLabel("компоновка", self)
        self.swab_true_edit_type = QComboBox(self)
        self.tableWidget = tableWidget
        paker_layout_list = ['двухпакерная', 'однопакерная',
                             'воронка', 'пакер с заглушкой', 'Опрессовка снижением уровня на шаблоне',
                             'Опрессовка снижением уровня на пакере с заглушкой']
        self.swab_true_edit_type.addItems(paker_layout_list)

        self.swab_true_edit_type.setCurrentIndex(3)

        self.depth_gauge_label = QLabel("глубинные манометры", self)
        self.depth_gauge_combo = QComboBox(self)
        self.depth_gauge_combo.addItems(['Нет', 'Да'])

        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.pakerLabel = QLabel("глубина пакера", self)
        self.pakerEdit = QLineEdit(self)
        self.pakerEdit.setValidator(self.validator_int)

        self.paker2Label = QLabel("глубина верхнего пакера", self)
        self.paker2Edit = QLineEdit(self)
        self.paker2Edit.setValidator(self.validator_int)

        if self.data_well:
            if (self.data_well.perforation_roof - 40) < self.data_well.current_bottom:
                self.pakerEdit.setText(f'{int(self.data_well.perforation_roof - 40)}')
            else:
                self.pakerEdit.setText(f'{int(self.data_well.current_bottom - 40)}')

            if (self.data_well.perforation_roof - 40) < self.data_well.current_bottom:
                self.paker2Edit.setText(f'{int(self.data_well.perforation_roof - 40)}')
            else:
                self.pakerEdit.setText(f'{int(self.data_well.current_bottom - 40)}')

        self.kvost_label = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)
        self.khvostEdit.setValidator(self.validator_int)
        self.khvostEdit.setText(str(10))
        self.khvostEdit.setClearButtonEnabled(True)

        plast_work = ['']
        if self.data_well:
            plast_work.extend(self.data_well.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.swab_type_label = QLabel("задача при освоении", self)
        self.swab_type_combo = QComboBox(self)
        self.swab_type_combo.addItems(['', 'Задача №2.1.13', 'Задача №2.1.14', 'Задача №2.1.16', 'Задача №2.1.11',
                                       'Задача №2.1.16 + герметичность пакера', 'ГРР'
                                                                                'своя задача'])
        self.swab_type_combo.setCurrentIndex(data_list.swab_type_comboIndex)

        self.swab_volume_editLabel = QLabel("объем освоения", self)
        self.swab_volume_edit = QLineEdit(self)
        self.swab_volume_edit.setValidator(self.validator_int)
        if self.data_well:
            if self.data_well.region in ['КГМ', 'АГМ']:
                self.swab_type_combo.setCurrentIndex(3)
                self.swab_volume_edit.setText('20')
            else:
                self.swab_type_combo.setCurrentIndex(1)
                self.swab_volume_edit.setText('25')

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)
        self.pressure_new_label = QLabel('Ожидаемое давление', self)
        self.pressure_new_edit = QLineEdit(self)
        self.pressure_new_edit.setValidator(self.validator_int)
        if self.data_well:
            if len(self.data_well.plast_project) != 0:
                self.plast_new_label = QLabel('индекс нового пласта', self)
                self.plast_new_combo = QComboBox(self)
                self.plast_new_combo.addItems(self.data_well.plast_project)
            else:
                self.plast_new_label = QLabel('индекс нового пласта', self)
                self.plast_new_combo = QLineEdit(self)

        self.paker_depth_zumpf_label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator_int)

        self.pressure_zumpf_question_label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressure_zumpf_question_combo = QComboBox(self)
        self.pressure_zumpf_question_combo.addItems(['Нет', 'Да'])

        self.swab_true_edit_type.currentTextChanged.connect(self.swabTrueEdit_select)

        # self.grid = QGridLayout(self)
        self.grid.addWidget(self.swab_true_label_type, 0, 0)
        self.grid.addWidget(self.swab_true_edit_type, 1, 0)
        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.diameter_paker_label_type, 0, 2)
        self.grid.addWidget(self.diameter_paker_edit, 1, 2)
        self.grid.addWidget(self.kvost_label, 0, 3)
        self.grid.addWidget(self.khvostEdit, 1, 3)
        self.grid.addWidget(self.pakerLabel, 0, 4)
        self.grid.addWidget(self.pakerEdit, 1, 4)
        self.grid.addWidget(self.paker2Label, 0, 5)
        self.grid.addWidget(self.paker2Edit, 1, 5)

        self.grid.addWidget(self.swab_type_label, 6, 1)
        self.grid.addWidget(self.swab_type_combo, 7, 1)

        self.grid.addWidget(self.swab_volume_editLabel, 6, 2)
        self.grid.addWidget(self.swab_volume_edit, 7, 2)
        self.grid.addWidget(self.depth_gauge_label, 6, 3)
        self.grid.addWidget(self.depth_gauge_combo, 7, 3)
        self.grid.addWidget(self.pressure_zumpf_question_label, 0, 6)
        self.grid.addWidget(self.pressure_zumpf_question_combo, 1, 6)
        self.grid.addWidget(self.paker_depth_zumpf_label, 0, 7)
        self.grid.addWidget(self.paker_depth_zumpf_edit, 1, 7)

        self.grid.addWidget(self.need_change_zgs_label, 9, 1)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 1)
        self.diameter_paker_edit.setText('122')
        if self.data_well:
            self.grid.addWidget(self.plast_new_label, 9, 2)
            self.grid.addWidget(self.plast_new_combo, 10, 2)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressure_new_label, 9, 5)
            self.grid.addWidget(self.pressure_new_edit, 10, 5)

            if all(self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                   list(self.data_well.dict_perforation.keys())):
                self.swab_true_edit_type.setCurrentIndex(0)
            else:
                self.swab_true_edit_type.setCurrentIndex(1)
        self.pakerEdit.textChanged.connect(self.update_paker_edit)
        self.paker2Edit.textChanged.connect(self.update_paker_edit)
        self.pakerEdit.textChanged.connect(self.update_paker_diameter)
        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)
        self.need_change_zgs_combo.setCurrentIndex(1)
        self.need_change_zgs_combo.setCurrentIndex(0)
        self.pressure_zumpf_question_combo.currentTextChanged.connect(self.update_paker_need)
        self.pressure_zumpf_question_combo.setCurrentIndex(1)
        self.pressure_zumpf_question_combo.setCurrentIndex(0)

    def update_paker_need(self, index):
        if index == 'Да' and self.data_well:
            if self.data_well:
                if len(self.data_well.plast_work) != 0:
                    paker_depth_zumpf = int(self.data_well.perforation_roof + 10)

                else:
                    if self.data_well.dict_leakiness:
                        paker_depth_zumpf = int(max([float(nek.split('-')[0]) + 10
                                                     for nek in
                                                     self.data_well.dict_leakiness['НЭК']['интервал'].keys()]))
                    else:
                        paker_depth_zumpf = int(self.data_well.perforation_roof + 10)

            self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid.addWidget(self.paker_depth_zumpf_label, 0, 7)
            self.grid.addWidget(self.paker_depth_zumpf_edit, 1, 7)
        elif index == 'Нет':
            self.paker_depth_zumpf_label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)

    def update_change_fluid(self, index):
        if index == 'Да' and self.data_well:

            category_h2s_list_plan = list(
                map(int, [self.data_well.dict_category[plast]['по сероводороду'].category for plast in
                          self.data_well.plast_project if self.data_well.dict_category.get(plast) and
                          self.data_well.dict_category[plast]['отключение'] == 'планируемый']))

            if len(category_h2s_list_plan) == 0:
                self.category_pressure_Label = QLabel('По Рпл')
                self.category_pressure_line_combo = QComboBox(self)
                self.category_pressure_line_combo.addItems(['1', '2', '3'])
                self.category_h2s_Label = QLabel('По H2S')
                self.category_h2s_edit = QComboBox(self)
                self.category_h2s_edit.addItems(['2', '1', '3'])
                self.h2s_pr_label = QLabel('значение H2s в %')
                self.h2s_pr_edit = QLineEdit(self)
                self.h2s_pr_edit.setValidator(self.validator_float)
                self.h2s_mg_label = QLabel('значение H2s в мг/л')
                self.h2s_mg_edit = QLineEdit(self)
                self.h2s_mg_edit.setValidator(self.validator_float)
                self.category_Label = QLabel('По газовому фактору')
                self.category_gf = QComboBox(self)
                self.category_gf.addItems(['2', '1', '3'])
                self.gf_label = QLabel('Газовый фактор')
                self.gf_edit = QLineEdit(self)
                self.gf_edit.setValidator(self.validator_float)
                self.h2s_mg_edit.textChanged.connect(self.update_calculate_h2s)
                self.h2s_pr_edit.textChanged.connect(self.update_calculate_h2s)
                self.gf_edit.textChanged.connect(self.update_calculate_h2s)

                self.calc_h2s_Label = QLabel('расчет поглотителя H2S по вскрываемому пласту')
                self.calc_plast_h2s = QLineEdit(self)

                self.grid.addWidget(self.category_pressure_Label, 11, 2)
                self.grid.addWidget(self.category_pressure_line_combo, 12, 2)

                self.grid.addWidget(self.category_h2s_Label, 11, 3)
                self.grid.addWidget(self.category_h2s_edit, 12, 3)

                self.grid.addWidget(self.h2s_pr_label, 13, 3)
                self.grid.addWidget(self.h2s_pr_edit, 14, 3)

                self.grid.addWidget(self.h2s_mg_label, 15, 3)
                self.grid.addWidget(self.h2s_mg_edit, 16, 3)

                self.grid.addWidget(self.category_Label, 11, 4)
                self.grid.addWidget(self.category_gf, 12, 4)

                self.grid.addWidget(self.gf_label, 13, 4)
                self.grid.addWidget(self.gf_edit, 14, 4)

                self.grid.addWidget(self.calc_h2s_Label, 11, 5)
                self.grid.addWidget(self.calc_plast_h2s, 12, 5)

            if len(self.data_well.plast_project) != 0:
                # self.plast_new_combo = QComboBox(self)
                self.plast_new_combo.addItems(self.data_well.plast_project)
                plast = self.plast_new_combo.currentText()
            else:
                # self.plast_new_combo = QLineEdit(self)
                plast = self.plast_new_combo.text()

            if len(category_h2s_list_plan) != 0:
                self.pressure_new_edit.setText(
                    f'{self.data_well.dict_category[plast]["по давлению"].data_pressure}')

            self.grid.addWidget(self.plast_new_label, 9, 2)
            self.grid.addWidget(self.plast_new_combo, 10, 2)

            self.grid.addWidget(self.fluid_new_label, 9, 3)
            self.grid.addWidget(self.fluid_new_edit, 10, 3)

            self.grid.addWidget(self.pressure_new_label, 9, 4)
            self.grid.addWidget(self.pressure_new_edit, 10, 4)
        else:
            try:
                self.category_pressure_Label.setParent(None)
                self.category_pressure_line_combo.setParent(None)

                self.category_h2s_Label.setParent(None)
                self.category_h2s_edit.setParent(None)

                self.h2s_pr_label.setParent(None)
                self.h2s_pr_edit.setParent(None)

                self.h2s_mg_label.setParent(None)
                self.h2s_mg_edit.setParent(None)

                self.category_Label.setParent(None)
                self.category_gf.setParent(None)
                self.calc_plast_h2s.setParent(None)

                self.gf_label.setParent(None)
                self.gf_edit.setParent(None)

                self.calc_h2s_Label.setParent(None)

                self.plast_new_label.setParent(None)
                self.plast_new_combo.setParent(None)
                self.fluid_new_label.setParent(None)
                self.fluid_new_edit.setParent(None)
                self.pressure_new_label.setParent(None)
                self.pressure_new_edit.setParent(None)
            except Exception:
                pass

    def update_calculate_h2s(self):
        if self.category_h2s_edit.currentText() in ['3', 3]:
            self.calc_plast_h2s.setText('0')
        else:
            if self.h2s_mg_edit.text() != '' and self.h2s_pr_edit.text() != '':
                self.calc_plast_h2s.setText(str(calv_h2s(self, self.category_h2s_edit.currentText(),
                                                         float(self.h2s_mg_edit.text().replace(',', '.')),
                                                         float(self.h2s_pr_edit.text().replace(',', '.')))))

    def update_paker_edit(self):
        dict_perforation = self.data_well.dict_perforation
        rows = self.tableWidget.rowCount()
        plasts = data_list.texts
        # print(plasts)
        roof_plast = self.data_well.current_bottom
        sole_plast = 0
        for plast in self.data_well.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']

        paker_depth = self.pakerEdit.text()

        if self.swab_true_edit_type.currentText() not in ['однопакерная']:
            self.pressure_zumpf_question_label.setParent(None)
            self.pressure_zumpf_question_combo.setParent(None)
        else:
            self.grid.addWidget(self.pressure_zumpf_question_label, 2, 8)
            self.grid.addWidget(self.pressure_zumpf_question_combo, 3, 8)

        if self.swab_true_edit_type.currentText() in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
            if paker_depth != '' and rows == 0:
                self.khvostEdit.setText(str(10))

            if rows == 0:
                if paker_depth != '' and self.khvostEdit.text() != '':
                    self.distance_between_packers_voronka = int(self.khvostEdit.text())
            else:
                self.khvostEdit.setEnabled(False)
                if self.khvostEdit != '':
                    self.khvostEdit.setText(f'{self.distance_between_packers_voronka}')
        elif self.swab_true_edit_type.currentText() in ['двухпакерная', 'двухпакерная, упорные']:
            if rows == 0:
                if paker_depth != '':
                    self.khvostEdit.setText(f'{10}')

                    if self.swab_true_edit_type.currentText() == 'двухпакерная, упорные':
                        self.khvostEdit.setText(str(int(self.data_well.current_bottom - int(paker_depth))))

                if self.pakerEdit.text() != '' and self.paker2Edit.text() != '':
                    self.distance_between_packers = abs(int(self.pakerEdit.text()) - int(self.paker2Edit.text()))

                    # print(f' расстояние между пакерами {self.distance_between_packers}')
            else:
                self.khvostEdit.setEnabled(False)
                self.paker2Edit.setEnabled(False)
                if self.pakerEdit.text() != '':
                    self.paker2Edit.setText(f'{int(self.pakerEdit.text()) - self.distance_between_packers}')

        elif self.swab_true_edit_type.currentText() in ['воронка']:
            self.khvostEdit.setText(f'{sole_plast}')

    def update_paker_diameter(self):
        from .opressovka import TabPageSo
        paker_depth = self.pakerEdit.text()
        if paker_depth:
            paker_diameter = int(self.paker_diameter_select(paker_depth))
            self.diameter_paker_edit.setText(str(int(paker_diameter)))

    def swabTrueEdit_select(self):

        if self.swab_true_edit_type.currentText() == 'однопакерная':
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "вид освоения", "объем освоения"]
            self.pakerLabel.setText('Глубина пакера')
            self.grid.addWidget(self.plast_label, 0, 1)
            self.grid.addWidget(self.plast_combo, 1, 1)
            self.grid.addWidget(self.kvost_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diameter_paker_label_type, 0, 2)
            self.grid.addWidget(self.diameter_paker_edit, 1, 2)



        elif self.swab_true_edit_type.currentText() == 'двухпакерная':
            self.pakerLabel.setText('Глубина нижнего пакера')
            self.grid.addWidget(self.kvost_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.plast_label, 0, 1)
            self.grid.addWidget(self.plast_combo, 1, 1)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)
            self.grid.addWidget(self.diameter_paker_label_type, 0, 2)
            self.grid.addWidget(self.diameter_paker_edit, 1, 2)

            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "2-й пакер", "вид освоения", "объем освоения"]

        elif self.swab_true_edit_type.currentText() == 'воронка':

            self.pakerLabel.setText('Глубина воронки')
            self.kvost_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            self.diameter_paker_label_type.setParent(None)
            self.diameter_paker_edit.setParent(None)

            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)

            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressure_new_label.setParent(None)
            self.pressure_new_edit.setParent(None)
            paker_layout_list_tab = ["Пласт", "воронка", "вид освоения", "объем освоения"]

        elif self.swab_true_edit_type.currentText() == 'пакер с заглушкой':
            # self.swab_type_label.setParent(None)
            # self.swab_type_combo.setParent(None)
            # self.swab_volume_edit.setParent(None)

            self.kvost_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.pakerLabel.setParent(None)
            self.pakerEdit.setParent(None)

            self.diameter_paker_label_type.setParent(None)
            self.diameter_paker_edit.setParent(None)
            # self.pakerLabel.setText('Глубина пакера')
            # self.paker2Label.setText('Глубина понижения')
            self.paker2Edit.setText(f'{self.data_well.perforation_roof + 10}')
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)

            self.grid.addWidget(self.kvost_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diameter_paker_label_type, 0, 2)
            self.grid.addWidget(self.diameter_paker_edit, 1, 2)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "вид освоения", "объем освоения"]
        elif self.swab_true_edit_type.currentText() == 'Опрессовка снижением уровня на шаблоне':
            self.depth_gauge_label.setParent(None)
            self.depth_gauge_combo.setParent(None)
            self.swab_volume_editLabel.setParent(None)
            self.swab_type_label.setParent(None)
            self.swab_type_combo.setParent(None)
            self.swab_volume_edit.setParent(None)
            self.plast_label.setParent(None)
            self.plast_combo.setParent(None)
            self.kvost_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.pakerLabel.setParent(None)
            self.pakerEdit.setParent(None)
            self.diameter_paker_label_type.setParent(None)
            self.diameter_paker_edit.setParent(None)
            self.paker2Label.setText('Глубина Понижения уровня')
            depth_swab = int(float(self.data_well.current_bottom - 250))
            if depth_swab > 1500:
                depth_swab = 1500
            self.paker2Edit.setText(f'{depth_swab}')
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)

            self.grid.addWidget(self.plast_new_label, 9, 2)
            self.grid.addWidget(self.plast_new_combo, 10, 2)

            self.grid.addWidget(self.fluid_new_label, 9, 3)
            self.grid.addWidget(self.fluid_new_edit, 10, 3)

            self.grid.addWidget(self.pressure_new_label, 9, 4)
            self.grid.addWidget(self.pressure_new_edit, 10, 4)

            paker_layout_list_tab = ["забой", "глубина понижения", "вид освоения"]

            first_template, template_second = TabPageSoWith.template_diam_ek(self)
            self.template_second_need_label = QLabel('Необходимость шаблонов в компоновке')
            self.template_second_need_combo = QComboBox(self)
            self.template_second_need_combo.addItems(['Да', 'Нет'])
            self.template_second_Label = QLabel("диаметр шаблона", self)
            self.template_second_edit = QLineEdit(self)
            self.template_second_edit.setValidator(self.validator_int)
            self.template_second_edit.setText(str(template_second))

            self.length_template_second_Label = QLabel("длина шаблона", self)
            self.length_template_second_edit = QLineEdit(self)
            self.length_template_second_edit.setValidator(self.validator_int)
            self.length_template_second_edit.setText('4')

            self.grid.addWidget(self.template_second_need_label, 3, 2)
            self.grid.addWidget(self.template_second_need_combo, 4, 2)

            self.grid.addWidget(self.template_second_Label, 3, 3)
            self.grid.addWidget(self.template_second_edit, 4, 3)

            self.grid.addWidget(self.length_template_second_Label, 3, 4)
            self.grid.addWidget(self.length_template_second_edit, 4, 4)


        elif self.swab_true_edit_type.currentText() == 'Опрессовка снижением уровня на пакере с заглушкой':
            self.paker2Label.setText('Глубина Понижения уровня')
            self.paker2Edit.setText(f'{self.data_well.current_bottom - 250}')
            self.grid.addWidget(self.kvost_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diameter_paker_label_type, 0, 2)
            self.grid.addWidget(self.diameter_paker_edit, 1, 2)
            paker_layout_list_tab = ["забой", "хвост", "посадка пакера", "глубина понижения"]
            self.need_change_zgs_combo.setCurrentIndex(1)
            self.need_change_zgs_combo.setCurrentIndex(0)
        self.tableWidget.setHorizontalHeaderLabels([])
        self.tableWidget.setHorizontalHeaderLabels(paker_layout_list_tab)

    def update_plast_edit(self):

        dict_perforation = self.data_well.dict_perforation
        plasts = data_list.texts
        # print(f'пласты {plasts, len(data_list.ptexts), len(plasts), data_list.texts}')
        roof_plast = self.data_well.current_bottom
        sole_plast = 0

        for plast in self.data_well.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:

                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']

        if self.swab_true_edit_type.currentText() in ['однопакерная', 'воронка',
                                                      'Опрессовка снижением уровня на шаблоне']:
            paker_depth = int(roof_plast - 40)
            self.pakerEdit.setText(f"{paker_depth}")
            self.paker2Edit.setText(str(int(paker_depth - 30)))

        else:
            paker_depth = int(sole_plast + 10)
            self.pakerEdit.setText(f"{paker_depth}")
            self.paker2Edit.setText(str(int(roof_plast - 10)))


class TabWidget(TabWidgetUnion):
    def __init__(self, tableWidget, parent=None):
        super().__init__()
        self.addTab(TabPageSoSwab(tableWidget, parent), 'Свабирование')


class SwabWindow(WindowUnion):
    def __init__(self, data_well=None, table_widget=None, parent=None):
        super().__init__(data_well)

        if data_well:
            self.insert_index = data_well.insert_index
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.dict_nkt = {}
        self.table_widget = table_widget
        self.tableWidget = QTableWidget(0, 8)
        self.tabWidget = TabWidget(self.tableWidget, self.data_well)

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonadd_string = QPushButton('Добавить освоение')
        self.buttonadd_string.clicked.connect(self.add_string)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonadd_string, 2, 0)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0, 1, 0)

    def add_string(self):

        swab_true_edit_type = self.tabWidget.currentWidget().swab_true_edit_type.currentText()
        plast_combo = self.tabWidget.currentWidget().plast_combo.combo_box.currentText()
        swab_type_combo = self.tabWidget.currentWidget().swab_type_combo.currentText()
        swab_list = ['', 'Задача №2.1.13', 'Задача №2.1.14', 'Задача №2.1.16', 'Задача №2.1.11',
                     'Задача №2.1.16 + герметичность пакера', 'ГРР'
                                                              'своя задача']

        swab_edit_combo = QComboBox(self)
        swab_edit_combo.addItems(swab_list)
        swab_edit_combo.setCurrentIndex(swab_list.index(swab_type_combo))

        swab_volume_edit = int(float(self.tabWidget.currentWidget().swab_volume_edit.text().replace(',', '.')))

        if (not plast_combo or not swab_volume_edit) and swab_true_edit_type in ['однопакерная', 'пакер с заглушкой',
                                                                                 'воронка', 'двухпакерная']:
            QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        if swab_true_edit_type in ['однопакерная', 'пакер с заглушкой']:
            if rows != 0:
                ques = QMessageBox.question(self, 'ОШИБКА',
                                            'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно, продолжить')
                if ques == QMessageBox.StandardButton.No:
                    return
            paker_khost = self.check_if_none(self.tabWidget.currentWidget().khvostEdit.text())
            paker_depth = self.check_if_none(self.tabWidget.currentWidget().pakerEdit.text())

            if self.data_well.current_bottom < float(paker_khost + paker_depth) or \
                    0 < paker_khost + paker_depth < self.data_well.current_bottom is False:
                QMessageBox.information(self, 'Внимание',
                                        f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                        f'{self.data_well.current_bottom}м')
                return
            if self.check_true_depth_template(paker_depth) is False:
                return
            if self.true_set_paker(paker_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth) is False:
                return

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 3, swab_edit_combo)
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(swab_volume_edit)))


        elif swab_true_edit_type in ['двухпакерная']:
            paker_khost = self.check_if_none(self.tabWidget.currentWidget().khvostEdit.text())
            paker_depth = self.check_if_none(self.tabWidget.currentWidget().pakerEdit.text())
            paker2_depth = self.check_if_none(self.tabWidget.currentWidget().paker2Edit.text())
            if self.check_true_depth_template(paker_depth) is False:
                return
            if self.true_set_paker(paker_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker_depth) is False:
                return
            if self.check_true_depth_template(paker2_depth) is False:
                return
            if self.true_set_paker(paker2_depth) is False:
                return
            if self.check_depth_in_skm_interval(paker2_depth) is False:
                return

            if self.data_well.current_bottom < float(paker_khost + paker2_depth):
                QMessageBox.information(self, 'Внимание',
                                        f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                        f'{self.data_well.current_bottom}м')
                return
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker2_depth)))
            self.tableWidget.setCellWidget(rows, 4, swab_edit_combo)
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(swab_volume_edit)))

        elif swab_true_edit_type in ['воронка']:
            if rows != 0:
                QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
                return
            paker_depth = self.check_if_none(self.tabWidget.currentWidget().pakerEdit.text())

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 2, swab_edit_combo)
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(swab_volume_edit)))

        elif swab_true_edit_type in ['Опрессовка снижением уровня на шаблоне']:

            self.data_well.template_length = \
                float(self.tabWidget.currentWidget().length_template_second_edit.text())
            # self.data_well.template_length_addition = length_template_first
            if rows != 0:
                ques = QMessageBox.question(self, 'ОШИБКА',
                                            'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно, продолжить')
                if ques == QMessageBox.StandardButton.No:
                    return
            paker_opy = self.tabWidget.currentWidget().paker2Edit.text()
            if paker_opy != '':
                paker_opy = int(float(str(paker_opy).replace(',', '.')))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(self.data_well.current_bottom)))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_opy)))

        elif swab_true_edit_type in ['Опрессовка снижением уровня на пакере с заглушкой']:
            paker_depth = self.check_if_none(self.tabWidget.currentWidget().pakerEdit.text())
            paker_khost = self.check_if_none(self.tabWidget.currentWidget().khvostEdit.text())

            if rows != 0:
                QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
            paker_opy = self.tabWidget.currentWidget().paker2Edit.text()
            if paker_opy != '':
                paker_opy = int(float(str(paker_opy).replace(',', '.')))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(self.data_well.current_bottom)))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker_opy)))

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def add_work(self):
        from work_py.acid_paker import AcidPakerWindow
        try:
            diameter_paker = int(float(self.tabWidget.currentWidget().diameter_paker_edit.text()))
            swab_true_edit_type = self.tabWidget.currentWidget().swab_true_edit_type.currentText()
            need_change_zgs_combo = self.tabWidget.currentWidget().need_change_zgs_combo.currentText()
            depth_gauge_combo = self.tabWidget.currentWidget().depth_gauge_combo.currentText()
            paker_depth_zumpf = ''
            pressure_zumph_combo = self.tabWidget.currentWidget().pressure_zumpf_question_combo.currentText()

            if pressure_zumph_combo == 'Да':
                paker_khost = self.check_if_none(self.tabWidget.currentWidget().khvostEdit.text())
                paker_depth_zumpf = int(float(self.tabWidget.currentWidget().paker_depth_zumpf_edit.text()))
                if paker_depth_zumpf == '':
                    QMessageBox.warning(self, 'Ошибка', f'не введены глубина опрессовки ЗУМПФа')
                    return
                else:
                    paker_depth_zumpf = int(float(paker_depth_zumpf))
                if paker_khost + paker_depth_zumpf >= self.data_well.current_bottom:
                    QMessageBox.warning(self, 'ОШИБКА', 'Длина хвостовика и пакера ниже текущего забоя')
                    return

                if self.check_true_depth_template(paker_depth_zumpf) is False:
                    return
                if self.true_set_paker(paker_depth_zumpf) is False:
                    return
                if self.check_depth_in_skm_interval(paker_depth_zumpf) is False:
                    return

            rows = self.tableWidget.rowCount()
            if need_change_zgs_combo == 'Да':
                if len(self.data_well.plast_project) != 0:
                    plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
                else:
                    plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()

                fluid_new_edit = self.tabWidget.currentWidget().fluid_new_edit.text()
                if fluid_new_edit != '':
                    fluid_new_edit = float(fluid_new_edit.replace(',', '.'))
                pressure_new_edit = self.tabWidget.currentWidget().pressure_new_edit.text()

                if pressure_new_edit != '':
                    pressure_new_edit = int(float(pressure_new_edit.replace(',', '.')))

                if self.data_well.dict_category[plast_new_combo]['отключение'] != 'планируемый':
                    h2s_pr_edit = self.tabWidget.currentWidget().h2s_pr_edit.text()
                    h2s_mg_edit = self.tabWidget.currentWidget().h2s_mg_edit.text()
                    gf_edit = self.tabWidget.currentWidget().gf_edit.text()
                    calc_plast_h2s = self.tabWidget.currentWidget().calc_plast_h2s.text()
                    if h2s_pr_edit != '' and h2s_mg_edit and gf_edit != '' and calc_plast_h2s != '' and pressure_new_edit != '':

                        asdwd = self.data_well.dict_category

                        pressure = namedtuple("pressure", "category data_pressure")
                        Data_h2s = namedtuple("Data_h2s", "category data_percent data_mg_l poglot")
                        Data_gaz = namedtuple("Data_gaz", "category data")

                        category_pressure_line_combo = self.tabWidget.currentWidget().category_pressure_line_combo.currentText()
                        category_h2s_edit = self.tabWidget.currentWidget().category_h2s_edit.currentText()

                        self.category_gf = self.tabWidget.currentWidget().category_gf.currentText()

                        self.data_well.dict_category.setdefault(plast_new_combo, {}).setdefault(
                            'по давлению',
                            pressure(int(float(category_pressure_line_combo)),
                                     float(pressure_new_edit)))

                        self.data_well.dict_category.setdefault(plast_new_combo, {}).setdefault(
                            'по сероводороду', Data_h2s(
                                int(float(category_h2s_edit)),
                                float(h2s_pr_edit.replace(',', '.')),
                                float(h2s_mg_edit.replace(',', '.')),
                                float(calc_plast_h2s.replace(',', '.'))))

                        self.data_well.dict_category.setdefault(plast_new_combo, {}).setdefault(
                            'по газовому фактору', Data_gaz(
                                int(self.data_well.category_gas_factor),
                                float(gf_edit)))
                        try:
                            self.data_well.dict_category[plast_new_combo]['отключение'] = 'планируемый'
                        except Exception:
                            self.data_well.dict_category.setdefault(plast_new_combo, {}).setdefault(
                                'отключение', 'планируемый')

            else:
                plast_new_combo = ''
                fluid_new_edit = ''
                pressure_new_edit = ''
        except Exception as e:
            mes = QMessageBox.critical(self, 'Ошибка', f'Введены не все параметры {type(e).__name__}\n\n{str(e)}')
            return
        if need_change_zgs_combo == 'Да':
            if (plast_new_combo == '' or fluid_new_edit == '' or pressure_new_edit == ''):
                mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return

        for row in range(rows):
            if swab_true_edit_type in ['двухпакерная', 'двухпакерная, упорные']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                swab_type_combo = self.tableWidget.cellWidget(row, 4).currentText()
                swab_volume_edit = int(float(self.tableWidget.item(row, 5).text()))
                if row == 0:
                    work_list = self.swabbing_with_2paker(diameter_paker, paker_depth, paker2_depth, paker_khost,
                                                          plast_combo, swab_type_combo, swab_volume_edit,
                                                          depth_gauge_combo,
                                                          need_change_zgs_combo,
                                                          plast_new_combo, fluid_new_edit, pressure_new_edit)
                elif rows == row + 1:
                    work_list = work_list[:-1]
                    work_list.extend(self.swabbing_with_2paker(diameter_paker, paker_depth, paker2_depth, paker_khost,
                                                               plast_combo, swab_type_combo, swab_volume_edit,
                                                               depth_gauge_combo,
                                                               need_change_zgs_combo,
                                                               plast_new_combo, fluid_new_edit, pressure_new_edit)[1:])
                else:
                    work_list = work_list[:-1]
                    work_list.extend(self.swabbing_with_2paker(diameter_paker, paker_depth, paker2_depth, paker_khost,
                                                               plast_combo, swab_type_combo, swab_volume_edit,
                                                               depth_gauge_combo,
                                                               need_change_zgs_combo,
                                                               plast_new_combo, fluid_new_edit, pressure_new_edit)[1:9])

            elif swab_true_edit_type in ['однопакерная']:

                plast_combo = self.tableWidget.item(row, 0).text()

                # if rows == row + 1:
                paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                if paker_khost < 0:
                    QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                    return
                    data_list.paker_khost = paker_khost
                # else:
                #     paker_khost = data_list.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                swab_type_combo = self.tableWidget.cellWidget(row, 3).currentText()
                swab_volume_edit = int(float(self.tableWidget.item(row, 4).text()))

                for plast in plast_combo.split(','):
                    if plast in self.data_well.plast_work:
                        if abs(paker_khost + paker_depth - self.data_well.dict_perforation[plast]['кровля']) < 20:
                            mes = QMessageBox.question(self, 'Вопрос',
                                                       f'Расстояние между низом компоновки'
                                                       f' {paker_khost + paker_depth} '
                                                       f'и кровлей ПВР меньше 20м '
                                                       f'{self.data_well.dict_perforation[plast]["кровля"]},'
                                                       f' Продолжить?')

                            if mes == QMessageBox.StandardButton.No:
                                return

                if row == 0:
                    work_list = self.swabbing_with_paker(diameter_paker, paker_depth, paker_khost, plast_combo,
                                                         swab_type_combo, swab_volume_edit, depth_gauge_combo,
                                                         need_change_zgs_combo,
                                                         plast_new_combo, fluid_new_edit, pressure_new_edit,
                                                         pressure_zumph_combo, paker_depth_zumpf)
                elif row > 0:
                    work_list = work_list[:-2]
                    swab_list = self.swabbing_with_paker(diameter_paker, paker_depth, paker_khost, plast_combo,
                                                         swab_type_combo, swab_volume_edit, depth_gauge_combo,
                                                         need_change_zgs_combo,
                                                         plast_new_combo, fluid_new_edit, pressure_new_edit)[
                                1:]
                    work_list.extend(swab_list)



            elif swab_true_edit_type == 'воронка':
                plast_combo = self.tableWidget.item(row, 0).text()
                paker_depth = int(float(self.tableWidget.item(row, 1).text()))
                swab_type_combo = self.tableWidget.cellWidget(row, 2).currentText()
                swab_volume_edit = int(float(self.tableWidget.item(row, 3).text()))

                work_list = self.swabbing_with_voronka(paker_depth, plast_combo, swab_type_combo,
                                                       swab_volume_edit, depth_gauge_combo, need_change_zgs_combo,
                                                       plast_new_combo, fluid_new_edit, pressure_new_edit)

            elif swab_true_edit_type == 'пакер с заглушкой':
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    data_list.paker_khost = paker_khost
                else:
                    paker_khost = data_list.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                swab_type_combo = self.tableWidget.cellWidget(row, 3).currentText()
                swab_volume_edit = int(float(self.tableWidget.item(row, 4).text()))

                work_list = self.swabbing_with_paker_stub(diameter_paker, paker_depth, paker_khost, plast_combo,
                                                          swab_type_combo, swab_volume_edit, depth_gauge_combo,
                                                          need_change_zgs_combo,
                                                          plast_new_combo, fluid_new_edit, pressure_new_edit)
            elif swab_true_edit_type == 'Опрессовка снижением уровня на шаблоне':
                template_second_need_combo = self.tabWidget.currentWidget().template_second_need_combo.currentText()
                if need_change_zgs_combo == 'Да':
                    category_h2s_list_plan = list(
                        map(int, [self.data_well.dict_category[plast]['по сероводороду'].category for plast in
                                  self.data_well.plast_project if self.data_well.dict_category.get(plast) and
                                  self.data_well.dict_category[plast]['отключение'] == 'планируемый']))

                    if len(category_h2s_list_plan) == 0:
                        gf_edit = self.tabWidget.currentWidget().gf_edit.text()
                        calc_plast_h2s = self.tabWidget.currentWidget().calc_plast_h2s.text()
                        if gf_edit == '' or calc_plast_h2s == '':
                            QMessageBox.warning(self, 'Ошибка',
                                                'Не введены данные для расчета поглотителя сероводорода')
                            return

                template_second_edit = self.tabWidget.currentWidget().template_second_edit.text()
                length_template_second_edit = self.tabWidget.currentWidget().length_template_second_edit.text()

                paker2_depth = int(float(self.tableWidget.item(row, 1).text()))
                work_list = self.swabbing_opy(
                    paker2_depth, fluid_new_edit, need_change_zgs_combo,
                    plast_new_combo, pressure_new_edit, template_second_edit, length_template_second_edit,
                    template_second_need_combo)
            elif swab_true_edit_type == 'Опрессовка снижением уровня на пакере с заглушкой':
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                work_list = self.swabbing_opy_with_paker(diameter_paker, paker_khost, paker_depth, paker2_depth)

        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def swabbing_opy_with_paker(self, diameter_paker, paker_khost, paker_depth, depth_opy):
        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'
        if self.check_true_depth_template(paker_depth) is False:
            return
        if self.true_set_paker(paker_depth) is False:
            return
        if self.check_depth_in_skm_interval(paker_depth) is False:
            return
        need_change_zgs_combo = str(self.tabWidget.currentWidget().need_change_zgs_combo.currentText())
        if need_change_zgs_combo == 'Да':
            if len(self.data_well.plast_project) != 0:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
            else:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()
            fluid_new_edit = int(float(self.tabWidget.currentWidget().fluid_new_edit.text()))
            pressure_new_edit = int(float(self.tabWidget.currentWidget().pressure_new_edit.text()))

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and
                self.data_well.column_additional is True \
                and self.data_well.head_column_additional.get_value < depth_opy is True) else '60'])

        if self.data_well.column_additional is False \
                or (self.data_well.column_additional is True and
                    paker_depth < self.data_well.head_column_additional.get_value and
                    self.data_well.head_column_additional.get_value > 800) or \
                (self.data_well.column_additional_diameter.get_value < 110 and
                 paker_depth > self.data_well.head_column_additional.get_value):
            paker_select = f'заглушка +  НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм +' \
                           f' щелевой фильтр НКТ 10м'
            paker_short = f'заглушка  + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм + ' \
                          f'щелевой фильтр НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х' \
                           f' {self.data_well.column_additional_wall_thickness.get_value}мм + щелевой фильтр ' \
                           f'+ НКТ60мм 10м '
            paker_short = f'заглушка+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм  + щелевой фильтр + ' \
                          f'НКТ60мм 10м '
            dict_nkt = {int(nkt_diam): self.data_well.head_column_additional.get_value, 60:
                int(paker_depth - self.data_well.head_column_additional.get_value)}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 \
                and paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'заглушка + НКТ{self.data_well.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм' \
                           f' + щелевой фильтр + НКТ{self.data_well.nkt_diam}мм со снятыми фасками 10м'
            paker_short = f'заглушка + НКТ{self.data_well.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diameter_paker}мм + щелевой фильтр + ' \
                          f'НКТ{self.data_well.nkt_diam}мм ' \
                          f'со снятыми фасками 10м'
            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}

        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м  до глубины {self.data_well.current_bottom}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  до глубины {self.data_well.current_bottom}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1)],
            [f'Посадить пакер на глубину {paker_depth}м', None,
             f'Посадить пакер на глубину {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной '
             f'главным инженером от '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое давление '
             f'опрессовки э/колонны на устье {self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.35],
            [None, None,
             f'Фоновая запись. Произвести  опрессовку колонны снижением уровня свабированием по Задаче №2.1.17 '
             f'Понижение уровня '
             f'до глубины {depth_opy}м, тех отстой 3ч. КВУ в течение 3 часов после тех.отстоя. Интервал времени '
             f'между замерами '
             f'1 час. В случае негерметичности произвести записи по тех карте 2.1.13 с целью определения НЭК',
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 20],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None]]

        fluid_change_quest = QMessageBox.question(self, 'Смена объема',
                                                  'Нужна ли смена удельного веса рабочей жидкости?')
        if fluid_change_quest == QMessageBox.StandardButton.Yes:
            self.data_well.fluid_work, self.data_well.fluid_work_short, plast, expected_pressure = \
                need_h2s(self, fluid_new_edit, plast_new_combo, pressure_new_edit)

            fluid_change_list = [
                [None, None,
                 f'Допустить до {self.data_well.current_bottom}м. Произвести смену объема обратной '
                 f'промывкой по круговой циркуляции  жидкостью  {self.data_well.fluid_work} '
                 f'(по расчету по вскрываемому пласта {plast} Рожид- {expected_pressure}атм) в объеме не '
                 f'менее {round(well_volume(self, self.data_well.current_bottom), 1)}м3  в присутствии '
                 f'представителя заказчика, Составить акт. '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                 f'часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', round(well_volume_norm(well_volume(self, self.data_well.current_bottom))
                                     + descentNKT_norm(self.data_well.current_bottom - depth_opy - 200, 1), 1)],
                [None, None,
                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {self.data_well.current_bottom}м с '
                 f'доливом скважины в '
                 f'объеме {round((self.data_well.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом '
                 f'{self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(self.data_well.current_bottom, 1)]
            ]

            for row in fluid_change_list:
                paker_list.append(row)
        else:
            paker_list.append(
                [None, None,
                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {depth_opy + 200}м с доливом скважины в '
                 f'объеме {round((depth_opy + 200) * 1.12 / 1000, 1)}м3 '
                 f'удельным весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(depth_opy + 200, 1)])
        return paker_list

    def swabbing_opy(self, depth_opy, fluid_new, need_change_zgs_combo, plast_new,
                     pressure_new, template_second, length_template_second, template_second_need_combo):

        template_second_str = ''
        if template_second_need_combo == 'Да':
            template_second_str = f'+ шаблон {template_second}мм L-{length_template_second}'

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and self.data_well.column_additional is True \
                and self.data_well.head_column_additional.get_value < depth_opy is True) else '60'])

        if self.data_well.head_column_additional.get_value < depth_opy + 200 and self.data_well.column_additional:
            nkt_diam = '60'

        if self.data_well.column_additional is False or self.data_well.column_additional is True and \
                self.data_well.current_bottom < self.data_well.head_column_additional.get_value and \
                self.data_well.head_column_additional.get_value > 600:
            paker_select = f'воронку со свабоограничителем {template_second_str} + НКТ{nkt_diam} + НКТ 10м + репер'
            paker_short = f'воронку со с/о  + НКТ{nkt_diam}  + НКТ 10м + репер'
            dict_nkt = {73: depth_opy}
            self.data_well.template_depth = self.data_well.current_bottom

        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:
            paker_select = f'воронку со свабоограничителем {template_second_str} + НКТ60мм 10м + репер +НКТ60мм ' \
                           f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 10, 0)}м'
            paker_short = f'воронку со с/о {template_second_str} + НКТ60мм 10м + репер + НКТ60мм'
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: int(self.data_well.current_bottom - self.data_well.head_column_additional.get_value)}
            self.data_well.template_depth = self.data_well.current_bottom
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:
            paker_select = f'воронку со свабоограничителем {template_second_str} + ' \
                           f'НКТ{self.data_well.nkt_diam}мм ' \
                           f'со снятыми фасками + ' \
                           f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками 10м ' \
                           f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 10, 0)}м'
            paker_short = f'в/у со c/о + шаблон {template_second} L-{length_template_second} + НКТ{self.data_well.nkt_diam}мм ' \
                          f'со снятыми фасками + ' \
                          f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками 10м'
            dict_nkt = {73: depth_opy}
            self.data_well.template_depth_addition = self.data_well.current_bottom
        elif nkt_diam == 60:
            dict_nkt = {60: depth_opy}

        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'

        paker_list = [
            [f'СПО {paker_short}до глубины {self.data_well.current_bottom}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  до глубины {self.data_well.current_bottom}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1)],
            [f'Промыть уд.весом {self.data_well.fluid_work} в объеме '
             f'{round(well_volume(self, self.data_well.current_bottom) * 1.5, 1)}м3', None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work}  при '
             f'расходе жидкости 6-8 л/сек '
             f'в присутствии представителя Заказчика в объеме '
             f'{round(well_volume(self, self.data_well.current_bottom) * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ '
             f'ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: '
             f'0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Нормализовать забой обратной промывкой тех жидкостью уд.весом '
             f'{self.data_well.fluid_work} до глубины {self.data_well.current_bottom}м.', None, None, None, None, None,
             None, None,
             'Мастер КРС', None],
            [f'Приподнять  воронку до глубины {depth_opy + 200}м', None,
             f'Приподнять  воронку до глубины {depth_opy + 200}м',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(float(self.data_well.current_bottom) - (depth_opy + 200), 1)],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое'
             f' давление опрессовки э/колонны на устье {self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.35],
            [f'ОПУ до глубины {depth_opy}м', None,
             f'Фоновая запись. Произвести  опрессовку колонны снижением уровня свабированием по Задаче №2.1.17 '
             f'Понижение уровня '
             f'до глубины {depth_opy}м, тех отстой 3ч. КВУ в течение 3 часов после тех.отстоя. Интервал времени между замерами '
             f'1 час. В случае негерметичности произвести записи по тех карте 2.1.13 с целью определения НЭК',
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 20],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None]]
        # print(f'перевод {need_change_zgs_combo}')

        if need_change_zgs_combo == 'Да':
            if plast_new not in self.data_well.plast_project:
                self.data_well.plast_project.append(plast_new)

            self.data_well.fluid_work, self.data_well.fluid_work_short, plast, expected_pressure = need_h2s(
                self, fluid_new, plast_new, pressure_new)

            fluid_change_list = [
                [
                    f'Допустить до {self.data_well.current_bottom}м. Произвести смену объема  {self.data_well.fluid_work_short} '
                    f'не менее {round(well_volume(self, self.data_well.current_bottom), 1)}м3', None,
                    f'Допустить до {self.data_well.current_bottom}м. Произвести смену объема обратной '
                    f'промывкой по круговой циркуляции  жидкостью  {self.data_well.fluid_work} '
                    f'(по расчету по вскрываемому пласта {plast} Рожид- {expected_pressure}атм) в объеме не '
                    f'менее {round(well_volume(self, self.data_well.current_bottom), 1)}м3  в присутствии '
                    f'представителя заказчика, Составить акт. '
                    f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                    f'часа до начала работ)',
                    None, None, None, None, None, None, None,
                    'мастер КРС', round(well_volume_norm(well_volume(self, self.data_well.current_bottom))
                                        + descentNKT_norm(self.data_well.current_bottom - depth_opy - 200, 1), 1)],
                [None, None,
                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {self.data_well.current_bottom}м с '
                 f'доливом скважины в '
                 f'объеме {round((self.data_well.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(self.data_well.current_bottom, 1)]
            ]

            paker_list.extend(fluid_change_list)

        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {depth_opy + 200}м с доливом скважины в '
                               f'объеме {round((depth_opy + 200) * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(depth_opy + 200, 1)])
        return paker_list

    def swabbing_with_paker_stub(self, diameter_paker, paker_depth, paker_khost, plast_combo, swab_type_combo,
                                 swab_volume_edit, depth_gauge_combo, need_change_zgs_combo,
                                 plast_new, fluid_new, pressure_new):

        swab_short, swab_select = self.swab_select(swab_type_combo, plast_combo, swab_volume_edit)

        if depth_gauge_combo == 'Да':
            depth_gauge = 'контейнер с манометром МТГ-25 + '
        else:
            depth_gauge = ''

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and self.data_well.column_additional is True and
                self.data_well.head_column_additional.get_value > 800) else '60'])

        if self.data_well.column_additional is False or (self.data_well.column_additional is True and \
                                                         paker_depth < self.data_well.head_column_additional.get_value and self.data_well.head_column_additional.get_value > 800) or \
                (self.data_well.column_additional_diameter.get_value < 110 and
                 paker_depth > self.data_well.head_column_additional.get_value):
            paker_select = f'заглушка + {depth_gauge} НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                           f'щелевой фильтр + {depth_gauge} НКТ 10м'
            paker_short = f'заглушка {depth_gauge} + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм +' \
                          f' {depth_gauge} щелевой фильтр  +НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х' \
                           f' {self.data_well.column_additional_wall_thickness.get_value}мм + НКТ60мм 10м '
            paker_short = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм  + ' \
                          f'НКТ60мм 10м '
            dict_nkt = {int(nkt_diam): self.data_well.head_column_additional.get_value, 60:
                int(paker_depth - self.data_well.head_column_additional.get_value)}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 \
                and paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'заглушка +  НКТ{self.data_well.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм' \
                           f' + щелевой фильтр + НКТ{self.data_well.nkt_diam}мм со снятыми фасками 10м'
            paker_short = f'заглушка + НКТ{self.data_well.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diameter_paker}мм + щелевой фильтр + ' \
                          f'НКТ{self.data_well.nkt_diam}мм ' \
                          f'со снятыми фасками 10м'
            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}
        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'
        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м до H- {paker_depth}м, заглушкой до {paker_depth + paker_khost}м',
             None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker_depth}м, воронкой до'
             f' {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}.'
             f' {("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на глубине {paker_depth}м', None,
             f'Посадить пакер на глубине {paker_depth}м, заглушкой на '
             f'глубине {paker_khost + paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],

            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г.'
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
             f'давление на устье {self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
             f'практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин Промывка менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии'
             f' избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} '
             f'при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            ['выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить '
             f'замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
        ]
        ovtr = 'ОВТР 4ч' if self.data_well.region == 'ЧГМ' else 'ОВТР 6ч'
        ovtr4 = 4 if self.data_well.region == 'ЧГМ' else 6
        if swab_type_combo == 'Задача №2.1.13' and self.data_well.region not in ['ИГМ', 'ТГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker_depth)) < 10 or abs(float(interval[0] - paker_depth)) < 10:
                    if self.privyazka_nkt() not in paker_list and data_list.privyazkaSKO == 0:
                        data_list.privyazkaSKO += 1
                        paker_list.insert(1, self.privyazka_nkt()[0])

        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressure_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом'
                               f' {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                               f'{self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        return paker_list

    def swabbing_with_paker(self, diameter_paker, paker_depth, paker_khost, plast_combo, swab_type_combo,
                            swab_volume_edit,
                            depth_gauge_combo, need_change_zgs_combo='нет', plast_new='', fluid_new='',
                            pressure_new='', pressure_zumph_combo='Нет', paker_depth_zumpf=0):
        from .opressovka import OpressovkaEK

        swab_short, swab_select = self.swab_select(swab_type_combo, plast_combo, swab_volume_edit)

        if depth_gauge_combo == 'Да':
            depth_gauge = 'контейнер с манометром МТГ-25 + '
        else:
            depth_gauge = ''

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and
                self.data_well.column_additional is True and
                self.data_well.head_column_additional.get_value > 800) else '60'])

        if self.data_well.column_additional is False or (self.data_well.column_additional is True and \
                                                         paker_depth < self.data_well.head_column_additional.get_value and \
                                                         self.data_well.head_column_additional.get_value > 800):
            paker_select = f'воронку со свабоограничителем + {depth_gauge} НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм ' \
                           f'+ {depth_gauge} НКТ 10м'
            paker_short = f'в/ку со с/о {depth_gauge} + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм' \
                          f' + {depth_gauge}НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'воронку со свабоограничителем+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х' \
                           f' {self.data_well.column_additional_wall_thickness.get_value}мм + ' \
                           f'НКТ60мм 10м + репер + НКТ60мм ' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '
            paker_short = f'в-ку со свабоогр.+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм  + ' \
                          f'НКТ60мм 10м + ' \
                          f'НКТ60мм{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '

            dict_nkt = {int(nkt_diam): self.data_well.head_column_additional.get_value, 60:
                int(paker_depth - self.data_well.head_column_additional.get_value)}

        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 \
                and paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'воронку со свабоограничителем+ НКТ{self.data_well.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм' \
                           f' + НКТ{self.data_well.nkt_diam}мм со ' \
                           f'снятыми фасками 10м + НКТ{self.data_well.nkt_diam}мм ' \
                           f'со снятыми фасками' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '
            paker_short = f'в-ку со свабоогр.+ НКТ{self.data_well.nkt_diam}мм со ' \
                          f'снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diameter_paker}мм + НКТ{self.data_well.nkt_diam}мм ' \
                          f'со снятыми фасками 10м + НКТ{self.data_well.nkt_diam}мм ' \
                          f'со снятыми фасками ' \
                          f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м '

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}
        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'
        if pressure_zumph_combo == "Да":
            paker_list = [
                [f'СПО {paker_short} на НКТ{nkt_diam}м до H- {paker_depth}м, воронкой до {paker_depth + paker_khost}м',
                 None,
                 f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker_depth}м, воронкой до'
                 f' {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}.'
                 f' {("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [f'Опрессовать ЗУМПФ в инт {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм', None,
                 f'Посадить пакер. Опрессовать ЗУМПФ в интервале {paker_depth_zumpf} - {self.data_well.current_bottom}м на '
                 f'Р={self.data_well.max_admissible_pressure.get_value}атм в течение 30 минут в присутствии '
                 f'представителя заказчика, '
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
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для '
                 f'определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
        else:
            paker_list = [
                [f'СПО {paker_short} на НКТ{nkt_diam}м до H- {paker_depth}м, воронкой до {paker_depth + paker_khost}м',
                 None,
                 f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker_depth}м, воронкой до'
                 f' {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}.'
                 f' {("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [f'Посадить пакер на глубине {paker_depth}м', None,
                 f'Посадить пакер на глубине {paker_depth}м, воронку на '
                 f'глубине {paker_khost + paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [OpressovkaEK.testing_pressure(self, paker_depth)[1],
                 None, OpressovkaEK.testing_pressure(self, paker_depth)[0],
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.67],

                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК '
                 f'для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]

        paker_list.extend([
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г.'
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
             f'давление на устье {self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
             f'практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин  Промывка менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            ['выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить '
             f'замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5]])
        ovtr = 'ОВТР 4ч' if self.data_well.region == 'ЧГМ' else 'ОВТР 6ч'
        ovtr4 = 4 if self.data_well.region == 'ЧГМ' else 6
        if swab_type_combo == 'Задача №2.1.13' and self.data_well.region not in ['ИГМ', 'ТГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker_depth)) < 10 or abs(float(interval[0] - paker_depth)) < 10:
                    if self.privyazka_nkt() not in paker_list and data_list.privyazkaSKO == 0:
                        data_list.privyazkaSKO += 1
                        paker_list.insert(1, self.privyazka_nkt()[0])

        if need_change_zgs_combo == 'Да':
            # print(plast_new, fluid_new, pressure_new)
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressure_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 '
                               f'удельным весом {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 '
                               f'удельным весом {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])

        return paker_list

    def swabbing_with_2paker(self, diameter_paker, paker1_depth, paker2_depth, paker_khost, plast_combo,
                             swab_type_combo,
                             swab_volume_edit, depth_gauge_combo, need_change_zgs_combo,
                             plast_new, fluid_new, pressure_new):

        from .opressovka import OpressovkaEK

        swab_short, swab_select = self.swab_select(swab_type_combo, plast_combo, swab_volume_edit)

        nkt_diam = '73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and
                self.data_well.column_additional is True and \
                self.data_well.head_column_additional.get_value > 700) else '60'
        if depth_gauge_combo == 'Да':
            depth_gauge = 'контейнер с манометром МТГ-25 + '
        else:
            depth_gauge = ''

        if self.data_well.column_additional is False or self.data_well.column_additional is True and \
                paker1_depth < float(self.data_well.head_column_additional.get_value) and \
                float(self.data_well.head_column_additional.get_value) > 600:

            paker_select = f'заглушка + {depth_gauge} НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм ' \
                           f'(либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм + щелевой фильтр + ' \
                           f'{depth_gauge} НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ для ЭК ' \
                           f'{self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм + ' \
                           f'{depth_gauge} НКТ{nkt_diam} 20мм + репер'
            paker_short = f'заглушка + {depth_gauge}НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм + ' \
                          f'щелевой фильтр + {depth_gauge}' \
                          f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ {depth_gauge} + НКТ{nkt_diam} ' \
                          f'20мм + репер'
            dict_nkt = {73: paker1_depth + paker_khost}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and paker1_depth > float(
            self.data_well.head_column_additional.get_value):
            paker_select = f'заглушка +  НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм ' \
                           f'+ щелевой фильтр + ' \
                           f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ НКТ{60} 20мм + репер + НКТ60мм ' \
                           f'{round(float(self.data_well.head_column_additional.get_value) - paker2_depth, 0)}м '
            paker_short = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diameter_paker}мм ' \
                          f' + щелевой фильтр + НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ + НКТ{60} ' \
                          f'20мм + репер +' \
                          f' НКТ60мм {round(float(self.data_well.head_column_additional.get_value) - paker2_depth, 0)}м '
            dict_nkt = {73: self.data_well.head_column_additional.get_value,
                        60: int(paker1_depth - self.data_well.head_column_additional.get_value)}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 and \
                paker1_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'заглушка + {depth_gauge}НКТ{73}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diameter_paker}мм (либо аналог) для ЭК {self.data_well.column_diameter.get_value}мм х ' \
                           f'{self.data_well.column_wall_thickness.get_value}мм + щелевой фильтр + {depth_gauge}' \
                           f'НКТ l-{round(paker1_depth - paker2_depth, 0)} {depth_gauge} + пакер ПУ  со ' \
                           f'снятыми фасками 20мм + репер + ' \
                           f'НКТ{73}мм со снятыми фасками ' \
                           f'{round(float(self.data_well.head_column_additional.get_value) - paker2_depth, 0)}м '
            paker_short = f'заглушка +{depth_gauge}  НКТ{73}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{diameter_paker}мм + щелевой фильтр + {depth_gauge}' \
                          f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ  со снятыми фасками ' \
                          f'20мм + {depth_gauge} + репер + ' \
                          f'НКТ{73}мм со снятыми фасками ' \
                          f'{round(float(self.data_well.head_column_additional.get_value) - paker2_depth, 0)}м '
            dict_nkt = {73: paker1_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker1_depth + paker_khost}
        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'
        paker_list = [
            [f'Спуск {paker_short} до глубины {paker1_depth}/{paker2_depth}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker1_depth}/{paker2_depth}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}. '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker1_depth, 1.2)],
            [f'Посадить пакера на глубине {paker1_depth}/{paker2_depth}м',
             None, f'Посадить пакера на глубине {paker1_depth}/{paker2_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [OpressovkaEK.testing_pressure(self, paker2_depth)[1],
             None,
             OpressovkaEK.testing_pressure(self, paker2_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],

            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабированиии утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое давление на '
             f'устье {self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин. Промывка менее {round(well_volume(self, paker1_depth) * 1.5, 1)}м3',
             None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления:'
             f' произвести промывку скважину обратной промывкой '
             f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости не '
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker1_depth) * 1.5, 1)}м3 '
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            [f' выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного статического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления на устье, выполнить '
             f'замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5]
        ]

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker1_depth)) < 10 or abs(float(interval[0] - paker1_depth)) < 10:
                    if self.privyazka_nkt() not in paker_list and data_list.privyazkaSKO == 0:
                        data_list.privyazkaSKO += 1
                        paker_list.insert(1, self.privyazka_nkt())
        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressure_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker1_depth}м с '
                               f'доливом скважины в '
                               f'объеме {round(paker1_depth * 1.12 / 1000, 1)}м3 удельным весом'
                               f' {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker1_depth, 1.2)])
        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker1_depth}м с '
                               f'доливом скважины в '
                               f'объеме {round(paker1_depth * 1.12 / 1000, 1)}м3 удельным весом '
                               f'{self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker1_depth, 1.2)])

        return paker_list

    def swabbing_with_voronka(self, paker_depth, plast_combo, swab_type_combo, swab_volume_edit, depth_gauge_combo,
                              need_change_zgs_combo, plast_new, fluid_new, pressure_new):

        swab_short, swab_select = self.swab_select(swab_type_combo, plast_combo, swab_volume_edit)
        nkt_diam = '73' if self.data_well.column_diameter.get_value > 110 or (
                self.data_well.column_diameter.get_value > 110 and
                self.data_well.column_additional is True and
                self.data_well.head_column_additional.get_value > 700) else '60'

        if depth_gauge_combo == 'Да':
            depth_gauge = 'контейнер с манометром МТГ-25 + '
        else:
            depth_gauge = ''

        paker_short = ''
        if self.data_well.column_additional is False or \
                (self.data_well.column_additional is True and
                 paker_depth <= self.data_well.head_column_additional.get_value):
            paker_select = f'воронку + {depth_gauge} свабоограничитель  НКТ{nkt_diam} +репер + НКТ 10м'
            paker_short = f'в/у + {depth_gauge} со с/о НКТ{nkt_diam} +репер + НКТ 10м'
            dict_nkt = {73: paker_depth}
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'воронку со свабоограничителем  + НКТ{60}мм ' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 1)}м' \
                           f' {depth_gauge}'
            paker_short = f'обточ муфту + НКТ{60}мм ' \
                          f'{round(paker_depth - self.data_well.head_column_additional.get_value, 1)}м ' \
                          f'{depth_gauge}'
            dict_nkt = {60: paker_depth}
        if 'Ойл' in data_list.contractor:
            schema_swab = '8'
        elif 'РН' in data_list.contractor:
            schema_swab = '7'
        paker_list = [
            [paker_short, None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  воронкой до {paker_depth}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}. ',
             None, None, None, None, None, None, None,
             'мастер КРС', round(
                self.data_well.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008
                * paker_depth / 9.52 + 0.003 * self.data_well.current_bottom / 9.52,
                2)],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы №{schema_swab} при свабировании утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
             f'давление на устье '
             f'{self.data_well.max_admissible_pressure.get_value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'промывка в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f' При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} '
             f'при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', well_volume_norm(well_volume(self, paker_depth))],
            [f' выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стататического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления на устье, '
             f'выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
        ]
        ovtr = 'ОВТР 4ч' if self.data_well.region == 'ЧГМ' else 'ОВТР 6ч'
        ovtr4 = 4 if self.data_well.region == 'ЧГМ' else 6
        if swab_type_combo == 'Задача №2.1.13' and self.data_well.region not in ['ИГМ']:
            paker_list.insert(1, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressure_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                               f'{self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом'
                               f' {self.data_well.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        return paker_list


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()

    window = SwabWindow()
    window.show()
    sys.exit(app.exec_())
