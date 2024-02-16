from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QRegExpValidator, QColor, QPalette
from main import MyWindow
import re


class FloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(FloatLineEdit, self).__init__(parent)

        # Устанавливаем валидатор для проверки на float

        reg = QRegExp("[0-9.отсут]*")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.setValidator(pValidator)

    def focusOutEvent(self, event):
        # При потере фокуса проверяем, является ли текст float
        if self.validator().validate(self.text(), 0)[0] != QValidator.Acceptable:
            # Если текст не является числом, меняем цвет фона на красный
            palette = self.palette()
            palette.setColor(QPalette.Base, QColor(Qt.red))
            self.setPalette(palette)
        else:
            # Если текст является числом, возвращаем цвет фона по умолчанию
            self.setPalette(self.parentWidget().palette())


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from open_pz import CreatePZ

        self.labels_nkt = {}
        self.labels_nkt_po = {}
        self.labels_sucker = {}
        self.labels_sucker_po = {}

        self.column_direction_diametr_Label = QLabel("диаметр направление", self)
        self.column_direction_diametr_Edit = FloatLineEdit(self)
        if CreatePZ.column_direction_True:
            self.column_direction_diametr_Edit.setText(f'{CreatePZ.column_direction_diametr}')
        else:
            self.column_direction_diametr_Edit.setText(f'отсут')

        self.column_direction_wall_thickness_Label = QLabel("Толщина стенки направление", self)
        self.column_direction_wall_thickness_Edit = FloatLineEdit(self)
        if CreatePZ.column_direction_True:
            self.column_direction_wall_thickness_Edit.setText(f'{CreatePZ.column_direction_wall_thickness}')
        else:
            self.column_direction_wall_thickness_Edit.setText(f'отсут')
        self.column_direction_lenght_Label = QLabel("башмак направления", self)
        self.column_direction_lenght_Edit = FloatLineEdit(self)
        if CreatePZ.column_direction_True:
            self.column_direction_lenght_Edit.setText(f'{CreatePZ.column_direction_lenght}')
        else:
            self.column_direction_lenght_Edit.setText(f'отсут')

        self.level_cement_direction_Label = QLabel("Уровень цемента за направление", self)
        self.level_cement_direction_Edit = FloatLineEdit(self)
        if CreatePZ.column_direction_True:
            self.level_cement_direction_Edit.setText(f'{CreatePZ.level_cement_direction}')
        else:
            self.level_cement_direction_Edit.setText(f'отсут')

        self.column_conductor_diametr_Label = QLabel("диаметр кондуктора", self)
        self.column_conductor_diametr_Edit = FloatLineEdit(self)
        self.column_conductor_diametr_Edit.setText(f'{CreatePZ.column_conductor_diametr}')

        self.column_conductor_wall_thickness_Label = QLabel("Толщина стенки ", self)
        self.column_conductor_wall_thickness_Edit = FloatLineEdit(self)
        self.column_conductor_wall_thickness_Edit.setText(f'{CreatePZ.column_conductor_wall_thickness}')

        self.column_conductor_lenght_Label = QLabel("башмак кондуктора", self)
        self.column_conductor_lenght_Edit = FloatLineEdit(self)
        self.column_conductor_lenght_Edit.setText(f'{CreatePZ.column_conductor_lenght}')

        self.level_cement_conductor_Label = QLabel("Уровень цемента за кондуктором", self)
        self.level_cement_conductor_Edit = FloatLineEdit(self)
        self.level_cement_conductor_Edit.setText(f'{CreatePZ.level_cement_conductor}')

        self.columnLabel = QLabel("диаметр ЭК", self)
        self.columnType = FloatLineEdit(self)
        self.columnType.setText(f"{self.ifNone(CreatePZ.column_diametr)}")

        # self.columnType.setClearButtonEnabled(True)

        self.column_wall_thicknessLabel = QLabel("Толщина стенки ЭК", self)
        self.column_wall_thicknessEditType2 = FloatLineEdit(self)
        self.column_wall_thicknessEditType2.setText(f"{self.ifNone(CreatePZ.column_wall_thickness)}")
        # self.column_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.shoe_columnLabel = QLabel("башмак ЭК", self)
        self.shoe_columnEditType2 = FloatLineEdit(self)
        self.shoe_columnEditType2.setText(f"{self.ifNone(CreatePZ.shoe_column)}")
        # self.shoe_columnEditType2.setClearButtonEnabled(True)

        self.column_add_trueLabel = QLabel("наличие Доп. колонны", self)
        self.column_add_true_comboBox = QComboBox(self)
        self.column_add_true_comboBox.addItems(['в наличии', 'отсутствует'])
        if CreatePZ.column_additional == True:
            column_add = 0
        else:
            column_add = 1
        self.column_add_true_comboBox.setCurrentIndex(column_add)

        self.column_addLabel = QLabel("диаметр доп. колонны", self)
        self.column_addEditType = FloatLineEdit(self)
        self.column_addEditType.setText(f"{self.ifNone(CreatePZ.column_additional_diametr)}")
        # self.column_addEditType.setClearButtonEnabled(True)

        self.column_add_wall_thicknessLabel = QLabel("Толщина стенки доп.колонны", self)
        self.column_add_wall_thicknessEditType2 = FloatLineEdit(self)
        self.column_add_wall_thicknessEditType2.setText(F'{self.ifNone(CreatePZ.column_additional_wall_thickness)}')
        # self.column_add_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.head_column_addLabel = QLabel("Голова доп колонны", self)
        self.head_column_add_EditType2 = FloatLineEdit(self)
        self.head_column_add_EditType2.setText(f'{self.ifNone(CreatePZ.head_column_additional)}')

        self.shoe_column_addLabel = QLabel("башмак доп колонны", self)
        self.shoe_column_add_EditType2 = FloatLineEdit(self)
        self.shoe_column_add_EditType2.setText(f'{self.ifNone(CreatePZ.shoe_column_additional)}')
        # self.shoe_column_add_EditType2.setClearButtonEnabled(True)

        self.bottomhole_drill_Label = QLabel('Пробуренный забой')
        self.bottomhole_drill_EditType = FloatLineEdit(self)
        self.bottomhole_drill_EditType.setText(f'{self.ifNone(CreatePZ.bottomhole_drill)}')

        self.bottomhole_artificial_Label = QLabel('Искусственный забой')
        self.bottomhole_artificial_EditType = FloatLineEdit(self)
        self.bottomhole_artificial_EditType.setText(f'{self.ifNone(CreatePZ.bottomhole_artificial)}')

        self.current_bottom_Label = QLabel('Текущий забой')
        self.current_bottom_EditType = FloatLineEdit(self)
        self.current_bottom_EditType.setText(f'{self.ifNone(CreatePZ.current_bottom)}')

        self.max_angle_Label = QLabel('Максимальный угол')
        self.max_angle_EditType = FloatLineEdit(self)
        self.max_angle_EditType.setText(f'{self.ifNone(CreatePZ.max_angle)}')

        self.max_expected_pressure_Label = QLabel('Максимальный ожидаемое давление')
        self.max_expected_pressure_EditType = FloatLineEdit(self)
        self.max_expected_pressure_EditType.setText(f'{self.ifNone(CreatePZ.max_expected_pressure)}')

        self.max_admissible_pressure_Label = QLabel('Максимальный допустимое давление')
        self.max_admissible_pressure_EditType = FloatLineEdit(self)
        self.max_admissible_pressure_EditType.setText(f'{self.ifNone(CreatePZ.max_admissible_pressure)}')

        self.pump_SHGN_do_Label = QLabel('Штанговый насос')
        self.pump_SHGN_do_EditType = QLineEdit(self)
        self.pump_SHGN_do_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_SHGN["do"])}')

        self.pump_SHGN_depth_do_Label = QLabel('Глубина штангового насоса')
        self.pump_SHGN_depth_do_EditType = FloatLineEdit(self)
        if self.pump_SHGN_do_EditType.text() != 'отсут':
            self.pump_SHGN_depth_do_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_SHGN_h["do"])}')
        else:
            self.pump_SHGN_depth_do_EditType.setText('отсут')

        self.pump_SHGN_posle_Label = QLabel('Плановый штанговый насос')
        self.pump_SHGN_posle_EditType = QLineEdit(self)
        self.pump_SHGN_posle_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_SHGN["posle"])}')

        self.pump_SHGN_depth_posle_Label = QLabel('Плановая глубина спуска насоса')
        self.pump_SHGN_depth_posle_EditType = FloatLineEdit(self)
        if self.pump_SHGN_posle_EditType.text() != 'отсут':
            self.pump_SHGN_depth_posle_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_SHGN_h["posle"])}')
        else:
            self.pump_SHGN_depth_posle_EditType.setText('отсут')

        self.pump_ECN_do_Label = QLabel('Спущенный ЭЦН')
        self.pump_ECN_do_EditType = QLineEdit(self)
        self.pump_ECN_do_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_ECN["do"])}')

        self.pump_ECN_depth_do_Label = QLabel('Глубина спуска ЭЦН')
        self.pump_ECN_depth_do_EditType = FloatLineEdit(self)
        if self.pump_ECN_do_EditType.text() != 'отсут':
            self.pump_ECN_depth_do_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_ECN_h["do"])}')
        else:
            self.pump_ECN_depth_do_EditType.setText('отсут')

        self.pump_ECN_posle_Label = QLabel('Плановый ЭЦН на спуск')
        self.pump_ECN_posle_EditType = QLineEdit(self)
        self.pump_ECN_posle_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_ECN["posle"])}')

        self.pump_ECN_depth_posle_Label = QLabel('Плановая глубина спуска ЭЦН')
        self.pump_ECN_depth_posle_EditType = FloatLineEdit(self)
        if self.pump_ECN_posle_EditType.text() != 'отсут':
            self.pump_ECN_depth_posle_EditType.setText(f'{self.ifNone(CreatePZ.dict_pump_ECN_h["posle"])}')
        else:
            self.pump_ECN_depth_posle_EditType.setText('отсут')

        self.paker_do_Label = QLabel('Спущенный пакер')
        self.paker_do_EditType = QLineEdit(self)
        self.paker_do_EditType.setText(f'{self.ifNone(CreatePZ.paker_do["do"])}')

        self.paker_depth_do_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_do_EditType = FloatLineEdit(self)
        self.paker_depth_do_EditType.setText(f'{self.ifNone(CreatePZ.H_F_paker_do["do"])}')

        self.paker_posle_Label = QLabel('пакер на спуск')
        self.paker_posle_EditType = QLineEdit(self)
        self.paker_posle_EditType.setText(f'{self.ifNone(CreatePZ.paker_do["posle"])}')

        self.paker_depth_posle_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_posle_EditType = FloatLineEdit(self)
        self.paker_depth_posle_EditType.setText(f'{self.ifNone(CreatePZ.H_F_paker_do["posle"])}')

        self.paker2_do_Label = QLabel('Спущенный пакер')
        self.paker2_do_EditType = QLineEdit(self)
        self.paker2_do_EditType.setText(f'{self.ifNone(CreatePZ.paker2_do["do"])}')

        self.paker2_depth_do_Label = QLabel('Глубина спуска пакера')
        self.paker2_depth_do_EditType = FloatLineEdit(self)
        self.paker2_depth_do_EditType.setText(str(self.ifNone(str(CreatePZ.H_F_paker2_do["do"]))))

        self.paker2_posle_Label = QLabel('пакер на спуск')
        self.paker2_posle_EditType = QLineEdit(self)
        # print(self.ifNone(CreatePZ.paker2_do["posle"]))
        self.paker2_posle_EditType.setText(self.ifNone(CreatePZ.paker2_do["posle"]))

        self.paker2_depth_posle_Label = QLabel('Глубина спуска пакера')
        self.paker2_depth_posle_EditType = FloatLineEdit(self)
        self.paker2_depth_posle_EditType.setText(str(self.ifNone(str(CreatePZ.H_F_paker2_do["posle"]))))
        # print(f' насос спуск {CreatePZ.dict_pump["posle"]}')

        self.static_level_Label = QLabel('Статический уровень в скважине')
        self.static_level_EditType = FloatLineEdit(self)
        self.static_level_EditType.setText(str(self.ifNone(CreatePZ.static_level)))

        self.dinamic_level_Label = QLabel('Динамический уровень в скважине')
        self.dinamic_level_EditType = FloatLineEdit(self)
        self.dinamic_level_EditType.setText(str(self.ifNone(CreatePZ.dinamic_level)))

        self.nkt_do_label = QLabel('НКТ  до ремонта')
        self.nkt_posle_label = QLabel('НКТ плановое согласно расчета')

        self.sucker_rod_label = QLabel('Штанги  до ремонта')
        self.sucker_rod_po_label = QLabel('Штанги плановое согласно расчета')

        self.dict_nkt = CreatePZ.dict_nkt
        self.dict_nkt_po = CreatePZ.dict_nkt_po
        self.dict_sucker_rod = CreatePZ.dict_sucker_rod
        self.dict_sucker_rod_po = CreatePZ.dict_sucker_rod_po

        grid = QGridLayout(self)
        grid.addWidget(self.column_direction_diametr_Label, 0, 0)
        grid.addWidget(self.column_direction_diametr_Edit, 1, 0)
        grid.addWidget(self.column_direction_wall_thickness_Label, 0, 1)
        grid.addWidget(self.column_direction_wall_thickness_Edit, 1, 1)
        grid.addWidget(self.column_direction_lenght_Label, 0, 2)
        grid.addWidget(self.column_direction_lenght_Edit, 1, 2)
        grid.addWidget(self.level_cement_direction_Label, 0, 4)
        grid.addWidget(self.level_cement_direction_Edit, 1, 4)

        grid.addWidget(self.column_conductor_diametr_Label, 2, 0)
        grid.addWidget(self.column_conductor_diametr_Edit, 3, 0)
        grid.addWidget(self.column_conductor_wall_thickness_Label, 2, 1)
        grid.addWidget(self.column_conductor_wall_thickness_Edit, 3, 1)
        grid.addWidget(self.column_conductor_lenght_Label, 2, 2)
        grid.addWidget(self.column_conductor_lenght_Edit, 3, 2)
        grid.addWidget(self.level_cement_conductor_Label, 2, 4)
        grid.addWidget(self.level_cement_conductor_Edit, 3, 4)

        grid.addWidget(self.columnLabel, 8, 0)
        grid.addWidget(self.columnType, 9, 0)
        grid.addWidget(self.column_wall_thicknessLabel, 8, 1)
        grid.addWidget(self.column_wall_thicknessEditType2, 9, 1)
        grid.addWidget(self.shoe_columnLabel, 8, 2)
        grid.addWidget(self.shoe_columnEditType2, 9, 2)
        grid.addWidget(self.column_add_trueLabel, 8, 3)
        grid.addWidget(self.column_add_true_comboBox, 9, 3)
        grid.addWidget(self.column_addLabel, 8, 4)
        grid.addWidget(self.column_addEditType, 9, 4)
        grid.addWidget(self.column_add_wall_thicknessLabel, 8, 5)
        grid.addWidget(self.column_add_wall_thicknessEditType2, 9, 5)
        grid.addWidget(self.head_column_addLabel, 8, 6)
        grid.addWidget(self.head_column_add_EditType2, 9, 6)
        grid.addWidget(self.shoe_column_addLabel, 8, 7)
        grid.addWidget(self.shoe_column_add_EditType2, 9, 7)

        grid.addWidget(self.bottomhole_drill_Label, 10, 0)
        grid.addWidget(self.bottomhole_drill_EditType, 11, 0)
        grid.addWidget(self.bottomhole_artificial_Label, 10, 1)
        grid.addWidget(self.bottomhole_artificial_EditType, 11, 1)
        grid.addWidget(self.current_bottom_Label, 10, 2)
        grid.addWidget(self.current_bottom_EditType, 11, 2)
        grid.addWidget(self.max_angle_Label, 10, 3)
        grid.addWidget(self.max_angle_EditType, 11, 3)
        grid.addWidget(self.max_expected_pressure_Label, 10, 4)
        grid.addWidget(self.max_expected_pressure_EditType, 11, 4)
        grid.addWidget(self.max_admissible_pressure_Label, 10, 5)
        grid.addWidget(self.max_admissible_pressure_EditType, 11, 5)
        grid.addWidget(self.pump_ECN_do_Label, 13, 0)
        grid.addWidget(self.pump_ECN_do_EditType, 14, 0)
        grid.addWidget(self.pump_ECN_depth_do_Label, 13, 1)
        grid.addWidget(self.pump_ECN_depth_do_EditType, 14, 1)
        grid.addWidget(self.pump_ECN_posle_Label, 13, 4)
        grid.addWidget(self.pump_ECN_posle_EditType, 14, 4)
        grid.addWidget(self.pump_ECN_depth_posle_Label, 13, 5)
        grid.addWidget(self.pump_ECN_depth_posle_EditType, 14, 5)

        grid.addWidget(self.pump_SHGN_do_Label, 15, 0)
        grid.addWidget(self.pump_SHGN_do_EditType, 16, 0)
        grid.addWidget(self.pump_SHGN_depth_do_Label, 15, 1)
        grid.addWidget(self.pump_SHGN_depth_do_EditType, 16, 1)
        grid.addWidget(self.pump_SHGN_posle_Label, 15, 4)
        grid.addWidget(self.pump_SHGN_posle_EditType, 16, 4)
        grid.addWidget(self.pump_SHGN_depth_posle_Label, 15, 5)
        grid.addWidget(self.pump_SHGN_depth_posle_EditType, 16, 5)

        grid.addWidget(self.paker_do_Label, 17, 0)
        grid.addWidget(self.paker_do_EditType, 18, 0)
        grid.addWidget(self.paker_depth_do_Label, 17, 1)
        grid.addWidget(self.paker_depth_do_EditType, 18, 1)
        grid.addWidget(self.paker_posle_Label, 17, 4)
        grid.addWidget(self.paker_posle_EditType, 18, 4)
        grid.addWidget(self.paker_depth_posle_Label, 17, 5)
        grid.addWidget(self.paker_depth_posle_EditType, 18, 5)

        grid.addWidget(self.paker2_do_Label, 19, 0)
        grid.addWidget(self.paker2_do_EditType, 20, 0)
        grid.addWidget(self.paker2_depth_do_Label, 19, 1)
        grid.addWidget(self.paker2_depth_do_EditType, 20, 1)
        grid.addWidget(self.paker2_posle_Label, 19, 4)
        grid.addWidget(self.paker2_posle_EditType, 20, 4)
        grid.addWidget(self.paker2_depth_posle_Label, 19, 5)
        grid.addWidget(self.paker2_depth_posle_EditType, 20, 5)

        grid.addWidget(self.static_level_Label, 21, 2)
        grid.addWidget(self.static_level_EditType, 22, 2)
        grid.addWidget(self.dinamic_level_Label, 21, 3)
        grid.addWidget(self.dinamic_level_EditType, 22, 3)

        grid.addWidget(self.nkt_do_label, 23, 1)
        grid.addWidget(self.nkt_posle_label, 24, 5)

        grid.addWidget(self.sucker_rod_label, 25, 1)
        grid.addWidget(self.sucker_rod_po_label, 26, 5)

        # добавление строк с НКТ спущенных
        if len(self.dict_nkt) != 0:
            n = 1
            for nkt, lenght in self.dict_nkt.items():
                # print(f'НКТ {nkt, lenght}')
                nkt_line_edit = QLineEdit(self)
                nkt_line_edit.setText(str(self.ifNone(nkt)))

                lenght_line_edit = QLineEdit(self)
                lenght_line_edit.setText(str(self.ifNone(lenght)))

                grid.addWidget(nkt_line_edit, 22 + n, 1)
                grid.addWidget(lenght_line_edit, 22 + n, 2)

                # Переименование атрибута
                setattr(self, f"{nkt}_{n}_line", nkt_line_edit)
                setattr(self, f"{lenght}_{n}_line", lenght_line_edit)

                self.labels_nkt[n] = (nkt_line_edit, lenght_line_edit)
                n += 1
        else:
            nkt_line_edit = QLineEdit(self)
            lenght_line_edit = QLineEdit(self)

            setattr(self, f"nkt_line", nkt_line_edit)
            setattr(self, f"lenght_line", lenght_line_edit)

            self.labels_nkt[1] = (nkt_line_edit, lenght_line_edit)

            grid.addWidget(nkt_line_edit, 23, 1)
            grid.addWidget(lenght_line_edit, 23, 2)

        # добавление строк с штанг спущенных
        if len(self.dict_sucker_rod) != 0:
            n = 1
            for sucker, lenght in self.dict_sucker_rod.items():
                sucker_rod_line_edit = QLineEdit(self)
                sucker_rod_line_edit.setText(str(self.ifNone(sucker)))

                lenght_sucker_line_edit = QLineEdit(self)
                lenght_sucker_line_edit.setText(str(self.ifNone(lenght)))

                grid.addWidget(sucker_rod_line_edit, 27 + n, 1)
                grid.addWidget(lenght_sucker_line_edit, 27 + n, 2)

                # Переименование атрибута
                setattr(self, f"sucker_{n}_line", sucker_rod_line_edit)
                setattr(self, f"lenght_{n}_line", lenght_sucker_line_edit)

                self.labels_sucker[n] = (sucker_rod_line_edit, lenght_sucker_line_edit)
                n += 1
        else:
            sucker_rod_line_edit = QLineEdit(self)
            lenght_sucker_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"sucker_line", sucker_rod_line_edit)
            setattr(self, f"lenght_line", lenght_sucker_line_edit)

            self.labels_sucker[1] = (sucker_rod_line_edit, lenght_sucker_line_edit)

            grid.addWidget(sucker_rod_line_edit, 28, 1)
            grid.addWidget(lenght_sucker_line_edit, 28, 2)

        if len(self.dict_nkt_po) != 0:
            # добавление строк с НКТ плановых
            n = 1
            for nkt_po, lenght_po in self.dict_nkt_po.items():
                # print(f'НКТ план {nkt_po, lenght_po}')

                nkt_po_line_edit = QLineEdit(self)
                nkt_po_line_edit.setText(str(self.ifNone(nkt_po)))

                lenght_po_line_edit = QLineEdit(self)
                lenght_po_line_edit.setText(str(self.ifNone(lenght_po)))

                grid.addWidget(nkt_po_line_edit, 22 + n, 5)
                grid.addWidget(lenght_po_line_edit, 22 + n, 6)

                # Переименование атрибута
                setattr(self, f"nkt_po_{n}_line", nkt_po_line_edit)
                setattr(self, f"lenght_po_{n}_line", lenght_po_line_edit)

                self.labels_nkt_po[n] = (nkt_po_line_edit, lenght_po_line_edit)
                n += 1
        else:
            nkt_po_line_edit = QLineEdit(self)
            lenght_po_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"nkt_po_line", nkt_po_line_edit)
            setattr(self, f"lenght_po_line", lenght_po_line_edit)

            self.labels_nkt_po[1] = (nkt_po_line_edit, lenght_po_line_edit)

            grid.addWidget(nkt_po_line_edit, 23, 1)
            grid.addWidget(lenght_po_line_edit, 23, 2)
        # добавление строк с штангами плановых

        if len(self.dict_sucker_rod_po) != 0:
            n = 1
            for sucker_po, lenght_po in self.dict_sucker_rod_po.items():
                # print(f'штанги план {sucker_po, lenght_po}')
                sucker_rod_po_line_edit = QLineEdit(self)
                sucker_rod_po_line_edit.setText(str(self.ifNone(sucker_po)))

                lenght_sucker_po_line_edit = QLineEdit(self)
                lenght_sucker_po_line_edit.setText(str(self.ifNone(lenght_po)))

                grid.addWidget(sucker_rod_po_line_edit, 27 + n, 5)
                grid.addWidget(lenght_sucker_po_line_edit, 27 + n, 6)

                # Переименование атрибута
                setattr(self, f"sucker_{n}_line", sucker_rod_po_line_edit)
                setattr(self, f"lenght_{n}_line", lenght_sucker_po_line_edit)

                self.labels_sucker_po[n] = (sucker_rod_po_line_edit, lenght_sucker_po_line_edit)
                n += 1
        else:
            sucker_rod_po_line_edit = QLineEdit(self)
            lenght_sucker_po_line_edit = QLineEdit(self)

            # Переименование атрибута
            setattr(self, f"sucker_line", sucker_rod_po_line_edit)
            setattr(self, f"lenght_line", lenght_sucker_po_line_edit)

            self.labels_sucker_po[1] = (sucker_rod_po_line_edit, lenght_sucker_po_line_edit)

            grid.addWidget(sucker_rod_po_line_edit, 28, 5)
            grid.addWidget(lenght_sucker_po_line_edit, 28, 6)

    def ifNone(self, string):

        if str(string) in ['0', str(None), '-']:
            return 'отсут'
        elif str(string).replace('.', '').replace(',', '').isdigit():

            # print(str(round(float(string), 1))[-1] == '0', int(string), float(string))
            return int(float(string)) if str(round(float(str(string).replace(',', '.')), 1))[-1] == "0" else \
                round(float(str(string).replace(',', '.')), 1)
        else:
            return str(string)

    def updateLabel(self):
        # self.dinamic_level_Label
        self.columnType.setText()
        self.column_addEditType.setText()
        self.update()


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Проверка корректности данных')


