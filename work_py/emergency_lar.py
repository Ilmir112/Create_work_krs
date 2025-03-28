from PyQt5.QtGui import QIntValidator

import data_list

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, \
    QPushButton, QApplication

from work_py.emergencyWork import sbt_select
from work_py.parent_work import TabWidgetUnion, TabPageUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm


class TabPageSoLar(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.validator_int = QIntValidator(0, 10)

        self.lar_diameter_label = QLabel("Диаметр ловителя", self)
        self.lar_diameter_line = QLineEdit(self)

        self.lar_type_label = QLabel("Тип л овителя", self)
        self.lar_type_combo = QComboBox(self)
        raid_type_list = ['ОВ', 'ВТ', 'метчик', 'колокол', 'МЭС', 'МБУ', 'штанголовитель']
        self.lar_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['оборудование в ЭК', 'оборудование в ДП'])

        self.gidroayss_label = QLabel("Необходимость Гидроясса", self)
        self.gidroayss_combo = QComboBox(self)
        self.gidroayss_combo.addItems(['Нет', 'Да'])

        self.ubt_label = QLabel("Необходимость УБТ", self)
        self.ubt_combo = QComboBox(self)
        self.ubt_combo.addItems(['Нет', 'Да'])

        self.udlinitelel_label = QLabel("Необходимость удлинителя", self)
        self.udlinitelel = QComboBox(self)
        self.udlinitelel.addItems(['Нет', 'Да'])

        self.udlinitelel_length_label = QLabel("Длина удлинителя", self)
        self.udlinitelel_length = QLineEdit(self)
        self.udlinitelel_length.setValidator(self.validator_int)
        self.udlinitelel_length.setText('2')
        if self.data_well:
            if self.data_well.column_additional is False or \
                    (self.data_well.column_additional and self.data_well.head_column_additional.get_value < self.data_well.current_bottom):
                self.nkt_select_combo.setCurrentIndex(0)
            else:
                self.nkt_select_combo.setCurrentIndex(1)

        self.emergency_bottom_label = QLabel("аварийный забой", self)
        self.emergency_bottom_line = QLineEdit(self)
        self.emergency_bottom_line.setClearButtonEnabled(True)

        self.bottom_label = QLabel("Забой после ЛАР", self)
        self.bottom_line = QLineEdit(self)
        self.bottom_line.setClearButtonEnabled(True)

        self.nkt_str_label = QLabel("НКТ или СБТ, штанги", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ', "штанги"])
        # self.nkt_select_combo.currentTextChanged.connect(self.update_nkt)

        # self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)
        self.grid.addWidget(self.nkt_str_label, 0, 2)
        self.grid.addWidget(self.nkt_str_combo, 1, 2)

        self.grid.addWidget(self.nkt_select_label, 0, 3)
        self.grid.addWidget(self.nkt_select_combo, 1, 3)

        self.grid.addWidget(self.lar_type_label, 2, 1)
        self.grid.addWidget(self.lar_type_combo, 3, 1)

        self.grid.addWidget(self.lar_diameter_label, 2, 2)
        self.grid.addWidget(self.lar_diameter_line, 3, 2)

        self.grid.addWidget(self.gidroayss_label, 2, 3)
        self.grid.addWidget(self.gidroayss_combo, 3, 3)

        self.grid.addWidget(self.udlinitelel_label, 2, 4)
        self.grid.addWidget(self.udlinitelel, 3, 4)

        self.grid.addWidget(self.udlinitelel_length_label, 2, 5)
        self.grid.addWidget(self.udlinitelel_length, 3, 5)
        self.grid.addWidget(self.ubt_label, 2, 6)
        self.grid.addWidget(self.ubt_combo, 3, 6)

        self.grid.addWidget(self.emergency_bottom_label, 7, 1)
        self.grid.addWidget(self.emergency_bottom_line, 8, 1)

        self.grid.addWidget(self.bottom_label, 7, 2)
        self.grid.addWidget(self.bottom_line, 8, 2)

        # self.nkt_select_combo.currentTextChanged.connect(self.update_raid_edit)

        self.nkt_select_combo.setCurrentIndex(1)
        if self.data_well:
            self.bottom_line.setText(f'{self.data_well.current_bottom}')

            if self.data_well.column_additional is False or \
                    (self.data_well.column_additional and self.data_well.current_bottom < self.data_well.head_column_additional.get_value):
                self.nkt_select_combo.setCurrentIndex(1)
                self.nkt_select_combo.setCurrentIndex(0)
            else:
                self.nkt_select_combo.setCurrentIndex(1)

            if self.data_well.emergency_well is True:
                if self.data_well:
                    self.emergency_bottom_line.setText(f'{self.data_well.emergency_bottom}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoLar(parent), 'ловильные работы')


class EmergencyLarWork(WindowUnion):

    def __init__(self, data_well=None, table_widget=None, parent=None):
        super().__init__(data_well)
        self.data_well = data_well
        if self.data_well:
            self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.table_widget = table_widget

        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def add_work(self):
        self.gidroayss_combo = self.tab_widget.currentWidget().gidroayss_combo.currentText()
        self.ubt_combo = self.tab_widget.currentWidget().ubt_combo.currentText()
        self.nkt_str_combo = self.tab_widget.currentWidget().nkt_str_combo.currentText()
        self.lar_diameter_line = self.tab_widget.currentWidget().lar_diameter_line.text()
        self.udlinitelel = self.tab_widget.currentWidget().udlinitelel.currentText()
        self.udlinitelel = self.tab_widget.currentWidget().udlinitelel_length.text()
        if self.lar_diameter_line == '':
            QMessageBox.warning(self, 'Ошибка',
                                      'Выберете диаметр ловильного оборудования')
            return
        self.nkt_key = self.tab_widget.currentWidget().nkt_select_combo.currentText()
        self.lar_type_combo = self.tab_widget.currentWidget().lar_type_combo.currentText()
        self.emergency_bottom_line = self.tab_widget.currentWidget().emergency_bottom_line.text().replace(',', '.')
        self.bottom_line = self.tab_widget.currentWidget().bottom_line.text().replace(',', '.')
        if self.lar_type_combo in ['метчик', 'колокол', 'МЭС', 'МБУ'] and self.nkt_str_combo == 'НКТ':
            QMessageBox.warning(self, 'Недопустимая операция', f'Нельзя спускать {self.lar_type_combo} '
                                                               f'на не извлекаемые ловитель на НКТ')
            return
        if self.bottom_line != '':
            bottom_line = int(float(self.bottom_line))

        if self.emergency_bottom_line != '':
            emergency_bottom_line = int(float(self.emergency_bottom_line))

            if emergency_bottom_line > self.data_well.current_bottom:
                QMessageBox.warning(self, 'Ошибка',
                                          'Забой ниже глубины текущего забоя')
                return
        else:
            QMessageBox.warning(self, 'Ошибка',
                                      'ВВедите аварийный забой')
            return

        if self.nkt_key == 'оборудование в ЭК' and self.data_well.column_additional and \
                emergency_bottom_line > self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для доп колонны')
            return
        elif self.nkt_key == 'оборудование в ДП' and self.data_well.column_additional and \
                emergency_bottom_line < self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для основной колонны')
            return
        raid_list = []
        if self.nkt_str_combo == 'НКТ':
            raid_list = self.emergency_nkt()
        elif self.nkt_str_combo == 'СБТ':
            raid_list = self.emergence_sbt()
        elif self.nkt_str_combo == 'штанги':
            raid_list = self.emergency_pods()

        self.data_well.current_bottom = float(self.bottom_line)

        if raid_list:
            self.populate_row(self.insert_index, raid_list, self.table_widget)
            data_list.pause = False
            self.close()
            self.close_modal_forcefully()

    def emergence_sbt(self):
        bp_str = '+ БРП '
        gidroayss_str = ''
        usilit_gidroayss_str = ''
        ubt_str = ''
        udlinitelel_str = ''
        if self.udlinitelel == 'Да':
            udlinitelel_str = f' + удлинитель  (L={self.udlinitelel_length}м) '
        if self.gidroayss_combo == 'Да':
            gidroayss_str = 'гидроясс '
            usilit_gidroayss_str = ' + усилитель гидроясса '
        if self.ubt_combo == 'Да':
            ubt_str = '+ УБТ 3шт '

        if self.lar_type_combo in ['ВТ', 'ОВ']:
            bp_str = ''
            if self.gidroayss_combo == 'Нет':
                emergency_str = f'{self.lar_type_combo}-{self.lar_diameter_line} ' \
                                f'(типоразмер согласовать с аварийной службой УСРСиСТ){udlinitelel_str}{gidroayss_str} {bp_str}'
            else:
                emergency_str = f'{self.lar_type_combo}-{self.lar_diameter_line} ' \
                                f'(типоразмер согласовать с аварийной службой УСРСиСТ){udlinitelel_str} + мех ясс ' \
                                f'+ {gidroayss_str}{ubt_str}{usilit_gidroayss_str}'
        else:
            emergency_str = f'{self.lar_type_combo}-{self.lar_diameter_line} (типоразмер согласовать с аварийной службой УСРСиСТ)'\
                            f' {udlinitelel_str}{bp_str}{gidroayss_str} + патрубок 1м +' \
                            f'{ubt_str} {usilit_gidroayss_str}'

        emergence_sbt = [
            [f'СПО ловильного оборудования ', None,
             f'По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: {emergency_str} на '
             f'{sbt_select(self, self.nkt_key)} '
             f' до глубины нахождения аварийной головы ({self.emergency_bottom_line}м)\n '
             f'Включение в компоновку ударной компоновки дополнительно согласовать с УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1)],
            [None, None,
             f'Во избежание срабатывания механизма фиксации плашек в освобожденном положении, спуск '
             f'следует производить без вращения труболовки',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'монтаж ведущей трубы', None,
             f'Произвести монтаж ведущей трубы и мех.ротора.\n '
             f'За 2-5 метров до верхнего конца аварийного объекта при наличии циркуляции рекомендуется '
             f'восстановить '
             f'циркуляцию и промыть скважину тех водой {self.data_well.fluid_work}. При прокачке промывочной '
             f'жидкости спустить '
             f'{self.lar_type_combo} до верхнего конца аварийной колонны.\n'
             f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
             f'инструмента  согласовать с аварийной службой супервайзинга.', None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 3],
            [None, None,
             f'Произвести расхаживание аварийной компоновки с постепенным увеличением'
             f' веса до 50т. Дальнейшие '
             f'увеличение нагрузки согласовать с УСРСиСТ. При отрицательных '
             f'результатах произвести освобождение ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 10],
            [None, None,
             f'При положительных результатах расхаживания - демонтаж ведущей трубы и мех.ротора. '
             f'Поднять компоновку с доливом тех жидкости в '
             f'объеме {round(self.data_well.current_bottom * 1.25 / 1000, 1)}м3'
             f' удельным весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер', lifting_nkt_norm(self.data_well.current_bottom, 1)],
            [None, None,
             f'При необходимости: Сборка и спуск компоновки: кольцевой фрезер с удлинителем '
             f'L= {udlinitelel_str}м + СБТ, до глубины нахождения аварийной "головы". (Компоновку согласовать '
             f'дополнительно с УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', descentNKT_norm(self.data_well.current_bottom, 1.2)],
            [None, None,
             f'Монтаж монтаж ведущей трубы и мех.ротора. Обуривание аварийной головы на глубины согласованной с '
             f'УСРСиСТ демонтаж мех ротора',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 10],
            [None, None,
             f'Поднять компоновку с доливом тех жидкости в объеме {round(self.data_well.current_bottom * 1.25 / 1000, 1)}м3'
             f' удельным весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', lifting_nkt_norm(self.data_well.current_bottom, 1)],
            [None, None,
             f'По согласованию заказчиком повторить ловильные аварийные работы'
             f' с подбором аварийного оборудования',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', None],
            [None, None,
             f'При отрицательном результате дальнейшие работы по дополнительному плану работ',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', None]]

        self.data_well.current_bottom = self.bottom_line
        return emergence_sbt

    def emergency_nkt(self):

        emergency_nkt_list = [
            [None, 'СПО ловильного оборудования',
             f'По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: '
             f'Спустить с замером {self.lar_type_combo}-{self.lar_diameter_line} + штангах на '
             f'{self.nkt_str_combo} до Н= {self.emergency_bottom_line}м с замером . ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.emergency_bottom_line, 1.2)],
            [None, None,
             f'Во избежание срабатывания механизма фиксации плашек в освобожденном положении, спуск '
             f'следует производить без вращения труболовки',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'монтаж ведущей трубы', None,
             f'Произвести монтаж ведущей трубы.\n '
             f'За 2-5 метров до верхнего конца аварийного объекта при наличии циркуляции рекомендуется '
             f'восстановить циркуляцию и промыть скважину тех водой {self.data_well.fluid_work}. При прокачке промывочной '
             f'жидкости спустить '
             f'{self.lar_type_combo} до верхнего конца аварийной колонны.\n'
             f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
             f'инструмента  согласовать с аварийной службой супервайзинга.'],
            [None, None,
             f'Произвести расхаживание аварийной компоновки с постепенным увеличением'
             f' веса до 28т. Дальнейшие '
             f'увеличение нагрузки согласовать с УСРСиСТ. При отрицательных '
             f'результатах произвести освобождение ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 10],
            [None, None,
             f'При положительных результатах расхаживания - демонтаж ведущей трубы. '
             f'Поднять компоновку с доливом тех жидкости в '
             f'объеме {round(self.data_well.current_bottom * 1.25 / 1000, 1)}м3'
             f' удельным весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер', lifting_nkt_norm(self.data_well.current_bottom, 1)],
        ]
        self.data_well.current_bottom = self.bottom_line

        return emergency_nkt_list

    def emergency_pods(self):

        emergency_nkt_list = [
            [None, 'СПО ловильного оборудования',
             f'По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: '
             f'Спустить с замером {self.lar_type_combo}-{self.lar_diameter_line} на '
             f'{self.nkt_str_combo} до Н= {self.emergency_bottom_line}м с замером . ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.emergency_bottom_line, 1.2)],
            [f'ЛАР', None,
             f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов '
             f'инструмента  согласовать с аварийной службой супервайзинга.'],
            [None, None,
             f'Произвести расхаживание аварийной компоновки с постепенным увеличением'
             f' веса до 10т. Дальнейшие '
             f'увеличение нагрузки согласовать с УСРСиСТ. При отрицательных '
             f'результатах произвести освобождение ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 10],
            [None, None,
             f'Поднять компоновку с доливом тех жидкости в объеме '
             f'{round(self.data_well.current_bottom * 0.25 / 1000, 1)}м3'
             f' удельным весом {self.data_well.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер', lifting_nkt_norm(self.data_well.current_bottom, 1)],
        ]
        self.data_well.current_bottom = self.bottom_line

        return emergency_nkt_list

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = EmergencyLarWork()
    window.show()
    sys.exit(app.exec_())
