import logging
import well_data

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

from main import MyMainWindow
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm




class TabPage_SO_print(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.print_diametr_label = QLabel("Диаметр печати", self)
        self.print_diametr_line = QLineEdit(self)

        self.print_type_label = QLabel("Тип печати", self)
        self.print_type_combo = QComboBox(self)
        raid_type_list = ['торцевую печать', 'конусную печать', 'свинцовую печать', 'гудроновую печать']
        self.print_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка НКТ", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['печать в ЭК', 'печать в ДП'])

        if well_data.column_additional is False or (well_data.column_additional and
                                                    well_data.head_column_additional._value < well_data.current_bottom):
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            
            self.nkt_select_combo.setCurrentIndex(1)

        self.emergency_bottom_label = QLabel("аварийный забой", self)
        self.emergency_bottom_line = QLineEdit(self)
        self.emergency_bottom_line.setClearButtonEnabled(True)        

        self.nkt_str_label = QLabel("НКТ или СБТ", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ'])
        # self.nkt_select_combo.currentTextChanged.connect(self.update_nkt)

        self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.print_type_label, 2, 1)
        self.grid.addWidget(self.print_type_combo, 3, 1)

        self.grid.addWidget(self.print_diametr_label, 2, 2)
        self.grid.addWidget(self.print_diametr_line, 3, 2)

        self.grid.addWidget(self.nkt_str_label, 2, 3)
        self.grid.addWidget(self.nkt_str_combo, 3, 3)

        self.grid.addWidget(self.nkt_select_label, 2, 4)
        self.grid.addWidget(self.nkt_select_combo, 3, 4)

        self.grid.addWidget(self.emergency_bottom_label, 7, 1, 1, 4)
        self.grid.addWidget(self.emergency_bottom_line, 8, 1, 1, 4)

        self.nkt_select_combo.currentTextChanged.connect(self.update_raid_edit)
        
        self.nkt_select_combo.setCurrentIndex(1)

        if well_data.column_additional is False or \
                (well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value):
            self.nkt_select_combo.setCurrentIndex(1)
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        if well_data.emergency_well is True:
            self.emergency_bottom_line.setText(f'{well_data.emergency_bottom}')
    
    def update_raid_edit(self, index):
        if index == 'печать в ЭК':
            self.print_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.head_column_additional._value - 10)))
        elif index == 'печать в ДП':
            self.print_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.current_bottom)))
                
    def raiding_Bit_diam_select(self, depth):
        try:
            raiding_Bit_dict = {
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
    
            if well_data.column_additional is False or (
                    well_data.column_additional is True and depth <= well_data.head_column_additional._value):
                diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
            else:
                diam_internal_ek = well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value
    
            for diam, diam_internal_bit in raiding_Bit_dict.items():
                if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
                    bit_diametr = diam
            return bit_diametr
        except:
            pass
       

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_print(), 'Работа печатью')


class Emergency_print(MyMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(Emergency_print, self).__init__()
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
        print_diametr_line = self.tabWidget.currentWidget().print_diametr_line.text()
        nkt_key = self.tabWidget.currentWidget().nkt_select_combo.currentText()
        print_type_combo = self.tabWidget.currentWidget().print_type_combo.currentText()
        emergency_bottom_line = self.tabWidget.currentWidget().emergency_bottom_line.text().replace(',', '')

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

        if nkt_str_combo == 'печать в ЭК' and well_data.column_additional and \
                emergency_bottom_line > well_data.head_column_additional._value:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка печати для доп колонны')
            return
        elif nkt_str_combo == 'печать в ДП' and well_data.column_additional and \
                emergency_bottom_line < well_data.head_column_additional._value:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для основной колонны')
            return

        raid_list = self.emergencyNKT(print_diametr_line, nkt_str_combo, print_type_combo, nkt_key,
                                      emergency_bottom_line)

        self.populate_row(self.ins_ind, raid_list, self.table_widget)
        well_data.pause = False
        self.close()



    def emergencyNKT(self, print_diametr_line, nkt_str_combo, print_type_combo, nkt_key,
                                      emergency_bottom_line):
        from work_py.emergencyWork import magnet_select

        emergencyNKT_list = [[f'СПо печати до Н={emergency_bottom_line}м', None,
                              f'Спустить с замером {print_type_combo}-{print_diametr_line}мм на '
                              f'{magnet_select(self, nkt_str_combo)}  на {nkt_str_combo} до '
                              f'Н={emergency_bottom_line}м '
                              f'(Аварийная голова) с замером.'
                              f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
                              None, None, None, None, None, None, None,
                              'мастер КРС', descentNKT_norm(emergency_bottom_line, 1)],
                             [None, None,
                              f'Произвести работу печатью на глубине {emergency_bottom_line}м с обратной промывкой с '
                              f'разгрузкой до 5т.',
                              None, None, None, None, None, None, None,
                              'мастер КРС', 2.5],
                             [None, None,
                              f'Поднять {magnet_select(self, nkt_str_combo)} с доливом тех жидкости в объеме '
                              f'{round(well_data.current_bottom * 1.25 / 1000, 1)}м3 удельным весом {well_data.fluid_work}.',
                              None, None, None, None, None, None, None,
                              'Мастер', liftingNKT_norm(emergency_bottom_line, 1.2)],
                             [None, None,
                              f'По результату ревизии печати, согласовать с ПТО  и УСРСиСТ дальнейшие работы',
                              None, None, None, None, None, None, None,
                              'мастер КРС', None],
                             ]

        return emergencyNKT_list




# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     # app.setStyleSheet()
#     window = Raid()
#     # window.show()
#     sys.exit(app.exec_())
