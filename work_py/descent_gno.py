from typing import List

from openpyxl.descriptors import String

import data_list
from abc import ABC, abstractmethod

from log_files.log import logger
from main import MyMainWindow

from work_py.parent_work import TabWidgetUnion, TabPageUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, descent_sucker_pod

from work_py.template_work import TemplateKrs
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QPushButton


class TabPageGno(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.nkt_label = QLabel('компоновка НКТ')
        self.nkt_edit = QLineEdit(self)
        self.nkt_edit.setText(f'{self.gno_nkt_opening(self.data_well.dict_nkt_after)}')

        self.gno_label = QLabel("вид спускаемого ГНО", self)
        self.gno_combo = QComboBox(self)
        gno_list = ['пакер', 'ОРЗ', 'ОРД', 'воронка', 'НН с пакером', 'НВ с пакером',
                    'ЭЦН с пакером', 'ЭЦН', 'НВ', 'НН', 'консервация']

        self.rgd_question_label = QLabel("проведение РГД", self)
        self.rgd_question_combo = QComboBox(self)
        self.rgd_question_combo.addItems(['Да', 'Нет'])

        self.sucker_label = QLabel('компоновка штанг')
        self.sucker_edit = QLineEdit(self)
        self.sucker_edit.setText(f'{self.gno_nkt_opening(self.data_well.dict_sucker_rod_after)}')

        self.distance_between_nkt_label = QLabel('Расстояние между НКТ')
        self.distance_between_nkt_edit = QLineEdit(self)
        self.distance_between_nkt_edit.setText(f'{300}')

        self.gno_combo.addItems(gno_list)

        lift_key = self.select_gno()

        # self.grid = QGridLayout(self)
        self.grid.addWidget(self.rgd_question_label, 4, 6)
        self.grid.addWidget(self.rgd_question_combo, 5, 6)
        self.grid.addWidget(self.gno_label, 4, 3)
        self.grid.addWidget(self.gno_combo, 5, 3)
        self.grid.addWidget(self.nkt_label, 4, 4)
        self.grid.addWidget(self.nkt_edit, 5, 4)
        self.grid.addWidget(self.distance_between_nkt_label, 4, 8)
        self.grid.addWidget(self.distance_between_nkt_edit, 5, 8)
        self.grid.setColumnMinimumWidth(4, len(self.nkt_edit.text()) * 6)

        self.need_juming_after_sko_label = QLabel('Нужно ли проводить промывку после СКО')
        self.need_juming_after_sko_combo = QComboBox(self)
        self.need_juming_after_sko_combo.addItems(['Нет', 'Да'])
        self.grid.addWidget(self.need_juming_after_sko_label, 4, 7)
        self.grid.addWidget(self.need_juming_after_sko_combo, 5, 7)

        if self.data_well.region != 'КГМ':
            self.need_juming_after_sko_label.setParent(None)
            self.need_juming_after_sko_combo.setParent(None)
            self.need_juming_after_sko_combo.setCurrentIndex(1)

        self.gno_combo.currentTextChanged.connect(self.update_lift_key)
        self.gno_combo.setCurrentIndex(3)
        self.gno_combo.setCurrentIndex(gno_list.index(lift_key))

    def update_lift_key(self, index):
        if index == 'пакер':
            self.grid.addWidget(self.rgd_question_label, 4, 5)
            self.grid.addWidget(self.rgd_question_combo, 5, 5)
            self.sucker_label.setParent(None)
            self.sucker_edit.setParent(None)
            self.need_juming_after_sko_label.setParent(None)
            self.need_juming_after_sko_combo.setParent(None)
        elif index in ['пакер', 'ОРЗ', 'воронка', 'ЭЦН с пакером', 'ЭЦН']:
            self.sucker_label.setParent(None)
            self.sucker_edit.setParent(None)
            self.rgd_question_label.setParent(None)
            self.rgd_question_combo.setParent(None)
        else:
            self.grid.addWidget(self.sucker_label, 4, 5)
            self.grid.addWidget(self.sucker_edit, 5, 5)
            self.grid.setColumnMinimumWidth(5, len(self.sucker_edit.text()) * 6)
            self.rgd_question_label.setParent(None)
            self.rgd_question_combo.setParent(None)

    @staticmethod
    def gno_nkt_opening(dict_nkt_po):

        str_gno = ''
        for nkt, length_nkt in dict_nkt_po.items():
            if str(nkt).isdigit():
                str_gno += f'{nkt}мм - {round(float(length_nkt), 1)}м, '
            else:
                str_gno += f'{nkt} - {round(float(length_nkt), 1)}м, '
        return str_gno[:-3]

    def select_gno(self):
        lift_key = ''

        if self.check_if_none(self.data_well.dict_pump_ecn["after"]) != 'отсут' and \
                self.check_if_none(self.data_well.dict_pump_shgn["after"]) != 'отсут':
            lift_key = 'ОРД'
        elif self.check_if_none(self.data_well.dict_pump_ecn["after"]) != 'отсут' and \
                self.check_if_none(self.data_well.paker_before["after"]) == 'отсут':
            lift_key = 'ЭЦН'
        elif self.check_if_none(self.data_well.dict_pump_ecn["after"]) != 'отсут' and \
                self.check_if_none(self.data_well.paker_before["after"]) != 'отсут':
            lift_key = 'ЭЦН с пакером'
        elif self.check_if_none(self.data_well.dict_pump_shgn["after"]) != 'отсут' and \
                self.data_well.dict_pump_shgn["after"].upper() != 'НН' \
                and self.check_if_none(self.data_well.paker_before["after"]) == 'отсут':
            lift_key = 'НВ'
        elif self.check_if_none(self.data_well.dict_pump_shgn["after"]) != 'отсут' and \
                self.check_if_none(self.data_well.dict_pump_shgn["after"]).upper() != 'НН' \
                and self.check_if_none(self.data_well.paker_before["after"]) != 'отсут':
            lift_key = 'НВ с пакером'
        elif 'НН' in self.check_if_none(self.data_well.dict_pump_shgn["after"]).upper() \
                and self.check_if_none(self.data_well.paker_before["after"]) == 'отсут':
            lift_key = 'НН'
        elif 'НН' in self.check_if_none(self.data_well.dict_pump_shgn["after"]).upper() and \
                self.check_if_none(self.check_if_none(self.data_well.paker_before["after"])) != 'отсут':
            lift_key = 'НН с пакером'
        elif self.check_if_none(self.data_well.dict_pump_shgn["after"]) == 'отсут' and \
                self.check_if_none(self.data_well.paker_before["after"]) == 'отсут' \
                and self.check_if_none(self.data_well.dict_pump_ecn["after"]) == 'отсут':
            lift_key = 'воронка'
        elif '89' in self.data_well.dict_nkt_after.keys() and '48' in self.data_well.dict_nkt_after.keys() and \
                self.check_if_none(
                    self.data_well.paker_before["after"]) != 'отсут':
            lift_key = 'ОРЗ'
        elif self.check_if_none(self.data_well.dict_pump_shgn["after"]) == 'отсут' and \
                self.check_if_none(self.data_well.paker_before["after"]) != 'отсут' \
                and self.check_if_none(self.data_well.dict_pump_ecn["after"]) == 'отсут':
            lift_key = 'пакер'
        if 'КР11' in self.data_well.type_kr:
            lift_key = 'консервация'

        return lift_key


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageGno(parent), 'Спуск ГНО')


