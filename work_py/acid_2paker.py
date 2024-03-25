from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QInputDialog, QTabWidget, QPushButton, Qt
from PyQt5.QtWidgets import QMessageBox

import well_data
from main import MyWindow
from open_pz import CreatePZ


from work_py.rationingKRS import descentNKT_norm, well_volume_norm, liftingNKT_norm

from work_py.acid_paker import CheckableComboBox
class TabPage_SO(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.countAcid = well_data.countAcid

        self.swabTruelabelType = QLabel("необходимость освоения", self)
        self.swabTrueEditType = QComboBox(self)
        self.swabTrueEditType.addItems(['Нужно освоение', 'без освоения'])

        self.swabTrueEditType.setProperty("value", "без освоения")
        self.swabTrueEditType.setCurrentIndex(well_data.swabTrueEditType)

        self.depthGaugeLabel = QLabel("глубинные манометры", self)
        self.depthGaugeCombo = QComboBox(self)
        self.depthGaugeCombo.addItems(['Нет', 'Да'])
        self.depthGaugeCombo.setProperty("value", "Нет")

        self.pakerLabel = QLabel("глубина Нижнего пакера", self)
        self.pakerEdit = QLineEdit(self)

        self.khovstLabel = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)

        self.khvostEdit.setText(f"{1}")
        self.khvostEdit.setClearButtonEnabled(True)

        plast_work = well_data.plast_work

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)
        # self.ComboBoxGeophygist.setProperty("value", 'ГП')

        # self.privyazkaTrueLabelType = QLabel("необходимость освоения", self)
        # self.privyazkaTrueEdit = QComboBox(self)
        # self.privyazkaTrueEdit.addItems(['Нужна привязка', 'без привязки'])
        # self.privyazkaTrueEdit.setCurrentIndex(1)
        # self.privyazkaTrueEdit.setProperty('value', 'без привязки')

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_edit = QComboBox(self)
        self.svk_true_edit.addItems(['Нужно СКВ', 'без СКВ'])
        self.svk_true_edit.setCurrentIndex(1)
        self.svk_true_edit.setProperty('value', 'без СКВ')

        self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
        self.skv_acid_edit = QComboBox(self)
        self.skv_acid_edit.addItems(['HCl', 'HF'])
        self.skv_acid_edit.setCurrentIndex(0)
        self.skv_acid_edit.setProperty('value', 'HCl')

        self.skv_volume_label = QLabel("Объем СКВ", self)
        self.skv_volume_edit = QLineEdit(self)
        self.skv_volume_edit.setText('1')
        self.skv_volume_edit.setClearButtonEnabled(True)

        self.Qplast_labelType = QLabel("Нужно ли определять приемистоть до СКО", self)
        self.QplastEdit = QComboBox(self)
        self.QplastEdit.addItems(['ДА', 'НЕТ'])
        self.QplastEdit.setCurrentIndex(1)
        self.QplastEdit.setProperty('value', 'НЕТ')

        self.skv_proc_label = QLabel("Концентрация СКВ", self)
        self.skv_proc_edit = QLineEdit(self)
        self.skv_proc_edit.setClearButtonEnabled(True)
        self.skv_proc_edit.setText('15')

        self.acid_label_type = QLabel("Вид кислотной обработки", self)
        self.acid_edit = QComboBox(self)
        self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acid_edit.setCurrentIndex(0)

        self.acid_volume_label = QLabel("Объем кислотной обработки", self)
        self.acid_volume_edit = QLineEdit(self)
        self.acid_volume_edit.setText("10")
        self.acid_volume_edit.setClearButtonEnabled(True)

        self.acid_proc_label = QLabel("Концентрация кислоты", self)
        self.acid_proc_edit = QLineEdit(self)
        self.acid_proc_edit.setText('15')
        self.acid_proc_edit.setClearButtonEnabled(True)

        self.acidOilProcLabel = QLabel("объем нефти", self)
        self.acidOilProcEdit = QLineEdit(self)
        self.acidOilProcEdit.setClearButtonEnabled(True)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setClearButtonEnabled(True)
        self.pressure_edit.setText(str(well_data.max_admissible_pressure._value))

        self.swabTypeLabel = QLabel("задача при освоении", self)
        self.swabTypeCombo = QComboBox(self)
        self.swabTypeCombo.addItems(['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'])
        self.swabTypeCombo.setCurrentIndex(well_data.swabTypeComboIndex)
        self.swabTypeCombo.setProperty('value', 'Задача №2.1.16')

        self.swab_pakerLabel = QLabel("Глубина посадки нижнего пакера при освоении", self)
        self.swab_pakerEdit = QLineEdit(self)



        self.swab_volumeLabel = QLabel("объем освоения", self)
        self.swab_volumeEdit = QLineEdit(self)
        self.swab_volumeEdit.setText('20')
        if self.countAcid == 0:
            self.swab_pakerEdit.setText(str(self.pakerEdit.text()))
            self.pakerEdit.setText(f"{int(well_data.perforation_sole + 10)}")
            self.pakerEdit.textChanged.connect(self.update_paker_edit)
            self.pakerEdit.setClearButtonEnabled(True)
            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{int(well_data.perforation_roof - 10)}")
            self.paker2Edit.setClearButtonEnabled(True)

            well_data.differencePakers = int(self.pakerEdit.text()) - int(self.paker2Edit.text())
            well_data.paker2Edit = int(self.pakerEdit.text())

        if well_data.countAcid == 1:
            self.pakerEdit.setText(f"{int(well_data.paker2Edit)}")
            self.pakerEdit.textChanged.connect(self.update_paker_edit)
            self.pakerEdit.setClearButtonEnabled(True)
            self.swabTrueEditType.setCurrentIndex(well_data.swabTrueEditType)
            self.swab_pakerEdit.setText(str(self.pakerEdit.text()))
            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{int(int(well_data.paker2Edit) - well_data.differencePakers)}")
            self.paker2Edit.setClearButtonEnabled(True)

            self.swab_pakerEdit.setText(f'{well_data.swab_paker}')
            self.swab_volumeEdit.setText(f'{well_data.swab_volume}')
            for enable in [self.khovstLabel, self.khvostEdit,]:
                enable.setEnabled(False)

        elif well_data.countAcid == 2:
            self.pakerEdit.setText(f"{int(well_data.paker2Edit)}")
            self.pakerEdit.setClearButtonEnabled(True)
            self.paker2Label = QLabel("глубина вверхнего пакера", self)
            self.paker2Edit = QLineEdit(self)
            self.paker2Edit.setText(f"{int(float(well_data.paker2Edit) - well_data.differencePakers)}")
            self.paker2Edit.setClearButtonEnabled(True)

            self.swabTrueEditType.setCurrentIndex(well_data.swabTrueEditType)
            # print(f' освоение {well_data.swab_paker}')
            self.swab_pakerEdit.setText(f'{well_data.swab_paker}')
            self.swab_volumeEdit.setText(f'{well_data.swab_volume}')
            listEnabel = [self.khovstLabel, self.khvostEdit, self.swabTruelabelType, self.swabTrueEditType,
                          self.plast_combo, self.pakerEdit, self.paker2Edit,
                          self.svk_true_edit, self.QplastEdit, self.skv_proc_edit, self.acid_edit, self.acid_volume_edit,
                          self.acid_proc_edit]
            for enable in listEnabel:
                enable.setEnabled(False)

        grid = QGridLayout(self)

        grid.addWidget(self.swabTruelabelType, 0, 0)
        grid.addWidget(self.swabTrueEditType, 1, 0)

        grid.addWidget(self.plast_label, 0, 1)
        grid.addWidget(self.plast_combo, 1, 1)
        grid.addWidget(self.khovstLabel, 0, 2)
        grid.addWidget(self.khvostEdit, 1, 2)
        grid.addWidget(self.pakerLabel, 0, 3)
        grid.addWidget(self.pakerEdit, 1, 3)
        grid.addWidget(self.paker2Label, 0, 4)
        grid.addWidget(self.paker2Edit, 1, 4)

        # grid.addWidget(self.privyazkaTrueLabelType, 0, 4)
        # grid.addWidget(self.privyazkaTrueEdit, 1, 4)

        grid.addWidget(self.skv_true_label_type, 2, 0)
        grid.addWidget(self.svk_true_edit, 3, 0)
        grid.addWidget(self.skv_acid_label_type, 2, 1)
        grid.addWidget(self.skv_acid_edit, 3, 1)
        grid.addWidget(self.skv_volume_label, 2, 2)
        grid.addWidget(self.skv_volume_edit, 3, 2)
        grid.addWidget(self.skv_proc_label, 2, 3)
        grid.addWidget(self.skv_proc_edit, 3, 3)

        grid.addWidget(self.acid_label_type, 4, 1)
        grid.addWidget(self.acid_edit, 5, 1)
        grid.addWidget(self.acid_volume_label, 4, 2)
        grid.addWidget(self.acid_volume_edit, 5, 2)
        grid.addWidget(self.acid_proc_label, 4, 3)
        grid.addWidget(self.acid_proc_edit, 5, 3)
        grid.addWidget(self.acidOilProcLabel, 4, 4)
        grid.addWidget(self.acidOilProcEdit, 5, 4)
        grid.addWidget(self.pressure_Label, 4, 5)
        grid.addWidget(self.pressure_edit, 5, 5)
        grid.addWidget(self.Qplast_labelType, 4, 0)
        grid.addWidget(self.QplastEdit, 5, 0)
        grid.addWidget(self.swabTypeLabel, 6, 1)
        grid.addWidget(self.swabTypeCombo, 7, 1)
        grid.addWidget(self.swab_pakerLabel, 6, 2)
        grid.addWidget(self.swab_pakerEdit, 7, 2)
        grid.addWidget(self.swab_volumeLabel, 6, 3)
        grid.addWidget(self.swab_volumeEdit, 7, 3)
        grid.addWidget(self.depthGaugeLabel, 6, 4)
        grid.addWidget(self.depthGaugeCombo, 7, 4)

    def update_plast_edit(self):
        dict_perforation = well_data.dict_perforation

        plasts = well_data.texts

        roof_plast = well_data.current_bottom
        sole_plast = 0
        for plast in well_data.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    # print(plast, sole_plast)

                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']
                # print(f' кровля {roof_plast} подошва {sole_plast, dict_perforation[plast]["подошва"]}')
            self.pakerEdit.setText(f"{int(sole_plast + 10)}")


            if well_data.countAcid != 2:
                self.paker2Edit.setText(f"{int(roof_plast - 10)}")


    def update_paker_edit(self):
        dict_perforation = well_data.dict_perforation
        if well_data.countAcid == 0:
            plasts = well_data.texts
            # print(f' пласты {plasts}')
            roof_plast = well_data.current_bottom
            sole_plast = 0
            # for plast in well_data.plast_work:
            #     for plast_sel in plasts:
            #
            #         if plast_sel == plast:
            #             #     print(dict_perforation[plast_sel], plast)
            #             print(plast, sole_plast)
            #             if roof_plast >= dict_perforation[plast]['кровля']:
            #                 roof_plast = dict_perforation[plast]['кровля']
            #             if sole_plast < dict_perforation[plast]['подошва']:
            #                 sole_plast = dict_perforation[plast]['подошва']
            # print(f' кровля {roof_plast} подошва {sole_plast,  dict_perforation[plast]["подошва"]}')


            if self.pakerEdit.text():
                paker_depth = int(self.pakerEdit.text())
                # self.khvostEdit.setText(str(int(sole_plast - paker_depth)))
                self.swab_pakerEdit.setText(str(int(paker_depth - 30)))
        elif well_data.countAcid == 1:
            if self.pakerEdit.text():
                paker_depth = int(self.pakerEdit.text())
                self.paker2Edit.setText(str(paker_depth-well_data.difference_paker))
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
        from krs import well_volume
        from work_py.opressovka import OpressovkaEK
        if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля ' \
                          f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                          f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'Сваб {swab_volume}м3 + Профиль притока.'
        elif swab == 'Задача №2.1.16':
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и ' \
                          f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения ' \
                          f'свабированием  не менее не менее {swab_volume}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'Сваб {swab_volume}м3 + КВУ, ВНР.'
        elif swab == 'Задача №2.1.11':
            swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                          f'менее  {swab_volume}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'
            swab_short = f'Сваб {swab_volume}м3.'
        paker_depth = MyWindow.true_set_Paker(self, paker_depth)
        paker2_depth = MyWindow.true_set_Paker(self, float(paker_depth) - float(deferencePaker))

        paker_list = [

            [f'пакер на  {paker_depth}/{paker2_depth}м',
             None, f'Посадить пакера на глубине {paker_depth}/{paker2_depth}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [f'{OpressovkaEK.testing_pressure(self, paker_depth)[1]}'
                , None,
             OpressovkaEK.testing_pressure(self, paker_depth)[0],
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
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально возможное давление на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'срыв пакера (30мин). промывка {round(well_volume(self, paker_depth) * 1.5, 1)}м3',
             None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            [f'отбивка КВУ 15мин', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
            [None, None,
             f'Поднять компоновку на НКТ{well_data.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)]]
        ovtr = 'ОВТР 4ч' if well_data.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if well_data.region == 'ЧГМ' else 10
        if swab == 'Задача №2.1.13' and well_data.region not in ['ИГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        return paker_list

    def acidSelect(self, swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, depthGaugeEdit):
        from work_py.opressovka import OpressovkaEK, TabPage_SO
        from krs import well_volume


        swabTrueEditType = True if swabTrueEditType == 'Нужно освоение' else False
        difference_paker = round(pakerEdit - paker2Edit, 0)
        well_data.difference_paker = difference_paker
        pakerEdit = MyWindow.true_set_Paker(self, pakerEdit)
        paker2Edit = MyWindow.true_set_Paker(self, paker2Edit)
        paker_diametr = TabPage_SO.paker_diametr_select(self, pakerEdit)
        gidroyakor_str = ''
        if depthGaugeEdit == 'Да' and well_data.column_additional is False:
            self.paker_select = f'заглушку + сбивной с ввертышем контейнер с манометром МТГ + НКТ{well_data.nkt_diam}м ' \
                                f'{khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой ' \
                                f'фильтр НКТ {difference_paker}м + контейнер с манометром МТГ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{well_data.nkt_diam}мм 20м +' \
                                f'реперный патрубок + сбивной с ввертышем контейнер с манометром МТГ на НКТ{well_data.nkt_diam}'
            self.paker_short = f'заглушку + сбивной МТГ + НКТ{well_data.nkt_diam}м ' \
                                f'{khvostEdit}м  + пакер ПРО-ЯМО-{paker_diametr}мм + щелевой ' \
                                f'фильтр НКТ {difference_paker}м + МТГ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{well_data.nkt_diam}мм 20м +' \
                                f'реперный патрубок + МТГ на НКТ{well_data.nkt_diam}'
            dict_nkt = {73: pakerEdit}
        elif well_data.column_additional is False or (
                well_data.column_additional is True and pakerEdit < well_data.head_column_additional._value):
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{well_data.nkt_diam}м {khvostEdit}м  + ' \
                                f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + ' \
                                f'щелевой фильтр НКТ {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{well_data.nkt_diam}мм 20м + ' \
                                f'реперный патрубок на НКТ{well_data.nkt_diam}'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{well_data.nkt_diam}м {khvostEdit}м  + ' \
                               f'пакер ПРО-ЯМО-{paker_diametr}мм + щелевой фильтр НКТ {difference_paker}м ' \
                                f' + пакер ПУ - {paker_diametr} + НКТ{well_data.nkt_diam}мм 20м + ' \
                               f'репер на НКТ{well_data.nkt_diam}'
            dict_nkt = {73: pakerEdit}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and pakerEdit > well_data.head_column_additional._value:
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ{60}мм {khvostEdit}м  + пакер ПРО-ЯМО-' \
                                f'{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + ' \
                                f'щелевой фильтр НКТ{60} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{60}мм 20м +реперный патрубок ' \
                                f'на НКТ{60} {round(well_data.head_column_additional._value - pakerEdit+10,0)}'
            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ{60}мм {khvostEdit}м  + пакер ПРО-ЯМО-' \
                               f'{paker_diametr}мм + щелевой ' \
                               f'фильтр НКТ{60} {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ{60}мм 20м +репер  на ' \
                               f'НКТ{60} {round(well_data.head_column_additional._value - pakerEdit+10,0)}'
            well_data.dict_nkt = {73: well_data.head_column_additional._value - 10,
                                 60: int(pakerEdit - float(well_data.head_column_additional._value))}
            gidroyakor_str = 'ЯГ'

        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and pakerEdit > well_data.head_column_additional._value:
            self.paker_select = f'заглушку + сбивной с ввертышем + НКТ73 со снятыми фасками {khvostEdit}м  + пакер ' \
                                f'ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                                f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + щелевой ' \
                                f'фильтр НКТ73 со снятыми фасками {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ73 со снятыми фасками 20м + ' \
                                f'реперный патрубок на НКТ73 со снятыми фасками {round(well_data.head_column_additional._value - pakerEdit+10,0)}м'

            self.paker_short = f'заглушку + сбивной с ввертышем + НКТ73 со снятыми фасками {khvostEdit}м  + ' \
                               f'пакер ПРО-ЯМО-{paker_diametr}мм + щелевой фильтр НКТ73 со' \
                               f' снятыми фасками {difference_paker}м ' \
                                f'+ пакер ПУ - {paker_diametr} + НКТ73 со снятыми фасками 20м +репер' \
                               f' на НКТ73 со снятыми фасками {round(well_data.head_column_additional._value - pakerEdit+10,0)}м'
            gidroyakor_str = 'ЯГ'

            well_data.dict_nkt = {73: pakerEdit}
        elif well_data.nkt_diam == 60:
            well_data.dict_nkt = {60: pakerEdit}

        paker_list = [
            [self.paker_short, None,
             f'Спустить {self.paker_select} {gidroyakor_str} + {gidroyakor_str} на НКТ{well_data.nkt_diam}мм до глубины {pakerEdit}/{paker2Edit}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional == False else "")} ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerEdit, 1.2)],
            [f'Посадить пакер на Н- {pakerEdit}/{paker2Edit}м'
                , None, f'Посадить пакер на глубине {pakerEdit}/{paker2Edit}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.3],
            [OpressovkaEK.testing_pressure(self, pakerEdit)[1], None,
             OpressovkaEK.testing_pressure(self, pakerEdit)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.83 + 0.58],
            [f'срыв 30мин', None,
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
            paker_list.insert(0, [f'Заявить 3 глубинных манометра', None,
                                  f'Заявить 3 глубинных манометра подрядчику по ГИС',
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', None])
        return paker_list

    def acid_work(self, swabTrueEditType, acid_proc_edit, khvostEdit, pakerEdit, paker2Edit, skv_acid_edit, acid_edit,
                  skv_volume_edit,
                  QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit, dict_nkt, pressure_edit):
        from krs import volume_vn_nkt, well_volume
        paker_list = []
        swabTrueEditType = [False if swabTrueEditType == 'без СКВ' else False][0]
        skv_list = [[f'Определить приемистость при Р-{well_data.max_admissible_pressure._value}атм'
                        , None,
                     f'Определить приемистость при Р-{well_data.max_admissible_pressure._value}атм в присутствии представителя заказчика.'
                     f'при отсутствии приемистости произвести установку СКВ по согласованию с заказчиком',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 1.2],
                    [f'СКВ {skv_acid_edit} {skv_proc_edit}%', None, f'Произвести установку СКВ {skv_acid_edit} {skv_proc_edit}% концентрации в объеме'
                                 f' {skv_volume_edit}м3 (0,7т HCL 24%)(по спец. плану, составляет старший мастер)',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 1.2],
                    [None, None,
                     f'закачать {skv_acid_edit} {skv_proc_edit}% в объеме V={skv_volume_edit}м3; довести кислоту до пласта '
                     f'тех.жидкостью в объеме {volume_vn_nkt(dict_nkt)}м3 . ',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.6],
                    [ f'реагирование 2 часа.', None, f'реагирование 2 часа.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 2],
                    [f'Промывка 1,5-м объеме скв',
                         None, f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
                                 f'кратном обьеме. Посадить пакер. Определить приемистость пласта в присутствии '
                                 f'представителя ЦДНГ (составить акт). Сорвать пакер. '
                                 f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
                                 f'методом дренирования.',
                     None, None, None, None, None, None, None,
                     'мастер КРС, УСРСиСТ', 0.83 + 0.2 + 0.83 + 0.5 + 0.5]]
        print(f'СКВ {svk_true_edit}')
        if svk_true_edit == 'Нужно СКВ':
            for row in skv_list:
                paker_list.append(row)

        if acid_edit == 'HCl':

            acid_sel = f'Произвести  солянокислотную обработку {plast_combo}  в объеме  {acid_volume_edit}м3  ({acid_edit} - {acid_proc_edit} %) ' \
                       f' в присутствии представителя Заказчика с составлением акта, не превышая давления закачки не более Р={well_data.max_admissible_pressure._value}атм. \n' \
                       f'(для приготовления соляной кислоты в объеме {acid_volume_edit}м3 - {acid_proc_edit}% необходимо замешать {round(acid_volume_edit * acid_proc_edit / 24 * 1.118, 1)}т HCL 24% и' \
                       f' пресной воды {round(float(acid_volume_edit) - float(acid_volume_edit) * float(acid_proc_edit) / 24 * 1.118, 1)}м3) ' \
                       f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол. '
            acid_sel_short =f'Произвести  СКО {plast_combo}  в V  {acid_volume_edit}м3  ({acid_edit} - {acid_proc_edit} %) ' \

        elif acid_edit == 'ВТ':

            vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
            acid_sel = f'Произвести кислотную обработку {plast_combo} {vt}  в присутствии представителя ' \
                       f'Заказчика с составлением акта, не превышая давления закачки не более Р=' \
                       f'{well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = vt
        elif acid_edit == 'HF':

            acid_sel = f'Произвести глинокислотную обработку пласта {plast_combo}  в объеме  {acid_volume_edit}м3  ' \
                       f'(концентрация в смеси HF 3% / HCl 13%) силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не' \
                       f' более Р={well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'ГКО пласта {plast_combo}  в V {acid_volume_edit}м3 '
        elif acid_edit == 'Нефтекислотка':
            acid_sel = f'Произвести нефтекислотную обработку пласта {plast_combo} в V=2тн товарной нефти + ' \
                       f'{acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acidOilProcEdit) - 2}т товарной ' \
                       f'нефти силами СК Крезол ' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки ' \
                       f'не более Р={well_data.max_admissible_pressure._value}атм.'
            acid_sel_short = f'НКО пласта {plast_combo} в V=2тн товарной нефти + ' \
                       f'{acid_volume_edit}м3  (HCl - {acid_proc_edit} %) + {float(acidOilProcEdit) - 2}т товарной ' \
                       f'нефти'
        elif acid_edit == 'Противогипсовая обработка':
            acid_sel = f'Произвести противогипсовую обработку пласта{plast_combo} в объеме {acid_volume_edit}м3 - ' \
                       f'{20}% раствором каустической соды' \
                       f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                       f'более Р={well_data.max_admissible_pressure._value}атм.\n'
            acid_sel_short = f' ПГО обработку пласта{plast_combo} в объеме {acid_volume_edit}м3'
            # print(f'Ожидаемое показатели {well_data.expected_pick_up.values()}')
        print(f'внутрен {dict_nkt, volume_vn_nkt(dict_nkt)}')
        acid_list_1 = [[acid_sel_short, None,
                        f'{acid_sel}'
                        f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ И СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
                        None, None, None, None, None, None, None,
                        'мастер КРС, УСРСиСТ', None],
                       [None, None,
                        ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
                                 f"объем НКТ)" if acid_volume_edit > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                                                f"объеме {round(acid_volume_edit, 1)}м3, "
                                                                                                f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - acid_volume_edit, 1)}м3 "]),
                        None, None, None, None, None, None, None,
                        'мастер КРС', None],
                       [None, None,
                        f'посадить пакера на глубине {pakerEdit}/{paker2Edit}м',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.3],
                       [None, None,
                        ''.join(
                            [
                                f'продавить кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 при давлении не '
                                f'более {well_data.max_admissible_pressure._value}атм. Увеличение давления согласовать'
                                f' с заказчиком' if acid_volume_edit < volume_vn_nkt(
                                    dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме {round(acid_volume_edit - volume_vn_nkt(dict_nkt), 1)}м3 и тех жидкостью '
                                                   f'в объеме {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 при давлении не более {pressure_edit}атм. '
                                                   f'Увеличение давления согласовать с заказчиком']),
                        None, None, None, None, None, None, None,
                        'мастер КРС', 6],
                       [f'без реагирования' if (
                                   well_data.region == 'ТГМ' and acid_sel == 'HF') else 'реагирование 2 часа.', None,
                        f'без реагирования' if (
                                    well_data.region == 'ТГМ' and acid_sel == 'HF') else 'реагирование 2 часа.',
                        None, None, None, None, None, None, None,
                        'мастер КРС', '' if (well_data.region == 'ТГМ' and acid_sel == 'HF') else 2],

                       [f'срыв 30мин', None,
                        f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                        f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                        None, None, None, None, None, None, None,
                        'мастер КРС', 0.7],
                       [self.flushingDownhole(pakerEdit)[1], None,
                        self.flushingDownhole(pakerEdit)[0],
                        None, None, None, None, None, None, None,
                        'мастер КРС', well_volume_norm(well_volume(self, well_data.current_bottom))]
                       ]

        for row in acid_list_1:
            paker_list.append(row)

        if well_data.curator == 'ОР':
            try:
                well_data.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                              f'Ожидаемая приемистость по пласту {plast_combo} ',
                                                              well_data.expected_Q, 0,
                                                              1600)
                well_data.expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                                              f'Ожидаемое Давление закачки по пласту {plast_combo}',
                                                              well_data.expected_P, 0,
                                                              250)
            except:
                well_data.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                              f'Ожидаемая приемистость по пласту {plast_combo} ',
                                                              100, 0,
                                                              1600)
                well_data.expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                              f'Ожидаемое Давление закачки по пласту {plast_combo}',
                                                              100, 0,
                                                              250)
            if QplastEdit == 'ДА':
                paker_list.insert(-2, [f'Насыщение 5м3. Определ '
                                       f'Q-при {self.pressure_mode(well_data.expected_P, plast_combo)}атм',
                                       None,
                                       f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. '
                                       f'Опробовать '
                                       f'пласт {plast_combo} на приемистость в трех режимах при Р='
                                       f'{self.pressure_mode(well_data.expected_P, plast_combo)}атм в присутствии '
                                       f'представителя ЦДНГ. '
                                       f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 '
                                       f'часов, с подтверждением за 2 часа до '
                                       f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {well_data.expected_Q}м3/сут при '
                                       f'давлении {well_data.expected_P}атм '
                                       f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС', 0.17 + 0.52 + 0.2 + 0.2 + 0.2])

            paker_list.append([f'Посадить пакера на {pakerEdit}/{paker2Edit}м. Насыщение 5м3. Определение Q при '
                               f'{self.pressure_mode(well_data.expected_P, plast_combo)}атм ', None,
                               f'Посадить пакера на {pakerEdit}/{paker2Edit}м. Произвести насыщение скважины до '
                               f'стабилизации давления закачки не менее 5м3. Опробовать '
                               f'пласт {plast_combo} на приемистость в трех режимах при Р='
                               f'{self.pressure_mode(well_data.expected_P, plast_combo)}атм в присутствии представителя ЦДНГ. '
                               f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                               f'с подтверждением за 2 часа до '
                               f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {well_data.expected_Q}м3/сут при '
                               f'давлении {well_data.expected_P}атм '
                               f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                               None, None, None, None, None, None, None,
                               'мастер КРС', 0.5 + 0.17 + 0.15 + 0.52 + 0.2 + 0.2 + 0.2])

        return paker_list

        # Определение трех режимов давлений при определении приемистости

    def pressure_mode(self, mode, plast):

        mode = int(mode / 10) * 10
        if mode > well_data.max_admissible_pressure._value and (plast != 'D2ps' or plast.lower() != 'дпаш'):
            mode_str = f'{mode}, {mode - 10}, {mode - 20}'
        elif (plast == 'D2ps' or plast.lower() == 'дпаш') and well_data.region == 'ИГМ':
            mode_str = f'{120}, {140}, {160}'
        else:
            mode_str = f'{mode - 10}, {mode}, {mode + 10}'
        return mode_str

        # промывка скважины после кислотной обработки в зависимости от интервала перфорации и комповноки и текущего забоя

    def flushingDownhole(self, paker_depth):
        from krs import well_volume

        flushingDownhole_list = f'Только при наличии избыточного давления или когда при проведении ОПЗ получен технологический ""СТОП":' \
                                f'произвести промывку скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
        flushingDownhole_short = f'Только при наличии избыточного давления: уд.весом {well_data.fluid_work} в ' \
                                f'V- {round(well_volume(self, paker_depth) * 1.5, 1)}м3 '

        return flushingDownhole_list, flushingDownhole_short

    #
    def addRowTable(self):

        swabTrueEditType = self.tabWidget.currentWidget().swabTrueEditType.currentText()
        if swabTrueEditType == 'Нужно освоение':
            well_data.swabTrueEditType = 0
        else:
            well_data.swabTrueEditType = 1
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        khvostEdit = int(self.tabWidget.currentWidget().khvostEdit.text().replace(',', '.'))
        pakerEdit = int(self.tabWidget.currentWidget().pakerEdit.text().replace(',', '.'))
        paker2Edit = int(self.tabWidget.currentWidget().paker2Edit.text().replace(',', '.'))
        skv_volume_edit = float(self.tabWidget.currentWidget().skv_volume_edit.text().replace(',', '.'))
        skv_proc_edit = int(self.tabWidget.currentWidget().skv_proc_edit.text().replace(',', '.'))
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
        swab_paker = int(self.tabWidget.currentWidget().swab_pakerEdit.text().replace(',', '.'))
        swab_volume = int(self.tabWidget.currentWidget().swab_volumeEdit.text().replace(',', '.'))
        pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text().replace('.', ''))
        swabType = str(self.tabWidget.currentWidget().swabTypeCombo.currentText())

        acidOilProcEdit = self.tabWidget.currentWidget().acidOilProcEdit.text()

        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        svk_true_edit = str(self.tabWidget.currentWidget().svk_true_edit.currentText())
        skv_acid_edit = str(self.tabWidget.currentWidget().skv_acid_edit.currentText())
        QplastEdit = str(self.tabWidget.currentWidget().QplastEdit.currentText())
        depthGaugeEdit = str(self.tabWidget.currentWidget().depthGaugeCombo.currentText())

        if ((self.if_None(khvostEdit) == 0 or self.if_None(pakerEdit) == 0 or self.if_None(paker2Edit) == 0) and well_data.countAcid != 2):
            msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return
        # privyazka = str(self.tabWidget.currentWidget().privyazka.currentText())
        if self.countAcid == 0:

            work_list = self.acidSelect(swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, depthGaugeEdit)
            well_data.differencePaker = pakerEdit - paker2Edit
            well_data.swabTypeComboIndex = swabType
            well_data.swab_paker = swab_paker
            well_data.swab_volume = swab_volume
            well_data.depthGaugeEdit = depthGaugeEdit
            well_data.khvostEdit = khvostEdit
            well_data.swabType = swabType
            well_data.pakerEdit = pakerEdit
            for row in self.acid_work(swabTrueEditType, acid_proc_edit, khvostEdit, pakerEdit, paker2Edit, skv_acid_edit,
                                      acid_edit, skv_volume_edit,
                                      QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit,
                                      well_data.dict_nkt, pressure_edit):
                work_list.append(row)
            self.populate_row(well_data.ins_ind, work_list)
            well_data.ins_ind += len(work_list)
            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 2

        elif self.countAcid == 1:
            well_data.swab_paker = swab_paker
            well_data.swab_volume = swab_volume
            paker2Edit = pakerEdit - well_data.difference_paker
            well_data.depthGaugeEdit = depthGaugeEdit
            well_data.khvostEdit = khvostEdit
            well_data.swabType = swabType
            well_data.pakerEdit = pakerEdit



            self.acidSelect(swabTrueEditType, khvostEdit, pakerEdit, paker2Edit, well_data.depthGaugeEdit)

            work_list = [
                [f'пакер на глубине {pakerEdit}/{paker2Edit}м', None, f'установить пакер на глубине {pakerEdit}/{paker2Edit}м', None, None, None, None, None,
                 None, None,
                 'мастер КРС', 1.2]]
            for row in self.acid_work(swabTrueEditType, acid_proc_edit, khvostEdit, pakerEdit, paker2Edit,
                                      skv_acid_edit, acid_edit, skv_volume_edit,
                                      QplastEdit, skv_proc_edit, plast_combo, acidOilProcEdit, acid_volume_edit, svk_true_edit,
                                      well_data.dict_nkt, pressure_edit):
                work_list.append(row)
            self.populate_row(well_data.ins_ind, work_list)
            print(f' индекс строк {well_data.ins_ind}')
            well_data.ins_ind += len(work_list)
            print(f'второй индекс строк {well_data.ins_ind}')

            if swabType == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 0
            elif swabType == 'Задача №2.1.16':  # , 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 1
            elif swabType == 'Задача №2.1.11':  # , 'Задача №2.1.11', 'своя задача'
                well_data.swabTypeComboIndex = 2

        elif self.countAcid == 2:

            # self.acidSelect(well_data.swabTrueEditType, well_data.khvostEdit, well_data.pakerEdit)
            swabTrueEditType = True if swabTrueEditType == 'Нужно освоение' else False
            if swabTrueEditType:
                work_list = []
                swabbing_with_paker = self.swabbing_with_paker(well_data.khvostEdit, well_data.swab_paker, well_data.differencePaker,
                                                               well_data.swabType, well_data.swab_volume)

                for row in swabbing_with_paker:
                    work_list.append(row)
                if well_data.depthGaugeEdit == 'Да':
                    work_list.append([f'Подать заявку на вывоз глубинных манометров', None,
                                      f'Подать заявку на вывоз глубинных манометров',
                                      None, None, None, None, None, None, None,
                                      'мастер КРС', None])
            else:
                work_list = [[None, None,
                              f'Поднять компоновку на НКТ с доливом скважины в '
                              f'объеме {round(well_data.pakerEdit * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС',
                              liftingNKT_norm(pakerEdit, 1.2)]]

            self.populate_row(well_data.ins_ind, work_list)
            # print(f' индекс строк {well_data.ins_ind}')
            well_data.ins_ind += len(work_list)
            well_data.countAcid = 0
            well_data.swabTypeComboIndex = 1

            # print(f'  третья индекс строк {well_data.ins_ind}')
        well_data.pause = False
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

    def if_None(self, value):

        if isinstance(value, int) or isinstance(value, float):
            return int(value)

        elif str(value).replace('.','').replace(',','').isdigit():
            if str(round(float(value.replace(',','.')), 1))[-1] == 0:
                return int(float(value.replace(',','.')))
        else:
            return 0

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = AcidPakerWindow()
    window.show()
    sys.exit(app.exec_())
