
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QComboBox, QGridLayout, \
    QPushButton, QMessageBox

import data_list
from work_py.parent_work import TabWidgetUnion, WindowUnion, TabPageUnion
from work_py.rir import RirWindow


class TabPageVp(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.need_question_Label = QLabel("Нужно ли наращивать желонками", self)
        self.need_question_qcombo = QComboBox(self)
        self.need_question_qcombo.addItems(['Нет', 'Да', 'без ВП'])

        vp_list = ['ВП', 'ГПШ', 'ВПШ']

        self.vp_type_Label = QLabel("вид пакера геофизического", self)
        self.vp_type_qcombo = QComboBox(self)
        self.vp_type_qcombo.addItems(vp_list)

        self.vp_depth_label = QLabel("Глубина установки пакера", self)
        self.vp_depth_edit = QLineEdit(self)
        self.vp_depth_edit.setValidator(self.validator_int)
        self.vp_depth_edit.setText(f'{int(float(self.data_well.perforation_roof - 20))}')

        self.cement_vp_Label = QLabel("Глубина докрепления цементом", self)
        self.cement_vp_edit = QLineEdit(self)
        self.cement_vp_edit.setValidator(self.validator_int)
        vp_depth = self.vp_depth_edit.text()
        if vp_depth != '':
            self.cement_vp_edit.setText(f'{int(float(vp_depth) - 3)}')

        # self.grid = QGridLayout(self)
        self.grid.addWidget(self.need_question_Label, 4, 4)
        self.grid.addWidget(self.need_question_qcombo, 5, 4)

        self.grid.addWidget(self.vp_type_Label, 4, 5)
        self.grid.addWidget(self.vp_type_qcombo, 5, 5)

        self.grid.addWidget(self.vp_depth_label, 6, 3)
        self.grid.addWidget(self.vp_depth_edit, 7, 3)

        self.grid.addWidget(self.cement_vp_Label, 6, 4)
        self.grid.addWidget(self.cement_vp_edit, 7, 4)

        self.vp_depth_edit.textChanged.connect(self.update_vp_depth)
        self.need_question_qcombo.currentTextChanged.connect(self.update_vp)
        self.need_question_qcombo.setCurrentIndex(1)

    def update_vp_depth(self):
        vp_depth = self.vp_depth_edit.text()
        if vp_depth != '':
            # print(f'ВП {vp_depth}')
            self.cement_vp_edit.setText(f'{int(float(vp_depth)) - 3}')

    def update_vp(self, index):

        if index == "Да":
            self.grid.addWidget(self.vp_type_Label, 4, 5)
            self.grid.addWidget(self.vp_type_qcombo, 5, 5)
            self.grid.addWidget(self.vp_depth_label, 6, 3)
            self.grid.addWidget(self.vp_depth_edit, 7, 3)
            self.grid.addWidget(self.cement_vp_Label, 6, 4)
            self.grid.addWidget(self.cement_vp_edit, 7, 4)
        elif index == "Нет":
            self.cement_vp_Label.setParent(None)
            self.cement_vp_edit.setParent(None)
            self.cement_vp_edit.setText(f'{int(float(self.data_well.current_bottom)) - 3}')
        else:
            self.vp_type_Label.setParent(None)
            self.vp_type_qcombo.setParent(None)
            self.vp_depth_label.setParent(None)
            self.vp_depth_edit.setParent(None)
            self.grid.addWidget(self.cement_vp_Label, 6, 4)
            self.grid.addWidget(self.cement_vp_edit, 7, 4)


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageVp(parent), 'Установка ВП')