class DataWindow(QMainWindow):

    def __init__(self, parent=None):
        super(DataWindow, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        self.tabWidget = TabWidget()
        # self.tableWidget = QTableWidget(0, 4)
        # self.labels_nkt = labels_nkt

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.addRowTable)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def addRowTable(self):
        from open_pz import CreatePZ

        columnType = self.tabWidget.currentWidget().columnType.text()
        column_wall_thickness = self.tabWidget.currentWidget().column_wall_thicknessEditType2.text()
        shoe_column = self.tabWidget.currentWidget().shoe_columnEditType2.text()
        column_add_True = str(self.tabWidget.currentWidget().column_add_true_comboBox.currentText())
        if column_add_True == 'в наличии':
            CreatePZ.column_additional = True
        else:
            CreatePZ.column_additional = False
        column_additional_diametr = self.tabWidget.currentWidget().column_addEditType.text()
        column_additional_wall_thickness = self.tabWidget.currentWidget().column_add_wall_thicknessEditType2.text()
        shoe_column_additional = self.tabWidget.currentWidget().shoe_column_add_EditType2.text()
        head_column_additional = self.tabWidget.currentWidget().head_column_add_EditType2.text()
        bottomhole_drill = self.tabWidget.currentWidget().bottomhole_drill_EditType.text()
        bottomhole_artificial = self.tabWidget.currentWidget().bottomhole_artificial_EditType.text()
        current_bottom = self.tabWidget.currentWidget().current_bottom_EditType.text()
        max_angle = self.tabWidget.currentWidget().max_angle_EditType.text()
        max_expected_pressure = self.tabWidget.currentWidget().max_expected_pressure_EditType.text()
        max_admissible_pressure = self.tabWidget.currentWidget().max_admissible_pressure_EditType.text()

        column_direction_diametr = self.tabWidget.currentWidget().column_direction_diametr_Edit.text()
        column_direction_wall_thickness = self.tabWidget.currentWidget().column_direction_wall_thickness_Edit.text()
        column_direction_lenght = self.tabWidget.currentWidget().column_direction_lenght_Edit.text()
        level_cement_direction = self.tabWidget.currentWidget().level_cement_direction_Edit.text()
        column_conductor_diametr = self.tabWidget.currentWidget().column_conductor_diametr_Edit.text()
        column_conductor_wall_thickness = self.tabWidget.currentWidget().column_conductor_wall_thickness_Edit.text()
        column_conductor_lenght = self.tabWidget.currentWidget().column_conductor_lenght_Edit.text()
        level_cement_conductor = self.tabWidget.currentWidget().level_cement_conductor_Edit.text()

        dict_pump_SHGN_do = str(self.tabWidget.currentWidget().pump_SHGN_do_EditType.text())
        dict_pump_SHGN_h_do = self.tabWidget.currentWidget().pump_SHGN_depth_do_EditType.text()

        dict_pump_SHGN_posle = str(self.tabWidget.currentWidget().pump_SHGN_posle_EditType.text())
        dict_pump_SHGN_h_posle = str(self.tabWidget.currentWidget().pump_SHGN_depth_posle_EditType.text())

        dict_pump_ECN_do = str(self.tabWidget.currentWidget().pump_ECN_do_EditType.text())
        dict_pump_ECN_h_do = self.tabWidget.currentWidget().pump_ECN_depth_do_EditType.text()

        dict_pump_ECN_posle = str(self.tabWidget.currentWidget().pump_ECN_posle_EditType.text())
        dict_pump_ECN_h_posle = str(self.tabWidget.currentWidget().pump_ECN_depth_posle_EditType.text())

        # print(f'прио {type(dict_pump_h_posle)}')
        paker_do = str(self.tabWidget.currentWidget().paker_do_EditType.text())
        H_F_paker_do = str(self.tabWidget.currentWidget().paker_depth_do_EditType.text())
        paker_posle = self.tabWidget.currentWidget().paker_posle_EditType.text()
        H_F_paker_posle = self.tabWidget.currentWidget().paker_depth_posle_EditType.text()

        paker2_do = str(self.tabWidget.currentWidget().paker2_do_EditType.text())
        H_F_paker2_do = self.tabWidget.currentWidget().paker2_depth_do_EditType.text()
        paker2_posle = self.tabWidget.currentWidget().paker2_posle_EditType.text()
        H_F_paker2_posle = self.tabWidget.currentWidget().paker2_depth_posle_EditType.text()

        static_level = self.tabWidget.currentWidget().static_level_EditType.text()
        dinamic_level = self.tabWidget.currentWidget().dinamic_level_EditType.text()

        # Пересохранение данных по НКТ и штангам
        self.dict_sucker_rod = CreatePZ.dict_sucker_rod
        self.dict_sucker_rod = CreatePZ.dict_sucker_rod_po
        self.dict_nkt = CreatePZ.dict_nkt
        self.dict_nkt_po = CreatePZ.dict_nkt_po
        if self.dict_nkt:
            for key in range(1, len(self.dict_nkt)):
                CreatePZ.dict_nkt[self.tabWidget.currentWidget().labels_nkt[key][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_nkt[key][1].text())
        else:
            if self.tabWidget.currentWidget().labels_nkt[1][1].text():
                CreatePZ.dict_nkt[self.tabWidget.currentWidget().labels_nkt[1][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_nkt[1][1].text())
        if self.dict_nkt_po:
            for key in range(1, len(self.dict_nkt_po)):
                dict_nkt_correct = self.tabWidget.currentWidget().labels_nkt_po[key][1].text()

                CreatePZ.dict_nkt_po[self.tabWidget.currentWidget().labels_nkt_po[key][0].text()] = self.if_None(
                    dict_nkt_correct)
        else:
            if self.tabWidget.currentWidget().labels_nkt_po[1][1].text():
                CreatePZ.dict_nkt[self.tabWidget.currentWidget().labels_nkt_po[1][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_nkt_po[1][1].text())

        if self.dict_sucker_rod:
            for key in range(1, len(self.dict_sucker_rod)):
                # print(self.tabWidget.currentWidget().labels_sucker.keys())
                CreatePZ.dict_sucker_rod[self.tabWidget.currentWidget().labels_sucker[key][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_sucker[key][1].text())
        else:
            if self.tabWidget.currentWidget().labels_sucker[1][1].text():
                CreatePZ.dict_sucker_rod[self.tabWidget.currentWidget().labels_sucker[1][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_sucker[1][1].text())

        if self.dict_sucker_rod.items():
            for key in range(1, len(self.dict_sucker_rod.items())):
                CreatePZ.dict_sucker_rod_po[
                    self.tabWidget.currentWidget().labels_sucker_po[key][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_sucker_po[key][1].text())
        else:
            if self.tabWidget.currentWidget().labels_sucker_po[1][1].text():
                CreatePZ.dict_sucker_rod_po[
                    self.tabWidget.currentWidget().labels_sucker_po[1][0].text()] = self.if_None(
                    self.tabWidget.currentWidget().labels_sucker_po[1][1].text())

        close_file = True
        print(f'голова {[self.ifNum(columnType), self.ifNum(column_wall_thickness), self.ifNum(shoe_column)]}')
        if any([data_well == 'отсут' for data_well in
                [columnType, column_wall_thickness, shoe_column]]):
            msg = QMessageBox.information(self, 'Внимание', 'Не все поля в данных колонне соответствуют значениям')
            close_file = False
        elif CreatePZ.column_additional \
                and any([data_well == 'отсут' for data_well in
                     [column_additional_diametr,
                      column_additional_wall_thickness,
                      shoe_column_additional, head_column_additional]]):
            msg = QMessageBox.information(self, 'Внимание', 'Не все поля в доп колонне соответствуют значениям')
            close_file = False
        elif self.ifNum(bottomhole_artificial) is False \
           or self.ifNum(bottomhole_drill) is False \
           or self.ifNum(current_bottom) is False \
           or self.ifNum(max_angle) is False \
           or self.ifNum(max_admissible_pressure) is False \
           or self.ifNum(max_expected_pressure) is False \
           or self.ifNum(dict_pump_ECN_h_do) is False \
           or self.ifNum(static_level) is False \
           or self.ifNum(static_level) is False \
           or self.ifNum(dinamic_level) is False \
           or self.ifNum(dict_pump_ECN_h_posle) is False \
           or self.ifNum(dict_pump_SHGN_h_do) is False \
           or self.ifNum(dict_pump_SHGN_h_posle) is False \
           or self.ifNum(H_F_paker_do) is False \
           or self.ifNum(H_F_paker_posle) is False \
           or self.ifNum(H_F_paker2_do) is False \
           or self.ifNum(H_F_paker2_posle) is False \
           or self.ifNum(column_direction_diametr) is False \
           or self.ifNum(column_direction_wall_thickness) is False \
           or self.if_string_list(level_cement_direction) is False \
           or self.ifNum(column_conductor_diametr) is False \
           or self.ifNum(column_conductor_wall_thickness) is False:
           # or self.if_string_list(column_conductor_lenght) is False \
           # or self.if_string_list(column_direction_lenght) is False \
           # or self.if_string_list(level_cement_conductor) is False:

            msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            close_file = False

        elif any(['НВ' in dict_pump_SHGN_do.upper(), 'ШГН' in dict_pump_SHGN_do.upper(),
                  'НН' in dict_pump_SHGN_do.upper(), dict_pump_SHGN_do == 'отсут',
                  'RHAM' in dict_pump_SHGN_do]) is False \
             or any(['НВ' in dict_pump_SHGN_posle.upper(), 'ШГН' in dict_pump_SHGN_posle.upper(),
                     'НН' in dict_pump_SHGN_posle.upper(), dict_pump_SHGN_posle == 'отсут',
                     'RHAM' in dict_pump_SHGN_do]) is False \
             or any(['ЭЦН' in dict_pump_ECN_posle.upper(), 'ВНН' in dict_pump_ECN_posle.upper(),
                     dict_pump_ECN_posle == 'отсут']) is False \
             or (dict_pump_ECN_do != 'отсут' and dict_pump_ECN_h_do == 'отсут') \
             or (dict_pump_ECN_posle != 'отсут' and dict_pump_ECN_h_posle == 'отсут') \
             or (dict_pump_SHGN_do != 'отсут' and dict_pump_SHGN_h_do == 'отсут') \
             or (dict_pump_SHGN_posle != 'отсут' and dict_pump_SHGN_h_posle == 'отсут') \
             or (paker_do != 'отсут' and H_F_paker_do == 'отсут') \
             or (paker_posle != 'отсут' and H_F_paker_posle == 'отсут') \
             or (paker2_do != 'отсут' and H_F_paker2_do == 'отсут') \
             or (paker2_posle != 'отсут' and H_F_paker2_posle == 'отсут') \
             or any(['ЭЦН' in dict_pump_ECN_do.upper(), 'ВНН' in dict_pump_ECN_do.upper(),
                     dict_pump_ECN_do == 'отсут']) is False:

            msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            close_file = False

        elif self.if_None(20 if self.ifNum(head_column_additional) else head_column_additional) < 5:
        # print(self.if_None(head_column_additional))
            msg = QMessageBox.information(self, 'Внимание', 'В скважине отсутствует доп колонна')
            close_file = False

        elif all([pump for pump in [self.ifNum(dict_pump_ECN_do), self.ifNum(paker2_do),
                                               self.ifNum(dict_pump_SHGN_do), self.ifNum(paker_do)]]):
            voronka_question = QMessageBox.question(self, 'Внимание',
                                                    'Программа определила что в скважине до ремонта воронка, верно ли')
            if voronka_question == QMessageBox.StandardButton.No:
                close_file = False
            else:
                close_file = True

        elif all([pump for pump in [self.ifNum(dict_pump_ECN_posle), self.ifNum(paker2_posle),
                                               self.ifNum(dict_pump_SHGN_posle), self.ifNum(paker_posle)]]):

            voronka_question = QMessageBox.question(self, 'Внимание',
                                                    'Программа определила что в скважине После ремонта воронка, верно ли')
            if voronka_question == QMessageBox.StandardButton.No:
                close_file = False
            else:
                close_file = True

        if close_file is False:
            return
        elif close_file == True:
            CreatePZ.column_diametr = self.if_None(columnType)
            CreatePZ.column_wall_thickness = self.if_None(column_wall_thickness)
            CreatePZ.shoe_column = self.if_None(shoe_column)
            CreatePZ.column_additional_diametr = self.if_None(column_additional_diametr)
            CreatePZ.column_additional_wall_thickness = self.if_None(column_additional_wall_thickness)
            CreatePZ.shoe_column_additional = self.if_None(shoe_column_additional)
            CreatePZ.head_column_additional = self.if_None(head_column_additional)

            CreatePZ.bottomhole_drill = self.if_None(bottomhole_drill)
            CreatePZ.bottomhole_artificial = self.if_None(bottomhole_artificial)
            CreatePZ.current_bottom = self.if_None(current_bottom)
            CreatePZ.max_angle = self.if_None(max_angle)
            CreatePZ.max_expected_pressure = self.if_None(max_expected_pressure)
            CreatePZ.max_admissible_pressure = self.if_None(max_admissible_pressure)

            # print(f'макс {CreatePZ.max_expected_pressure}')
            CreatePZ.dict_pump_SHGN["do"] = self.if_None(dict_pump_SHGN_do)
            CreatePZ.dict_pump_SHGN_h["do"] = self.if_None(dict_pump_SHGN_h_do)
            CreatePZ.dict_pump_SHGN_h["posle"] = self.if_None(dict_pump_SHGN_h_posle)
            CreatePZ.dict_pump_SHGN["posle"] = self.if_None(dict_pump_SHGN_posle)

            CreatePZ.dict_pump_ECN["do"] = self.if_None(dict_pump_ECN_do)
            CreatePZ.dict_pump_ECN_h["do"] = self.if_None(dict_pump_ECN_h_do)
            CreatePZ.dict_pump_ECN["posle"] = self.if_None(dict_pump_ECN_posle)
            CreatePZ.dict_pump_ECN_h["posle"] = self.if_None(dict_pump_ECN_h_posle)

            CreatePZ.paker_do["do"] = self.if_None(paker_do)
            CreatePZ.H_F_paker_do["do"] = self.if_None(H_F_paker_do)
            CreatePZ.paker_do["posle"] = self.if_None(paker_posle)
            CreatePZ.H_F_paker_do["posle"] = self.if_None(H_F_paker_posle)

            CreatePZ.paker2_do["do"] = self.if_None(paker2_do)
            CreatePZ.H_F_paker2_do["do"] = self.if_None(H_F_paker2_do)
            CreatePZ.paker2_do["posle"] = self.if_None(paker2_posle)
            CreatePZ.H_F_paker2_do["posle"] = self.if_None(H_F_paker2_posle)
            CreatePZ.static_level = self.if_None(static_level)
            CreatePZ.dinamic_level = self.if_None(dinamic_level)
            # print(f' после ок {CreatePZ.dict_pump, CreatePZ.paker_do, CreatePZ.H_F_paker_do, CreatePZ.dict_pump_h}')

            CreatePZ.column_direction_diametr = self.if_None(column_direction_diametr)
            CreatePZ.column_direction_wall_thickness = self.if_None(column_direction_wall_thickness)
            CreatePZ.column_direction_lenght = self.if_None(column_direction_lenght)
            CreatePZ.level_cement_direction = self.if_None(level_cement_direction)
            CreatePZ.column_conductor_diametr = self.if_None(column_conductor_diametr)
            CreatePZ.column_conductor_wall_thickness = self.if_None(column_conductor_wall_thickness)
            CreatePZ.column_conductor_lenght = self.if_None(column_conductor_lenght)
            CreatePZ.level_cement_conductor = self.if_None(level_cement_conductor)

            CreatePZ.pause = False
            self.close()


    def if_None(self, value):
        if value is None or 'отс' in str(value).lower() or value == '-' or str(value) == 0:
            return 0
        elif isinstance(value, int):
            return int(value)
        elif str(value).replace('.', '').replace(',', '').isdigit():

            if str(round(float(value.replace(',', '.')), 1))[-1] == "0":

                return int(float(value.replace(',', '.')))
            else:

                return round(float(value.replace(',', '.')), 1)
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


    def ifNum(self, string):
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

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = DataWindow()
    QTimer.singleShot(2000, DataWindow.updateLabel)
    # window.show()
    app.exec_()
