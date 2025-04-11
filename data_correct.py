import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QGridLayout, QMessageBox, QWidget, QPushButton, QApplication
from find import FindIndexPZ
import data_list
import re

from perforation_correct import FloatLineEdit
from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion


class TabPageSoCorrect(TabPageUnion):
    def __init__(self, data_well: FindIndexPZ):
        super().__init__(data_well)

        self.data_well = data_well
        self.labels_nkt = {}
        self.labels_nkt_po = {}
        self.labels_sucker = {}
        self.labels_sucker_po = {}

        self.column_direction_diameter_Label = QLabel("диаметр направление ", self)
        self.column_direction_diameter_edit = FloatLineEdit()
        if self.data_well.column_direction_true:
            self.column_direction_diameter_edit.setText(
                f'{str(self.data_well.column_direction_diameter.get_value).strip()}')
        else:
            self.column_direction_diameter_edit.setText(f'отсут')

        self.column_direction_wall_thickness_Label = QLabel("Толщина \nстенки", self)
        self.column_direction_wall_thickness_edit = FloatLineEdit()
        if self.data_well.column_direction_true:
            self.column_direction_wall_thickness_edit.setText(
                f'{str(self.data_well.column_direction_wall_thickness.get_value).strip()}')
        else:
            self.column_direction_wall_thickness_edit.setText(f'отсут')
        self.column_direction_length_Label = QLabel("башмак направления", self)
        self.column_direction_length_edit = FloatLineEdit()
        if self.data_well.column_direction_true:
            self.column_direction_length_edit.setText(
                f'{str(self.data_well.column_direction_length.get_value).strip()}')
        else:
            self.column_direction_length_edit.setText(f'отсут')

        self.level_cement_direction_Label = QLabel("Уровень \nцемента", self)
        self.level_cement_direction_edit = FloatLineEdit()
        if self.data_well.column_direction_true:
            self.level_cement_direction_edit.setText(
                f'{str(self.data_well.level_cement_direction.get_value).strip()}')
        else:
            self.level_cement_direction_edit.setText(f'отсут')

        self.column_conductor_diameter_Label = QLabel("диаметр \nкондуктора", self)
        self.column_conductor_diameter_edit = FloatLineEdit()
        self.column_conductor_diameter_edit.setText(
            f'{str(self.data_well.column_conductor_diameter.get_value).strip()}')

        self.column_conductor_wall_thickness_Label = QLabel("Толщина \nстенки ", self)
        self.column_conductor_wall_thickness_edit = FloatLineEdit()
        self.column_conductor_wall_thickness_edit.setText(
            f'{str(self.data_well.column_conductor_wall_thickness.get_value).strip()}')

        self.well_number_label = QLabel('номер \nскважины')
        self.well_number_edit = QLineEdit(self)
        self.well_number_edit.setText(self.data_well.well_number.get_value)

        self.well_area_label = QLabel('площадь')
        self.well_area_line = QLineEdit(self)
        self.well_area_line.setText(self.data_well.well_area.get_value)

        self.well_oilfield_label = QLabel('месторождение')
        self.well_oilfield_line = QLineEdit(self)
        self.well_oilfield_line.setText(self.data_well.well_oilfield.get_value)

        self.appointment_well_label = QLabel('назначение')
        self.appointment_well_line = QLineEdit(self)
        self.appointment_well_line.setText(self.data_well.appointment_well.get_value)

        self.column_conductor_length_Label = QLabel("башмак кондуктора", self)
        self.column_conductor_length_edit = FloatLineEdit()
        self.column_conductor_length_edit.setText(
            f'{str(self.data_well.column_conductor_length.get_value).strip()}')

        self.level_cement_conductor_Label = QLabel("Уровень \nцемента", self)
        self.level_cement_conductor_edit = FloatLineEdit()
        self.level_cement_conductor_edit.setText(f'{str(self.data_well.level_cement_conductor.get_value).strip()}')

        self.column_label = QLabel("диаметр ЭК", self)
        self.column_type = FloatLineEdit()
        self.column_type.setText(f'{self.ifNone(self.data_well.column_diameter.get_value)}')

        # self.column_type.setClearButtonEnabled(True)

        self.column_wall_thickness_label = QLabel("Толщина \nстенки ЭК", self)
        self.column_wall_thickness_edit_type2 = FloatLineEdit()
        self.column_wall_thickness_edit_type2.setText(
            f'{self.ifNone(self.data_well.column_wall_thickness.get_value)}')
        # self.column_wall_thickness_edit_type2.setClearButtonEnabled(True)

        self.head_column_label = QLabel("Голова ЭК", self)
        self.head_column_edit_type2 = FloatLineEdit()
        self.head_column_edit_type2.setText(f'{0}')

        self.shoe_column_label = QLabel("башмак ЭК", self)
        self.shoe_column_edit_type2 = FloatLineEdit()
        self.shoe_column_edit_type2.setText(f'{self.ifNone(self.data_well.shoe_column.get_value)}')

        self.level_cement_label = QLabel("Высота цемента \nза колонной", self)
        self.level_cement_edit = FloatLineEdit()
        if '-' in str(self.data_well.level_cement_column.get_value):
            self.level_cement_edit.setText(self.ifNone(self.data_well.level_cement_column.get_value).split("-")[0].strip())
        else:
            self.level_cement_edit.setText(f'{self.ifNone(self.data_well.level_cement_column.get_value)}')
        # self.shoe_column_edit_type2.setClearButtonEnabled(True)

        self.column_add_trueLabel = QLabel("наличие \nдоп. колонны", self)
        self.column_add_true_comboBox = QComboBox(self)
        self.column_add_true_comboBox.addItems(['в наличии', 'отсутствует'])
        if self.data_well.column_additional is True:
            column_add = 0
        else:
            column_add = 1
        self.column_add_true_comboBox.setCurrentIndex(column_add)

        self.column_add_label = QLabel("диаметр \nдоп. колонны", self)
        self.column_add_edit_type = FloatLineEdit()
        self.column_add_edit_type.setText(f'{self.ifNone(self.data_well.column_additional_diameter.get_value)}')
        # self.column_add_edit_type.setClearButtonEnabled(True)

        self.column_add_wall_thicknessLabel = QLabel("Толщина стенки ", self)
        self.column_add_wall_thicknessedit_type2 = FloatLineEdit()
        self.column_add_wall_thicknessedit_type2.setText(
            f'{self.ifNone(self.data_well.column_additional_wall_thickness.get_value)}')
        # self.column_add_wall_thicknessedit_type2.setClearButtonEnabled(True)

        self.head_column_add_label = QLabel("Голова \nдоп колонны", self)
        self.head_column_add_edit_type2 = FloatLineEdit()
        self.head_column_add_edit_type2.setText(f'{self.ifNone(self.data_well.head_column_additional.get_value)}')

        self.shoe_column_add_label = QLabel("башмак \nдоп колонны", self)
        self.shoe_column_add_edit_type2 = FloatLineEdit()
        self.shoe_column_add_edit_type2.setText(f'{self.ifNone(self.data_well.shoe_column_additional.get_value)}')
        # self.shoe_column_add_edit_type2.setClearButtonEnabled(True)

        self.bottomhole_drill_Label = QLabel('Пробуренный забой')
        self.bottomhole_drill_edit_type = FloatLineEdit()


        self.bottomhole_drill_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.bottom_hole_drill.get_value))}')
        if self.bottomhole_drill_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указан пробуренный забой\n')

        self.bottomhole_artificial_Label = QLabel('Искусственный забой')
        self.bottomhole_artificial_edit_type = FloatLineEdit()
        self.bottomhole_artificial_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.bottom_hole_artificial.get_value))}')

        if self.bottomhole_artificial_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указан искусственный забой\n')

        self.current_bottom_Label = QLabel('Текущий забой')
        self.current_bottom_edit_type = FloatLineEdit()
        self.current_bottom_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.current_bottom))}')

        self.max_angle_Label = QLabel('Максимальный угол')
        self.max_angle_edit_type = FloatLineEdit()
        self.max_angle_edit_type.setText(f'{self.ifNone(self.data_well.max_angle.get_value)}')

        if self.max_angle_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указан максимальный угол\n')

        self.max_angle_depth_Label = QLabel('Глубина \nмаксимального угла')
        self.max_angle_depth_edit_type = FloatLineEdit()
        self.max_angle_depth_edit_type.setText(f'{self.ifNone(self.data_well.max_angle_depth.get_value)}')
        if  self.max_angle_depth_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указана глубина максимального угола\n')

        self.max_expected_pressure_Label = QLabel('Максимальный \nожидаемое давление')
        self.max_expected_pressure_edit_type = FloatLineEdit()
        self.max_expected_pressure_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.max_expected_pressure.get_value))}')
        if self.max_expected_pressure_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указана глубина максимального ожидаемое давление\n')

        self.max_admissible_pressure_Label = QLabel('Максимальный \nдопустимое давление')
        self.max_admissible_pressure_edit_type = FloatLineEdit()
        self.max_admissible_pressure_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.max_admissible_pressure.get_value))}')

        if self.max_admissible_pressure_edit_type.text() == 'отсут':
            self.data_well.check_data_in_pz.append('Не корректно указана глубина максимального допустимое давление\n')

        self.pump_SHGN_do_Label = QLabel('Штанговый насос')
        self.pump_SHGN_do_edit_type = QLineEdit(self)
        self.pump_SHGN_do_edit_type.setText(f'{self.ifNone(self.data_well.dict_pump_shgn["before"])}')

        self.pump_SHGN_depth_do_Label = QLabel('Глубина \nштангового насоса')
        self.pump_SHGN_depth_do_edit_type = FloatLineEdit()
        if self.pump_SHGN_do_edit_type.text() != 'отсут':
            self.pump_SHGN_depth_do_edit_type.setText(
                f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.dict_pump_shgn_depth["before"]))}')
        else:
            self.pump_SHGN_depth_do_edit_type.setText('отсут')

        self.pump_SHGN_posle_Label = QLabel('Плановый штанговый насос')
        self.pump_SHGN_posle_edit_type = QLineEdit(self)
        self.pump_SHGN_posle_edit_type.setText(f'{self.ifNone(self.data_well.dict_pump_shgn["after"])}')

        self.pump_SHGN_depth_posle_Label = QLabel('Плановая глубина \nспуска насоса')
        self.pump_SHGN_depth_posle_edit_type = FloatLineEdit()
        if self.pump_SHGN_posle_edit_type.text() != 'отсут':
            self.pump_SHGN_depth_posle_edit_type.setText(
                f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.dict_pump_shgn_depth["after"]))}')
        else:
            self.pump_SHGN_depth_posle_edit_type.setText('отсут')

        self.pump_ECN_do_Label = QLabel('Спущенный ЭЦН')
        self.pump_ECN_do_edit_type = QLineEdit(self)
        self.pump_ECN_do_edit_type.setText(f'{self.ifNone(self.data_well.dict_pump_ecn["before"])}')

        self.pump_ECN_depth_do_Label = QLabel('Глубина \nспуска ЭЦН')
        self.pump_ECN_depth_do_edit_type = FloatLineEdit()
        if self.pump_ECN_do_edit_type.text() != 'отсут':
            self.pump_ECN_depth_do_edit_type.setText(
                f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.dict_pump_ecn_depth["before"]))}')
        else:
            self.pump_ECN_depth_do_edit_type.setText('отсут')

        self.pump_ECN_posle_Label = QLabel('Плановый ЭЦН \nна спуск')
        self.pump_ECN_posle_edit_type = QLineEdit(self)
        self.pump_ECN_posle_edit_type.setText(f'{self.ifNone(self.data_well.dict_pump_ecn["after"])}')

        self.pump_ECN_depth_posle_Label = QLabel('Плановая глубина \nспуска ЭЦН')
        self.pump_ECN_depth_posle_edit_type = FloatLineEdit()
        if self.pump_ECN_posle_edit_type.text() != 'отсут':
            self.pump_ECN_depth_posle_edit_type.setText(
                f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.dict_pump_ecn_depth["after"]))}')
        else:
            self.pump_ECN_depth_posle_edit_type.setText('отсут')

        self.paker_do_Label = QLabel('Спущенный \nпакер')
        self.paker_do_edit_type = QLineEdit(self)
        self.paker_do_edit_type.setText(f'{self.ifNone(self.data_well.paker_before["before"])}')

        self.paker_depth_do_Label = QLabel('Глубина спуска \nпакера')
        self.paker_depth_do_edit_type = FloatLineEdit()
        self.paker_depth_do_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.depth_fond_paker_before["before"]))}')

        self.paker_posle_Label = QLabel('пакер на спуск')
        self.paker_posle_edit_type = QLineEdit(self)
        self.paker_posle_edit_type.setText(f'{self.ifNone(self.data_well.paker_before["after"])}')

        self.paker_depth_posle_Label = QLabel('Глубина спуска \nпакера')
        self.paker_depth_posle_edit_type = FloatLineEdit()
        self.paker_depth_posle_edit_type.setText(
            f'{self.remove_non_numeric_chars(self.ifNone(self.data_well.depth_fond_paker_before["after"]))}')

        self.paker2_do_Label = QLabel('Спущенный пакер')
        self.paker2_do_edit_type = QLineEdit(self)
        self.paker2_do_edit_type.setText(f'{self.ifNone(self.data_well.paker_second_before["before"])}')

        self.paker2_depth_do_Label = QLabel('Глубина спуска \nпакера')
        self.paker2_depth_do_edit_type = FloatLineEdit()
        self.paker2_depth_do_edit_type.setText(self.remove_non_numeric_chars(
            self.ifNone(str(self.data_well.depth_fond_paker_second_before["before"]))))

        self.paker2_posle_Label = QLabel('пакер на спуск')
        self.paker2_posle_edit_type = QLineEdit(self)
        # print(self.data_well.paker_second_before[self.ifNone("after")])
        self.paker2_posle_edit_type.setText(str(self.ifNone(self.data_well.paker_second_before["after"])))

        self.paker2_depth_posle_Label = QLabel('Глубина спуска пакера')
        self.paker2_depth_posle_edit_type = FloatLineEdit()
        self.paker2_depth_posle_edit_type.setText(
            self.remove_non_numeric_chars(self.ifNone(str(self.data_well.depth_fond_paker_second_before["after"]))))
        # print(f' насос спуск {data_list.pdict_pump["after"]}')

        self.static_level_Label = QLabel('Статический уровень \nв скважине')
        self.static_level_edit_type = FloatLineEdit()
        self.static_level_edit_type.setText(self.remove_non_numeric_chars(
            self.ifNone(self.data_well.static_level.get_value)))

        self.dinamic_level_Label = QLabel('Динамический уровень \nв скважине')
        self.dinamic_level_edit_type = FloatLineEdit()
        self.dinamic_level_edit_type.setText(self.remove_non_numeric_chars(
            self.ifNone(self.data_well.dinamic_level.get_value)))

        self.date_commissioning_Label = QLabel('Дата ввода в эксплуатацию')
        self.date_commissioning_line = QLineEdit(self)
        self.date_commissioning_line.setText(self.data_well.date_commissioning.get_value)

        self.result_pressure_date_label = QLabel('Дата последней опрессовки')
        self.result_pressure_date = QLineEdit(self)
        self.result_pressure_date.setText(self.data_well.result_pressure_date.get_value)

        self.curator_Label = QLabel('Куратор ремонта')
        self.curator_Combo = QComboBox(self)
        self.curator_Combo.setMinimumWidth(50)

        self.region_Label = QLabel('Регион')
        self.region_combo = QComboBox(self)

        self.type_kr_Label = QLabel('Вид и категория ремонта, его шифр')
        self.type_kr_combo = QComboBox(self)

        self.nkt_do_label = QLabel('НКТ  до ремонта')
        self.nkt_posle_label = QLabel('НКТ плановое согласно расчета')

        self.sucker_rod_label = QLabel('Штанги  до ремонта')
        self.sucker_rod_po_label = QLabel('Штанги плановое согласно расчета')

        self.dict_nkt = self.data_well.dict_nkt_before
        self.dict_nkt_po = self.data_well.dict_nkt_after
        # print(self.data_well.dict_nkt_before,  self.data_well.dict_nkt_after)

        self.dict_sucker_rod = self.data_well.dict_sucker_rod
        self.dict_sucker_rod_po = self.data_well.dict_sucker_rod_after

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.column_direction_diameter_Label, 0, 0)
        self.grid.addWidget(self.column_direction_diameter_edit, 1, 0)
        self.grid.addWidget(self.column_direction_wall_thickness_Label, 0, 1)
        self.grid.addWidget(self.column_direction_wall_thickness_edit, 1, 1)
        self.grid.addWidget(self.column_direction_length_Label, 0, 2)
        self.grid.addWidget(self.column_direction_length_edit, 1, 2)
        self.grid.addWidget(self.level_cement_direction_Label, 0, 4)
        self.grid.addWidget(self.level_cement_direction_edit, 1, 4)
        self.grid.addWidget(self.well_number_label, 92, 2)
        self.grid.addWidget(self.well_number_edit, 93, 2)
        self.grid.addWidget(self.well_area_label, 92, 3)
        self.grid.addWidget(self.well_area_line, 93, 3)
        self.grid.addWidget(self.well_oilfield_label, 92, 4)
        self.grid.addWidget(self.well_oilfield_line, 93, 4)
        self.grid.addWidget(self.appointment_well_label, 92, 5)
        self.grid.addWidget(self.appointment_well_line, 93, 5)


        self.grid.addWidget(self.column_conductor_diameter_Label, 2, 0)
        self.grid.addWidget(self.column_conductor_diameter_edit, 3, 0)
        self.grid.addWidget(self.column_conductor_wall_thickness_Label, 2, 1)
        self.grid.addWidget(self.column_conductor_wall_thickness_edit, 3, 1)
        self.grid.addWidget(self.column_conductor_length_Label, 2, 2)
        self.grid.addWidget(self.column_conductor_length_edit, 3, 2)
        self.grid.addWidget(self.level_cement_conductor_Label, 2, 4)
        self.grid.addWidget(self.level_cement_conductor_edit, 3, 4)

        self.grid.addWidget(self.column_label, 8, 0)
        self.grid.addWidget(self.column_type, 9, 0)
        self.grid.addWidget(self.column_wall_thickness_label, 8, 1)
        self.grid.addWidget(self.column_wall_thickness_edit_type2, 9, 1)
        self.grid.addWidget(self.head_column_label, 8, 2)
        self.grid.addWidget(self.head_column_edit_type2, 9, 2)
        self.grid.addWidget(self.shoe_column_label, 8, 3)
        self.grid.addWidget(self.shoe_column_edit_type2, 9, 3)
        self.grid.addWidget(self.level_cement_label, 8, 4)
        self.grid.addWidget(self.level_cement_edit, 9, 4)

        self.grid.addWidget(self.column_add_trueLabel, 8, 5)
        self.grid.addWidget(self.column_add_true_comboBox, 9, 5)
        self.grid.addWidget(self.column_add_label, 8, 6)
        self.grid.addWidget(self.column_add_edit_type, 9, 6)
        self.grid.addWidget(self.column_add_wall_thicknessLabel, 8, 7)
        self.grid.addWidget(self.column_add_wall_thicknessedit_type2, 9, 7)
        self.grid.addWidget(self.head_column_add_label, 8, 8)
        self.grid.addWidget(self.head_column_add_edit_type2, 9, 8)
        self.grid.addWidget(self.shoe_column_add_label, 8, 9)
        self.grid.addWidget(self.shoe_column_add_edit_type2, 9, 9)

        self.grid.addWidget(self.bottomhole_drill_Label, 10, 0)
        self.grid.addWidget(self.bottomhole_drill_edit_type, 11, 0)
        self.grid.addWidget(self.bottomhole_artificial_Label, 10, 1)
        self.grid.addWidget(self.bottomhole_artificial_edit_type, 11, 1)
        self.grid.addWidget(self.current_bottom_Label, 10, 2)
        self.grid.addWidget(self.current_bottom_edit_type, 11, 2)
        self.grid.addWidget(self.max_angle_Label, 10, 3)
        self.grid.addWidget(self.max_angle_edit_type, 11, 3)
        self.grid.addWidget(self.max_angle_depth_Label, 10, 4)
        self.grid.addWidget(self.max_angle_depth_edit_type, 11, 4)
        self.grid.addWidget(self.max_expected_pressure_Label, 10, 5)
        self.grid.addWidget(self.max_expected_pressure_edit_type, 11, 5)
        self.grid.addWidget(self.max_admissible_pressure_Label, 10, 6)
        self.grid.addWidget(self.max_admissible_pressure_edit_type, 11, 6)
        self.grid.addWidget(self.pump_ECN_do_Label, 13, 0)
        self.grid.addWidget(self.pump_ECN_do_edit_type, 14, 0)
        self.grid.addWidget(self.pump_ECN_depth_do_Label, 13, 1)
        self.grid.addWidget(self.pump_ECN_depth_do_edit_type, 14, 1)
        self.grid.addWidget(self.pump_ECN_posle_Label, 13, 4)
        self.grid.addWidget(self.pump_ECN_posle_edit_type, 14, 4)
        self.grid.addWidget(self.pump_ECN_depth_posle_Label, 13, 5)
        self.grid.addWidget(self.pump_ECN_depth_posle_edit_type, 14, 5)

        self.grid.addWidget(self.pump_SHGN_do_Label, 15, 0)
        self.grid.addWidget(self.pump_SHGN_do_edit_type, 16, 0)
        self.grid.addWidget(self.pump_SHGN_depth_do_Label, 15, 1)
        self.grid.addWidget(self.pump_SHGN_depth_do_edit_type, 16, 1)
        self.grid.addWidget(self.pump_SHGN_posle_Label, 15, 4)
        self.grid.addWidget(self.pump_SHGN_posle_edit_type, 16, 4)
        self.grid.addWidget(self.pump_SHGN_depth_posle_Label, 15, 5)
        self.grid.addWidget(self.pump_SHGN_depth_posle_edit_type, 16, 5)

        self.grid.addWidget(self.paker_do_Label, 17, 0)
        self.grid.addWidget(self.paker_do_edit_type, 18, 0)
        self.grid.addWidget(self.paker_depth_do_Label, 17, 1)
        self.grid.addWidget(self.paker_depth_do_edit_type, 18, 1)
        self.grid.addWidget(self.paker_posle_Label, 17, 4)
        self.grid.addWidget(self.paker_posle_edit_type, 18, 4)
        self.grid.addWidget(self.paker_depth_posle_Label, 17, 5)
        self.grid.addWidget(self.paker_depth_posle_edit_type, 18, 5)

        self.grid.addWidget(self.paker2_do_Label, 19, 0)
        self.grid.addWidget(self.paker2_do_edit_type, 20, 0)
        self.grid.addWidget(self.paker2_depth_do_Label, 19, 1)
        self.grid.addWidget(self.paker2_depth_do_edit_type, 20, 1)
        self.grid.addWidget(self.paker2_posle_Label, 19, 4)
        self.grid.addWidget(self.paker2_posle_edit_type, 20, 4)
        self.grid.addWidget(self.paker2_depth_posle_Label, 19, 5)
        self.grid.addWidget(self.paker2_depth_posle_edit_type, 20, 5)

        self.grid.addWidget(self.static_level_Label, 21, 2)
        self.grid.addWidget(self.static_level_edit_type, 22, 2)
        self.grid.addWidget(self.dinamic_level_Label, 21, 3)
        self.grid.addWidget(self.dinamic_level_edit_type, 22, 3)

        self.grid.addWidget(self.date_commissioning_Label, 21, 5)
        self.grid.addWidget(self.date_commissioning_line, 22, 5)

        self.grid.addWidget(self.result_pressure_date_label, 21, 6)
        self.grid.addWidget(self.result_pressure_date, 22, 6)

        self.grid.addWidget(self.curator_Label, 23, 1)
        self.grid.addWidget(self.curator_Combo, 24, 1)

        self.grid.addWidget(self.region_Label, 23, 2)
        self.grid.addWidget(self.region_combo, 24, 2)

        self.grid.addWidget(self.type_kr_Label, 23, 3)
        self.grid.addWidget(self.type_kr_combo, 24, 3)

        self.grid.addWidget(self.nkt_do_label, 27, 1)
        self.grid.addWidget(self.nkt_posle_label, 27, 5)

        self.grid.addWidget(self.sucker_rod_label, 35, 1)
        self.grid.addWidget(self.sucker_rod_po_label, 35, 5)

        self.grid.setColumnStretch(3, 1)
        self.grid.setColumnMinimumWidth(3, 50)

        # добавление строк с НКТ спущенных
        if len(self.dict_nkt) != 0:
            n = 1
            for nkt, length in self.dict_nkt.items():
                # print(f'НКТ {nkt, length}')
                nkt_line_edit = QLineEdit(self)
                nkt_line_edit.setText(str(self.ifNone(nkt)))

                length_line_edit = QLineEdit(self)
                length_line_edit.setText(str(self.ifNone(length)))

                self.grid.addWidget(nkt_line_edit, 27 + n, 1)
                self.grid.addWidget(length_line_edit, 27 + n, 2)

                # Переименование атрибута
                setattr(self, f"{nkt}_{n}_line", nkt_line_edit)
                setattr(self, f"{length}_{n}_line", length_line_edit)

                self.labels_nkt[n] = (nkt_line_edit, length_line_edit)
                n += 1
        else:
            nkt_line_edit = QLineEdit(self)
            length_line_edit = QLineEdit(self)

            setattr(self, f"nkt_line", nkt_line_edit)
            setattr(self, f"length_line", length_line_edit)

            self.labels_nkt[1] = (nkt_line_edit, length_line_edit)

            self.grid.addWidget(nkt_line_edit, 28, 1)
            self.grid.addWidget(length_line_edit, 28, 2)

        # добавление строк с штанг спущенных
        if len(self.dict_sucker_rod) != 0:
            n = 1
            for sucker, length in self.dict_sucker_rod.items():
                sucker_rod_line_edit = QLineEdit(self)
                sucker_rod_line_edit.setText(str(self.ifNone(sucker)))

                length_sucker_line_edit = QLineEdit(self)
                length_sucker_line_edit.setText(str(self.ifNone(length)))

                self.grid.addWidget(sucker_rod_line_edit, 37 + n, 1)
                self.grid.addWidget(length_sucker_line_edit, 37 + n, 2)

                # Переименование атрибута
                setattr(self, f"sucker_{n}_line", sucker_rod_line_edit)
                setattr(self, f"length_{n}_line", length_sucker_line_edit)

                self.labels_sucker[n] = (sucker_rod_line_edit, length_sucker_line_edit)
                n += 1
        else:
            sucker_rod_line_edit = QLineEdit(self)
            length_sucker_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"sucker_line", sucker_rod_line_edit)
            setattr(self, f"length_line", length_sucker_line_edit)

            self.labels_sucker[1] = (sucker_rod_line_edit, length_sucker_line_edit)

            self.grid.addWidget(sucker_rod_line_edit, 38, 1)
            self.grid.addWidget(length_sucker_line_edit, 38, 2)

        if len(self.dict_nkt_po) != 0:
            # добавление строк с НКТ плановых
            n = 1
            for nkt_po, length_po in self.dict_nkt_po.items():
                # print(f'НКТ план {nkt_po, length_po}')

                nkt_po_line_edit = QLineEdit(self)
                nkt_po_line_edit.setText(str(self.ifNone(nkt_po)))

                length_po_line_edit = QLineEdit(self)
                length_po_line_edit.setText(str(self.ifNone(length_po)))

                self.grid.addWidget(nkt_po_line_edit, 27 + n, 5)
                self.grid.addWidget(length_po_line_edit, 27 + n, 6)

                # Переименование атрибута
                setattr(self, f"nkt_po_{n}_line", nkt_po_line_edit)
                setattr(self, f"length_po_{n}_line", length_po_line_edit)

                self.labels_nkt_po[n] = (nkt_po_line_edit, length_po_line_edit)
                n += 1
        else:
            nkt_po_line_edit = QLineEdit(self)
            length_po_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"nkt_po_line", nkt_po_line_edit)
            setattr(self, f"length_po_line", length_po_line_edit)

            self.labels_nkt_po[1] = (nkt_po_line_edit, length_po_line_edit)

            self.grid.addWidget(nkt_po_line_edit, 28, 5)
            self.grid.addWidget(length_po_line_edit, 28, 6)
        # добавление строк с штангами плановых

        if len(self.dict_sucker_rod_po) != 0:
            n = 1
            for sucker_po, length_po in self.dict_sucker_rod_po.items():
                # print(f'штанги план {sucker_po, length_po}')
                sucker_rod_po_line_edit = QLineEdit(self)
                sucker_rod_po_line_edit.setText(str(self.ifNone(sucker_po)))

                length_sucker_po_line_edit = QLineEdit(self)
                length_sucker_po_line_edit.setText(str(self.ifNone(length_po)))

                self.grid.addWidget(sucker_rod_po_line_edit, 37 + n, 5)
                self.grid.addWidget(length_sucker_po_line_edit, 37 + n, 6)

                # Переименование атрибута
                setattr(self, f"sucker_{n}_line", sucker_rod_po_line_edit)
                setattr(self, f"length_{n}_line", length_sucker_po_line_edit)

                self.labels_sucker_po[n] = (sucker_rod_po_line_edit, length_sucker_po_line_edit)
                n += 1
        else:
            sucker_rod_po_line_edit = QLineEdit(self)
            length_sucker_po_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"sucker_line", sucker_rod_po_line_edit)
            setattr(self, f"length_line", length_sucker_po_line_edit)

            self.labels_sucker_po[1] = (sucker_rod_po_line_edit, length_sucker_po_line_edit)

            self.grid.addWidget(sucker_rod_po_line_edit, 38, 5)
            self.grid.addWidget(length_sucker_po_line_edit, 38, 6)

        if self.curator_Combo.currentText() == 'ОР':

            self.expected_pickup_label = QLabel('Ожидаемая приемистость')
            self.expected_pickup_edit = FloatLineEdit()
            try:
                self.expected_pickup_edit.setText(f'{self.data_well.expected_pickup}')
                # print(f'ожидаемая приемистисть{self.data_well.expected_pickup}')
            except:
                pass
            self.grid.addWidget(self.expected_pickup_label, 25, 2)
            self.grid.addWidget(self.expected_pickup_edit, 26, 2)

            self.expected_pressure_label = QLabel('Ожидаемое давление закачки')
            self.expected_pressure_edit = FloatLineEdit()
            try:
                self.expected_pressure_edit.setText(f'{self.data_well.expected_pressure}')
            except:
                pass
            self.grid.addWidget(self.expected_pressure_label, 25, 3)
            self.grid.addWidget(self.expected_pressure_edit, 26, 3)
        else:
            self.water_cut_Label = QLabel('Дебит по жидкости')
            self.water_cut_edit = FloatLineEdit()
            try:
                self.water_cut_edit.setText(f'{self.data_well.water_cut}')
            except:
                pass
            self.grid.addWidget(self.water_cut_Label, 25, 1)
            self.grid.addWidget(self.water_cut_edit, 26, 1)
            self.expected_oil_Label = QLabel('Дебит по нефти')
            self.expected_oil_edit = FloatLineEdit()
            try:
                self.expected_oil_edit.setText(f'{self.data_well.expected_oil}')
            except:
                pass
            self.grid.addWidget(self.expected_oil_Label, 25, 2)
            self.grid.addWidget(self.expected_oil_edit, 26, 2)
            self.proc_water_Label = QLabel('Обводненность')

            self.proc_water_edit = FloatLineEdit()
            try:
                self.proc_water_edit.setText(f'{self.data_well.percent_water}')
            except:
                pass
            self.grid.addWidget(self.proc_water_Label, 25, 3)
            self.grid.addWidget(self.proc_water_edit, 26, 3)

        curator_list = ['', 'ГРР', 'ОР', 'ГТМ', 'ГО', 'ВНС']
        self.curator_Combo.addItems(curator_list)
        # print(self.pump_SHGN_posle_edit_type.text() != 'отсут', self.pump_ECN_posle_edit_type.text() != 'отсут')

        curator = 'ОР' if (self.pump_SHGN_posle_edit_type.text() == 'отсут' \
                           and self.pump_ECN_posle_edit_type.text() == 'отсут') else 'ГТМ'
        if self.data_well.work_plan in ['gnkt_frez', 'gnkt_bopz']:
            curator = 'ВНС'

        self.curator_Combo.currentTextChanged.connect(self.update_curator)
        # print(f'куратор индекс {curator, curator_list.index(curator)}')
        self.curator_Combo.setCurrentIndex(curator_list.index(curator))
        self.region_combo.addItems(data_list.REGION_LIST)
        self.region_combo.setCurrentIndex(data_list.REGION_LIST.index(self.data_well.region))

        self.type_kr_combo.view().setWordWrap(True)
        self.type_kr_combo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        if self.data_well.work_plan in ['prs']:
            self.type_kr_combo.addItems(data_list.TYPE_TR_LIST)
        else:
            self.type_kr_combo.addItems(data_list.TYPE_KR_LIST)

        self.type_kr_combo.setCurrentIndex(self.select_type_kr())

    def select_type_kr(self):
        kr = self.data_well.type_kr
        if 'prs' in self.data_well.work_plan:
            TYPE_KR_LIST = data_list.TYPE_TR_LIST
        else:
            TYPE_KR_LIST = data_list.TYPE_KR_LIST
        index_sel = 0
        if kr:
            kr = kr.split(' ')[0] + ' '
            for index, type_kr in enumerate(TYPE_KR_LIST):
                if kr in type_kr and kr != ' ':
                    index_sel = index
        return index_sel

    def update_curator(self):

        # Очистка и удаление существующих виджетов, если они уже были добавлены ранее

        try:
            self.expected_pressure_label.setParent(None)
        except:
            pass
        try:
            self.expected_pressure_edit.setParent(None)
        except:
            pass
        try:
            self.expected_pickup_label.setParent(None)
        except:
            pass
        try:
            self.expected_pickup_edit.setParent(None)
        except:
            pass
        try:
            self.water_cut_Label.setParent(None)
        except:
            pass
        try:
            self.water_cut_edit.setParent(None)
        except:
            pass
        try:
            self.expected_oil_Label.setParent(None)
        except:
            pass
        try:
            self.expected_oil_edit.setParent(None)
        except:
            pass
        try:
            self.proc_water_Label.setParent(None)
        except:
            pass
        try:
            self.proc_water_edit.setParent(None)
        except:
            pass

        if self.curator_Combo.currentText() == 'ОР':
            self.expected_pickup_label = QLabel('Ожидаемая приемистость')
            self.expected_pickup_edit = FloatLineEdit()
            try:
                self.expected_pickup_edit.setText(f'{self.data_well.expected_pickup}')
            except:
                pass
            self.grid.addWidget(self.expected_pickup_label, 25, 4)
            self.grid.addWidget(self.expected_pickup_edit, 26, 4)

            self.expected_pressure_label = QLabel('Ожидаемое давление закачки')
            self.expected_pressure_edit = FloatLineEdit()
            self.expected_pressure_edit.setText(f'{self.data_well.expected_pressure}')
            self.grid.addWidget(self.expected_pressure_label, 25, 5)
            self.grid.addWidget(self.expected_pressure_edit, 26, 5)
        else:
            self.water_cut_Label = QLabel('Дебит по жидкости')
            self.water_cut_edit = FloatLineEdit()
            try:
                self.water_cut_edit.setText(f'{self.data_well.water_cut}')
            except:
                pass
            self.grid.addWidget(self.water_cut_Label, 25, 1)
            self.grid.addWidget(self.water_cut_edit, 26, 1)
            self.expected_oil_Label = QLabel('Дебит по нефти')
            self.expected_oil_edit = FloatLineEdit()
            try:
                self.expected_oil_edit.setText(f'{self.data_well.expected_oil}')
            except:
                pass
            self.grid.addWidget(self.expected_oil_Label, 25, 2)
            self.grid.addWidget(self.expected_oil_edit, 26, 2)
            self.proc_water_Label = QLabel('Обводненность')

            self.proc_water_edit = FloatLineEdit()
            try:
                self.proc_water_edit.setText(f'{self.data_well.percent_water}')
            except:
                pass
            self.grid.addWidget(self.proc_water_Label, 25, 3)
            self.grid.addWidget(self.proc_water_edit, 26, 3)

    def ifNone(self, string):
        try:
            if str(string).lower() in ['0', 'none', '-', '--', 'отсутствует', 'отсут']:
                return 'отсут'
            if '/' in str(string):
                return string.split('/')[0]
            elif str(string).replace('.', '').replace(',', '').isdigit():

                # print(str(round(float(string), 1))[-1] == '0', int(string), float(string))
                return int(float(str(string).replace(',', '.'))) if str(round(float(str(string).replace(',', '.')), 1))[
                                                                        -1] == "0" else \
                    round(float(str(string).replace(',', '.')), 1)
            else:
                return str(string).strip()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'ошибка обработки \n {e}')

    def remove_non_numeric_chars(self, string):

        pattern = r"[^\d\.,]"
        if re.sub(pattern, "", str(string)) == '':
            return string
        else:
            return re.sub(pattern, "", str(string))

    def updateLabel(self):
        # self.dinamic_level_Label
        self.column_type.setText()
        self.column_add_edit_type.setText()
        self.update()


