import well_data
from work_py.alone_oreration import privyazkaNKT
from .rationingKRS import descentNKT_norm, descent_sucker_pod
from .calc_fond_nkt import CalcFond
from .template_work import TemplateKrs
from PyQt5.QtWidgets import  QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton


class TabPage_Gno(QWidget):
    def __init__(self):
        super().__init__()

        self.nkt_label = QLabel('компоновка НКТ')
        self.nkt_edit = QLineEdit(self)
        self.nkt_edit.setText(f'{self.gno_nkt_opening(well_data.dict_nkt_po)}')

        self.gno_label = QLabel("вид спускаемого ГНО", self)
        self.gno_combo = QComboBox(self)
        gno_list = ['пакер', 'ОРЗ', 'ОРД', 'воронка', 'НН с пакером', 'НВ с пакером',
                    'ЭЦН с пакером', 'ЭЦН', 'НВ', 'НН']

        self.rgd_question_label = QLabel("проведение РГД", self)
        self.rgd_question_combo = QComboBox(self)
        self.rgd_question_combo.addItems(['Да', 'Нет'])

        self.sucker_label = QLabel('компоновка штанг')
        self.sucker_edit = QLineEdit(self)
        self.sucker_edit.setText(f'{self.gno_nkt_opening(well_data.dict_sucker_rod_po)}')

        self.distance_between_nkt_label = QLabel('Расстояние между НКТ')
        self.distance_between_nkt_edit = QLineEdit(self)
        self.distance_between_nkt_edit.setText(f'{300}')

        self.gno_combo.addItems(gno_list)

        lift_key = self.select_gno()

        self.grid = QGridLayout(self)
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
        self.need_juming_after_sko_combo.addItems(['Да', 'Нет'])
        self.grid.addWidget(self.need_juming_after_sko_label, 4, 7)
        self.grid.addWidget(self.need_juming_after_sko_combo, 5, 7)

        if well_data.region != 'КГМ':
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
            str_gno += f'{nkt}мм - {round(float(length_nkt), 1)}м, '
        return str_gno[:-3]

    @staticmethod
    def select_gno():

        if well_data.if_None(well_data.dict_pump_ECN["posle"]) != 'отсут' and \
                well_data.if_None(well_data.dict_pump_SHGN["posle"]) != 'отсут':
            lift_key = 'ОРД'
        elif well_data.if_None(well_data.dict_pump_ECN["posle"]) != 'отсут' and \
                well_data.if_None(well_data.paker_do["posle"]) == 'отсут':
            lift_key = 'ЭЦН'
        elif well_data.if_None(well_data.dict_pump_ECN["posle"]) != 'отсут' and \
                well_data.if_None(well_data.paker_do["posle"]) != 'отсут':
            lift_key = 'ЭЦН с пакером'
        elif well_data.if_None(well_data.dict_pump_SHGN["posle"]) != 'отсут' and \
                well_data.dict_pump_SHGN["posle"].upper() != 'НН' \
                and well_data.if_None(well_data.paker_do["posle"]) == 'отсут':
            lift_key = 'НВ'
        elif well_data.if_None(well_data.dict_pump_SHGN["posle"]) != 'отсут' and \
                well_data.if_None(well_data.dict_pump_SHGN["posle"]).upper() != 'НН' \
                and well_data.if_None(well_data.paker_do["posle"]) != 'отсут':
            lift_key = 'НВ с пакером'
        elif 'НН' in well_data.if_None(well_data.dict_pump_SHGN["posle"]).upper() \
                and well_data.if_None(well_data.paker_do["posle"]) == 'отсут':
            lift_key = 'НН'
        elif 'НН' in well_data.if_None(well_data.dict_pump_SHGN["posle"]).upper() and \
                well_data.if_None(well_data.if_None(well_data.paker_do["posle"])) != 'отсут':
            lift_key = 'НН с пакером'
        elif well_data.if_None(well_data.dict_pump_SHGN["posle"]) == 'отсут' and \
                well_data.if_None(well_data.paker_do["posle"]) == 'отсут' \
                and well_data.if_None(well_data.dict_pump_ECN["posle"]) == 'отсут':
            lift_key = 'воронка'
        elif '89' in well_data.dict_nkt.keys() and '48' in well_data.dict_nkt.keys() and \
                well_data.if_None(
                    well_data.paker_do["posle"]) != 'отсут':
            lift_key = 'ОРЗ'
        elif well_data.if_None(well_data.dict_pump_SHGN["posle"]) == 'отсут' and \
                well_data.if_None(well_data.paker_do["posle"]) != 'отсут' \
                and well_data.if_None(well_data.dict_pump_ECN["posle"]) == 'отсут':
            lift_key = 'пакер'

        return lift_key


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_Gno(), 'Спуск ГНО')


