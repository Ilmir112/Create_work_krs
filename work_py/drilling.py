from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

import well_data
from PyQt5.QtCore import Qt


from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm



class TabPage_SO_drill(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.drill_select_label = QLabel("компоновка НКТ", self)
        self.drill_select_combo = QComboBox(self)

        self.drill_type_label = QLabel("Тип разрушающегося инструмента", self)
        self.drill_type_combo = QComboBox(self)

        drill_type_list = ['долото', 'долото ВС', "фрез торцевой", "фрез кольцевой", "фрез пилотный"]
        self.drill_type_combo.addItems(drill_type_list)

        self.drill_diametr_label = QLabel("Диаметр долото", self)
        self.drill_diametr_line = QLineEdit(self)

        self.drill_select_combo.addItems(
            ['долото в ЭК', 'долото в ДП'])


        self.downhole_motor_label = QLabel("Забойный двигатель", self)
        self.downhole_motor_line = QLineEdit(self)
        self.downhole_motor_line.setClearButtonEnabled(True)

        self.nkt_str_label = QLabel("НКТ или СБТ", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ'])

        if well_data.column_additional is False or (well_data.column_additional and
                                                   well_data.head_column_additional._value >= well_data.current_bottom):
            self.drill_select_combo.setCurrentIndex(0)
            if well_data.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')

            self.drill_diametr_line.setText(str(self.drillingBit_diam_select(well_data.current_bottom)))


        else:
            if well_data.column_additional_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
            self.drill_select_combo.setCurrentIndex(1)
            self.drill_diametr_line.setText(str(self.drillingBit_diam_select(well_data.current_bottom)))

        self.roof_drill_label = QLabel("Кровля", self)
        self.roof_drill_line = QLineEdit(self)
        self.roof_drill_line.setText(f'{well_data.current_bottom}')
        self.roof_drill_line.setClearButtonEnabled(True)

        self.sole_drill_label = QLabel("Подошва", self)
        self.sole_drill_line = QLineEdit(self)
        self.sole_drill_line.setClearButtonEnabled(True)

        self.drill_True_label = QLabel("вид разбуриваемого материала", self)
        self.drill_label = QLabel("добавление поинтервального бурения", self)
        self.drill_cm_combo = QComboBox(self)
        self.bottomType_list = ['ЦМ', 'РПК', 'РПП', 'ВП']
        self.drill_cm_combo.addItems(self.bottomType_list)

        grid = QGridLayout(self)
        grid.setColumnMinimumWidth(1, 150)

        grid.addWidget(self.drill_select_label, 2, 0)
        grid.addWidget(self.drill_select_combo, 3, 0)

        grid.addWidget(self.drill_type_label, 2, 1)
        grid.addWidget(self.drill_cm_combo, 3, 1)

        grid.addWidget(self.drill_diametr_label, 2, 2)
        grid.addWidget(self.drill_diametr_line, 3, 2)

        grid.addWidget(self.nkt_str_label, 2, 3)
        grid.addWidget(self.nkt_str_combo, 3, 3)

        grid.addWidget(self.downhole_motor_label, 2, 4)
        grid.addWidget(self.downhole_motor_line, 3, 4)

        grid.addWidget(self.drill_label, 4, 1, 2, 2)

        grid.addWidget(self.roof_drill_label, 7, 0)
        grid.addWidget(self.sole_drill_label, 7, 1)
        grid.addWidget(self.drill_True_label, 7, 2)

        grid.addWidget(self.roof_drill_line, 8, 0)
        grid.addWidget(self.sole_drill_line, 8, 1)
        grid.addWidget(self.drill_type_combo, 8, 2, 2, 1)


        self.drill_select_combo.currentTextChanged.connect(self.update_drill_edit)

    def update_drill_edit(self, index):

        if index == 'долото в ЭК':
            self.drill_diametr_line.setText(str(self.drillingBit_diam_select(well_data.current_bottom)))
            if well_data.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
        else:
            self.drill_diametr_line.setText(
                str(self.drillingBit_diam_select(well_data.head_column_additional._value - 1)))
            if well_data.column_additional_diametr._value < 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')

    def drillingBit_diam_select(self, depth_landing):



        drillingBit_dict = {
            84: (88, 92),
            90: (92.1, 97),
            94: (97.1, 102),
            102: (102.1, 109),
            105: (109, 115),
            114: (118, 120),
            116: (120.1, 121.9),
            118: (122, 123.9),
            120.6: (124, 127.9),
            124: (128, 133),
            140: (144, 148),
            143: (148.1, 154),
            145: (154.1, 164),
            160: (166, 176),
            190: (190.6, 203.6),
            204: (215, 221)
        }

        if well_data.column_additional is False or (
                well_data.column_additional is True and depth_landing <= well_data.head_column_additional._value):
            diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
        else:
            diam_internal_ek = well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value

        for diam, diam_internal_bit in drillingBit_dict.items():
            if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
                bit_diametr = diam

        return bit_diametr


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_drill(self), 'Бурение')


class Drill_window(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(Drill_window, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "вид разбуриваемого забоя"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddString = QPushButton('Добавить интервалы бурения')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

    def addRowTable(self):

        roof_drill = self.tabWidget.currentWidget().roof_drill_line.text().replace(',', '.')
        sole_drill = self.tabWidget.currentWidget().sole_drill_line.text().replace(',', '.')
        drill_type_combo = QComboBox(self)
        drill_type_combo.addItems(['ЦМ', 'РПК', 'РПП', 'ВП'])
        index_drill_True = self.tabWidget.currentWidget().drill_type_combo.currentIndex()
        drill_type_combo.setCurrentIndex(index_drill_True)

        if not roof_drill or not sole_drill:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        # if well_data.current_bottom < float(sole_drill):
        #     msg = QMessageBox.information(self, 'Внимание', 'глубина НЭК ниже искусственного забоя')
        #     return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_drill))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_drill))
        self.tableWidget.setCellWidget(rows, 2, drill_type_combo)

        self.tableWidget.setSortingEnabled(False)

    def addString(self):

        drill_key = self.tabWidget.currentWidget().drill_select_combo.currentText()
        self.drillingBit_diam = self.tabWidget.currentWidget().drill_diametr_line.text()
        self.downhole_motor = self.tabWidget.currentWidget().downhole_motor_line.text()
        self.nkt_str = self.tabWidget.currentWidget().nkt_str_combo.currentText()
        current_depth = self.tabWidget.currentWidget().sole_drill_line.text()
        if not current_depth:
            msg = QMessageBox.information(self, 'Внимание', 'Не заполнен необходимый забой')
            return

        drilling_interval = [well_data.dict_perforation[plast]["подошва"] for plast in well_data.plast_all]
        drilling_interval.append(int(current_depth))
        if len(well_data.dict_leakiness) != 0:
            leakness_list = [
                well_data.dict_leakiness['нэк']['интервал'][
                    nek][1] for nek in list(well_data.dict_leakiness['нэк']['интервал'].keys())]
            drilling_interval.extend([leakness_list])
        # drilling_interval = list(filter(key = lambda x: x[0] > well_data.current_bottom, drilling_interval))
        print(drilling_interval)
        rows = self.tableWidget.rowCount()
        roof = well_data.current_bottom
        for sole in sorted(drilling_interval):
            drill_combo = QComboBox(self)
            bottomType_list = ['ЦМ', 'РПК', 'РПП', 'ВП']
            drill_combo.addItems(bottomType_list)
            if roof <= int(sole + 4) and int(current_depth) > int(sole + 4):
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole + 4))))
                self.tableWidget.setCellWidget(rows, 2, drill_combo)
                self.tableWidget.setSortingEnabled(False)
                roof = int(sole + 4)
            else:
                self.tableWidget.insertRow(rows)
                self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
                self.tableWidget.setItem(rows, 1, QTableWidgetItem(current_depth))
                self.tableWidget.setCellWidget(rows, 2, drill_combo)

                roof = int(current_depth)

    def add_work(self):
        from main import MyWindow
        self.nkt_str = self.tabWidget.currentWidget().nkt_str_combo.currentText()
        self.drillingBit_diam = self.tabWidget.currentWidget().drill_diametr_line.text()
        self.downhole_motor = self.tabWidget.currentWidget().downhole_motor_line.text()
        self.drill_cm_combo = self.tabWidget.currentWidget().drill_cm_combo.currentText()
        self.drill_type_combo = self.tabWidget.currentWidget().drill_type_combo.currentText()

        rows = self.tableWidget.rowCount()
        drill_tuple = []
        for row in range(rows):

            roof_drill = self.tableWidget.item(row, 0)
            sole_drill = self.tableWidget.item(row, 1)
            drill_type_combo = self.tableWidget.cellWidget(row, 2)

            if roof_drill and sole_drill:
                roof = int(float(roof_drill.text()))
                sole = int(float(sole_drill.text()))
                drill_True = drill_type_combo.currentText()

                drill_tuple.append((sole, drill_True))
                roof = sole

        drill_tuple = sorted(drill_tuple, key=lambda x: x[0])
        if self.nkt_str == 'НКТ':
            drill_list = self.drilling_nkt(drill_tuple, self.drill_type_combo, self.drillingBit_diam, self.downhole_motor)
        elif self.nkt_str == 'СБТ':
            drill_list = self.drilling_sbt(drill_tuple, self.drill_type_combo, self.drillingBit_diam, self.downhole_motor)

        MyWindow.populate_row(self.ins_ind, drill_list, self.table_widget)
        well_data.pause = False
        self.close()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def drilling_nkt(self, drill_tuple, drill_type_combo, drillingBit_diam, downhole_motor):

        currentBottom = well_data.current_bottom

        current_depth = drill_tuple[-1][0]
        bottomType = drill_tuple[-1][1]

        if well_data.column_additional is True:
            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        nkt_diam = well_data.nkt_diam

        if well_data.column_additional is False \
                or (well_data.column_additional is True
                    and well_data.head_column_additional._value >= well_data.current_bottom):
            drilling_str = f'{drill_type_combo}-{drillingBit_diam} для ' \
                           f'ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм +' \
                           f' забойный двигатель {downhole_motor} + НКТ{nkt_diam} 20м + репер '
            drilling_short = f'{drill_type_combo}-{drillingBit_diam} + ' \
                             f'забойный двигатель {downhole_motor}  + НКТ{nkt_diam} 20м + репер '


        elif well_data.column_additional is True:
            drilling_str = f'{drill_type_combo}-{drillingBit_diam} для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм + забойный двигатель ' \
                           f'{downhole_motor} +НКТ{nkt_pod} 20м + репер + ' \
                           f'НКТ{nkt_pod} {round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м'
            drilling_short = f'{drill_type_combo}-{drillingBit_diam}  + забойный двигатель  {downhole_motor} +НКТ{nkt_pod} 20м + ' \
                             f'репер + ' \
                             f'НКТ{nkt_pod} {round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м'

        well_data.drilling_interval.append([well_data.current_bottom, current_depth])

        drilling_list = [
            [f'СПО {drilling_short} до т.з -', None,
             f'Спустить {drilling_str} на НКТ{nkt_diam}м до до текущего забоя с замером, '
             f'шаблонированием шаблоном {well_data.nkt_template}мм\n'
             f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
             f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1.2)],
            [None, None,
             f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
             f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', round(0.14 + 0.17 + 0.08 + 0.48, 1)],
        ]

        if self.check_pressure(current_depth):
            drilling_list.append(
                [f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм', None,
              f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм в присутствии '
              f'представителя заказчика. Составить акт. '
              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
              f'начала работ) \n'
              f'В случае негерметичности произвести РИР по согласованию с заказчиком',
              None, None, None, None, None, None, None,
              'Мастер КРС, УСРСиСТ', 0.67])
        if len(drill_tuple) == 1:
            for drill_sole, bottomType2 in drill_tuple:
                for row in self.reply_drilling(drill_sole, bottomType2, drilling_str, nkt_diam):
                    drilling_list.append(row)

        else:
            for drill_sole, bottomType2 in drill_tuple:
                # print(drill_sole, self.check_pressure(drill_sole))
                if self.check_pressure(drill_sole) is True:
                    for row in self.reply_drilling(drill_sole, bottomType2, drilling_str, nkt_diam):
                        drilling_list.append(row)



        drilling_list_end = [
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
             f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [None, None,
             f'Поднять  {drilling_str} на НКТ{nkt_diam} с глубины {well_data.current_bottom}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.4 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.3)]
        ]

        drilling_list.extend(drilling_list_end)

        well_data.current_bottom = current_depth

        if bottomType == "РПК" or bottomType == "РПП":
            well_data.current_bottom = currentBottom
            drilling_list.append([f'Завоз СБТ', None,
                                  f'В случае возможности завоза тяжелого оборудования и установки УПА-60 (АПР60/80), '
                                  f'по согласованию с Заказчиком нормализацию выполнить по следующему пункту',
                                  None, None, None, None, None, None, None,
                                  'Мастер КРС, УСРСиСТ', None])

            for row in self.drilling_sbt(self, drill_tuple, drill_type_combo, drillingBit_diam):
                drilling_list.append(row)

        return drilling_list

    def reply_drilling(self, current_depth, bottomtype, drilling_str, nkt_diam):

        from work_py.alone_oreration import well_volume

        drilling_true_quest_list = [
            [f'Произвести нормализацию {bottomtype} до Н -{current_depth}м', None,
             f'Произвести нормализацию {bottomtype} до глубины {current_depth}м с наращиванием, промывкой '
             f'тех жидкостью уд.весом {well_data.fluid_work}. '
             f'Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
             f' представителя заказчика.',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 8, ],
            [f'Промыть  {well_data.fluid_work} в объеме '
             f'{round(well_volume(self, well_data.current_bottom) * 2, 1)}м3', None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  '
             f'в присутствии представителя заказчика в объеме '
             f'{round(well_volume(self, well_data.current_bottom) * 2, 1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 1.5],
        ]

        if self.check_pressure(current_depth):
            drilling_true_quest_list.append(
                [f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм в '
                 f'присутствии представителя заказчика. Составить акт. '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с '
                 f'подтверждением за 2 часа до начала работ) \n'
                 f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, УСРСиСТ', 0.67]
            )
        well_data.current_bottom = current_depth
        return drilling_true_quest_list

    def drilling_sbt(self, drill_tuple, drill_type_combo, drillingBit_diam, downhole_motor):


        currentBottom = well_data.current_bottom

        current_depth = drill_tuple[-1][0]

        nkt_pod = "2'3/8"
        nkt_diam = "2'7/8" if well_data.column_diametr._value > 110 else "2'3/8"

        if well_data.column_additional is False or (
                well_data.column_additional is True and well_data.head_column_additional._value >= current_depth):
            drilling_str = f'{drill_type_combo}-{drillingBit_diam} для ЭК {well_data.column_diametr._value}мм х ' \
                           f'{well_data.column_wall_thickness._value}мм '
            drilling_short = f'{drill_type_combo}-{drillingBit_diam} для ЭК {well_data.column_diametr._value}мм х ' \
                             f'{well_data.column_wall_thickness._value}мм '
            sbt_lenght = f'СБТ {nkt_diam} - {int(current_depth + 100)}м'

        elif well_data.column_additional is True:
            drilling_str = f'{drill_type_combo}-{drillingBit_diam} для ЭК ' \
                           f'{well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм + СБТ{nkt_pod} ' \
                           f'{well_data.current_bottom - well_data.head_column_additional._value}м'
            drilling_short = f'{drill_type_combo}-{drillingBit_diam}  + СБТ{nkt_pod} ' \
                             f'{well_data.current_bottom - well_data.head_column_additional._value}м'
            sbt_lenght = f'СБТ {nkt_diam} - {well_data.head_column_additional._value}м и СБТ {nkt_pod}' \
                         f' {int(current_depth + 100)-well_data.head_column_additional._value}м'

        well_data.drilling_interval.append([well_data.current_bottom, current_depth])

        drilling_list = [
            [f'Завезти на скважину {sbt_lenght}', None,
                 f'Завезти на скважину СБТ {sbt_lenght} – Укладка труб на стеллажи.',
                 None, None, None, None, None, None, None,
                 'Мастер', None],
            [f'СПО {drilling_short} на СБТ {nkt_diam} до Н= {well_data.current_bottom - 30}', None,
                 f'Спустить {drilling_str}  на СБТ {nkt_diam} до Н= {well_data.current_bottom - 30}м с замером, '
                 f' (При СПО первых десяти СБТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
                 f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., '
                 f'составить акт. СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ '
                 f'СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
                 f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(well_data.current_bottom, 1.1)],
            [f'монтаж мех.ротора', None,
                 f'Произвести монтаж мех.ротора. Собрать промывочное оборудование: вертлюг, ведущая труба (установить '
                 f'вставной фильтр под ведущей трубой), '
                 f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, УСРСиСТ', round(0.14 + 0.17 + 0.08 + 0.48 + 1.1, 1)],
            ]


        if self.check_pressure(current_depth) == 0:
            drilling_list.append(
                [f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Опрессовать ЭК и ЦМ на Р={well_data.max_admissible_pressure._value}атм в присутствии представителя '
                 f'заказчика. Составить акт. '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
                 f'начала работ) \n'
                 f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, УСРСиСТ', 0.67])

        well_data.current_bottom = current_depth

        for drill_sole, bottomType2 in drill_tuple:
            # print(drill_sole, self.check_pressure(drill_sole))
            if self.check_pressure(drill_sole) is True:
                for row in self.reply_drilling(drill_sole, bottomType2, drilling_str, nkt_diam):
                    drilling_list.append(row)

        drilling_list_end = [
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [f'д/ж мех ротора',
                None,
                f'Демонтировать мех ротор',
                None, None, None, None, None, None, None,
                'мастер КРС, предст. заказчика', 0.77],
            [None, None,
             f'Поднять  {drilling_str} на СБТ с глубины {well_data.current_bottom}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.4 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.3)]
        ]
        drilling_list.extend(drilling_list_end)
        return drilling_list

    def check_pressure(self, depth):


        check_True = True

        for plast in well_data.plast_all:
            if well_data.dict_perforation[plast]['отключение'] is False:
                for interval in well_data.dict_perforation[plast]['интервал']:
                    if depth > interval[0]:
                        check_True = False

        if well_data.leakiness is True:

            for nek in well_data.dict_leakiness['НЭК']['интервал']:
                # print(well_data.dict_leakiness)
                if well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение'] is False:
                    if depth > nek[0]:
                        check_True = False
        return check_True

    def frezer_ports(self):

        from work_py.alone_oreration import well_volume
        from work_py.alone_oreration import kot_work

        max_port = max([well_data.dict_perforation[plast]['подошва'] for plast in well_data.plast_work])
        min_port = max([well_data.dict_perforation[plast]['кровля'] for plast in well_data.plast_work])

        current_depth, ok = QInputDialog.getInt(None, 'Нормализация забоя',
                                                'Введите глубину необходимого забоя при нормализации',
                                                int(max_port-2), 0,
                                                int(well_data.bottomhole_artificial._value + 500))

        kot_question = QMessageBox.question(self, 'КОТ', 'Нужно ли произвести СПО '
                                                         'обратных клапанов перед фрезом?')

        if kot_question == QMessageBox.StandardButton.Yes:
            kot_list = kot_work(self, min_port)[::-1]



        drillingBit_diam = TabPage_SO_drill.drillingBit_diam_select(self, current_depth)

        drillingBit_diam, ok = QInputDialog.getDouble(None, 'Диаметр фреза',
                                                'Введите диаметр фреза', drillingBit_diam, 50, 210, 1)
        nkt_pod = "2' 3/8"

        nkt_diam = ''.join(["2 7/8" if well_data.column_diametr._value > 110 else "2 3/8"])

        if well_data.column_additional is False or (
                well_data.column_additional is True and well_data.head_column_additional._value >= well_data.current_bottom):
            drilling_str = f'торцевой фрезер -{drillingBit_diam} + СБТ + магнит колонный  2⅜ БТ (П) '
            drilling_short = f'торцевой фрезер -{drillingBit_diam} + СБТ + магнит колонный  2⅜ БТ (П) '


        elif well_data.column_additional is True:
            drilling_str = f'торцевой фрезер -{drillingBit_diam} + СБТ + магнит колонный  2⅜ БТ (П) + ' \
                           f'СБТ{nkt_pod} ' \
                           f'{round(current_depth - well_data.head_column_additional._value, 1)}м'
            drilling_short = f'торцевой фрезер -{drillingBit_diam} + СБТ + магнит колонный  2⅜ БТ (П) + ' \
                             f'СБТ{nkt_pod} ' \
                             f'{round(current_depth - well_data.head_column_additional._value, 1)}м'

        well_data.drilling_interval.append([well_data.current_bottom, current_depth])
        drilling_list = [[f'Завоз на скважину СБТ', None,
         f'Завоз на скважину СБТ – Укладка труб на стеллажи.',
         None, None, None, None, None, None, None,
         'Мастер', None],
            [f'СПО {drilling_short} на СБТ{nkt_diam} до Н= {well_data.perforation_roof - 30}', None,
             f'Спустить {drilling_str}  на СБТ{nkt_diam} до Н= {well_data.perforation_roof - 30}м с замером, '
             f' (При СПО первых десяти СБТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
             f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1.1)],
            [f'монтаж мех.ротора', None,
             f'Произвести монтаж мех.ротора. Собрать промывочное оборудование: вертлюг, ведущая труба (установить '
             f'вставной фильтр под ведущей трубой), '
             f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', round(0.14 + 0.17 + 0.08 + 0.48 + 1.1, 1)],
            [f'нормализацию до Н= {current_depth}м', None,
             f'Произвести фрезерование муфт ГРП  с гл.{well_data.perforation_roof}м до '
             f'гл.{well_data.perforation_sole}м  до первого порта с периодической обратной промывкой, с проработкой э/к в'
             f' интервале {well_data.perforation_roof}-{well_data.perforation_sole}м (режим работы 60-80 об/мин, расход '
             f'6-10 литров, нагрузка на фрезерующий инструмент до 3-х тонн. Приподнимаем инструмент после 15-20 минут '
             f'работы).',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 20, ],
            [f'При отсутствии циркуляции заказчка блок пачки', None,
             f'При отсутствии циркуляции или потери циркуляции согласовать заказчку блок пачки по дополнительному плану',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ  И ДОЛОТА);'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ)) \n'
             f'ПРИПОДНИМАЕМ ИНСТРУМЕНТ ПОСЛЕ 15-20 МИНУТ РАБОТЫ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [f'Промыть  {well_data.fluid_work}  '
             f'в объеме {round(well_volume(self, well_data.current_bottom) * 2, 1)}м3', None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  '
             f'в присутствии представителя заказчика в объеме {round(well_volume(self, well_data.current_bottom) * 2, 1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', well_volume_norm(well_volume(self, well_data.current_bottom))],
            [None, None,
             f'Поднять  {drilling_str} на СБТ {nkt_diam} с глубины {well_data.current_bottom}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.4 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.3)],
            [None, None,
             f'В случае превышении норм времени на фрезерование портов увеличение продолжительности дополнительно '
             f'согласовать с супервайзерской службой с составление акта на фактически затраченное время. Или согласовать '
             f'смену вооружения и повторить работы',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.3)],
            [None, None,
             f'При посадке фреза на глубине выше планируемого порта по согласованию с УСРСиСТ произвести следующие работы:',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.3)]
        ]
        for row in kot_list:
            drilling_list.insert(0, row)

        for row in kot_work(self, current_depth):
            drilling_list.append(row)

        return drilling_list
