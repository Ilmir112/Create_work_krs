from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QGridLayout, QWidget, QTabWidget, \
    QMainWindow, QPushButton
# from PyQt5.uic.properties import QtWidgets

import krs
import main
import well_data
from main import MyWindow
from work_py.alone_oreration import kot_select
from work_py.opressovka import OpressovkaEK
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from work_py.opressovka import OpressovkaEK, TabPage_SO


class TabPage_SO_grp(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        validator = QDoubleValidator(0.0, 80000.0, 2)

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)

        self.paker_khost_Label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(validator)

        self.paker_depth_Label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(validator)
        self.paker_depth_edit.textChanged.connect(self.update_paker)
        self.paker_depth_edit.setText(str(int(well_data.perforation_roof - 50)))

        self.otz_question_Label = QLabel("Нужно ли отбивать забой после подьема пакера ГРП", self)
        self.otz_question_QCombo = QComboBox(self)
        self.otz_question_QCombo.currentTextChanged.connect(self.update_paker)
        self.otz_question_QCombo.addItems(['Да', 'Нет'])

        self.normalization_question_Label = QLabel("Нужно ли нормализовывать забой?", self)
        self.normalization_QCombo = QComboBox(self)
        self.normalization_QCombo.currentTextChanged.connect(self.update_paker)
        self.normalization_QCombo.addItems(['Да', 'Нет'])

        self.current_depth_label = QLabel("Глубина нормализации", self)
        self.current_depth_edit = QLineEdit(self)
        self.current_depth_edit.setValidator(validator)
        self.current_depth_edit.setText(str(int(well_data.current_bottom)))


        self.grid_layout = QGridLayout(self)

        self.grid_layout.addWidget(self.diametr_paker_labelType, 3, 1)
        self.grid_layout.addWidget(self.diametr_paker_edit, 4, 1)

        self.grid_layout.addWidget(self.paker_khost_Label, 3, 2)
        self.grid_layout.addWidget(self.paker_khost_edit, 4, 2)

        self.grid_layout.addWidget(self.paker_depth_Label, 3, 3)
        self.grid_layout.addWidget(self.paker_depth_edit, 4, 3)

        self.grid_layout.addWidget(self.otz_question_Label, 3, 4)
        self.grid_layout.addWidget(self.otz_question_QCombo, 4, 4)

        self.grid_layout.addWidget(self.normalization_question_Label, 3, 5)
        self.grid_layout.addWidget(self.normalization_QCombo, 4, 5)

        self.grid_layout.addWidget(self.current_depth_label, 3, 6)
        self.grid_layout.addWidget(self.current_depth_edit, 4, 6)


    def update_paker(self):

        if well_data.open_trunk_well == True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 1.5
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 1.5
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(paker_depth))}')

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_grp(self), 'пакер ГРП')