class VpWindow(WindowUnion):
    work_clay_window = None

    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)
        self.insert_index = data_well.insert_index
        self.tab_widget = TabWidget(self.data_well)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        vp_type_qcombo = self.tab_widget.currentWidget().vp_type_qcombo.currentText()
        need_question_qcombo = self.tab_widget.currentWidget().need_question_qcombo.currentText()
        vp_depth = int(float(self.tab_widget.currentWidget().vp_depth_edit.text()))
        cement_vp = int(float(self.tab_widget.currentWidget().cement_vp_edit.text()))

        self.cable_type_text = ''
        self.angle_text = ''
        if self.data_well.angle_data and self.data_well.max_angle.get_value > 45:
            tuple_angle = self.calculate_angle(vp_depth, self.data_well.angle_data)
            if float(str(tuple_angle[0]).replace(',', '.')) >= 45:
                self.angle_text = tuple_angle[2]
                if self.angle_text:
                    question = QMessageBox.question(self, 'Ошибка', f'{self.angle_text},'
                                                                    f' есть риски не прохода ВП, продолжить?')
                    if question == QMessageBox.StandardButton.Yes:
                        self.cable_type_text = ' СОГЛАСОВАТЬ ГИС НА ЖЕСТКОМ КАБЕЛЕ'
                    else:
                        return

        if need_question_qcombo == "Да":
            if self.check_true_depth_template(vp_depth) is False:
                return
            if self.true_set_paker(vp_depth) is False:
                return
            if self.check_depth_in_skm_interval(vp_depth) is False:
                return
            work_list = self.vp(vp_type_qcombo, vp_depth, cement_vp, need_question_qcombo)
        elif need_question_qcombo == "Нет":
            if self.check_true_depth_template(vp_depth) is False:
                return
            if self.true_set_paker(vp_depth) is False:
                return
            if self.check_depth_in_skm_interval(vp_depth) is False:
                return
            work_list = self.vp(vp_type_qcombo, vp_depth, cement_vp, need_question_qcombo)
        else:
            work_list = self.czh(cement_vp)

        # if roof_clay_edit > sole_clay_edit:
        #     QMessageBox.warning(self, 'Ошибка', 'Не корректные интервалы ')
        #     return

        if work_list:
            self.populate_row(self.insert_index, work_list, self.table_widget)
            data_list.pause = False
            self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    def vp(self, vp_type_qcombo, vp_depth, cement_vp_edit, need_question_qcombo):
        if self.data_well.perforation_roof > vp_depth:

            vp_list = [
                [None, None,
                 f'Вызвать геофизическую партию {self.cable_type_text} {self.angle_text}. '
                 f'Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                 f'При необходимости подготовить место для установки партии ГИС напротив мостков. '
                 f'Произвести  монтаж ГИС согласно схемы схема №11 утвержденной главным инженером '
                 f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None, None, None],
                [f'Произвести установку {vp_type_qcombo} на {vp_depth}м', None,
                 f'Произвести установку {vp_type_qcombo} (ЗАДАЧА 2.9.4.) на глубине  {vp_depth}м',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 10],
                [f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм',
                 None,
                 f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм '
                 f'в присутствии представителя заказчика '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением '
                 f'за 2 часа до начала работ) ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
                [f'докрепление цементными желонками до глубины {vp_depth - 3}м', None,
                 f'ПРИ НЕГЕРМЕТИЧНОСТИ {vp_type_qcombo}: \n '
                 f'произвести докрепление цементными желонками до глубины {vp_depth - 3}м (цемент с использование '
                 f'ускорителя схватывания кальций хлористого).'
                 f' Задача 9.5.2   ОЗЦ-12ч',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 18],
                [None, None,
                 f'Примечание: \n'
                 f'1) Обязательное актирование процесса приготовления ЦР с представителем геофизической партии, '
                 f'с отражением '
                 f'параметров раствора (удельный вес, объем), так же отражать информацию в сводке. \n'
                 f'2) Производить отбор проб цементного раствора, результат застывания проб отражать в сводке.\n'
                 f'3) При приготовлении ЦР использовать CаСl \n'
                 f'4) Обеспечить видео фиксацию приготовленного цементного раствора \n'
                 f'5) Не проводить ПВР, в случае отсутствия ЦМ на ВП. \n '
                 f'6) Над ВП , ГПШ устанавливать цем мост не менее 4 м, (первые две желонки использовать механические, '
                 f'далее '
                 f'взрывные желонки).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', None],
                [f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм',
                 None,
                 f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм в '
                 f'присутствии представителя заказчика '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                 f'подтверждением за 2 часа до начала работ) ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
        else:
            vp_list = [
                [None, None,
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                 f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                 f'Произвести  монтаж ГИС согласно схемы схема №11 утвержденной главным инженером от '
                 f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None, None, None],
                [f'Произвести установку {vp_type_qcombo} на {vp_depth}м',
                 None,
                 f'Произвести установку {vp_type_qcombo} (ЗАДАЧА 2.9.4.) на глубине  {vp_depth}м',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 10],
                [f'докреплением цементными желонками до глубины {cement_vp_edit}м', None,
                 f'Произвести докреплением цементными желонками до глубины {cement_vp_edit}м (цемент с использование '
                 f'ускорителя схватывания кальций хлористого). Задача 9.5.2   ОЗЦ-12ч',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 15],
                [None, None,
                 f'Примечание: \n'
                 f'1) Обязательное актирование процесса приготовления ЦР с представителем геофизической партии, '
                 f'с отражением '
                 f'параметров раствора (удельный вес, объем), так же отражать информацию в сводке. \n'
                 f'2) Производить отбор проб цементного раствора, результат застывания проб отражать в сводке.\n'
                 f'3) При приготовлении ЦР использовать CаСl \n'
                 f'4) Обеспечить видео фиксацию приготовленного цементного раствора \n'
                 f'5) Не проводить ПВР, в случае отсутствия ЦМ на ВП. \n '
                 f'6) Над ВП , ГПШ устанавливать цем мост не менее 4 м, (первые две желонки использовать механические, '
                 f'далее '
                 f'взрывные желонки).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', None]
            ]
        self.data_well.current_bottom = cement_vp_edit

        if need_question_qcombo == 'Нет':
            vp_list = [
                [None, None,
                 f'Вызвать геофизическую партию {self.cable_type_text}. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                 f'При необходимости подготовить место для установки партии ГИС напротив мостков. '
                 f'Произвести  монтаж ГИС согласно схемы схема №11 утвержденной главным инженером '
                 f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None, None, None],
                [f'Произвести установку {vp_type_qcombo} на {vp_depth}м', None,
                 f'Произвести установку {vp_type_qcombo} (ЗАДАЧА 2.9.4.) на глубине  {vp_depth}м',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 10],
                [f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм',
                 None,
                 f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм в '
                 f'присутствии представителя заказчика '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с '
                 f'подтверждением за 2 часа до начала работ) ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
            if self.data_well.perforation_roof > vp_depth:
                vp_list.pop(-1)
                vp_list.pop(-1)
            self.data_well.current_bottom = vp_depth

        RirWindow.perf_new(self, self.data_well.current_bottom, vp_depth)
        return vp_list

    def czh(self, cement_vp):
        vp_list = [
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
             f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
             f'Произвести  монтаж ГИС согласно схемы схема №11 утвержденной главным инженером от '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г',
             None, None, None, None, None, None, None,
             'Мастер КРС', None, None, None],

            [f'докрепление цементными желонками до глубины {cement_vp}м', None,
             f'произвести докрепление цементными желонками до глубины {cement_vp}м (цемент с использование '
             f'ускорителя схватывания кальций хлористого).'
             f' Задача 9.5.2   ОЗЦ-12ч',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [None, None,
             f'Примечание: \n'
             f'1) Обязательное актирование процесса приготовления ЦР с представителем геофизической партии, с отражением '
             f'параметров раствора (удельный вес, объем), так же отражать информацию в сводке. \n'
             f'2) Производить отбор проб цементного раствора, результат застывания проб отражать в сводке.\n'
             f'3) При приготовлении ЦР использовать CаСl \n'
             f'4) Обеспечить видео фиксацию приготовленного цементного раствора \n'
             f'5) Не проводить ПВР, в случае отсутствия ЦМ на ВП. \n '
             f'6) Над ВП , ГПШ устанавливать цем мост не менее 4 м, (первые две желонки использовать механические, далее '
             f'взрывные желонки).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],
            [f'Опрессовать ЭК на Р={self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Опрессовать эксплуатационную колонну на Р={self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до начала работ) ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
        ]
        interval_list = []
        for plast in self.data_well.plast_work:
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                interval_list.append(interval)

        if self.data_well.dict_leakiness:
            for nek in self.data_well.dict_leakiness['НЭК']['интервал']:
                # print(nek)
                if self.data_well.dict_leakiness['НЭК']['интервал'][nek]['отключение'] is False:
                    interval_list.append(nek)

        if any([float(interval[0]) < float(cement_vp) for interval in interval_list]):
            vp_list = vp_list[:3]

        self.data_well.current_bottom = cement_vp
        return vp_list
