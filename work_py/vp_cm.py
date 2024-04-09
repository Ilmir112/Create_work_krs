from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QInputDialog, QTabWidget, QMainWindow, QWidget, QLineEdit, QLabel, QComboBox, QGridLayout, \
    QPushButton, QMessageBox

import well_data
from main import MyWindow
from .rir import RirWindow

class TabPage_Vp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 80000)

        self.need_question_Label = QLabel("Нужно ли наращивать желонками", self)
        self.need_question_QCombo = QComboBox(self)
        self.need_question_QCombo.addItems(['Нет', 'Да', 'без ВП'])

        vp_list = ['ВП', 'ГПШ', 'ВПШ']

        self.vp_type_Label = QLabel("вид пакера геофизического", self)
        self.vp_type_QCombo = QComboBox(self)
        self.vp_type_QCombo.addItems(vp_list)


        self.vp_depth_label = QLabel("Глубина установки пакера", self)
        self.vp_depth_edit = QLineEdit(self)
        self.vp_depth_edit.setValidator(self.validator)
        self.vp_depth_edit.setText(f'{int(float(well_data.perforation_roof -20))}')

        self.cement_vp_Label = QLabel("Глубина докрепления цементом", self)
        self.cement_vp_edit = QLineEdit(self)
        self.cement_vp_edit.setValidator(self.validator)
        vp_depth = self.vp_depth_edit.text()
        if vp_depth != '':
            self.cement_vp_edit.setText(f'{int(float(vp_depth)-3)}')


        self.grid = QGridLayout(self)

        self.grid.addWidget(self.need_question_Label, 4, 4)
        self.grid.addWidget(self.need_question_QCombo, 5, 4)

        self.grid.addWidget(self.vp_type_Label, 4, 5)
        self.grid.addWidget(self.vp_type_QCombo, 5, 5)

        self.grid.addWidget(self.vp_depth_label, 6, 3)
        self.grid.addWidget(self.vp_depth_edit, 7, 3)

        self.grid.addWidget(self.cement_vp_Label, 6, 4)
        self.grid.addWidget(self.cement_vp_edit, 7, 4)


        self.vp_depth_edit.textChanged.connect(self.update_vp_depth)
        self.need_question_QCombo.currentTextChanged.connect(self.update_vp)


    def update_vp_depth(self):
        vp_depth = self.vp_depth_edit.text()
        if vp_depth != '':
            self.cement_vp_edit.setText(int(float(vp_depth)) -3)



    def update_vp(self, index):

        if index == "Да":
            self.grid.addWidget(self.vp_type_Label, 4, 5)
            self.grid.addWidget(self.vp_type_QCombo, 5, 5)
            self.grid.addWidget(self.vp_depth_label, 6, 3)
            self.grid.addWidget(self.vp_depth_edit, 7, 3)
            self.grid.addWidget(self.cement_vp_Label, 6, 4)
            self.grid.addWidget(self.cement_vp_edit, 7, 4)
        elif index == "Нет":
            self.cement_vp_Label.setParent(None)
            self.cement_vp_edit.setParent(None)
        else:
            self.vp_type_Label.setParent(None)
            self.vp_type_QCombo.setParent(None)
            self.vp_depth_label.setParent(None)
            self.vp_depth_edit.setParent(None)
            self.grid.addWidget(self.cement_vp_Label, 6, 4)
            self.grid.addWidget(self.cement_vp_edit, 7, 4)




class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_Vp(self), 'Установка ВП')


