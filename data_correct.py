from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from main import MyWindow


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from open_pz import CreatePZ

        self.columnLabel = QLabel("диаметр ЭК", self)
        self.columnType = QLineEdit(self)
        self.columnType.setPlaceholderText(f"{CreatePZ.column_diametr}")
        # self.columnType.setClearButtonEnabled(True)

        self.column_wall_thicknessLabel = QLabel("Толщина стенки ЭК", self)
        self.column_wall_thicknessEditType2 = QLineEdit(self)
        self.column_wall_thicknessEditType2.setPlaceholderText(f"{CreatePZ.column_wall_thickness}")
        # self.column_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.shoe_columnLabel = QLabel("башмак ЭК", self)
        self.shoe_columnEditType2 = QLineEdit(self)
        self.shoe_columnEditType2.setPlaceholderText(f"{CreatePZ.shoe_column}")
        # self.shoe_columnEditType2.setClearButtonEnabled(True)

        self.column_addLabel = QLabel("диаметр Доп. колонны", self)
        self.column_addEditType = QLineEdit(self)
        self.column_addEditType.setPlaceholderText(f"{CreatePZ.column_diametr}")
        # self.column_addEditType.setClearButtonEnabled(True)

        self.column_add_wall_thicknessLabel = QLabel("Толщина стенки доп.колонны", self)
        self.column_add_wall_thicknessEditType2 = QLineEdit(self)
        self.column_add_wall_thicknessEditType2.setPlaceholderText(F'{CreatePZ.column_additional_wall_thickness}')
        # self.column_add_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.shoe_column_addLabel = QLabel("башмак доп колонны", self)
        self.shoe_column_add_EditType2 = QLineEdit(self)
        self.shoe_column_add_EditType2.setPlaceholderText(f'{CreatePZ.shoe_column_additional}')
        # self.shoe_column_add_EditType2.setClearButtonEnabled(True)



        self.bottomhole_drill_Label = QLabel('Пробуренный забой')
        self.bottomhole_drill_EditType = QLineEdit(self)
        self.bottomhole_drill_EditType.setPlaceholderText(f'{CreatePZ.bottomhole_drill}')

        self.bottomhole_artificial_Label = QLabel('Искусственный забой')
        self.bottomhole_artificial_EditType = QLineEdit(self)
        self.bottomhole_artificial_EditType.setPlaceholderText(f'{CreatePZ.bottomhole_artificial}')

        self.current_bottom_Label = QLabel('Текущий забой')
        self.current_bottom_EditType = QLineEdit(self)
        self.current_bottom_EditType.setPlaceholderText(f'{CreatePZ.current_bottom}')

        self.max_angle_Label = QLabel('Максимальный угол')
        self.max_angle_EditType = QLineEdit(self)
        self.max_angle_EditType.setPlaceholderText(f'2')

        self.max_expected_pressure_Label = QLabel('Максимальный ожидаемое давление')
        self.max_expected_pressure_EditType = QLineEdit(self)
        self.max_expected_pressure_EditType.setPlaceholderText(f'{CreatePZ.max_expected_pressure}')

        self.max_admissible_pressure_Label = QLabel('Максимальный допустимое давление')
        self.max_admissible_pressure_EditType = QLineEdit(self)
        self.max_admissible_pressure_EditType.setPlaceholderText(f'{CreatePZ.max_admissible_pressure}')

        self.pump_do_Label = QLabel('Спущенный Насос')
        self.pump_do_EditType = QLineEdit(self)
        self.pump_do_EditType.setPlaceholderText(f'{CreatePZ.dict_pump["do"]}')

        self.pump_depth_do_Label = QLabel('Глубина спуска насоса')
        self.pump_depth_do_EditType = QLineEdit(self)
        self.pump_depth_do_EditType.setPlaceholderText(f'{CreatePZ.dict_pump_h["do"]}')

        self.pump_posle_Label = QLabel('Насос на спуск')
        self.pump_posle_EditType = QLineEdit(self)
        self.pump_posle_EditType.setPlaceholderText(f'{CreatePZ.dict_pump["posle"]}')

        self.pump_depth_posle_Label = QLabel('Глубина спуска насоса')
        self.pump_depth_posle_EditType = QLineEdit(self)
        self.pump_depth_posle_EditType.setPlaceholderText(f'{CreatePZ.dict_pump_h["posle"]}')

        self.paker_do_Label = QLabel('Спущенный пакер')
        self.paker_do_EditType = QLineEdit(self)
        self.paker_do_EditType.setPlaceholderText(f'{CreatePZ.paker_do["do"]}')

        self.paker_depth_do_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_do_EditType = QLineEdit(self)
        self.paker_depth_do_EditType.setPlaceholderText(f'{CreatePZ.H_F_paker_do["do"]}')

        self.paker_posle_Label = QLabel('пакер на спуск')
        self.paker_posle_EditType = QLineEdit(self)
        self.paker_posle_EditType.setPlaceholderText(f'{CreatePZ.paker_do["posle"]}')

        self.paker_depth_posle_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_posle_EditType = QLineEdit(self)
        self.paker_depth_posle_EditType.setPlaceholderText(f'{CreatePZ.H_F_paker_do["posle"]}')


        grid = QGridLayout(self)
        grid.addWidget(self.columnLabel, 0, 0)
        grid.addWidget(self.columnType, 1, 0)
        grid.addWidget(self.column_wall_thicknessLabel, 0, 1)
        grid.addWidget(self.column_wall_thicknessEditType2, 1, 1)
        grid.addWidget(self.shoe_columnLabel, 0, 2)
        grid.addWidget(self.shoe_columnEditType2, 1, 2)
        grid.addWidget(self.column_addLabel, 0, 3)
        grid.addWidget(self.column_addEditType, 1, 3)
        grid.addWidget(self.column_add_wall_thicknessLabel, 0, 4)
        grid.addWidget(self.column_add_wall_thicknessEditType2, 1, 4)
        grid.addWidget(self.shoe_column_addLabel, 0, 5)
        grid.addWidget(self.shoe_column_add_EditType2, 1, 5)
        grid.addWidget(self.bottomhole_drill_Label, 2, 0)
        grid.addWidget(self.bottomhole_drill_EditType, 3, 0)
        grid.addWidget(self.bottomhole_artificial_Label, 2, 1)
        grid.addWidget(self.bottomhole_artificial_EditType, 3, 1)
        grid.addWidget(self.current_bottom_Label, 2, 2)
        grid.addWidget(self.current_bottom_EditType, 3, 2)
        grid.addWidget(self.max_angle_Label, 2, 3)
        grid.addWidget(self.max_angle_EditType, 3, 3)
        grid.addWidget(self.max_expected_pressure_Label, 2, 4)
        grid.addWidget(self.max_expected_pressure_EditType, 3, 4)
        grid.addWidget(self.max_admissible_pressure_Label, 2, 5)
        grid.addWidget(self.max_admissible_pressure_EditType, 3, 5)
        grid.addWidget(self.pump_do_Label, 4, 0)
        grid.addWidget(self.pump_do_EditType, 5, 0)
        grid.addWidget(self.pump_depth_do_Label, 4, 1)
        grid.addWidget(self.pump_depth_do_EditType, 5, 1)
        grid.addWidget(self.pump_posle_Label, 4, 4)
        grid.addWidget(self.pump_posle_EditType, 5, 4)
        grid.addWidget(self.pump_depth_posle_Label, 4, 5)
        grid.addWidget(self.pump_depth_posle_EditType, 5, 5)
        grid.addWidget(self.paker_do_Label, 6, 0)
        grid.addWidget(self.paker_do_EditType, 7, 0)
        grid.addWidget(self.paker_depth_do_Label, 6, 1)
        grid.addWidget(self.paker_depth_do_EditType, 7, 1)
        grid.addWidget(self.paker_posle_Label, 6, 4)
        grid.addWidget(self.paker_posle_EditType, 7, 4)
        grid.addWidget(self.paker_depth_posle_Label, 6, 5)
        grid.addWidget(self.paker_depth_posle_EditType, 7, 5)

        #

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Проверка корректности данных')


class DataWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        # self.setCentralWidget(self.centralWidget)

        self.tabWidget = TabWidget()
        # self.tableWidget = QTableWidget(0, 4)


        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.addRowTable)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)


    def addRowTable(self):
        from open_pz import CreatePZ
        CreatePZ.column_diametr = CreatePZ.column_diametr
#
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = DataWindow()
    # window.show()
    sys.exit(app.exec_())