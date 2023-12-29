from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from krs import volume_vn_nkt, well_volume
from main import MyWindow
from open_pz import CreatePZ
from work_py.acids_work import flushingDownhole, pressure_mode
from work_py.rationingKRS import descentNKT_norm, well_volume_norm


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.swabTrueEditType.setProperty("value", "без освоения")

        self.swabTrueEditType.setCurrentIndex(1)

        self.pakerLabel = QLabel("глубина пакера", self)
        self.pakerEdit = QLineEdit(self)
        self.pakerEdit.setText(f"{CreatePZ.perforation_roof - 10}")
        self.pakerEdit.setClearButtonEnabled(True)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)

        self.khvostEdit.setText(f"{round(CreatePZ.perforation_sole - float(self.pakerEdit.text()),0)}")
        self.khvostEdit.setClearButtonEnabled(True)



        self.plastLabel = QLabel("Выбор пласта", self)
        self.plastCombo = QComboBox(self)
        self.plastCombo.addItems(CreatePZ.plast_work)
        self.plastCombo.setCurrentIndex(0)
        # self.ComboBoxGeophygist.setProperty("value", 'ГП')

        self.privyazkaTrueLabelType = QLabel("необходимость освоения", self)
        self.privyazkaTrueEdit = QComboBox(self)
        self.privyazkaTrueEdit.addItems(['Нужна привязка', 'без привязки'])
        self.privyazkaTrueEdit.setCurrentIndex(1)
        self.privyazkaTrueEdit.setProperty('value', 'без привязки')

        self.skvTrueLabelType = QLabel("необходимость кислотной ванны", self)
        self.svkTrueEdit = QComboBox(self)
        self.svkTrueEdit.addItems(['Нужно СКВ', 'без СКВ'])
        self.svkTrueEdit.setCurrentIndex(1)
        self.svkTrueEdit.setProperty('value', 'без СКВ')

        self.skvAcidLabelType = QLabel("Вид кислоты для СКВ", self)
        self.skvAcidEdit = QComboBox(self)
        self.skvAcidEdit.addItems(['HCl', 'HF'])
        self.skvAcidEdit.setCurrentIndex(0)
        self.skvAcidEdit.setProperty('value', 'HCl')

        self.skvVolumeLabel = QLabel("Объем СКВ", self)
        self.skvVolumeEdit = QLineEdit(self)
        self.skvVolumeEdit.setText('1')
        self.skvVolumeEdit.setClearButtonEnabled(True)

        self.QplastLabelType = QLabel("Нужно ли определять приемистоть до СКО", self)
        self.QplastEdit = QComboBox(self)
        self.QplastEdit.addItems(['ДА', 'НЕТ'])
        self.QplastEdit.setCurrentIndex(1)
        self.QplastEdit.setProperty('value', 'НЕТ')

        self.skvProcLabel = QLabel("Концентрация СКВ", self)
        self.skvProcEdit = QLineEdit(self)
        self.skvProcEdit.setClearButtonEnabled(True)
        self.skvProcEdit.setText('15')

        self.acidLabelType = QLabel("Вид кислотной обработки", self)
        self.acidEdit = QComboBox(self)
        self.acidEdit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acidEdit.setCurrentIndex(0)

        self.acidVolumeLabel = QLabel("Объем кислотной обработки", self)
        self.acidVolumeEdit = QLineEdit(self)
        self.acidVolumeEdit.setText("10")
        self.acidVolumeEdit.setClearButtonEnabled(True)

        self.acidProcLabel = QLabel("Концентрация кислоты", self)
        self.acidProcEdit = QLineEdit(self)
        self.acidProcEdit.setText('15')
        self.acidProcEdit.setClearButtonEnabled(True)

        self.acidOilProcLabel = QLabel("объем нефти", self)

        self.acidOilProcEdit = QLineEdit(self)
        self.acidOilProcEdit.setClearButtonEnabled(True)

        grid = QGridLayout(self)
        grid.addWidget(self.swabTruelabelType, 0, 0)
        grid.addWidget(self.swabTrueEditType, 1, 0)
        grid.addWidget(self.plastLabel, 0, 1)
        grid.addWidget(self.plastCombo, 1, 1)
        grid.addWidget(self.pakerLabel, 0, 2)
        grid.addWidget(self.pakerEdit, 1, 2)
        grid.addWidget(self.khovstLabel, 0, 3)
        grid.addWidget(self.khvostEdit, 1, 3)
        grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        grid.addWidget(self.privyazkaTrueEdit, 1, 4)

        grid.addWidget(self.skvTrueLabelType, 2, 0)
        grid.addWidget(self.svkTrueEdit, 3, 0)
        grid.addWidget(self.skvAcidLabelType, 2, 1)
        grid.addWidget(self.skvAcidEdit, 3, 1)
        grid.addWidget(self.skvVolumeLabel, 2, 2)
        grid.addWidget(self.skvVolumeEdit, 3, 2)
        grid.addWidget(self.skvProcLabel, 2, 3)
        grid.addWidget(self.skvProcEdit, 3, 3)

        grid.addWidget(self.acidLabelType, 4, 1)
        grid.addWidget(self.acidEdit, 5, 1)
        grid.addWidget(self.acidVolumeLabel, 4, 2)
        grid.addWidget(self.acidVolumeEdit, 5, 2)
        grid.addWidget(self.acidProcLabel, 4, 3)
        grid.addWidget(self.acidProcEdit, 5, 3)
        grid.addWidget(self.acidOilProcLabel, 4, 4)
        grid.addWidget(self.acidOilProcEdit, 5, 4)
        grid.addWidget(self.QplastLabelType, 6, 0)
        grid.addWidget(self.QplastEdit, 7, 0)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Кислотная обработка на одном пакере')


