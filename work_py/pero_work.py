from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton

import data_list
from work_py.calculate_work_parametrs import volume_work

from work_py.parent_work import TabWidgetUnion, TabPageUnion, WindowUnion


class TabPageSoSand(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.current_label = QLabel("необходимый забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.validator)
        self.current_edit.setText(str(self.data_well.current_bottom))

        self.pero_combo_Label = QLabel("выбор пера", self)
        self.pero_combo = QComboBox(self)
        self.pero_combo.addItems(
            ['перо + КОТ', 'Перо', 'обточную муфту + КОТ', 'обточную муфту', 'перо-110мм', 'пило-муфту'])

        if self.data_well.column_additional or self.data_well.column_diameter.get_value < 120:
            self.pero_combo.setCurrentIndex(2)

        self.solvent_question_label = QLabel("необходимость растворителя", self)
        self.solvent_question_combo = QComboBox(self)
        self.solvent_question_combo.addItems(['Нет', 'Да'])

        self.solvent_label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(self.validator)
        self.solvent_volume_edit.setText("2")

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

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

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.pero_combo_Label, 4, 4)
        self.grid.addWidget(self.pero_combo, 5, 4)
        self.grid.addWidget(self.solvent_question_label, 4, 5)
        self.grid.addWidget(self.solvent_question_combo, 5, 5)

        self.grid.addWidget(self.solvent_label, 6, 3)
        self.grid.addWidget(self.solvent_volume_edit, 7, 3)

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
        self.need_change_zgs_combo.setCurrentIndex(0)

        if len(self.data_well.plast_work) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

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
        self.addTab(TabPageSoSand(parent), 'перо')


class PeroWindow(WindowUnion):
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

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def add_work(self):
        try:
            pero_combo = self.tab_widget.currentWidget().pero_combo.currentText()
            current_edit = int(float(self.tab_widget.currentWidget().current_edit.text().replace(',', '.')))
            if current_edit >= self.data_well.bottom_hole_artificial.get_value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{current_edit}м ниже искусственного '
                                    f'{self.data_well.bottom_hole_artificial.get_value}м')
                return

            solvent_question_combo = str(self.tab_widget.currentWidget().solvent_question_combo.currentText())
            solvent_volume_edit = self.tab_widget.currentWidget().solvent_volume_edit.text().replace(',', '.')
            if solvent_volume_edit != '':
                solvent_volume_edit = round(float(solvent_volume_edit), 1)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        work_list = self.pero(current_edit, pero_combo, solvent_question_combo, solvent_volume_edit)

        self.data_well.current_bottom = current_edit
        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def pero(self, current_edit, pero_combo, solvent_question_combo, solvent_volume_edit):
        from work_py.rir import RirWindow
        from work_py.template_work import TemplateKrs

        pero_list = RirWindow.pero_select(self, current_edit, pero_combo)

        gips_pero_list = [
            [f'Спустить {pero_list} на тНКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить {pero_list} на тНКТ{self.data_well.nkt_diam}мм до глубины {self.data_well.current_bottom}м '
             f'с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None, f'Нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{self.data_well.fluid_work} до глубины {self.data_well.current_bottom}м.',
             None, None, None, None,
             None, None, None,
             'Мастер КРС', None],
            [f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3', None,
             f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
             f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3. При открытом затрубном '
             f'пространстве закачать в '
             f'трубное пространство растворитель в объеме {solvent_volume_edit}м3, продавить в трубное '
             f'пространство тех.жидкостью '
             f'в объеме {round(3 * float(current_edit) / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [
                f'Промывка уд.весом {self.data_well.fluid_work_short} в объеме {volume_work(self.data_well)* 1.5:.1f}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости '
                f'6-8 л/сек в присутствии представителя Заказчика в объеме {volume_work(self.data_well)* 1.5:.1f}м3. '
                f'ПРИ ПРОМЫВКЕ НЕ '
                f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
                f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(self.data_well.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{self.data_well.nkt_diam}мм с глубины {self.data_well.current_bottom}м с доливом скважины в '
             f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             round(
                 self.data_well.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * self.data_well.current_bottom / 9.5 + 0.17 + 0.5,
                 2)],
        ]
        if solvent_question_combo == "Нет":
            gips_pero_list.pop(2)
        return gips_pero_list
