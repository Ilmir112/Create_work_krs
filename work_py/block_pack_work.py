from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton

import data_list
from main import MyMainWindow
from .acid_paker import CheckableComboBox
from .alone_oreration import volume_vn_ek
from .parent_work import TabPageUnion, WindowUnion, TabWidgetUnion


class TabPageSoBlock(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_label = QLabel("забой", self)
        self.current_edit = QLineEdit(self)
        self.current_edit.setValidator(self.validator_float)
        self.current_edit.setText(str(self.dict_data_well["current_bottom"]))

        self.pero_combo_Label = QLabel("выбор компоновки", self)
        self.pero_combo_QCombo = QComboBox(self)
        self.pero_combo_QCombo.addItems(['перо', 'обточную муфту', 'перо-110мм', 'пило-муфту', 'по затрубу'])

        if self.dict_data_well["column_additional"] or self.dict_data_well["column_diametr"]._value < 120:
            self.pero_combo_QCombo.setCurrentIndex(1)

        plast_work = ['']
        plast_work.extend(self.dict_data_well['plast_work'])

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)

        self.block_Label = QLabel("объем блок пачки", self)
        self.block_volume_edit = QLineEdit(self)
        self.block_volume_edit.setValidator(self.validator_float)

        self.oil_Label = QLabel("объем нефти", self)
        self.oil_volume_edit = QLineEdit(self)
        self.oil_volume_edit.setValidator(self.validator_float)

        self.block_type_Label = QLabel("объем Эмульгатора", self)
        self.block_type_volume_edit = QLineEdit(self)
        self.block_type_volume_edit.setValidator(self.validator_float)

        self.fluid_new_label = QLabel('удельный вес блок пачки', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.type_of_block_processing_label = QLabel('Цель закачки блокпачки')
        self.type_of_block_processing_combo = QComboBox(self)
        self.type_of_block_processing_combo.addItems(['для глушения', 'для нормалищации'])

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.plast_label, 4, 2)
        self.grid.addWidget(self.plast_combo, 5, 2)

        self.grid.addWidget(self.current_label, 4, 3)
        self.grid.addWidget(self.current_edit, 5, 3)

        self.grid.addWidget(self.pero_combo_Label, 4, 4)
        self.grid.addWidget(self.pero_combo_QCombo, 5, 4)
        self.grid.addWidget(self.block_Label, 4, 5)
        self.grid.addWidget(self.block_volume_edit, 5, 5)
        self.grid.addWidget(self.block_type_Label, 4, 6)
        self.grid.addWidget(self.block_type_volume_edit, 5, 6)

        self.grid.addWidget(self.type_of_block_processing_label, 6, 2)
        self.grid.addWidget(self.type_of_block_processing_combo, 7, 2)

        self.grid.addWidget(self.oil_Label, 6, 3)
        self.grid.addWidget(self.oil_volume_edit, 7, 3)

        self.grid.addWidget(self.fluid_new_label, 9, 4)
        self.grid.addWidget(self.fluid_new_edit, 10, 4)

        self.block_volume_edit.textChanged.connect(self.update_volume_block_pack)
        self.block_volume_edit.setText(str(self.calculate_volume_block_pack()))

    def update_volume_block_pack(self):
        self.fluid_new_edit.setText(str(float(self.dict_data_well["fluid_work"][:4]) + 0.04))
        self.block_type_volume_edit.setText(f"{round(float(self.block_volume_edit.text()) * 0.044, 1)}")
        self.oil_volume_edit.setText(str(round(float(self.block_volume_edit.text()) * 0.16, 1)))

    def update_type_of_block_processing_combo(self):
        self.block_volume_edit.setText(str(self.calculate_volume_block_pack()))

    def calculate_volume_block_pack(self):
        from work_py.alone_oreration import well_volume
        k = 0.05
        if float(self.dict_data_well["max_angle"]._value) > 85:
            k = 0.01
        if self.type_of_block_processing_combo.currentText() == 'для глушения':
            volume_udel = 1
        else:
            volume_udel = 2.5

        depth_nkt = float(self.dict_data_well["perforation_roof"]) - 150
        self.current_edit.setText(str(depth_nkt))
        volume_izb = 0.0007 * depth_nkt + k * self.calculate_pvr() + volume_udel * self.calculate_pvr()

        volume_block = 0.001 * well_volume(self, float(self.current_edit.text())) * depth_nkt + volume_izb
        return round(volume_block, 1)

    def calculate_pvr(self):
        plasts = data_list.texts
        metr_pvr = 0
        for plast in self.dict_data_well['plast_work']:
            for plast_sel in plasts:
                if plast_sel == plast:
                    for interval in self.dict_data_well["dict_perforation"][plast]['интервал']:
                        metr_pvr += abs(interval[0] - interval[1])
        return metr_pvr


