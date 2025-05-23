import logging
import data_list

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

from main import MyMainWindow
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm, well_volume_norm


class TabPageSoMagnit(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.print_diameter_label = QLabel("Диаметр магнит", self)
        self.print_diameter_line = QLineEdit(self)

        self.print_type_label = QLabel("Тип магнита", self)
        self.print_type_combo = QComboBox(self)
        raid_type_list = ['магнит']
        self.print_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка НКТ", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['магнит в ЭК', 'магнит в ДП', 'Силами ККТ или ГИРС'])
        # self.nkt_select_combo.setCurrentIndex(2)

        if self.data_well.column_additional is False or (self.data_well.column_additional and
                                                         self.data_well.head_column_additional.get_value <
                                                         self.data_well.current_bottom):
            self.nkt_select_combo.setCurrentIndex(0)
        elif self.data_well.max_angle < 50:
            self.nkt_select_combo.setCurrentIndex(2)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        self.emergency_bottom_label = QLabel("аварийный забой", self)
        self.emergency_bottom_line = QLineEdit(self)
        self.emergency_bottom_line.setClearButtonEnabled(True)
        self.emergency_bottom_line.setText(f'{self.data_well.current_bottom}')

        self.nkt_str_label = QLabel("НКТ или СБТ", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ'])
        # self.nkt_select_combo.currentTextChanged.connect(self.update_nkt)

        # self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.print_type_label, 2, 1)
        self.grid.addWidget(self.print_type_combo, 3, 1)

        self.grid.addWidget(self.print_diameter_label, 2, 2)
        self.grid.addWidget(self.print_diameter_line, 3, 2)

        self.grid.addWidget(self.nkt_str_label, 2, 3)
        self.grid.addWidget(self.nkt_str_combo, 3, 3)

        self.grid.addWidget(self.nkt_select_label, 2, 4)
        self.grid.addWidget(self.nkt_select_combo, 3, 4)

        self.grid.addWidget(self.emergency_bottom_label, 7, 1, 1, 4)
        self.grid.addWidget(self.emergency_bottom_line, 8, 1, 1, 4)

        self.nkt_select_combo.currentTextChanged.connect(self.update_raid_edit)

        self.nkt_select_combo.setCurrentIndex(1)

        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and self.data_well.current_bottom <
                 self.data_well.head_column_additional.get_value):
            self.nkt_select_combo.setCurrentIndex(1)
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

    def update_raid_edit(self, index):
        if index == 'магнит в ЭК':
            self.print_diameter_line.setText(
                str(self.raiding_bit_diam_select(self.data_well.head_column_additional.get_value - 10)))
        elif index == 'магнит в ДП':
            self.print_diameter_line.setText(str(self.raiding_bit_diam_select(self.data_well.current_bottom)))

    def raiding_bit_diam_select(self, depth):
        try:
            raiding_bit_dict = {
                82: (88, 92),
                88: (92.1, 96.6),
                90: (96.7, 102),
                100: (102.1, 115),
                112: (118, 120),
                113: (120.1, 121.9),
                114: (122, 123.9),
                118: (124, 144),

                136: (144.1, 148),
                140: (148.1, 154),
                146: (154.1, 221)
            }

            if self.data_well.column_additional is False or (
                    self.data_well.column_additional is True and depth <= self.data_well.head_column_additional.get_value):
                diam_internal_ek = self.data_well.column_diameter.get_value - 2 * self.data_well.column_wall_thickness.get_value
            else:
                diam_internal_ek = self.data_well.column_additional_diameter.get_value - 2 * self.data_well.column_additional_wall_thickness.get_value

            for diam, diam_internal_bit in raiding_bit_dict.items():
                if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
                    bit_diameter = diam
            return bit_diameter
        except:
            pass


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoMagnit(parent), 'Работа магнитом')


