from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, QMainWindow, QPushButton

import well_data
from work_py.alone_oreration import check_h2s, need_h2s
from .rationingKRS import well_volume_norm


class TabPage_SO_swab(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

        self.plast_new_label = QLabel('индекс нового пласта', self)
        self.plast_new_combo = QComboBox(self)
        self.plast_new_combo.addItems(well_data.plast_project)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)



        self.grid = QGridLayout(self)

        self.grid.addWidget(self.need_change_zgs_label, 9, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

        self.grid.addWidget(self.plast_new_label, 9, 3)
        self.grid.addWidget(self.plast_new_combo, 10, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.grid.addWidget(self.pressuar_new_label, 9, 5)
        self.grid.addWidget(self.pressuar_new_edit, 10, 5)

    def update_need_fluid(self, index):
        if index == 'Да':
            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressuar_new_label, 9, 5)
            self.grid.addWidget(self.pressuar_new_edit, 10, 5)
            fluid_new, plast, expected_pressure = check_h2s(self)


            self.plast_new_combo.setCurrentIndex(well_data.plast_project.index(plast))
            self.fluid_new_edit.setText(str(fluid_new))
            self.pressuar_new_edit.setText(str(expected_pressure))
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
        plast_new = str(self.tabWidget.currentWidget().plast_new_combo.currentText())
        fluid_new = round(float(float(self.tabWidget.currentWidget().fluid_new_edit.text().replace(',', '.'))), 2)
        pressuar_new = float(self.tabWidget.currentWidget().pressuar_new_edit.text())

        work_list = self.fluid_change(plast_new, fluid_new, pressuar_new)
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