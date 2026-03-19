from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton

import data_list
from work_py.calculate_work_parametrs import volume_work

from work_py.parent_work import TabWidgetUnion, TabPageUnion, WindowUnion

YES_NO_OPTIONS = ['Нет', 'Да']


class TabPageSoSand(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.INT_VALIDATOR = QIntValidator(0, 80000)
        self.FLOAT_VALIDATOR = QDoubleValidator(0.0, 1.65, 2)
        self.PERO_OPTIONS = ['перо + КОТ', 'Перо', 'обточную муфту + КОТ', 'обточную муфту', 'перо-110мм', 'пило-муфту']
        self.YES_NO_OPTIONS = YES_NO_OPTIONS
        self.DEFAULT_SOLVENT_VOLUME = "2"

        self.current_label = QLabel("необходимый забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.INT_VALIDATOR)
        self.current_edit.setText(str(self.data_well.current_bottom))

        self.pero_combo_label = QLabel("выбор пера", self)
        self.pero_combo = QComboBox(self)
        self.pero_combo.addItems(self.PERO_OPTIONS)

        if self.data_well.column_additional or self.data_well.column_diameter.get_value < 120:
            self.pero_combo.setCurrentIndex(2)

        self.solvent_question_label = QLabel("необходимость растворителя", self)
        self.solvent_question_combo = QComboBox(self)
        self.solvent_question_combo.addItems(self.YES_NO_OPTIONS)

        self.solvent_label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(self.INT_VALIDATOR)
        self.solvent_volume_edit.setText(self.DEFAULT_SOLVENT_VOLUME)

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(self.YES_NO_OPTIONS)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.FLOAT_VALIDATOR)

        self.pressure_new_label = QLabel('Ожидаемое давление', self)
        self.pressure_new_edit = QLineEdit(self)
        self.pressure_new_edit.setValidator(self.INT_VALIDATOR)

        if len(self.data_well.plast_project) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(self.data_well.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)

        self.fluid_widgets = [
            self.plast_new_label, self.plast_new_combo,
            self.fluid_new_label, self.fluid_new_edit,
            self.pressure_new_label, self.pressure_new_edit
        ]

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.pero_combo_label, 4, 4)
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
        is_visible = (index == self.YES_NO_OPTIONS[1])

        for widget in self.fluid_widgets:
            widget.setVisible(is_visible)

        if is_visible:
            category_h2s_list_plan = list(
                map(int, [self.data_well.dict_category[plast]['по сероводороду'].category for plast in
                          self.data_well.plast_project if self.data_well.dict_category.get(plast) and
                          self.data_well.dict_category[plast]['отключение'] == 'планируемый']))

            if len(category_h2s_list_plan) != 0:
                plast = self.data_well.plast_project[0]
                self.pressure_new_edit.setText(
                    f'{self.data_well.dict_category[plast]["по давлению"].data_pressure}')


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
            try:
                current_edit = int(float(self.tab_widget.currentWidget().current_edit.text().replace(',', '.')))
            except ValueError:
                QMessageBox.warning(self, 'Ошибка', 'Некорректное значение в поле "необходимый забой". Введите число.')
                return

            if current_edit >= self.data_well.bottom_hole_artificial.get_value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{current_edit}м ниже искусственного '
                                    f'{self.data_well.bottom_hole_artificial.get_value}м')
                return

            solvent_question_combo = str(self.tab_widget.currentWidget().solvent_question_combo.currentText())
            solvent_volume_edit_text = self.tab_widget.currentWidget().solvent_volume_edit.text().replace(',', '.')
            solvent_volume_edit = None
            if solvent_volume_edit_text != '':
                try:
                    solvent_volume_edit = round(float(solvent_volume_edit_text), 1)
                except ValueError:
                    QMessageBox.warning(self, 'Ошибка', 'Некорректное значение в поле "объем растворителя". Введите число.')
                    return

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')
            return # Добавлен возврат, чтобы предотвратить дальнейшее выполнение в случае общей ошибки

        gips_pero_list = self.pero(current_edit, pero_combo, solvent_question_combo, solvent_volume_edit)
        # populate_row ожидает list[list], а pero() возвращает list[dict]
        work_list = [
            [
                row.get("short_description"),
                None,
                row.get("detailed_description"),
                None, None, None, None, None, None, None, None,
                row.get("executor"),
                row.get("duration"),
            ]
            for row in gips_pero_list
        ]

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
            {
                'short_description': f'Спустить {pero_list} на тНКТ{self.data_well.nkt_diam}мм',
                'detailed_description': (
                    f'Спустить {pero_list} на тНКТ{self.data_well.nkt_diam}мм до глубины {self.data_well.current_bottom}м '
                    f'с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
                    f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)'
                ),
                'executor': 'мастер КРС',
                'duration': 2.5,
            },
            {
                'short_description': None,
                'detailed_description': (
                    f'Нормализовать забой обратной промывкой тех жидкостью уд.весом '
                    f'{self.data_well.fluid_work} до глубины {self.data_well.current_bottom}м.'
                ),
                'executor': 'Мастер КРС',
                'duration': None,
            },
            {
                'short_description': f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3',
                'detailed_description': (
                    f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
                    f'Очистить колонну от АСПО растворителем - {solvent_volume_edit}м3. При открытом затрубном '
                    f'пространстве закачать в '
                    f'трубное пространство растворитель в объеме {solvent_volume_edit}м3, продавить в трубное '
                    f'пространство тех.жидкостью '
                    f'в объеме {round(3 * float(current_edit) / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
                    f'пространство. Реагирование 2 часа.'
                ),
                'executor': 'Мастер КРС, предст. заказчика',
                'duration': 4,
            },
            {
                'short_description': f'Промывка уд.весом {self.data_well.fluid_work_short} в объеме {volume_work(self.data_well)* 1.5:.1f}м3 ',
                'detailed_description': (
                    f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.data_well.fluid_work} при расходе жидкости '
                    f'6-8 л/сек в присутствии представителя Заказчика в объеме {volume_work(self.data_well)* 1.5:.1f}м3. '
                    f'ПРИ ПРОМЫВКЕ НЕ '
                    f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.data_well.max_admissible_pressure.get_value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
                    f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН'
                ),
                'executor': 'Мастер КРС, представитель ЦДНГ',
                'duration': 1.5,
            },
            {
                'short_description': None,
                'detailed_description': (
                    f'Приподнять до глубины {round(self.data_well.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
                    f'при необходимости повторная промывка.'
                ),
                'executor': 'Мастер КРС, представитель ЦДНГ',
                'duration': 2.49,
            },
            {
                'short_description': None,
                'detailed_description': (
                    f'Поднять {pero_list} на НКТ{self.data_well.nkt_diam}мм с глубины {self.data_well.current_bottom}м с доливом скважины в '
                    f'объеме {round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work}'
                ),
                'executor': 'Мастер КРС',
                'duration': round(
                    self.data_well.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * self.data_well.current_bottom / 9.5 + 0.17 + 0.5,
                    2),
            },
        ]
        if solvent_question_combo == YES_NO_OPTIONS[0]:  # 'Нет'
            # Find the index of the solvent step and remove it
            solvent_step_index = -1
            for i, step in enumerate(gips_pero_list):
                if "Очистить колонну от АСПО растворителем" in step.get('short_description', ''):
                    solvent_step_index = i
                    break
            if solvent_step_index != -1:
                gips_pero_list.pop(solvent_step_index)
        return gips_pero_list
