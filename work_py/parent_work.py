import json
from collections import namedtuple
from datetime import datetime
from typing import List

import data_list
from data_base.config_base import connection_to_database, WorkDatabaseWell
from decrypt import decrypt
from find import FindIndexPZ
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QTabWidget, QInputDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QGridLayout

from main import MyMainWindow
from work_py.calculate_work_parametrs import volume_work, volume_well_pod_nkt_calculate
from data_list import contractor, ProtectedIsDigit

from work_py.advanted_file import definition_plast_work
from work_py.alone_oreration import volume_vn_nkt, well_volume
from work_py.calc_fond_nkt import CalcFond
from work_py.rationingKRS import well_volume_norm


class TabPageUnion(QWidget):
    def __init__(self, data_well: FindIndexPZ):
        super().__init__()
        self.pressure_zumpf_question_combo = None
        self.pressure_zumpf_question_label = None
        self.need_privyazka_q_combo = None
        self.need_privyazka_Label = None
        self.grid = QGridLayout(self)

        self.validator_float = QDoubleValidator(0.0, 8000.0, 2)
        self.validator_int = QIntValidator(0, 8000)
        self.data_well = data_well

    def view_paker_work(self):
        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.paker_khost_label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator_int)

        self.paker_depth_label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator_int)
        self.paker_depth_edit.textChanged.connect(self.update_paker)

        self.paker_depth_zumpf_label = QLabel("Глубина посадки для ЗУМПФа", self)
        self.paker_depth_zumpf_edit = QLineEdit(self)
        self.paker_depth_zumpf_edit.setValidator(self.validator_int)

        self.need_privyazka_Label = QLabel("Привязка оборудования", self)
        self.need_privyazka_q_combo = QComboBox()
        self.need_privyazka_q_combo.addItems(['Нет', 'Да'])

        self.pressure_zumpf_question_label = QLabel("Нужно ли опрессовывать ЗУМПФ", self)
        self.pressure_zumpf_question_combo = QComboBox(self)
        self.pressure_zumpf_question_combo.currentTextChanged.connect(self.update_paker_need)
        self.pressure_zumpf_question_combo.addItems(['Нет', 'Да'])

        paker_depth = ''
        if len(self.data_well.plast_work) != 0:
            paker_depth = self.data_well.perforation_roof - 20
        else:
            if self.data_well.dict_leakiness:
                paker_depth = min([float(nek.split('-')[0]) - 10
                                   for nek in self.data_well.dict_leakiness['НЭК']['интервал'].keys()])
        if paker_depth != '':
            self.paker_depth_edit.setText(str(int(paker_depth)))

        self.grid.addWidget(self.diameter_paker_label_type, 1, 1)
        self.grid.addWidget(self.diameter_paker_edit, 2, 1)

        self.grid.addWidget(self.paker_khost_label, 1, 2)
        self.grid.addWidget(self.paker_khost_edit, 2, 2)

        self.grid.addWidget(self.paker_depth_label, 1, 3)
        self.grid.addWidget(self.paker_depth_edit, 2, 3)

        self.grid.addWidget(self.pressure_zumpf_question_label, 1, 4)
        self.grid.addWidget(self.pressure_zumpf_question_combo, 2, 4)
        self.grid.addWidget(self.need_privyazka_Label, 1, 6)
        self.grid.addWidget(self.need_privyazka_q_combo, 2, 6)

    def calculate_h2s(self, type_absorbent, category_h2s, h2s_mg, h2s_pr):
        if '2' in str(category_h2s) or '1' in str(category_h2s):
            if type_absorbent == 'EVASORB марки 121':
                koeff_zapas = 1.05
            else:
                koeff_zapas = 1

            volume_pod_nkt = volume_well_pod_nkt_calculate(self.data_well)
            udel_vodoiz_nkt = 0
            volume_well = volume_work(self.data_well)
            vodoiz_nkt = 0

            for nkt_key, nkt_values in self.data_well.dict_nkt_before.items():
                if '73' in nkt_key:
                    nkt_1 = 73
                    nkt_width = 5.5
                elif '60' in nkt_key:
                    nkt_1 = 60
                    nkt_width = 5
                elif '48' in nkt_key:
                    nkt_1 = 48
                    nkt_width = 4
                elif '89' in nkt_key:
                    nkt_1 = 89
                    nkt_width = 6.5

                vodoiz_nkt = round(10 * 3.14 * ((nkt_1 * 0.01) ** 2 - (nkt_1 * 0.01 - nkt_width * 2 * 0.01) ** 2) / 4,
                                   2)
                udel_vodoiz_nkt += vodoiz_nkt * nkt_values / 1000

            sucker_rod_l_25 = 0
            sucker_rod_l_22 = 0
            sucker_rod_l_19 = 0

            for sucker_key, sucker_value in self.data_well.dict_sucker_rod.items():
                if '25' in sucker_key:
                    sucker_rod_l_25 = sucker_value
                elif '22' in sucker_key:
                    sucker_rod_l_22 = sucker_value
                elif '19' in sucker_key:
                    sucker_rod_l_19 = sucker_value

            vodoiz_sucker = (10 * 3.14 * ((25 * 0.01) ** 2 / 4) * sucker_rod_l_25 / 1000) + (
                    10 * 3.14 * ((25 * 0.01) ** 2 / 4) * sucker_rod_l_22 / 1000) + (
                                    10 * 3.14 * ((25 * 0.01) ** 2 / 4) * sucker_rod_l_19 / 1000)

            oil_mass = round(float(udel_vodoiz_nkt * (100 - self.data_well.percent_water) * 0.9 / 100), 2)

            try:
                volume_h2s = self.data_well.gaz_factor_percent[0] * oil_mass * (float(h2s_pr)) / 100
            except Exception:
                self.data_well.gaz_factor_percent = [11]
                volume_h2s = self.data_well.gaz_factor_percent[0] * oil_mass * (float(h2s_pr)) / 100

            h2s_mass_in_oil = round(34 * volume_h2s * 1000 / 22.14, 0)

            h2s_mass_in_water = round(float(vodoiz_sucker + udel_vodoiz_nkt) * h2s_mg, 0)

            mass_oil_pog_gno = volume_pod_nkt * (100 - self.data_well.percent_water) * 0.9 / 100
            h2s_volume_pod_gno = mass_oil_pog_gno * self.data_well.gaz_factor_percent[0] * h2s_pr / 100
            mass_h2s_gas = round(34 * h2s_volume_pod_gno * 1000 / 22.14, 0)
            mass_h2s_water = round(volume_pod_nkt * h2s_mg, 0)

            mass_h2s_all = h2s_mass_in_water + h2s_mass_in_oil + mass_h2s_gas + mass_h2s_water

            emk_reag = 24
            plotn_reag = 1.065
            raschet_mass = mass_h2s_all * emk_reag / 1000
            mass_reag_s_zapas = raschet_mass * koeff_zapas
            # print(f'mass{mass_reag_s_zapas}')
            udel_mas_raskhod = mass_reag_s_zapas / volume_well / plotn_reag
            # print(udel_mas_raskhod)

            if udel_mas_raskhod <= 0.01:
                udel_mas_raskhod = 0.01
            return round(udel_mas_raskhod, 3)
        else:
            return 0

    def check_combobox_in_layout(self, layout, combo_name):
        for i in range(layout.count()):
            widget_item = layout.itemAt(i).widget()
            if widget_item and widget_item.objectName() == combo_name:
                return True
        return False

    def update_sko_true(self, index):
        if self.check_combobox_in_layout(self.grid, "acid_edit") is False:
            self.Qplast_labelType = QLabel("Нужно ли определять приемистость до СКО", self)
            self.QplastEdit = QComboBox(self)
            self.QplastEdit.addItems(['ДА', 'НЕТ'])
            self.QplastEdit.setCurrentIndex(1)
            self.QplastEdit.setProperty('value', 'НЕТ')

            self.acid_label_type = QLabel("Вид кислотной обработки", self)
            self.acid_edit = QComboBox(self)
            self.acid_edit.setObjectName("acid_edit")
            self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
            self.acid_edit.setCurrentIndex(0)

            self.acid_volume_label = QLabel("Объем кислотной обработки", self)
            self.acid_volume_edit = QLineEdit(self)

            self.acid_volume_edit.setText("10")
            self.acid_volume_edit.setClearButtonEnabled(True)

            self.acid_proc_label = QLabel("Концентрация кислоты", self)
            self.acid_proc_edit = QLineEdit(self)
            self.acid_proc_edit.setText('12')
            self.acid_proc_edit.setClearButtonEnabled(True)

            self.acid_oil_proc_label = QLabel("объем нефти", self)
            self.acid_oil_proc_edit = QLineEdit(self)
            self.acid_oil_proc_edit.setText('0')

            self.iron_volume_label = QLabel("Объем стабилизатора", self)
            self.iron_volume_edit = QLineEdit(self)

            self.expected_pickup_label = QLabel('Ожидаемая приемистость')
            self.expected_pickup_edit = QLineEdit(self)
            self.expected_pickup_edit.setValidator(self.validator_int)

            self.expected_pressure_label = QLabel('Ожидаемое давление закачки')
            self.expected_pressure_edit = QLineEdit(self)

            self.expected_pressure_edit.textChanged.connect(self.update_pressure)
            self.pressure_three_label = QLabel('в трех режимам давлений')
            self.pressure_three_edit = QLineEdit(self)
            self.expected_pressure_edit.setValidator(self.validator_int)

            if self.__class__.__name__ == 'TabPageSoAcid':
                self.paker_layout_combo.currentTextChanged.connect(self.update_paker_layout)

            self.Qplast_after_labelType = QLabel("Нужно ли определять приемистость после СКО", self)
            self.Qplast_after_edit = QComboBox(self)
            self.Qplast_after_edit.addItems(['НЕТ', 'ДА'])

            self.calculate_sko_label = QLabel('Расчет на п.м.')
            self.calculate_sko_line = QLineEdit(self)

            self.iron_label_type = QLabel("необходимость стабилизатора железа", self)
            self.iron_true_combo = QComboBox(self)
            self.iron_true_combo.addItems(['Нет', 'Да'])

            self.pressure_Label = QLabel("Давление закачки", self)
            self.pressure_edit = QLineEdit(self)

            if self.data_well:
                if self.data_well.stabilizator_need:
                    self.iron_true_combo.setCurrentIndex(1)

            self.grid.addWidget(self.pressure_Label, 6, 6)
            self.grid.addWidget(self.pressure_edit, 7, 6)

            self.grid.addWidget(self.iron_label_type, 4, 4)
            self.grid.addWidget(self.iron_true_combo, 5, 4)
            self.grid.addWidget(self.iron_volume_label, 4, 5)
            self.grid.addWidget(self.iron_volume_edit, 5, 5)

            self.grid.addWidget(self.acid_label_type, 6, 2)
            self.grid.addWidget(self.acid_edit, 7, 2)
            self.grid.addWidget(self.acid_volume_label, 6, 3)
            self.grid.addWidget(self.acid_volume_edit, 7, 3)
            self.grid.addWidget(self.acid_proc_label, 6, 4)
            self.grid.addWidget(self.acid_proc_edit, 7, 4)
            self.grid.addWidget(self.acid_oil_proc_label, 6, 5)
            self.grid.addWidget(self.acid_oil_proc_edit, 7, 5)
            if self.__class__.__name__ == 'TabPageSo':
                from work_py.acid_paker import CheckableComboBox
                self.plast_combo = CheckableComboBox(self)
                self.grid.addWidget(self.plast_combo, 7, 7)

            self.grid.addWidget(self.calculate_sko_label, 6, 8)
            self.grid.addWidget(self.calculate_sko_line, 7, 8)
            self.grid.addWidget(self.Qplast_labelType, 6, 1)
            self.grid.addWidget(self.QplastEdit, 7, 1)

            self.grid.addWidget(self.Qplast_after_labelType, 10, 1)
            self.grid.addWidget(self.Qplast_after_edit, 11, 1)

            self.grid.addWidget(self.expected_pickup_label, 10, 2)
            self.grid.addWidget(self.expected_pickup_edit, 11, 2)
            self.grid.addWidget(self.expected_pressure_label, 10, 3)
            self.grid.addWidget(self.expected_pressure_edit, 11, 3)
            self.grid.addWidget(self.pressure_three_label, 10, 4)
            self.grid.addWidget(self.pressure_three_edit, 11, 4)
            self.Qplast_after_edit.currentTextChanged.connect(self.update_q_plast_after)

            if self.data_well:
                if self.__class__.__name__ == 'TabPageSoAcid':
                    if all([self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                            self.data_well.plast_work]):
                        self.paker_layout_combo.setCurrentIndex(2)
                    else:
                        self.paker_layout_combo.setCurrentIndex(1)

            self.iron_volume_edit.setText(f'{round(float(self.acid_volume_edit.text()), 1) * 10}')
            self.acid_volume_edit.textChanged.connect(self.change_volume_acid)
            self.acid_edit.currentTextChanged.connect(self.update_sko_type)
            self.Qplast_after_edit.setCurrentIndex(1)
            self.Qplast_after_edit.setCurrentIndex(0)

        if index == 'Нет':
            self.Qplast_labelType.setVisible(False)
            self.QplastEdit.setVisible(False)
            self.acid_label_type.setVisible(False)
            self.acid_edit.setVisible(False)

            self.acid_volume_label.setVisible(False)
            self.acid_volume_edit.setVisible(False)

            self.acid_proc_label.setVisible(False)
            self.acid_proc_edit.setVisible(False)

            self.acid_oil_proc_label.setVisible(False)
            self.acid_oil_proc_edit.setVisible(False)

            self.iron_volume_label.setVisible(False)
            self.iron_volume_edit.setVisible(False)



            self.calculate_sko_label.setVisible(False)
            self.calculate_sko_line.setVisible(False)

            self.iron_label_type.setVisible(False)
            self.iron_true_combo.setVisible(False)
        else:
            self.Qplast_labelType.setVisible(True)
            self.QplastEdit.setVisible(True)
            self.acid_label_type.setVisible(True)
            self.acid_edit.setVisible(True)

            self.acid_volume_label.setVisible(True)
            self.acid_volume_edit.setVisible(True)

            self.acid_proc_label.setVisible(True)
            self.acid_proc_edit.setVisible(True)

            self.acid_oil_proc_label.setVisible(True)
            self.acid_oil_proc_edit.setVisible(True)

            self.iron_volume_label.setVisible(True)
            self.iron_volume_edit.setVisible(True)
            self.plast_combo.setVisible(True)
            self.expected_pressure_label.setVisible(True)
            self.expected_pressure_edit.setVisible(True)
            self.expected_pickup_label.setVisible(True)

            self.expected_pickup_edit.setVisible(True)

            self.pressure_three_label.setVisible(True)
            self.pressure_three_edit.setVisible(True)

            self.pressure_Label.setVisible(True)
            self.pressure_edit.setVisible(True)

            self.Qplast_after_labelType.setVisible(True)
            self.Qplast_after_edit.setVisible(True)

            self.calculate_sko_label.setVisible(True)
            self.calculate_sko_line.setVisible(True)

            self.iron_label_type.setVisible(True)
            self.iron_true_combo.setVisible(True)

        if self.data_well:
            if self.data_well.curator == 'ОР':
                self.Qplast_after_edit.setCurrentIndex(0)
                self.Qplast_after_edit.setCurrentIndex(1)
            else:
                self.Qplast_after_edit.setCurrentIndex(1)
                self.Qplast_after_edit.setCurrentIndex(0)
        self.calculate_sko_line.editingFinished.connect(self.update_calculate_sko)

    def update_calculate_sko(self):
        plasts = data_list.texts
        metr_pvr = 0
        for plast in self.data_well.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    for interval in self.data_well.dict_perforation[plast]['интервал']:
                        if interval[1] < self.data_well.current_bottom:
                            metr_pvr += abs(interval[0] - interval[1])
        calculate_sko = self.calculate_sko_line.text()
        if calculate_sko != '':
            calculate_sko = calculate_sko.replace(',', '.')
            self.acid_volume_edit.setText(f'{round(metr_pvr * float(calculate_sko), 1)}')

    def update_sko_type(self, type_sko):
        if type_sko == 'ВТ':
            self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
            self.sko_vt_edit = QLineEdit(self)
            self.grid.addWidget(self.sko_vt_label, 6, 7)
            self.grid.addWidget(self.sko_vt_edit, 7, 7)
        else:
            self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
            self.sko_vt_edit = QLineEdit(self)
            self.sko_vt_label.setParent(None)
            self.sko_vt_edit.setParent(None)

    def change_volume_acid(self):
        if self.acid_volume_edit.text() != '':
            self.iron_volume_edit.setText(f'{round(float(self.acid_volume_edit.text().replace(",", ".")), 1) * 10}')

    def update_q_plast_after(self, index):
        if self.data_well:
            if self.data_well.expected_pickup != 0:
                self.expected_pickup_edit.setText(f'{self.data_well.expected_pickup}')

            if self.data_well.expected_pressure != 0:
                self.expected_pressure_edit.setText(f'{self.data_well.expected_pressure}')

            self.expected_pickup_edit.setText(str(self.data_well.expected_pickup))
            self.expected_pressure_edit.setText(str(self.data_well.expected_pressure))

            self.grid.addWidget(self.expected_pickup_label, 10, 2)
            self.grid.addWidget(self.expected_pickup_edit, 11, 2)
            self.grid.addWidget(self.expected_pressure_label, 10, 3)
            self.grid.addWidget(self.expected_pressure_edit, 11, 3)
            self.grid.addWidget(self.pressure_three_label, 10, 4)
            self.grid.addWidget(self.pressure_three_edit, 11, 4)

        if index == 'НЕТ':
            self.expected_pickup_label.setVisible(False)
            self.expected_pickup_edit.setVisible(False)
            self.expected_pressure_label.setVisible(False)
            self.expected_pressure_label.setVisible(False)
            self.expected_pressure_edit.setVisible(False)
            self.pressure_three_label.setVisible(False)
            self.pressure_three_edit.setVisible(False)

        else:
            self.expected_pickup_label.setVisible(True)
            self.expected_pickup_edit.setVisible(True)
            self.expected_pressure_label.setVisible(True)
            self.expected_pressure_label.setVisible(True)
            self.expected_pressure_edit.setVisible(True)
            self.pressure_three_label.setVisible(True)
            self.pressure_three_edit.setVisible(True)


    def pressure_mode(self, mode, plast):
        if self.data_well:
            mode = int(mode / 10) * 10
            if ('d2ps' in plast.lower() or 'дпаш' in plast.lower()) and self.data_well.region == 'ИГМ':
                mode_str = f'{120}, {140}, {160}'
            elif mode > self.data_well.max_admissible_pressure.get_value:
                mode_str = f'{mode}, {mode - 10}, {mode - 20}'
            else:
                mode_str = f'{mode - 10}, {mode}, {mode + 10}'
            return mode_str

    def update_pressure(self):
        expected_pressure = self.expected_pressure_edit.text()
        if expected_pressure.isdigit():
            expected_pressure = int(float(expected_pressure))
            self.pressure_three_edit.setText(
                self.pressure_mode(expected_pressure, self.plast_combo.combo_box.currentText()))

    def update_skv_edit(self, index):

        if index == 'без СКВ':
            self.skv_acid_label_type.setParent(None)
            self.skv_acid_edit.setParent(None)
            self.skv_volume_label.setParent(None)
            self.skv_volume_edit.setParent(None)
            self.skv_proc_label.setParent(None)
            self.skv_proc_edit.setParent(None)
        else:
            self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
            self.skv_acid_edit = QComboBox(self)
            self.skv_acid_edit.addItems(['HCl', 'HF'])
            self.skv_acid_edit.setCurrentIndex(0)
            self.skv_acid_edit.setProperty('value', 'HCl')
            self.skv_volume_label = QLabel("Объем СКВ", self)
            self.skv_volume_edit = QLineEdit(self)
            self.skv_volume_edit.setText('1')
            self.skv_volume_edit.setClearButtonEnabled(True)
            self.skv_proc_label = QLabel("Концентрация СКВ", self)
            self.skv_proc_edit = QLineEdit(self)
            self.skv_proc_edit.setClearButtonEnabled(True)
            self.skv_proc_edit.setText('12')

            self.grid.addWidget(self.skv_acid_label_type, 4, 1)
            self.grid.addWidget(self.skv_acid_edit, 5, 1)
            self.grid.addWidget(self.skv_volume_label, 4, 2)
            self.grid.addWidget(self.skv_volume_edit, 5, 2)
            self.grid.addWidget(self.skv_proc_label, 4, 3)
            self.grid.addWidget(self.skv_proc_edit, 5, 3)

    def update_need_swab(self, index):
        if index == 'без освоения':
            self.swab_type_label.setParent(None)
            self.swab_type_combo.setParent(None)
            self.swab_pakerLabel.setParent(None)
            self.swab_paker_depth.setParent(None)
            self.swab_volumeLabel.setParent(None)
            self.swab_volume_edit.setParent(None)
        else:
            self.swab_pakerLabel = QLabel("Глубина посадки нижнего пакера при освоении", self)
            self.swab_paker_depth = QLineEdit(self)
            if self.paker_depth_edit.text() != '':
                self.swab_paker_depth.setText(str(float(self.paker_depth_edit.text()) - 50))

            self.swab_type_label = QLabel("задача при освоении", self)
            self.swab_type_combo = QComboBox(self)
            self.swab_type_combo.addItems(['Задача №2.1.13', 'Задача №2.1.14', 'Задача №2.1.16', 'Задача №2.1.11',
                                           'Задача №2.1.16 + герметичность пакера', 'ГРР', 'своя задача'])
            self.swab_type_combo.setCurrentIndex(data_list.swab_type_comboIndex)

            self.swab_volumeLabel = QLabel("объем освоения", self)
            self.swab_volume_edit = QLineEdit(self)

            self.grid.addWidget(self.swab_type_label, 12, 1)
            self.grid.addWidget(self.swab_type_combo, 13, 1)
            self.grid.addWidget(self.swab_pakerLabel, 12, 2)
            self.grid.addWidget(self.swab_paker_depth, 13, 2)
            self.grid.addWidget(self.swab_volumeLabel, 12, 3)
            self.grid.addWidget(self.swab_volume_edit, 13, 3)
            if self.data_well:
                if self.data_well.region in ['КГМ', 'АГМ'] or self.__class__.__name__ == 'TabPageSo':
                    self.swab_type_combo.setCurrentIndex(2)
                    self.swab_volume_edit.setText('20')
                else:
                    self.swab_type_combo.setCurrentIndex(0)
                    self.swab_volume_edit.setText('25')

    @staticmethod
    def difference_date_days(date1, today=data_list.current_date):
        # Задание дат
        date1 = datetime.strptime(date1, "%d.%m.%Y")

        # Вычисление разницы в днях
        difference = (today - date1).days

        return difference

    def update_paker_need(self, index):
        if index == 'Нет':
            self.paker_depth_zumpf_label.setParent(None)
            self.paker_depth_zumpf_edit.setParent(None)
        elif index == 'Да':
            if len(self.data_well.plast_work) != 0:
                paker_depth_zumpf = int(self.data_well.perforation_roof + 10)
            else:
                if self.data_well.dict_leakiness:
                    paker_depth_zumpf = int(max([float(nek.split('-')[0]) + 10
                                                 for nek in self.data_well.dict_leakiness['НЭК']['интервал'].keys()]))
                else:
                    paker_depth_zumpf = self.data_well.current_bottom - 10

            self.paker_depth_zumpf_edit.setText(f'{paker_depth_zumpf}')

            self.grid.addWidget(self.paker_depth_zumpf_label, 1, 5)
            self.grid.addWidget(self.paker_depth_zumpf_edit, 2, 5)

    def update_paker(self):
        paker_depth = self.paker_depth_edit.text()
        if paker_depth != '':
            if self.data_well.open_trunk_well is True:

                paker_khost = self.data_well.current_bottom - int(float(paker_depth))
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(float(paker_depth)))}')
            else:
                paker_khost = 10
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(float(paker_depth)))}')
            need_count = 0
            for plast in self.data_well.plast_all:
                for roof, sole in self.data_well.dict_perforation[plast]['интервал']:
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth)) < 10:
                        need_count += 1
            if self.data_well.dict_leakiness:
                for interval in self.data_well.dict_leakiness['НЭК']['интервал']:
                    roof, sole = interval.split('-')
                    if abs(float(roof) - float(paker_depth)) < 10 or abs(float(sole) - float(paker_depth)) < 10:
                        need_count += 1

            if need_count == 0:
                self.need_privyazka_q_combo.setCurrentIndex(0)
            else:
                self.need_privyazka_q_combo.setCurrentIndex(1)

    def paker_diameter_select(self, depth_landing):
        paker_diam_dict = {
            82: (84, 92),
            88: (92.1, 97),
            92: (97.1, 102),
            100: (102.1, 109),
            104: (109, 115),
            112: (118, 120),
            114: (120.1, 121.9),
            116: (122, 123.9),
            118: (124, 127.9),
            122: (128, 133),
            136: (144, 148),
            142: (148.1, 154),
            145: (154.1, 164),
            158: (166, 176),
            182: (190.6, 203.6),
            204: (215, 221)
        }
        paker_diameter = 0
        try:
            if self.data_well.column_additional is False or (
                    self.data_well.column_additional is True and int(
                depth_landing) <= self.data_well.head_column_additional.get_value):
                diam_internal_ek = self.data_well.column_diameter.get_value - 2 * self.data_well.column_wall_thickness.get_value
            else:
                diam_internal_ek = self.data_well.column_additional_diameter.get_value - \
                                   2 * self.data_well.column_additional_wall_thickness.get_value

            for diam, diam_internal_paker in paker_diam_dict.items():
                if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                    paker_diameter = diam
                    break
        except Exception as e:
            print('ошибка проверки диаметра пакера')

        return paker_diameter

    def insert_data_dop_plan(self, result, paragraph_row):
        self.data_well.plast_project = []
        self.data_well.dict_perforation_project = {}
        self.data_well.data_list = []
        self.data_well.gips_in_well = False
        self.data_well.drilling_interval = []
        self.data_well.for_paker_list = False
        self.data_well.grp_plan = False
        self.data_well.angle_data = []
        self.data_well.nkt_opress_true = False
        self.data_well.bvo = False
        self.data_well.stabilizator_need = False
        self.data_well.current_bottom_second = 0

        paragraph_row = paragraph_row - 1

        if len(result) <= paragraph_row:
            QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пунктов')
            return

        self.data_well.current_bottom = result[paragraph_row][1]

        self.data_well.dict_perforation = json.loads(result[paragraph_row][2])

        self.data_well.plast_all = json.loads(result[paragraph_row][3])
        self.data_well.plast_work = json.loads(result[paragraph_row][4])
        self.data_well.dict_leakiness = json.loads(result[paragraph_row][5])
        self.data_well.leakiness = False
        self.data_well.leakiness_interval = []
        if self.data_well.dict_leakiness:
            self.data_well.leakiness = True
            self.data_well.leakiness_interval = list(self.data_well.dict_leakiness['НЭК'].keys())

        if result[paragraph_row][6] is True:
            self.data_well.column_additional = True
        else:
            self.data_well.column_additional = False

        self.data_well.fluid_work = result[paragraph_row][7]

        self.data_well.category_pressure = result[paragraph_row][8]
        self.data_well.category_h2s = result[paragraph_row][9]
        self.data_well.category_gas_factor = result[paragraph_row][10]
        self.data_well.category_pvo = 2
        if str(self.data_well.category_pressure) == '1' or str(self.data_well.category_h2s) == '1' \
                or self.data_well.category_gas_factor == '1':
            self.data_well.category_pvo = 1

        self.data_well.template_depth, self.data_well.template_length, \
        self.data_well.template_depth_addition, self.data_well.template_length_addition = \
            json.loads(result[paragraph_row][11])

        self.data_well.skm_interval = json.loads(result[paragraph_row][12])

        self.data_well.problem_with_ek_depth = result[paragraph_row][13]
        self.data_well.problem_with_ek_diameter = result[paragraph_row][14]
        try:
            self.data_well.head_column = ProtectedIsDigit(result[paragraph_row][16])
        except Exception:
            print('отсутствуют данные по голове хвостовика')
        self.data_well.dict_perforation_short = json.loads(result[paragraph_row][2])

        try:
            self.data_well.ribbing_interval = json.loads(result[paragraph_row][15])
        except Exception:
            print('отсутствуют данные по интервалам райбирования')

        definition_plast_work(self)
        return True

    @staticmethod
    def check_if_none(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
                or value == 0 or str(value).replace(' ', '') == '':
            return 'отсут'
        else:
            return value


class TabWidgetUnion(QTabWidget):
    def __init__(self, parent=None):
        super().__init__()


class WindowUnion(MyMainWindow):
    def __init__(self, data_well: FindIndexPZ):
        super().__init__()
        self.QplastEdit = None
        self.data_well = data_well
        self.tableWidget = None

    def acid_work(self):
        from work_py.alone_oreration import volume_vn_nkt, well_volume
        paker_list = []

        if self.iron_true_combo == 'Да':
            iron_str = f' с добавлением стабилизатор железа (Hi-Iron)  из расчета 10кг на 1тн ({self.iron_volume_edit}кг)'
        else:
            iron_str = ""

        if self.acid_edit == 'HCl':

            acid_sel = f'Произвести солянокислотную обработку {self.plast_combo} в объеме {self.acid_volume_edit}м3 ' \
                       f'({self.acid_edit} - {self.acid_proc_edit} %) {iron_str}' \
                       f' в присутствии представителя Заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.data_well.max_admissible_pressure.get_value}атм. \n' \
                       f'(для приготовления соляной кислоты в объеме {self.acid_volume_edit}м3 - {self.acid_proc_edit}% ' \
                       f'необходимо ' \
                       f'замешать {round(self.acid_volume_edit * self.acid_proc_edit / 24 * 1.118, 1)}т HCL 24% и' \
                       f' пресной воды ' \
                       f'{round(float(self.acid_volume_edit) - float(self.acid_volume_edit) * float(self.acid_proc_edit) / 24 * 1.118, 1)}м3) ' \
                       f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол по технологическому' \
                       f' плану работ СК КРЕЗОЛ. '
            acid_sel_short = f'Произвести  СКО {self.plast_combo}  в V  {self.acid_volume_edit}м3  ({self.acid_edit} -' \
                             f' {self.acid_proc_edit} %) '
        elif self.acid_edit == 'ВТ':

            vt = self.current_widget.sko_vt_edit.text()
            acid_sel = f'Произвести кислотную обработку {self.plast_combo} {vt} в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более' \
                       f' Р={self.pressure_edit}атм.'
            acid_sel_short = vt
        elif self.acid_edit == 'HF':

            acid_sel = f'Произвести кислотную обработку пласта {self.plast_combo} в объеме  {self.acid_volume_edit}м3 ' \
                       f'(концентрация в смеси HF 3% / HCl 13%){iron_str} силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления ' \
                       f'закачки не более Р={self.pressure_edit}атм.'
            acid_sel_short = f'Произвести ГКО пласта {self.plast_combo}  в V- {self.acid_volume_edit}м3  ' \
                             f'не более Р={self.pressure_edit}атм.'
        elif self.acid_edit == 'Нефтекислотка':
            acid_sel = f'Произвести нефтекислотную обработку пласта {self.plast_combo} в V=2тн товарной нефти +' \
                       f' {self.acid_volume_edit}м3  (HCl - {self.acid_proc_edit} %) + {float(self.acid_oil_proc_edit) - 2}т товарной ' \
                       f'нефти  {iron_str} силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.pressure_edit}атм.'
            acid_sel_short = f'нефтекислотную обработку пласта {self.plast_combo} в V=2тн товарной нефти +' \
                             f' {self.acid_volume_edit}м3  (HCl - {self.acid_proc_edit} %) + {float(self.acid_oil_proc_edit) - 2}т ' \
                             f'товарной нефти '
        elif self.acid_edit == 'Противогипсовая обработка':
            acid_sel = f'Произвести противогипсовую обработку пласта{self.plast_combo} в объеме {self.acid_volume_edit}м3 - ' \
                       f'{20}% раствором каустической соды' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={self.pressure_edit}атм.\n'
            acid_sel_short = f'Произвести противогипсовую обработку пласта{self.plast_combo} в объеме ' \
                             f'{self.acid_volume_edit}м3 - {20}% не ' \
                             f'более Р={self.pressure_edit}атм.\n'
            # print(f'Ожидаемое показатели {self.data_well.expected_pick_up.values()}')
        layout_select = f'посадить пакер на глубине {self.paker_depth}м'

        if self.__class__.__name__ == 'AcidPakerWindow':
            if self.paker_layout_combo in ['воронка', 'пакер с заглушкой', 'без монтажа компоновки на спуск']:
                layout_select = 'Закрыть затрубное пространство'
            if 'одно' in self.paker_layout_combo:
                layout_select = f'посадить пакер на глубине {self.paker_depth}м'
            elif 'дву' in self.paker_layout_combo:
                layout_select = f'посадить пакера на глубине {self.paker_depth}/{self.paker2_depth}м'

        acid_list_1 = [
            [acid_sel_short, None,
             f'{acid_sel}'
             f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', None],
            [None, None,
             f"Закачать кислоту в объеме V={round(volume_vn_nkt(self.dict_nkt), 1)}м3 (внутренний "
             f"объем НКТ)" if self.acid_volume_edit > volume_vn_nkt(self.dict_nkt)
             else f"Закачать кислоту в "
                  f"объеме {round(self.acid_volume_edit, 1)}м3, "
                  f"довести кислоту тех жидкостью в объеме "
                  f"{round(volume_vn_nkt(self.dict_nkt) - self.acid_volume_edit, 1)}м3 ",
             None, None, None, None, None, None, None,
             'мастер КРС', 1.25],
            [None, None,
             layout_select,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [None, None,
             ''.join(
                 [f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(self.dict_nkt) + 0.5, 1)}м3 '
                  f'при давлении не '
                  f'более {self.data_well.max_admissible_pressure.get_value}атм. Увеличение давления согласовать'
                  f' с заказчиком' if self.acid_volume_edit < volume_vn_nkt(
                     self.dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме '
                                         f'{round(self.acid_volume_edit - volume_vn_nkt(self.dict_nkt), 1)}м3 и тех '
                                         f'жидкостью '
                                         f'в объеме {round(volume_vn_nkt(self.dict_nkt) + 0.5, 1)}м3 '
                                         f'при давлении '
                                         f'не более {self.data_well.max_admissible_pressure.get_value}атм. '
                                         f'Увеличение давления согласовать с заказчиком\n'
                                         f'(в случае поглощения произвести продавку в '
                                         f'V-{round(volume_vn_nkt(self.dict_nkt) * 1.5, 1)}м3 '
                                         f'(1.5-ом объеме НКТ)) ']),
             None, None, None, None, None, None, None,
             'мастер КРС', 6],
            [f'без реагирования' if (
                    self.data_well.region == 'ТГМ' and self.acid_edit == 'HF') else 'реагирование 2 часа.', None,
             f'без реагирования' if (
                     self.data_well.region == 'ТГМ' and self.acid_edit == 'HF') else 'реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС', '' if (self.data_well.region == 'ТГМ' and self.acid_edit == 'HF') else 2],
            [f'Срыв 30мин', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [self.flushing_downhole(self.paker_layout_combo)[1], None,
             self.flushing_downhole(self.paker_layout_combo)[0],
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(well_volume(self, self.data_well.current_bottom))]
        ]
        if self.paker_layout_combo in ['воронка', 'без монтажа компоновки на спуск']:
            acid_list_1.pop(-2)

        for row in acid_list_1:
            paker_list.append(row)

        if self.Qplast_after_edit == 'ДА':

            paker_list.append([f'{layout_select}. насыщение 5м3', None,
                               f'{layout_select}. Произвести насыщение скважины до стабилизации '
                               f'давления закачки не менее 5м3. Опробовать  '
                               f'пласт {self.plast_combo} на приемистость в трех режимах при Р='
                               f'{self.pressure_three}атм в присутствии '
                               f'представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                               f'подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {self.expected_pickup}м3/сут при '
                               f'давлении {self.expected_pressure}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list

        # Определение трех режимов давлений при определении приемистости

    def read_update_need_swab(self, current_widget):
        try:

            self.swab_type_combo = current_widget.swab_type_combo.currentText()

            self.swab_paker_depth = current_widget.swab_paker_depth.text()
            if self.swab_paker_depth != '':
                self.swab_paker_depth = int(float(self.swab_paker_depth))

            self.swab_volume_edit = current_widget.swab_volume_edit.text()
            if self.swab_volume_edit != '':
                self.swab_volume_edit = int(float(self.swab_volume_edit))
            return True
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка сохранения данных сваба {e}')
            return False

    def select_diameter_nkt(self, paker_depth, swab_true_edit_type):
        nkt_diam = 73
        nkt_pod = '73мм'
        template_nkt_diam = '59.6мм'
        if self.data_well:
            if self.data_well.column_additional is True and \
                    110 > float(self.data_well.column_additional_diameter.get_value) and \
                    paker_depth > self.data_well.head_column_additional.get_value > 1000:
                nkt_diam = 73
                nkt_pod = '60'
                template_nkt_diam = '59.6мм, 47.9мм'
            elif self.data_well.column_additional is True and float(
                    self.data_well.column_additional_diameter.get_value) > 110 and \
                    paker_depth > self.data_well.head_column_additional.get_value:
                nkt_diam = 73
                nkt_pod = '73мм со снятыми фасками'
                template_nkt_diam = '59.6'
            elif self.data_well.column_additional and self.data_well.head_column_additional.get_value <= 1000 and \
                    swab_true_edit_type == 'Нужно освоение':
                nkt_list = ["60", "73"]
                nkt_diam, ok = QInputDialog.getItem(self, 'выбор диаметра НКТ',
                                                    'динамический уровень в скважине ниже головы хвостовика,'
                                                    'Выберете диаметр НКТ', nkt_list, 0, False)
                nkt_pod = '60мм'
                template_nkt_diam = '59.6мм, 47.9мм'
            elif self.data_well.column_additional and self.data_well.column_additional_diameter.get_value < 110:
                nkt_diam = '73мм'
                nkt_pod = '60мм'
                template_nkt_diam = '59.6мм, 47.9мм'

            elif self.data_well.column_additional is False and self.data_well.column_diameter.get_value < 110:
                nkt_diam = 60
                nkt_pod = '60мм'
                template_nkt_diam = '47.9мм'

        return nkt_diam, nkt_pod, template_nkt_diam

    def skv_acid_work(self):

        skv_list = [

            [f'СКВ {self.skv_acid_edit} {self.skv_proc_edit}%', None,
             f'Произвести установку СКВ {self.skv_acid_edit} {self.skv_proc_edit}% концентрации '
             f'в объеме'
             f' {self.skv_volume_edit}м3 ({round(self.skv_volume_edit * 1.12 * self.skv_proc_edit / 24, 2)}т HCL 24%) (по спец. плану, '
             f'составляет старший мастер)',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.5],
            [None, None,
             f'закачать {self.skv_acid_edit} {self.skv_proc_edit}% в объеме V={self.skv_volume_edit}м3; довести кислоту до пласта '
             f'тех.жидкостью в объеме {volume_vn_nkt(self.dict_nkt)}м3 . ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.6],
            [f'реагирование 2 часа.', None, f'реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 2],
            [f'Промывка, Q(повторно)', None,
             f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
             f'кратном объеме. Определить приемистость пласта в присутствии '
             f'представителя ЦДНГ (составить акт). '
             f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
             f'методом дренирования.',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]
        ]
        self.calculate_chemistry(self.skv_acid_edit, self.skv_volume_edit)
        return skv_list

    def swab_select(self):
        if self.swab_type_combo == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            swab_select = f'Произвести  геофизические исследования пласта {self.plast_combo} по технологической ' \
                          f'задаче № 2.1.13 Определение профиля ' \
                          f'и состава притока, дебита, источника обводнения и технического состояния ' \
                          f'эксплуатационной колонны и НКТ ' \
                          f'после свабирования с отбором жидкости не менее {self.swab_volume_edit}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {self.swab_volume_edit - 10}, ' \
                          f'{self.swab_volume_edit - 5}, {self.swab_volume_edit}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'сваб не менее {self.swab_volume_edit}м3 + профиль притока'
        elif self.swab_type_combo == 'Задача №2.1.14':
            swab_select = f'Произвести  геофизические исследования {self.plast_combo} по технологической задаче № 2.1.14 ' \
                          f'Определение профиля и состава притока, дебита, источника обводнения и технического ' \
                          f'состояния эксплуатационной колонны и НКТ с использованием малогабаритного пакерного ' \
                          f'расходомера (РН) после свабирования не менее {self.swab_volume_edit}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {self.swab_volume_edit - 10}, ' \
                          f'{self.swab_volume_edit - 5}, {self.swab_volume_edit}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'сваб не менее {self.swab_volume_edit}м3 + профиль притока Малогабаритный прибор'

        elif self.swab_type_combo == 'Задача №2.1.16':
            swab_select = f'Произвести  геофизические исследования {self.plast_combo} по технологической задаче № 2.1.16 ' \
                          f'Определение дебита и ' \
                          f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного ' \
                          f'давления после освоения ' \
                          f'свабированием  не менее {self.swab_volume_edit}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {self.swab_volume_edit - 10}, ' \
                          f'{self.swab_volume_edit - 5}, {self.swab_volume_edit}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'сваб не менее {self.swab_volume_edit}м3 + КВУ, ВНР'
        elif self.swab_type_combo == 'Задача №2.1.11':
            swab_select = f'Произвести  геофизические исследования {self.plast_combo} по технологической задаче № 2.1.11' \
                          f' свабирование в объеме не ' \
                          f'менее  {self.swab_volume_edit}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба ' \
                          f'(объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'
            swab_short = f'сваб не менее {self.swab_volume_edit}м3'

        elif self.swab_type_combo == 'Задача №2.1.16 + герметичность пакера':
            swab_select = f'Произвести фоновую запись. Понизить до стабильного динамического уровня. ' \
                          f'Произвести записи по определению герметичности пакера. При герметичности произвести ' \
                          f'геофизические исследования {self.plast_combo} по технологической задаче № 2.1.16' \
                          f'свабирование в объеме не менее  {self.swab_volume_edit}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба ' \
                          f'(объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'
            swab_short = f'сваб не менее {self.swab_volume_edit}м3'

        elif self.swab_type_combo == 'ГРР':
            swab_select = f'Провести освоение объекта {self.plast_combo} свабированием ' \
                          f'(объем согласовать с ОГРР) не менее ' \
                          f'{self.swab_volume_edit}м3 с отбором поверхностных ' \
                          f'проб через каждые 5м3 сваб и передачей представителю ЦДНГ, выполнить ' \
                          f'прослеживание уровней ' \
                          f'и ВНР с регистрацией КВУ глубинными манометрами, записать профиль притока, в случае ' \
                          f'получения притока нефти отобрать глубинные пробы (при выполнении условий отбора), ' \
                          f'провести ГДИС (КВДз).'
            swab_short = f'сваб профиль не менее ' \
                         f'{self.swab_volume_edit}'

        return swab_short, swab_select

    def flushing_downhole(self, paker_layout):

        self.data_well.fluid_work_short = self.data_well.fluid_work[:4]

        if 'одно' in paker_layout:
            if (self.data_well.perforation_roof - 5 + self.paker_khost >= self.data_well.current_bottom) or \
                    (all([self.data_well.dict_perforation[plast]['отрайбировано'] for plast in
                          self.data_well.plast_work])):
                flushing_downhole_list = f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                         f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                         f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ. \n' \
                                         f'При наличии ЦИРКУЛЯЦИИ: Допустить компоновку до глубины ' \
                                         f'{self.data_well.current_bottom}м. ' \
                                         f'Промыть скважину обратной промывкой ' \
                                         f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                         f'ри расходе жидкости не ' \
                                         f'менее 6-8 л/сек в объеме не менее ' \
                                         f'{round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 ' \
                                         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ. '
                flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить ' \
                                          f'до Н- {self.data_well.current_bottom}м. ' \
                                          f'Промыть уд.весом ' \
                                          f'{self.data_well.fluid_work[:4]}' \
                                          f'не менее {round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 '

            elif self.data_well.perforation_roof - 5 + self.paker_khost < self.data_well.current_bottom:
                flushing_downhole_list = f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                         f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                         f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ\n' \
                                         f'При наличии ЦИРКУЛЯЦИИ: Допустить пакер до глубины ' \
                                         f'{int(self.data_well.perforation_roof - 5)}м. ' \
                                         f'(на 5м выше кровли интервала перфорации), низ НКТ до глубины' \
                                         f' {self.data_well.perforation_roof - 5 + self.paker_khost}м) ' \
                                         f'Промыть скважину обратной промывкой по круговой циркуляции ' \
                                         f'жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости не ' \
                                         f'менее 6-8 л/сек в объеме не менее ' \
                                         f'{round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 ' \
                                         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ. \n' \
                                         f'в случае ГНО с НВ промывку от забоя делаем с допуском замковой опоры, ' \
                                         f'в случае НН и ЭЦН и наличия пакера в компоновке выполняем отдельное ' \
                                         f'СПО пера для вымыва продуктов реакции'

                flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить пакер до H- ' \
                                          f'{int(self.data_well.perforation_roof - 5)}м. ' \
                                          f' низ НКТ до H' \
                                          f' {self.data_well.perforation_roof - 5 + self.paker_khost}м) ' \
                                          f'Промыть уд.весом {self.data_well.fluid_work} не менее ' \
                                          f'{round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 ' \
                                          f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                          f'При отсутствии циркуляции на скважине промывку исключить, ' \
                                          f'увеличить объем продавки кислотного состава в 1,5 кратном объеме НКТ'
        elif 'ворон' in paker_layout:
            flushing_downhole_list = f'При наличии ЦИРКУЛЯЦИИ: Допустить компоновку до глубины ' \
                                     f'{self.data_well.current_bottom}м.' \
                                     f' Промыть скважину обратной промывкой ' \
                                     f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                     f'ри расходе жидкости не ' \
                                     f'менее 6-8 л/сек в объеме не менее ' \
                                     f'{round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 ' \
                                     f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.' \
                                     f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                     f'При отсутствии циркуляции произвести замещения продуктов реакции тех ' \
                                     f'жидкостью большей плотностью с последующей промывкой'

            flushing_downhole_short = f'При наличии ЦИРКУЛЯЦИИ: Допустить до Н- {self.data_well.current_bottom}м. Промыть уд.весом ' \
                                      f'{self.data_well.fluid_work}' \
                                      f'не менее {round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 '
        else:
            flushing_downhole_list = f'При наличии ЦИРКУЛЯЦИИ: При наличии избыточного давления:' \
                                     f'Промыть скважину обратной промывкой ' \
                                     f'по круговой циркуляции  жидкостью уд.весом {self.data_well.fluid_work} п' \
                                     f'ри расходе жидкости не ' \
                                     f'менее 6-8 л/сек в объеме не менее ' \
                                     f'{round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 ' \
                                     f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.' \
                                     f'МЕРОПРИЯТИЯ ПОСЛЕ ОПЗ: \n' \
                                     f'При отсутствии циркуляции произвести замещения продуктов реакции тех ' \
                                     f'жидкостью большей плотностью с последующей промывкой'
            flushing_downhole_short = f'При наличии избыточного давления: Промыть уд.весом ' \
                                      f'{self.data_well.fluid_work_short} ' \
                                      f'не менее {round(well_volume(self, self.paker_depth + self.paker_khost) * 1.5, 1)}м3 '

        return flushing_downhole_list, flushing_downhole_short

    @staticmethod
    def calculate_time_ozc(roof_rir_edit):
        if roof_rir_edit >= 1300:
            string = f'ОЗЦ 24 часа: (по качеству пробы) с момента срезки В случае не получения ' \
                     f'технологического "СТОП" ОЗЦ без давления.'
            string_short = 'ОЗЦ 24 часа'
            time = 24

        else:
            string = f'ОЗЦ 12-16 часа: (по качеству пробы) с момента срезки В случае не получения ' \
                     f'технологического "СТОП" ОЗЦ без давления.'
            string_short = 'ОЗЦ 12-16 часа'
            time = 16
        return string_short, string, time

    def read_sko_need(self, current_widget):
        try:
            self.QplastEdit = current_widget.QplastEdit.currentText()
            self.acid_edit = current_widget.acid_edit.currentText()
            self.acid_volume_edit = current_widget.acid_volume_edit.text().replace(",", ".")
            if self.acid_volume_edit != '':
                self.acid_volume_edit = float(self.acid_volume_edit.replace(",", "."))
            self.acid_proc_edit = current_widget.acid_proc_edit.text()
            if self.acid_proc_edit != '':
                self.acid_proc_edit = int(float(self.acid_proc_edit.replace(",", ".")))
            self.acid_oil_proc_edit = current_widget.acid_oil_proc_edit.text()
            if self.acid_oil_proc_edit != '':
                self.acid_oil_proc_edit = float(self.acid_oil_proc_edit.replace(",", "."))
            self.iron_volume_edit = current_widget.iron_volume_edit.text().replace(",", ".")
            if self.iron_volume_edit != '':
                self.iron_volume_edit = float(self.iron_volume_edit)
            self.expected_pressure = current_widget.expected_pressure_edit.text()
            self.expected_pickup = current_widget.expected_pickup_edit.text()
            self.pressure_three = current_widget.pressure_three_edit.text()
            self.pressure_edit = current_widget.pressure_edit.text()
            self.Qplast_after_edit = current_widget.Qplast_after_edit.currentText()
            self.iron_true_combo = current_widget.iron_true_combo.currentText()
            return True
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка в обработке данных СКО {e}')
            return False

    def testing_pressure(self, depth):

        interval_list = []

        for plast in self.data_well.plast_all:
            if self.data_well.dict_perforation[plast]['отключение'] is False:
                for interval in self.data_well.dict_perforation[plast]['интервал']:
                    if interval[0] < self.data_well.current_bottom:
                        interval_list.append(interval)

        if self.data_well.leakiness is True:
            for nek in self.data_well.dict_leakiness['НЭК']['интервал']:
                if self.data_well.dict_leakiness['НЭК']['интервал'][nek]['отключение'] is False and float(
                        nek.split('-')[0]) < depth:
                    interval_list.append(list(map(float, nek.split('-'))))

        if any([float(interval[1]) < float(depth) for interval in interval_list]):
            check_true = True
            testing_pressure_str = f'Закачкой тех жидкости в затрубное пространство при Р=' \
                                   f'{self.data_well.max_admissible_pressure.get_value}атм' \
                                   f' удостоверить в отсутствии выхода тех жидкости и герметичности пакера, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Закачкой в затруб при Р=' \
                                     f'{self.data_well.max_admissible_pressure.get_value}атм' \
                                     f' удостоверить в герметичности пакера'
        else:
            check_true = False
            testing_pressure_str = f'Опрессовать эксплуатационную колонну в интервале {depth}-0м на ' \
                                   f'Р={self.data_well.max_admissible_pressure.get_value}атм' \
                                   f' в течение 30 минут в присутствии представителя заказчика, составить акт. ' \
                                   f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                                   f'до начала работ)'
            testing_pressure_short = f'Опрессовать в {depth}-0м на Р={self.data_well.max_admissible_pressure.get_value}атм'

        return testing_pressure_str, testing_pressure_short, check_true

    def privyazka_nkt_work(self):

        priv_list = [[f'ГИС Привязка по ГК и ЛМ', None,
                      f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через РИТС {data_list.contractor}". '
                      f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №11 утвержденной главным инженером '
                      f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                      f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
                      None, None, None, None, None, None, None,
                      'Мастер КРС, подрядчик по ГИС', 4]]
        return priv_list

    def find_item_in_table(self, value):
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)  # Проверяем первый столбец
            if item and item.text() == str(value):
                return item
        return None

    def calc_fond_nkt(self, len_nkt: str, distance_between_nkt: str) -> List:

        # расчет необходимого давления опрессовки НКТ при спуске
        static_level = self.data_well.static_level.get_value
        fluid = float(self.data_well.fluid_work[:4].replace(',', '.').replace('г', ''))

        pressure = 40

        if self.data_well.dict_pump_ecn["after"] != "0":
            pressure = 50

        calc = CalcFond(static_level, len_nkt, fluid, pressure, distance_between_nkt)
        calc_fond_dict = calc.calc_pressure_list()
        press_str = f'В случае не завоза новых или завоза не опрессованных НКТ, согласовать алгоритм ' \
                    f'опрессовки с ЦДНГ,' \
                    f' произвести спуск  фондовых НКТ с поинтервальной опрессовкой через ' \
                    f'каждые {distance_between_nkt}м ' \
                    f'с учетом статического уровня уровня на на глубине {static_level}м  по телефонограмме заказчика ' \
                    f'в следующей последовательности:\n'
        n = 0
        for nkt, pressure in calc_fond_dict.items():
            press_str += f'Опрессовать НКТ в интервале {n} - {int(nkt)} на давление {pressure}атм \n'
            n = nkt

        return press_str

    def select_nkt_grp(self):

        if self.data_well.column_additional is False or \
                (self.data_well.column_additional is True and self.data_well.current_bottom >=
                 self.data_well.head_column_additional.get_value):
            return f'НКТ{self.data_well.nkt_diam}мм'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110:
            return f'НКТ60мм L- {round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 20, 0)}'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110:
            return f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками L- ' \
                   f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 20, 0)}'

    @staticmethod
    def difference_date_days(date1, today=data_list.current_date):
        # Задание дат
        date1 = datetime.strptime(date1, "%d.%m.%Y")

        # Вычисление разницы в днях
        difference = (today - date1).days

        return difference

    @staticmethod
    def read_excel_in_base(number_well, area_well, work_plan, type_kr):
        db = connection_to_database(decrypt("DB_WELL_DATA"))
        data_well_base = WorkDatabaseWell(db)

        data_well = data_well_base.read_excel_in_base(number_well, area_well, work_plan, type_kr)

        try:
            col_width = []
            dict_well = json.loads(data_well[len(data_well) - 1][0])
            data = dict_well['data']
            row_heights = dict_well['rowHeights']
            if 'colWidth' in list(dict_well.keys()):
                col_width = dict_well['colWidth']
            elif 'col_width' in list(dict_well.keys()):
                col_width = dict_well['col_width']
            boundaries_dict = dict_well['merged_cells']

        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Введены не все параметры {type(e).__name__}\n\n{str(e)}')
            return

        return data, row_heights, col_width, boundaries_dict

    def extraction_data(self, table_name, paragraph_row=0):
        date_table = table_name.split(' ')[-1]
        well_number = table_name.split(' ')[0]
        well_area = table_name.split(' ')[1]
        type_kr = table_name.split(' ')[-4].replace('None', 'null')
        contractor_select = data_list.contractor
        work_plan = table_name.split(' ')[-3]

        db = connection_to_database(decrypt("DB_WELL_DATA"))
        data_well_base = WorkDatabaseWell(db, self.data_well)

        result_table = data_well_base.extraction_data(str(well_number), well_area, type_kr,
                                                      work_plan, date_table, contractor_select)

        if result_table is None:
            QMessageBox.warning(self, 'Ошибка',
                                f'В базе данных скв {well_number} {well_area} отсутствует данные, '
                                f'используйте excel вариант плана работ')
            return None

        if result_table[0]:
            result = json.loads(result_table[0])

            self.data_well.type_absorbent = 'EVASORB марки 121'
            if 'ХИМТЕХНО 101' in str(result[paragraph_row][7]):
                self.data_well.type_absorbent = 'ХИМТЕХНО 101 Марка А'
            elif 'СНПХ-1200' in str(result[paragraph_row][7]):
                self.data_well.type_absorbent = 'СНПХ-1200'
            elif 'ПСВ-3401' in str(result[paragraph_row][7]):
                self.data_well.type_absorbent = 'ПСВ-3401'
            elif 'Гастрит-К131М' in str(result[paragraph_row][7]):
                self.data_well.type_absorbent = 'Гастрит-К131М'


            from data_base.work_with_base import insert_data_well_dop_plan
            insert_data_well_dop_plan(self, result_table[1])

            self.data_well.type_kr = result_table[2]
            if result_table[3]:
                dict_data_well = json.loads(result_table[3])
                # self.data_well.dict_category
                pressure = namedtuple("pressure", "category data_pressure")
                Data_h2s = namedtuple("Data_h2s", "category data_percent data_mg_l poglot")
                Data_gaz = namedtuple("Data_gaz", "category data")
                self.data_well.dict_category = {}
                self.data_well.category_pressure_list = []
                self.data_well.category_h2s_list = []
                self.data_well.category_gaz_factor_percent = []
                for plast, plast_data in dict_data_well.items():
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по давлению',
                        pressure(*dict_data_well[plast]['по давлению']))
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по сероводороду', Data_h2s(*dict_data_well[plast]['по сероводороду']))
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по газовому фактору', Data_gaz(*dict_data_well[plast]['по газовому фактору']))

                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'отключение', dict_data_well[plast]['отключение'])

                    self.data_well.category_pressure_list.append(plast_data['по давлению'][0])
                    self.data_well.category_h2s_list.append(plast_data['по сероводороду'][0])
                    self.data_well.category_gaz_factor_percent.append(plast_data['по газовому фактору'][0])

            if self.data_well.work_plan in ['dop_plan', 'dop_plan_in_base']:
                data = self.insert_data_dop_plan(result, paragraph_row)
                if data is None:
                    return None
            elif self.data_well.work_plan == 'plan_change':
                data = self.insert_data_plan(result)
                if data is None:
                    return None
            data_list.data_well_is_True = True

        else:
            data_list.data_in_base = False
            QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                f"Таблицы '{table_name}' нет в базе данных.")

        return True

    def insert_data_plan(self, result):
        self.data_well.data_list = []
        self.data_well.gips_in_well = False
        self.data_well.drilling_interval = []
        self.data_well.for_paker_list = False
        self.data_well.grp_plan = False
        self.data_well.angle_data = []
        self.data_well.nkt_opress_true = False
        self.data_well.plast_project = []
        self.data_well.drilling_interval = []
        self.data_well.dict_perforation_project = {}
        self.data_well.bvo = False
        self.data_well.fluid_work = result[0][7]
        self.data_well.fluid_work_short = result[0][7]

        self.data_well.fluid = float(result[0][7][:4].replace('г', ''))
        self.data_well.stabilizator_need = False
        self.data_well.current_bottom_second = 0

        for ind, row in enumerate(result):
            if ind == 1:
                self.data_well.bottom = row[1]
                self.data_well.category_pressure_second = row[8]
                self.data_well.category_h2s_second = row[9]
                self.data_well.gaz_factor_pr_second = row[10]

                self.data_well.plast_work_short = json.dumps(row[3], ensure_ascii=False)

            data_in_base_list = []
            for index, data in enumerate(row):
                if index == 6:
                    if data == 'false' or data == 0 or data == '0':
                        data = False
                    else:
                        data = True
                data_in_base_list.append(data)
            self.data_well.data_list.append(data_in_base_list)
        self.data_well.current_bottom = result[ind][1]
        self.data_well.dict_perforation = json.loads(result[ind][2])

        self.data_well.plast_all = json.loads(result[ind][3])
        self.data_well.plast_work = json.loads(result[ind][4])
        self.data_well.dict_leakiness = json.loads(result[ind][5])
        self.data_well.leakiness = False
        self.data_well.leakiness_interval = []
        if self.data_well.dict_leakiness:
            self.data_well.leakiness = True
            self.data_well.leakiness_interval = list(self.data_well.dict_leakiness['НЭК']['интервал'].keys())


        self.data_well.category_pressure = result[ind][8]
        self.data_well.category_pvo = 2

        self.data_well.category_h2s = result[ind][9]
        self.data_well.category_gas_factor = result[ind][10]
        asded = str(result[ind][8]) == '1', str(result[ind][9]) == '1', str(result[ind][10])
        if str(result[ind][8]) == '1' or str(result[ind][9]) == '1' or str(result[ind][10]) == '1':
            self.data_well.bvo = True
        if str(self.data_well.category_pressure) == '1' or str(self.data_well.category_h2s) == '1' \
                or self.data_well.category_gas_factor == '1':
            self.data_well.category_pvo = 1

        self.data_well.template_depth, self.data_well.template_length, \
        self.data_well.template_depth_addition, self.data_well.template_length_addition = \
            json.loads(result[ind][11])

        self.data_well.skm_interval = json.loads(result[ind][12])

        self.data_well.problem_with_ek_depth = result[ind][13]
        self.data_well.problem_with_ek_diameter = result[ind][14]
        try:
            self.data_well.head_column = ProtectedIsDigit(result[ind][16])
        except Exception:
            print('отсутствуют данные по голове хвостовика')
        self.data_well.dict_perforation_short = json.loads(result[ind][2])

        try:
            self.data_well.ribbing_interval = json.loads(result[ind][15])
        except Exception:
            print('отсутствуют данные по интервалам райбирования')

        definition_plast_work(self)
        return True

    @staticmethod
    def calculate_angle(max_depth_pvr, angle_data):
        tuple_angle = ()
        for depth, angle, _ in angle_data:
            asdfg = abs(float(depth) - float(max_depth_pvr))
            if abs(float(depth) - float(max_depth_pvr)) < 20:
                tuple_angle = depth, angle, f'Зенитный угол на глубине {depth}м равен {angle}гр'
        if tuple_angle:
            return tuple_angle

    def calc_work_fluid(self, fluid_work_insert):

        self.data_well.fluid_short = fluid_work_insert

        category_h2s_list = [
            self.data_well.dict_category[plast]['по сероводороду'].category
            for plast in list(
                self.data_well.dict_category.keys()) if self.data_well.dict_category[plast]['отключение'] == 'рабочий']

        if 2 in category_h2s_list or 1 in category_h2s_list:
            expenditure_h2s_list = []
            if self.data_well.plast_work:
                try:
                    for _ in self.data_well.plast_work:
                        poglot = [self.data_well.dict_category[plast]['по сероводороду'].poglot for plast in
                                  list(self.data_well.dict_category.keys())
                                  if self.data_well.dict_category[plast]['по сероводороду'].category in [1, 2]][
                            0]
                        expenditure_h2s_list.append(poglot)
                except ValueError:
                    pass
            else:
                expenditure_h2s, _ = QInputDialog.getDouble(self, 'Расчет поглотителя',
                                                            'Отсутствуют рабочие пласты, нужно ввести '
                                                            'необходимый расчет поглотителя', 0.01, 0, 10, 2)

            expenditure_h2s = round(max(expenditure_h2s_list), 3)
            fluid_work = f'{fluid_work_insert}г/см3 с добавлением поглотителя сероводорода ' \
                         f'{self.data_well.type_absorbent} из ' \
                         f'расчета {expenditure_h2s}л/м3 либо аналог '
            fluid_work_short = f'{fluid_work_insert}г/см3 c ' \
                               f'{self.data_well.type_absorbent} - {expenditure_h2s}л/м3 '
        else:
            fluid_work = f'{fluid_work_insert}г/см3 '
            fluid_work_short = f'{fluid_work_insert}г/см3'

        return fluid_work, fluid_work_short

    def read_update_skv(self, current_widget):
        try:
            self.skv_acid_edit = current_widget.skv_acid_edit.currentText()
            self.skv_volume_edit = current_widget.skv_volume_edit.text()
            if self.skv_volume_edit != '':
                self.skv_volume_edit = float(self.skv_volume_edit)
            self.skv_proc_edit = current_widget.skv_proc_edit.text()
            if self.skv_proc_edit != '':
                self.skv_proc_edit = int(float(self.skv_proc_edit))
            self.pressure_edit = current_widget.pressure_edit.text()
            if self.pressure_edit != '':
                self.pressure_edit = int(float(self.pressure_edit))
            return True
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'ошибка в прочтении данных СКВ {e}')
            return False

    def pvo_gno(self, kat_pvo):
        self.text_pvo = f'{self.data_well.max_expected_pressure.get_value}атм (на максимально ожидаемое ' \
                        f'давление в течении 30мин, но не менее 30атм )'
        if self.data_well.curator == 'ВНС':
            self.text_pvo = f'{self.data_well.max_expected_pressure.get_value * 1.1:.1f}атм. ' \
                            f'(на максимально ожидаемое давление в течении ' \
                            f'30мин +10% на скважинах освоения), но не менее 30атм '

        date_str = data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]

        # print(f' ПВО {kat_pvo}')
        pvo_2 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} (тип плашечный ' \
                f'сдвоенный ПШП-2ФТ-152х21) и посадить пакер. ' \
                f'Спустить пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и ' \
                f'линии манифольда до концевых ' \
                f'задвижек на Р-{self.text_pvo} на максимально ' \
                f'допустимое давление ' \
                f'опрессовки эксплуатационной колонны в течении ' \
                f'30мин), сорвать пакер. '

        pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} ' \
                f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
                f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
                f' (при необходимости произвести монтаж переводника' \
                f' П178х168 или П168 х 146 или ' \
                f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
                f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на ' \
                f'Р-{self.text_pvo} сорвать и извлечь пакер. Опрессовать выкидную линию после концевых задвижек на ' \
                f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на ' \
                f'давление до 210 кгс/см2 ((21 МПа)\n' \
                f'- Обеспечить обогрев превентора и СУП в зимнее время . \n Получить разрешение на ' \
                f'производство работ в ' \
                f'присутствии представителя ПФС'
        if kat_pvo == 1:
            return pvo_1, f'Монтаж ПВО по схеме №2 + ГидроПревентор'
        else:
            # print(pvo_2)
            return pvo_2, f'Монтаж ПВО по схеме №2'