class TabWidget(TabWidgetUnion):
    def __init__(self, parent):
        super().__init__()
        self.addTab(TabPageSoBlock(parent), 'отсыпка')


class BlockPackWindow(WindowUnion):
    work_sand_window = None

    def __init__(self, dict_data_well, table_widget, parent=None):
        super().__init__(dict_data_well)

        self.ins_ind = dict_data_well['ins_ind']
        self.tabWidget = TabWidget(self.dict_data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.table_widget = table_widget

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        try:
            pero_combo_QCombo = self.tabWidget.currentWidget().pero_combo_QCombo.currentText()
            current_edit = int(float(self.tabWidget.currentWidget().current_edit.text().replace(',', '.')))
            if current_edit >= self.dict_data_well["bottomhole_artificial"]._value:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Необходимый забой-{current_edit}м ниже исскуственного '
                                    f'{self.dict_data_well["bottomhole_artificial"]._value}м')
                return
            plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
            type_of_block_processing_combo = str(
                self.tabWidget.currentWidget().type_of_block_processing_combo.currentText())
            block_volume_edit = self.tabWidget.currentWidget().block_volume_edit.text().replace(',', '.')
            if block_volume_edit != '':
                block_volume_edit = round(float(block_volume_edit), 1)
            oil_volume_edit = self.tabWidget.currentWidget().oil_volume_edit.text().replace(',', '.')
            if oil_volume_edit != '':
                oil_volume_edit = round(float(oil_volume_edit), 1)

            fluid_new_edit = float(self.tabWidget.currentWidget().fluid_new_edit.text().replace(',', '.'))
            block_type_edit = round(
                float(self.tabWidget.currentWidget().block_type_volume_edit.text().replace(',', '.')), 1)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        work_list = self.block_pack_work(current_edit, pero_combo_QCombo,
                                         type_of_block_processing_combo, block_volume_edit, oil_volume_edit,
                                         fluid_new_edit, block_type_edit)

        self.calculate_chemistry('ЕЛАН', block_type_edit)

        self.populate_row(self.ins_ind, work_list, self.table_widget)
        data_list.pause = False
        self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def block_pack_work(self, current_edit, pero_combo_QCombo,
                        type_of_block_processing_combo, block_volume_edit, oil_volume_edit, fluid_new_edit,
                        block_type_edit):
        from .rir import RirWindow
        from work_py.alone_oreration import well_volume, volume_nkt, volume_nkt_metal
        from .template_work import TemplateKrs
        if 1 < fluid_new_edit < 1.34:
            type_of_chemistry = 'CaCl'
            water_fresh = round(data_list.DICT_CALC_CACL[fluid_new_edit][1] * (
                        block_volume_edit - oil_volume_edit - block_type_edit) / 1000, 1)
            volume_chemistry = round(data_list.DICT_CALC_CACL[fluid_new_edit][0] * (
                        block_volume_edit - oil_volume_edit - block_type_edit) / 1000, 1)
        elif 1.34 < fluid_new_edit < 1.6:
            type_of_chemistry = 'CaЖГ'
            water_fresh = round(data_list.DICT_CALC_CAZHG[fluid_new_edit][
                                    1] * block_volume_edit - oil_volume_edit - block_type_edit / 1000, 1)
            volume_chemistry = round(data_list.DICT_CALC_CAZHG[fluid_new_edit][
                                         0] * block_volume_edit - oil_volume_edit - block_type_edit / 1000, 1)

        volume_zatrub = well_volume(self, current_edit) - volume_nkt_metal(
            self.dict_data_well["dict_nkt"]) - volume_nkt(self.dict_data_well["dict_nkt"])
        count_cycle = int(block_volume_edit / 4)

        pero_list = RirWindow.pero_select(self, current_edit, pero_combo_QCombo)
        if pero_combo_QCombo != 'по затрубу':
            block_pack_list = [
                [f'Спустить {pero_list} на тНКТ{self.dict_data_well["nkt_diam"]} до глубины {current_edit}мм', None,
                 f'Спустить {pero_list} на тНКТ{self.dict_data_well["nkt_diam"]}мм до глубины {current_edit}м '
                 f'с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. '
                 f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 2.5],
                [None, None,
                 f'Завезти пресной воды -{water_fresh}м3, {type_of_chemistry}-{volume_chemistry}т, '
                 f'эмульгатор «Девон-4» в объеме {block_type_edit}м3, '
                 f'дегазированную нефть-{oil_volume_edit}м3. ', None, None, None, None,
                 None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 f'Приготовить водный раствор хлористого кальция {round((block_volume_edit - oil_volume_edit - block_type_edit), 1)}м3 '
                 f'плотностью {self.dict_data_well["fluid_work"]} перекачать в АЦ-10. Замерить уд.вес полученного раствора. ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', 4],
                [None, None,
                 f'Приготовить блокирующую пачку в объеме {block_volume_edit}м3 плотностью {fluid_new_edit}г/см3 с '
                 f'использованием насосного агрегата ЦА-320:\n'
                 f'- в мерник агрегата перекачать нефть в объеме {round(oil_volume_edit / count_cycle, 1)}м3 и эмульгатор в объеме '
                 f'{round(block_type_edit / count_cycle, 1)}м3,и перемешать в течение 15-20 мин;\n'
                 f'- при перемешивании насосного агрегата «на себя» произвести подачу солевого раствора CaCl в объеме '
                 f' {round((block_volume_edit - oil_volume_edit - block_type_edit) / count_cycle, 1)}м3 в емкость '
                 f'агрегата. Скорость подачи солевого'
                 f' раствора должна быть в 2-3 ниже скорости агрегата, перемешивающего «на себя»;\n'
                 f'- после ввода в систему всего расчетного объема солевого раствора CaCl, продолжать перемешивать '
                 f'эмульсию не менее 30 минут.\n'
                 f'-Количество циклов приготовления: {count_cycle}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, КРЕЗОЛ НС', 2],
                [None, None,
                 f'Отобрать контрольные пробы эмульсии. Произвести проверку плотности эмульсии путем погружения в '
                 f'жидкости глушения, приготовленной для продавки блок-пачки (блок-пачка должна быть плотнее и '
                 f'погружаться на дно емкости).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представитель ЦДНГ', 2.49],
                [None, None,
                 f'Провести закачку блок-пачки в трубное пространство скважины до гл.{current_edit}м в '
                 f'объеме {block_volume_edit}м3. Довести тех.водой уд.весом {self.dict_data_well["fluid_work"]}г/см3 в '
                 f'объеме {round(3 * current_edit / 1000, 1)}м3. '
                 f'Закрыть затрубное пространство. '
                 f'Продавить блок-пачку в интервал перфорации ствола продавочной жидкостью {self.dict_data_well["fluid_work"]}г/см3 '
                 f'в объеме {round(3 * current_edit / 1000, 1)}м3. '
                 f'Технологический отстой - 2 часа. Для предотвращения срыва блокирующей пачки, при проведении '
                 f'спускоподъемных операций на скважине, запрещается превышать предельную нормативную скорость подъема '
                 f'подземного (глубинного) скважинного оборудования.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представитель ЦДНГ', 2.49],
                [None, None,
                 f'Поднять {pero_list} на НКТ{self.dict_data_well["nkt_diam"]}мм с глубины {current_edit}м с доливом скважины в '
                 f'объеме {round(current_edit * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {self.dict_data_well["fluid_work"]}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС',
                 round(current_edit / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * current_edit / 9.5 + 0.17 + 0.5,
                       2)]]
        else:
            block_pack_list = [
                [f'Приподнять компоновку до глубины {current_edit}мм', None,
                 f'Приподнять компоновку на тНКТ{self.dict_data_well["nkt_diam"]}мм до глубины {current_edit}м '
                 f'с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм. '
                 f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 2.5],
                [None, None,
                 f'Завезти пресной воды 1,01г/см3-{water_fresh}м3, {type_of_chemistry}-{volume_chemistry}т, '
                 f'эмульгатор «Девон-4» в объеме {block_type_edit}м3, '
                 f'дегазированную нефть-{oil_volume_edit}м3. ', None, None, None, None,
                 None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 f'Приготовить водный раствор хлористого кальция {round((block_volume_edit - oil_volume_edit) * 0.9, 1)}м3 '
                 f'плотностью {self.dict_data_well["fluid_work"]} перекачать в АЦ-10. Замерить уд.вес полученного раствора. ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', 4],
                [None, None,
                 f'Приготовить блокирующую пачку в объеме {block_volume_edit}м3 плотностью {fluid_new_edit}г/см3 с '
                 f'использованием насосного агрегата ЦА-320:\n'
                 f'- в мерник агрегата перекачать нефть в объеме {round(oil_volume_edit / count_cycle, 1)}м3 и '
                 f'эмульгатор в объеме {round(block_type_edit, 1)}м3,и перемешать в течение 15-20 мин;\n'
                 f'- при перемешивании насосного агрегата «на себя» произвести подачу солевого раствора CaCl в объеме '
                 f' {round((block_volume_edit - oil_volume_edit - block_type_edit) / count_cycle, 1)}м3 в емкость '
                 f'агрегата. Скорость подачи солевого'
                 f' раствора должна быть в 2-3 ниже скорости агрегата, перемешивающего «на себя»;\n'
                 f'- после ввода в систему всего расчетного объема солевого раствора CaCl, продолжать перемешивать '
                 f'эмульсию не менее 30 минут.\n'
                 f'-Количество циклов приготовления: {count_cycle}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, КРЕЗОЛ НС', 2],
                [None, None,
                 f'Отобрать контрольные пробы эмульсии. Произвести проверку плотности эмульсии путем погружения в '
                 f'жидкости глушения, приготовленной для продавки блок-пачки (блок-пачка должна быть плотнее и '
                 f'погружаться на дно емкости).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представитель ЦДНГ', 2.49],
                [None, None,
                 f'Провести закачку блок-пачки в затрубное пространство скважины до гл.{current_edit}м в '
                 f'объеме {volume_zatrub}м3.'
                 f'Закрыть затрубное пространство. '
                 f'Продавить блок-пачку в интервал перфорации оставшимся объемом блок пачки и продавочной жидкостью '
                 f'{self.dict_data_well["fluid_work"]}г/см3 '
                 f'в объеме {volume_zatrub}м3. '
                 f'Технологический отстой - 2 часа. Для предотвращения срыва блокирующей пачки, при проведении '
                 f'спускоподъемных операций на скважине, запрещается превышать предельную нормативную скорость подъема '
                 f'подземного (глубинного) скважинного оборудования.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представитель ЦДНГ', 2.49],
            ]

        return block_pack_list
