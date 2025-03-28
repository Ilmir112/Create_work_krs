import json
import math
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTabWidget, QWidget, QLabel, QComboBox, QMainWindow, QLineEdit, \
    QGridLayout, QPushButton, QBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QApplication

import data_list
from PyQt5.QtCore import Qt


from PyQt5.QtGui import QDoubleValidator
from main import MyMainWindow
from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion
from work_py.rationingKRS import descentNKT_norm, well_volume_norm, lifting_nkt_norm


class TabPageSoWith(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)


        validator = QDoubleValidator(0.0, 80000.0, 2)

        self.template_labelType = QLabel("Вид компоновки ПСШ", self)
        self.template_combo = QComboBox(self)

        self.privyazka_question_Label = QLabel("Нужно ли привязывать компоновку", self)
        self.privyazka_question_QCombo = QComboBox(self)
        self.privyazka_question_QCombo.addItems(['Нет', 'Да'])

        if self.data_well.current_bottom - self.data_well.perforation_roof <= 10 \
                and self.data_well.open_trunk_well is False and self.data_well.count_template != 0:
            self.privyazka_question_QCombo.setCurrentIndex(1)

        self.skm_label = QLabel("диаметр СГМ", self)
        self.skm_edit = QLineEdit(self)
        self.skm_edit.setValidator(validator)
        self.skm_edit.setText(str(self.data_well.column_diameter.get_value))


        self.roof_skm_label = QLabel("Кровля скреперования", self)
        self.roof_skm_line = QLineEdit(self)
        self.roof_skm_line.setValidator(validator)
        self.roof_skm_line.setClearButtonEnabled(True)

        self.sole_skm_label = QLabel("Подошва скреперования", self)
        self.sole_skm_line = QLineEdit(self)
        self.sole_skm_line.setClearButtonEnabled(True)
        self.sole_skm_line.setValidator(validator)

        self.skm_type_label = QLabel("Тип скрепера", self)
        self.skm_type_combo = QComboBox(self)
        self.skm_type_combo.addItems(['', 'СГМ'])


        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')

        # self.grid = QGridLayout(self)

        self.definition_template_work(float(self.current_bottom_edit.text()))

        self.grid.addWidget(self.current_bottom_label, 8, 3)
        self.grid.addWidget(self.current_bottom_edit, 9, 3)

        self.template_str_Label = QLabel("строка с СГМ", self)
        self.template_str_edit = QLineEdit(self)

        self.grid.addWidget(self.template_str_Label, 11, 1, 1, 8)
        self.grid.addWidget(self.template_str_edit, 12, 1, 1, 8)

        self.skm_teml_str_Label = QLabel("глубины спуска шаблонов", self)
        self.skm_teml_str_edit = QLineEdit(self)

        self.grid.addWidget(self.skm_teml_str_Label, 13, 1, 1, 8)
        self.grid.addWidget(self.skm_teml_str_edit, 14, 1, 1, 8)





        self.grid.addWidget(self.privyazka_question_Label, 8, 6)
        self.grid.addWidget(self.privyazka_question_QCombo, 9, 6)



        self.grid.addWidget(self.roof_skm_label, 35, 2, 1, 3)
        self.grid.addWidget(self.roof_skm_line, 36, 2, 1, 3)

        self.grid.addWidget(self.sole_skm_label, 35, 5, 1, 3)
        self.grid.addWidget(self.sole_skm_line, 36, 5, 1, 3)

        self.skm_edit.editingFinished.connect(self.update_template)

        self.current_bottom_edit.editingFinished.connect(self.update_template)
        self.skm_type_combo.currentTextChanged.connect(self.update_template)
        self.skm_type_combo.setCurrentIndex(1)

    def definition_template_work(self, current_bottom):
        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and current_bottom < self.data_well.head_column_additional.get_value):
            self.template_select_list = ['', 'СГМ ЭК', 'СГМ открытый ствол']

            self.template_combo.addItems(self.template_select_list)

            template_key = self.definition_pssh(current_bottom)
            self.template_combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_combo, 2, 2, 2, 8)

            self.grid.addWidget(self.skm_label, 4, 5)
            self.grid.addWidget(self.skm_edit, 5, 5)
            self.grid.addWidget(self.skm_type_label, 4, 6)
            self.grid.addWidget(self.skm_type_combo, 5, 6)



        else:
            self.template_select_list = ['', 'СГМ в основной колонне',
                                         'СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне']
            self.template_combo.addItems(self.template_select_list)
            template_key = self.definition_pssh(current_bottom)
            # print(template_key)
            self.template_combo.setCurrentIndex(self.template_select_list.index(template_key))

            self.grid.addWidget(self.template_labelType, 1, 2, 1, 8)
            self.grid.addWidget(self.template_combo, 2, 2, 2, 8)

            self.grid.addWidget(self.skm_label, 4, 6)
            self.grid.addWidget(self.skm_edit, 5, 6)
            self.grid.addWidget(self.skm_type_label, 4, 7)
            self.grid.addWidget(self.skm_type_combo, 5, 7)


    def definition_pssh(self, current_bottom):

        if self.data_well.column_additional is False and self.data_well.open_trunk_well is False:
            template_key = 'СГМ ЭК'

        elif self.data_well.column_additional is False and self.data_well.open_trunk_well is True:
            template_key = 'СГМ открытый ствол'

        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is False:
            template_key = 'СГМ в доп колонне'



        elif self.data_well.column_additional is True and self.data_well.open_trunk_well is True:
            template_key = 'СГМ в доп колонне + открытый ствол'


        return template_key

    def update_template(self):
        skm_type = self.skm_type_combo.currentText()
        current_bottom = self.current_bottom_edit.text()
        if current_bottom != '':
            self.data_well.current_bottom = float(current_bottom)
        template_str = ''
        if self.skm_edit.text() != '':
            skm = self.skm_edit.text()
        if self.template_combo.currentText() == 'СГМ ЭК':
            self.skm_edit.setText(str(self.data_well.column_diameter.get_value))
            template_str = f'{skm_type}-{skm} + НКТ + репер'

            self.data_well.skm_depth = self.data_well.current_bottom

        elif self.template_combo.currentText() == 'СГМ открытый ствол':
            self.skm_edit.setText(self.data_well.column_diameter)

            template_str = f'заглушка + НКТ{self.data_well.nkt_diam}мм ' \
                           f'{current_bottom - self.data_well.shoe_column.get_value +10}м + {skm_type}-{skm} + НКТ + репер'

        elif self.template_combo.currentText() == 'СГМ в доп колонне':
            self.skm_edit.setText(self.data_well.column_additional_diameter.get_value)

            template_str = f'{skm_type}-{skm} + НКТ{self.data_well.nkt_diam} ' \
                           f'{current_bottom - self.data_well.head_column_additional.get_value +10} + НКТ + репер'

            self.data_well.skm_depth = current_bottom
        elif self.template_combo.currentText() == 'СГМ в основной колонне':
            self.skm_edit.setText(self.data_well.column_additional_diameter)

            template_str = f'{skm_type}-{skm} + НКТ{self.data_well.nkt_diam} ' \
                           f'{self.data_well.current_bottom - self.data_well.head_column_additional.get_value +10} + НКТ + репер'

            self.data_well.skm_depth = current_bottom


        skm_teml_str = f'{skm_type}-{skm} до глубины {self.data_well.skm_depth}м'

        self.template_str_edit.setText(template_str)
        self.skm_teml_str_edit.setText(skm_teml_str)



