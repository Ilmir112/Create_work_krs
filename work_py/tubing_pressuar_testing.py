from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import  QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton

import data_list
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageSoBlock(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)
        self.validator_float = QDoubleValidator(0.0, 1.65, 2)

        self.current_label = QLabel("Текущий забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.validator_float)
        self.current_edit.setText(str(self.data_well.current_bottom))

        self.select_nkt_label = QLabel("выбор компоновки", self)
        self.select_nkt_combo = QComboBox(self)
        self.select_nkt_combo.addItems(['Фондовые НКТ', 'Технологическое НКТ'])

        self.pressure_label = QLabel("Давление опрессовки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setValidator(self.validator_float)
        self.pressure_edit.setText(str(220))

        self.length_nkt_label = QLabel("Длина НКТ", self)
        self.length_nkt_edit = QLineEdit(self)
        self.length_nkt_edit.setValidator(self.validator_float)
        self.length_nkt_edit.setText(f'{sum(self.data_well.dict_nkt_after.values())}')

        self.distance_between_nkt_label = QLabel('Расстояние между НКТ')
        self.distance_between_nkt_edit = QLineEdit(self)
        self.distance_between_nkt_edit.setValidator(self.validator_float)
        self.distance_between_nkt_edit.setText(f'{300}')

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.select_nkt_label, 4, 4)
        self.grid.addWidget(self.select_nkt_combo, 5, 4)

        self.grid.addWidget(self.distance_between_nkt_label, 4, 5)
        self.grid.addWidget(self.distance_between_nkt_edit, 5, 5)

        self.grid.addWidget(self.length_nkt_label, 4, 6)
        self.grid.addWidget(self.length_nkt_edit, 5, 6)

        self.grid.addWidget(self.pressure_label, 4, 7)
        self.grid.addWidget(self.pressure_edit, 5, 7)

        self.select_nkt_combo.currentTextChanged.connect(self.update_tubing)

    def update_tubing(self, index):
        if index == 'Фондовые НКТ':
            self.length_nkt_edit.setText(f'{sum(self.data_well.dict_nkt_after.values())}')
        else:
            self.length_nkt_edit.setText(f'{self.data_well.current_bottom}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoBlock(parent), 'Опрессовка НКТ')


class TubingPressureWindow(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.pressure_data = None
        self.length_nkt = None
        self.current_bottom = None
        self.select_nkt_combo = None
        self.distance_between_nkt = None
        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)
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

            self.distance_between_nkt = self.tabWidget.currentWidget().distance_between_nkt_edit.text().replace(',', '.')
            if self.distance_between_nkt != '':
                self.distance_between_nkt = int(float(self.distance_between_nkt))
            self.select_nkt_combo = self.tabWidget.currentWidget().select_nkt_combo.currentText()
            self.current_bottom = int(float(self.tabWidget.currentWidget().current_edit.text().replace(',', '.')))
            if self.current_bottom >= self.data_well.bottom_hole_artificial.get_value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{self.current_bottom}м ниже искусственного '
                                    f'{self.data_well.bottom_hole_artificial.get_value}м')
                return

            self.length_nkt = self.tabWidget.currentWidget().length_nkt_edit.text().replace(',', '.')
            if self.length_nkt != '':
                self.length_nkt = int(float(self.length_nkt))
            self.pressure_data = self.tabWidget.currentWidget().pressure_edit.text().replace(',', '.')
            if self.pressure_data != '':
                self.pressure_data = round(float(self.pressure_data), 1)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        work_list = self.pressure_nkt_work()
        if work_list:
            self.populate_row(self.insert_index, work_list, self.table_widget)
            data_list.pause = False
            self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def pressure_nkt_work(self):
        from work_py.descent_gno import DescentParent
        from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm

        if self.select_nkt_combo != 'Фондовые НКТ' or self.data_well.curator == 'ОР':
            block_pack_list = [
                [f'Спустить заглушку на фНКТ{self.data_well.nkt_diam} до глубины {self.current_bottom}мм', None,
                 f'Произвести спуск заглушки на фондовых НКТ с поинтервальной опрессовкой их через каждые '
                 f'{self.distance_between_nkt}м на Р={self.pressure_data}тм  на Н={self.length_nkt}м. '
                 f'Негерметичные НКТ отбраковать. (При СПО первых десяти НКТ на спайдере дополнительно устанавливать'
                 f' элеватор ЭХЛ). ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(self.length_nkt, 1)],
                [None, None,
                 f'Поднять заглушку на НКТ с доливом тех жидкости {self.data_well.fluid_work}', None, None, None, None,
                 None, None, None,
                 'Мастер КРС', liftingNKT_norm(self.length_nkt, 1)],
            ]
        else:

            calc_fond_list = self.calc_fond_nkt(self.length_nkt, self.distance_between_nkt)

            block_pack_list = [
                [f'Спустить заглушку на фНКТ{self.data_well.nkt_diam} до глубины {self.current_bottom}мм', None,
                 f'Произвести спуск заглушки на фондовых НКТ с поинтервальной опрессовкой их через каждые '
                 f'{self.distance_between_nkt}м на Р={self.pressure_data}атм  на Н={self.length_nkt}м. '
                 f'Негерметичные НКТ отбраковать. (При СПО первых десяти НКТ на спайдере дополнительно устанавливать'
                 f' элеватор ЭХЛ). ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(self.length_nkt, 1)],
                [None, None,
                 calc_fond_list,
                 None, None, None, None, None, None, None,
                 'мастер КРС, заказчик', descentNKT_norm(self.length_nkt, 1)],
                [None, None,
                 f'Поднять заглушку на НКТ с доливом тех жидкости {self.data_well.fluid_work} с глубины {self.length_nkt}м',
                 None, None, None, None,
                 None, None, None,
                 'Мастер КРС', liftingNKT_norm(self.length_nkt, 1)]]

        return block_pack_list
