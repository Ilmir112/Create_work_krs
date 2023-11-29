from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import re
from main import MyWindow


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from open_pz import CreatePZ

        self.columnLabel = QLabel("диаметр ЭК", self)
        self.columnType = QLineEdit(self)
        self.columnType.setText(f"{CreatePZ.column_diametr}")
        # self.columnType.setClearButtonEnabled(True)

        self.column_wall_thicknessLabel = QLabel("Толщина стенки ЭК", self)
        self.column_wall_thicknessEditType2 = QLineEdit(self)
        self.column_wall_thicknessEditType2.setText(f"{CreatePZ.column_wall_thickness}")
        # self.column_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.shoe_columnLabel = QLabel("башмак ЭК", self)
        self.shoe_columnEditType2 = QLineEdit(self)
        self.shoe_columnEditType2.setText(f"{CreatePZ.shoe_column}")
        # self.shoe_columnEditType2.setClearButtonEnabled(True)

        self.column_add_trueLabel = QLabel("наличие Доп. колонны", self)
        self.column_add_true_comboBox = QComboBox(self)
        self.column_add_true_comboBox.addItems(['в наличии', 'отсутствует'])
        if CreatePZ.column_additional == True:
            column_add = 0
        else:
            column_add = 1
        self.column_add_true_comboBox.setCurrentIndex(column_add)

        self.column_addLabel = QLabel("диаметр Доп. колонны", self)
        self.column_addEditType = QLineEdit(self)
        self.column_addEditType.setText(f"{CreatePZ.column_additional_diametr}")
        # self.column_addEditType.setClearButtonEnabled(True)

        self.column_add_wall_thicknessLabel = QLabel("Толщина стенки доп.колонны", self)
        self.column_add_wall_thicknessEditType2 = QLineEdit(self)
        self.column_add_wall_thicknessEditType2.setText(F'{CreatePZ.column_additional_wall_thickness}')
        # self.column_add_wall_thicknessEditType2.setClearButtonEnabled(True)

        self.head_column_addLabel = QLabel("Голова доп колонны", self)
        self.head_column_add_EditType2 = QLineEdit(self)
        self.head_column_add_EditType2.setText(f'{CreatePZ.head_column_additional}')

        self.shoe_column_addLabel = QLabel("башмак доп колонны", self)
        self.shoe_column_add_EditType2 = QLineEdit(self)
        self.shoe_column_add_EditType2.setText(f'{CreatePZ.shoe_column_additional}')
        # self.shoe_column_add_EditType2.setClearButtonEnabled(True)

        self.bottomhole_drill_Label = QLabel('Пробуренный забой')
        self.bottomhole_drill_EditType = QLineEdit(self)
        self.bottomhole_drill_EditType.setText(f'{CreatePZ.bottomhole_drill}')

        self.bottomhole_artificial_Label = QLabel('Искусственный забой')
        self.bottomhole_artificial_EditType = QLineEdit(self)
        self.bottomhole_artificial_EditType.setText(f'{CreatePZ.bottomhole_artificial}')

        self.current_bottom_Label = QLabel('Текущий забой')
        self.current_bottom_EditType = QLineEdit(self)
        self.current_bottom_EditType.setText(f'{CreatePZ.current_bottom}')

        self.max_angle_Label = QLabel('Максимальный угол')
        self.max_angle_EditType = QLineEdit(self)
        self.max_angle_EditType.setText(f'{CreatePZ.max_angle}')

        self.max_expected_pressure_Label = QLabel('Максимальный ожидаемое давление')
        self.max_expected_pressure_EditType = QLineEdit(self)
        self.max_expected_pressure_EditType.setText(f'{CreatePZ.max_expected_pressure}')

        self.max_admissible_pressure_Label = QLabel('Максимальный допустимое давление')
        self.max_admissible_pressure_EditType = QLineEdit(self)
        self.max_admissible_pressure_EditType.setText(f'{CreatePZ.max_admissible_pressure}')

        self.pump_do_Label = QLabel('Спущенный Насос')
        self.pump_do_EditType = QLineEdit(self)
        self.pump_do_EditType.setText(f'{CreatePZ.dict_pump["do"]}')

        self.pump_depth_do_Label = QLabel('Глубина спуска насоса')
        self.pump_depth_do_EditType = QLineEdit(self)
        self.pump_depth_do_EditType.setText(f'{CreatePZ.dict_pump_h["do"]}')

        self.pump_posle_Label = QLabel('Насос на спуск')
        self.pump_posle_EditType = QLineEdit(self)
        self.pump_posle_EditType.setText(f'{CreatePZ.dict_pump["posle"]}')

        self.pump_depth_posle_Label = QLabel('Глубина спуска насоса')
        self.pump_depth_posle_EditType = QLineEdit(self)
        self.pump_depth_posle_EditType.setText(f'{CreatePZ.dict_pump_h["posle"]}')

        self.paker_do_Label = QLabel('Спущенный пакер')
        self.paker_do_EditType = QLineEdit(self)
        self.paker_do_EditType.setText(f'{CreatePZ.paker_do["do"]}')

        self.paker_depth_do_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_do_EditType = QLineEdit(self)
        self.paker_depth_do_EditType.setText(f'{CreatePZ.H_F_paker_do["do"]}')

        self.paker_posle_Label = QLabel('пакер на спуск')
        self.paker_posle_EditType = QLineEdit(self)
        self.paker_posle_EditType.setText(f'{CreatePZ.paker_do["posle"]}')

        self.paker_depth_posle_Label = QLabel('Глубина спуска пакера')
        self.paker_depth_posle_EditType = QLineEdit(self)
        self.paker_depth_posle_EditType.setText(f'{CreatePZ.H_F_paker_do["posle"]}')

        print(f' насос спуск {CreatePZ.dict_pump["posle"]}')

        grid = QGridLayout(self)
        grid.addWidget(self.columnLabel, 0, 0)
        grid.addWidget(self.columnType, 1, 0)
        grid.addWidget(self.column_wall_thicknessLabel, 0, 1)
        grid.addWidget(self.column_wall_thicknessEditType2, 1, 1)
        grid.addWidget(self.shoe_columnLabel, 0, 2)
        grid.addWidget(self.shoe_columnEditType2, 1, 2)
        grid.addWidget(self.column_add_trueLabel, 0, 3)
        grid.addWidget(self.column_add_true_comboBox, 1, 3)
        grid.addWidget(self.column_addLabel, 0, 4)
        grid.addWidget(self.column_addEditType, 1, 4)
        grid.addWidget(self.column_add_wall_thicknessLabel, 0, 5)
        grid.addWidget(self.column_add_wall_thicknessEditType2, 1, 5)
        grid.addWidget(self.shoe_column_addLabel, 0, 6)
        grid.addWidget(self.shoe_column_add_EditType2, 1, 6)
        grid.addWidget(self.head_column_addLabel, 0, 7)
        grid.addWidget(self.head_column_add_EditType2, 1, 7)

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


