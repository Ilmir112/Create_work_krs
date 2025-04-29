from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import data_list
from work_py.alone_oreration import volume_vn_ek
from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from work_py.rir import RirWindow

from work_py.opressovka import OpressovkaEK
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm


class TabPageSoSand(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.roof_sand_label = QLabel("кровля ПМ", self)
        self.roof_sand_edit = QLineEdit(self)
        self.roof_sand_edit.setValidator(self.validator)

        self.roof_sand_edit.setText(f'{self.data_well.perforation_roof - 20}')
        self.roof_sand_edit.setClearButtonEnabled(True)

        self.sole_sand_LabelType = QLabel("Подошва ПМ", self)
        self.sole_sand_edit = QLineEdit(self)
        self.sole_sand_edit.setText(f'{self.data_well.current_bottom}')
        self.sole_sand_edit.setValidator(self.validator)

        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        self.rir_question_Label = QLabel("Нужно ли производить УЦМ на данной компоновке", self)
        self.rir_question_qcombo = QComboBox(self)
        self.rir_question_qcombo.addItems(['Нет', 'Да'])

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

        self.pressure_new_label = QLabel('Ожидаемое давление', self)
        self.pressure_new_edit = QLineEdit(self)
        self.pressure_new_edit.setValidator(self.validator)

        if len(self.data_well.plast_project) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(self.data_well.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)
        self.cement_volume_label = QLabel('Объем цемента')
        self.cement_volume_line = QLineEdit(self)

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.privyazka_question_Label, 4, 3)
        self.grid.addWidget(self.privyazka_question_QCombo, 5, 3)

        self.grid.addWidget(self.roof_sand_label, 4, 4)
        self.grid.addWidget(self.roof_sand_edit, 5, 4)
        self.grid.addWidget(self.sole_sand_LabelType, 4, 5)
        self.grid.addWidget(self.sole_sand_edit, 5, 5)

        self.grid.addWidget(self.rir_question_Label, 6, 3)
        self.grid.addWidget(self.rir_question_qcombo, 7, 3)

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

        self.grid.addWidget(self.pressure_new_label, 9, 5)
        self.grid.addWidget(self.pressure_new_edit, 10, 5)

        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)
        self.need_change_zgs_combo.setCurrentIndex(1)

        self.roof_rir_edit.textChanged.connect(self.update_volume_cement)
        self.sole_rir_edit.textChanged.connect(self.update_volume_cement)
        self.roof_sand_edit.textChanged.connect(self.update_roof)
        self.rir_question_qcombo.currentTextChanged.connect(self.update_rir)
        self.rir_question_qcombo.setCurrentIndex(1)
        self.rir_question_qcombo.setCurrentIndex(0)

        if len(self.data_well.plast_work) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

    def update_volume_cement(self):
        if self.roof_rir_edit.text() != '' and self.sole_rir_edit.text() != '':
            self.cement_volume_line.setText(
                f'{round(volume_vn_ek(self, float(self.roof_rir_edit.text())) * (float(self.sole_rir_edit.text()) - float(self.roof_rir_edit.text())) / 1000, 1)}')

    def update_roof(self):
        roof_sand_edit = self.roof_sand_edit.text()
        if roof_sand_edit != '':
            roof_sand_edit = int(float(self.roof_sand_edit.text()))
        rir_question_qcombo = self.rir_question_qcombo.currentText()
        if roof_sand_edit:
            if int(roof_sand_edit) + 10 > self.data_well.perforation_roof:
                self.privyazka_question_QCombo.setCurrentIndex(1)
            else:
                self.privyazka_question_QCombo.setCurrentIndex(0)
            if rir_question_qcombo == 'Да':
                self.sole_rir_edit.setText(f'{roof_sand_edit}')
                self.roof_rir_edit.setText(f'{roof_sand_edit - 50}')

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
            category_h2s_list_plan = list(
                map(int, [self.data_well.dict_category[plast]['по сероводороду'].category for plast in
                          self.data_well.plast_project if self.data_well.dict_category.get(plast) and
                          self.data_well.dict_category[plast]['отключение'] == 'планируемый']))

            if len(category_h2s_list_plan) != 0:
                plast = self.data_well.plast_project[0]
                self.pressure_new_edit.setText(
                    f'{self.data_well.dict_category[plast]["по давлению"].data_pressure}')
            self.grid.addWidget(self.plast_new_label, 9, 3)
            self.grid.addWidget(self.plast_new_combo, 10, 3)

            self.grid.addWidget(self.fluid_new_label, 9, 4)
            self.grid.addWidget(self.fluid_new_edit, 10, 4)

            self.grid.addWidget(self.pressure_new_label, 9, 5)
            self.grid.addWidget(self.pressure_new_edit, 10, 5)
        else:
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressure_new_label.setParent(None)
            self.pressure_new_edit.setParent(None)


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoSand(parent), 'отсыпка')


