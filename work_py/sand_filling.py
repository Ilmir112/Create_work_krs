from PyQt5.QtGui import QDoubleValidator,QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import well_data
from main import MyWindow
from .alone_oreration import volume_vn_ek
from .rir import RirWindow

from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from .rir import TabPage_SO_rir


class TabPage_SO_sand(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.roof_sand_label = QLabel("кровля ПМ", self)
        self.roof_sand_edit = QLineEdit(self)
        self.roof_sand_edit.setValidator(self.validator)

        self.roof_sand_edit.setText(f'{well_data.perforation_roof -20}')
        self.roof_sand_edit.setClearButtonEnabled(True)

        self.sole_sand_LabelType = QLabel("Подошва ПМ", self)
        self.sole_sand_edit = QLineEdit(self)
        self.sole_sand_edit.setText(f'{well_data.current_bottom}')
        self.sole_sand_edit.setValidator(self.validator)


        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        self.rir_question_Label = QLabel("Нужно ли производить УЦМ на данной компоновке", self)
        self.rir_question_QCombo = QComboBox(self)
        self.rir_question_QCombo.addItems(['Нет', 'Да'])

        self.roof_rir_label = QLabel("Плановая кровля РИР", self)
        self.roof_rir_edit = QLineEdit(self)

        self.sole_rir_LabelType = QLabel("Подошва РИР", self)
        self.sole_rir_edit = QLineEdit(self)

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Да', 'Нет'])


        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator)

        if len(well_data.plast_project) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(well_data.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)
        self.cement_volume_label = QLabel('Объем цемента')
        self.cement_volume_line = QLineEdit(self)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.privyazka_question_Label, 4, 3)
        self.grid.addWidget(self.privyazka_question_QCombo, 5, 3)

        self.grid.addWidget(self.roof_sand_label, 4, 4)
        self.grid.addWidget(self.roof_sand_edit, 5, 4)
        self.grid.addWidget(self.sole_sand_LabelType, 4, 5)
        self.grid.addWidget(self.sole_sand_edit, 5, 5)

        self.grid.addWidget(self.rir_question_Label, 6, 3)
        self.grid.addWidget(self.rir_question_QCombo, 7, 3)

        self.grid.addWidget(self.roof_rir_label, 6, 4)
        self.grid.addWidget(self.roof_rir_edit, 7, 4)
        self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
        self.grid.addWidget(self.sole_rir_edit, 7, 5)
        self.grid.addWidget(self.cement_volume_label, 6, 6)
        self.grid.addWidget(self.cement_volume_line, 7, 6)

        self.grid.addWidget(self.need_change_zgs_label, 9, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 2)

        self.grid.addWidget(self.plast_new_label, 9, 3)
        self.grid.addWidget(self.plast_new_combo, 10, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.grid.addWidget(self.pressuar_new_label, 9, 5)
        self.grid.addWidget(self.pressuar_new_edit, 10, 5)

        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)
        self.need_change_zgs_combo.setCurrentIndex(1)

        self.roof_rir_edit.textChanged.connect(self.update_volume_cement)
        self.sole_rir_edit.textChanged.connect(self.update_volume_cement)
        self.roof_sand_edit.textChanged.connect(self.update_roof)
        self.rir_question_QCombo.currentTextChanged.connect(self.update_rir)
        self.rir_question_QCombo.setCurrentIndex(1)
        self.rir_question_QCombo.setCurrentIndex(0)

        if len(well_data.plast_work) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

    def update_volume_cement(self):
        if self.roof_rir_edit.text() != '' and self.sole_rir_edit.text() != '':
            self.cement_volume_line.setText(
                f'{round(volume_vn_ek(float(self.roof_rir_edit.text())) * (float(self.sole_rir_edit.text())- float(self.roof_rir_edit.text())) / 1000, 1)}')
    def update_roof(self):
        roof_sand_edit = self.roof_sand_edit.text()
        if roof_sand_edit != '':
            roof_sand_edit = int(float(self.roof_sand_edit.text()))
        rir_question_QCombo = self.rir_question_QCombo.currentText()
        if roof_sand_edit:
            if int(roof_sand_edit) + 10 > well_data.perforation_roof:
                self.privyazka_question_QCombo.setCurrentIndex(1)
            else:
                self.privyazka_question_QCombo.setCurrentIndex(0)
            if rir_question_QCombo == 'Да':
                self.sole_rir_edit.setText(f'{roof_sand_edit}')
                self.roof_rir_edit.setText(f'{roof_sand_edit-50}')

    def update_rir(self, index):
        roof_sand_edit = self.roof_sand_edit.text()
        if roof_sand_edit != '':
            roof_sand_edit = int(float(self.roof_sand_edit.text()))
        if index == "Да":
            self.grid.addWidget(self.roof_rir_label, 6, 4)
            self.grid.addWidget(self.roof_rir_edit, 7, 4)
            self.grid.addWidget(self.sole_rir_LabelType, 6, 5)
            self.grid.addWidget(self.sole_rir_edit, 7, 5)
            self.grid.addWidget(self.cement_volume_label, 6, 6)
            self.grid.addWidget(self.cement_volume_line, 7, 6)
            self.sole_rir_edit.setText(f'{roof_sand_edit}')
            self.roof_rir_edit.setText(f'{roof_sand_edit - 50}')
        else:
            self.roof_rir_label.setParent(None)
            self.roof_rir_edit.setParent(None)
            self.sole_rir_LabelType.setParent(None)
            self.sole_rir_edit.setParent(None)
            self.cement_volume_label.setParent(None)
            self.cement_volume_line.setParent(None)

    def update_change_fluid(self, index):
        if index == 'Да':


            cat_h2s_list_plan = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                               well_data.plast_project if well_data.dict_category.get(plast) and
                                               well_data.dict_category[plast]['отключение'] == 'планируемый']))

            if len(cat_h2s_list_plan) != 0:
                plast = well_data.plast_project[0]
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
        self.addTab(TabPage_SO_sand(self), 'отсыпка')

