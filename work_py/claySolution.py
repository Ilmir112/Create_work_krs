from PyQt5.QtWidgets import QInputDialog, QMessageBox

import well_data
from work_py.alone_oreration import volume_vn_ek, volume_vn_nkt, well_volume



from PyQt5.QtGui import QDoubleValidator,QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import well_data
from main import MyMainWindow
from .rir import RirWindow

from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPage_SO_clay(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.validator = QIntValidator(0, 80000)

        self.purpose_of_clay_label = QLabel("цель закачки глинистого раствора", self)
        self.purpose_of_clay_combo = QComboBox(self)
        self.purpose_of_clay_combo.addItems(['сбитие приемистости', 'в колонне'])

        self.current_bottom_label = QLabel("забой", self)
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setValidator(self.validator)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.volume_clay_label = QLabel("Объем глинистого раствора", self)
        self.volume_clay_edit = QLineEdit(self)
        self.volume_clay_edit.setValidator(self.validator)
        self.volume_clay_edit.setText(f'{5}')

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

        self.cement_volume_label = QLabel('Объем цемента')
        self.cement_volume_line = QLineEdit(self)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.purpose_of_clay_label, 2, 4)
        self.grid.addWidget(self.purpose_of_clay_combo, 3, 4)

        self.roof_clay_edit.textChanged.connect(self.update_roof)
        self.rir_question_QCombo.currentTextChanged.connect(self.update_rir)
        self.purpose_of_clay_combo.currentTextChanged.connect(self.update_purpose_of_clay)
        self.purpose_of_clay_combo.setCurrentIndex(1)
    def update_purpose_of_clay(self, index):
        if index == 'в колонне':
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


            self.current_bottom_label.setParent(None)
            self.current_bottom_edit.setParent(None)

            self.volume_clay_label.setParent(None)
            self.volume_clay_edit.setParent(None)

        else:
            self.roof_clay_label.setParent(None)
            self.roof_clay_edit.setParent(None)
            self.sole_clay_LabelType.setParent(None)
            self.sole_clay_edit.setParent(None)

            self.rir_question_Label.setParent(None)
            self.rir_question_QCombo.setParent(None)

            self.roof_rir_label.setParent(None)
            self.roof_rir_edit.setParent(None)
            self.sole_rir_LabelType.setParent(None)
            self.sole_rir_edit.setParent(None)
            self.grid.addWidget(self.current_bottom_label, 6, 4)
            self.grid.addWidget(self.current_bottom_edit, 7, 4)
            self.grid.addWidget(self.volume_clay_label, 6, 5)
            self.grid.addWidget(self.volume_clay_edit, 7, 5)

    def update_roof(self):
        roof_clay_edit = self.roof_clay_edit.text()

        if roof_clay_edit != '':
            self.sole_rir_edit.setText(f'{float(roof_clay_edit)}')
            self.roof_rir_edit.setText(f'{float(roof_clay_edit)-50}')


    def update_rir(self, index):

        if index == "Нет":
            self.roof_rir_label.setParent(None)
            self.roof_rir_edit.setParent(None)
            self.sole_rir_LabelType.setParent(None)
            self.sole_rir_edit.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)
        else:
            self.grid.addWidget(self.roof_rir_label, 6, 4)
            self.grid.addWidget(self.roof_rir_edit, 7, 4)
            self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
            self.grid.addWidget(self.sole_rir_edit, 7, 5)
            self.grid.addWidget(self.cement_volume_label, 6, 6)
            self.grid.addWidget(self.cement_volume_line, 7, 6)
            self.roof_rir_edit.editingFinished.connect(self.update_volume_cement)
            self.sole_rir_edit.editingFinished.connect(self.update_volume_cement)
    def update_volume_cement(self):
        if self.roof_rir_edit.text() != '' and self.sole_rir_edit.text() != '':
            self.cement_volume_line.setText(
                f'{round(volume_vn_ek(float(self.roof_rir_edit.text())) * (float(self.sole_rir_edit.text()) - float(self.roof_rir_edit.text())) / 1000, 1)}')


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_clay(self), 'отсыпка')


