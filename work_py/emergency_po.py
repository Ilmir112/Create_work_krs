from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, QPushButton, \
    QMessageBox

import data_list

from work_py.parent_work import TabPageUnion, WindowUnion,TabWidgetUnion
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm


class TabPageSoLar(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.po_type_label = QLabel("Прихваченное оборудование", self)
        self.po_type_combo = QComboBox(self)
        raid_type_list = ['ЭЦН', 'пакер', 'НКТ']
        self.po_type_combo.addItems(raid_type_list)

        self.lar_diameter_label = QLabel("Диаметр ловителя", self)
        self.lar_diameter_line = QLineEdit(self)

        self.lar_type_label = QLabel("Тип ловителя", self)
        self.lar_type_combo = QComboBox(self)
        raid_type_list = ['ОВ', 'ВТ', 'метчик', 'колокол']
        self.lar_type_combo.addItems(raid_type_list)

        self.nkt_select_label = QLabel("компоновка НКТ", self)
        self.nkt_select_combo = QComboBox(self)
        self.nkt_select_combo.addItems(['оборудование в ЭК', 'оборудование в ДП'])

        if self.data_well.column_additional is False or (self.data_well.column_additional and
                                                    self.data_well.head_column_additional.get_value < self.data_well.current_bottom):
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

        # self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.po_type_label, 2, 0)
        self.grid.addWidget(self.po_type_combo, 3, 0)

        self.grid.addWidget(self.lar_type_label, 2, 1)
        self.grid.addWidget(self.lar_type_combo, 3, 1)

        self.grid.addWidget(self.lar_diameter_label, 2, 2)
        self.grid.addWidget(self.lar_diameter_line, 3, 2)

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
        self.bottom_line.setText(f'{self.data_well.current_bottom}')

        if self.data_well.column_additional is False or \
                (self.data_well.column_additional and self.data_well.current_bottom < self.data_well.head_column_additional.get_value):
            self.nkt_select_combo.setCurrentIndex(1)
            self.nkt_select_combo.setCurrentIndex(0)
        else:
            self.nkt_select_combo.setCurrentIndex(1)

        if self.data_well.emergency_well is True:
            self.emergency_bottom_line.setText(f'{self.data_well.emergency_bottom}')





class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoLar(parent), 'ловильные работы')


class EmergencyPo(WindowUnion):

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)


        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.table_widget = table_widget

        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)

        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonadd_work, 3, 0)

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия
    def add_work(self):
        po_str_combo = self.tabWidget.currentWidget().po_type_combo.currentText()
        nkt_str_combo = self.tabWidget.currentWidget().nkt_str_combo.currentText()
        lar_diameter_line = self.tabWidget.currentWidget().lar_diameter_line.text()
        nkt_key = self.tabWidget.currentWidget().nkt_select_combo.currentText()
        lar_type_combo = self.tabWidget.currentWidget().lar_type_combo.currentText()
        emergency_bottom_line = self.tabWidget.currentWidget().emergency_bottom_line.text().replace(',', '')
        bottom_line = self.tabWidget.currentWidget().bottom_line.text().replace(',', '')
        if bottom_line != '':
            bottom_line = int(float(bottom_line))

        if emergency_bottom_line != '':
            emergency_bottom_line = int(float(emergency_bottom_line))

            if emergency_bottom_line > self.data_well.current_bottom:
                QMessageBox.warning(self, 'Ошибка',
                                          'Забой ниже глубины текущего забоя')
                return
        else:
            QMessageBox.warning(self, 'Ошибка',
                                      'ВВедите аварийный забой')
            return

        if nkt_key == 'оборудование в ЭК' and self.data_well.column_additional and \
                emergency_bottom_line > self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для доп колонны')
            return
        elif nkt_key == 'оборудование в ДП' and self.data_well.column_additional and \
                emergency_bottom_line < self.data_well.head_column_additional.get_value:
            QMessageBox.warning(self, 'Ошибка',
                                      'Не корректно выбрана компоновка для основной колонны')
            return

        raid_list = self.emergency_sticking(po_str_combo, lar_diameter_line, nkt_key, lar_type_combo,
                                           emergency_bottom_line, bottom_line)
        self.data_well.current_bottom = bottom_line

        self.populate_row(self.insert_index, raid_list, self.table_widget)
        data_list.pause = False
        self.close()


    def emergency_sticking(self, emergence_type, lar_diameter_line, nkt_key, lar_type_combo,
                      emergency_bottom_line, bottom_line):
        from work_py.emergency_lar import EmergencyLarWork
        from work_py.emergencyWork import emergency_hook, magnet_select

        emergency_list = [
            [None, None,
             f'При отрицательных результатах по срыву {emergence_type}, по согласованию с '
             f'УСРСиСТ увеличить нагрузку до 33т. При отрицательных результатах:',
             None, None, None, None, None, None, None,
             'Аварийный Мастер КРС, УСРСиСТ', 12],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
             f'Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', None],
            [f' Запись ПО', None,
             f'Произвести запись по определению прихвата по НКТ',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', 8],
            [None, None,
             f'По согласованию с аварийной службой супервайзинга, произвести ПВР - отстрел прихваченной части компоновки '
             f'НКТ с помощью ЗТК-С-54 (2 заряда) (или аналогичным ТРК).'
             f'Работы производить по техническому проекту на ПВР, согласованному с Заказчиком. ЗАДАЧА 2.9.3',
             None, None, None, None, None, None, None,
             'Мастер, подрядчик по ГИС', 5],
            [None, None,
             f'Поднять аварийные НКТ до устья. \nПри выявлении отложений солей и гипса, отобрать шлам. '
             f'Сдать в лабораторию для проведения хим. анализа.',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(self.data_well.current_bottom, 1.2)],
            [f'Завоз на скважину СБТ', None,
             f'Завоз на скважину СБТ – Укладка труб на стеллажи.',
             None, None, None, None, None, None, None,
             'Мастер', None],
            [None, None,
             f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: удочка ловильная, Метчик,'
             f' Овершот, Внутренние труболовки, кольцевой фрез (типоразмер оборудования согласовать с '
             f'аварийной службой УСРСиСТ)',
             None, None, None, None, None, None, None,
             'Мастер', None]]

        if emergence_type == 'ЭЦН':  # Добавление ловильного крючка при спущенном ЭЦН
            for row in emergency_hook(self):
                emergency_list.append(row)

        seal_list = [
            [f'СПо печати', None,
              f'Спустить с замером торцевую печать {magnet_select(self, "НКТ")} до аварийная головы с замером.'
              f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
              None, None, None, None, None, None, None,
              'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1.2)],
             [None, None,
              f'Произвести работу печатью  с обратной промывкой с разгрузкой до 5т.',
              None, None, None, None, None, None, None,
              'мастер КРС, УСРСиСТ', 2.5],
             [None, None,
              f'Поднять {magnet_select(self, "НКТ")} с доливом тех жидкости в '
              f'объеме {round(self.data_well.current_bottom * 1.25 / 1000, 1)}м3'
              f' удельным весом {self.data_well.fluid_work}.',
              None, None, None, None, None, None, None,
              'Мастер КРС', liftingNKT_norm(self.data_well.current_bottom, 1.2)],
             [None, None,
              f'По результату ревизии печати, согласовать с ПТО  и УСРСиСТ и '
              f'подобрать ловильный инструмент',
              None, None, None, None, None, None, None,
              'мастер КРС', None]]

        for row in seal_list:
            emergency_list.append(row)

        return emergency_list