class GnoDescentWindow(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)

        self.data_well = data_well
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

    def closeEvent(self, event):

        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window =None
        event.accept()  # Принимаем событие закрытия

    def check_descent_paker(self):
        if self.lift_key == 'пакер':
            if self.data_well.depth_fond_paker_before["after"] > self.data_well.template_depth and \
                    (self.data_well.column_additional is False or
                     (self.data_well.column_additional and
                      self.data_well.current_bottom < self.data_well.head_column_additional.get_value)):

                QMessageBox.critical(self, 'Ошибка',
                                     f'Нельзя спускать пакер {self.data_well.depth_fond_paker_before["after"]}м'
                                     f'ниже глубины шаблонирования ЭК {self.data_well.template_depth}м')
                return

            elif self.data_well.depth_fond_paker_before["after"] < self.data_well.head_column_additional.get_value and \
                    self.data_well.depth_fond_paker_before["after"] > self.data_well.template_depth and \
                    self.data_well.column_additional:
                QMessageBox.critical(self, 'Ошибка',
                                     f'Нельзя спускать пакер {self.data_well.depth_fond_paker_before["after"]}м'
                                     f'ниже глубины шаблонирования ЭК {self.data_well.template_depth}м')
                return

            elif self.data_well.depth_fond_paker_before["after"] > self.data_well.head_column_additional.get_value and \
                    self.data_well.depth_fond_paker_before["after"] > \
                    self.data_well.template_depth_addition \
                    and self.data_well.column_additional:
                QMessageBox.critical(self, 'Ошибка',
                                     f'Нельзя спускать пакер {self.data_well.depth_fond_paker_before["after"]}м'
                                     f'ниже глубины шаблонирования ЭК '
                                     f'{self.data_well.template_depth_addition}м')
                return
        else:
            if self.lift_key in ['ОРД', 'ЭЦН с пакером', 'ЭЦН']:
                if self.data_well.dict_pump_ecn_depth["after"] > self.data_well.template_depth and \
                        (self.data_well.column_additional is False or
                         (self.data_well.column_additional and
                          self.data_well.current_bottom > self.data_well.head_column_additional.get_value and
                          self.data_well.dict_pump_ecn_depth["after"] < self.data_well.head_column_additional.get_value)):
                    QMessageBox.critical(self, 'Ошибка',
                                         f'Нельзя спускать ЭЦН {self.data_well.paker_before["after"]}м'
                                         f'ниже глубины шаблонирования ЭК {self.data_well.template_depth}м')
                    return
                elif self.data_well.dict_pump_ecn_depth["after"] < self.data_well.head_column_additional.get_value and \
                        self.data_well.dict_pump_ecn_depth["after"] > self.data_well.template_depth and \
                        self.data_well.column_additional:
                    QMessageBox.critical(self, 'Ошибка',
                                         f'Нельзя спускать ЭЦН {self.data_well.paker_before["after"]}м'
                                         f'ниже глубины шаблонирования ЭК {self.data_well.template_depth}м')
                    return
                elif self.data_well.dict_pump_ecn_depth["after"] > self.data_well.head_column_additional.get_value and \
                        self.data_well.dict_pump_ecn_depth["after"] > self.data_well.template_depth_addition \
                        and self.data_well.column_additional:
                    QMessageBox.critical(self, 'Ошибка',
                                         f'Нельзя спускать ЭЦН {self.data_well.paker_before["after"]}м'
                                         f'ниже глубины шаблонирования ЭК '
                                         f'{self.data_well.template_depth_addition}м')
                    return
        return True


    def add_work(self):
        try:
            self.current_widget = self.tab_widget.currentWidget()
            self.lift_key = self.current_widget.gno_combo.currentText()
            if sum(list(self.data_well.dict_nkt_after.values())) > self.data_well.current_bottom and \
                    self.lift_key not in ['ОРД', 'ОРЗ']:
                QMessageBox.warning(self, 'Ошибка', f'Длина НКТ {sum(list(self.data_well.dict_nkt_before.values()))}м '
                                                    f'После ремонта больше текущего забоя {self.data_well.current_bottom}м')
                return


            if self.check_descent_paker() is None:
                return

            self.lift_dict_strategies = {
                'НН с пакером': DescentNnWithPaker(self),
                'НВ с пакером': DescentNvWithPaker(self),
                'ЭЦН с пакером': DescentEcnWithPaker(self),
                'ЭЦН': DescentEcn(self),
                'НВ': DescentNv(self),
                'НН': DescentNn(self),
                'ОРД': DescentORD(self),
                'ОРЗ': DescentOrz(self),
                'воронка': DescentVoronka(self),
                'консервация': Conservation(self),
                'пакер': DescentPaker(self)
            }
            work_list = self.on_execute_strategy(self.lift_key)
        except Exception as e:
            logger.critical(e)
        if work_list:
            self.populate_row(self.insert_index, work_list, self.table_widget)
            data_list.pause = False
            self.close()
            self.close_modal_forcefully()

    def on_execute_strategy(self, index):
        strategy = self.lift_dict_strategies.get(index)
        if strategy:
            work_list = strategy.execute()
            return work_list


