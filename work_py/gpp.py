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
from .opressovka import OpressovkaEK
from .rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from .opressovka import OpressovkaEK, TabPage_SO
from .grp import Grp_window


class TabPage_SO_grp(QWidget):
    def __init__(self, parent=None):
       
        super().__init__(parent)

        validator = QDoubleValidator(0.0, 80000.0, 2)

        self.diametr_paker_labelType = QLabel("Диаметр ГПП", self)
        self.diametr_paker_edit = QLineEdit(self)

        self.paker_depth_Label = QLabel("Глубина ГПП", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(validator)
        self.paker_depth_edit.textChanged.connect(self.update_paker)
        self.paker_depth_edit.setText(str(int(well_data.perforation_roof)))

        self.current_depth_label = QLabel("Глубина нормализации", self)
        self.current_depth_edit = QLineEdit(self)
        self.current_depth_edit.setValidator(validator)
        self.current_depth_edit.setText(str(int(well_data.current_bottom)))


        self.grid_layout = QGridLayout(self)

        self.grid_layout.addWidget(self.diametr_paker_labelType, 3, 1)
        self.grid_layout.addWidget(self.diametr_paker_edit, 4, 1)

        self.grid_layout.addWidget(self.paker_depth_Label, 3, 3)
        self.grid_layout.addWidget(self.paker_depth_edit, 4, 3)

        self.grid_layout.addWidget(self.current_depth_label, 3, 5)
        self.grid_layout.addWidget(self.current_depth_edit, 4, 5)


    def update_paker(self):
       
        if well_data.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(self, int(paker_depth))}')

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_grp(self), 'ГПП')