class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoWith(parent), 'Выбор компоновки шаблонов')


class TemplateKrs(WindowUnion):

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)


        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        # print(f'дочерний класс TemplateKRS')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.table_widget = table_widget
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "необходимость Cкреперования"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.add_row_table)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonadd_string = QPushButton('Добавить интервалы скреперования')
        self.buttonadd_string.clicked.connect(self.add_string)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonadd_string, 3, 1)

    def add_row_table(self):
        roof_skm = self.tab_widget.currentWidget().roof_skm_line.text()
        sole_skm = self.tab_widget.currentWidget().sole_skm_line.text()
        if roof_skm != '':
            roof_skm = int(float(roof_skm))
        if sole_skm != '':
            sole_skm = int(float(sole_skm))
            if sole_skm > self.data_well.skm_depth:
                QMessageBox.information(self, 'Внимание',
                                              f'Глубина СКМ на {self.data_well.skm_depth}м не позволяет скреперовать в '
                                              f'{roof_skm}-{sole_skm}м')
                return
        template_key = self.tab_widget.currentWidget().template_combo.currentText()

        if not roof_skm or not sole_skm:
            QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if self.data_well.current_bottom < float(sole_skm):
            QMessageBox.information(self, 'Внимание', f'глубина забоя выше глубины нахождения '
                                                            f'СКМ {self.data_well.skm_depth}')
            return

        if template_key in ['СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне'] \
                and (roof_skm < self.data_well.head_column_additional.get_value or
                     sole_skm < self.data_well.head_column_additional.get_value):
            QMessageBox.warning(self, 'Ошибка',
                                      f'кровля скреперования выше головы '
                                      f'хвостовика {self.data_well.head_column_additional.get_value}')
            return

        elif template_key == 'СГМ в основной колонне' and \
                (sole_skm > self.data_well.head_column_additional.get_value or
                 roof_skm > self.data_well.head_column_additional.get_value):
            QMessageBox.warning(self, 'Ошибка',
                                      f'подошва скреперования ниже головы '
                                      f'хвостовика {self.data_well.head_column_additional.get_value}')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(roof_skm)))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(f'{sole_skm}'))

        self.tableWidget.setSortingEnabled(False)

    def add_string(self):
        from .advanted_file import skm_interval

        template_key = str(self.tab_widget.currentWidget().template_combo.currentText())
        skm_interval = skm_interval(self, template_key)


        rows = self.tableWidget.rowCount()

        for roof, sole in skm_interval:
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
            self.tableWidget.setSortingEnabled(False)

    def add_work(self):

        template_str = str(self.tab_widget.currentWidget().template_str_edit.text())
        template_key = str(self.tab_widget.currentWidget().template_combo.currentText())



        if self.data_well.column_additional is False or \
                self.data_well.column_additional and self.data_well.current_bottom <= self.data_well.head_column_additional.get_value:
            if self.data_well.template_depth >= self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'СГМ спускается ниже текущего забоя')
                return
        else:
            if self.data_well.template_depth_addition >= self.data_well.current_bottom:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'СГМспускается ниже текущего забоя')
                return
            if self.data_well.template_depth >= self.data_well.head_column_additional.get_value:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'СГМ спускается ниже головы хвостовика')
                return
            if template_key == 'ПСШ Доп колонна СКМ в основной колонне' and \
                    self.data_well.skm_depth >= self.data_well.head_column_additional.get_value:
                QMessageBox.warning(self, "ВНИМАНИЕ", 'СГМ спускается ниже головы хвостовика')
                return


        skm_tuple = []
        rows = self.tableWidget.rowCount()
        if rows == 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы скреперования')
            return
        for row in range(rows):
            roof_skm = self.tableWidget.item(row, 0)
            sole_skm = self.tableWidget.item(row, 1)
            if roof_skm and sole_skm:
                roof = int(roof_skm.text())
                sole = int(sole_skm.text())
                skm_tuple.append((roof, sole))

        # print(f'интервалы СКМ {self.data_well.skm_interval}')
        skm_list = sorted(skm_tuple, key=lambda x: x[0])


        work_template_list = self.template_ek(template_str, skm_list)
        if skm_tuple not in  self.data_well.skm_interval:
            self.data_well.skm_interval.extend(skm_list)

        self.populate_row(self.insert_index, work_template_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def well_volume(self):
        if not self.data_well.column_additional:

            volume_well = 3.14 * (
                    self.data_well.column_diameter.get_value - self.data_well.column_wall_thickness.get_value * 2) ** 2 / 4 / 1000000 * (
                              self.data_well.current_bottom)
            return volume_well
        else:
            volume_well = (3.14 * (
                    self.data_well.column_additional_diameter.get_value - self.data_well.column_wall_thickness.get_value * 2) ** 2 / 4 / 1000 * (
                                   self.data_well.current_bottom - float(
                               self.data_well.head_column_additional.get_value)) / 1000) + (
                                  3.14 * (
                                  self.data_well.column_diameter.get_value - self.data_well.column_wall_thickness.get_value * 2) ** 2 / 4 / 1000 * (
                                      self.data_well.head_column_additional.get_value) / 1000)
            return volume_well

    def template_ek(self, template_str, skm_list):

        from .advanted_file import raid
        # print(f'внут {skm_list}')
        skm_interval = raid(skm_list)



        privyazka_question = self.tab_widget.currentWidget().privyazka_question_QCombo.currentText()


        current_bottom = self.tab_widget.currentWidget().current_bottom_edit.text()
        if current_bottom != '':
            current_bottom = round(float(current_bottom), 1)

        list_template_ek = [
            [f'СПО  {template_str} на 'f'НКТ{self.data_well.nkt_diam}мм', None,
             f'Спустить  {template_str} на 'f'НКТ{self.data_well.nkt_diam}мм  с замером, шаблонированием НКТ. \n'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
             f'(при недохождении до нужного интервала допускается посадка инструмента не более 2т)',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(current_bottom, 1.2)],
            [f'Произвести скреперование в интервале {skm_interval}м Допустить низ НКТ до гл. {current_bottom}м',
             None,
             f'Произвести скреперование э/к в интервале {skm_interval}м  промывкой и проработкой 5 раз каждого '
             'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
             f'представителя Заказчика. Допустить низ НКТ до гл. {current_bottom}м, СГМ '
             f'до глубины {self.data_well.skm_depth}м. Составить акт. \n'
             '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель УСРСиСТ', round(0.012 * 90 * 1.04 + 1.02 + 0.77, 2)],
            [None, None,
             f'Поднять {template_str} на НКТ{self.data_well.nkt_diam}мм с глубины {current_bottom}м с доливом скважины в '
             f'объеме {round(current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'Мастер КРС', lifting_nkt_norm(float(current_bottom), 1.2)]
        ]


        privyazka_nkt = [f'Привязка по ГК и ЛМ По привязому НКТ удостовериться в наличии текущего забоя', None,
                         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}.'
                         f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                         f' По привязому НКТ удостовериться в наличии '
                         f'текущего забоя с плановым, Нормализовать '
                         f'забой обратной промывкой тех жидкостью '
                         f'уд.весом {self.data_well.fluid_work}   до глубины {current_bottom}м',
                         None, None, None, None, None, None, None, 'Мастер КРС', None, None]

        if privyazka_question == "Да":
            list_template_ek.insert(-1, privyazka_nkt)

        self.update_skm_interval(self.data_well.insert_index, skm_list)



        self.data_well.current_bottom = current_bottom

        return list_template_ek

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def update_skm_interval(self, index_plan, skm_list):

        row_index = index_plan - self.data_well.count_row_well
        template_ek = json.dumps(
            [self.data_well.template_depth, self.data_well.template_length, self.data_well.template_depth_addition,
             self.data_well.template_length_addition])
        for index, data in enumerate(self.data_well.data_list):
            if index == index:
                old_skm_2 = json.loads(self.data_well.data_list[index][12])
                template_ek_2 = self.data_well.data_list[index][11]
            if row_index < index:
                old_skm = json.loads(self.data_well.data_list[index][12])
                old_skm.extend(skm_list)
                self.data_well.data_list[index][12] = json.dumps(old_skm)
                if self.data_well.data_list[index][11] == template_ek_2:
                    self.data_well.data_list[index][11] = template_ek





if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()
    window = TemplateKrs(22, 22)
    window.show()
    app.exec_()
