from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, QMainWindow, QPushButton, \
    QMessageBox

import well_data
from work_py.alone_oreration import  need_h2s
from .rationingKRS import well_volume_norm


class TabPage_SO_swab(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.validator_int = QIntValidator(0, 600)
        self.validator_float = QDoubleValidator(0.87, 1.65, 2)

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

        self.plast_new_label = QLabel('индекс нового пласта', self)
        self.plast_new_combo = QComboBox(self)
        self.plast_new_combo.addItems(well_data.plast_project)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator_int)

        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.need_change_zgs_label, 9, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

        self.grid.addWidget(self.plast_new_label, 9, 3)
        self.grid.addWidget(self.plast_new_combo, 10, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.grid.addWidget(self.pressuar_new_label, 9, 5)
        self.grid.addWidget(self.pressuar_new_edit, 10, 5)
    def update_change_fluid(self, index):
        if index == 'Да':
            if len(well_data.plast_project) != 0:
                plast = well_data.plast_project[0]
                try:
                    fluid_new = list(well_data.dict_perforation_project[plast]['рабочая жидкость'])[0]
                    self.fluid_new_edit.setText(fluid_new)
                except:
                    pass


            cat_h2s_list_plan = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                               well_data.plast_project if well_data.dict_category.get(plast) and
                                               well_data.dict_category[plast]['отключение'] == 'планируемый']))

            if len(cat_h2s_list_plan) != 0:
                self.pressuar_new_edit.setText(f'{well_data.dict_category[plast]["по давлению"].data_pressuar}')

            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressuar_new_label, 9, 5)
            self.grid.addWidget(self.pressuar_new_edit, 10, 5)
        else:
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_swab(self), 'Смена объема')


class Change_fluid_Window(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind

        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from main import MyWindow
        plast_new_combo = str(self.tabWidget.currentWidget().plast_new_combo.currentText())
        fluid_new_edit = round(float(float(self.tabWidget.currentWidget().fluid_new_edit.text().replace(',', '.'))), 2)
        pressuar_new_edit = float(self.tabWidget.currentWidget().pressuar_new_edit.text())

        if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == ''):
            mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
            return
        if 0.87 <= fluid_new_edit < 1.65 is False:
            mes = QMessageBox.critical(self, 'Ошибка', 'Жидкость не может быть данным удельным весом')
            return
        if pressuar_new_edit < 10 is False:
            mes = QMessageBox.critical(self, 'Ошибка', 'Ожидаемое давление слишком низкое')
            return
        work_list = self.fluid_change(plast_new_combo, fluid_new_edit, pressuar_new_edit)
        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def fluid_change(self, plast_new, fluid_new, pressuar_new):
        from work_py.alone_oreration import well_volume

        well_data.fluid_work, well_data.fluid_work_short, plast, expected_pressure = need_h2s(fluid_new,
                                                                                              plast_new, pressuar_new)

        fluid_change_list = [
            [f'Cмена объема {well_data.fluid}г/см3- {round(well_volume(self, well_data.current_bottom), 1)}м3' ,
              None,
              f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {well_data.fluid_work} '
              f'(по расчету по вскрываемому пласта Рожид- {expected_pressure}атм) в объеме не '
              f'менее {round(well_volume(self, well_data.current_bottom), 1)}м3  в присутствии '
              f'представителя заказчика, Составить акт. '
              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
              f'2 часа до начала работ)',
              None, None, None, None, None, None, None,
              'мастер КРС', well_volume_norm(well_volume(self, well_data.current_bottom))]]

        return fluid_change_list