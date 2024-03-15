from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication,QMainWindow

from main import MyWindow
from work_py.alone_oreration import fluid_change
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from open_pz import CreatePZ

class TabPage_SO_raid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.raid_diametr_label = QLabel("Диаметр райбера", self)
        self.raid_diametr_line = QLineEdit(self)
        self.raid_diametr_line.setText(str(self.raiding_Bit_diam_select(CreatePZ.current_bottom)))
        self.raid_diametr_line.setClearButtonEnabled(True)

        self.raid_select_label = QLabel("компоновка НКТ", self)
        self.raid_select_combo = QComboBox(self)

        self.raid_select_combo.addItems(
            ['райбер в ЭК', 'райбер в ДП'])
        self.raid_select_combo.currentTextChanged.connect(self.update_raid_edit)

        self.downhole_motor_label = QLabel("Забойный двигатель", self)
        self.downhole_motor_line = QLineEdit(self)
        self.downhole_motor_line.setClearButtonEnabled(True)

        if CreatePZ.column_additional is False or (CreatePZ.column_additional and
                                                   CreatePZ.head_column_additional._value < CreatePZ.current_bottom):
            self.raid_select_combo.setCurrentIndex(0)
            if CreatePZ.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
        else:
            if CreatePZ.column_additional_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
            self.raid_select_combo.setCurrentIndex(1)

        self.roof_raid_label = QLabel("Кровля", self)
        self.roof_raid_line = QLineEdit(self)
        self.roof_raid_line.setClearButtonEnabled(True)

        self.sole_raid_label = QLabel("Подошва", self)
        self.sole_raid_line = QLineEdit(self)
        self.sole_raid_line.setClearButtonEnabled(True)

        self.raid_True_label = QLabel("необходимость райбировать интервал", self)
        self.raid_label = QLabel("добавление дополнительного интервала райбирования", self)
        self.raid_True_combo = QComboBox(self)
        self.raid_True_combo.addItems(
            ['нужно', 'не нужно'])

        grid = QGridLayout(self)
        grid.setColumnMinimumWidth(1, 150)

        grid.addWidget(self.raid_select_label, 2, 1)
        grid.addWidget(self.raid_select_combo, 3, 1)

        grid.addWidget(self.raid_diametr_label, 2, 2)
        grid.addWidget(self.raid_diametr_line, 3, 2)

        grid.addWidget(self.downhole_motor_label, 2, 3)
        grid.addWidget(self.downhole_motor_line, 3, 3)

        grid.addWidget(self.raid_label, 4, 1, 2, 2)


        grid.addWidget(self.roof_raid_label, 7, 0)
        grid.addWidget(self.sole_raid_label, 7, 1)
        grid.addWidget(self.raid_True_label, 7, 2)

        grid.addWidget(self.roof_raid_line, 8, 0)
        grid.addWidget(self.sole_raid_line, 8, 1)
        grid.addWidget(self.raid_True_combo, 8, 2, 2, 1)

    def update_raid_edit(self, index):

        if index == 'райбер в ЭК':
            self.raid_diametr_line.setText(str(self.raiding_Bit_diam_select(CreatePZ.current_bottom)))
            if CreatePZ.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
        else:
            self.raid_diametr_line.setText(str(self.raiding_Bit_diam_select(CreatePZ.head_column_additional._value-1)))
            if CreatePZ.column_additional_diametr._value < 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')


    def raiding_Bit_diam_select(self, depth):
        from open_pz import CreatePZ

        raiding_Bit_dict = {
            85: (88, 92),
            91: (92.1, 97),
            95: (97.1, 102),
            103: (102.1, 109),
            106: (109, 115),
            115: (118, 120),
            117: (120.1, 121.9),
            120: (122, 123.9),
            121: (124, 127.9),
            125: (128, 133),
            140: (144, 148),
            144: (148.1, 154),
            146: (154.1, 164),
            160: (166, 176),
            190: (190.6, 203.6),
            204: (215, 221)
        }

        if CreatePZ.column_additional is False or (
                CreatePZ.column_additional is True and depth <= CreatePZ.head_column_additional._value):
            diam_internal_ek = CreatePZ.column_diametr._value - 2 * CreatePZ.column_wall_thickness._value
        else:
            diam_internal_ek = CreatePZ.column_additional_diametr._value - 2 * CreatePZ.column_additional_wall_thickness._value

        for diam, diam_internal_bit in raiding_Bit_dict.items():
            if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
                bit_diametr = diam

        if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
            bit_diametr = 126

        return bit_diametr


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_raid(self), 'Райбер')
class Raid(MyWindow):
    def __init__(self, table_widget, ins_ind, parent=None):
        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "необходимость райбирования"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        self.buttonAddString = QPushButton('Добавить интервалы райбирования')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

    def addRowTable(self):

        roof_raid = self.tabWidget.currentWidget().roof_raid_line.text().replace(',', '.')
        sole_raid = self.tabWidget.currentWidget().sole_raid_line.text().replace(',', '.')
        raid_True_combo = QComboBox(self)
        raid_True_combo.addItems(
            ['нужно', 'не нужно'])
        index_raid_True = self.tabWidget.currentWidget().raid_True_combo.currentIndex()
        raid_True_combo.setCurrentIndex(index_raid_True)

        if not roof_raid or not sole_raid:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if CreatePZ.current_bottom < float(sole_raid):
            msg = QMessageBox.information(self, 'Внимание', 'глубина НЭК ниже искусственного забоя')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_raid))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_raid))
        self.tableWidget.setCellWidget(rows, 2, raid_True_combo)

        self.tableWidget.setSortingEnabled(True)

    def addString(self):

        from work_py.advanted_file import raiding_interval
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()
        self.downhole_motor = self.tabWidget.currentWidget().downhole_motor_line.text()
        raiding_interval = raiding_interval(ryber_key)

        rows = self.tableWidget.rowCount()
        for roof, sole in raiding_interval:

            raid_combo = QComboBox(self)
            raid_combo.addItems(['нужно', 'не нужно'])

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
            self.tableWidget.setCellWidget(rows, 2, raid_combo)
            self.tableWidget.setSortingEnabled(True)

        # except:
        #     mes = QMessageBox.warning(self, 'Ошибка', 'Данные введены не корректно')
        #     self.addString()


    def addWork(self):

        rows = self.tableWidget.rowCount()
        raid_tuple = []
        for row in range(rows):

            roof_raid = self.tableWidget.item(row, 0)
            sole_raid =self.tableWidget.item(row, 1)
            raid_True_combo = self.tableWidget.cellWidget(row, 2)

            if roof_raid and sole_raid:
                roof = int(roof_raid.text())
                sole = int(sole_raid.text())
                raid_True = raid_True_combo.currentText()

                if raid_True == 'нужно':
                    raid_tuple.append((roof, sole))


        raid_list = self.raidingColumn(raid_tuple, self.downhole_motor)

        CreatePZ.pause = False
        self.close()
        return raid_list
    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)
    def raidingColumn(self, raiding_interval_tuple, downhole_motor):
        from work_py.template_work import TemplateKrs
        from work_py.advanted_file import raiding_interval, raid
        from open_pz import CreatePZ

        ryber_diam = self.tabWidget.currentWidget().raid_diametr_line.text()
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()

        nkt_pod = 0
        if CreatePZ.column_additional:
            nkt_pod = '60мм' if CreatePZ.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        nkt_diam = CreatePZ.nkt_diam
        nkt_template = CreatePZ.nkt_template


        ryber_str_EK = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_diametr._value}мм х {CreatePZ.column_wall_thickness._value}мм +'\
                       f' забойный двигатель {downhole_motor} + НКТ{CreatePZ.nkt_diam} 20м + репер '

        ryber_str_DP = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_additional_diametr._value}мм х ' \
                f'{CreatePZ.column_additional_wall_thickness._value}мм + забойный двигатель ' \
                       f'{downhole_motor} + НКТ{nkt_pod} 20м + репер + ' \
                f'НКТ{nkt_pod} {round(CreatePZ.current_bottom - float(CreatePZ.head_column_additional._value))}м'

        rayber_dict = {'райбер в ЭК': ryber_str_EK, 'райбер в ДП': ryber_str_DP}


        ryber_str = rayber_dict[ryber_key]

        if len(raiding_interval_tuple) != 0:
            krovly_raiding = int(raiding_interval_tuple[0][0])
        else:
            krovly_raiding = CreatePZ.perforation_roof

        raiding_interval = raid(raiding_interval_tuple)
        ryber_list = [
            [f'СПО {ryber_str}  на НКТ{nkt_diam} до Н={krovly_raiding}м', None,
             f'Спустить {ryber_str}  на НКТ{nkt_diam} до Н={krovly_raiding}м с замером, '
             f'шаблонированием шаблоном {nkt_template}мм (При СПО первых десяти НКТ на спайдере дополнительно '
             f'устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
             f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО '
             f'ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(krovly_raiding, 1.2)],
            [None, None, f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
                         f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 0.6],
            [f'райбирование ЭК в инт. {raiding_interval}', None,
             f'Произвести райбирование ЭК в инт. {raiding_interval}м с наращиванием, с промывкой и проработкой 5 раз каждого наращивания. '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
             f'до начала работ) Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
             f' представителя заказчика. Допустить до текущего забоя {CreatePZ.current_bottom}м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 8],
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
             f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [f'Промывка уд.весом {CreatePZ.fluid_work[:6]}  в объеме {round(TemplateKrs.well_volume(self)*2,1)}м3',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
             f'в присутствии представителя заказчика в объеме {round(TemplateKrs.well_volume(self)*2,1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', well_volume_norm(TemplateKrs.well_volume(self))],
            [None, None,
             f'Поднять  {ryber_str} на НКТ{nkt_diam}м с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom,1.2)]]

        # print(f' после отрайбирования {[CreatePZ.dict_perforation[plast]["отрайбировано"] for plast in CreatePZ.plast_work]}')
        if len(CreatePZ.plast_work) == 0:
            acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                   'Нужно ли изменять удельный вес?')
            if acid_true_quest == QMessageBox.StandardButton.Yes:
                for row in fluid_change(self):
                    ryber_list.insert(-1, row)
        return ryber_list



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = Raid()
    # window.show()
    sys.exit(app.exec_())