class ClayWindow(MyMainWindow):
    work_clay_window = None
    def __init__(self, ins_ind, table_widget, parent=None):
        super().__init__()
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
        purpose_of_clay_combo = self.tabWidget.currentWidget().purpose_of_clay_combo.currentText()
        if purpose_of_clay_combo == 'в колонне':
            roof_clay_edit = int(float(self.tabWidget.currentWidget().roof_clay_edit.text()))
            sole_clay_edit = int(float(self.tabWidget.currentWidget().sole_clay_edit.text()))
            rir_question_QCombo = str(self.tabWidget.currentWidget().rir_question_QCombo.currentText())
            roof_rir_edit = int(float(self.tabWidget.currentWidget().roof_rir_edit.text()))
            sole_rir_edit = int(float(self.tabWidget.currentWidget().sole_rir_edit.text()))
            volume_cement = self.tabWidget.currentWidget().cement_volume_line.text().replace(',', '.')
            if volume_cement != '':
                volume_cement = round(float(volume_cement), 1)
            elif volume_cement == '' and rir_question_QCombo == "Да":
                mes = QMessageBox.question(self, 'Вопрос', f'Не указан объем цемента')
                return
            if roof_clay_edit > sole_clay_edit:
                mes = QMessageBox.warning(self, 'Ошибка', 'Не корректные интервалы ')
                return

            work_list = self.claySolutionDef(roof_clay_edit, sole_clay_edit, rir_question_QCombo,
                                             roof_rir_edit, sole_rir_edit, volume_cement)
        else:
            current_bottom_edit = int(float(self.tabWidget.currentWidget().current_bottom_edit.text()))
            volume_clay_edit = int(float(self.tabWidget.currentWidget().volume_clay_edit.text()))
            work_list = self.clay_solution_q(current_bottom_edit, volume_clay_edit)

        self.populate_row(self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def clay_solution_q(self, current_bottom_edit, volume_clay_edit):
        if well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                current_bottom_edit > well_data.head_column_additional._value:
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: current_bottom_edit - well_data.head_column_additional._value}
        else:
            dict_nkt = {73: current_bottom_edit}
        glin_list = [
            [f'СПО пера до глубины {current_bottom_edit}м. Опрессовать НКТ на 200атм', None,
             f'Спустить {RirWindow.pero_select(self, current_bottom_edit)}  на тНКТ{well_data.nkt_diam}м до '
             f'глубины {current_bottom_edit}м с замером, шаблонированием '
             f'шаблоном {well_data.nkt_template}мм. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom_edit, 1)],
            [None, None,
             f'По результатам определения приёмистости выполнить следующие работы: \n'
             f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке гдинистого раствора '
             f'(по согласованию с ГС и ПТО {well_data.contractor} и заказчика). \n'
             f'В случае приёмистости менее 480 м3/сут при Р=100атм и более 120м3/сут при Р=100атм приступить '
             f'к выполнению РИР',
             None, None, None, None, None, None, None,
             'мастер КРС, заказчик', None],
            [None, None,
             f'Объём глинистого р-ра скорректировать на устье на основании тех.возможности. \n'
             f'Приготовить глинистый раствор в объёме 5м3 (расчет на 1 м3 - сухой глинопорошок массой 0,3т + '
             f'вода у=1,00г/см3 в объёме 0,9м3) плотностью у=1,24г/см3',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Закачка глины для сбития приемистости', None,
             f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме {volume_clay_edit}м3 + тех. воду '
             f'в объёме {round(volume_vn_nkt(dict_nkt) - volume_clay_edit, 1)}м3. Закрыть затруб. '
             f'Продавить в НКТ тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более '
             f'{well_data.max_admissible_pressure._value}атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [f'Коагуляция 4 часа', None,
             f'Коагуляция 4 часа (на основании конечного давления при продавке. '
             f'В случае конечного давления менее 50атм, согласовать объем глинистого раствора с '
             f'Заказчиком и продолжить приготовление следующего объема глинистого объема).',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Определить приёмистость по НКТ при Р=100атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.35],
            [None, None,
             f'В случае необходимости выполнить работы по закачке глнистого раствора, с корректировкой '
             f'по объёму раствора.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью '
             f'в объеме не менее {well_volume(self, volume_vn_nkt(dict_nkt))}м3 с расходом жидкости не менее 8 л/с.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(24)],
            [None, None,
             f'Опрессовать НКТ на 200атм. Вымыть шар. Поднять перо на тНКТ{well_data.nkt_diam}м с глубины {current_bottom_edit}м с доливом скважины в объеме '
             f'{round(current_bottom_edit * 1.12 / 1000, 1)}м3 тех. жидкостью '
             f'уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(current_bottom_edit, 1)]
        ]
        a = volume_vn_nkt(dict_nkt)
        if volume_vn_nkt(dict_nkt) <= 5:
            glin_list[3] = [
                None, None,
                    f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в '
                    f'объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                    f'Продавить в НКТ остаток глинистого раствора в объеме '
                    f'{round(volume_clay_edit - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме '
                    f'{volume_vn_nkt(dict_nkt)}м3 при давлении не более {well_data.max_admissible_pressure._value}атм.',
                    None, None, None, None, None, None, None,
                    'мастер КРС', 0.5]
        return glin_list
    def claySolutionDef(self, rirRoof, rirSole, rir_question_QCombo,
                                         roof_rir_edit, sole_rir_edit, volume_cement):
       
        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])

        if well_data.column_additional is True and well_data.column_additional_diametr._value <110 and\
                rirSole > well_data.head_column_additional._value:
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: well_data.head_column_additional._value-rirSole}
        else:
            dict_nkt = {73: rirSole}
    

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
                rir_work_list = RirWindow.rirWithPero_gl(self, 'Не нужно', '', roof_rir_edit, sole_rir_edit, volume_cement)
                pero_list.extend(rir_work_list[-9:])
            else:
                rir_work_list = RirWindow.rirWithPero_gl(self, 'Не нужно', '', roof_rir_edit, sole_rir_edit, volume_cement)
                pero_list.extend(rir_work_list[-10:])
        return pero_list