from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QLabel, QLineEdit, QComboBox, QGridLayout, QWidget, QTabWidget, \
     QPushButton


import krs
import main
import data_list
from main import MyMainWindow
from .parent_work import TabWidgetUnion, WindowUnion, TabPageUnion

from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from .opressovka import TabPageSo
from .grp import GrpWindow


class TabPageSoGrp(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.diameter_paker_label_type = QLabel("Диаметр ГПП", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.paker_depth_label = QLabel("Глубина ГПП", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator_int)
        self.paker_depth_edit.textChanged.connect(self.update_paker)
        self.paker_depth_edit.setText(str(int(self.data_well.perforation_roof)))

        self.current_depth_label = QLabel("Глубина нормализации", self)
        self.current_depth_edit = QLineEdit(self)
        self.current_depth_edit.setValidator(self.validator_float)
        self.current_depth_edit.setText(str(int(self.data_well.current_bottom)))

        self.otz_after_question_Label = QLabel("Нужно ли отбивать забой после нормализации", self)
        self.otz_after_question_qcombo = QComboBox(self)
        self.otz_after_question_qcombo.currentTextChanged.connect(self.update_paker)
        self.otz_after_question_qcombo.addItems(['Да', 'Нет'])

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.diameter_paker_label_type, 3, 1)
        self.grid.addWidget(self.diameter_paker_edit, 4, 1)

        self.grid.addWidget(self.paker_depth_label, 3, 3)
        self.grid.addWidget(self.paker_depth_edit, 4, 3)

        self.grid.addWidget(self.current_depth_label, 3, 5)
        self.grid.addWidget(self.current_depth_edit, 4, 5)
        self.grid.addWidget(self.otz_after_question_Label, 3, 6)
        self.grid.addWidget(self.otz_after_question_qcombo, 4, 6)

    def update_paker(self):

        if self.data_well.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoGrp(parent), 'ГПП')