class GnoDescentWindow(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(GnoDescentWindow, self).__init__(parent)
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
        from main import MyWindow

        lift_key = str(self.tabWidget.currentWidget().gno_combo.currentText())
        nkt_edit = self.tabWidget.currentWidget().nkt_edit.text()
        sucker_edit = self.tabWidget.currentWidget().sucker_edit.text()
        distance_between_nkt_edit = self.tabWidget.currentWidget().distance_between_nkt_edit.text()
        if distance_between_nkt_edit != '':
            distance_between_nkt_edit = int(float(distance_between_nkt_edit))

        if well_data.region == 'КГМ':
            need_juming_after_sko_combo = self.tabWidget.currentWidget().need_juming_after_sko_combo.currentText()
        else:
            need_juming_after_sko_combo = 'Нет'
        if lift_key == 'пакер':
            if well_data.depth_fond_paker_do["posle"] > well_data.template_depth and \
                    (well_data.column_additional is False or \
                     (well_data.column_additional and \
                      well_data.current_bottom < well_data.head_column_additional._value)):

                QMessageBox.critical(self, 'Ошибка',
                                           f'Нельзя спускать пакер {well_data.depth_fond_paker_do["posle"]}м'
                                           f'ниже глубины шаблонирования ЭК {well_data.template_depth}м')
                return
            elif well_data.depth_fond_paker_do["posle"] < well_data.head_column_additional._value and \
                    well_data.depth_fond_paker_do["posle"] > well_data.template_depth and well_data.column_additional:
                mes = QMessageBox.critical(self, 'Ошибка',
                                           f'Нельзя спускать пакер {well_data.depth_fond_paker_do["posle"]}м'
                                           f'ниже глубины шаблонирования ЭК {well_data.template_depth}м')
                return
            elif well_data.depth_fond_paker_do["posle"] > well_data.head_column_additional._value and \
                    well_data.depth_fond_paker_do["posle"] > well_data.template_depth_addition \
                    and well_data.column_additional:
                mes = QMessageBox.critical(self, 'Ошибка',
                                           f'Нельзя спускать пакер {well_data.depth_fond_paker_do["posle"]}м'
                                           f'ниже глубины шаблонирования ЭК '
                                           f'{well_data.template_depth_addition}м')
                return
            rgd_question_combo = self.tabWidget.currentWidget().rgd_question_combo.currentText()
            work_list = self.paker_down(nkt_edit, rgd_question_combo)
        elif lift_key == 'воронка':
            work_list = self.voronka_down(lift_key, nkt_edit)
        else:
            if lift_key in ['ОРД', 'ЭЦН с пакером', 'ЭЦН']:
                # print(f'ЭЦН, Шаблон {well_data.dict_pump_ECN_h["posle"], well_data.template_depth}')
                if well_data.dict_pump_ECN_h["posle"] > well_data.template_depth and \
                        (well_data.column_additional is False or \
                         (well_data.column_additional and \
                          well_data.current_bottom > well_data.head_column_additional._value and \
                          well_data.dict_pump_ECN_h["posle"] < well_data.head_column_additional._value)):
                    mes = QMessageBox.critical(self, 'Ошибка', f'Нельзя спускать ЭЦН {well_data.paker_do["posle"]}м'
                                                               f'ниже глубины шаблонирования ЭК {well_data.template_depth}м')
                    return
                elif well_data.dict_pump_ECN_h["posle"] < well_data.head_column_additional._value and \
                        well_data.dict_pump_ECN_h["posle"] > well_data.template_depth and well_data.column_additional:
                    mes = QMessageBox.critical(self, 'Ошибка', f'Нельзя спускать ЭЦН {well_data.paker_do["posle"]}м'
                                                               f'ниже глубины шаблонирования ЭК {well_data.template_depth}м')
                    return
                elif well_data.dict_pump_ECN_h["posle"] > well_data.head_column_additional._value and \
                        well_data.dict_pump_ECN_h[
                            "posle"] > well_data.template_depth_addition and well_data.column_additional:
                    mes = QMessageBox.critical(self, 'Ошибка', f'Нельзя спускать ЭЦН {well_data.paker_do["posle"]}м'
                                                               f'ниже глубины шаблонирования ЭК '
                                                               f'{well_data.template_depth_addition}м')
                    return

            work_list = self.gno_down(lift_key, nkt_edit, sucker_edit, distance_between_nkt_edit, need_juming_after_sko_combo)

        for row in self.end_list:
            work_list.append(row)

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def paker_down(self, nkt_edit, rgd_question_combo, sucker_edit='', need_juming_after_sko_combo='Нет'):
        from work_py.opressovka import OpressovkaEK
        from .rgdVcht import rgdWithPaker, rgdWithoutPaker
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
            [f'Спуск с пакером {well_data.paker_do["posle"]} '
             f'на глубину {well_data.depth_fond_paker_do["posle"]}м,'
             f' воронку на {int(float(sum(well_data.dict_nkt_po.values())))}м.',

             None,
             f'Спустить подземное оборудование  согласно расчету и карте спуска ЦДНГ '
             f'НКТ с пакером {well_data.paker_do["posle"]} '
             f'на глубину {well_data.depth_fond_paker_do["posle"]}м, воронку на глубину '
             f'{round(sum(well_data.dict_nkt_po.values()), 1)}м. '
             f'(Компоновку НКТ{nkt_edit}м) '
             f'прошаблонировать для проведения ГИС.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(sum(well_data.dict_nkt_po.values()), 1.2)],
            [f'Посадить пакер на глубине {well_data.depth_fond_paker_do["posle"]}м', None,
             f'Демонтировать превентор. Посадить пакер на глубине {well_data.depth_fond_paker_do["posle"]}м. '
             f'Отревизировать и ориентировать планшайбу для проведения ГИС. '
             f'Заменить и установить устьевую арматуру для ППД. Обвязать с нагнетательной линией.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.25 + 0.5 + 0.5],
            [f'{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[1]}', None,
             f'{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[0]}',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
        ]

        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(well_data.depth_fond_paker_do["posle"]))) < 10 or abs(
                        float(interval[0] - float(well_data.depth_fond_paker_do["posle"]))) < 10:
                    if privyazkaNKT(self)[0] not in paker_descent:
                        paker_descent.insert(2, privyazkaNKT(self)[0])

        if rgd_question_combo == 'Да':
            if well_data.column_additional and well_data.depth_fond_paker_do[
                'posle'] >= well_data.head_column_additional._value:
                # print(rgdWithoutPaker(self))
                for row in rgdWithoutPaker(self)[::-1]:
                    paker_descent.insert(0, row)
            else:
                for row in rgdWithPaker(self):
                    paker_descent.append(row)
        return paker_descent

    def voronka_down(self, lift_key, nkt_edit):

        descent_voronka = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ, '
             f'произвести спуск '
             f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [f'СПО воронки {sum(list(well_data.dict_nkt_po.values()))}м', None,
             f'Спустить предварительно воронку на НКТ{nkt_edit} (завоз с УСО ГНО, '
             f'ремонтные/новые) на '
             f'гл. {sum(list(well_data.dict_nkt_po.values()))}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'произвести разделку'
             f' кабеля под устьевой сальник произвести герметизацию устья. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
        ]
        return descent_voronka

    def gno_down(self, lift_key, nkt_edit, sucker_edit, distance_between_nkt_edit, need_juming_after_sko_combo='Нет'):

        from .opressovka import OpressovkaEK

        gno_list = [
            [None, None,
             f'За 48 часов до спуска запросить КАРТУ спуска на ГНО и заказать оборудование согласно карты спуска.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None]
        ]

        # print(f'ключ {lift_key}')
        if lift_key in ['ЭЦН', 'НВ', 'НН', 'НН с пакером', 'ЭЦН с пакером', 'НВ с пакером', 'ОРД']:
            calc_fond_nkt_str = self.calc_fond_nkt(sum(list(well_data.dict_nkt_po.values())), distance_between_nkt_edit)
        else:
            calc_fond_nkt_str = None

        descent_nv = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной'
             f' патрубок на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'спустить замковую опору на гл {well_data.dict_pump_SHGN_h["posle"]}м', None,
             f'Заявить  комплект подгоночных штанг, полированный шток (вывоз согласовать с ТС ЦДНГ). '
             f'В ЦДНГ заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на '
             f'гл {well_data.dict_pump_SHGN_h["posle"]}м. (в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием с отбраковкой с калибровкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать '
             f'только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67 + 0.5],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить {well_data.dict_pump_SHGN["posle"]} на'
             f' {sucker_edit}'
                , None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{well_data.max_admissible_pressure._value}атм.'
             f'Спустить {well_data.dict_pump_SHGN["posle"]} на компоновке штанг: '
             f'{sucker_edit}  '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descent_sucker_pod(float(well_data.dict_pump_SHGN_h["posle"]))],
            [None, None,
             f'Перед пуском произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтироваь ПШ+СУСГ.\n'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью '
             f'y={well_data.fluid_work}; '
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с '
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести Обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору; '
             f'смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм - время '
             f'опрессовки 15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию '
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]
        ]

        descent_nn = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок '
             f'на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [f'спустить {well_data.dict_pump_SHGN["posle"]} на гл {float(well_data.dict_pump_SHGN_h["posle"])}м',
             None,
             f'Заявить комплект подгоночных штанг, полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить '
             f'сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить {well_data.dict_pump_SHGN["posle"]} на гл '
             f'{float(well_data.dict_pump_SHGN_h["posle"])}м. (в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1)],
            [None, None,
             f'Демонтировать превентор. Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить плунжер на компоновке штанг:'
             f' {sucker_edit}', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{well_data.max_admissible_pressure._value}атм.'
             f'Спустить плунжер на компоновке штанг: {sucker_edit} '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descent_sucker_pod(float(well_data.dict_pump_SHGN_h["posle"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтироваь ПШ+СУСГ.\n'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью y={well_data.fluid_work};'
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с'
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести Обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору; смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм - время опрессовки 15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию'
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]
        ]

        descent_nv_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [f'СПО з.о. на гл {float(well_data.dict_pump_SHGN_h["posle"])}м. пакер - '
             f'{well_data.paker_do["posle"]} на глубину {well_data.depth_fond_paker_do["posle"]}м ',
             None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). '
             f'В ЦДНГ заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на гл '
             f'{float(well_data.dict_pump_SHGN_h["posle"])}м. (в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {nkt_edit} пакер - {well_data.paker_do["posle"]} на глубину '
             f'{well_data.depth_fond_paker_do["posle"]}м  (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1.2)],

            [None, None,
             f'Демонтировать превентор. Посадить пакер на глубине {well_data.depth_fond_paker_do["posle"]}м. '
             f'Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО '
             f'ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.27],
            [OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[0], None,
             f'{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[1]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить {well_data.dict_pump_SHGN["posle"]} на компоновке штанг:'
             f' {sucker_edit}', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). '
             f'Опрессовать ПВО на {well_data.max_admissible_pressure._value}атм.'
             f'Спустить {well_data.dict_pump_SHGN["posle"]} на компоновке штанг: '
             f'{sucker_edit}  Окончательный компоновку штанг '
             f'производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: '
             f'АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(well_data.dict_pump_SHGN_h["posle"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:\n'
             f'1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтироваь ПШ+СУСГ.при необходимости сорвать пакер'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью y={well_data.fluid_work};'
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с'
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору; смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм - время опрессовки 15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию'
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]
        ]
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(well_data.depth_fond_paker_do["posle"]))) < 10 or abs(
                        float(interval[0] - float(well_data.depth_fond_paker_do["posle"]))) < 10:
                    if privyazkaNKT(self)[0] not in descent_nv_with_paker:
                        descent_nv_with_paker.insert(3, privyazkaNKT(self)[0])

        descent_nn_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            [f'СПО {well_data.dict_pump_SHGN["posle"]} на гл {float(well_data.dict_pump_SHGN_h["posle"])}м. пакер - '
             f'{well_data.paker_do["posle"]} на глубину {well_data.depth_fond_paker_do["posle"]}м ',
             None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить '
             f'сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n'
             f'Предварительно, по согласованию с ЦДНГ, спустить {well_data.dict_pump_SHGN["posle"]} на '
             f'гл {float(well_data.dict_pump_SHGN_h["posle"])}м. '
             f'пакер - {well_data.paker_do["posle"]} на глубину {well_data.depth_fond_paker_do["posle"]}м '
             f'(в компоновке предусмотреть установку '
             f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
             f'компоновка НКТ: {nkt_edit} (завоз с УСО ГНО, ремонтные/новые).\n'
             f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1)],
            [f'Посадить пакер на глубине {well_data.paker_do["posle"]}м.', None,
             f'Демонтировать превентор. Посадить пакер на глубине {well_data.paker_do["posle"]}м. '
             f'Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[1], None,
             f'{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[0]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'Спустить плунжер на компоновке штанг: {sucker_edit}м',
             None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{well_data.max_admissible_pressure._value}атм.'
             f'Спустить плунжер на компоновке штанг: {sucker_edit} '
             f'Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика',
             descent_sucker_pod(float(well_data.dict_pump_SHGN_h["posle"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5],
            [None, None,
             f'ПРИМЕЧАНИЕ №6: Опробовать работу ШГН НВ, при отрицательном результате произвести реанимационные работы '
             f'по следующему алгоритму:\n'
             f'1. Разобрать СУСГ, сорвать насос с замковой опоры (ом), демонтироваь ПШ+СУСГ.при необходимости сорвать пакер'
             f'2. Произвести подъем 2 штанг (порядка 16-19м), установить ПШ+СУСГ, '
             f'смонтировать тройник с задвижкой с БРС под СУСГ\n'
             f'3. Смонтировать ЦA-320 к ВУС на УА (центральная задвижка); обвязываем затрубное пространство с ЕДК;\n'
             f'4. Закачка растворителя в объеме не менее V= 1 м3, произвести доводку тех.жидкостью y={well_data.fluid_work};'
             f'При доведении растворителя во время закачки тех. жидкости одновременно производим расхаживание насоса с'
             f'помощью ПА ,на длину L= Lпш-1м;\n'
             f'5. После завершения закачки, центральную задвижку закрыть, продолжить поступательные движения для '
             f'промывки клапанов в течении 30 минут.\n'
             f'6. Реагирование 2ч\n'
             f'7. Произвести обратную промывку круговой циркуляцией\n'
             f'8. Демонтировать СУСГ+ПШ; Спуск 2 шт. ШН, установить ПШ; посадить насос в замковую опору; смонтировать СУСГ;\n'
             f'9.Произвести пробный вызов подачи и опрессовку насоса при помощи ПА на 40атм - время опрессовки 15 мин; снять динамограмму. '
             f'При положительном результате сдать скважину (устьевую арматуру, устьевую площадку, территорию'
             f'обваловки) в надлежащем состоянии представителю ЦДНГ по акту.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 11.5]
        ]
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - float(well_data.depth_fond_paker_do["posle"]))) < 10 or abs(
                        float(interval[0] - float(well_data.depth_fond_paker_do["posle"]))) < 10:
                    if privyazkaNKT(self)[0] not in descent_nn_with_paker:
                        descent_nn_with_paker.insert(3, privyazkaNKT(self)[0])
        descentORD = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного '
             'клапанов. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [None, None,
             f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ), комплект НКТ. В ЦДНГ '
             f'заявить сальниковые '
             f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм. \n',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [f'СПО {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit} c пакером '
             f'{well_data.paker_do["posle"]}',
             None,
             f'Спустить предварительно {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit} '
             f'c пакером {well_data.paker_do["posle"]} на'
             f' глубину {well_data.depth_fond_paker_do["posle"]}м'
             f'(завоз с УСО ГНО, ремонтные/новые) на гл. {well_data.dict_pump_ECN_h["posle"]}м. Спуск НКТ производить с '
             f'шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(well_data.dict_nkt_po.values())), 1.2)],
            [OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[0], None,
             f'Демонтировать превентор. Посадить пакер на глубине {well_data.depth_fond_paker_do["posle"]}м. Монтаж '
             f'устьевой арматуры. При монтаже использовать только сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. произвести '
             f'разделку'
             f' кабеля под устьевой сальник '
             f'произвести герметизацию устья. \n{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[1]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [f'СПО {well_data.dict_pump_SHGN["posle"]} на компоновке штанг', None,
             f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на'
             f' {well_data.max_admissible_pressure._value}атм.'
             f'Спустить {well_data.dict_pump_SHGN["posle"]} на компоновке штанг: '
             f'{sucker_edit}  Окончательный компоновку штанг производить по расчету '
             f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
             f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descent_sucker_pod(float(well_data.dict_pump_ECN_h["posle"]))],
            [None, None,
             f'Перед пуском  произвести подгонку штанг и '
             f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика с помощью ЦА-320 '
             f'(составить акт). Предоставить Заказчику замер НКТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.5]]

        descent_orz = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного '
             'клапанов. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [None, None,
             f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ,'
             f'произвести спуск '
             f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [f'СПО двух пакерную компоновку ОРЗ на НКТ89', None,
             f'Спустить двух пакерную компоновку ОРЗ на НКТ89  '
             f'(завоз с УСО ГНО, '
             f'ремонтные/новые) '
             f'на гл. {well_data.depth_fond_paker_do["posle"]}/{float(well_data.depth_fond_paker2_do["posle"])}м. '
             f'Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(well_data.depth_fond_paker_do["posle"], 1.2)],
            [f'Привязка', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {well_data.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
             f' {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [None, None,
             f'Демонтировать превентор. Монтаж устьевой арматуры согласно схемы ОРЗ. При монтаже использовать только '
             f'сертифицированное'
             f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
             f'акачать в межтрубное пространство раствор ингибитора коррозии. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1.77],
            [None, None,
             f'Опрессовать пакер и ЭК и арматуру ППД на Р= {well_data.max_admissible_pressure._value}атм с открытым '
             f'трубном пространством '
             f'в присутствии представителя заказчика на наличие перетоков.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести опрессовку фонтанной арматуры после монтажа на устье скважины '
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [None, None,
             f'Спустить стыковочное устройство на НКТ48мм до глубины {float(well_data.depth_fond_paker2_do["posle"])}м '
             f'с замером и шаблонированием. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(float(well_data.depth_fond_paker2_do["posle"]), 1)],
            [None, None,
             f'Произвести стыковку. Смонтировать арматуру ОРЗ. Опрессовать пакер и арматуру ОРЗ в межтрубное пространство'
             f' на Р= {well_data.max_admissible_pressure._value}атм с открытым трубном пространством '
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
             f'Произвести насыщение скважины в объеме не менее 5м3 в межтрубное пространство. Произвести определение '
             f'приемистости при давлении 100атм в присутствии '
             f'представителя заказчика. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.67 + 0.2 + 0.17],
            [None, None,
             f'Согласовать с заказчиком завершение скважины.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

        ]
        # except:
        #     descent_orz = ''
        descent_ecn = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на '
             f'сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],

            ['Опрессовать НКТ между УЭЦН и обратным клапаном', None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного клапанов. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [f'СПО {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit} на '
             f'гл. {well_data.dict_pump_ECN_h["posle"]}м', None,
             f'Спустить предварительно {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit} '
             f'(завоз с УСО ГНО, ремонтные/новые) на '
             f'гл. {well_data.dict_pump_ECN_h["posle"]}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(float(well_data.dict_pump_ECN_h["posle"]), 1.2)],
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
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [None, None,
             f'Перед пуском УЭЦН опрессовать ГНО на 50атм в течении 30 минут в присутствии представителя '
             f'заказчика с помощью ЦА-320 '
             f'(составить акт). Предоставить Заказчику замер НКТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 1],
        ]
        descent_ecn_with_paker = [
            [None, None,
             f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной '
             f'патрубок на сертифицированный.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             calc_fond_nkt_str,
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', None],
            [None, None,
             'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт). '
             'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного '
             'клапанов. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.3],
            [f'СПО {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit}, '
             f'пакер - {well_data.paker_do["posle"]} на глубину {well_data.depth_fond_paker_do["posle"]}м',
             None,
             f'Спустить предварительно {well_data.dict_pump_ECN["posle"]} на НКТ{nkt_edit}, '
             f'пакер - {well_data.paker_do["posle"]} на глубину {well_data.depth_fond_paker_do["posle"]}м. (завоз с УСО ГНО,'
             f' ремонтные/новые) '
             f'на гл. {well_data.dict_pump_ECN["posle"]}м. Спуск НКТ производить с шаблонированием и '
             f'смазкой резьбовых соединений, замером изоляции каждые 100м. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', descentNKT_norm(float(well_data.dict_pump_ECN_h["posle"]), 1.2)],
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
             f'на давление {well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика'
             f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 0.7],
            [OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[1], None,
             f'{OpressovkaEK.testing_pressure(self, well_data.depth_fond_paker_do["posle"])[0]} Опрессовать кабельный '
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

        lift_dict = {
            'НН с пакером': descent_nn_with_paker,
            'НВ с пакером': descent_nv_with_paker,
            'ЭЦН с пакером': descent_ecn_with_paker,
            'ЭЦН': descent_ecn,
            'НВ': descent_nv,
            'НН': descent_nn,
            'ОРД': descentORD,
            'ОРЗ': descent_orz}

        lift_select = lift_dict[lift_key]
        for row in lift_select:
            gno_list.append(row)

        if lift_key in ['ЭЦН', 'НВ', 'НН', 'НН с пакером', 'ЭЦН с пакером', 'НВ с пакером', 'ОРД'] and \
                well_data.region == 'КГМ':

            if lift_key in ['НВ', 'НН']:
                if need_juming_after_sko_combo == 'Да':
                    jumping_sko_list = [None, None,
                                        f'ПРИ НАЛИЧИИ ЦИРКУЛЯЦИИ ДОПУСТИТЬ КОМПОНОВКУ НА ТНКТ ДО ТЕКУЩЕГО ЗАБОЯ 1350м. '
                                        f'ПРОИЗВЕСТИ ВЫМЫВ ПРОДУКТОВ '
                                        f'РЕАКЦИИ С ТЕКУЩЕГО ЗАБОЯ ОБРАТНОЙ ПРОМЫВКОЙ УД.ВЕСОМ {well_data.fluid_work}. '
                                        f'ПОДНЯТЬ тНКТ ДО ПЛАНОВОЙ ГЛУБИНЫ {well_data.dict_pump_SHGN_h["posle"]}м',
                                        None, None, None, None, None, None, None,
                                        'мастер КРС', float(8.5)]
                    gno_list.insert(-4, jumping_sko_list)
            else:
                if need_juming_after_sko_combo == 'Да':
                    pero_list = [[None, None,
                                  'С целью вымыва продуктов реакции:',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', '']]
                    for row in TemplateKrs.pero(self):
                        pero_list.append(row)

                    for row in pero_list[::-1]:
                        gno_list.insert(0, row)

        return gno_list

    end_list = [
        [None, None,
         f'Все работы производить с соблюдением т/б и технологии'
         f' согласно утвержденному плану. Демонтировать подьемный агрегат и оборудование. Пустить скважину в работу.',
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

    def PzakPriGis(self):
        if well_data.region == 'ЧГМ' and well_data.expected_P < 80:
            return 80
        else:
            return well_data.expected_P

    def calc_fond_nkt(self, len_nkt, distance_between_nkt=300):
        # расчет необходимого давления опрессовки НКТ при спуске
        static_level = well_data.static_level._value
        fluid = float(well_data.fluid_work[:4].replace(',', '.'))

        pressuar = 40
        # print(f' ЭЦН {well_data.dict_pump_ECN["posle"]}')
        if well_data.dict_pump_ECN["posle"] != "0":
            pressuar = 50

        calc = CalcFond(static_level, len_nkt, fluid, pressuar, distance_between_nkt)
        calc_fond_dict = calc.calc_pressuar_list()
        press_str = f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ, ' \
                    f'произвести спуск  фондовых НКТ с поинтервальной опрессовкой через каждые {distance_between_nkt}м ' \
                    f'с учетом статического уровня уровня на на глубине {static_level}м  по телефонограмме заказчика ' \
                    f'в следующей последовательности:\n'
        n = 0
        for nkt, pressuar in calc_fond_dict.items():
            press_str += f'Опрессовать НКТ в интервале {n} - {int(nkt)} на давление {pressuar}атм \n'
            n = nkt

        return press_str