class EmergencyMagnit(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)
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
        self.close_modal_forcefully()
        event.accept()  # Принимаем событие закрытия

    def add_work(self):
        nkt_str_combo = self.tab_widget.currentWidget().nkt_str_combo.currentText()
        print_diameter_line = self.tab_widget.currentWidget().print_diameter_line.text()
        nkt_key = self.tab_widget.currentWidget().nkt_select_combo.currentText()
        if nkt_key == 'Силами ККТ или ГИРС':
            mes = QMessageBox.question(self, 'ПРЕДУПРЕЖДЕНИЕ',
                                       'Использование магнита с ККТ или ГИС можно только при полётах '
                                       'оборудования без кабеля и штанг , после фрезерования аварийной головы и т.д, '
                                       'а также при отсутствии рисков наличия предметов  и сужений, АСПО,'
                                       ' гипсоотложения, которые могут привезти к заклиниванию оборудования ')
            if mes == QMessageBox.StandardButton.No:
                return
        print_type_combo = self.tab_widget.currentWidget().print_type_combo.currentText()
        emergency_bottom_line = self.tab_widget.currentWidget().emergency_bottom_line.text().replace(',', '')
        nkt_select_combo = self.tab_widget.currentWidget().nkt_select_combo.currentText()

        if emergency_bottom_line != '':
            emergency_bottom_line = int(float(emergency_bottom_line))

        if emergency_bottom_line > self.data_well.current_bottom:
            QMessageBox.warning(self, 'Ошибка',
                                'Забой ниже глубины текущего забоя')
            return

        if nkt_select_combo == 'магнит в ЭК' and self.data_well.column_additional and \
                emergency_bottom_line > self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                'Не корректно выбрана компоновка печати для доп колонны')
            return
        elif nkt_select_combo == 'магнит в ДП' and self.data_well.column_additional and \
                emergency_bottom_line < self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                'Не корректно выбрана компоновка для основной колонны')
            return

        raid_list = self.emergency_magnit(print_diameter_line, nkt_str_combo, print_type_combo, nkt_key,
                                          emergency_bottom_line)

        self.populate_row(self.insert_index, raid_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def emergency_magnit(self, print_diameter_line, nkt_str_combo, print_type_combo, nkt_key,
                         emergency_bottom_line):
        from work_py.emergencyWork import magnet_select
        if nkt_key == 'Силами ККТ или ГИРС':
            magnet_list = [
                [None, None, f'Вызвать геофизическую партию или подрядчика по ККТ. '
                             f'Заявку оформить за 16 часов сутки через '
                             f'геологическую службу {data_list.contractor}. '
                             f'Произвести монтаж ПАРТИИ ГИС согласно утвержденной главным инженером от'
                             f' {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}. '
                             f'Предварительно нужно заявить вставку №6',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.25],
                [None, None, f'Произвести работу магнитом на глубине {emergency_bottom_line}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 12]]
        else:

            magnet_list = [
                [f'СПО {print_type_combo}-{print_diameter_line}  до '
                 f'глубины {emergency_bottom_line}м',
                 None,
                 f'Спустить {print_type_combo}-{print_diameter_line}  '
                 f'{magnet_select(self, nkt_str_combo)} на '
                 f'{nkt_str_combo}{self.data_well.nkt_diam}мм до '
                 f'глубины {emergency_bottom_line}м с замером, шаблонированием '
                 f'шаблоном {self.data_well.nkt_template}мм.  \n'
                 f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1)],
                [None, None,
                 f'Произвести работу магнитом на глубине {emergency_bottom_line}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.5],
                [None, None,
                 f'Поднять {magnet_select(self, nkt_str_combo)} на {nkt_key}{self.data_well.nkt_diam}мм с глубины '
                 f'{emergency_bottom_line}м '
                 f'с доливом скважины в объеме {round(emergency_bottom_line * 1.12 / 1000, 1)}м3 тех. жидкостью '
                 f'уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', lifting_nkt_norm(emergency_bottom_line, 1)],
                [None, None,
                 f'ПО результатам ревизии СПО магнита повторить',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]
            ]
        return magnet_list

# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     # app.setStyleSheet()
#     window = Raid()
#     # window.show()
#     sys.exit(app.exec_())