class GppWindow(WindowUnion):
    def __init__(self, data_well, table_widget, parent=None):
        super().__init__(data_well)
        self.insert_index = data_well.insert_index
        self.tabWidget = TabWidget(self.data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        
        self.paker_select = None

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия
        
    def add_work(self):
        diameter_paker = int(float(self.tabWidget.currentWidget().diameter_paker_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        current_depth = int(float(self.tabWidget.currentWidget().current_depth_edit.text()))
        gis_otz_after_true_quest = self.tabWidget.currentWidget().otz_after_question_qcombo.currentText()

        if int(paker_depth) > self.data_well.current_bottom:
            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                             f'ниже текущего забоя')
            return
        work_list = self.grp_gpp_work(paker_depth, current_depth, diameter_paker, gis_otz_after_true_quest)
        if work_list:
            self.populate_row(self.insert_index, work_list, self.table_widget)
            data_list.pause = False
            self.close()

    def grp_gpp_work(self, gpp_depth, current_depth, diameter_paker, gis_otz_after_true_quest):
        schema_grp = ''
        if 'Ойл' in data_list.contractor:
            schema_grp = '7'
        elif 'РН' in data_list.contractor:
            schema_grp = '6'

        nkt_diam = ''.join(['89' if self.data_well.column_diameter.get_value > 110 else '60'])

        gpp_300 = self.check_depth_in_skm_interval(300)
        if gpp_300 is False:
            return

        main.MyWindow.check_gpp_upa(self, self.table_widget)

        gpp_list = [
            ['За 48 часов оформить заявку на завоз оборудования ГРП.',
             None, f'За 48 часов оформить заявку на завоз оборудования ГРП. Уложить НКТ на дополнительные стеллажи',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Спуск производить с применением спец.смазки  и рекомендуемым моментом свинчивания для НКТ{nkt_diam}м'
             f'(N-80)'
             f' согласно плана от подрядчика по ГРП.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'СПО: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} на Н {gpp_depth}м', None,
             f'Спустить компоновку с замером и шаблонированием НКТ: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} '
             f'на '
             f'глубину {gpp_depth}м, с замером, шаблонированием НКТ. В компоновке предусмотреть пакер с установкой '
             f'на глубине 300м для внештатных ситуаций во время ГРП',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(gpp_depth, 1.2)],
            [None, None, f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
                         f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
                         f'В случае отсутствия представителя подрядчика по ГРП ltd оповестить Заказчика письменной '
                         f'телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'мастер КРС', ''],
            [f'СПО: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} на Н {gpp_depth}м', None,
             f'Спустить компоновку с замером и шаблонированием НКТ: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} '
             f'на '
             f'глубину {gpp_depth}м, с замером, шаблонированием НКТ. В компоновке предусмотреть пакер с установкой '
             f'на глубине 300м для внештатных ситуаций во время ГРП',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(gpp_depth, 1.2)],
            [f'Опрессовать эксплуатационную колонну и пакер на Р='
             f'{self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Посадить пакер на глубину 100м.\n'
             f'Опрессовать эксплуатационную колонну и ПВО на Р='
             f'{self.data_well.max_admissible_pressure.get_value}атм составить акт в присутствии следующих '
             f'представителей: УСРСиСТ (супервайзер), подрядчика по ГРП.  Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС, Представ заказчика, ГПП', 1.2],
            [f'Срыв 30мин', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [f'Допустить ГПП до плановой глубины {gpp_depth}м', None,
             f'Допустить ГПП до плановой глубины {gpp_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [f'Привязка по ГК и ЛМ',
             None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС '
                   f'{data_list.contractor}". '
                   f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
                   f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                   f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [f'Установить ГПП  на гл. {gpp_depth}м', None,
             f'Установить ГПП  на гл. {gpp_depth}м. В случае отсутствия представителя подрядчика по ГРП ltd '
             f'оповестить Заказчика письменной телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГРП', 1.2],
            [None, None,
             f'Письменно согласовать с Заказчиком: 1. ожидание ГРП за обваловкой; 2.переезд на другую скважину.',
             None, None, None, None, None, None, None,
             'Мастер КРС, заказчик', " "],
            [None, None,
             f'Обвязать устье скважины согласно схемы ПВО №{schema_grp} утвержденной главным инженером'
             f' {data_list.contractor} '
             f' {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г для проведения ГРП на месторождениях'
             f' ООО "БашнефтьДобыча". Посадить планшайбу. '
             f'Произвести демонтаж'
             f' оборудования. Опрессовать установленную арматуру для ГРП на '
             f'Р={self.data_well.max_admissible_pressure.get_value}атм, '
             f'составить акт в присутствии следующих представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. '
             f'В случае негерметичности арматуры, составить акт и устранить негерметичность под руководством следующих '
             f'представителей:  УСРСиСТ (супервайзер), подрядчика по ГРП .',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГРП, УСРСиСТ', 1.2],
            [None, None,
             f'Освободить территорию куста от оборудования бригады.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', 7.2],
            [None, None,
             f'Проведение работ ГРП силами  подрядчика по ГРП по дизайну, сформированному технологической '
             f'службой подрядчика'
             f' по ГРП (дизайн ГРП)',
             None, None, None, None, None, None, None,
             'Подрядчик по ГРП', None],
            [None, None,
             f'За 24 часа дать заявку на вывоз оборудования ГРП.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГРП', None],
            [None, None,
             f'Принять территорию скважины у представителя заказчика с составлением 3-х стороннего акта. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика, подрядчик по ГРП', None],
            [None, None,
             f'ПРИ ПРИЕМЕ СКВАЖИНЫ В РЕМОНТ УБЕДИТЬСЯ В ОТСУТСТВИИ ИЗБЫТОЧНОГО ДАВЛЕНИЯ (ДАВЛЕНИЕ РАВНО АТМОСФЕРНОМУ) '
             f'И В СВОДНОМ ОТКРЫТИИ ЗАДВИЖЕК), ПРИ НЕОБХОДИМОСТИ ДАТЬ ЗАЯВКУ в ЦДНГ ОБ ОТОГРЕВЕ АРМАТУРЫ'
             f' С ИСПОЛЬЗОВАНИЕМ ППУ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика, подрядчик по ГРП', 2.5],

            [None, None,
             f'После разрядки скважины в объеме не менее 25м3, подтвержденной представителями ЦДНГ согласовать '
             f'проведение '
             f'ГИС -пластомер для расчета жидкости глушения, произвести перерасчет ЖГ и проглушить скважину '
             f'соответствующей '
             f'жидкостью. Дальнейшие работы продолжить на жидкости глушения согласно расчета. В случае отрицательных '
             f'результатов согласовать съезд бригады',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 8],
            [None, None,
             f'Установить подъёмный агрегат на устье не менее 60т. Пусковой комиссией составить акт готовности '
             f'подъемного агрегата и бригады для проведения ремонта скважины.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.2],
            [None, None,
             f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
             f'глушения скважины, работы производить в присутствии представителей подрядной организации по проведению '
             f'ГРП и УСРСиСТ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 0.37],
            [f'смену объема  уд.весом {self.data_well.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, self.data_well.current_bottom)}м3', None,
             f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {self.data_well.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, self.data_well.current_bottom)}м3. Закрыть скважину на '
             f'стабилизацию не менее 2 часов. \n'
             f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика',
             well_volume_norm(krs.volume_jamming_well(self, self.data_well.current_bottom))],
            [None, None,
             f'Вести контроль плотности на выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
             f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей '
             f'промывок '
             f'согласовать с Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', None],
            [None, None,
             self.pvo_gno(self.data_well.category_pvo)[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.67],
            [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1],
            [None, None,
             f'Поднять устройство ГПП на НКТ{nkt_diam}м с глубины {gpp_depth}м на поверхность, '
             f'с доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  в объеме '
             f'{round(gpp_depth * 1.12 / 1000, 1)}м3. \n'
             f'На демонтаж пригласить представителя подрядчика по ГРП',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', liftingNKT_norm(gpp_depth, 1.2)],
        ]

        for row in GrpWindow.normalization(self, current_depth, diameter_paker, gis_otz_after_true_quest):
            gpp_list.append(row)

        return gpp_list

    def check_gpp_upa(self):
        QMessageBox.information(self, 'Смена подъемника',
                                      'Согласно регламента для проведения ГПП ГРП необходим тяжелый подьемник')
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                value = self.table_widget.item(row, column)
                if value is not None:
                    value = value.text()
                    if 'Установить подъёмный агрегат на устье не менее 40т' in value:
                        new_value = QtWidgets.QTableWidgetItem(
                            f'Установить подъёмный агрегат на устье не менее 60т. '
                            f'Пусковой комиссией составить акт готовности подъемного '
                            f'агрегата и бригады для проведения ремонта скважины.')

                        self.table_widget.setItem(row, column, new_value)

    def gpp_select(self, paker_depth):

        from .opressovka import TabPageSo
        if self.data_well.column_diameter.get_value > 120:
            nkt_diam = '89'
        else:
            nkt_diam = '60'
        nkt_diam_add = ''
        if self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value <= 120:
            nkt_diam_add = '60'

        if self.data_well.column_additional is False or (
                self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value):
            paker_select = f'гидропескоструйный перфоратор под ЭК {self.data_well.column_diameter.get_value}мм-' \
                           f'{self.data_well.column_wall_thickness.get_value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,'
            paker_short = f'ГПП под ЭК {self.data_well.column_diameter.get_value}мм' \
                          f'-{self.data_well.column_wall_thickness.get_value}мм+' \
                          f'опрессовочный узел +НКТ{nkt_diam}м - 10м, репер НКТ{nkt_diam}м - 2м,'
        else:

            paker_select = f'гидропескоструйный перфоратор под ЭК {self.data_well.column_additional_diameter.get_value}мм-' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, реперный патрубок НКТ{nkt_diam_add}мм -' \
                           f' 2м, + НКТ{nkt_diam_add} L-' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
            paker_short = f'ГПП под ЭК {self.data_well.column_additional_diameter.get_value}мм-' \
                          f'{self.data_well.column_additional_wall_thickness.get_value}мм +' \
                          f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, репер НКТ{nkt_diam_add}мм - 2м,+ ' \
                          f'НКТ{nkt_diam_add} L-' \
                          f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'

        return paker_select, paker_short