class DataWindow(MyWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

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

        dict_pump_do = str(self.tabWidget.currentWidget().pump_do_EditType.text())
        dict_pump_h_do = self.tabWidget.currentWidget().pump_depth_do_EditType.text()

        dict_pump_do = str(self.tabWidget.currentWidget().pump_posle_EditType.text())
        dict_pump_h_posle = self.tabWidget.currentWidget().pump_depth_posle_EditType.text()
        paker_do = str(self.tabWidget.currentWidget().paker_do_EditType.text())
        H_F_paker_do = self.tabWidget.currentWidget().paker_depth_do_EditType.text()
        paker_posle = self.tabWidget.currentWidget().paker_do_EditType.text()
        H_F_paker_posle = self.tabWidget.currentWidget().paker_depth_do_EditType.text()

        if self.ifNum(columnType) == False \
                or self.ifNum(column_wall_thickness) == False \
                or self.ifNum(shoe_column) == False \
                or self.ifNum(column_additional_diametr) == False \
                or self.ifNum(column_additional_wall_thickness) == False \
                or self.ifNum(shoe_column_additional) == False \
                or self.ifNum(head_column_additional) == False \
                or self.ifNum(bottomhole_artificial) == False \
                or self.ifNum(bottomhole_drill) == False \
                or self.ifNum(current_bottom) == False \
                or self.ifNum(max_angle) == False \
                or self.ifNum(max_admissible_pressure) == False \
                or self.ifNum(max_expected_pressure) == False \
                or self.ifNum(dict_pump_h_do) == False \
                or self.ifNum(dict_pump_h_posle) == False \
                or self.ifNum(H_F_paker_do) == False \
                or self.ifNum(H_F_paker_posle) == False:
            msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return
        else:
            CreatePZ.column_diametr = float(columnType)
            CreatePZ.column_wall_thickness = float(column_wall_thickness)
            CreatePZ.shoe_column = float(shoe)}')
        print(CreatePZ.column_additional, CreatePZ.column_additional_diametr, CreatePZ.column_additional_wall_thickness,
              CreatePZ.shoe_column_additional, CreatePZ.head_column_additional,
              CreatePZ.bottomhole_drill)  # bWidget.currentWidget().bottomhole_drill_EditType.text())
        print(CreatePZ.bottomhole_artificial, CreatePZ.current_bottom, CreatePZ.max_angle,
              CreatePZ.max_expected_pressure,
              CreatePZ.max_admissible_pressure)  # = float(self.tabWidget.currentWidget().max_admissible_pressure_EditType.text())
        print(CreatePZ.dict_pump["do"], CreatePZ.dict_pump_h["do"], CreatePZ.dict_pump["posle"],
              CreatePZ.dict_pump_h["posle"])
        print(CreatePZ.paker_do["do"], CreatePZ.H_F_paker_do["do"], CreatePZ.paker_do["posle"],
              CreatePZ.H_F_paker_do["posle"])

        self.close()

    def ifNum(self, string):
        if re.search(r'\d+(,\d+){0,2}', string):
            return True
        else:
            return False


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = DataWindow()
    # window.show()
    sys.exit(app.exec_())
