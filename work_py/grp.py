import krs
import data_list

from PyQt5.QtWidgets import  QMessageBox, QLabel, QLineEdit, QComboBox, QGridLayout, QWidget, QPushButton

from work_py.alone_oreration import kot_select
from work_py.parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm, well_volume_norm
from work_py.opressovka import OpressovkaEK, TabPageSo


class TabPageSoGrp(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)

        self.paker_khost_label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator_int)

        self.paker_depth_label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator_int)
        self.paker_depth_edit.textChanged.connect(self.update_paker)
        asaw = self.data_well.perforation_roof
        self.paker_depth_edit.setText(str(int(float(self.data_well.perforation_roof)) - 50))

        self.otz_question_Label = QLabel("Нужно ли отбивать забой после подьема пакера ГРП", self)
        self.otz_question_qcombo = QComboBox(self)
        self.otz_question_qcombo.currentTextChanged.connect(self.update_paker)
        self.otz_question_qcombo.addItems(['Да', 'Нет'])

        self.normalization_question_Label = QLabel("Нужно ли нормализовывать забой?", self)
        self.normalization_qcombo = QComboBox(self)
        self.normalization_qcombo.currentTextChanged.connect(self.update_paker)
        self.normalization_qcombo.addItems(['Да', 'Нет'])

        self.current_depth_label = QLabel("Глубина нормализации", self)
        self.current_depth_edit = QLineEdit(self)
        self.current_depth_edit.setValidator(self.validator_float)
        self.current_depth_edit.setText(str(int(self.data_well.current_bottom)))

        self.otz_after_question_Label = QLabel("Нужно ли отбивать забой после нормализации", self)
        self.otz_after_question_qcombo = QComboBox(self)
        self.otz_after_question_qcombo.currentTextChanged.connect(self.update_paker)
        self.otz_after_question_qcombo.addItems(['Да', 'Нет'])

        if self.current_depth_edit.text() != '':

            if float(self.current_depth_edit.text()) - self.data_well.perforation_roof > 100 \
                    or (self.data_well.max_angle.get_value > 60 and self.data_well.max_angle_depth.get_value < self.data_well.perforation_roof) \
                    or self.data_well.open_trunk_well is True:
                self.otz_after_question_qcombo.setCurrentIndex(1)
                self.otz_question_qcombo.setCurrentIndex(1)

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.diameter_paker_label_type, 3, 1)
        self.grid.addWidget(self.diameter_paker_edit, 4, 1)

        self.grid.addWidget(self.paker_khost_label, 3, 2)
        self.grid.addWidget(self.paker_khost_edit, 4, 2)

        self.grid.addWidget(self.paker_depth_label, 3, 3)
        self.grid.addWidget(self.paker_depth_edit, 4, 3)

        self.grid.addWidget(self.otz_question_Label, 3, 4)
        self.grid.addWidget(self.otz_question_qcombo, 4, 4)

        self.grid.addWidget(self.normalization_question_Label, 3, 5)
        self.grid.addWidget(self.normalization_qcombo, 4, 5)

        self.grid.addWidget(self.current_depth_label, 3, 6)
        self.grid.addWidget(self.current_depth_edit, 4, 6)

        self.grid.addWidget(self.otz_after_question_Label, 3, 7)
        self.grid.addWidget(self.otz_after_question_qcombo, 4, 7)

    def update_paker(self):

        if self.data_well.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 1.5
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 1.5
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoGrp(parent), 'пакер ГРП')