class VpWindow(QMainWindow):
    work_clay_window = None
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        vp_type_QCombo = self.tabWidget.currentWidget().vp_type_QCombo.currentText()
        need_question_QCombo = self.tabWidget.currentWidget().need_question_QCombo.currentText()
        vp_depth = int(float(self.tabWidget.currentWidget().vp_depth_edit.text()))
        cement_vp = int(float(self.tabWidget.currentWidget().cement_vp_edit.text()))
        if need_question_QCombo == "Да":
            if MyWindow.check_true_depth_template(self, vp_depth) is False:
                return
            if MyWindow.true_set_Paker(self, vp_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, vp_depth) is False:
                return
            work_list = self.vp(vp_type_QCombo, vp_depth, cement_vp)
        elif need_question_QCombo == "Нет":
            if MyWindow.check_true_depth_template(self, vp_depth) is False:
                return
            if MyWindow.true_set_Paker(self, vp_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, vp_depth) is False:
                return
            work_list = self.vp(vp_type_QCombo, vp_depth, cement_vp)
        else:
            work_list = self.czh(cement_vp)

        # if roof_clay_edit > sole_clay_edit:
        #     mes = QMessageBox.warning(self, 'Ошибка', 'Не корректные интервалы ')
        #     return



        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def vp(self, vp_type_QCombo, vp_depth, cement_vp_edit):



        if well_data.perforation_roof > vp_depth:
            vp_list = [
                [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                             f'При необходимости подготовить место для установки партии ГИС напротив мостков. '
                             f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером оТ 14.10.2021г',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None, None, None],
                [f'Произвести установку {vp_type_QCombo} на {vp_depth}м', None,
                 f'Произвести установку {vp_type_QCombo} (ЗАДАЧА 2.9.4.) на глубине  {vp_depth}м',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 10],
                [f'Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм '
                 f'в присутствии представителя заказчика '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением '
                 f'за 2 часа до начала работ) ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
                [f'докрепление цементными желонками до глубины {vp_depth - 3}м',None,
                 f'ПРИ НЕГЕРМЕТИЧНОСТИ {vp_type_QCombo}: \n '
                 f'произвести докрепление цементными желонками до глубины {vp_depth - 3}м (цемент с использование '
                 f'ускорителя схватывания кальций хлористого).'
                 f' Задача 9.5.2   ОЗЦ-12ч',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик РИР, УСРСиСТ', 6],
                [None, None,
                 f'Примечание: \n'
                 f'1) Обязательное актирование процесса приготовления ЦР с представителем геофизической партии, '
                 f'с отражением '
                 f'параметров раствора (удельный вес, обьем), так же отражать информацию в сводке. \n'
                 f'2) Производить отбор проб цементного раствора, результат застывания проб отражать в сводке.\n'
                 f'3) При приготовлении ЦР использовать CаСl \n'
                 f'4) Обеспечить видео фиксацию приготовленного цементного раствора \n'
                 f'5) Не проводить ПВР, в случае отсутствия ЦМ на ВП. \n '
                 f'6) Над ВП , ГПШ устанавливать цем мост не менее 4 м, (первые две желонки использовать механические, '
                 f'далее '
                 f'взрывные желонки).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', None],
                [f'Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм', None,
                 f'Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм в '
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
            well_data.current_bottom = vp_depth - 3

        else:
            vp_list = [
                [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                             f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                             f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером оТ 14.10.2021г',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None, None, None],
                [f'Произвести установку {vp_type_QCombo} на {vp_depth}м',
                 None,
                 f'Произвести установку {vp_type_QCombo} (ЗАДАЧА 2.9.4.) на глубине  {vp_depth}м',
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
                 f'параметров раствора (удельный вес, обьем), так же отражать информацию в сводке. \n'
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

            well_data.current_bottom = vp_depth-3
        RirWindow.perf_new(self, vp_depth, well_data.current_bottom)
        return vp_list


    def czh(self, cement_vp):



        vp_list = [
            [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                         f'Произвести  монтаж ГИС согласно схемы  №8а утвержденной главным инженером оТ 14.10.2021г',
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
             f'параметров раствора (удельный вес, обьем), так же отражать информацию в сводке. \n'
             f'2) Производить отбор проб цементного раствора, результат застывания проб отражать в сводке.\n'
             f'3) При приготовлении ЦР использовать CаСl \n'
             f'4) Обеспечить видео фиксацию приготовленного цементного раствора \n'
             f'5) Не проводить ПВР, в случае отсутствия ЦМ на ВП. \n '
             f'6) Над ВП , ГПШ устанавливать цем мост не менее 4 м, (первые две желонки использовать механические, далее '
             f'взрывные желонки).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],
            [f'Опрессовать ЭК на Р={well_data.max_admissible_pressure._value}атм',
             None,
             f'Опрессовать эксплуатационную колонну на Р={well_data.max_admissible_pressure._value}атм в присутствии '
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
        for plast in well_data.plast_work:
            for interval in well_data.dict_perforation[plast]['интервал']:
                interval_list.append(interval)

        if well_data.leakiness:
          # print(well_data.dict_leakiness)
            for nek in well_data.dict_leakiness['НЭК']['интервал']:
                print(nek)
                if well_data.dict_leakiness['НЭК']['интервал'][nek]['отключение'] is False:
                    interval_list.append(nek)

        if any([float(interval[0]) < float(cement_vp) for interval in interval_list]):
            vp_list = vp_list[:3]

        well_data.current_bottom = cement_vp
        return vp_list
