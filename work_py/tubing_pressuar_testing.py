from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import  QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, QPushButton

import well_data
from main import MyMainWindow
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageSoBlock(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__()

        self.dict_data_well = parent

        self.validator = QIntValidator(0, 80000)

        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.current_label = QLabel("Текущий забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.validator_float)
        self.current_edit.setText(str(self.dict_data_well["current_bottom"]))

        self.select_nkt_label = QLabel("выбор компоновки", self)
        self.select_nkt_combo = QComboBox(self)
        self.select_nkt_combo.addItems(['Фондовые НКТ', 'Технологическое НКТ'])

        self.pressuar_label = QLabel("Давление опрессовки", self)
        self.pressuar_edit = QLineEdit(self)
        self.pressuar_edit.setValidator(self.validator_float)
        self.pressuar_edit.setText(str(220))

        self.length_nkt_label = QLabel("Длина НКТ", self)
        self.length_nkt_edit = QLineEdit(self)
        self.length_nkt_edit.setValidator(self.validator_float)
        self.length_nkt_edit.setText(f'{sum(self.dict_data_well["dict_nkt_po"].values())}')

        self.distance_between_nkt_label = QLabel('Расстояние между НКТ')
        self.distance_between_nkt_edit = QLineEdit(self)
        self.distance_between_nkt_edit.setValidator(self.validator_float)
        self.distance_between_nkt_edit.setText(f'{300}')

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.select_nkt_label, 4, 4)
        self.grid.addWidget(self.select_nkt_combo, 5, 4)

        self.grid.addWidget(self.distance_between_nkt_label, 4, 5)
        self.grid.addWidget(self.distance_between_nkt_edit, 5, 5)

        self.grid.addWidget(self.length_nkt_label, 4, 6)
        self.grid.addWidget(self.length_nkt_edit, 5, 6)

        self.grid.addWidget(self.pressuar_label, 4, 7)
        self.grid.addWidget(self.pressuar_edit, 5, 7)

        self.select_nkt_combo.currentTextChanged.connect(self.update_tubing)

    def update_tubing(self, index):
        if index == 'Фондовые НКТ':
            self.length_nkt_edit.setText(f'{sum(self.dict_data_well["dict_nkt_po"].values())}')
        else:
            self.length_nkt_edit.setText(f'{self.dict_data_well["current_bottom"]}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoBlock(parent), 'Опрессовка НКТ')


class TubingPressuarWindow(WindowUnion):
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

    def add_work(self):
        try:

            distance_between_nkt_edit = self.tabWidget.currentWidget().distance_between_nkt_edit.text().replace(',', '.')
            if distance_between_nkt_edit != '':
                distance_between_nkt_edit = int(float(distance_between_nkt_edit))
            select_nkt_combo = self.tabWidget.currentWidget().select_nkt_combo.currentText()
            current_edit = int(float(self.tabWidget.currentWidget().current_edit.text().replace(',', '.')))
            if current_edit >= self.dict_data_well["bottomhole_artificial"]._value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{current_edit}м ниже исскуственного '
                                    f'{self.dict_data_well["bottomhole_artificial"]._value}м')
                return

            length_nkt_edit = self.tabWidget.currentWidget().length_nkt_edit.text().replace(',', '.')
            if length_nkt_edit != '':
                length_nkt_edit = int(float(length_nkt_edit))
            pressuar_edit = self.tabWidget.currentWidget().pressuar_edit.text().replace(',', '.')
            if pressuar_edit != '':
                pressuar_edit = round(float(pressuar_edit), 1)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        work_list = self.pressuar_nkt_work(current_edit, select_nkt_combo, length_nkt_edit, pressuar_edit,
                                           distance_between_nkt_edit)

        self.populate_row(self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def pressuar_nkt_work(self, current_edit, select_nkt_combo, length_nkt_edit, pressuar_edit,
                          distance_between_nkt_edit):
        from .descent_gno import GnoDescentWindow
        from .rationingKRS import liftingNKT_norm, descentNKT_norm

        if select_nkt_combo != 'Фондовые НКТ' or self.dict_data_well["curator"] == 'ОР':
            block_pack_list = [
                [f'Спустить заглушку на фНКТ{self.dict_data_well["nkt_diam"]} до глубины {current_edit}мм', None,
                 f'Произвести спуск заглушки на фондовых НКТ с поинтервальной опрессовкой их через каждые '
                 f'{distance_between_nkt_edit}м на Р={pressuar_edit}тм  на Н={length_nkt_edit}м. '
                 f'Негерметичные НКТ отбраковать. (При СПО первых десяти НКТ на спайдере дополнительно устанавливать'
                 f' элеватор ЭХЛ). ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(length_nkt_edit, 1)],
                [None, None,
                 f'Поднять заглушку на НКТ с доливом тех жидкости {self.dict_data_well["fluid_work"]}', None, None, None, None,
                 None, None, None,
                 'Мастер КРС', liftingNKT_norm(length_nkt_edit, 1)],
            ]
        else:

            calc_fond_list = GnoDescentWindow.calc_fond_nkt(self, length_nkt_edit, distance_between_nkt_edit)

            block_pack_list = [
                [f'Спустить заглушку на фНКТ{self.dict_data_well["nkt_diam"]} до глубины {current_edit}мм', None,
                 f'Произвести спуск заглушки на фондовых НКТ с поинтервальной опрессовкой их через каждые '
                 f'{distance_between_nkt_edit}м на Р={pressuar_edit}тм  на Н={length_nkt_edit}м. '
                 f'Негерметичные НКТ отбраковать. (При СПО первых десяти НКТ на спайдере дополнительно устанавливать'
                 f' элеватор ЭХЛ). ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(length_nkt_edit, 1)],
                [None, None,
                 calc_fond_list,
                 None, None, None, None, None, None, None,
                 'мастер КРС, заказчик', descentNKT_norm(length_nkt_edit, 1)],
                [None, None,
                 f'Поднять заглушку на НКТ с доливом тех жидкости {self.dict_data_well["fluid_work"]} с глубины {length_nkt_edit}м',
                 None, None, None, None,
                 None, None, None,
                 'Мастер КРС', liftingNKT_norm(length_nkt_edit, 1)]]

        return block_pack_list