class AcidPakerWindow(MyWindow):

    def __init__(self, parent=None):

        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # self.table_widget = table_widget
        # self.ins_ind = ins_ind
        self.tabWidget = TabWidget()
        self.dict_nkt = {}
        # self.tableWidget = QTableWidget(0, 2)
        # self.tableWidget.setHorizontalHeaderLabels(
        #     ["Ход работ", "ответственные", "нормы"])
        # for i in range(3):
        #     self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        #
        # self.tableWidget.setSortingEnabled(True)
        # self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить данные в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить строку из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddWork = QPushButton('Добавить в план работ')
        self.buttonAddWork.clicked.connect(self.addWork)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAddWork, 3, 0)

    def addWork(self):
        pass
    def acidSelect(self, swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, skvAcidEdit, acidEdit, skvVolumeEdit,
                   QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit):
        from work_py.opressovka import paker_diametr_select
        # print(swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, skvAcidEdit, acidEdit, skvVolumeEdit,
        #            QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit)
        swabTrueEditType = [True if swabTrueEditType == 'Нужно освоение' else False][0]
        svkTrueEdit = [False if swabTrueEditType == 'без СКВ' else False][0]
        print(CreatePZ.column_additional == False, swabTrueEditType == True)
        if (CreatePZ.column_additional == False and swabTrueEditType == True) or (CreatePZ.column_additional == True \
                                                                                  and pakerEdit < CreatePZ.head_column_additional and swabTrueEditType == True):
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм {khvostEdit}м + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ{CreatePZ.nkt_diam} 10м + репер'
            self.dict_nkt = {73: float(khvostEdit) + float(pakerEdit)}

        elif CreatePZ.column_additional == True and float(CreatePZ.column_additional_diametr) < 110 and \
                pakerEdit > CreatePZ.head_column_additional and swabTrueEditType == True:
            paker_select = f'воронку + НКТ{60}мм {float(khvostEdit)}м + пакер ПРО-ЯМО-{paker_diametr_select(float(pakerEdit))}мм (либо аналог) ' \
                           f'для ЭК {float(CreatePZ.column_additional_diametr)}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м + репер'
            self.dict_nkt = {73: CreatePZ.head_column_additional,
                        60: int(float(pakerEdit) + float(khvostEdit) - float(CreatePZ.head_column_additional))}
        elif CreatePZ.column_additional == True and float(CreatePZ.column_additional_diametr) > 110 and pakerEdit > CreatePZ.head_column_additional and swabTrueEditType == True:
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {float(khvostEdit)}м + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                           f'для ЭК {float(CreatePZ.column_additional_diametr)}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 10м'
            self.dict_nkt = {73: float(pakerEdit) + float(khvostEdit)}
        elif (CreatePZ.column_additional == False and swabTrueEditType == False) or (
                CreatePZ.column_additional == True
                and pakerEdit < float(CreatePZ.head_column_additiona) and swabTrueEditType == False):
            paker_select = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}м {float(khvostEdit)}м + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м + сбивной клапан с ввертышем'
            self.dict_nkt = {73: float(pakerEdit) + float(khvostEdit)}
            # print(f' 5 {CreatePZ.column_additional == False, (CreatePZ.column_additional == True and pakerEdit < CreatePZ.head_column_additional), swabTrueEditType == False}')
        elif CreatePZ.column_additional == True or (float(CreatePZ.column_additional_diametr) < 110 and (
                pakerEdit > CreatePZ.head_column_additional) and swabTrueEditType == False):
            paker_select = f'Заглушку + щелевой фильтр + НКТ{60}мм {float(khvostEdit)}м + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                           f'для ЭК {float(CreatePZ.column_additional_diametr)}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м + сбивной клапан с ввертышем'
            self.dict_nkt = {73: float(CreatePZ.head_column_additional), 60: int(pakerEdit - float(CreatePZ.head_column_additional))}
        elif CreatePZ.column_additional == True and float(CreatePZ.column_additional_diametr) > 110 and pakerEdit > float(CreatePZ.head_column_additional) \
                and swabTrueEditType == False:
            paker_select = f'Заглушку + щелевой фильтр + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {khvostEdit}м + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                           f'для ЭК {float(CreatePZ.column_additional_diametr)}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 10м + сбивной клапан с ввертышем'
            self.dict_nkt = {73: float(pakerEdit) + float(khvostEdit)}

        elif CreatePZ.nkt_diam == 60:
            self.dict_nkt = {60: float(pakerEdit) + float(khvostEdit)}

        paker_list = [
            [None, None,
             f'Спустить {paker_select} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerEdit}м, воронкой до {pakerEdit + khvostEdit}м'
             f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerEdit, 1.2)],
            [None, None, f'Посадить пакер на глубине {pakerEdit}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Опрессовать эксплуатационную колонну в интервале {pakerEdit}-0м на Р={CreatePZ.max_admissible_pressure}атм'
             f' в течение 30 минут  в присутствии представителя заказчика, составить акт.  '
             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.83 + 0.58],
            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None]]
        return paker_list
    def acid_work(self, swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, skvAcidEdit, acidEdit, skvVolumeEdit,
                   QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit, dict_nkt):
        paker_list = []

        skv_list = [[None, None,
                     f'Определить приемистость при Р-{CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика.'
                     f'при отсутствии приемистости произвести установку СКВ по согласованию с заказчиком',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 1.2],
                    [None, None, f'Произвести установку СКВ {skvAcidEdit} {skvProcEdit}% концентрации в объеме'
                                 f' {skvVolumeEdit}м3 (0,7т HCL 24%)(по спец. плану, составляет старший мастер)',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 1.2],
                    [None, None,
                     f'закачать {skvAcidEdit} {skvProcEdit}% в объеме V={skvVolumeEdit}м3; довести кислоту до пласта '
                     f'тех.жидкостью в объеме {volume_vn_nkt(dict_nkt)}м3 . ',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.6],
                    [None, None, f'реагирование 2 часа.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 2],
                    [None, None, f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
                                 f'кратном обьеме. Посадить пакер. Определить приемистость пласта в присутствии '
                                 f'представителя ЦДНГ (составить акт). Сорвать пакер. '
                                 f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
                                 f'методом дренирования.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]]
        print(f' СКВ  {svkTrueEdit}')
        if svkTrueEdit == True:
            for row in skv_list:
                paker_list.append(row)

        if acidEdit == 'HCl':

            acid_sel = f'Произвести  солянокислотную обработку {plastCombo}  в объеме  {acidVolumeEdit}м3  ({acidEdit} - {acidProcEdit} %) ' \
                       f' в присутствии представителя Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм. \n' \
                       f'(для приготовления соляной кислоты в объеме {acidVolumeEdit}м3 - {acidProcEdit}% необходимо замешать {round(acidVolumeEdit * acidProcEdit / 24 * 1.118, 1)}т HCL 24% и' \
                       f' пресной воды {round(float(acidVolumeEdit) - float(acidVolumeEdit) * float(acidProcEdit) / 24 * 1.118, 1)}м3) ' \
                       f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол. '
        elif acidEdit == 'ВТ':

            vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
            acid_sel = f'Произвести кислотную обработку {plastCombo} {vt}  в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
        elif acidEdit == 'HF':

            acid_sel = f'Произвести кислотную обработку пласта {plastCombo}  в объеме  {acidVolumeEdit}м3  ({acidEdit} - {acidProcEdit} %) силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
        elif acidEdit == 'Нефтекислотка':
            acid_sel = f'Произвести нефтекислотную обработку пласта {plastCombo} в V=2тн товарной нефти + {acidVolumeEdit}м3  (HCl - {acidProcEdit} %) + {acidOilProcEdit - 2}т товарной нефти силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
        elif acidEdit == 'Противогипсовая обработка':
            acid_sel = f'Произвести противогипсовую обработку пласта{plastCombo} в объеме {acidVolumeEdit}м3 - {20}% раствором каустической соды' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={CreatePZ.max_admissible_pressure}атм.\n'
                    # print(f'Ожидаемое показатели {CreatePZ.expected_pick_up.values()}')
        acid_list_1 = [[None, None,
                        f'{acid_sel}'
                        f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ И СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
                        None, None, None, None, None, None, None,
                        'мастер КРС, УСРСиСТ', 8],
                       [None, None,
                        ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
                                 f"объем НКТ)" if acidVolumeEdit > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                                                f"объеме {round(acidVolumeEdit, 1)}м3, "
                                                                                                f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - acidVolumeEdit, 1)}м3 "]),
                        None, None, None, None, None, None, None,
                        'мастер КРС', None],
                       [None, None,
                        f'посадить пакер на глубине {pakerEdit}м',
                        None, None, None, None, None, None, None,
                        'мастер КРС', None],
                       [None, None,
                        ''.join(
                            [
                                f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 при давлении не '
                                f'более {CreatePZ.max_admissible_pressure}атм. Увеличение давления согласовать'
                                f' с заказчиком' if acidVolumeEdit < volume_vn_nkt(
                                    dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме {round(acidVolumeEdit - volume_vn_nkt(dict_nkt), 1)}м3 и тех жидкостью '
                                                   f'в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 при давлении не более {CreatePZ.max_admissible_pressure}атм. '
                                                   f'Увеличение давления согласовать с заказчиком']),
                        None, None, None, None, None, None, None,
                        'мастер КРС', None],
                       [None, None,
                        f'реагирование 2 часа.',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 2],

                       [None, None,
                        f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                        f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.7],
                       # [None, None,
                       #  flushingDownhole(self, pakerEdit, khvostEdit, 1),
                       #  None, None, None, None, None, None, None,
                       #  'мастер КРС', well_volume_norm(well_volume(self, CreatePZ.current_bottom))]
                       ]

        for row in acid_list_1:
            paker_list.append(row)
        print(f'определение {QplastEdit}')
        if CreatePZ.curator == 'ОР':
            if QplastEdit == True:
                try:
                    CreatePZ.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                                  f'Ожидаемая приемистость по пласту {plastCombo} ',
                                                                  list(CreatePZ.expected_pick_up.keys())[0], 0,
                                                                  1600)
                    CreatePZ.expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                                                  f'Ожидаемое Давление закачки по пласту {plastCombo}',
                                                                  list(CreatePZ.expected_pick_up.values())[0], 0,
                                                                  250)
                except:
                    CreatePZ.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                                  f'Ожидаемая приемистость по пласту {plastCombo} ',
                                                                  100, 0,
                                                                  1600)
                    CreatePZ.expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                                  f'Ожидаемое Давление закачки по пласту {plastCombo}',
                                                                  100, 0,
                                                                  250)
            paker_list.append([None, None,
                               f'Посадить пакер на {pakerEdit}м. Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                               f'пласт {plastCombo} на приемистость в трех режимах при Р={pressure_mode(CreatePZ.expected_P, plastCombo)}атм в присутствии представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {CreatePZ.expected_Q}м3/сут при давлении {CreatePZ.expected_P}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list



        # Определение трех режимов давлений при определении приемистости
    def pressure_mode(mode, plast):
        from open_pz import CreatePZ

        mode = int(mode / 10) * 10
        if mode > CreatePZ.max_admissible_pressure and (plast != 'D2ps' or plast.lower() != 'дпаш'):
            mode_str = f'{mode}, {mode - 10}, {mode - 20}'
        elif (plast == 'D2ps' or plast.lower() == 'дпаш') and CreatePZ.region == 'ИГМ':
            mode_str = f'{120}, {140}, {160}'
        else:
            mode_str = f'{mode - 10}, {mode}, {mode + 10}'
        return mode_str

        # промывка скважины после кислотной обработки в зависимости от интервала перфорации и комповноки и текущего забоя
    def flushingDownhole(self, paker_depth, paker_khost, paker_layout):
        from open_pz import CreatePZ

        if paker_layout == 2:
            flushingDownhole_list = f'Только при наличии избыточного давления или когда при проведении ОПЗ получен технологический ""СТОП":' \
                                    f'произвести промывку скважину обратной промывкой ' \
                                    f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                    f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
                                    f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
        elif paker_depth + paker_khost >= CreatePZ.current_bottom or (
                paker_depth + paker_khost < CreatePZ.current_bottom and CreatePZ.work_pervorations_approved == True):
            flushingDownhole_list = f'Допустить компоновку до глубины {CreatePZ.current_bottom}м. Промыть скважину обратной промывкой ' \
                                    f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                    f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                    f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
        elif paker_depth + paker_khost < CreatePZ.current_bottom and CreatePZ.work_pervorations_approved == False:
            flushingDownhole_list = f'Допустить пакер до глубины {int(CreatePZ.perforation_roof - 5)}м. (на 5м выше кровли интервала перфорации), ' \
                                    f'низ НКТ до глубины {CreatePZ.perforation_roof - 5 + paker_khost}м) ' \
                                    f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                    f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                    f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'

        return flushingDownhole_list


    #
    def addRowTable(self):
        swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        acidEdit = self.tabWidget.currentWidget().acidEdit.currentText()
        khvostEdit = float(self.tabWidget.currentWidget().khvostEdit.text())
        pakerEdit = float(self.tabWidget.currentWidget().pakerEdit.text())
        skvVolumeEdit = float(self.tabWidget.currentWidget().skvVolumeEdit.text())
        skvProcEdit = float(self.tabWidget.currentWidget().skvProcEdit.text())
        acidVolumeEdit = float(self.tabWidget.currentWidget().acidVolumeEdit.text())
        acidProcEdit = float(self.tabWidget.currentWidget().acidProcEdit.text())

        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()

        plastCombo = str(self.tabWidget.currentWidget().plastCombo.currentText())
        svkTrueEdit = str(self.tabWidget.currentWidget().svkTrueEdit.currentText())
        skvAcidEdit = str(self.tabWidget.currentWidget().skvAcidEdit.currentText())
        QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        # privyazka = str(self.tabWidget.currentWidget().privyazka.currentText())

        CreatePZ.acid_V = acidVolumeEdit
        CreatePZ.acid_pr = acidProcEdit
        CreatePZ.acid_oil = acidOilProcEdit
        CreatePZ.acid_true_quest_scv = svkTrueEdit
        CreatePZ.acid_V_scv = skvVolumeEdit
        CreatePZ.acid_pr_scv = skvProcEdit
        CreatePZ.acid = acidEdit
        CreatePZ.pause = False
        CreatePZ.swabbing_true_quest = swabTrueEditType
        CreatePZ.plast = plastCombo
        CreatePZ.paker_khost1 =  khvostEdit
        CreatePZ.paker_depth = pakerEdit

        # work_list = self.acidSelect(swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, skvAcidEdit, acidEdit,
        #                             skvVolumeEdit, QplastEdit, skvProcEdit, plastCombo,
        #                             acidOilProcEdit, acidVolumeEdit, svkTrueEdit)
        #
        # for row in self.acid_work(swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, skvAcidEdit, acidEdit, skvVolumeEdit,
        #            QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit, self.dict_nkt):
        #     work_list.append(row)
        # self.populate_row(self.ins_ind, work_list)
        # self.ins_ind += len(work_list)
        # CreatePZ.pause = False
        # self.close()




    def populate_row(self, ins_ind, work_list):
        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 1500)}

        for i, row_data in enumerate(work_list):
            row = self.ins_ind + i
            self.table_widget.insertRow(row)

            self.table_widget.setSpan(i + self.ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                # widget = QtWidgets.QLabel(str())
                # widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')

                # self.table_widget.setCellWidget(row, column, widget)

                if not data is None:
                    self.table_widget.setItem(row, column, item)

                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))



    def del_row_table(self):
        pass
    #     row = self.tableWidget.currentRow()
    #     if row == -1:
    #         msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
    #         return
    #     self.tableWidget.removeRow(row)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = AcidPakerWindow()
    window.show()
    sys.exit(app.exec_())