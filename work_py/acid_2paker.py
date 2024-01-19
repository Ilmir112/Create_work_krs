from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QInputDialog, QTabWidget, QPushButton, Qt

from krs import well_volume
from main import MyWindow
from open_pz import CreatePZ
from work_py.opressovka import testing_pressure

from work_py.rationingKRS import descentNKT_norm, well_volume_norm, liftingNKT_norm


class TabPage_SO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.countAcid = CreatePZ.countAcid

        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.swabTrueEditType.setProperty("value", "без освоения")
        self.swabTrueEditType.setCurrentIndex(CreatePZ.swabTrueEditType)

        self.depthGaugeLabel = QLabel("глубинные манометры", self)
        self.depthGaugeCombo = QComboBox(self)
        self.depthGaugeCombo.addItems(['Нет', 'Да'])
        self.depthGaugeCombo.setProperty("value", "Нет")

        self.pakerLabel = QLabel("глубина Нижнего пакера", self)
        self.pakerEdit = QLineEdit(self)
        if self.countAcid == 0:
            self.pakerEdit.setText(f"{round(CreatePZ.perforation_sole + 10, 0)}")
            self.pakerEdit.setClearButtonEnabled(True)
            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{round(CreatePZ.perforation_roof - 10, 0)}")
            self.paker2Edit.setClearButtonEnabled(True)
            CreatePZ.differencePakers = float(self.pakerEdit.text()) - float(self.paker2Edit.text())
            CreatePZ.paker2Edit = float(self.pakerEdit.text())
        if self.countAcid == 1:
            self.pakerEdit.setText(f"{round(CreatePZ.paker2Edit, 0)}")
            self.pakerEdit.setClearButtonEnabled(True)

            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{round(float(CreatePZ.paker2Edit) - CreatePZ.differencePakers, 0)}")
            self.paker2Edit.setClearButtonEnabled(True)
        elif self.countAcid == 2:
            self.pakerEdit.setText(f"{round(CreatePZ.paker2Edit, 0)}")
            self.pakerEdit.setClearButtonEnabled(True)
            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{round(float(CreatePZ.paker2Edit) - CreatePZ.differencePakers, 0)}")
            self.paker2Edit.setClearButtonEnabled(True)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)

        self.khvostEdit.setText(f"{1}")
        self.khvostEdit.setClearButtonEnabled(True)

        self.plastLabel = QLabel("Выбор пласта", self)
        self.plastCombo = QComboBox(self)
        self.plastCombo.addItems(CreatePZ.plast_work)
        self.plastCombo.setCurrentIndex(0)
        # self.ComboBoxGeophygist.setProperty("value", 'ГП')

        # self.privyazkaTrueLabelType = QLabel("необходимость освоения", self)
        # self.privyazkaTrueEdit = QComboBox(self)
        # self.privyazkaTrueEdit.addItems(['Нужна привязка', 'без привязки'])
        # self.privyazkaTrueEdit.setCurrentIndex(1)
        # self.privyazkaTrueEdit.setProperty('value', 'без привязки')

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

        self.swabTypeLabel = QLabel("задача при освоении", self)
        self.swabTypeCombo = QComboBox(self)
        self.swabTypeCombo.addItems(['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'])
        self.swabTypeCombo.setCurrentIndex(CreatePZ.swabTypeComboIndex)
        self.swabTypeCombo.setProperty('value', 'Задача №2.1.16')

        self.swab_pakerLabel = QLabel("Глубина посадки нижнего пакера при освоении", self)
        self.swab_pakerEdit = QLineEdit(self)
        self.swab_pakerEdit.setText(str(self.pakerEdit.text()))

        self.swab_volumeLabel = QLabel("объем освоения", self)
        self.swab_volumeEdit = QLineEdit(self)
        self.swab_volumeEdit.setText('20')

        if CreatePZ.countAcid == 1:
            for enable in [self.khovstLabel, self.khvostEdit, self.swabTruelabelType, self.swabTrueEditType,
                           self.swabTrueEditType,
                           self.paker2Edit]:
                enable.setEnabled(False)
        elif CreatePZ.countAcid == 2:
            listEnabel = [self.khovstLabel, self.khvostEdit, self.swabTruelabelType, self.swabTrueEditType,
                          self.plastCombo,
                          self.svkTrueEdit, self.QplastEdit, self.skvProcEdit, self.acidEdit, self.acidVolumeEdit,
                          self.acidProcEdit]
            for enable in listEnabel:
                enable.setEnabled(False)

        grid = QGridLayout(self)

        grid.addWidget(self.swabTruelabelType, 0, 0)
        grid.addWidget(self.swabTrueEditType, 1, 0)

        grid.addWidget(self.plastLabel, 0, 1)
        grid.addWidget(self.plastCombo, 1, 1)
        grid.addWidget(self.khovstLabel, 0, 2)
        grid.addWidget(self.khvostEdit, 1, 2)
        grid.addWidget(self.pakerLabel, 0, 3)
        grid.addWidget(self.pakerEdit, 1, 3)
        grid.addWidget(self.paker2Label, 0, 4)
        grid.addWidget(self.paker2Edit, 1, 4)

        # grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        # grid.addWidget(self.privyazkaTrueEdit, 1, 4)

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
        grid.addWidget(self.QplastLabelType, 4, 0)
        grid.addWidget(self.QplastEdit, 5, 0)
        grid.addWidget(self.swabTypeLabel, 6, 1)
        grid.addWidget(self.swabTypeCombo, 7, 1)
        grid.addWidget(self.swab_pakerLabel, 6, 2)
        grid.addWidget(self.swab_pakerEdit, 7, 2)
        grid.addWidget(self.swab_volumeLabel, 6, 3)
        grid.addWidget(self.swab_volumeEdit, 7, 3)
        grid.addWidget(self.depthGaugeLabel, 6, 4)
        grid.addWidget(self.depthGaugeCombo, 7, 4)


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Кислотная обработка на двух пакерах')