class SandWindow(WindowUnion):
    work_sand_window = None

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        privyazka_question_QCombo = str(self.tab_widget.currentWidget().privyazka_question_QCombo.currentText())
        roof_sand_edit = int(float(self.tab_widget.currentWidget().roof_sand_edit.text()))
        sole_sand_edit = int(float(self.tab_widget.currentWidget().sole_sand_edit.text()))
        rir_question_qcombo = str(self.tab_widget.currentWidget().rir_question_qcombo.currentText())

        need_change_zgs_combo = self.tab_widget.currentWidget().need_change_zgs_combo.currentText()
        if len(self.data_well.plast_project) != 0:
            plast_new_combo = self.tab_widget.currentWidget().plast_new_combo.currentText()
        else:
            plast_new_combo = self.tab_widget.currentWidget().plast_new_combo.text()
        fluid_new_edit = self.tab_widget.currentWidget().fluid_new_edit.text()
        pressure_new_edit = self.tab_widget.currentWidget().pressure_new_edit.text()
        if (plast_new_combo == '' or fluid_new_edit == '' or pressure_new_edit == '') and \
                need_change_zgs_combo == 'Да':
            mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
            return
        volume_cement = self.tab_widget.currentWidget().cement_volume_line.text().replace(',', '.')
        if volume_cement != '':
            volume_cement = round(float(volume_cement), 1)
        elif volume_cement == '' and rir_question_qcombo == "Да":
            QMessageBox.question(self, 'Вопрос', f'Не указан объем цемента')
            return

        work_list = self.sandFilling(roof_sand_edit, sole_sand_edit, privyazka_question_QCombo)
        if rir_question_qcombo == "Да":
            work_list = work_list[:-1]
            roof_rir_edit = int(float(self.tab_widget.currentWidget().roof_rir_edit.text()))
            sole_rir_edit = int(float(self.tab_widget.currentWidget().sole_rir_edit.text()))
            rir_list = RirWindow.rir_with_pero_gl(self, "Не нужно", '', roof_rir_edit, sole_rir_edit, volume_cement)
            work_list.extend(rir_list[1:])

        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def sand_select(self):
        self.dict_nkt = {}
        self.dict_nkt[self.data_well.nkt_diam] = None
        if self.data_well.column_additional is False or (self.data_well.column_additional is True and \
                                                         self.data_well.current_bottom <=
                                                         self.data_well.head_column_additional.get_value):
            sand_select = f'перо + НКТ{self.data_well.nkt_diam}мм 20м + реперный патрубок'
            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.current_bottom - 50

        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:
            sand_select = f'обточную муфту + НКТ{60}мм 20м + реперный патрубок + НКТ60мм ' \
                          f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value, 0)}м '

            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.head_column_additional.get_value - 50
            self.dict_nkt["60"] = round(
                self.data_well.current_bottom - self.data_well.head_column_additional.get_value - 50, 0)
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:
            sand_select = f'обточную муфту + НКТ{self.data_well.nkt_diam}мм со снятыми фасками {20}м + реперный патрубок + ' \
                          f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками ' \
                          f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value, 0)}м'
            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.current_bottom - 50
        return sand_select

    def sandFilling(self, filling_depth, sole_sand_edit, privyazka_question_QCombo):
        from work_py.alone_oreration import well_volume, volume_vn_ek, volume_nkt

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])
        self.dict_nkt = {}
        self.dict_nkt[self.data_well.nkt_diam] = None
        if self.data_well.column_additional is False or (self.data_well.column_additional is True and \
                                                         self.data_well.current_bottom <=
                                                         self.data_well.head_column_additional.get_value):
            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.current_bottom - 50

        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value < 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:

            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.head_column_additional.get_value - 50
            self.dict_nkt["60"] = round(
                self.data_well.current_bottom - self.data_well.head_column_additional.get_value - 50, 0)
        elif self.data_well.column_additional is True and \
                self.data_well.column_additional_diameter.get_value > 110 and \
                self.data_well.current_bottom >= self.data_well.head_column_additional.get_value:
            self.dict_nkt[self.data_well.nkt_diam] = self.data_well.current_bottom - 50
        volume_vn = volume_vn_ek(self, filling_depth)

        sand_volume = round(1.05 * (sole_sand_edit - filling_depth) * volume_vn, 1)

        hours = round(filling_depth / 320, 1)

        if hours < 4 and "Ойл" in data_list.contractor:
            hours = 4

        volume_nkt = volume_nkt(self.dict_nkt)
        filling_list = [
            [None, 1,
             'Работы по установке песчаного моста выполнять согласно технологической инструкции'
             ' П2-05.01 ТИ-1430 ЮЛ-111 "ОТСЫПКА ЗАБОЯ СКВАЖИНЫ КВАРЦЕВЫМ ПЕСКОМ, ПРОППАНТОМ"',
             None, None, None, None, None, None, None, 'Мастер, бурильщик', None],
            [f'Спустить  {self.sand_select()} на НКТ{nkt_diam}мм до глубины Н={self.data_well.current_bottom - 20}м '
             f'(т.з. {self.data_well.current_bottom}м)', None,
             f'Спустить  {self.sand_select()} на НКТ{nkt_diam}мм до глубины Н={self.data_well.current_bottom - 20}м '
             f'(т.з. {self.data_well.current_bottom}м) с замером, '
             f'ШАБЛОНИРОВАНИЕМ шаблоном {self.data_well.nkt_template}мм. (При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ) ',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(sole_sand_edit, 1)],
            [f'Промыть скважину  с допуском пера в интервале {sole_sand_edit - 20}-{sole_sand_edit}м',
             None, f'Промыть скважину обратной циркуляцией жидкостью плотностью {self.data_well.fluid_work} с '
                   f'допуском пера в интервале {sole_sand_edit - 20}-{sole_sand_edit}м до выхода чистой жидкости, '
                   f'отбить забой с циркуляцией промывочной жидкости. При несоответствии текущего забоя плановому, '
                   f'дальнейшие работы согласовать с геологической службой подрядчика по ТКРС.',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [f'Приподнять перо до Н={sole_sand_edit - 50}м', None,
             f'Приподнять перо до Н={filling_depth - 50}м (на 50 м выше планируемой кровли песчаного моста). '
             f'В СЛУЧАЕ ОТСУТСТВИЯ ЦИРКУЛЯЦИИ ПРИ ПРОМЫВКЕ СКВАЖИНЫ (ПОГЛОЩЕНИЕ ЖИДКОСТИ) ГЛУБИНА НАХОЖДЕНИЯ ПЕРА '
             F'ДОЛЖНА БЫТЬ ВЫШЕ ПОГЛОЩАЮЩИХ ИНТЕРВАЛОВ.',
             None, None, None, None, None, None, None,
             'мастер КРС', lifting_nkt_norm(filling_depth, 1)],
            [None,
             None, f'Подготовить проппант (кварцевый песок) в объеме {sand_volume * 1.1:.0f} литров.\n'
                   f' Расчетный объем песка определяется по формуле \n'
                   f'(H - мощность песчаного моста, м; D-внутренний диаметр ЭК, мм; \n'
                   f'1,05 - коэффициент усадки песка; 1000 - переводной коэффициент)',
             None, None, None, None, None, None, None,
             None, None],
            [f'отсыпка кварцевым песком в инт. {filling_depth} - {sole_sand_edit} в объеме {sand_volume}л',
             None, f'Произвести отсыпку кварцевым песком в инт. {filling_depth} - {sole_sand_edit} '
                   f'в объеме {sand_volume}л: \n'
                   f' Включить подачу насосного агрегата с равномерным расходом жидкости 2-3 л/сек. '
                   f'Отсыпку проппантом (кварцевым песком) выполнять с помощью оттарированной емкости, объем которой '
                   f'точно определен. Отсыпку выполнять путем ПОСТЕПЕННОГО РАВНОМЕРНОГО добавления проппанта '
                   f'(кварцевого песка) в поток жидкости с концентрацией не более 10 ЛИТРОВ ПЕСКА НА 100 ЛИТРОВ '
                   F'ЖИДКОСТИ. После каждого введения 50 литров песка подавать чистую жидкость в объеме не менее '
                   f'100 литров. Чередовать циклы "50 ЛИТРОВ ПЕСОК С ЖИДКОСТЬЮ / 100 ЛИТРОВ ЧИСТОЙ ЖИДКОСТИ" до '
                   f'отсыпки полного объема.  \nПродолжить подачу в НКТ жидкости глушения с расходом 2-3 л/сек, '
                   f'закачать жидкость в объеме, равном внутреннему объему НКТ V= {volume_nkt:.1f}м3. \n'
                   f'Поднять перо на безопасное '
                   f'расстояние - 200 м. \nВремя начала оседания песка определяется '
                   f'с момента завершения отсыпки. Расстояние принимается от устья до кровли песчаного моста по '
                   f'формуле (Н - расстояние от устья до кровли; 320 - скорость оседания, м/час) \n'
                   f't = H / 320, час',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],

            [f'Ожидание оседания песка {hours} часа.',
             None,
             f'Ожидание оседания песка {hours} часа. \n Во время оседания песка проверять подвижность подвески НКТ '
             f'вытяжкой на полную трубу не реже одного раза в 5 мин. \nПосле завершения времени оседания песка '
             f'допуском НКТ со скоростью спуска не более 0,1 м/с отбить кровлю песчаного моста. Если '
             f'кровля определена ниже планируемой глубины – произвести досыпку проппанта (кварцевого песка), '
             f'если выше – вымыв излишков песка обратной промывкой.',
             None, None, None, None, None, None, None,
             'мастер КРС', hours],
            [None, None,
             f'Допуском компоновки со скоростью спуска не более 0,1 м/с отбить кровлю песчаного моста'
             f'(плановый забой -{filling_depth}м). '
             f'Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через РИТС {data_list.contractor}". '
             f'При необходимости '
             f'подготовить место для установки партии ГИС напротив мостков. Произвести  монтаж ГИС согласно схемы №8 при '
             f'привязке утвержденной главным инженером {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'Привязка ', None,
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'Определение кровли', None,
             f'В случае если кровля песчаного моста на гл.{filling_depth}м дальнейшие работы продолжить дальше по плану'
             f'В случае пеcчаного моста ниже гл.{filling_depth}м работы повторить с корректировкой объема и '
             f'технологических глубин.'
             f' В случае песчаного моста выше гл.{filling_depth}м вымыть песок до гл.{filling_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', None]
        ]

        if OpressovkaEK.testing_pressure(self, filling_depth) is False:
            filling_list.insert(-1,
                                [
                                    f'Опрессовать в инт{filling_depth}-0м на Р={self.data_well.max_admissible_pressure.get_value}атм',
                                    None, f'Опрессовать эксплуатационную колонну в интервале {filling_depth}-0м на'
                                          f'Р={self.data_well.max_admissible_pressure.get_value}атм'
                                          f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
                                          f'(Вызов представителя осуществлять телефонограммой за 12 часов, '
                                          f'с подтверждением за 2 часа'
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
                                 'мастер КРС', None])

        if privyazka_question_QCombo != "Да":
            filling_list.pop(9)
            filling_list.pop(8)

        filling_list.append([None, None,
                             f'Поднять {self.sand_select()} НКТ{nkt_diam}м с глубины {filling_depth}м с доливом '
                             f'скважины в объеме {round(filling_depth * 1.12 / 1000, 1)}м3 тех. жидкостью '
                             f'уд.весом {self.data_well.fluid_work}',
                             None, None, None, None, None, None, None,
                             'мастер КРС', lifting_nkt_norm(filling_depth, 1)])
        self.data_well.current_bottom = filling_depth

        self.calculate_chemistry('песок', sand_volume)

        if "Ойл" in data_list.contractor:
            filling_list = filling_list[1:]

        return filling_list

    def sandWashing(self):

        nkt_diam = ''.join(['73' if self.data_well.column_diameter.get_value > 110 else '60'])

        washingDepth, ok = QInputDialog.getDouble(None, 'вымыв песка',
                                                  'Введите глубину вымыва песчанного моста',
                                                  self.data_well.current_bottom, 0, 6000, 1)
        washingOut_list = [
            [f'СПО пера до {round(self.data_well.current_bottom, 0)}м', None,
             f'Спустить  {SandWindow.sand_select(self)}  на НКТ{nkt_diam}м до глубины {round(self.data_well.current_bottom, 0)}м с '
             f'замером,'
             f' шаблонированием шаблоном {self.data_well.nkt_template}мм. '
             f'(При СПО первых десяти НКТ на '
             f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'Мастер КР', descentNKT_norm(self.data_well.current_bottom, 1)],
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
             f'жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', lifting_nkt_norm(washingDepth, 1.2)]]
        self.data_well.current_bottom = washingDepth

        return washingOut_list
