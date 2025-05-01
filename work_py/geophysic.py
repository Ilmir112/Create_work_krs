from PyQt5 import QtWidgets
from PyQt5.Qt import *

import data_list
from main import MyMainWindow
from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion


class TabPageSo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.labelType = QLabel("Кровля записи", self)
        self.lineedit_type = QLineEdit(self)
        self.lineedit_type.setClearButtonEnabled(True)

        self.labelType2 = QLabel("Подошва записи", self)
        self.lineedit_type2 = QLineEdit(self)
        self.lineedit_type2.setClearButtonEnabled(True)

        self.labelGeores = QLabel("вид исследования", self)
        self.ComboBoxGeophygist = QComboBox(self)
        self.ComboBoxGeophygist.addItems(
            ['Гироскоп', 'АКЦ', 'АКЦ + СГДТ', 'СГДТ', 'ИНГК', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ'])
        self.ComboBoxGeophygist.currentTextChanged.connect(self.geophygist_data)

        self.labeldop_information = QLabel("Доп информация", self)
        self.lineEditdop_information = QLineEdit(self)
        self.lineEditdop_information.setClearButtonEnabled(True)

        # grid = QGridLayout(self)
        self.grid.addWidget(self.labelGeores, 0, 0)
        self.grid.addWidget(self.labelType, 0, 1)
        self.grid.addWidget(self.labelType2, 0, 2)
        self.grid.addWidget(self.labeldop_information, 0, 3)

        self.grid.addWidget(self.ComboBoxGeophygist, 1, 0)
        self.grid.addWidget(self.lineedit_type, 1, 1)
        self.grid.addWidget(self.lineedit_type2, 1, 2)
        self.grid.addWidget(self.lineEditdop_information, 1, 3)

    def geophygist_data(self):
        if self.ComboBoxGeophygist.currentText() in ['Гироскоп', 'АКЦ', 'ЭМДС', 'ПТС', 'РК', 'ГК и ЛМ']:
            self.lineedit_type.setText('0')
            self.lineedit_type2.setText(f'{self.data_well.current_bottom}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSo(parent), 'Геофизические исследований')


class GeophysicWindow(WindowUnion):

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)
        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.tableWidget = QTableWidget(0, 4)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Геофизические исследования", "Кровля записи", "Подошва записи", "доп информация"])
        for i in range(4):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def geophysicalSelect(self, geophysic):

        return geophysic

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def add_row_table(self):

        edit_type = self.tab_widget.currentWidget().lineedit_type.text().replace(',', '.')
        edit_type2 = self.tab_widget.currentWidget().lineedit_type2.text().replace(',', '.')
        researchGis = self.geophysicalSelect(str(self.tab_widget.currentWidget().ComboBoxGeophygist.currentText()))

        dop_information = self.tab_widget.currentWidget().lineEditdop_information.text()
        if not edit_type or not edit_type2 or not researchGis:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if self.data_well.current_bottom < float(edit_type2):
            QMessageBox.information(self, 'Внимание', 'глубина исследований ниже текущего забоя')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(researchGis))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(edit_type))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(edit_type2))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(dop_information))
        self.tableWidget.setSortingEnabled(True)

    def geophysic_sel(self, geophysic, edit_type, edit_type2):
        research, research_short = '', ''

        if geophysic == 'АКЦ':
            research = f'ЗАДАЧА 2.7.1 Определение состояния цементного камня (АКЦ, АК сканирование) в ' \
                       f'интервале {edit_type}-{edit_type2}м. '
            research_short = f'АКЦ в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'СГДТ':
            research = f'ЗАДАЧА 2.7.2 Определение плотности, дефектов цементного камня, эксцентриситета колонны ' \
                       f'(СГДТ) в интервале {edit_type}-{edit_type2}м.'
            research_short = f'СГДТ в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'АКЦ + СГДТ':
            research = f'ЗАДАЧА 2.7.3  Определение состояния цементного камня (АКЦ, АК сканирование). в интервале ' \
                       f'{edit_type}-{edit_type2}м,' \
                       f'Определение плотности, дефектов цементного камня, эксцентриситета колонны (СГДТ) в ' \
                       f'интервале 0 - {self.data_well.perforation_roof - 20}м '
            research_short = f'АКЦ в интервале {edit_type}-{edit_type2}м.' \
                             f'СГДТ в интервале 0 - {self.data_well.perforation_roof - 20}'

        elif geophysic == 'ИНГК':
            research = f'ЗАДАЧА 2.4.3 Определение текущей нефтенасыщенности по данным интегрального импульсного ' \
                       f'нейтронного' \
                       f'каротажа пласта  в интервале {edit_type}-{edit_type2}м. '
            research_short = f'ИНГК в интервале {edit_type}-{edit_type2}м.'

        elif geophysic == 'Гироскоп':
            research = f'ЗАДАЧА 2.7.4. Определение траектории ствола скважины гироскопическим инклинометром ' \
                       f'в интервале {edit_type}-{edit_type2}м. '
            research_short = f'Гироскоп в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'РК':
            research = f'ЗАДАЧА 2.4.1 РК в интервале {edit_type}-{edit_type2}м. '
            research_short = f'РК в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'ЭМДС':
            research = f' ЗАДАЧА 2.6.11. Определение интервалов дефектов и толщины колонн и НКТ с ' \
                       f'использованием электромагнитной дефектоскопии  и толщинометрии в ' \
                       f'интервале {edit_type}-{edit_type2}м.'
            research_short = f'ЭМДС в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'ПТС':
            research = f'ЗАДАЧА 2.6.10 Профилимер в интервале {edit_type}-{edit_type2}м.'
            research_short = f'ПТС в интервале {edit_type}-{edit_type2}м.'

        elif geophysic == 'ГК и ЛМ':
            research = f'Произвести записи ГК и ЛМ интервале {edit_type}-{edit_type2}м. '
            research_short = f'ГК и ЛМ в интервале {edit_type}-{edit_type2}м.'
        elif geophysic == 'прихватоопределитель':
            research = f'Произвести прихватоопределитель интервале {edit_type}-{edit_type2}м. '
            research_short = f'ГК и ЛМ в интервале {edit_type}-{edit_type2}м.'

        return research, research_short
    def check_if_none_gis(self, value):

        if isinstance(value, int) or isinstance(value, float):
            return int(value)

        elif str(value).replace('.', '').replace(',', '').isdigit():
            if str(round(float(value.replace(',', '.')), 1))[-1] == 0:
                return int(float(value.replace(',', '.')))
        else:
            return 0

    def add_work(self):

        rows = self.tableWidget.rowCount()
        cable_type_text = ''
        angle_text = ''
        
        if self.data_well.angle_data:
            if self.data_well.max_angle.get_value > 45:
                max_depth_pvr = max([float(self.tableWidget.item(row, 2).text()) for row in range(rows)])

                tuple_angle = self.calculate_angle(max_depth_pvr, self.data_well.angle_data)
                if tuple_angle:
                    if float(tuple_angle[0]) <= max_depth_pvr:
                        cable_type_text = ' СОГЛАСОВАТЬ ЖЕСТКИЙ КАБЕЛЬ'
                        angle_text = tuple_angle[2]
        
        geophysical_research = [
            [" ", None,
             f'Вызвать геофизическую партию{cable_type_text}. Заявку оформить за 16 часов сутки через '
             f'РИТС {data_list.contractor}". '
             f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
             f'Произвести  монтаж ГИС согласно схемы схема №11 утвержденной главным инженером '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
             None, None, None, None, None, None, None,
             'Мастер КРС', ' '],
            [' ', None,
             f'Долить скважину до устья тех жидкостью уд.весом {self.data_well.fluid_work} .Установить ПВО по'
             f' схеме  №11 утвержденной '
             f'главным инженером {data_list.contractor} '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. Опрессовать  плашки  ПВО '
             f'(на давление опрессовки ЭК, но '
             f'не ниже максимального ожидаемого давления на устье) {self.data_well.max_admissible_pressure.get_value}атм, '
             f'по невозможности на давление поглощения, но '
             f'не менее 30атм в течении 30мин (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ). \n {angle_text}',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2]
        ]

        for row in range(rows):
            research_gis_list = []
            item = self.tableWidget.item(row, 0)
            edit1 = self.tableWidget.item(row, 1)
            edit2 = self.tableWidget.item(row, 2)
            if item and edit1 and edit2:
                value = item.text()
                edit1_1 = edit1.text()
                edit2_1 = edit2.text()
                geo_sel = self.geophysic_sel(value, edit1_1, edit2_1)
                # print(f'геофои {geo_sel}')
                research_gis_list.extend([geo_sel[1], None, geo_sel[0], None, None, None, None, None, None, None,
                                         'подряд по ГИС', 4])

            if len(research_gis_list) == 0:
                QMessageBox.critical(self, 'Ошибка', 'Исследования не добавлены')
                return

            geophysical_research.append(research_gis_list)
            # print(geophysical_research)

        ori = QMessageBox.question(self, 'ОРИ', 'Нужна ли интерпретация?')
        if ori == QMessageBox.StandardButton.Yes:
            geophysical_research.append([f'ОРИ', None,
                                        f'Интерпретация данных ГИС, согласовать с ПТО и Ведущим инженером ЦДНГ опрессовку фНКТ ',
                                        None, None, None, None, None, None, None,
                                        'Мастер КРС, подрядчик по ГИС', 8])

        if geophysical_research:
            self.populate_row(self.insert_index, geophysical_research, self.table_widget)
            data_list.pause = False

        self.close()
        self.close_modal_forcefully()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = GeophysicWindow(22, 22)
    window.show()
    sys.exit(app.exec_())