class AcidPakerWindow(MyWindow):

    def __init__(self, table_widget, ins_ind, countAcid, parent=None):

        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind
        self.countAcid = countAcid
        self.paker_select = None
        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.addRowTable)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def swabbing_with_paker(self, paker_khost, paker_depth, deferencePaker, swab, swab_volume):
        if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля ' \
                          f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                          f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
        elif swab == 'Задача №2.1.16':
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и ' \
                          f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения ' \
                          f'свабированием  не менее не менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
        elif swab == 'Задача №2.1.11':
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                          f'менее  {swab_volume}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'

        paker_depth = MyWindow.true_set_Paker(self, paker_depth)
        paker2_depth = MyWindow.true_set_Paker(self, float(paker_depth) - float(deferencePaker))

        paker_list = [

            [None, None, f'Посадить пакер на глубине {paker_depth}/{paker2_depth}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [None, None,
             testing_pressure(self, paker_depth),
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],

            [None, None,
             f'В случае негерметичности э/к согласовать с заказчиком дальнейшие действия',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье {CreatePZ.max_expected_pressure}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [None, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            [None, None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
            [None, None,
             f'Поднять компоновку на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)]]
        ovtr = 'ОВТР 4ч' if CreatePZ.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if CreatePZ.region == 'ЧГМ' else 10
        if swab == 'Задача №2.1.13' and CreatePZ.region not in ['ИГМ']:
            paker_list.insert(3, [None, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        return paker_list

    def acidSelect(self, swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, depthGaugeEdit):
        from work_py.opressovka import paker_diametr_select

        swabTrueEditType = True if swabTrueEditType == 'Нужно освоение' else False
        difference_paker = round(pakerEdit - paker2Edit, 0)
        CreatePZ.difference_paker = difference_paker
        pakerEdit = MyWindow.true_set_Paker(self, pakerEdit)
        paker2Edit = MyWindow.true_set_Paker(self, paker2Edit)
        if depthGaugeEdit == 'Да' and CreatePZ.column_additional == False:
            self.paker_select = f'заглушку + сбивной с ввертышем контейнер с манометром МТГ + НКТ{CreatePZ.nkt_diam}м {khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ {difference_paker}м + сбивной с ввертышем контейнер с манометром МТГ' \
                                f'+ пакер ПУ - {paker_diametr_select(paker2Edit)} + НКТ{CreatePZ.nkt_diam}мм 20м +реперный патрубок + сбивной с ввертышем контейнер с манометром МТГ на НКТ{CreatePZ.nkt_diam}'
            dict_nkt = {73: pakerEdit}
        elif CreatePZ.column_additional == False or (
                CreatePZ.column_additional == True and pakerEdit < CreatePZ.head_column_additional):
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{CreatePZ.nkt_diam}м {khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr_select(paker2Edit)} + НКТ{CreatePZ.nkt_diam}мм 20м +реперный патрубок на НКТ{CreatePZ.nkt_diam}'
            dict_nkt = {73: pakerEdit}
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and pakerEdit > CreatePZ.head_column_additional:
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{60}мм {khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ{60} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr_select(pakerEdit)} + НКТ{60}мм 20м +реперный патрубок на НКТ{60} {CreatePZ.head_column_additional - pakerEdit}'
            CreatePZ.dict_nkt = {73: CreatePZ.head_column_additional - 10,
                                 60: int(pakerEdit - float(CreatePZ.head_column_additional))}
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and pakerEdit > CreatePZ.head_column_additional:
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ73 со снятыми фасками {khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr_select(pakerEdit)}мм (либо аналог) ' \
                                f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ73 со снятыми фасками {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr_select(pakerEdit)} + НКТ73 со снятыми фасками 20м +реперный патрубок на НКТ73 со снятыми фасками {CreatePZ.head_column_additional - pakerEdit}'

            CreatePZ.dict_nkt = {73: pakerEdit}
        elif CreatePZ.nkt_diam == 60:
            CreatePZ.dict_nkt = {60: pakerEdit}

        paker_list = [
            [None, None,
             f'Спустить {self.paker_select} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerEdit}/{paker2Edit}м'
             f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerEdit, 1.2)],
            [None, None, f'Посадить пакер на глубине {pakerEdit}/{paker2Edit}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [None, None,
             testing_pressure(self, pakerEdit),
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
        if depthGaugeEdit == 'Да':
            paker_list.insert(0, [None, None,
                                  f'Заявить 3 глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])
        return paker_list

    def acid_work(self, swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, paker2Edit, skvAcidEdit, acidEdit,
                  skvVolumeEdit,
                  QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit, dict_nkt):
        from krs import volume_vn_nkt
        paker_list = []
        swabTrueEditType = [False if swabTrueEditType == 'без СКВ' else False][0]
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
        print(f'СКВ {svkTrueEdit}')
        if svkTrueEdit == 'Нужно СКВ':
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
            acid_sel = f'Произвести нефтекислотную обработку пласта {plastCombo} в V=2тн товарной нефти + {acidVolumeEdit}м3  (HCl - {acidProcEdit} %) + {float(acidOilProcEdit) - 2}т товарной нефти силами СК Крезол ' \
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
                        'мастер КРС, УСРСиСТ', None],
                       [None, None,
                        ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
                                 f"объем НКТ)" if acidVolumeEdit > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                                                f"объеме {round(acidVolumeEdit, 1)}м3, "
                                                                                                f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - acidVolumeEdit, 1)}м3 "]),
                        None, None, None, None, None, None, None,
                        'мастер КРС', None],
                       [None, None,
                        f'посадить пакера на глубине {pakerEdit}/{paker2Edit}м',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.3],
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
                        'мастер КРС', 6],
                       [None, None,
                        f'реагирование 2 часа.',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 2],

                       [None, None,
                        f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                        f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.7],
                       [None, None,
                        self.flushingDownhole(pakerEdit, khvostEdit, 1),
                        None, None, None, None, None, None, None,
                        'мастер КРС', well_volume_norm(well_volume(self, CreatePZ.current_bottom))]
                       ]

        for row in acid_list_1:
            paker_list.append(row)

        if CreatePZ.curator == 'ОР':
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
            if QplastEdit == 'ДА':
                paker_list.insert(-2, [None, None,
                                       f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. '
                                       f'Опробовать '
                                       f'пласт {plastCombo} на приемистость в трех режимах при Р={self.pressure_mode(CreatePZ.expected_P, plastCombo)}атм в присутствии представителя ЦДНГ. '
                                       f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 '
                                       f'часов, с подтверждением за 2 часа до '
                                       f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {CreatePZ.expected_Q}м3/сут при давлении {CreatePZ.expected_P}атм '
                                       f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС', 0.17 + 0.52 + 0.2 + 0.2 + 0.2])

            paker_list.append([None, None,
                               f'Посадить пакера на {pakerEdit}/{paker2Edit}м. Произвести насыщение скважины до '
                               f'стабилизации давления закачки не менее 5м3. Опробовать '
                               f'пласт {plastCombo} на приемистость в трех режимах при Р={self.pressure_mode(CreatePZ.expected_P, plastCombo)}атм в присутствии представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                               f'с подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {CreatePZ.expected_Q}м3/сут при давлении {CreatePZ.expected_P}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list

        # Определение трех режимов давлений при определении приемистости

    def pressure_mode(self, mode, plast):
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

    def flushingDownhole(self, paker_depth, khvostEdit, paker_layout):
        from open_pz import CreatePZ

        flushingDownhole_list = f'Только при наличии избыточного давления или когда при проведении ОПЗ получен технологический ""СТОП":' \
                                f'произвести промывку скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'

        return flushingDownhole_list

    #
    def addRowTable(self):

        swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        if swabTrueEditType == 'Нужно освоение':
            CreatePZ.swabTrueEditType = 0
        else:
            CreatePZ.swabTrueEditType = 1
        acidEdit = self.tabWidget.currentWidget().acidEdit.currentText()
        khvostEdit = float(self.tabWidget.currentWidget().khvostEdit.text().replace(',', '.'))
        pakerEdit = float(self.tabWidget.currentWidget().pakerEdit.text().replace(',', '.'))
        paker2Edit = float(self.tabWidget.currentWidget().paker2Edit.text().replace(',', '.'))
        skvVolumeEdit = float(self.tabWidget.currentWidget().skvVolumeEdit.text().replace(',', '.'))
        skvProcEdit = float(self.tabWidget.currentWidget().skvProcEdit.text().replace(',', '.'))
        acidVolumeEdit = float(self.tabWidget.currentWidget().acidVolumeEdit.text().replace(',', '.'))
        acidProcEdit = float(self.tabWidget.currentWidget().acidProcEdit.text().replace(',', '.'))
        swab_paker = float(self.tabWidget.currentWidget().swab_pakerEdit.text().replace(',', '.'))
        swab_volume = float(self.tabWidget.currentWidget().swab_volumeEdit.text().replace(',', '.'))
        swabType = str(self.tabWidget.currentWidget().swabTypeCombo.currentText())

        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()

        plastCombo = str(self.tabWidget.currentWidget().plastCombo.currentText())
        svkTrueEdit = str(self.tabWidget.currentWidget().svkTrueEdit.currentText())
        skvAcidEdit = str(self.tabWidget.currentWidget().skvAcidEdit.currentText())
        QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        depthGaugeEdit = str(self.tabWidget.currentWidget().depthGaugeCombo.currentText())

        # privyazka = str(self.tabWidget.currentWidget().privyazka.currentText())
        if self.countAcid == 0:

            work_list = self.acidSelect(swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, depthGaugeEdit)
            CreatePZ.differencePaker = pakerEdit - paker2Edit
            CreatePZ.swabTypeComboIndex = swabType
            CreatePZ.depthGaugeEdit = depthGaugeEdit
            for row in self.acid_work(swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, paker2Edit, skvAcidEdit,
                                      acidEdit, skvVolumeEdit,
                                      QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit,
                                      CreatePZ.dict_nkt):
                work_list.append(row)
            self.populate_row(CreatePZ.ins_ind, work_list)
            CreatePZ.ins_ind += len(work_list)
            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 2

        elif self.countAcid == 1:
            paker2Edit = pakerEdit - CreatePZ.difference_paker
            CreatePZ.khvostEdit = paker2Edit

            self.acidSelect(CreatePZ.swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, CreatePZ.depthGaugeEdit)

            work_list = [
                [None, None, f'установить пакер на глубине {pakerEdit}/{paker2Edit}м', None, None, None, None, None,
                 None, None,
                 'мастер КРС', 1.2]]
            for row in self.acid_work(CreatePZ.swabTrueEditType, acidProcEdit, khvostEdit, pakerEdit, paker2Edit,
                                      skvAcidEdit, acidEdit, skvVolumeEdit,
                                      QplastEdit, skvProcEdit, plastCombo, acidOilProcEdit, acidVolumeEdit, svkTrueEdit,
                                      CreatePZ.dict_nkt):
                work_list.append(row)
            self.populate_row(CreatePZ.ins_ind, work_list)
            print(f' индекс строк {CreatePZ.ins_ind}')
            CreatePZ.ins_ind += len(work_list)
            print(f'второй индекс строк {CreatePZ.ins_ind}')

            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                CreatePZ.swabTypeComboIndex = 2

        elif self.countAcid == 2:

            # self.acidSelect(CreatePZ.swabTrueEditType, CreatePZ.khvostEdit, CreatePZ.pakerEdit)
            swabTrueEditType = True if swabTrueEditType == 'Нужно освоение' else False
            if swabTrueEditType:
                work_list = []
                swabbing_with_paker = self.swabbing_with_paker(khvostEdit, swab_paker, CreatePZ.differencePaker,
                                                               swabType, swab_volume)

                for row in swabbing_with_paker:
                    work_list.append(row)
                if CreatePZ.depthGaugeEdit == 'Да':
                    work_list.append([None, None,
                                      f'Подать заявку на вывоз глубинных манометров',
                                      None, None, None, None, None, None, None,
                                      'мастер КРС', None])
            else:
                work_list = [[None, None,
                              f'Поднять компоновку на НКТ с доливом скважины в '
                              f'объеме {round(pakerEdit * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС',
                              liftingNKT_norm(pakerEdit, 1.2)]]

            self.populate_row(CreatePZ.ins_ind, work_list)
            # print(f' индекс строк {CreatePZ.ins_ind}')
            CreatePZ.ins_ind += len(work_list)
            CreatePZ.countAcid = 0
            CreatePZ.swabTypeComboIndex = 1

            # print(f'  третья индекс строк {CreatePZ.ins_ind}')
        CreatePZ.pause = False
        self.close()

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
