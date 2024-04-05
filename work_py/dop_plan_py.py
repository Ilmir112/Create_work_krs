from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton
from datetime import datetime

import well_data
from krs import TabPageGno, GnoWindow
from work_py.alone_oreration import lifting_unit, weigth_pipe, volume_pod_NKT, pvo_gno, volume_jamming_well
from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import liftingNKT_norm


class TabPageDp(QWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.work_plan = work_plan

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        self.fluid_edit.setText(f'{TabPageGno.calc_fluid(self.work_plan, well_data.current_bottom)}')

        self.work_label = QLabel("Ранее проведенные работы:", self)
        self.work_edit = QLineEdit(self)

        grid = QGridLayout(self)
        grid.addWidget(self.current_bottom_label, 4, 4)
        grid.addWidget(self.current_bottom_edit, 5, 4)
        grid.addWidget(self.fluid_label, 4, 5)
        grid.addWidget(self.fluid_edit, 5, 5)
        grid.addWidget(self.work_label, 4, 6)
        grid.addWidget(self.work_edit, 5, 6)





class TabWidget(QTabWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.addTab(TabPageDp(work_plan), 'Дополнительный план работ')


class DopPlanWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan, parent=None):

        super(DopPlanWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.work_plan = work_plan
        self.tabWidget = TabWidget(self.work_plan)

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from main import MyWindow

        current_bottom = round(float(self.tabWidget.currentWidget().current_bottom_edit.text()), 1)
        fluid = round(float(self.tabWidget.currentWidget().fluid_edit.text().replace(',', '.')), 2)
        work_earlier = self.tabWidget.currentWidget().work_edit.text()
        well_data.current_bottom = current_bottom

        if current_bottom != '' or fluid != '' or work_earlier != '':
            mes = QMessageBox.critical(self, 'Забой', 'не все значения введены')
            return
        if current_bottom >well_data.bottomhole_drill:
            mes = QMessageBox.critical(self, 'Забой', 'Текущий забой больше пробуренного забоя')
            return
        if 0.87 <= fluid <= 1.64 is False:
            mes = QMessageBox.critical(self, 'рабочая жидкость',
                                       'уд. вес рабочей жидкости не может быть меньше 0,87 и больше 1,64')
            return
        well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(self, fluid)
        work_list = self.work_list(work_earlier)
        MyWindow.populate_row(self, self.ins_ind+2, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def work_list(self, work_earlier):
        krs_begin = [[None, None,
             f' Ранее проведенные работ: \n {work_earlier}',
             None, None, None, None, None, None, None,
             'Мастер КРС', None]]
        return krs_begin