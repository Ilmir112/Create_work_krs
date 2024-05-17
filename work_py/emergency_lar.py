import logging
import well_data

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

from main import MyWindow
from work_py.emergencyWork import magnet_select, sbt_select
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm


class TabPage_SO_lar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lar_diametr_label = QLabel("Диаметр ловителя", self)
        self.lar_diametr_line = QLineEdit(self)

        self.lar_type_label = QLabel("Тип ловителя", self)
        self.lar_type_combo = QComboBox(self)
        raid_type_list = ['ОВ', 'ВТ', 'метчик', 'колокол']
        self.lar_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка НКТ", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['оборудование в ЭК', 'оборудование в ДП'])

        if well_data.column_additional is False or (well_data.column_additional and
                                                    well_data.head_column_additional._value < well_data.current_bottom):
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        self.emergency_bottom_label = QLabel("аварийный забой", self)
        self.emergency_bottom_line = QLineEdit(self)
        self.emergency_bottom_line.setClearButtonEnabled(True)

        self.bottom_label = QLabel("Забой после ЛАР", self)
        self.bottom_line = QLineEdit(self)
        self.bottom_line.setClearButtonEnabled(True)

        self.nkt_str_label = QLabel("НКТ или СБТ", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ'])
        # self.nkt_select_combo.currentTextChanged.connect(self.update_nkt)

        self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.lar_type_label, 2, 1)
        self.grid.addWidget(self.lar_type_combo, 3, 1)

        self.grid.addWidget(self.lar_diametr_label, 2, 2)
        self.grid.addWidget(self.lar_diametr_line, 3, 2)

        self.grid.addWidget(self.nkt_str_label, 2, 3)
        self.grid.addWidget(self.nkt_str_combo, 3, 3)

        self.grid.addWidget(self.nkt_select_label, 2, 4)
        self.grid.addWidget(self.nkt_select_combo, 3, 4)

        self.grid.addWidget(self.emergency_bottom_label, 7, 1)
        self.grid.addWidget(self.emergency_bottom_line, 8, 1)

        self.grid.addWidget(self.bottom_label, 7, 2)
        self.grid.addWidget(self.bottom_line, 8, 2)

        # self.nkt_select_combo.currentTextChanged.connect(self.update_raid_edit)

        self.nkt_select_combo.setCurrentIndex(1)
        self.bottom_line.setText(f'{well_data.current_bottom}')

        if well_data.column_additional is False or \
                (well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value):
            self.nkt_select_combo.setCurrentIndex(1)
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        if well_data.emergency_well is True:
            self.emergency_bottom_line.setText(f'{well_data.emergency_bottom}')


            # def update_raid_edit(self, index):
    #     if index == 'оборудование в ЭК':
    #         self.lar_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.head_column_additional._value - 10)))
    #     elif index == 'оборудование в ДП':
    #         self.lar_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.current_bottom)))
    #
    # def raiding_Bit_diam_select(self, depth):
    #     try:
    #         raiding_Bit_dict = {
    #             82: (88, 92),
    #             88: (92.1, 96.6),
    #             90: (96.7, 102),
    #             100: (102.1, 115),
    #             112: (118, 120),
    #             113: (120.1, 121.9),
    #             114: (122, 123.9),
    #             118: (124, 144),
    #
    #             136: (144.1, 148),
    #             140: (148.1, 154),
    #             146: (154.1, 221)
    #         }
    #
    #         if well_data.column_additional is False or (
    #                 well_data.column_additional is True and depth <= well_data.head_column_additional._value):
    #             diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
    #         else:
    #             diam_internal_ek = well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value
    #
    #         for diam, diam_internal_bit in raiding_Bit_dict.items():
    #             if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
    #                 bit_diametr = diam
    #         return bit_diametr
    #     except:
    #         pass


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_lar(), 'ловильные работы')


