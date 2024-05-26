from PyQt5.QtWidgets import QInputDialog, QMessageBox

import well_data
from work_py.alone_oreration import volume_vn_ek, volume_vn_nkt

from .rationingKRS import descentNKT_norm
from main import MyWindow
from .rir import RirWindow

from PyQt5.QtGui import QDoubleValidator,QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import well_data
from main import MyWindow
from .rir import RirWindow

from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPage_SO_clay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.roof_clay_label = QLabel("кровля ГР", self)
        self.roof_clay_edit = QLineEdit(self)
        self.roof_clay_edit.setValidator( self.validator)

        self.roof_clay_edit.setText(f'{well_data.perforation_sole +70}')
        self.roof_clay_edit.setClearButtonEnabled(True)

        self.sole_clay_LabelType = QLabel("Подошва ГР", self)
        self.sole_clay_edit = QLineEdit(self)
        self.sole_clay_edit.setText(f'{well_data.current_bottom}')
        self.sole_clay_edit.setValidator(self.validator)       

        self.rir_question_Label = QLabel("Нужно ли УЦМ производить на данной компоновке", self)
        self.rir_question_QCombo = QComboBox(self)
        self.rir_question_QCombo.addItems(['Нет', 'Да'])

        self.roof_rir_label = QLabel("Плановая кровля РИР", self)
        self.roof_rir_edit = QLineEdit(self)
        self.roof_rir_edit.setText(f'{well_data.current_bottom - 50}')
        self.roof_rir_edit.setClearButtonEnabled(True)

        self.sole_rir_LabelType = QLabel("Подошва РИР", self)
        self.sole_rir_edit = QLineEdit(self)
        self.sole_rir_edit.setText(f'{well_data.current_bottom}')
        self.sole_rir_edit.setClearButtonEnabled(True)



        self.grid = QGridLayout(self)

        self.grid.addWidget(self.roof_clay_label, 4, 4)
        self.grid.addWidget(self.roof_clay_edit, 5, 4)
        self.grid.addWidget(self.sole_clay_LabelType, 4, 5)
        self.grid.addWidget(self.sole_clay_edit, 5, 5)

        self.grid.addWidget(self.rir_question_Label, 6, 3)
        self.grid.addWidget(self.rir_question_QCombo, 7, 3)

        self.grid.addWidget(self.roof_rir_label, 6, 4)
        self.grid.addWidget(self.roof_rir_edit, 7, 4)
        self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
        self.grid.addWidget(self.sole_rir_edit, 7, 5)

        self.roof_clay_edit.textChanged.connect(self.update_roof)
        self.rir_question_QCombo.currentTextChanged.connect(self.update_rir)
        self.rir_question_QCombo.setCurrentIndex(1)
        self.rir_question_QCombo.setCurrentIndex(0)

    def update_roof(self):
        roof_clay_edit = self.roof_clay_edit.text()

        if roof_clay_edit != '':
            self.sole_rir_edit.setText(f'{float(roof_clay_edit)}')
            self.roof_rir_edit.setText(f'{float(roof_clay_edit)-50}')

    def update_rir(self, index):

        if index == "Да":
            self.grid.addWidget(self.roof_rir_label, 6, 4)
            self.grid.addWidget(self.roof_rir_edit, 7, 4)
            self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
            self.grid.addWidget(self.sole_rir_edit, 7, 5)
        else:
            self.roof_rir_label.setParent(None)
            self.roof_rir_edit.setParent(None)
            self.sole_rir_LabelType.setParent(None)
            self.sole_rir_edit.setParent(None)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_clay(self), 'отсыпка')


class ClayWindow(QMainWindow):
    work_clay_window = None
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        roof_clay_edit = int(float(self.tabWidget.currentWidget().roof_clay_edit.text()))
        sole_clay_edit = int(float(self.tabWidget.currentWidget().sole_clay_edit.text()))
        rir_question_QCombo = str(self.tabWidget.currentWidget().rir_question_QCombo.currentText())
        roof_rir_edit = int(float(self.tabWidget.currentWidget().roof_rir_edit.text()))
        sole_rir_edit = int(float(self.tabWidget.currentWidget().sole_rir_edit.text()))
        if roof_clay_edit > sole_clay_edit:
            mes = QMessageBox.warning(self, 'Ошибка', 'Не корректные интервалы ')
            return

        work_list = self.claySolutionDef(roof_clay_edit, sole_clay_edit, rir_question_QCombo,
                                         roof_rir_edit, sole_rir_edit)


        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def claySolutionDef(self, rirRoof, rirSole, rir_question_QCombo,
                                         roof_rir_edit, sole_rir_edit):
       
        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])

        if well_data.column_additional is True and well_data.column_additional_diametr._value <110 and\
                rirSole > well_data.head_column_additional._value:
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: well_data.head_column_additional._value-rirSole}
        else:
            dict_nkt = {73: rirSole}
    
        volume_cement = round(volume_vn_ek(rirRoof) * (rirSole - rirRoof)/1000, 1)
        dict_nkt = {73: rirRoof}
        pero_list = [
            [f'СПО {RirWindow.pero_select(self, rirSole)}  на тНКТ{nkt_diam}м до {rirSole}м', None,
             f'Спустить {RirWindow.pero_select(self, rirSole)}  на тНКТ{nkt_diam}м до глубины {rirSole}м с '
             f'замером, шаблонированием '
             f'шаблоном {well_data.nkt_template}мм. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС',descentNKT_norm(rirSole, 1)],
            [f'закачку глинистого раствора в интервале {rirSole}-{rirRoof}м в объеме {volume_cement}м3 '
             f'({round(volume_cement*0.45,2)}т'
             f' сухого порошка)', None,
             f'Произвести закачку глинистого раствора с добавлением ингибитора коррозии {round(volume_cement*11,1)}гр с '
             f'удельной дозировкой 11гр/м3 '
             f'удельным весом не менее 1,24г/см3 в интервале {rirSole}-{rirRoof}м.\n'
             f'- Приготовить и закачать в глинистый раствор уд.весом не менее 1,24г/см3 в объеме {volume_cement}м3 '
             f'({round(volume_cement*0.45,2)}т'
             f' сухого порошка).\n'
             f'-Продавить тех жидкостью  в объеме {volume_vn_nkt(dict_nkt)}м3.',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5]]
        well_data.current_bottom = rirRoof

        if rir_question_QCombo == 'Нет':
            pero_list.append([None, None,
             f'Поднять перо на тНКТ{nkt_diam}м с глубины {rirSole}м с доливом скважины в объеме '
             f'{round(rirSole*1.3/1000, 1)}м3 тех. жидкостью '
             f'уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(rirRoof, 1)])
        else:
            pero_list.append([None, None,
                              f'Поднять перо на тНКТ{nkt_diam}м до глубины {rirRoof}м с доливом скважины в объеме'
                              f' {round((rirSole-rirRoof)*1.3/1000, 1)}м3 тех. жидкостью '
                              f'уд.весом {well_data.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(float(rirSole)-float(rirRoof), 1)])
            if (well_data.plast_work) != 0 or rirSole > well_data.perforation_sole:
                rir_work_list = RirWindow.rirWithPero(self, 'Не нужно', '', roof_rir_edit, sole_rir_edit)
                pero_list.extend(rir_work_list[-9:])
            else:
                rir_work_list = RirWindow.rirWithPero(self,'Не нужно', '', roof_rir_edit, sole_rir_edit)
                pero_list.extend(rir_work_list[-10:])
        return pero_list