class SandWindow(QMainWindow):
    work_sand_window = None
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

        privyazka_question_QCombo = str(self.tabWidget.currentWidget().privyazka_question_QCombo.currentText())
        roof_sand_edit = int(float(self.tabWidget.currentWidget().roof_sand_edit.text()))
        sole_sand_edit = int(float(self.tabWidget.currentWidget().sole_sand_edit.text()))
        rir_question_QCombo = str(self.tabWidget.currentWidget().rir_question_QCombo.currentText())
        volume_cement = self.tabWidget.currentWidget().cement_volume_line.text().replace(',', '.')
        need_change_zgs_combo = self.tabWidget.currentWidget().need_change_zgs_combo.currentText()
        if len(well_data.plast_project) != 0:
            plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
        else:
            plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()
        fluid_new_edit = self.tabWidget.currentWidget().fluid_new_edit.text()
        pressuar_new_edit = self.tabWidget.currentWidget().pressuar_new_edit.text()
        if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == '') and \
                need_change_zgs_combo == 'Да':
            mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
            return
        if volume_cement != '':
            volume_cement = round(float(volume_cement),1)
        elif volume_cement == '' and rir_question_QCombo == "Да":
            mes = QMessageBox.question(self, 'Вопрос',
                                                       f'Не указан объем цемента')
            return

        work_list = self.sandFilling(roof_sand_edit, sole_sand_edit, privyazka_question_QCombo)
        if rir_question_QCombo == "Да":
            work_list = work_list[:-1]
            roof_rir_edit = int(float(self.tabWidget.currentWidget().roof_rir_edit.text()))
            sole_rir_edit = int(float(self.tabWidget.currentWidget().sole_rir_edit.text()))
            rir_list = RirWindow.rirWithPero_gl(self, "Не нужно", '', roof_rir_edit, sole_rir_edit, volume_cement,
                                                need_change_zgs_combo, plast_new_combo, fluid_new_edit, pressuar_new_edit)
            work_list.extend(rir_list[1:])

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()
    def sand_select(self):

        if well_data.column_additional is False or (well_data.column_additional is True and \
                                                    well_data.current_bottom <= well_data.head_column_additional._value):
            sand_select = f'перо + НКТ{well_data.nkt_diam}мм 20м + реперный патрубок'

        elif well_data.column_additional is True and \
                well_data.column_additional_diametr._value < 110 and \
                well_data.current_bottom >= well_data.head_column_additional._value:
            sand_select = f'обточную муфту + НКТ{60}мм 20м + реперный патрубок + НКТ60мм ' \
                          f'{round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м '
        elif well_data.column_additional is True and \
                well_data.column_additional_diametr._value > 110 and \
                well_data.current_bottom >= well_data.head_column_additional._value:
            sand_select = f'обточную муфту + НКТ{well_data.nkt_diam}мм со снятыми фасками {20}м + реперный патрубок + ' \
                          f'НКТ{well_data.nkt_diam}мм со снятыми фасками ' \
                          f'{round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м'
        return sand_select

    def sandFilling(self, filling_depth, sole_sand_edit, privyazka_question_QCombo):

        from work_py.alone_oreration import well_volume, volume_vn_ek

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])

        sand_volume = round(volume_vn_ek(filling_depth) * (sole_sand_edit - filling_depth), 1)


        filling_list = [
            [f'Спустить  {self.sand_select()} на НКТ{nkt_diam}м до глубины {round(filling_depth-100,0)}м', None,
         f'Спустить  {self.sand_select()}  на НКТ{nkt_diam}м до глубины {round(filling_depth-100,0)}м с замером, '
         f'шаблонированием шаблоном {well_data.nkt_template}мм. (При СПО первых десяти НКТ на '
         f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'Мастер КР', descentNKT_norm(sole_sand_edit,1)],
            [f'отсыпка кварцевым песком в инт. {filling_depth} - {sole_sand_edit} в объеме {sand_volume}л',
             None, f'Произвести отсыпку кварцевым песком в инт. {filling_depth} - {sole_sand_edit} '
                 f'в объеме {sand_volume}л '
                 f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Ожидание оседания песка 4 часа.',
             None, f'Ожидание оседания песка 4 часа.',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста '
             f'(плановый забой -{filling_depth}м). '
             f'Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}". При необходимости '
             f'подготовить место для установки партии ГИС напротив мостков. Произвести  монтаж ГИС согласно схемы  №8 при '
             f'привязке утвержденной главным инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'Привязка ', None,
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'Определение кровли', None,
             f'В случае если кровля песчаного моста на гл.{filling_depth}м дальнейшие работы продолжить дальше по плану'
             f'В случае пеcчаного моста ниже гл.{filling_depth}м работы повторить с корректировкой обьема и '
             f'технологических глубин.'
             f' В случае песчаного моста выше гл.{filling_depth}м вымыть песок до гл.{filling_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', None]
        ]
        if OpressovkaEK.testing_pressure(self, filling_depth):
            filling_list.insert(-1,
                        [f'Опрессовать в инт{filling_depth}-0м на Р={well_data.max_admissible_pressure._value}атм',
                         None, f'Опрессовать эксплуатационную колонну в интервале {filling_depth}-0м на'
                               f'Р={well_data.max_admissible_pressure._value}атм'
                         f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
                         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа'
                                       f' до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67])
            filling_list.insert(-1,
                                [None, None,
                         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для '
                         f'определения интервала '
                         f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                         f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                         f'Определить приемистость НЭК.',
                         None, None, None, None, None, None, None,
                         'мастер КРС', None] )

        if privyazka_question_QCombo == "Да":
            pass
        else:
            filling_list.pop(5)
            filling_list.pop(4)


        filling_list.append([None, None,
                             f'Поднять {self.sand_select()} НКТ{nkt_diam}м с глубины {filling_depth}м с доливом '
                             f'скважины в объеме {round(filling_depth * 1.12 / 1000, 1)}м3 тех. жидкостью '
                             f'уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(filling_depth, 1)])
        well_data.current_bottom = filling_depth

        return filling_list

    def sandWashing(self):


        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])


        washingDepth, ok = QInputDialog.getDouble(None, 'вымыв песка',
                                                    'Введите глубину вымыва песчанного моста',
                                                    well_data.current_bottom, 0, 6000, 1)
        washingOut_list = [
            [f'СПО пера до {round(well_data.current_bottom,0)}м', None,
         f'Спустить  {SandWindow.sand_select(self)}  на НКТ{nkt_diam}м до глубины {round(well_data.current_bottom,0)}м с '
         f'замером,'
         f' шаблонированием шаблоном {well_data.nkt_template}мм. '
         f'(При СПО первых десяти НКТ на '
         f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'Мастер КР', descentNKT_norm(well_data.current_bottom, 1)],
            [f'вымыв песка до {washingDepth}м',
             None, f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной '
                   f'промывкой по круговой циркуляции '
                   f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{washingDepth}м. \n'
                   f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Поднять {SandWindow.sand_select(self)} НКТ{nkt_diam}м с глубины {washingDepth}м с доливом скважины в объеме '
             f'{round(washingDepth * 1.12 / 1000, 1)}м3 тех. '
             f'жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(washingDepth, 1.2)]]
        well_data.current_bottom = washingDepth

        return washingOut_list