class Emergency_lar(MyWindow):

    def __init__(self, ins_ind, table_widget, parent=None):
        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()

        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def add_work(self):
        nkt_str_combo = self.tabWidget.currentWidget().nkt_str_combo.currentText()
        lar_diametr_line = self.tabWidget.currentWidget().lar_diametr_line.text()
        nkt_key = self.tabWidget.currentWidget().nkt_select_combo.currentText()
        lar_type_combo = self.tabWidget.currentWidget().lar_type_combo.currentText()
        emergency_bottom_line = self.tabWidget.currentWidget().emergency_bottom_line.text().replace(',', '')
        bottom_line = self.tabWidget.currentWidget().bottom_line.text().replace(',', '')
        if bottom_line != '':
            bottom_line = int(float(bottom_line))

        if emergency_bottom_line != '':
            emergency_bottom_line = int(float(emergency_bottom_line))

            if emergency_bottom_line > well_data.current_bottom:
                mes = QMessageBox.warning(self, 'Ошибка',
                                          'Забой ниже глубины текущего забоя')
                return
        else:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'ВВедите аварийный забой')
            return

        if nkt_key == 'оборудование в ЭК' and well_data.column_additional and \
                emergency_bottom_line > well_data.head_column_additional._value:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для доп колонны')
            return
        elif nkt_key == 'оборудование в ДП' and well_data.column_additional and \
                emergency_bottom_line < well_data.head_column_additional._value:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для основной колонны')
            return
        if nkt_str_combo == 'НКТ':
            raid_list = self.emergencyNKT(lar_diametr_line, nkt_key, lar_type_combo, nkt_str_combo,
                     emergency_bottom_line, bottom_line)
        elif nkt_str_combo == 'СБТ':
            raid_list = self.emergence_sbt(lar_diametr_line, nkt_key, lar_type_combo,
                      emergency_bottom_line, bottom_line)
        well_data.current_bottom = bottom_line


        MyWindow.populate_row(self, self.ins_ind, raid_list, self.table_widget)
        well_data.pause = False
        self.close()

    def emergence_sbt(self, lar_diametr_line, nkt_key, lar_type_combo,
                      emergency_bottom_line, bottom_line):

        emergence_sbt = [
            [f'СПО ловильного оборудования ', None,
             f'По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: {lar_type_combo}-{lar_diametr_line} '
             f'(типоразмер согласовать с аварийной службой УСРСиСТ) + удлинитель (L=2м) + БП {sbt_select(self, nkt_key)} '
             f' до глубины нахождения аварийной головы ({emergency_bottom_line}м)\n '
             f'Включение в компоновку ударной компоновки дополнительно согласовать с УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
            [None, None,
             f'Во избежание срабатывания механизма фиксации плашек в освобожденном положении, спуск '
             f'следует производить без вращения труболовки',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'монтаж ведущей трубы', None,
             f'Произвести монтаж ведущей трубы и мех.ротора.\n '
             f'За 2-5 метров до верхнего конца аварийного объекта при наличии циркуляции рекомендуется '
             f'восстановить '
             f'циркуляцию и промыть скважину тех водой {well_data.fluid_work}. При прокачке промывочной '
             f'жидкости спустить '
             f'{lar_type_combo} до верхнего конца аварийной колонны.\n'
             f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
             f'инструмента  согласовать с аварийной службой супервайзинга.'],
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
             f'объеме {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
             f' удельным весом {well_data.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер', liftingNKT_norm(well_data.current_bottom, 1)],
            [None, None,
             f'При необходимости: Сборка и спуск компоновки: кольцевой фрезер с удлинителем '
             f'L= 2,0м + СБТ, до глубины нахождения аварийной "головы". (Компоновку согласовать дополнительно с УСРСиСТ',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', descentNKT_norm(well_data.current_bottom, 1.2)],
            [None, None,
             f'Монтаж монтаж ведущей трубы и мех.ротора. Обуривание аварийной головы на глубины согласованной с '
             f'УСРСиСТ демонтаж мех ротора',
             None, None, None, None, None, None, None,
             'мастер КРС, УСРСиСТ', 10],
            [None, None,
             f'Поднять компоновку с доливом тех жидкости в объеме {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
             f' удельным весом {well_data.fluid_work}.',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', liftingNKT_norm(well_data.current_bottom, 1)],
            [None, None,
             f'По согласованию заказчиком повторить ловильные аварийные работы'
             f' с подбором аварийного оборудования',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', None],
            [None, None,
             f'При отрицательном результате дальнейшие работы по дополнительному плану работ',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', None]]

        well_data.current_bottom = bottom_line
        return emergence_sbt

    def emergencyNKT(self, lar_diametr_line, nkt_key, lar_type_combo, nkt_str_combo,
                     emergency_bottom_line, bottom_line):

        emergencyNKT_list = [
            [None, 'СПО ловильного оборудования',
             f'По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: '
             f'Спустить с замером {lar_type_combo}-{lar_diametr_line} + {magnet_select(self, nkt_str_combo)} на '
             f'{nkt_key} до Н= {emergency_bottom_line}м с замером . ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(emergency_bottom_line, 1.2)],
            [None, 'ЛАР',
             f'Произвести  ловильные работы при представителе заказчика на глубине '
             f'{emergency_bottom_line}м в присутствии представителя заказчика.',
             None, None, None, None, None, None, None,
             'мастер КРС', 5.5],
            [None, None,
             f'Расходить и извлечь аварийный инструмент.',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(emergency_bottom_line, 1.2)]]
        well_data.current_bottom = bottom_line

        return emergencyNKT_list

# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     # app.setStyleSheet()
#     window = Raid()
#     # window.show()
#     sys.exit(app.exec_())