class DescentParent(ABC):
    def __init__(self, parent=None):
        super().__init__()
        self.current_widget = parent.current_widget
        self.data_well = parent.data_well
        self.calc_fond_nkt = parent.calc_fond_nkt

        self.nkt_edit = self.current_widget.nkt_edit.text()
        self.sucker_edit = self.current_widget.sucker_edit.text()
        self.distance_between_nkt = self.current_widget.distance_between_nkt_edit.text()
        self.lift_key = parent.lift_key

        if self.distance_between_nkt != '':
            self.distance_between_nkt = int(float(self.distance_between_nkt))

        if self.data_well.region == 'КГМ':
            self.need_juming_after_sko_combo = self.current_widget.need_juming_after_sko_combo.currentText()
        else:
            self.need_juming_after_sko_combo = 'Нет'

        self.len_nkt = sum(list(self.data_well.dict_nkt_after.values()))
        self.privyazka_nkt = parent.privyazka_nkt
        self.calc_fond_nkt_str = self.calc_fond_nkt(self.len_nkt, self.distance_between_nkt)

    @abstractmethod
    def execute(self) -> String:
        NotImplementedError('Не выбран метод реализации, метод должен быть переопределен')

    @staticmethod
    def insert_text_depth_paker_1000(depth):
        if depth < 1000:
            work_list = [
                [None, None,
                 f'При посадки пакерного устройства с верхним механическим якорем в скважине на плановой глубине до '
                 f'1000м, обеспечить контрольную проверку посадки пакерного устройства путем создания '
                 f'натяжения (без рывков) колонны НКТ+пакер на величину превышающую собственный вес компоновки на 2 тонны.'
                 f'Контрольную проверку выполнять сразу после посадки пакерного устройства в скважине. '
                 f'В случае, если при натяжении парное устройство сорвалось с места посадки, '
                 f'что характеризуется падением показаний на индикаторе веста до собственного веса'
                 f'компоновки - выполнить повторную посадку с проведением контрольной проверки.\n'
                 f'При повторении отрицательного результата посадки - подать оперативную заявку на замену '
                 f'пакерного устройства\n'
                 f'Результаты контрольной проверки необходимо оформлять актом и отражать в ежедневных сводках ТКРС',
                 None, None, None, None, None, None, None,
                 'мастер КРС', float(8.5)]
            ]
            return work_list

    def jumping_after_sko(self):
        jumping_sko_list = []
        if self.lift_key in ['ЭЦН', 'НВ', 'НН', 'НН с пакером', 'ЭЦН с пакером', 'НВ с пакером', 'ОРД'] and \
                self.data_well.region == 'КГМ' and self.need_juming_after_sko_combo == 'Да':

            if self.lift_key in ['НВ', 'НН']:
                jumping_sko_list = [
                    [None, None,
                     f'ПРИ НАЛИЧИИ ЦИРКУЛЯЦИИ ДОПУСТИТЬ КОМПОНОВКУ НА ТНКТ ДО ТЕКУЩЕГО ЗАБОЯ. '
                     f'ПРОИЗВЕСТИ ВЫМЫВ ПРОДУКТОВ '
                     f'РЕАКЦИИ С ТЕКУЩЕГО ЗАБОЯ ОБРАТНОЙ ПРОМЫВКОЙ УД.ВЕСОМ {self.data_well.fluid_work}. '
                     f'ПОДНЯТЬ тНКТ ДО ПЛАНОВОЙ ГЛУБИНЫ {self.data_well.dict_pump_shgn_depth["after"]}м',
                     None, None, None, None, None, None, None,
                     'мастер КРС', float(8.5)]]
                # gno_list.insert(-4, jumping_sko_list)
            else:
                jumping_sko_list = [[None, None,
                                     'С целью вымыва продуктов реакции:',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', '']]
                for row in TemplateKrs.pero(self):
                    jumping_sko_list.append(row)

                    # for row in pero_list[::-1]:
                    #     gno_list.insert(0, row)
        return jumping_sko_list

    def need_privyazka_nkt(self):
        for plast in list(self.data_well.dict_perforation.keys()):
            for interval in self.data_well.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(self.data_well.depth_fond_paker_before["after"]))) < 10 or abs(
                        float(interval[0] - float(self.data_well.depth_fond_paker_before["after"]))) < 10:
                    return True

    def begin_text(self) -> List:
        gno_list = [
            [None, None,
             f'За 48 часов до спуска запросить КАРТУ спуска на ГНО и заказать оборудование согласно карты спуска.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None]
        ]
        return gno_list



    def append_note_6(self):
        work_list = [
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:\n'
             f'1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтировать ПШ+СУСГ.при необходимости '
             f'сорвать пакер'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью'
             f' y={self.data_well.fluid_work};'
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с'
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору;'
             f' смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм - время опрессовки '
             f'15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию '
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]]
        return work_list

    def append_finish(self):
        end_list = [
            [None, None,
             f'Все работы производить с соблюдением т/б и технологии'
             f' согласно утвержденному плану. Демонтировать подъемный агрегат и оборудование. ',
             None, None, None, None, None, None, None,
             'мастер КРС', float(8.5)],
            [None, None,
             f'При всех работах не допускать утечек пластовой жидкости и жидкости глушения. В случае пропуска, разлива,'
             f' немедленно производить зачистку территории.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1],
            [None, None,
             f'Произвести заключительные работы  после ремонта скважины.',
             None, None, None, None, None, None, None,
             'мастер КРС', 1],
            [None, None,
             f'Сдать скважину представителю ЦДНГ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1]]
        return end_list


class DescentNnWithPaker(DescentParent):
    def __init__(self, parent=None):
        super(DescentNnWithPaker, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.extend(jumping_after_sko_list)
        work_list.extend(self.descent_nn_with_paker())

        work_list.extend(self.append_note_6())
        work_list.extend(self.append_finish())

        return work_list

    def descent_nn_with_paker(self):
        from work_py.opressovka import OpressovkaEK

        descent_nn_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'СПО {self.data_well.dict_pump_shgn["after"]} на глубину'
             f' {float(self.data_well.dict_pump_shgn_depth["after"])}м. пакер - '
             f'{self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м ',
             None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить '
             f'сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить {self.data_well.dict_pump_shgn["after"]} на '
             f'гл {float(self.data_well.dict_pump_shgn_depth["after"])}м. '
             f'пакер - {self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м '
             f'(в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {self.nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием  с отбраковкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(self.len_nkt, 1)],
            [f'Посадить пакер на глубине {self.data_well.paker_before["after"]}м.', None,
             f'Демонтировать превентор. Посадить пакер на глубине {self.data_well.paker_before["after"]}м. '
             f'Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[1], None,
             f'{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[0]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае '
             f'поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ '
             f'о невозможности проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить плунжер на компоновке штанг: {self.sucker_edit}м',
             None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.data_well.max_admissible_pressure.get_value}атм.'
             f'Спустить плунжер на компоновке штанг: {self.sucker_edit} '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(self.data_well.dict_pump_shgn_depth["after"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],

        ]
        if self.privyazka_nkt()[0] not in descent_nn_with_paker:
            descent_nn_with_paker.insert(3, self.privyazka_nkt()[0])
        return descent_nn_with_paker


class Conservation(DescentParent):
    def __init__(self, parent=None):
        super(Conservation, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        work_list.extend(self.сonservation_well(self.nkt_edit))
        work_list.extend(self.append_finish())
        return work_list

    def сonservation_down(self, nkt_edit: str) -> List:
        from work_py.alone_oreration import volume_jamming_well, volume_nkt_metal
        volume_well_30 = volume_jamming_well(self, 30) / 1.1
        dict_nkt = {}
        dict_nkt[nkt_edit] = 1

        if '73' in str(nkt_edit):
            volume_nkt_metal = 1.17 * 1.0 / 1000
        elif '60' in str(nkt_edit):
            volume_nkt_metal = 0.87 * 1.0 / 1000
        elif '89' in str(nkt_edit):
            volume_nkt_metal = 1.7 * 1.0 / 1000
        elif '48' in str(nkt_edit):
            volume_nkt_metal = 0.55 * 1.0 / 1000

        length_nkt = volume_well_30 / volume_nkt_metal
        lenght_nkt_descent = length_nkt + sum(list(self.data_well.dict_nkt_after.values()))
        if lenght_nkt_descent > self.data_well.current_bottom:
            lenght_nkt_descent = self.data_well.current_bottom

        descent_voronka = [
            [f'Не замерзающая жидкость 0,3м3', None,
             f'С целью вытеснения тех. жидкости из скважины и заполнения скважины не замерзающей жидкостью: '
             f'Допустить компоновку на технологических НКТ на глубину '
             f'{lenght_nkt_descent:.1f}м. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(length_nkt, 1)],
            [None, None,
             f'Поднять тНКТ до глубины {sum(list(self.data_well.dict_nkt_after.values())):.1f}м '
             f'с доливом незамерзающей'
             f' жидкостью (растворитель РКД 0,3м3) до устья',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(length_nkt, 1)],
            [None, None,
             f'Заполнить полость НКТ в интервале 0-30м незамерзающей жидкостью полость НКТ (растворитель РКД 0,09м3)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1)]]
        return descent_voronka

    def сonservation_well(self, nkt_edit: str):
        descent_voronka = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'СПО воронки {sum(list(self.data_well.dict_nkt_after.values()))}м', None,
             f'Спустить предварительно воронку на НКТ{nkt_edit} (завоз с УСО ГНО, '
             f'ремонтные/новые) на '
             f'гл. {sum(list(self.data_well.dict_nkt_after.values()))}м. Спуск НКТ '
             f'производить с шаблонированием и '
             f'смазкой резьбовых соединений.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1)],

            [None, None,
             'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только '
             'сертифицированное оборудование в коррозионностойком исполнении, снять штурвалы с задвижек, крайние '
             'фланцы задвижек, крайние фланцы задвижек оборудовать заглушками, снять манометры. Установить '
             'паспортизированный подвесной патрубок под планшайбой. Составить АКТ. При несоответствии технических '
             'параметров, отсутствия паспорта, отсутствия сертификата, отсутствие или не читаемости номера и '
             'даты выпуска-подвесного патрубок считается не пригодным к применению. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае поглощения '
             f'при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности проведения '
             f'опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [None, None,
             f'Устье скважины оборудовать оградой размером 2х2м. На устье законсервированных скважин установить '
             f'металлическую табличку с обозначением'
             f'скв.№ {self.data_well.well_number.get_value} {self.data_well.well_area.get_value}'
             f' месторождение, ПАО АНК Башнефть, '
             f'дата начала и окончания консервации силами ЦДНГ после съезда бригады.',
             None, None, None, None, None, None, None,
             'ЦДНГ ', 2],
        ]
        for row in self.сonservation_down(nkt_edit)[::-1]:
            descent_voronka.insert(2, row)
        return descent_voronka


class DescentPaker(DescentParent):
    def __init__(self, parent=None):
        super(DescentPaker, self).__init__(parent)
        self.rgd_question_combo = parent.current_widget.rgd_question_combo.currentText()

    def execute(self) -> List:
        work_list = self.begin_text()
        work_list.extend(self.paker_down())
        work_list.extend(self.append_finish())
        return work_list

    def paker_down(self) -> List:
        from work_py.opressovka import OpressovkaEK
        from work_py.rgdVcht import rgd_with_paker, rgd_without_paker
        paker_descent = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной '
             f'патрубок на сертифицированный. Для опрессовки фондовых НКТ необходимо заявить в '
             f'ЦДНГ за 24 часа клапан А-КСШ-89-48-30. По согласованию с ТС и ГС настроить клапан '
             f'А-КСШ-89-48-30 на необходимое давление (1,5 кратное от планируемого '
             f'давления закачки) открытия путем регулирования количества срезных винтов. \n'
             f'Перед спуском подрядчик ТКРС определяет статический уровень Нст (эхолот подрядчика ТКРС, '
             f'при необходимости Нст определяется заказчиком)  и согласовывает с заказчиком (ЦДНГ, ПТО) давление '
             f'опрессовки НКТ и срезки винтов (открытие клапана). По результатам расчета давления открытия клапана '
             f'(согласованный с заказчиком), подрядчик производит отворот необходимого количества винтов. '
             f'(согласно паспорта клапана А-КСШ-89-48-30)',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [f'Спуск с пакером {self.data_well.paker_before["after"]} '
             f'на глубину {self.data_well.depth_fond_paker_before["after"]}м,'
             f' воронку на {int(float(sum(self.data_well.dict_nkt_after.values())))}м.',
             None,
             f'Спустить подземное оборудование  согласно расчету и карте спуска ЦДНГ '
             f'НКТ с пакером {self.data_well.paker_before["after"]} '
             f'на глубину {self.data_well.depth_fond_paker_before["after"]}м, воронку на глубину '
             f'{round(sum(self.data_well.dict_nkt_after.values()), 1)}м. '
             f'(Компоновку НКТ{self.nkt_edit}м) '
             f'прошаблонировать для проведения ГИС.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sum(self.data_well.dict_nkt_after.values()), 1.2)],
            [f'Посадить пакер на глубине {self.data_well.depth_fond_paker_before["after"]}м', None,
             f'Демонтировать превентор. Посадить пакер на глубине '
             f'{self.data_well.depth_fond_paker_before["after"]}м. '
             f'Отревизировать и ориентировать планшайбу для проведения ГИС. '
             f'Заменить и установить устьевую арматуру для ППД. Обвязать с нагнетательной линией.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.25 + 0.5 + 0.5],
            [f'{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[1]}', None,
             f'{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[0]}',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае поглощения '
             f'при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности проведения '
             f'опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
        ]
        work_list_depth = self.insert_text_depth_paker_1000(self.data_well.depth_fond_paker_before["after"])
        if work_list_depth:
            paker_descent.insert(-2, work_list_depth[0])

        if self.need_privyazka_nkt():
            if self.privyazka_nkt()[0] not in paker_descent:
                paker_descent.insert(2, self.privyazka_nkt()[0])

        if self.rgd_question_combo == 'Да':
            if self.data_well.column_additional and self.data_well.depth_fond_paker_before['after'] >= self.data_well.head_column_additional.get_value:
                # print(rgd_without_paker(self))
                for row in rgd_without_paker(self)[::-1]:
                    paker_descent.insert(0, row)
            else:
                for row in rgd_with_paker(self):
                    paker_descent.append(row)
        else:
            QMessageBox.warning(None, 'РГД не проводиться', 'При не проведении РГД при бригаде кислотную обработку '
                                                            'нужно запланировать на фондовом НКТ с обранной арматурой')
        return paker_descent


class DescentVoronka(DescentParent):
    def __init__(self, parent=None):
        super(DescentVoronka, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        work_list.extend(self.voronka_down(self.nkt_edit))
        work_list.extend(self.append_finish())
        return work_list

    def voronka_down(self, nkt_edit: str) -> List:
        descent_voronka = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             f'В случае не завоза новых или завоза не опрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ, '
             f'произвести спуск '
             f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'СПО воронки {self.len_nkt}м', None,
             f'Спустить предварительно воронку на НКТ{nkt_edit} (завоз с УСО ГНО, '
             f'ремонтные/новые) на '
             f'гл. {self.len_nkt}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(self.len_nkt, 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'произвести разделку'
             f' кабеля под устьевой сальник произвести герметизацию устья. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае '
             f'поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности '
             f'проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
        ]
        return descent_voronka


class DescentOrz(DescentParent):
    def __init__(self, parent=None):
        super(DescentOrz, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        work_list.extend(self.descent_orz())
        work_list.extend(self.append_finish())
        return work_list

    def descent_orz(self):
        descent_orz = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             f'В случае не завоза новых или завоза не опрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ,'
             f'произвести спуск '
             f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'СПО двух пакерную компоновку ОРЗ на НКТ89', None,
             f'Спустить двух пакерную компоновку ОРЗ на НКТ89  '
             f'(завоз с УСО ГНО, '
             f'ремонтные/новые) '
             f'на гл. {self.data_well.depth_fond_paker_before["after"]}/'
             f'{float(self.data_well.depth_fond_paker_second_before["after"])}м. '
             f'Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(self.data_well.depth_fond_paker_before["after"], 1.2)],
            [f'Привязка', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через РИТС {data_list.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №11 утвержденной главным инженером '
             f' {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры согласно схемы ОРЗ. При монтаже использовать только '
             f'сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'Закачать в меж трубное пространство раствор ингибитора коррозии. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [None, None,
             f'Опрессовать пакер и ЭК и арматуру ППД на Р= '
             f'{self.data_well.max_admissible_pressure.get_value}атм с открытым '
             f'трубном пространством '
             f'в присутствии представителя заказчика на наличие перетоков.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии'
             f' представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), '
             f'в случае поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ '
             f'о невозможности проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [None, None,
             f'Спустить стыковочное устройство на НКТ48мм до глубины '
             f'{float(self.data_well.depth_fond_paker_second_before["after"])}м '
             f'с замером и шаблонированием. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(float(self.data_well.depth_fond_paker_second_before["after"]), 1)],
            [None, None,
             f'Произвести стыковку. Смонтировать арматуру ОРЗ. Опрессовать пакер и арматуру ОРЗ в '
             f'меж трубное пространство'
             f' на Р= {self.data_well.max_admissible_pressure.get_value}атм с открытым трубном пространством '
             f'в присутствии представителя заказчика на наличие перетоков.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести насыщение скважины в объеме не менее 5м3 в НКТ48мм. Произвести определение приемистости при '
             f'давлении 100атм в присутствии '
             f'представителя заказчика. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67 + 0.2 + 0.17],
            [None, None,
             f'Произвести насыщение скважины в объеме не менее 5м3 в меж трубное пространство. Произвести определение '
             f'приемистости при давлении 100атм в присутствии '
             f'представителя заказчика. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67 + 0.2 + 0.17],
            [None, None,
             f'Согласовать с заказчиком завершение скважины.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

        ]
        return descent_orz


class DescentORD(DescentParent):
    def __init__(self, parent=None):
        super(DescentORD, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.extend(jumping_after_sko_list)
        work_list.extend(self.descent_ord())
        work_list.extend(self.append_note_6())
        work_list.extend(self.append_finish())
        return work_list

    def descent_ord(self) -> List:
        from work_py.opressovka import OpressovkaEK
        descent_ord_list = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             'При монтаже УЭЦН провести резьбы: ловильной головки ЭЦН, обратного и сбивного '
             'клапанов. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [None, None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ), '
             f'комплект НКТ. В ЦДНГ '
             f'заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [f'СПО {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit} c пакером '
             f'{self.data_well.paker_before["after"]}',
             None,
             f'Спустить предварительно {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit} '
             f'c пакером {self.data_well.paker_before["after"]} на'
             f' глубину {self.data_well.depth_fond_paker_before["after"]}м'
             f'(завоз с УСО ГНО, ремонтные/новые) на гл. {self.data_well.dict_pump_ecn_depth["after"]}м. '
             f'Спуск НКТ производить с '
             f'шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1.2)],
            [OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[0], None,
             f'Демонтировать превентор. Посадить пакер на глубине '
             f'{self.data_well.depth_fond_paker_before["after"]}м. Монтаж '
             f'устьевой арматуры. При монтаже использовать только сертифицированное '
             f'оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.'
             f' произвести '
             f'разделку'
             f' кабеля под устьевой сальник '
             f'произвести герметизацию устья. '
             f'\n{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[1]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае '
             f'поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ '
             f'о невозможности проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'СПО {self.data_well.dict_pump_shgn["after"]} на компоновке штанг', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг'
             f' (ПМШ 62х21 либо аналог). Опрессовать ПВО на'
             f' {self.data_well.max_admissible_pressure.get_value}атм.'
             f'Спустить {self.data_well.dict_pump_shgn["after"]} на компоновке штанг: '
             f'{self.sucker_edit}  Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(self.data_well.dict_pump_ecn_depth["after"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика с'
             f' помощью ЦА-320 '
             f'(составить акт). Предоставить Заказчику замер НКТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5]]

        if self.privyazka_nkt()[0] not in descent_ord_list:
            descent_ord_list.insert(4, self.privyazka_nkt()[0])
        return descent_ord_list


class DescentNv(DescentParent):
    def __init__(self, parent=None):
        super(DescentNv, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()

        work_list.extend(self.descent_nv())
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.insert(-4, jumping_after_sko_list)
        work_list.extend(self.append_finish())
        return work_list

    def descent_nv(self) -> List:
        descent_nv = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной'
             f' патрубок на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'спустить замковую опору на гл {self.data_well.dict_pump_shgn_depth["after"]}м', None,
             f'Заявить  комплект подгоночных штанг, полированный шток (вывоз согласовать с ТС ЦДНГ). '
             f'В ЦДНГ заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на '
             f'гл {self.data_well.dict_pump_shgn_depth["after"]}м. (в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {self.nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием с отбраковкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать '
             f'только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67 + 0.5],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в'
             f' присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), '
             f'в случае поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ о '
             f'невозможности проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить {self.data_well.dict_pump_shgn["after"]} на'
             f' {self.sucker_edit}'
                , None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.data_well.max_admissible_pressure.get_value}атм.'
             f'Спустить {self.data_well.dict_pump_shgn["after"]} на компоновке штанг: '
             f'{self.sucker_edit}  '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(self.data_well.dict_pump_shgn_depth["after"]))],
            [None, None,
             f'Перед пуском произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
        ]
        return descent_nv


class DescentEcnWithPaker(DescentParent):
    def __init__(self, parent=None):
        super(DescentEcnWithPaker, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.extend(jumping_after_sko_list)
        work_list.extend(self.descent_ecn_with_paker())
        work_list.extend(self.append_finish())
        return work_list

    def descent_ecn_with_paker(self) -> List:
        from work_py.opressovka import OpressovkaEK
        descent_ecn_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной '
             f'патрубок на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             ,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [f'СПО {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit}, '
             f'пакер - {self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м',
             None,
             f'Спустить предварительно {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit}, '
             f'пакер - {self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м. (завоз с УСО ГНО,'
             f' ремонтные/новые) '
             f'на гл. {self.data_well.dict_pump_ecn_depth["after"]}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(float(self.data_well.dict_pump_ecn_depth["after"]), 1.2)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'произвести разделку'
             f' кабеля под устьевой сальник '
             f'произвести герметизацию устья. Опрессовать кабельный ввод устьевой арматуры',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае поглощения '
             f'при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности проведения '
             f'опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[1], None,
             f'{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[0]} '
             f'Опрессовать кабельный '
             f'ввод устьевой арматуры',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Перед пуском УЭЦН опрессовать ГНО на 50атм в течении 30 минут в присутствии представителя заказчика с '
             f'помощью ЦА-320 '
             f'(составить акт). Предоставить Заказчику замер НКТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1],
        ]
        return descent_ecn_with_paker


class DescentEcn(DescentParent):
    def __init__(self, parent=None):
        super(DescentEcn, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.extend(jumping_after_sko_list)
        work_list.extend(self.descent_ecn())
        work_list.extend(self.append_finish())
        return work_list

    def descent_ecn(self) -> List:
        descent_ecn = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            ['Опрессовать НКТ между УЭЦН и обратным клапаном', None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [f'СПО {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit} на '
             f'гл. {self.data_well.dict_pump_ecn_depth["after"]}м', None,
             f'Спустить предварительно {self.data_well.dict_pump_ecn["after"]} на НКТ{self.nkt_edit} '
             f'(завоз с УСО ГНО, ремонтные/новые) на '
             f'гл. {self.data_well.dict_pump_ecn_depth["after"]}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(float(self.data_well.dict_pump_ecn_depth["after"]), 1.2)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'произвести разделку'
             f' кабеля под устьевой сальник '
             f'произвести герметизацию устья. Опрессовать кабельный ввод устьевой арматуры',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), '
             f'в случае поглощения при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ '
             f'о невозможности проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [None, None,
             f'Перед пуском УЭЦН опрессовать ГНО на 50атм в течении 30 минут в присутствии представителя '
             f'заказчика с помощью ЦА-320 '
             f'(составить акт). Предоставить Заказчику замер НКТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1],
        ]
        return descent_ecn


class DescentNvWithPaker(DescentParent):
    def __init__(self, parent=None):
        super(DescentNvWithPaker, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.extend(jumping_after_sko_list)
        work_list.extend(self.descent_nv_with_paker())
        work_list.extend(self.append_note_6())
        work_list.extend(self.append_finish())
        return work_list

    def descent_nv_with_paker(self):
        from work_py.opressovka import OpressovkaEK
        descent_nv_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [f'СПО з.о. на гл {float(self.data_well.dict_pump_shgn_depth["after"])}м. пакер - '
             f'{self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м ',
             None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). '
             f'В ЦДНГ заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на гл '
             f'{float(self.data_well.dict_pump_shgn_depth["after"])}м. (в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {self.nkt_edit} пакер - {self.data_well.paker_before["after"]} на глубину '
             f'{self.data_well.depth_fond_paker_before["after"]}м  (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1.2)],

            [None, None,
             f'Демонтировать превентор. Посадить пакер на глубине '
             f'{self.data_well.depth_fond_paker_before["after"]}м. '
             f'Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО '
             f'ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[0], None,
             f'{OpressovkaEK.testing_pressure(self, self.data_well.depth_fond_paker_before["after"])[1]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае поглощения '
             f' при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности проведения '
             f'опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить {self.data_well.dict_pump_shgn["after"]} на компоновке штанг:'
             f' {self.sucker_edit}', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при'
             f' СПО штанг (ПМШ 62х21 либо аналог). '
             f'Опрессовать ПВО на {self.data_well.max_admissible_pressure.get_value}атм.'
             f'Спустить {self.data_well.dict_pump_shgn["after"]} на компоновке штанг: '
             f'{self.sucker_edit}  Окончательный компоновку штанг '
             f'производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: '
             f'АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(self.data_well.dict_pump_shgn_depth["after"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
        ]
        if self.privyazka_nkt()[0] not in descent_nv_with_paker:
            descent_nv_with_paker.insert(3, self.privyazka_nkt()[0])
        return descent_nv_with_paker


class DescentNn(DescentParent):
    def __init__(self, parent=None):
        super(DescentNn, self).__init__(parent)

    def execute(self) -> List:
        work_list = self.begin_text()

        work_list.extend(self.descent_nn())
        jumping_after_sko_list = self.jumping_after_sko()
        if jumping_after_sko_list:
            work_list.insert(-4, jumping_after_sko_list)
        work_list.extend(self.append_note_6())
        work_list.extend(self.append_finish())
        return work_list

    def descent_nn(self):
        descent_nn = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок '
             f'на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             self.calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [
                f'спустить {self.data_well.dict_pump_shgn["after"]} на глубина'
                f' {float(self.data_well.dict_pump_shgn_depth["after"])}м',
                None,
                f'Заявить комплект подгоночных штанг, полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить '
                f'сальниковые '
                f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
                f'Предварительно, по согласованию с ЦДНГ, спустить '
                f'{self.data_well.dict_pump_shgn["after"]} на гл '
                f'{float(self.data_well.dict_pump_shgn_depth["after"])}м. (в компоновке предусмотреть установку '
                f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
                f'компоновка НКТ: {self.nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
                f' спуск ФНКТ произвести с шаблонированием  с отбраковкой',
                None, None, None, None, None, None, None,
                'Мастер КРС, предст. заказчика',
                descentNKT_norm(sum(list(self.data_well.dict_nkt_after.values())), 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {self.data_well.max_admissible_pressure.get_value}атм в присутствии '
             f'представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эксплуатационной колонны), в случае поглощения'
             f' при опрессовке ФА, совместно с представителем ЦДНГ составляется АКТ  о невозможности '
             f'проведения опрессовки ФА',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить плунжер на компоновке штанг:'
             f' {self.sucker_edit}', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.data_well.max_admissible_pressure.get_value}атм.'
             f'Спустить плунжер на компоновке штанг: {self.sucker_edit} '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(self.data_well.dict_pump_shgn_depth["after"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтировать ПШ+СУСГ.\n'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью '
             f'y={self.data_well.fluid_work};'
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с'
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести Обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору; '
             f'смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм -'
             f' время опрессовки 15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию'
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]
        ]
        return descent_nn

     