class Gpp_window(QMainWindow):
    def __init__(self, table_widget, ins_ind):
        super(Gpp_window, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.paker_select = None
        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
       


        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))

        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))
        current_depth = int(float(self.tabWidget.currentWidget().current_depth_edit.text()))

        if int(paker_depth) > well_data.current_bottom:
            mes = QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        work_list = self.grpGpp(paker_depth, current_depth, diametr_paker)

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()
    def grpGpp(self, gpp_depth, current_depth, diametr_paker):
       

        nkt_diam = ''.join(['89' if well_data.column_diametr._value > 110 else '60'])


        gPP_300 = MyWindow.true_set_Paker(self, 300)

        main.MyWindow.check_gpp_upa(self)

        gpp_list = [
            ['За 48 часов оформить заявку на завоз оборудования ГРП.',
             None, f'За 48 часов оформить заявку на завоз оборудования ГРП. Уложить НКТ на дополнительные стеллажи',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Спуск производить с применением спец.смазки  и рекомендуемым моментом свинчивания для НКТ{nkt_diam}м(N-80)'
             f' согласно плана от подрядчика по ГРП.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'СПО: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} на Н {gpp_depth}м', None,
             f'Спустить компоновку с замером и шаблонированием НКТ: {self.gpp_select(gpp_depth)[0]} на НКТ{nkt_diam} на '
             f'глубину {gpp_depth}м, с замером, шаблонированием НКТ. В компоновке предусмотреть пакер с установкой '
             f'на глубине 300м для внештатных ситуаций во время ГРП'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(gpp_depth, 1.2)],
            [None, None, f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
                         f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
                         f'В случае отсутствия представителя подрядчика по ГРП ltd оповестить Заказчика письменной '
                         f'телефонограммой и выйти в вынужденный простой.',
             None, None, None, None, None, None, None,
             'мастер КРС', ''],
            [f'Привязка по ГК и ЛМ',
             None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
             f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
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
             f'Обвязать устье скважины согасно схемы ПВО №7 утвержденной главным инженером ООО "Ойл-сервис" '
             f'от 14.10.2021г для проведения ГРП на месторождениях ООО "БашнефтьДобыча". Посадить планшайбу. '
             f'Произвести демонтаж'
             f' оборудования. Опрессовать установленную арматуру для ГРП на Р={well_data.max_admissible_pressure._value}атм, '
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
             f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
             f'глушения скважины, работы производить в присутствии представителей подрядной организации по проведению '
             f'ГРП и УСРСиСТ',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 0.37],
            [None, None,
             f'После разрядки скважины в объеме не менее 25м3, подтвержденной представителями ЦДНГ согласовать проведение '
             f'ГИС -пластомер для расчета жидкости глушения, произвести перерасчет ЖГ и проглушить скважину соответствующей '
             f'жидкостью. Дальнейшие работы продолжить на жидкости глушения согласно расчета. В случае отрицательных '
             f'результатов согласовать съезд бригады',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 8],
            [None, None,
             f'Установить подъёмный агрегат на устье не менее 60т. Пусковой комиссией составить акт готовности '
             f'подьемного агрегата и бригады для проведения ремонта скважины.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.2],
            [f'смену объема  уд.весом {well_data.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, well_data.current_bottom)}м3', None,
             f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {well_data.fluid_work} на циркуляцию '
             f'в объеме {krs.volume_jamming_well(self, well_data.current_bottom)}м3. Закрыть скважину на стабилизацию не менее 2 часов. \n'
             f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', well_volume_norm(krs.volume_jamming_well(self, well_data.current_bottom))],
            [None, None,
             f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
             f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей промывок '
             f'согласовать с Заказчиком.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', None],
            [None, None,
             krs.pvo_gno(well_data.kat_pvo)[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 4.67],
            [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', 1],
            [None, None,
             f'Поднять устройство ГПП на НКТ{nkt_diam}м с глубины {gpp_depth}м на поверхность, '
             f'с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  в объеме '
             f'{round(gpp_depth * 1.12 / 1000, 1)}м3. \n'
             f'На демонтаж пригласить представителя подрядчика по ГРП',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ. заказчика', liftingNKT_norm(gpp_depth,1.2)],
        ]



        for row in Grp_window.normalization(self, current_depth, diametr_paker):
            gpp_list.append(row)

        return gpp_list


    def check_gpp_upa(self):
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                value = self.table_widget.item(row, column)
                if value != None:
                    value = value.text()
                    if 'Установить подъёмный агрегат на устье не менее 40т' in value:
                        new_value = QtWidgets.QTableWidgetItem(f'Установить подъёмный агрегат на устье не менее 60т. '
                                                               f'Пусковой комиссией составить акт готовности подьемного '
                                                               f'агрегата и бригады для проведения ремонта скважины.')

                        self.table_widget.setItem(row, column, new_value)




    def gpp_select(self, paker_depth):
       
        from .opressovka import TabPage_SO
        if well_data.column_diametr._value > 120:
            nkt_diam = '89'
        else:
            nkt_diam = '60'
        if well_data.column_additional is True and well_data.column_additional_diametr._value <= 120:
            nkt_diam_add = '60'

        if well_data.column_additional is False or (
                well_data.column_additional is True and paker_depth < well_data.head_column_additional._value):
            paker_select = f'гидропескоструйный перфоратор под ЭК {well_data.column_diametr._value}мм-{well_data.column_wall_thickness._value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, реперный патрубок НКТ{nkt_diam}м - 2м,'
            paker_short = f'ГПП под ЭК {well_data.column_diametr._value}мм-{well_data.column_wall_thickness._value}мм+' \
                           f'опрессовочный узел +НКТ{nkt_diam}м - 10м, репер НКТ{nkt_diam}м - 2м,'
        else:

            paker_select = f'гидропескоструйный перфоратор под ЭК {well_data.column_additional_diametr._value}мм-{well_data.column_additional_wall_thickness._value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, реперный патрубок НКТ{nkt_diam_add}мм - 2м, + НКТ{nkt_diam_add} L-' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'ГПП под ЭК {well_data.column_additional_diametr._value}мм-{well_data.column_additional_wall_thickness._value}мм +' \
                           f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, репер НКТ{nkt_diam_add}мм - 2м, + НКТ{nkt_diam_add} L-' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'

        return paker_select, paker_short


    def nktGrp(self):
       

        if well_data.column_additional is False or (
                well_data.column_additional is True and well_data.current_bottom >= well_data.head_column_additional._value):
            return f'НКТ{well_data.nkt_diam}мм'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110:
            return f'НКТ60мм L- {round(well_data.current_bottom - well_data.head_column_additional._value + 20, 0)}'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110:
            return f'НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                   f'{round(well_data.current_bottom - well_data.head_column_additional._value + 20, 0)}'
