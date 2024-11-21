from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import data_list
from main import MyMainWindow
from .alone_oreration import volume_vn_ek
from .parent_work import TabWidgetUnion, TabPageUnion, WindowUnion
from .rir import RirWindow

from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from .rir import TabPageSoRir


class TabPageSoSand(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.dict_data_well = parent

        self.validator = QIntValidator(0, 80000)

        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.current_label = QLabel("необходимый забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.validator)
        self.current_edit.setText(str(self.dict_data_well["current_bottom"]))

        self.pero_combo_Label = QLabel("выбор пера", self)
        self.pero_combo_QCombo = QComboBox(self)
        self.pero_combo_QCombo.addItems(
            ['перо + КОТ', 'Перо', 'обточную муфту + КОТ', 'обточную муфту', 'перо-110мм', 'пило-муфту'])

        if self.dict_data_well["column_additional"] or self.dict_data_well["column_diametr"]._value < 120:
            self.pero_combo_QCombo.setCurrentIndex(2)

        self.solvent_question_Label = QLabel("необходимость растворителя", self)
        self.solvent_question_QCombo = QComboBox(self)
        self.solvent_question_QCombo.addItems(['Нет', 'Да'])

        self.solvent_Label = QLabel("объем растворителя", self)
        self.solvent_volume_edit = QLineEdit(self)
        self.solvent_volume_edit.setValidator(self.validator)
        self.solvent_volume_edit.setText("2")

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator)

        if len(self.dict_data_well["plast_project"]) != 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(self.dict_data_well["plast_project"])
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.pero_combo_Label, 4, 4)
        self.grid.addWidget(self.pero_combo_QCombo, 5, 4)
        self.grid.addWidget(self.solvent_question_Label, 4, 5)
        self.grid.addWidget(self.solvent_question_QCombo, 5, 5)

        self.grid.addWidget(self.solvent_Label, 6, 3)
        self.grid.addWidget(self.solvent_volume_edit, 7, 3)

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
        self.need_change_zgs_combo.setCurrentIndex(0)

        if len(self.dict_data_well['plast_work']) == 0:
            self.need_change_zgs_combo.setCurrentIndex(1)

    def update_change_fluid(self, index):
        if index == 'Да':

            category_h2s_list_plan = list(
                map(int, [self.dict_data_well["dict_category"][plast]['по сероводороду'].category for plast in
                          self.dict_data_well["plast_project"] if self.dict_data_well["dict_category"].get(plast) and
                          self.dict_data_well["dict_category"][plast]['отключение'] == 'планируемый']))

            if len(category_h2s_list_plan) != 0:
                plast = self.dict_data_well["plast_project"][0]
                self.pressuar_new_edit.setText(
                    f'{self.dict_data_well["dict_category"][plast]["по давлению"].data_pressuar}')
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


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoSand(parent), 'перо')


class PeroWindow(WindowUnion):
    work_sand_window = None

    def __init__(self, dict_data_well, table_widget, parent=None):
        super().__init__()

        self.dict_data_well = dict_data_well
        self.ins_ind = dict_data_well['ins_ind']
        self.tabWidget = TabWidget(self.dict_data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)        
        self.table_widget = table_widget
       

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def add_work(self):
        try:
            pero_combo_QCombo = self.tabWidget.currentWidget().pero_combo_QCombo.currentText()
            current_edit = int(float(self.tabWidget.currentWidget().current_edit.text().replace(',', '.')))
            if current_edit >= self.dict_data_well["bottomhole_artificial"]._value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{current_edit}м ниже исскуственного '
                                    f'{self.dict_data_well["bottomhole_artificial"]._value}м')
                return

            solvent_question_QCombo = str(self.tabWidget.currentWidget().solvent_question_QCombo.currentText())
            solvent_volume_edit = self.tabWidget.currentWidget().solvent_volume_edit.text().replace(',', '.')
            if solvent_volume_edit != '':
                solvent_volume_edit = round(float(solvent_volume_edit), 1)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        work_list = self.pero(current_edit, pero_combo_QCombo, solvent_question_QCombo, solvent_volume_edit)

        self.dict_data_well["current_bottom"] = current_edit
        self.populate_row(self.ins_ind, work_list, self.table_widget)
        data_list.pause = False
        self.close()

    def pero(self, current_edit, pero_combo_QCombo, solvent_question_QCombo, solvent_volume_edit):
        from .rir import RirWindow
        from .template_work import TemplateKrs

        pero_list = RirWindow.pero_select(self, current_edit, pero_combo_QCombo)

        gipsPero_list = [
            [f'Спустить {pero_list} на тНКТ{self.dict_data_well["nkt_diam"]}мм', None,
             f'Спустить {pero_list} на тНКТ{self.dict_data_well["nkt_diam"]}мм до глубины {self.dict_data_well["current_bottom"]}м '
             f'с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. Опрессовать НКТ на 200атм. Вымыть шар. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 2.5],
            [None, None, f'Нормализовать забой обратной промывкой тех жидкостью уд.весом '
                         f'{self.dict_data_well["fluid_work"]} до глубины {self.dict_data_well["current_bottom"]}м.',
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
                f'Промывка уд.весом {self.dict_data_well["fluid_work_short"]} в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ',
                None,
                f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {self.dict_data_well["fluid_work"]} при расходе жидкости '
                f'6-8 л/сек в присутствии представителя Заказчика в объеме {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3. '
                f'ПРИ ПРОМЫВКЕ НЕ '
                f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {self.dict_data_well["max_admissible_pressure"]._value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
                f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
                None, None, None, None, None, None, None,
                'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'Приподнять до глубины {round(self.dict_data_well["current_bottom"] - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
             f'при необходимости повторная промывка.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 2.49],
            [None, None,
             f'Поднять {pero_list} на НКТ{self.dict_data_well["nkt_diam"]}мм с глубины {self.dict_data_well["current_bottom"]}м с доливом скважины в '
             f'объеме {round(self.dict_data_well["current_bottom"] * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.dict_data_well["fluid_work"]}',
             None, None, None, None, None, None, None,
             'Мастер КРС',
             round(
                 self.dict_data_well["current_bottom"] / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * self.dict_data_well[
                     "current_bottom"] / 9.5 + 0.17 + 0.5,
                 2)],
        ]
        if solvent_question_QCombo == "Нет":
            gipsPero_list.pop(2)
        return gipsPero_list