class TabWidget(TabWidgetUnion):
    def __init__(self, data_well):
        super().__init__()
        self.addTab(TabPageSoCorrect(data_well), 'Проверка корректности данных')


class DataWindow(WindowUnion):

    def __init__(self, data_well: FindIndexPZ):
        super(DataWindow, self).__init__(data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        self.tab_widget = TabWidget(self.data_well)
        # self.tableWidget = QTableWidget(0, 4)
        # self.labels_nkt = labels_nkt

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def add_row_table(self):
        from find import ProtectedIsNonNone, ProtectedIsDigit
        from work_py.opressovka import TabPageSo
        self.current_widget = self.tab_widget.currentWidget()

        region_combo = self.current_widget.region_combo.currentText()
        type_kr_combo = self.current_widget.type_kr_combo.currentText()
        try:
            if region_combo == '':
                QMessageBox.warning(self, 'ОШИБКА', 'Не выбран регион')
                return
            self.data_well.region = region_combo
            if type_kr_combo == '':
                QMessageBox.warning(self, 'ОШИБКА', 'Не выбран Вид и категория ремонта')
                return
            else:
                self.data_well.type_kr = type_kr_combo

            column_type = self.current_widget.column_type.text().replace(',', '.')
            column_wall_thickness = self.current_widget.column_wall_thickness_edit_type2.text()
            shoe_column = self.current_widget.shoe_column_edit_type2.text().strip().replace(',', '.')
            level_cement = self.current_widget.level_cement_edit.text()
            if '-' in level_cement:
                level_cement = level_cement.split("-")[0]
            head_column = float(self.current_widget.head_column_edit_type2.text().replace(',', '.'))
            column_add_True = str(self.current_widget.column_add_true_comboBox.currentText())
            if column_add_True == 'в наличии':
                self.data_well.column_additional = True
            else:
                self.data_well.column_additional = False

            column_additional_diameter = self.current_widget.column_add_edit_type.text().replace(',', '.')
            column_additional_wall_thickness = self.current_widget.column_add_wall_thicknessedit_type2.text().replace(',', '.')
            shoe_column_additional = self.current_widget.shoe_column_add_edit_type2.text().replace(',', '.')
            head_column_additional = self.current_widget.head_column_add_edit_type2.text().replace(',', '.')
            bottomhole_drill = self.current_widget.bottomhole_drill_edit_type.text().replace(',', '.')
            if bottomhole_drill == 'отсут':
                QMessageBox.warning(self, 'Ошибка', 'Ошибка в пробуренном забое')
                return
            bottomhole_artificial = self.current_widget.bottomhole_artificial_edit_type.text().replace(',', '.')
            current_bottom = self.current_widget.current_bottom_edit_type.text().replace(',', '.')
            max_angle_depth = self.current_widget.max_angle_depth_edit_type.text().replace(',', '.')
            max_angle = self.current_widget.max_angle_edit_type.text().replace(',', '.')
            max_expected_pressure = self.current_widget.max_expected_pressure_edit_type.text().replace(',', '.')
            max_admissible_pressure = self.current_widget.max_admissible_pressure_edit_type.text().replace(',', '.')

            column_direction_diameter = self.current_widget.column_direction_diameter_edit.text().replace(',', '.')
            column_direction_wall_thickness = self.current_widget.column_direction_wall_thickness_edit.text().replace(',', '.')
            column_direction_length = self.current_widget.column_direction_length_edit.text().replace(',', '.')
            level_cement_direction = self.current_widget.level_cement_direction_edit.text()
            column_conductor_diameter = self.current_widget.column_conductor_diameter_edit.text().replace(',', '.')
            column_conductor_wall_thickness = self.current_widget.column_conductor_wall_thickness_edit.text().replace(',', '.')
            column_conductor_length = self.current_widget.column_conductor_length_edit.text().replace(',', '.')
            level_cement_conductor = self.current_widget.level_cement_conductor_edit.text().replace(',', '.')

            dict_pump_shgn_do = str(self.current_widget.pump_SHGN_do_edit_type.text())
            dict_pump_shgn_h_do = self.current_widget.pump_SHGN_depth_do_edit_type.text()

            dict_pump_shgn_posle = str(self.current_widget.pump_SHGN_posle_edit_type.text())
            dict_pump_shgn_h_posle = str(self.current_widget.pump_SHGN_depth_posle_edit_type.text())

            dict_pump_ecn_do = str(self.current_widget.pump_ECN_do_edit_type.text())
            dict_pump_ecn_h_do = self.current_widget.pump_ECN_depth_do_edit_type.text()

            dict_pump_ecn_posle = str(self.current_widget.pump_ECN_posle_edit_type.text())
            dict_pump_ecn_h_posle = str(self.current_widget.pump_ECN_depth_posle_edit_type.text())

            # print(f'прио {type(dict_pump_h_posle)}')
            paker_do = str(self.current_widget.paker_do_edit_type.text())
            depth_fond_paker_do = str(self.current_widget.paker_depth_do_edit_type.text())
            paker_posle = self.current_widget.paker_posle_edit_type.text()
            depth_fond_paker_posle = self.current_widget.paker_depth_posle_edit_type.text()

            paker2_do = str(self.current_widget.paker2_do_edit_type.text())
            depth_fond_paker2_do = self.current_widget.paker2_depth_do_edit_type.text()
            paker2_posle = self.current_widget.paker2_posle_edit_type.text()
            depth_fond_paker2_posle = self.current_widget.paker2_depth_posle_edit_type.text()

            static_level = self.current_widget.static_level_edit_type.text()
            dinamic_level = self.current_widget.dinamic_level_edit_type.text()
            date_commissioning_line = self.current_widget.date_commissioning_line.text()
            result_pressure_date = self.current_widget.result_pressure_date.text()
            curator = str(self.current_widget.curator_Combo.currentText())
            if self.check_date_format(result_pressure_date) is False:
                if curator != 'ВНС':
                    QMessageBox.warning(self, 'Ошибка', 'Не корректна дата последней опрессовки')
                    return
                else:
                    self.data_well.result_pressure_date = data_list.ProtectedIsNonNone(self.data_well.date_drilling_cancel)

            if self.check_date_format(date_commissioning_line) is False:
                if curator != 'ВНС':
                    QMessageBox.warning(self, 'Ошибка', 'Не корректна дата ввода в эскплуатацию')
                    return
                else:
                    self.data_well.date_commissioning = data_list.ProtectedIsNonNone(self.data_well.date_drilling_cancel)

                # try:
                #     # Попытка распарсить строку в формате 'ДД.ММ.ГГГГ'
                #     datetime.strptime(self.data_well.date_commissioning, '%d.%m.%Y')
                #
                # except:
                #     QMessageBox.warning(self, 'Ошибка', 'Не корректна дата ввода в эскплуатацию')
                #     return

            if curator == 'ОР':
                expected_pickup_edit = self.current_widget.expected_pickup_edit.text()
                expected_pressure_edit = self.current_widget.expected_pressure_edit.text()
            else:
                water_cut_edit = self.current_widget.water_cut_edit.text()
                expected_oil_edit = self.current_widget.expected_oil_edit.text()
                proc_water_edit = self.current_widget.proc_water_edit.text()

            a = self.current_widget.labels_nkt

            # Пересохранение данных по НКТ и штангам
            self.data_well.dict_sucker_rod = {}
            self.data_well.dict_sucker_rod_after = {}
            self.data_well.dict_nkt_before = {}
            self.data_well.dict_nkt_after = {}

            if self.current_widget.labels_nkt:
                for key, value in self.current_widget.labels_nkt.values():
                    asdf = key.text(), value.text()
                    if key.text() != '' and value.text() != '':
                        self.data_well.dict_nkt_before[key.text()] = self.check_if_none(float(value.text()))

            if all([pump for pump in [self.if_none(dict_pump_ecn_posle), self.if_none(paker2_posle),
                                      self.if_none(dict_pump_shgn_posle), self.if_none(paker_posle)]]):

                voronka_question = QMessageBox.question(self, 'Внимание',
                                                        'Программа определила что в скважине '
                                                        'После ремонта воронка, верно ли')
                if voronka_question == QMessageBox.StandardButton.No:
                    return

            if self.current_widget.labels_nkt_po:
                for key, value in self.current_widget.labels_nkt_po.values():
                    if key.text() != '' and value.text() != '':
                        self.data_well.dict_nkt_after[key.text()] = self.check_if_none(float(value.text()))

            if len(self.data_well.dict_nkt_before) == 0:
                mes = QMessageBox.question(self, 'Расчет на ГНО', 'НКТ на спуск отсутствует?')
                if mes == QMessageBox.StandardButton.No:
                    return
            if self.current_widget.labels_sucker:
                for key, value in self.current_widget.labels_sucker.values():
                    if key.text() != '' and value.text() != '':
                        self.data_well.dict_sucker_rod[key.text()] = self.check_if_none(int(float(value.text())))

            if self.current_widget.labels_sucker_po:
                for key, value in self.current_widget.labels_sucker_po.values():
                    if key.text() != '' and value.text() != '':
                        self.data_well.dict_sucker_rod_after[key.text()] = self.check_if_none(int(float(value.text())))

            question = QMessageBox.question(self, 'выбор куратора', f'Куратор ремонта сектор {curator}, верно ли?')
            if question == QMessageBox.StandardButton.No:
                return

            close_file = True

            if any([self.if_none(data_well) is False or data_well in ['не корректно', 0, 'отсут'] for data_well in
                    [column_type, column_wall_thickness, shoe_column]]):
                QMessageBox.information(self, 'Внимание', 'Не все поля в данных колонне соответствуют значениям')
                close_file = False

            if float(bottomhole_artificial) > 10000 or float(bottomhole_drill) > 10000:
                QMessageBox.information(self, 'Внимание', 'Забой не корректный')
                close_file = False

            if any([self.if_none(data_well) is False for data_well in
                    [column_additional_diameter, column_additional_wall_thickness,
                     shoe_column_additional, head_column_additional]]) and self.data_well.column_additional:
                QMessageBox.information(self, 'Внимание', 'Не все поля в доп колонне соответствуют значениям')
                close_file = False

            if self.if_none(bottomhole_artificial) is False \
                    or self.if_none(bottomhole_drill) is False \
                    or self.if_none(current_bottom) is False \
                    or self.if_none(max_angle_depth) is False \
                    or self.if_none(max_angle) is False \
                    or self.if_none(max_admissible_pressure) is False \
                    or self.if_none(max_expected_pressure) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в забое соответствуют значениям')
                close_file = False
            if self.if_none(static_level) is False \
                    or self.if_none(dinamic_level) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в уровнях соответствуют значениям')
                close_file = False
            if self.if_none(dict_pump_ecn_h_do) is False \
                    or self.if_none(dict_pump_ecn_h_posle) is False \
                    or self.if_none(dict_pump_shgn_h_do) is False \
                    or self.if_none(dict_pump_shgn_h_posle) is False \
                    or self.if_none(depth_fond_paker_do) is False \
                    or self.if_none(depth_fond_paker_posle) is False \
                    or self.if_none(depth_fond_paker2_do) is False \
                    or self.if_none(depth_fond_paker2_posle) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в спущенном оборудовании соответствуют значениям')
                close_file = False
            if self.if_none(level_cement) is False:
                QMessageBox.information(self, 'Внимание', 'Уровень цемента за ЭК не соответствуют значениям')
                close_file = False
            if self.if_none(column_direction_diameter) is False \
                    or self.if_none(column_direction_wall_thickness) is False \
                    or self.if_none(column_direction_length) is False \
                    or self.if_none(level_cement_direction) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в Направлении соответствуют значениям')
                close_file = False
            if self.if_none(column_conductor_diameter) is False \
                    or self.if_none(column_conductor_wall_thickness) is False \
                    or self.if_none(column_conductor_length) is False \
                    or self.if_none(column_direction_length) is False \
                    or self.if_none(level_cement_conductor) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в кондукторе соответствуют значениям')
                close_file = False

            if any(['НВ' in dict_pump_shgn_do.upper(), 'ШГН' in dict_pump_shgn_do.upper(),
                    'НН' in dict_pump_shgn_do.upper(), dict_pump_shgn_do == 'отсут',
                    'RH' in dict_pump_shgn_do.upper()]) is False \
                    or any(['НВ' in dict_pump_shgn_posle.upper(), 'ШГН' in dict_pump_shgn_posle.upper(),
                            'НН' in dict_pump_shgn_posle.upper(), dict_pump_shgn_posle == 'отсут',
                            'RHAM' in dict_pump_shgn_do]) is False \
                    or any(['ЭЦН' in dict_pump_ecn_posle.upper(), 'ВНН' in dict_pump_ecn_posle.upper(),
                            dict_pump_ecn_posle == 'отсут']) is False \
                    or (dict_pump_ecn_do != 'отсут' and dict_pump_ecn_h_do == 'отсут') \
                    or (dict_pump_ecn_posle != 'отсут' and dict_pump_ecn_h_posle == 'отсут') \
                    or (dict_pump_shgn_do != 'отсут' and dict_pump_shgn_h_do == 'отсут') \
                    or (dict_pump_shgn_posle != 'отсут' and dict_pump_shgn_h_posle == 'отсут') \
                    or (paker_do != 'отсут' and depth_fond_paker_do == 'отсут') \
                    or (paker_posle != 'отсут' and depth_fond_paker_posle == 'отсут') \
                    or (paker2_do != 'отсут' and depth_fond_paker2_do == 'отсут') \
                    or (paker2_posle != 'отсут' and depth_fond_paker2_posle == 'отсут') \
                    or any(['ЭЦН' in dict_pump_ecn_do.upper(), 'ВНН' in dict_pump_ecn_do.upper(),
                            dict_pump_ecn_do == 'отсут']) is False:
                QMessageBox.information(self, 'Внимание', 'Не все поля в даннахы по насосом соответствуют значениям')
                close_file = False
            if isinstance(self.if_none(head_column_additional), str):
                # print(self.check_if_none(head_column_additional), isinstance(self.if_none(head_column_additional), str))
                if self.check_if_none(20 if self.if_none(head_column_additional) else head_column_additional) < 5:
                    # print(self.check_if_none(head_column_additional))
                    QMessageBox.information(self, 'Внимание', 'В скважине отсутствует доп колонна')
                    close_file = False
                else:
                    QMessageBox.information(self, 'Внимание', 'В скважине отсутствует доп колонна')
                    close_file = False

            if (data_list.nkt_mistake is True and len(self.data_well.dict_nkt_before) == 0):
                QMessageBox.information(self, 'Внимание',
                                        'При вызванной ошибке НКТ до ремонта не может быть пустым')
                close_file = False
            if data_list.nkt_mistake is True and len(self.data_well.dict_nkt_after) == 0:
                QMessageBox.information(self, 'Внимание',
                                        'При вызванной ошибке НКТ после ремонта не может быть пустым')
                close_file = False

            if self.data_well.column_additional:
                asdedf = [self.check_str_isdigit(column_additional_diameter),
                       self.check_str_isdigit(head_column_additional),
                       self.check_str_isdigit(shoe_column_additional),
                       self.check_str_isdigit(column_additional_wall_thickness)]
                if all([self.check_str_isdigit(column_additional_diameter),
                       self.check_str_isdigit(head_column_additional),
                       self.check_str_isdigit(shoe_column_additional),
                       self.check_str_isdigit(column_additional_wall_thickness)]):

                    if int(float(column_additional_diameter)) >= float(column_type):
                        QMessageBox.information(self, 'Внимание', 'Ошибка в диаметре доп колонны')
                        close_file = False

                    if any([70 > float(column_additional_diameter), float(column_additional_diameter) > 150,
                            5 > float(column_additional_wall_thickness), float(column_additional_wall_thickness) > 13,
                            5 > float(column_conductor_wall_thickness), float(column_conductor_wall_thickness) > 13,
                            5 > float(column_wall_thickness), float(column_wall_thickness) > 13]):
                        QMessageBox.information(self, 'Внимание', 'Проверьте толщину колонны')
                        close_file = False

                    if int(float(str(head_column_additional).replace(',', '.'))) < 10:
                        msg = QMessageBox.question(self, 'Внимание', 'доп колонна начинается с устья?')
                        if msg == QMessageBox.StandardButton.Yes:
                            column_direction_length = column_conductor_length
                            column_direction_diameter = column_conductor_diameter
                            column_direction_wall_thickness = column_conductor_wall_thickness
                            level_cement_direction = level_cement_conductor
                            column_conductor_length = shoe_column
                            column_conductor_diameter = column_type
                            column_conductor_wall_thickness = column_wall_thickness

                            shoe_column = shoe_column_additional
                            column_type = column_additional_diameter
                            column_wall_thickness = column_additional_wall_thickness
                            self.data_well.column_additional = False
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Ошибка в доп колонне')
                    close_file = False

            if type_kr_combo in ['КР13-1  Подготовительные работы к ГРП (ПР)',
                                 'КР13-2  Освоение скважины после ГРП (ЗР)',
                                 'КР13-1  Подготовительные работы к ГРП (ПР) КР13-2  Освоение скважины после ГРП (ЗР)',
                                 'КР13-5  Подготовка скважины к проведению работ по повышению н/отдачи пластов',
                                 'КР13-6  Подготовительные работы к ГГРП (ПР)',
                                 'КР13-7  Заключительные работы (ЗР) после ГГРП (освоение скважины и т.д.)',
                                 'КР7-2  Проведение ГРП',
                                 'КР7-3  Проведение ГГРП',
                                 'КР7-4  Проведение ГПП']:
                self.data_well.grp_plan = True

            if curator == 'ОР':
                if self.if_none(expected_pickup_edit) is False or self.if_none(expected_pressure_edit) is False:
                    QMessageBox.information(self, 'Внимание',
                                            'Не все поля в Ожидаемых показателях соответствуют значениям')
                    close_file = False
            else:
                if self.if_none(water_cut_edit) is False or self.if_none(expected_oil_edit) is False or \
                        self.if_none(proc_water_edit) is False:
                    QMessageBox.information(self, 'Внимание',
                                            'Не все поля в Ожидаемых показателях соответствуют значениям')
                    close_file = False
            try:
                if float(shoe_column) < 30:
                    QMessageBox.warning(self, 'Ошибка', 'Башмак ЭК слишком короткий')
                    return
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Башмак ЭК не корректен {type(e).__name__}\n\n{str(e)}')

            if close_file is False:
                return
            elif close_file is True:
                self.data_well.column_diameter = ProtectedIsDigit(self.check_if_none(column_type))
                self.data_well.column_wall_thickness = ProtectedIsDigit(self.check_if_none(column_wall_thickness))
                self.data_well.shoe_column = ProtectedIsDigit(float(self.check_if_none(shoe_column)))
                self.data_well.head_column = ProtectedIsDigit(head_column)
                self.data_well.diameter_doloto_ek = ProtectedIsDigit(0)
                if self.data_well.column_additional:
                    self.data_well.column_additional_diameter = ProtectedIsDigit(
                        self.check_if_none(column_additional_diameter))
                    self.data_well.column_additional_wall_thickness = ProtectedIsDigit(
                        self.check_if_none(column_additional_wall_thickness))
                    self.data_well.shoe_column_additional = ProtectedIsDigit(
                        int(float(self.check_if_none(shoe_column_additional))))
                    self.data_well.head_column_additional = ProtectedIsDigit(
                        int(float(self.check_if_none(head_column_additional))))
                else:
                    self.data_well.column_additional_diameter = ProtectedIsDigit(0)
                    self.data_well.column_additional_wall_thickness = ProtectedIsDigit(0)
                    self.data_well.shoe_column_additional = ProtectedIsDigit(0)
                    self.data_well.head_column_additional = ProtectedIsDigit(head_column)

                self.data_well.bottom_hole_drill = ProtectedIsDigit(self.check_if_none(bottomhole_drill))
                self.data_well.bottom_hole_artificial = ProtectedIsDigit(self.check_if_none(bottomhole_artificial))
                self.data_well.current_bottom = self.check_if_none(current_bottom)
                self.data_well.bottom = self.check_if_none(current_bottom)
                self.data_well.level_cement_column = ProtectedIsDigit(self.check_if_none(level_cement))
                self.data_well.max_angle = ProtectedIsDigit(self.check_if_none(max_angle))
                self.data_well.max_expected_pressure = ProtectedIsDigit(self.check_if_none(max_expected_pressure))
                self.data_well.max_admissible_pressure = ProtectedIsDigit(
                    self.check_if_none(max_admissible_pressure))
                self.data_well.date_commissioning = ProtectedIsNonNone(date_commissioning_line)
                self.data_well.result_pressure_date = ProtectedIsNonNone(result_pressure_date)

                # print(f'макс {self.data_well.max_expected_pressure.get_value}')
                self.data_well.dict_pump_shgn["before"] = self.check_if_none(dict_pump_shgn_do)
                self.data_well.dict_pump_shgn_depth["before"] = self.check_if_none(dict_pump_shgn_h_do)
                self.data_well.dict_pump_shgn_depth["after"] = self.check_if_none(dict_pump_shgn_h_posle)
                self.data_well.dict_pump_shgn["after"] = self.check_if_none(dict_pump_shgn_posle)

                self.data_well.dict_pump_ecn["before"] = self.check_if_none(dict_pump_ecn_do)
                self.data_well.dict_pump_ecn_depth["before"] = self.check_if_none(dict_pump_ecn_h_do)
                self.data_well.dict_pump_ecn["after"] = self.check_if_none(dict_pump_ecn_posle)
                self.data_well.dict_pump_ecn_depth["after"] = self.check_if_none(dict_pump_ecn_h_posle)

                self.data_well.paker_before["before"] = self.check_if_none(paker_do)
                self.data_well.depth_fond_paker_before["before"] = self.check_if_none(depth_fond_paker_do)
                self.data_well.paker_before["after"] = self.check_if_none(paker_posle)
                self.data_well.depth_fond_paker_before["after"] = self.check_if_none(depth_fond_paker_posle)

                self.data_well.paker_second_before["before"] = self.check_if_none(paker2_do)
                self.data_well.depth_fond_paker_second_before["before"] = self.check_if_none(depth_fond_paker2_do)
                self.data_well.paker_second_before["after"] = self.check_if_none(paker2_posle)
                self.data_well.depth_fond_paker_second_before["after"] = self.check_if_none(depth_fond_paker2_posle)
                self.data_well.static_level = ProtectedIsDigit(self.check_if_none(static_level))
                self.data_well.dinamic_level = ProtectedIsDigit(self.check_if_none(dinamic_level))

                self.data_well.column_direction_diameter = ProtectedIsDigit(
                    self.check_if_none(column_direction_diameter))
                self.data_well.column_direction_wall_thickness = ProtectedIsDigit(
                    self.check_if_none(column_direction_wall_thickness))
                self.data_well.column_direction_length = ProtectedIsDigit(
                    self.check_if_none(column_direction_length))
                self.data_well.level_cement_direction = ProtectedIsDigit(self.check_if_none(level_cement_direction))
                self.data_well.column_conductor_diameter = ProtectedIsDigit(
                    self.check_if_none(column_conductor_diameter))
                self.data_well.column_conductor_wall_thickness = ProtectedIsDigit(
                    self.check_if_none(column_conductor_wall_thickness))
                self.data_well.column_conductor_length = ProtectedIsDigit(
                    self.check_if_none(column_conductor_length))
                self.data_well.level_cement_conductor = ProtectedIsDigit(self.check_if_none(level_cement_conductor))
                if curator == 'ОР':
                    self.data_well.expected_pressure = self.check_if_none(expected_pressure_edit)
                    self.data_well.expected_pickup = self.check_if_none(expected_pickup_edit)
                    self.data_well.expected_pick_up[self.data_well.expected_pickup] = self.data_well.expected_pressure
                    self.data_well.percent_water = 100
                else:
                    self.data_well.expected_oil = self.check_if_none(expected_oil_edit)
                    self.data_well.water_cut = self.check_if_none(water_cut_edit)
                    self.data_well.percent_water = int(self.check_if_none(proc_water_edit))

                if str(self.data_well.dict_pump_shgn["before"]) != '0' and len(
                        self.data_well.dict_sucker_rod) == 0:
                    assdf = str(self.data_well.dict_pump_shgn["before"]), len(self.data_well.dict_sucker_rod), \
                            self.data_well.dict_sucker_rod
                    QMessageBox.warning(self, 'ОШИБКА',
                                        f'при спущенном насосе {self.data_well.dict_pump_shgn["before"]} '
                                        f'не указаны штанги, либо не корректно прочитаны данные ')
                    # self.pause_app()

                    return
                if str(self.data_well.dict_pump_shgn["after"]) != '0' and len(
                        self.data_well.dict_sucker_rod_after) == 0:
                    QMessageBox.warning(self, 'ОШИБКА',
                                        f'при плановом насосе {self.data_well.dict_pump_shgn["before"]} '
                                        f'не указаны штанги, либо не корректно прочитаны данные ')
                    # self.pause_app()

                    return
                if self.data_well.column_additional is False or\
                    (self.data_well.column_additional and
                     self.data_well.current_bottom > self.data_well.head_column_additional.get_value):
                    if self.data_well.dict_pump_ecn != '0':
                        self.data_well.template_depth = self.data_well.dict_pump_ecn_depth["before"]
                        self.data_well.template_length = 30
                else:
                    if self.data_well.dict_pump_ecn != 0:
                        if self.data_well.dict_pump_ecn_depth["before"] > self.data_well.head_column_additional.get_value:
                            self.data_well.template_depth_addition = self.data_well.dict_pump_ecn_depth
                            self.data_well.template_length_addition = 30
                        else:
                            self.data_well.template_depth = self.data_well.dict_pump_ecn_depth["before"]
                            self.data_well.template_length = 30

                self.data_well.curator = curator
                if curator in ['ВНС']:
                    self.data_well.bvo = True
                elif curator in ['ГРР'] and self.data_well.work_plan in ['gnkt_after_grp']:
                    self.data_well.bvo = True
                elif self.data_well.work_plan in ['gnkt_frez']:
                    self.data_well.bvo = True
                self.data_well.data_well_dict = {
                    'направление': {
                        'диаметр': self.data_well.column_direction_diameter.get_value,
                        'толщина стенки': self.data_well.column_direction_wall_thickness.get_value,
                        'башмак': self.data_well.column_direction_length.get_value,
                        'цемент': self.data_well.level_cement_direction.get_value},
                    'кондуктор': {
                        'диаметр': self.data_well.column_conductor_diameter.get_value,
                        'толщина стенки': self.data_well.column_conductor_wall_thickness.get_value,
                        'башмак': self.data_well.column_conductor_length.get_value,
                        'цемент': self.data_well.level_cement_conductor.get_value},
                    'ЭК': {
                        'диаметр': self.data_well.column_diameter.get_value,
                        'толщина стенки': self.data_well.column_wall_thickness.get_value,
                        'башмак': self.data_well.shoe_column.get_value,
                        'цемент': self.data_well.level_cement_column.get_value,
                        'голова ЭК': self.data_well.head_column.get_value
                    },
                    'допколонна': {
                        'наличие': self.data_well.column_additional,
                        'диаметр': self.data_well.column_additional_diameter.get_value,
                        'толщина стенки': self.data_well.column_additional_wall_thickness.get_value,
                        'голова': self.data_well.head_column_additional.get_value,
                        'башмак': self.data_well.shoe_column_additional.get_value},
                    'куратор': curator,
                    'регион': self.data_well.region,
                    'ЦДНГ': self.data_well.cdng.get_value,
                    'оборудование': {
                        'ЭЦН':
                            {
                                'тип': self.data_well.dict_pump_ecn,
                                'глубина ': self.data_well.dict_pump_ecn_depth
                            },
                        'ШГН':
                            {
                                'тип': self.data_well.dict_pump_shgn,
                                'глубина ': self.data_well.dict_pump_shgn_depth
                            },
                        'пакер':
                            {
                                'тип': self.data_well.paker_before,
                                'глубина ': self.data_well.depth_fond_paker_before
                            },
                        'пакер2':
                            {
                                'тип': self.data_well.paker_second_before,
                                'глубина ': self.data_well.depth_fond_paker_second_before
                            },

                    },
                    'статика': self.data_well.static_level.get_value,
                    'динамика': self.data_well.dinamic_level.get_value,
                    'дата ввода в эксплуатацию': self.data_well.date_commissioning.get_value,
                    'дата опрессовки': self.data_well.result_pressure_date.get_value,
                    'НКТ': {
                        'До': self.data_well.dict_nkt_before,
                        "После": self.data_well.dict_nkt_after
                    },
                    'штанги': {
                        'До': self.data_well.dict_sucker_rod,
                        "После": self.data_well.dict_sucker_rod_after
                    },
                    'ожидаемые': {
                        'нефть': self.data_well.expected_oil,
                        'вода': self.data_well.water_cut,
                        'обводненность': self.data_well.percent_water,
                        'давление': self.data_well.expected_pressure,
                        'приемистость': self.data_well.expected_pickup
                    },
                    'данные': {
                        'пробуренный забой': self.data_well.bottom_hole_drill.get_value,
                        'искусственный забой': self.data_well.bottom_hole_artificial.get_value,
                        'максимальный угол': self.data_well.max_angle.get_value,
                        'глубина': self.data_well.max_angle_depth.get_value,
                        'максимальное ожидаемое давление': self.data_well.max_expected_pressure.get_value,
                        'максимальное допустимое давление': self.data_well.max_admissible_pressure.get_value,
                        'диаметр долото при бурении': self.data_well.diameter_doloto_ek.get_value
                    },
                    'ПВР план': self.data_well.dict_perforation_project
                }
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка в обработке {e}')
            data_list.pause = False
            return

        if str(self.data_well.paker_before["before"]).lower() not in ['0', 0, '-', 'отсут', '', None]:
            try:
                paker_diameter = TabPageSo.paker_diameter_select(self, float(
                    self.data_well.depth_fond_paker_before["before"]))
                if str(paker_diameter) not in str(self.data_well.paker_before["before"]):
                    self.data_well.check_data_in_pz.append(
                        f'Не корректно указан диаметр фондового пакера в карте спуска '
                        f'ремонта {self.data_well.paker_before["after"].split("/")[0]} требуется пакер '
                        f'диаметром {paker_diameter}')

            except Exception as e:
                QMessageBox.information(self, 'Ошибка обработки', f'ошибка проверки ПЗ в части соответствия '
                                                                  f'диаметра пакера \n {type(e).__name__}\n\n{str(e)}')
                return
        self.definition_open_trunk_well()

        data_list.pause = False
        self.close()
        self.close_modal_forcefully()
    @staticmethod
    def check_date_format(date_string):
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        return bool(re.match(pattern, date_string))

    def check_if_none(self, value):
        if value is None or 'отс' in str(value).lower() or value == '-' or str(value) == '0':
            return 0
        elif isinstance(value, int):
            return int(value)
        elif str(value).replace('.', '').replace(',', '').isdigit():

            if str(round(float(str(value).replace(',', '.')), 1))[-1] == "0":

                return int(float(str(value).replace(',', '.')))
            else:
                return round(float(str(value).replace(',', '.')), 1)
        else:
            return value

    def if_string_list(self, string):
        try:
            if len(string.split('-')) == 2:
                return True
            else:
                if str(string) == 'отсут' or string == 0:
                    return True
                else:
                    return False
        except:
            if str(string) == 'отсут' or string == 0:
                return True
            else:
                return False

    def if_none(self, string):
        if str(string) == "['0']":
            return False
        elif str(string) == 'отсут':
            return True


        elif str(string).replace('.', '').replace(',', '').isdigit():
            if float(string.replace(',', '.')) < 5000:
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = DataWindow()
    QTimer.singleShot(2000, DataWindow.updateLabel)
    # window.show()
    app.exec_()
