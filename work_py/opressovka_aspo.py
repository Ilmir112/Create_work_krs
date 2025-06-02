from PyQt5.QtGui import QDoubleValidator, QIntValidator

import data_list
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QTabWidget, QPushButton

from log_files.log import logger
from work_py.opressovka import OpressovkaEK, TabPageSo
from work_py.parent_work import TabWidgetUnion, TabPageUnion, WindowUnion
from work_py.rationingKRS import descentNKT_norm, lifting_nkt_norm


class TabPageSoAspo(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator = QIntValidator(0, 5000)

        self.diameter_paker_label_type = QLabel("Диаметр пакера", self)
        self.diameter_paker_edit = QLineEdit(self)
        self.diameter_paker_edit.setValidator(self.validator)

        self.paker_khost_label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator)

        self.paker_depth_label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator)
        self.paker_depth_edit.textChanged.connect(self.update_paker)

        if len(self.data_well.plast_work) != 0:
            paker_depth = self.data_well.perforation_roof - 20
        else:
            if self.data_well.dict_leakiness:
                paker_depth = min([self.data_well.dict_leakiness['НЭК']['интервал'][nek][0] - 10
                                  for nek in self.data_well.dict_leakiness['НЭК']['интервал'].keys()])

        self.paker_depth_edit.setText(str(int(paker_depth)))

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.diameter_paker_label_type, 3, 1)
        self.grid.addWidget(self.diameter_paker_edit, 4, 1)

        self.grid.addWidget(self.paker_khost_label, 3, 2)
        self.grid.addWidget(self.paker_khost_edit, 4, 2)

        self.grid.addWidget(self.paker_depth_label, 3, 3)
        self.grid.addWidget(self.paker_depth_edit, 4, 3)

    def update_paker(self):
        try:
            if self.data_well.open_trunk_well is True:
                paker_depth = self.paker_depth_edit.text()
                if paker_depth != '':
                    paker_khost = self.data_well.current_bottom - int(paker_depth)
                    self.paker_khost_edit.setText(f'{paker_khost}')
                    self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')
            else:
                paker_depth = self.paker_depth_edit.text()
                if paker_depth != '':
                    paker_khost = 10
                    self.paker_khost_edit.setText(f'{paker_khost}')
                    self.diameter_paker_edit.setText(f'{self.paker_diameter_select(int(paker_depth))}')
        except Exception as e:
            logger.critical(e)

class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoAspo(parent), 'Очистка колонны с пакером')


class PakerAspo(WindowUnion):
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
        try:
            diameter_paker = int(float(self.tab_widget.currentWidget().diameter_paker_edit.text().replace(",", ".")))
            paker_khost = int(float(self.tab_widget.currentWidget().paker_khost_edit.text().replace(",", ".")))
            paker_depth = int(float(self.tab_widget.currentWidget().paker_depth_edit.text().replace(",", ".")))
        except ValueError:
            logger.critical()

        if int(paker_khost) + int(paker_depth) > self.data_well.current_bottom:
            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                             f'ниже текущего забоя')
            return
        if self.check_true_depth_template(paker_depth) is False:
            return
        if self.check_depth_paker_in_perforation(paker_depth) is False:
            return
        if self.check_depth_in_skm_interval(paker_depth) is False:
            return

        work_list = PakerAspo.paker_list(self, diameter_paker, paker_khost, paker_depth)
        self.populate_row(self.insert_index, work_list, self.table_widget)
        data_list.pause = False
        self.close()
        self.close_modal_forcefully()

    def closeEvent(self, event):
                # Закрываем основное окно при закрытии окна входа
        data_list.operation_window  = None
        event.accept()  # Принимаем событие закрытия

    # Добавление строк с опрессовкой ЭК
    def paker_list(self, paker_diameter, paker_khost, paker_depth):
        if self.data_well.column_additional is False or self.data_well.column_additional is True \
                and paker_depth < self.data_well.head_column_additional.get_value:

            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{self.data_well.nkt_diam}мм {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diameter}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_diameter.get_value}мм х {self.data_well.column_wall_thickness.get_value}мм + щелевой фильтр' \
                           f' {OpressovkaEK.nkt_opress(self)[0]}'
            paker_short = f'Заглушка сбивной клапан с ввертышем + + НКТ{self.data_well.nkt_diam}мм {paker_khost}м +' \
                          f' пакер ПРО-ЯМО-{paker_diameter}мм  + ' \
                          f'  + щелевой фильтр'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diameter}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм ' \
                           f'+ НКТ60мм L- {round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
            paker_short = f'Заглушка сбивной клапан с ввертышем + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{paker_diameter}мм + щелевой фильтр' \
                          f'+ НКТ60мм L- {round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110 and \
                paker_depth > self.data_well.head_column_additional.get_value:
            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{self.data_well.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diameter}мм (либо аналог) ' \
                           f'для ЭК {self.data_well.column_additional_diameter.get_value}мм х ' \
                           f'{self.data_well.column_additional_wall_thickness.get_value}мм + щелевой фильтр' \
                           f'+ НКТ{self.data_well.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'
            paker_short = f'Заглушка сбивной клапан с ввертышем + НКТ{self.data_well.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{paker_diameter}мм + щелевой фильтр' \
                          f'+ НКТ{self.data_well.nkt_diam}мм со снятыми фасками L- ' \
                          f'{round(paker_depth - self.data_well.head_column_additional.get_value, 0)}м'

        nkt_opress_list = OpressovkaEK.nkt_opress(self)

        paker_list = [
            [f'СПо {paker_short} до глубины {paker_depth}м', None,
             f'Спустить {paker_select} на НКТ{self.data_well.nkt_diam}мм до глубины {paker_depth}м, '
             f'воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {self.data_well.nkt_template}мм. {nkt_opress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if self.data_well.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
             f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [None, None, f'Посадить пакер на глубине {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [f'Очистить колонну от АСПО растворителем - 2м3', None,
             f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
             f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
             f'в объеме {round(3 * self.data_well.current_bottom / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
             f'пространство. Реагирование 2 часа.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст. заказчика', 4],
            [f'cрыв пакера 30мин +1ч', None,
             f'Сбить ввертыш. Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ '
             f'в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Поднять {paker_select} на НКТ{self.data_well.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {self.data_well.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', lifting_nkt_norm(paker_depth, 1.2)]]

        return paker_list