class Grp_window(QMainWindow):
    def __init__(self, ins_ind, table_widget):
        super(Grp_window, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        self.table_widget = table_widget

        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.addWork)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def addWork(self):


        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        gisOTZ_true_quest = self.tabWidget.currentWidget().otz_question_QCombo.currentText()
        normalization_true_quest = self.tabWidget.currentWidget().normalization_QCombo.currentText()
        current_depth = int(float(self.tabWidget.currentWidget().current_depth_edit.text()))

        if int(paker_khost) + int(paker_depth) > well_data.current_bottom:
            mes = QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        work_list = self.grpPaker(diametr_paker, paker_depth, paker_khost, gisOTZ_true_quest,
                                  normalization_true_quest, current_depth)

        MyWindow.populate_row(self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def normalization(self, current_depth, diametr_paker):

        from work_py.opressovka import TabPage_SO
        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])


        normalization_list = [
            [f'Согласовать Алгоритм нормализации до H- {current_depth}м', None,
             f'Алгоритм работ согласовать с Заказчиком: \n'
             f'В случае освоения скважины ГНКТ и дохождение до гл. не ниже {well_data.current_bottom}м '
             f'перейти к отбивки забоя '
             f'В случае если скважину не осваивали ГНКТ продолжить работы со следующего пункта.\n'
             f'В случае наличия ЗУМПФА не менее 10м продолжить работы со следующего пункта.\n'
             f'В случае наличия циркуляции при глушении скважины произвести работы  СПО пера \n'
             f'В случае отсутствия циркуляции при глушении скважины произвести работы  СПО ГВЖ',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, None,
             f'Спустить компоновку с замером и шаблонированием НКТ: перо (1м), {self.nktGrp()} на НКТ{nkt_diam} '
             f'до гл.текущего забоя.'
             f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
             None, None, None, None, None, None, None,
             'Мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
            [f'нормализацию забоя до гл. {current_depth}м', None,
             f'Произвести нормализацию забоя  с наращиванием, комбинированной  промывкой по круговой циркуляции  жидкостью '
             f'с расходом жидкости не менее 8 л/с до гл. {current_depth}м. Тех отстой 2ч. Повторное определение '
             f'текущего забоя, при необходимости повторно вымыть.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 2.5],
            [None, None,
             f'Поднять перо с глубины {current_depth}м с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  в объеме '
             f'{round(current_depth * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(current_depth, 1)],
            [None, None,
             f'Спустить {kot_select(self)} на НКТ{well_data.nkt_diam}мм до глубины текущего забоя'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
            [None, None,
             f'Произвести очистку забоя скважины до гл.{current_depth}м закачкой обратной промывкой тех жидкости'
             f' уд.весом {well_data.fluid_work}, по согласованию с Заказчиком',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [None, None,
             f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', None],
            [None, None,
             f'Поднять {kot_select(self)} на НКТ{well_data.nkt_diam}мм c глубины {current_depth}м с доливом скважины в '
             f'объеме {round(current_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(current_depth, 1)],
            [None, None,
             f'В случае наличия ЗУМПФа 10м и более продолжить работы с п. по отбивки забоя '
             f'В случае ЗУМПФа менее 10м: и не жесткая посадка компоновки СПО ГВЖ повторить. '
             f'В случае образование твердой корки (жесткой посадки): выполнить взрыхление ПМ с ВЗД'
             f' и повторить работы СПО ГВЖ.',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, None,
             f'Спустить компоновку с замером и шаблонированием НКТ:  долото Д='
             f'{diametr_paker + 2}мм, забойный двигатель,'
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
             f' {well_data.fluid_work}  в объеме '
             f'{round(well_data.current_bottom * 1.12 / 1000, 1)}м3',
             None, None, None, None, None, None, None,
             'Мастер КРС', liftingNKT_norm(current_depth,1.2)],
            [f'по согласованию с заказчиком: Отбивка забоя',
             None, f'по согласованию с заказчиком: \n'
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                 f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4]]
        return normalization_list



    def paker_select(self, paker_depth, diametr_paker):

        if well_data.column_diametr._value > 120:
            nkt_diam = '89'
        elif 110 < well_data.column_diametr._value < 120:
            nkt_diam = '73'
        else:
            nkt_diam = '60'

        if well_data.column_additional is False \
                or (well_data.column_additional is True and paker_depth < well_data.head_column_additional._value):
            paker_select = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП - {diametr_paker}мм для ЭК {well_data.column_diametr._value}мм ' \
                           f'х {well_data.column_wall_thickness._value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м'
            paker_short = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП {diametr_paker}мм для ЭК {well_data.column_diametr._value}мм ' \
                          f'х {well_data.column_wall_thickness._value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м'

        else:
            paker_select = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП- {diametr_paker}мм для ЭК ' \
                           f'{well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м, + ' \
                           f'НКТ{nkt_diam} ' \
                           f' L-{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'воронка, НКТ{nkt_diam}м - 1,5м, пакер ГРП - {diametr_paker}мм для ЭК ' \
                          f'{well_data.column_additional_diametr._value}мм х ' \
                          f'{well_data.column_additional_wall_thickness._value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,' \
                          f' + НКТ{nkt_diam} ' \
                           f' L-{round(paker_depth - well_data.head_column_additional._value, 0)}м'
        return paker_select, paker_short


    def grpPaker(self, diametr_paker, paker_depth, paker_khost, gisOTZ_true_quest,
                                  normalization_true_quest, current_depth):


        nkt_diam = ''.join(['89' if well_data.column_diametr._value > 110 else '60'])

        paker_depth = MyWindow.true_set_Paker(self, paker_depth)
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
             f'{"".join(["(Произвести пробную посадку на глубине 50м)" if well_data.column_additional == False else " "])}',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth,1.2)],
            [None, None, f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
                         f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
                         f'В случае отсутствия представителя подрядчика по ГРП ltd оповестить Заказчика письменной '
                         f'телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'мастер КРС', ''],
            [f'Привязка по ГК и ЛМ', None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
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
             f'представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. \n В случае негерметичности пакера, дальнейшие'
             f' работы согласовать с Заказчиком. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГРП, УСРСиСТ', 0.67],
            [None, None,
             f'Письменно согласовать с Заказчиком: 1. ожидание ГРП за обваловкой; 2.переезд на другую скважину.',
             None, None, None, None, None, None, None,
             'Мастер КРС, заказчик', " "],
            [None, None,
             f'Демонтировать ПВО. Обвязать устье скважины согасно схемы ПВО №7а утвержденной главным '
             f'инженером ООО "Ойл-сервис" '
             f'от 14.10.2021г для проведения ГРП на месторождениях ООО "БашнефтьДобыча". Посадить планшайбу. '
             f'Произвести демонтаж'
             f' оборудования. Опрессовать установленную арматуру для ГРП на '
             f'Р={well_data.max_admissible_pressure._value}атм, '
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
            [None, None,
             f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
             f'глушения скважины, работы производить в присутствии представителей подрядной организации по '
             f'проведению ГРП и УСРСиСТ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 0.5],
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
             krs.lifting_unit(self),
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.2],
            [f'сменf объема уд.весом {well_data.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, well_data.current_bottom)}м3', None,
             f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {well_data.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, well_data.current_bottom)}м3. Закрыть скважину на стабилизацию '
             f'не менее 2 часов. \n'
             f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика',
             well_volume_norm((krs.volume_jamming_well(self, well_data.current_bottom)))],
            [None, None,
             f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
             f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей промывок'
             f' согласовать с Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', None],
            [krs.pvo_gno(well_data.kat_pvo)[1], None,
             krs.pvo_gno(well_data.kat_pvo)[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1.67],
            [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1],
            [None, None,
             f'Поднять пакер ГРП на НКТ{nkt_diam}м с глубины {paker_depth}м на поверхность, '
             f'с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  в объеме '
             f'{round(well_data.current_bottom * 1.12 / 1000, 1)}м3. \n'
             f'На демонтаж пригласить представителя подрядчика по ГРП',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', liftingNKT_norm(paker_depth,1.2)],
            [None, None,
             f'Опрессовать глухие плашки превентора на максимально допустимое давление '
             f'{well_data.max_admissible_pressure._value}атм, но не выше '
             f'максимально допустимого давления опрессовки эксплуатационной колонны с выдержкой в течении '
             f'30 минут,в случае невозможности '
             f'опрессовки по результатам определения приемистости и по согласованию с заказчиком  опрессовать '
             f'глухие плашки ПВО на давление поглощения, '
             f'но не менее 30атм и  с составлением акта на опрессовку ПВО с представителем Заказчика. ', None,
             None,
             None, None, None, None, None,
             'Мастер КРС', 0.67]
        ]


        if gisOTZ_true_quest == 'Да':
            paker_list.append(
                [f'Отбить забой по ГК и ЛМ', None,
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                 f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4])
        else:
            pass

        if normalization_true_quest == 'Да':
            for row in self.normalization(current_depth, diametr_paker):
                paker_list.append(row)
        else:
            pass

        return paker_list

    def paker_select(self, paker_depth, paker_khost):

        from work_py.opressovka import TabPage_SO
        if well_data.column_diametr._value > 120:
            nkt_diam = '89'
        elif 110 < well_data.column_diametr._value < 120:
            nkt_diam = '73'
        else:
            nkt_diam = '60'



        paker_diametr = TabPage_SO.paker_diametr_select(self, paker_depth)
        if well_data.column_additional is False or well_data.column_additional is True and paker_depth < well_data.head_column_additional._value:
            paker_select = f'воронка, НКТ{nkt_diam}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diametr} (либо аналог) +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,'
            paker_short = f'в-ка, НКТ{nkt_diam}м - {paker_khost}м, пакер {paker_diametr}  +' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, репер НКТ{nkt_diam}м - 2м,'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            nkt_diam_add = '60'
            paker_select = f'воронка, НКТ{nkt_diam_add}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diametr} (либо аналог) +' \
                           f'опрессовочный узел +НКТ{nkt_diam_add}м - 10м, реперный патрубок НКТ{nkt_diam_add}м - 2м, + НКТ{nkt_diam_add} L-' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'в-ка, НКТ{nkt_diam_add}м - {paker_khost}м, пакер ПРО-ЯМО-{paker_diametr}' \
                          f'опрессовочный узел +НКТ{nkt_diam_add}м - 10м, репер НКТ{nkt_diam_add}м - 2м,' \
                          f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'


        return paker_select, paker_short


    def nktGrp(self):


        if well_data.column_additional is False or (
                well_data.column_additional is True and well_data.current_bottom >= well_data.head_column_additional._value):
            return f'НКТ{well_data.nkt_diam}мм'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110:
            return f'НКТ60мм L- {round(well_data.current_bottom - well_data.head_column_additional._value + 20, 0)}'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110:
            return f'НКТ{well_data.nkt_diam}мм со снятыми фасками L- {round(well_data.current_bottom - well_data.head_column_additional._value + 20, 0)}'