class GrpWindow(WindowUnion):
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

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept() 
                # Принимаем событие закрытия
    def add_work(self):
        diameter_paker = int(float(self.tab_widget.currentWidget().diameter_paker_edit.text().replace(',', '.')))
        paker_khost = int(float(self.tab_widget.currentWidget().paker_khost_edit.text().replace(',', '.')))
        paker_depth = int(float(self.tab_widget.currentWidget().paker_depth_edit.text().replace(',', '.')))
        gis_otz_true_quest = self.tab_widget.currentWidget().otz_question_qcombo.currentText()
        gis_otz_after_true_quest = self.tab_widget.currentWidget().otz_after_question_qcombo.currentText()
        normalization_true_quest = self.tab_widget.currentWidget().normalization_qcombo.currentText()
        current_depth = int(float(self.tab_widget.currentWidget().current_depth_edit.text().replace(',', '.')))
        if self.check_true_depth_template(paker_depth) is False:
            return
        if self.true_set_paker(paker_depth) is False:
            return
        if self.check_depth_in_skm_interval(paker_depth) is False:
            return

        if int(paker_khost) + int(paker_depth) > self.data_well.current_bottom:
            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер ниже текущего забоя')
            return
        work_list = self.grpPaker(diameter_paker, paker_depth, paker_khost,
                                  gis_otz_true_quest, gis_otz_after_true_quest,
                                  normalization_true_quest, current_depth)

        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def normalization(self, current_depth, diameter_paker, gis_otz_after_true_quest):

        from .opressovka import TabPageSo
        nkt_diam = self.data_well.nkt_diam

        normalization_list = [
            [f'Согласовать Алгоритм нормализации до H- {current_depth}м', None,
             f'Алгоритм работ согласовать с Заказчиком: \n'
             f'В случае освоения скважины ГНКТ и дохождение до гл. не ниже {self.data_well.current_bottom}м '
             f'работы по нормализации не планировать'
             f'В случае если скважину не осваивали ГНКТ продолжить работы со следующего пункта.\n'
             f'В случае наличия ЗУМПФА не менее 10м продолжить работы со следующего пункта.\n',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],

            [None, None,
             f'Спустить {kot_select(self, current_depth)} на НКТ{nkt_diam}мм до глубины текущего забоя'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(self.data_well.current_bottom, 1)],
            [None, None,
             f'Произвести очистку забоя скважины до гл.{current_depth}м закачкой обратной промывкой тех жидкости'
             f' уд.весом {self.data_well.fluid_work}, по согласованию с Заказчиком',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [None, None,
             f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', None],
            [None, None,
             f'Поднять {kot_select(self, current_depth)} на НКТ{nkt_diam}мм c глубины {current_depth}м с '
             f'доливом скважины в '
             f'объеме {round(current_depth * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', lifting_nkt_norm(current_depth, 1)],
            [None, None,
             f'В случае наличия ЗУМПФа 10м и более продолжить работы с п. по отбивки забоя '
             f'В случае ЗУМПФа менее 10м: и не жесткая посадка компоновки СПО КОТ повторить. '
             f'В случае образование твердой корки (жесткой посадки): выполнить взрыхление ПМ с ВЗД'
             f' и повторить работы СПО КОТ.',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, None,
             f'Спустить компоновку с замером и шаблонированием НКТ:  долото Д='
             f'{diameter_paker + 2}мм, забойный двигатель,'
             f' НКТ - 20м, вставной фильтр, НКТмм до кровли проппантной пробки. '
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
             None, None, None, None, None, None, None,
             'Мастер КРС', descentNKT_norm(current_depth, 1.2)],
            [None, None,
             f'Подогнать рабочую трубу патрубками на заход 9-10м. Вызвать циркуляцию прямой промывкой. '
             f'Произвести допуск с прямой промывкой и рыхление проппантной пробки 10м с проработкой э/колонны по 10 раз. ',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.9],
            [None, None,
             f'Поднять компоновку с глубины {current_depth}м с доливом скважины тех.жидкостью уд. весом'
             f' {self.data_well.fluid_work}  в объеме '
             f'{round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None,
             'Мастер КРС', lifting_nkt_norm(current_depth, 1.2)],
            [f'по согласованию с заказчиком: Отбивка забоя',
             None, f'по согласованию с заказчиком: \n'
                   f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                   f'Произвести монтаж ПАРТИИ ГИС согласно схемысхема №11 утвержденной главным инженером '
                   f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                   f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4]]

        if gis_otz_after_true_quest == 'Нет':
            normalization_list = normalization_list[:-1]
        self.data_well.current_bottom = current_depth

        return normalization_list

    def paker_select(self, paker_depth, diameter_paker):

        if self.data_well.column_diameter.get_value > 120:
            nkt_diam = '89'
        elif 110 < self.data_well.column_diameter.get_value < 120:
            nkt_diam = '73'
        else:
            nkt_diam = '60'

        if self.data_well.column_additional is False \
                or (self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value):
            paker_select = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП - {diameter_paker}мм для ЭК {self.data_well.column_diameter.get_value}мм ' \
                           f'х {self.data_well.column_wall_thickness.get_value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м'
            paker_short = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП {diameter_paker}мм для ЭК {self.data_well.column_diameter.get_value}мм ' \
                          f'х {self.data_well.column_wall_thickness.get_value}мм +' \
                          f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м'

        else:
            paker_select = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП- {diameter_paker}мм для ЭК ' \
                           f'{self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м, + ' \
                           f'НКТ{nkt_diam} ' \
                           f' L-{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
            paker_short = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП - {diameter_paker}мм для ЭК ' \
                          f'{self.data_well.column_additional_diameter.get_value}мм х ' \
                          f'{self.data_well.column_additional_wall_thickness.get_value}мм+' \
                          f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,' \
                          f' + НКТ{nkt_diam} ' \
                          f' L-{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
        return paker_select, paker_short

    def grpPaker(self, diameter_paker, paker_depth, paker_khost, gis_otz_true_quest, gis_otz_after_true_quest,
                 normalization_true_quest, current_depth):
        if 'Ойл' in data_list.contractor:
            schema_grp = '6'
        elif 'РН' in data_list.contractor:
            schema_grp = '6'

        if self.data_well.column_diameter.get_value > 133:
            nkt_diam = 89
        elif 110 < self.data_well.column_diameter.get_value <= 133:
            nkt_diam = 73
        else:
            nkt_diam = 60

        paker_list = [
            [f'За 48 часов оформить заявку на завоз оборудования ГРП.', None,
             f'За 48 часов оформить заявку на завоз оборудования ГРП. Уложить НКТ на дополнительные стеллажи',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Спуск производить с применением спец.смазки  и рекомендуемым моментом свинчивания для '
             f'НКТ{nkt_diam}м(N-80)'
             f' согласно плана от подрядчика по ГРП.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'СПО: {self.paker_select(paker_depth, paker_khost)[1]} на НКТ{nkt_diam}м на Н {paker_depth}м', None,
             f'Спустить компоновку с замером и шаблонированием НКТ: {self.paker_select(paker_depth, paker_khost)[0]} на '
             f'НКТ{nkt_diam}м на глубину {paker_depth}м, с замером, шаблонированием НКТ. '
             f'{"".join(["(Произвести пробную посадку на глубине 50м)" if self.data_well.column_additional is False else " "])}',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [None, None,
             f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
             f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
             f'В случае отсутствия представителя подрядчика по ГРП оповестить Заказчика письменной '
             f'телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'мастер КРС', ''],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы схема №11 утвержденной главным инженером  '
             f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
             f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4],
            [None, None,
             f'Посадить пакер с учетом расположения муфтовых соединений э/колонны под руководством представителя '
             f'подрядчика по ГРП. на гл. {paker_depth}м. В случае отсутствия представителя подрядчика по ГРП ltd '
             f'оповестить Заказчика письменной телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГРП', 0.77],
            [OpressovkaEK.testing_pressure(self, paker_depth)[1], None,
             f'{OpressovkaEK.testing_pressure(self, paker_depth)[0]}. Опрессовку производить в присутствии следующих '
             f'представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. \n '
             f'В случае негерметичности арматуры, составить акт и устранить негерметичность под руководством '
             f'следующих представителей:  УСРСиСТ  (супервайзер), подрядчика по ГРП, ..',
             None, None, None, None, None, None, None,
             'подрядчик по ГРП, УСРСиСТ', 0.67],
            [None, None,
             f'Письменно согласовать с Заказчиком: 1. ожидание ГРП за обваловкой; 2.переезд на другую скважину.',
             None, None, None, None, None, None, None,
             'Мастер КРС, заказчик', " "],
            [None, None,
             f'Демонтировать ПВО. Обвязать устье скважины согласно схемы ПВО №{schema_grp} утвержденной главным '
             f'инженером {data_list.contractor} '
             f' {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г для проведения ГРП на месторождениях '
             f'ООО "БашнефтьДобыча". Посадить планшайбу. '
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
             f'Проведение работ ГРП силами  подрядчика по ГРП по дизайну, сформированному '
             f'технологической службой подрядчика'
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
             f'И В СВОДНОМ ОТКРЫТИИ ЗАДВИЖЕК), ПРИ НЕОБХОДИМОСТИ ДАТЬ ЗАЯВКУ в ЦДНГ ОБ ОТОГРЕВЕ АРМАТУРЫ С '
             f'ИСПОЛЬЗОВАНИЕМ ППУ.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика, подрядчик по ГРП', 2.5],
            [f'При избыточном давлении более 10атм - разрядка не более 25м3', None,
             f'После разрядки скважины в объеме не менее 25м3, подтвержденной представителями ЦДНГ '
             f'согласовать проведение '
             f'ГИС -пластомер для расчета жидкости глушения, произвести перерасчет ЖГ и проглушить '
             f'скважину соответствующей '
             f'жидкостью. Дальнейшие работы продолжить на жидкости глушения согласно расчета. В случае отрицательных '
             f'результатов согласовать съезд бригады',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 8],
            [None, None,
             krs.GnoParent.lifting_unit(self),
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.2],
            [None, None,
             f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
             f'глушения скважины, работы производить в присутствии представителей подрядной организации по '
             f'проведению ГРП и УСРСиСТ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 0.5],
            [None, None,
             f'За 24 часа до готовности бригады вызвать Пусковую комиссию и представителя супервайзерской '
             f'службы Заказчика. Работу Пусковой комиссией производить в обязательном присутствии представителя '
             f'супервайзерской службы Заказчика. Провести работу пусковой комиссии. '
             f'Составить акт готовности подъемного агрегата и бригадного оборудования (Пускового паспорта) '
             f'для проведения ремонта скважины. Пусковая комиссия выдает разрешение на начало производство  работ '
             f' только, после устранения всех пунктов нарушений (несоответствий) выявленных в ходе проверки '
             f'готовности бригады. Пусковая комиссия завершает работу подписанием Пускового паспорта и Акта '
             f'готовности готовности подъемного агрегата.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 1.2],
            [f'смена объема уд.весом {self.data_well.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, self.data_well.current_bottom)}м3', None,
             f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {self.data_well.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, self.data_well.current_bottom)}м3. Закрыть скважину на стабилизацию '
             f'не менее 2 часов. \n'
             f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика',
             well_volume_norm((krs.volume_jamming_well(self, self.data_well.current_bottom)))],
            [None, None,
             f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
             f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей промывок'
             f' согласовать с Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', None],
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1.67],
            [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1],
            [None, None,
             f'Поднять пакер ГРП на НКТ{nkt_diam}м с глубины {paker_depth}м на поверхность, '
             f'с доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  в объеме '
             f'{round(self.data_well.current_bottom * 1.12 / 1000, 1)}м3. \n'
             f'На демонтаж пригласить представителя подрядчика по ГРП',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', lifting_nkt_norm(paker_depth, 1.2)],
            [None, None,
             f'Опрессовать глухие плашки превентора на максимально допустимое давление '
             f'{self.data_well.max_admissible_pressure.get_value}атм, но не выше '
             f'максимально допустимого давления опрессовки эксплуатационной колонны с выдержкой в течении '
             f'30 минут,в случае невозможности '
             f'опрессовки по результатам определения приемистости и по согласованию с заказчиком  опрессовать '
             f'глухие плашки ПВО на давление поглощения, '
             f'но не менее 30атм и  с составлением акта на опрессовку ПВО с представителем Заказчика. ', None,
             None,
             None, None, None, None, None,
             'Мастер КРС', 0.67]
        ]

        if gis_otz_true_quest == 'Да':
            paker_list.append(
                [f'Отбить забой по ГК и ЛМ', None,
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы схема №11 утвержденной главным инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                 f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4])
        else:
            pass

        if normalization_true_quest == 'Да':
            for row in self.normalization(current_depth, diameter_paker, gis_otz_after_true_quest):
                paker_list.append(row)
        else:
            pass

        return paker_list

    def paker_select(self, paker_depth, paker_khost):

        from .opressovka import TabPageSo
        if self.data_well.column_diameter.get_value > 120:
            nkt_diam = '89'
        elif 110 < self.data_well.column_diameter.get_value < 120:
            nkt_diam = '73'
        else:
            nkt_diam = '60'

        paker_diameter = TabPageSo.paker_diameter_select(self, paker_depth)
        if self.data_well.column_additional is False or self.data_well.column_additional is True and paker_depth < self.data_well.head_column_additional.get_value:
            paker_select = f'воронка, НКТ{nkt_diam}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diameter} (либо аналог) +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,'
            paker_short = f'в-ка, НКТ{nkt_diam}м - {paker_khost}м, пакер {paker_diameter}  +' \
                          f'опрессовочный узел +НКТ{nkt_diam}м - 10м, репер НКТ{nkt_diam}м - 2м,'
        else:
            nkt_diam_add = '60'
            paker_select = f'воронка, НКТ{nkt_diam_add}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diameter} ' \
                           f'(либо аналог) +' \
                           f'опрессовочный узел +НКТ{nkt_diam_add}м - 10м, реперный патрубок НКТ{nkt_diam_add}м' \
                           f' - 2м, + НКТ{nkt_diam_add} L-' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
            paker_short = f'в-ка, НКТ{nkt_diam_add}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diameter}' \
                          f'опрессовочный узел +НКТ{nkt_diam_add}м - 10м, репер НКТ{nkt_diam_add}м - 2м,' \
                          f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'

        return paker_select, paker_short


