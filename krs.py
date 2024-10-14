from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, \
    QPushButton
from datetime import datetime

import well_data
from main import MyMainWindow
from work_py.alone_oreration import lifting_unit, weigth_pipe, volume_pod_NKT, pvo_gno, volume_jamming_well
from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import liftingNKT_norm


class TabPageGno(QWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.work_plan = work_plan

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)
        self.current_bottom_edit.setText(f'{well_data.current_bottom}')

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)
        self.fluid_edit.setText(f'{self.calc_fluid(self.work_plan, well_data.current_bottom)}')

        self.volume_jumping_label = QLabel("Объем глушения", self)
        self.volume_jumping_edit = QLineEdit(self)
        volume_well_jaming = self.volume()
        if abs(float(well_data.well_volume_in_PZ[0]) - volume_well_jaming) > 0.5:
            QMessageBox.warning(None, 'Некорректный объем скважины',
                                      f'Объем скважины указанный в ПЗ -{well_data.well_volume_in_PZ}м3 не совпадает '
                                      f'с расчетным {volume_well_jaming}м3')
            volume_well_jaming, _ = QInputDialog.getDouble(self,
                                                           "корректный объем",
                                                           'Введите корректный объем', volume_well_jaming, 1, 80, 1)
        self.volume_jumping_edit.setText(f'{volume_well_jaming}')

        self.gno_label = QLabel("вид поднимаемого ГНО", self)
        self.gno_combo = QComboBox(self)
        gno_list = ['пакер', 'ОРЗ', 'ОРД', 'воронка', 'НН с пакером', 'НВ с пакером',
                    'ЭЦН с пакером', 'ЭЦН', 'НВ', 'НН', 'ЭЦН с автономными пакерами']
        self.gno_combo.addItems(gno_list)
        lift_key = self.select_gno()

        self.surfactant_hydrofabizer_label = QLabel("Необходимость гидрофабизатора ПАВ", self)
        self.surfactant_hydrofabizer_Combo = QComboBox(self)
        self.surfactant_hydrofabizer_Combo.addItems(['Нет', 'Да'])

        self.gno_combo.setCurrentIndex(gno_list.index(lift_key))

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.gno_label, 4, 3)
        self.grid.addWidget(self.gno_combo, 5, 3)
        self.grid.addWidget(self.current_bottom_label, 4, 4)
        self.grid.addWidget(self.current_bottom_edit, 5, 4)
        self.grid.addWidget(self.fluid_label, 4, 5)
        self.grid.addWidget(self.fluid_edit, 5, 5)
        self.grid.addWidget(self.volume_jumping_label, 4, 6)
        self.grid.addWidget(self.volume_jumping_edit, 5, 6)
        self.grid.addWidget(self.surfactant_hydrofabizer_label, 4, 7)
        self.grid.addWidget(self.surfactant_hydrofabizer_Combo, 5, 7)

        for plast in well_data.plast_work:
            if plast in ['Сбоб-рад', 'Сбоб', 'Crr-bb', 'CI', 'CII', 'CIII', 'СIV0', 'CIV', 'CV', 'CVI', 'CVI0', 'D2ps',
                         'Дпаш', 'Дкын', 'C1rd-bb-tl', 'Ctl']:
                self.surfactant_hydrofabizer_Combo.setCurrentIndex(1)

        self.gno_combo.currentTextChanged.connect(self.update_select_gno)

    def update_select_gno(self, index):
        self.current_bottom_ecn_label = QLabel('голова извлекаемых пакеров')
        self.current_bottom_ecn_edit = QLineEdit(self)

        if index == 'ЭЦН с автономными пакерами':
            self.grid.addWidget(self.current_bottom_ecn_label, 4, 8)
            self.grid.addWidget(self.current_bottom_ecn_edit, 5, 8)
        else:
            # self.grid.addWidget(self.current_bottom_ecn_label, 4, 7)
            # self.grid.addWidget(self.current_bottom_ecn_edit, 5, 7)
            self.current_bottom_ecn_edit.setParent(None)
            self.current_bottom_ecn_label.setParent(None)

    @staticmethod
    def select_gno():
        lift_key = ''
        if well_data.if_None(well_data.dict_pump_ECN["do"]) != 'отсут' and \
                well_data.if_None(well_data.dict_pump_SHGN["do"]) != 'отсут':
            lift_key = 'ОРД'
        elif well_data.if_None(well_data.dict_pump_ECN["do"]) != 'отсут' and \
                well_data.if_None(well_data.paker_do["do"]) == 'отсут':
            lift_key = 'ЭЦН'
        elif well_data.if_None(well_data.dict_pump_ECN["do"]) != 'отсут' and \
                well_data.if_None(well_data.paker_do['do']) != 'отсут':
            lift_key = 'ЭЦН с пакером'
        elif well_data.if_None(well_data.dict_pump_SHGN["do"]) != 'отсут' and \
                well_data.dict_pump_SHGN["do"].upper() != 'НН' \
                and well_data.if_None(well_data.paker_do['do']) == 'отсут':
            lift_key = 'НВ'
        elif well_data.if_None(well_data.dict_pump_SHGN["do"]) != 'отсут' and \
                well_data.if_None(well_data.dict_pump_SHGN["do"]).upper() != 'НН' \
                and well_data.if_None(well_data.paker_do['do']) != 'отсут':
            lift_key = 'НВ с пакером'
        elif 'НН' in well_data.if_None(well_data.dict_pump_SHGN["do"]).upper() \
                and well_data.if_None(well_data.paker_do['do']) == 'отсут':
            lift_key = 'НН'
        elif 'НН' in well_data.if_None(well_data.dict_pump_SHGN["do"]).upper() and \
                well_data.if_None(well_data.if_None(well_data.paker_do['do'])) != 'отсут':
            lift_key = 'НН с пакером'
        elif well_data.if_None(well_data.dict_pump_SHGN["do"]) == 'отсут' and \
                well_data.if_None(well_data.paker_do['do']) == 'отсут' \
                and well_data.if_None(well_data.dict_pump_ECN["do"]) == 'отсут':
            lift_key = 'воронка'

        elif '89' in well_data.dict_nkt.keys() and '48' in well_data.dict_nkt.keys() and \
                well_data.if_None(
                    well_data.paker_do['do']) != 'отсут':
            lift_key = 'ОРЗ'
        elif well_data.if_None(well_data.dict_pump_SHGN["do"]) == 'отсут' and \
                well_data.if_None(well_data.paker_do['do']) != 'отсут' \
                and well_data.if_None(well_data.dict_pump_ECN["do"]) == 'отсут':
            lift_key = 'пакер'
        return lift_key

    def volume(self):
        from work_py.alone_oreration import volume_jamming_well, volume_rod, volume_nkt_metal

        volume_well_jaming = round((volume_jamming_well(self, well_data.current_bottom) - volume_nkt_metal(
            well_data.dict_nkt) - volume_rod(self, well_data.dict_sucker_rod) - 0.2) * 1.1, 1)

        return volume_well_jaming

    @staticmethod
    def calc_fluid(work_plan, current_bottom):
        fluid_list = []
        if work_plan != 'gnkt_frez':
            well_data.current_bottom = current_bottom
        # Задаем начальную и конечную даты периода
        current_date = well_data.current_date
        if current_date.month > 4:
            start_date = datetime(current_date.year, 12, 1).date()
            end_date = datetime(current_date.year + 1, 4, 1).date()
        else:
            start_date = datetime(current_date.year - 1, 12, 1).date()
            end_date = datetime(current_date.year, 4, 1).date()

        # Проверяем условие: если текущая дата находится в указанном периоде    
        if well_data.region in ['КГМ', 'АГМ']:
            fluid_p = 1.02
        else:
            fluid_p = 1.01
        aase = well_data.plast_work

        a = well_data.dict_perforation
        for plast in well_data.plast_work:

            if float(list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]) > fluid_p:
                fluid_p = list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]
        fluid_list.append(fluid_p)
        if max(fluid_list) <= 1.18:

            if start_date <= current_date <= end_date and max(fluid_list) <= 1.18:
                fluid_max = 1.18
            else:
                fluid_max = max(fluid_list)
        else:
            fluid_max = max(fluid_list)
        if work_plan == 'gnkt_frez' or work_plan == 'gnkt_opz':
            fluid_max = 1.18
        return fluid_max


class TabWidget(QTabWidget):
    def __init__(self, work_plan):
        super().__init__()
        self.addTab(TabPageGno(work_plan), 'Подьем ГНО')


class GnoWindow(MyMainWindow):
    def __init__(self, ins_ind, table_widget, work_plan):

        super(GnoWindow, self).__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.ins_ind = ins_ind
        well_data.ins_ind2 = ins_ind
        self.table_widget = table_widget
        self.work_plan = work_plan
        self.tabWidget = TabWidget(self.work_plan)

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):

        from work_py.advanted_file import definition_plast_work
        current_widget = self.tabWidget.currentWidget()
        try:
            self.surfactant_hydrofabizer_Combo = current_widget.surfactant_hydrofabizer_Combo.currentText()
            lift_key = current_widget.gno_combo.currentText()
            current_bottom = round(float(current_widget.current_bottom_edit.text().replace(',', '.')),
                                   1)
            fluid = current_widget.fluid_edit.text()
            volume_well_jaming = round(
                float(current_widget.volume_jumping_edit.text().replace(',', '.')), 1)

            well_data.fluid_work, well_data.fluid_work_short = self.calc_work_fluid(fluid)
            well_data.current_bottom = current_bottom
            definition_plast_work(self)
            work_list = self.work_krs(self.work_plan, lift_key, volume_well_jaming, fluid)
            if lift_key == 'ЭЦН с автономными пакерами':
                current_bottom_ecn_edit = round(float(current_widget.current_bottom_ecn_edit.text()), 1)
                well_data.current_bottom = current_bottom_ecn_edit

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

            return

        check_question = QMessageBox.question(self, 'Корректность забой', f'Забой который можно нормализовать '
                                                                          f'без использования ВЗД на '
                                                                          f'глубине {current_bottom}м, корректен?')

        if check_question == QMessageBox.StandardButton.No:
            return
        self.populate_row(self.ins_ind, work_list, self.table_widget)
        well_data.current_bottom = current_bottom

        well_data.pause = False
        self.close()

    def work_krs(self, work_plan, lift_key, volume_well_jaming, fluid):
        from work_py.rationingKRS import lifting_sucker_rod, well_jamming_norm, liftingGNO
        from work_py.alone_oreration import well_jamming, konte
        from work_py.descent_gno import TabPage_Gno

        well_data.fluid_work, well_data.fluid_work_short = self.calc_work_fluid(fluid)
        nkt_diam_fond = TabPage_Gno.gno_nkt_opening(well_data.dict_nkt)
        surfactant_hydrofabizer_str = ''
        if self.surfactant_hydrofabizer_Combo == 'Да':
            surfactant_hydrofabizer_str = 'с добавлением в жидкость глушения гидрофобизатора из расчёта' \
                                          ' 0,05% на 1м3 (0,5л)'

        if work_plan not in ['dop_plan', 'dop_plan_in_base']:

            without_damping_True = well_data.without_damping
            print(f'без глушения {without_damping_True}')

            if any([cater == 1 for cater in well_data.cat_P_1]):
                well_data.kat_pvo, _ = QInputDialog.getInt(self, 'Категория скважины',
                                                           f'Категория скважины № {well_data.kat_pvo}, корректно?',
                                                           well_data.kat_pvo, 1, 2)

            well_jamming_str_in_nkt = " " if without_damping_True is True \
                else f"По результату приемистости произвести глушение скважины в НКТ тех.жидкостью в объеме " \
                     f"обеспечивающим " \
                     f"заполнение трубного пространства и скважины в подпакерной зоне в объеме " \
                     f"{volume_pod_NKT(self)} м3 " \
                     f"жидкостью уд.веса {well_data.fluid_work} при давлении не более " \
                     f"{well_data.max_admissible_pressure._value}атм. " \
                     f"Тех отстой 1-2 часа. Произвести замер избыточного давления в скважине."

            krs_begin = [
                [None, None,
                 f'Начальнику смены ЦТКРС, вызвать телефонограммой представителя Заказчика для оформления АКТа '
                 f'приёма-передачи скважины в ремонт. \n'
                 f'Совместно с представителем Заказчика оформить схему расстановки оборудования при КРС с обязательной '
                 f'подписью представителя Заказчика на схеме.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст-ль Заказчика.', float(0.5)],
                [None, None,
                 f'Принять скважину в ремонт у Заказчика с составлением АКТа. Переезд  бригады. '
                 f'Подготовительные работы '
                 f'к КРС. Определить технологические '
                 f'точки откачки жидкости у Заказчика согласно Договора.',
                 None, None, None, None, None, None, None,
                 ' Предст-тель Заказчика, мастер КРС', float(0.5)],
                [None, 3,
                 f'Перед началом работ по освоению, капитальному и текущему ремонту скважин бригада должна быть '
                 f'ознакомлена '
                 f'с возможными осложнениями и авариями'
                 f'в процессе работ, планом локализации и ликвидации аварии (ПЛА) и планом работ. С работниками должен '
                 f'быть проведен инструктаж по выполнению работ, '
                 f'связанных с применением новых технических устройств и технологий с соответствующим оформлением в'
                 f'журнал инструктажей на рабочем месте ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [None, 4,
                 f'При подъеме труб из скважины производить долив тех. жидкостью Y- {well_data.fluid_work}. '
                 f'Долив скважины '
                 f'должен быть равен объему извлекаемого металла.'
                 f'По мере расхода жидкости из ёмкости, производить своевременное её заполнение. При всех '
                 f'технологических '
                 f'спусках НКТ 73мм х 5,5мм и 60мм х 5мм производить '
                 f'контрольный замер и отбраковку + шаблонирование шаблоном {well_data.nkt_template}мм d=59,6мм и 47,'
                 f'9мм '
                 f'соответственно.',
                 None, None, None, None, None, None, None,
                 ' Мастер КРС.', None],
                [None, None,
                 f'ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ ПРОИЗВОДИТЬ НА ТЕХ ЖИДКОСТИ УД. ВЕСОМ РАВНОЙ {well_data.fluid_work} '
                 f'{surfactant_hydrofabizer_str}', None,
                 None, None, None, None, None, None, None,
                 None],
                [None, None, f'Замерить Ризб. При наличии избыточного давления произвести замер Ризб и уд.вес '
                             f'жидкости излива, по результату замеру произвести перерасчет и корректировку удельного '
                             f'веса тех.жидкости',
                 None, None, None, None, None, None, None,
                 ' Мастер КРС.', 0.5],
                [None, None,
                 f'Согласно инструкции ООО Башнефть-Добыча ПЗ-05 И-102089Ю ЮЛ-305 версия 2 п. 9.1.9 при отсутствии '
                 f'избыточного давления и '
                 f'наличии риска поглощения жидкости глушения. произвести замер статического уровня силами ЦДНГ перед '
                 f'началом работ и в '
                 f'процессе ремонта (с периодичностью определяемой ответственным руководителем работ, по согласованию с'
                 f' представителем Заказчика '
                 f'Результаты замеров статического уровня фиксировать в вахтовом журнале и передавать в сводке '
                 f'При изменении '
                 f'уровня в скважине от первоначально замеренного на 100м и более метров в сторону уменьшения или '
                 f'возрастания, '
                 f'необходимо скорректировать объем долива идобиться стабилизации уровня в скважине. Если по данным '
                 f'замера уровень в '
                 f'скважине растет, необходимо выполнить повторноеглушение скважины, сделав перерасчет плотности '
                 f'жидкости глушения в '
                 f'соответствии суточненными геологической службой данными по пластовому давлению.',
                 None, None, None, None, None, None, None,
                 ' Мастер КРС.', 1.5]
            ]
            if well_data.bvo is True:
                for row in mkp_revision_1_kateg(self):
                    krs_begin.insert(-3, row)

            update_change_fluid_str = [
                [None, None,
                 f'При отсутствии избыточного давления произвести замер статического уровня в присутствии представителя'
                 f' заказчика. Составить акт. По результатам замера статического уровня согласовать с заказчиком '
                 f'глушение скважины уд. весом 1,17{well_data.fluid_work[4:]} в алгоритме указанном ниже. '
                 f'При положительном результате глушения дальнейшие работ продолжить с учетом изменения уд.веса '
                 f'рабочей жидкости.',
                 None, None, None, None, None, None, None,
                 ' Мастер КРС.', None]]

            if float(fluid) > 1.18:
                krs_begin.insert(-1, update_change_fluid_str[0])

            posle_lift = [
                [None, None,
                 f'По результатам подъема провести ревизию НКТ в присутствии представителя ЦДНГ. В случае '
                 f'обнаружения дефекта НКТ, вызвать '
                 f'представителя ЦДНГ, составить акт. На Отказные НКТ закрепить бирку " на расследование", '
                 f'сдать в ООО "РН-Ремонт НПО" '
                 f'отдельно, с пометкой в БНД-25 "на расследование". Произвести Фотофиксацию отказных '
                 f'элементов, '
                 f'БНД-25. Фото предоставить в '
                 f'технологический отдел В течение 24 часов после подъема согласовать с ЦДНГ '
                 f'необходимость замены,'
                 f' пропарки, промывки ГНО, '
                 f'технологию опрессовки НКТ согласовать с ПТО', None, None,
                 None, None, None, None, None,
                 'Мастер КРС, представитель Заказчика', 0.5],
                [None, None,
                 f'Опрессовать глухие плашки превентора (после подъема инструмента, согласно ТИ № И2-05.01 '
                 f'И-01447 ЮЛ-111.13 версия 1.00  п. 5.34) на  '
                 f'{well_data.max_admissible_pressure._value}атм на '
                 f'максимально допустимое давление опрессовки эксплуатационной колонны с'
                 f' выдержкой в течении 30 '
                 f'минут,в случае невозможности '
                 f'опрессовки по результатам определения приемистости и по согласованию с '
                 f'заказчиком  опрессовать '
                 f'глухие плашки ПВО на давление поглощения, (согласно ТИ № П2-05.01 ТИ-0001 версия 3.00 п. '
                 f'5.3.14; Инструкция № П2-05.01 И-01447 ЮЛ-111.13 версия 1.00 п.5.34; 5-36)'
                 f'но не менее 30атм и  с составлением акта на опрессовку ПВО с представителем Заказчика '
                 f'(согласно ТИ № П2-05.01 ТИ-0001 версия 3.00 п. 5.3.14).  ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', 0.67],
                [None, None,
                 f'Скорость спуска (подъема) погружного оборудования в скважину не должна превышать 0,25 м/с '
                 f'в наклонно-направленных и '
                 f'горизонтальных скважинах. В скважинах набором кривизны более 1,5 градуса на 10 м скорость '
                 f'пуска (подъёма) не должна превышать '
                 f'0,1 м/с в интервалах искривления. Произвести визуальный осмотр колонной муфты и ниппеля '
                 f'колонного патрубка, отревизировать переводники. '
                 f'При отбраковке дать заявку в цех Заказчика на замену. Составить акт (при '
                 f'изменении альтитуды '
                 f'муфты э/колонны указать в акте).',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 f'В СЛУЧАЕ ВЫНУЖДЕННОГО ПРОДОЛЖИТЕЛЬНОГО ПРОСТОЯ ПО ЗАВОЗУ ТЕХНОЛОГИЧЕСКОГО '
                 f'ИЛИ ФОНДОВОГО ОБОРУДОВАНИЯ В СКВАЖИНУ НЕОБХОДИМО СПУСКАТЬ '
                 f'ПРОТИВОФОНТАННЫЙ ЛИФТ ДЛИНОЙ 300м. ', None, None,
                 None, None, None, None, None, 'Мастер КРС представитель Заказчика', None]]

            kvostovika_lenght = round(
                sum(list(well_data.dict_nkt.values())) - float(well_data.depth_fond_paker_do["do"]), 1)

            kvostovik = f' + хвостовиком {kvostovika_lenght}м ' if well_data.region == 'ТГМ' and \
                                                                   kvostovika_lenght > 0.001 else ''

            well_jamming_str = well_jamming(self, without_damping_True, lift_key,
                                            volume_well_jaming)  # экземпляр функции расчета глушения
            well_jamming_ord = volume_jamming_well(self, float(well_data.depth_fond_paker_do["do"]))
            lift_ord = [
                [f'Опрессовать ГНО на Р={40}атм', None,
                 f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять '
                 f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ '
                 f'НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.67],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'подьем {well_data.dict_pump_SHGN["do"]}', None,
                 f'Сорвать насос штанговый насос {well_data.dict_pump_SHGN["do"]}(зафиксировать вес при срыве).'
                 f' Обвязать устье скважины согласно схемы №3 утвержденной главным '
                 f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг '
                 f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
                 f'{well_data.max_admissible_pressure._value}атм. '
                 f'{"".join([" " if without_damping_True is True else f"Приподнять штангу. Произвести глушение в затрубное пространство в объеме{well_jamming_ord}м3 (объем колонны от пакера до устья уд.весом {well_data.fluid_work}. Техостой 2ч."])}'
                 f'Поднять на штангах насос с гл. {well_data.dict_pump_SHGN_h["do"]}м с доливом тех жидкости '
                 f'уд.весом {well_data.fluid_work} '
                 f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве '
                 f'насосов (не более 8 тн), без учета веса '
                 f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО '
                 f'региона  постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный отворот НШ с '
                 f'последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с '
                 f'подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 lifting_sucker_rod(well_data.dict_sucker_rod)],
                [f'Сорвать планшайбу и пакер  не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                 f'выдержкой 30мин для возврата резиновых элементов в исходное положение '
                 f'в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
                 f'более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
                 f'результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 + АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                 f'часов, через 5 часов '
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона -  для составления '
                 f'алгоритма '
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 0.67 + 1 + 0.07 + 0.32 + 0.45 + 0.3 + 0.23 + 0.83],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 ''.join(
                     ["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на "
                           "производство "
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                           "опасность для жизни людей "
                           "и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                           "Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде "
                           "ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', 2.8],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и '
                     'Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять  {well_data.dict_pump_ECN["do"]} с пакером {well_data.paker_do["do"]}',
                 None,
                 f'Поднять  {well_data.dict_pump_ECN["do"]} с пакером {well_data.paker_do["do"]} с '
                 f'глубины {round(sum(list(well_data.dict_nkt.values())), 1)}м (компоновка НКТ {nkt_diam_fond} '
                 f'на поверхность '
                 f'с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд.'
                 f' весом {well_data.fluid_work} '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с '
                 f'контролем АСПО '
                 f'на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)]
            ]
            lift_ecn_with_2paker = [
                [f'Опрессовать ГНО на Р=50атм', None,
                 'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. (Вызов '
                 'представителя осуществлять '
                 'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ'
                 ' ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [f'Сбить сбивной клапан. {well_jamming_str[2]}', None,
                 f'Сбить сбивной клапан. {well_jamming_str[0]}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика', 3.2],
                [None, None, well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Сорвать планшайбу не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
                 f'не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном'
                 f' результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  '
                 f'с противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                 f'часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                 f'алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на "
                               "производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                               "опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                               "ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде "
                               "ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0],
                 None,
                 None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять {well_data.dict_pump_ECN["do"]} с глубины {round(well_data.dict_pump_ECN_h["do"], 1)}м',
                 None,
                 f'Поднять  {well_data.dict_pump_ECN["do"]} с глубины '
                 f'{round(well_data.dict_pump_ECN_h["do"], 1)}м '
                 f' на поверхность с замером, '
                 f'накручиванием колпачков с доливом скважины '
                 f'тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с '
                 f'контролем АСПО'
                 f' на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)],
            ]
            lift_ecn = [
                [f'Опрессовать ГНО на Р=50атм', None,
                 'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. (Вызов '
                 'представителя осуществлять '
                 'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ'
                 ' ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [f'Сбить сбивной клапан. {well_jamming_str[2]}', None,
                 f'Сбить сбивной клапан. {well_jamming_str[0]}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика', 3.2],
                [None, None, well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Сорвать планшайбу не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
                 f'не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном'
                 f' результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  '
                 f'с противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                 f'часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                 f'алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на "
                               "производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                               "опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                               "ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде "
                               "ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 'Заглубить оставшийся  кабель в скважину на 1-3 технологических НКТ' + pvo_gno(well_data.kat_pvo)[0],
                 None,
                 None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [
                    f'Поднять  {well_data.dict_pump_ECN["do"]} с глубины {round(well_data.dict_pump_ECN_h["do"], 1)}м',
                    None,
                    f'Поднять  {well_data.dict_pump_ECN["do"]} с глубины '
                    f'{round(well_data.dict_pump_ECN_h["do"], 1)}м '
                    f'на поверхность с замером, накручиванием колпачков с доливом скважины '
                    f'тех.жидкостью уд. весом {well_data.fluid_work}  '
                    f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с '
                    f'контролем АСПО'
                    f' на стенках НКТ.',
                    None, None,
                    None, None, None, None, None,
                    'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)],
            ]

            lift_ecn_with_paker = [
                ['Опрессовать ГНО на Р=50атм', None,
                 'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. '
                 '(Вызов представителя осуществлять '
                 'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ'
                 ' ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [None, None,
                 f'Сбить сбивной клапан. '
                 f'{"".join([" " if without_damping_True is True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Произвести глушение в НКТ в объеме {volume_pod_NKT(self)}м3. {well_data.fluid_work}"])}'

                    , None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'срыв пакера не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки '
                 f'с выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя '
                 f'ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
                 f'более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                 f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
                 f'не более 6 часов, '
                 f'через 5 часов с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона '
                 f'- для составления алгоритма последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на "
                               "производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                               "опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                               "ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде"
                               " ВЫБРОС. "
                               "Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять  {well_data.dict_pump_ECN["do"]} с пакером {well_data.paker_do["do"]}', None,
                 f'Поднять  {well_data.dict_pump_ECN["do"]} с пакером {well_data.paker_do["do"]}'
                 f'с глубины {round(sum(list(well_data.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) '
                 f'на поверхность с замером, накручиванием '
                 f'колпачков с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.22 / 1000, 1)}м3 с контролем'
                 f' АСПО на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)],
            ]
            lift_pump_nv = [
                [f'Опрессовать ГНО на Р={40}атм', None,
                 f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять '
                 f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ '
                 f'ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Поднять {well_data.dict_pump_SHGN["do"]} с гл. {well_data.dict_pump_SHGN_h["do"]}м', None,
                 f'Сорвать насос {well_data.dict_pump_SHGN["do"]} (зафиксировать вес при срыве). '
                 f'Обвязать устье скважины '
                 f'согласно схемы №3 утвержденной главным '
                 f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг '
                 f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
                 f'{well_data.max_admissible_pressure._value}атм. Поднять на штангах насос '
                 f'с гл. {int(well_data.dict_pump_SHGN_h["do"])}м с доливом тех жидкости уд.весом {well_data.fluid_work} '
                 f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), '
                 f'без учета веса '
                 f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
                 f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ '
                 f'с последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с'
                 f' подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 lifting_sucker_rod(well_data.dict_sucker_rod)],
                [f'Сорвать планшайбу не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
                 f'не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
                 f'результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
                 f'не более 6 часов, '
                 f'через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
                 f'для составления алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [None, None,
                 ''.join(
                     ["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на"
                           " производство "
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                           "опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                           "ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде "
                           "ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else
                     'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости'
                 f' глушения и промывки с '
                 f'записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [
                f'{"".join(["Допустить фНКТ для определения текущего забоя. " if well_data.gipsInWell is True else ""])}Поднять  замковую опору с глубины {round(sum(list(well_data.dict_nkt.values())), 1)}м',
                None,
                f'{"".join(["Допустить фНКТ для определения текущего забоя. " if well_data.gipsInWell is True else ""])}Поднять  замковую опору  на НКТ с глубины {round(sum(list(well_data.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 '
                f'с контролем АСПО на стенках НКТ.',
                None, None,
                None, None, None, None, None,
                'Мастер КРС', liftingGNO(well_data.dict_nkt)],
            ]
            lift_pump_nv_with_paker = [
                [f'Опрессовать ГНО на Р={40}атм', None,
                 f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять '
                 f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ '
                 f'НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Поднять насос {well_data.dict_pump_SHGN["do"]}', None,
                 f'Сорвать насос {well_data.dict_pump_SHGN["do"]} (зафиксировать вес при срыве). Обвязать устье скважины '
                 f'согласно схемы №3 утвержденной главным '
                 f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). '
                 f'Опрессовать ПВО на {well_data.max_admissible_pressure._value}атм. '
                 f'{"".join([" " if without_damping_True is True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу. Произвести глушение в НКТ в объеме{volume_pod_NKT(self)}м3. Техостой 2ч."])}'
                 f' Поднять на штангах насос с гл. {float(well_data.dict_pump_SHGN_h["do"])}м с '
                 f'доливом тех жидкости уд.весом {well_data.fluid_work} '
                 f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  '
                 f'насосов (не более 8 тн), без учета веса '
                 f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона '
                 f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный '
                 f'отворот НШ с последующим '
                 f'комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с '
                 f'подтверждением супервайзера, '
                 f'распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 lifting_sucker_rod(well_data.dict_sucker_rod)],
                [f'Сорвать планшайбу и пакер не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                 f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
                 f'в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
                 f'не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
                 f'результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не '
                 f'более 6 часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
                 f'для составления алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на"
                               " производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                               "собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                               "Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по "
                               "команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else \
                         'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять  З.О. с пакером {well_data.paker_do["do"]}', None,
                 f'Поднять  замковую опору с пакером {well_data.paker_do["do"]} с глубины'
                 f' {round(sum(list(well_data.dict_nkt.values())), 1)}м  (компоновка НКТ{nkt_diam_fond}) на '
                 f'поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с '
                 f'контролем АСПО на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)],
            ]
            lift_pump_nn = [
                [f'Опрессовать ГНО на Р={40}атм', None,
                 f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять '
                 f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ '
                 f'ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'поднять плунжен', None,
                 f'Сорвать  плунжер. (зафиксировать вес при срыве). Обвязать устье скважины согласно схемы №3 '
                 f'утвержденной главным '
                 f'инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
                 f'{well_data.max_admissible_pressure._value}атм. Заловить конус спуском одной '
                 f'штанги. Поднять на штангах плунжер с гл. {float(well_data.dict_pump_SHGN_h["do"])}м с доливом тех '
                 f'жидкости уд.весом {well_data.fluid_work} '
                 f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов '
                 f'(не более 8 тн), без учета веса '
                 f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
                 f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с '
                 f'последующим '
                 f'комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением '
                 f'супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 lifting_sucker_rod(well_data.dict_sucker_rod)],
                [f'Сорвать планшайбу не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
                 f'не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
                 f'результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с'
                 f' противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
                 f'не более 6 часов, '
                 f'через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                 f'алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения "
                               "на производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                               "собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                               "Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение "
                               "по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять  {well_data.dict_pump_SHGN["do"]}', None,
                 f'Поднять  {well_data.dict_pump_SHGN["do"]} с глубины {round(well_data.dict_pump_SHGN_h["do"], 1)}м '
                 f'(компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины '
                 f'тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО '
                 f'на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', liftingGNO(well_data.dict_nkt)],
            ]
            lift_pump_nn_with_paker = [
                [f'Опрессовать ГНО на Р={40}атм', None,
                 f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять '
                 f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ '
                 f'НЕГЕРМЕТИЧНОСТИ НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                ['Поднять плунжер', None,
                 f'Сорвать плунжер насоса (зафиксировать вес при срыве). Обвязать устье скважины согласно '
                 f'схемы №3 утвержденной главным '
                 f'инженером {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
                 f'{well_data.max_admissible_pressure._value}атм. Спуском одной штанги заловить конус. '
                 f'{"".join([" " if without_damping_True is True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу. Произвести глушение в НКТ в объеме{volume_pod_NKT(self)}м3. Техостой 2ч."])}'

                 f' Поднять на штангах плунжер с гл. {int(well_data.dict_pump_SHGN_h["do"])}м с доливом тех '
                 f'жидкости уд.весом {well_data.fluid_work} '
                 f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве '
                 f'насосов (не более 8 тн), без учета веса '
                 f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона '
                 f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с '
                 f'последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с'
                 f' подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора '
                 f'учета НКТ и НШ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 lifting_sucker_rod(well_data.dict_sucker_rod)],
                [f'Сорвать планшайбу и пакер  не '
                 f'более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)',
                 None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                 f'выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя'
                 f' ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
                 f'более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
                 f'результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  '
                 f'с противодавлением в НКТ (время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на '
                 f'расхаживание - не более 6 часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления'
                 f' алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения "
                               "на производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                               "собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                               "Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по "
                               "команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, 1.2],
                [f'Поднять  насос {well_data.dict_pump_SHGN["do"]} с пакером {well_data.paker_do["do"]}',
                 None,
                 f'Поднять  насос {well_data.dict_pump_SHGN["do"]} с пакером {well_data.paker_do["do"]} с глубины '
                 f'{round(sum(list(well_data.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) на '
                 f'поверхность с '
                 f'замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем '
                 f'АСПО '
                 f'на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)],
            ]
            lift_voronka = [
                [well_jamming_str[2], None, well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][
                     0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС', None],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Сорвать планшайбу не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)',
                 None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую '
                 f'нагрузку на НКТ не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                 f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при '
                 f'необходимости  с противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на '
                 f'расхаживание - не более 6 часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО '
                 f'Региона - для составления алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить "
                               "представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и "
                               "выдачи разрешения на производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут "
                               "повлечь за собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                               "Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение "
                               "по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(
                     pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ '
                 f'В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости '
                 f'глушения и промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, None],
                [f'Поднять воронку  с Н-{round(sum(list(well_data.dict_nkt.values())), 1)}м',
                 None,
                 f'Поднять  воронку с глубины {round(sum(list(well_data.dict_nkt.values())), 1)}м'
                 f' (компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с '
                 f'доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                 f'в объеме {round(round(sum(list(well_data.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с'
                 f' контролем АСПО на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', liftingGNO(well_data.dict_nkt)],
            ]

            lift_paker = [
                [f'Опрессовать эксплуатационную колонну и пакер на Р={well_data.max_admissible_pressure._value}атм',
                 None,
                 f'Опрессовать эксплуатационную колонну и пакер на Р={well_data.max_admissible_pressure._value}атм в '
                 f'присутствии представителя ЦДНГ. '
                 f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением '
                 f'за 2 часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, Представ заказчика', 1.2],
                [f'При наличии Избыточного давления не позволяющее сорвать пакера:\n'
                 f'Произвести определение приемистости скважины', None,
                 f'При наличии Избыточного давления не позволяющее сорвать пакера:\n '
                 f'Произвести определение приемистости скважины при давлении не более '
                 f'{well_data.max_admissible_pressure._value}атм. '
                 f'{well_jamming_str_in_nkt}',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС, Представ заказчика', 1.2],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Произвести срыв пакера не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%)', None,
                 f'Разобрать устьевое оборудование. Произвести срыв пакера с поэтапным увеличением нагрузки '
                 f'на 3-4т выше веса НКТ в течении 30мин и с выдержкой '
                 f'1ч  для возврата резиновых элементов в исходное положение. Сорвать планшайбу в присутствии'
                 f' представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
                 f'НКТ не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                 f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости '
                 f'с противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
                 f'не более 6 часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
                 f'для составления алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 3.2],
                [well_jamming_str[2], None, well_jamming_str[0], None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                ['глушение', None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на"
                               " производство "
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                               "собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                               "Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде"
                               "ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(well_data.kat_pvo)[1], None,
                 pvo_gno(well_data.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и'
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, None],
                [f'Поднять  пакер {well_data.paker_do["do"]} с глубины {well_data.depth_fond_paker_do["do"]}м', None,
                 f'Поднять  пакер {well_data.paker_do["do"]} с глубины {well_data.depth_fond_paker_do["do"]}м '
                 f'{kvostovik}'
                 f'на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд.'
                 f' весом {well_data.fluid_work}  '
                 f'в объеме 1,7м3 с контролем АСПО на стенках НКТ.', None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingGNO(well_data.dict_nkt) * 1.2, 2)]
            ]
            # print(f'ключ НКТ {list(map(int, well_data.dict_nkt.keys())), well_data.dict_nkt}')
            lift_orz = [[]]
            if '89' in list(map(str, well_data.dict_nkt.keys())) and '48' in list(map(str, well_data.dict_nkt.keys())):
                lift_key = 'ОРЗ'
                lift_orz = [
                    [f'глушение скважины в НКТ48мм в объеме {round(1.3 * well_data.dict_nkt["48"] / 1000, 1)}м3, '
                     f'Произвести глушение скважины в '
                     f'НКТ89мм тех.жидкостью на поглощение в объеме '
                     f'{round(1.3 * well_data.dict_nkt["89"] * 1.1 / 1000, 1)}м3', None,
                     f'Произвести глушение скважины в НКТ48мм тех.жидкостью в объеме обеспечивающим заполнение трубного '
                     f'пространства в объеме {round(1.3 * well_data.dict_nkt["48"] / 1000, 1)}м3 жидкостью уд.веса '
                     f'{well_data.fluid_work}на давление поглощения до {well_data.max_admissible_pressure._value}атм. '
                     f'Произвести глушение скважины в '
                     f'НКТ89мм тех.жидкостью на поглощение в объеме обеспечивающим заполнение '
                     f'межтрубного и подпакерного пространства '
                     f'в объеме {round(1.3 * well_data.dict_nkt["89"] * 1.1 / 1000, 1)}м3 '
                     f'жидкостью уд.веса {well_data.fluid_work}. Тех отстой 1-2 часа. '
                     f'Произвести замер избыточного давления в скважине.',
                     None, None, None, None, None, None, None,
                     'Мастер КРС представитель Заказчика ', 0.7],
                    [None, None,
                     f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                     'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                    [f'Поднять стыковочное устройство на НКТ48мм', None,
                     f'Поднять стыковочное устройство на НКТ48мм  с гл. {well_data.dict_nkt["48"]}м с доливом тех жидкости '
                     f'уд.весом {well_data.fluid_work}',
                     None, None, None, None, None, None, None,
                     'Мастер КРС представитель Заказчика, пусков. Ком. ',
                     round((0.17 + 0.015 * well_data.dict_nkt["48"] / 8.5 + 0.12 + 1.02), 1)],
                    [f'Сорвать планшайбу и пакер', None,
                     f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                     f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
                     f'в присутствии представителя ЦДНГ, с '
                     f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
                     f'НКТ не более {round(weigth_pipe(well_data.dict_nkt) * 1.2, 1)}т. '
                     f'(вес подвески ({round(weigth_pipe(well_data.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                     f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                     f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                     f'противодавлением в НКТ '
                     f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                     f'часов, через 5 часов'
                     f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                     f'алгоритма'
                     f' последующих работ. ', None, None,
                     None, None, None, None, None,
                     'Мастер КРС представитель Заказчика', 1.5],
                    [well_jamming_str[2], None,
                     well_jamming_str[0],
                     None, None, None, None, None, None, None,
                     'Мастер КРС, представ заказчика',
                     [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                    [None, None,
                     well_jamming_str[1],
                     None, None, None, None, None, None, None,
                     ' Мастер КРС',
                     None],
                    [None, None,
                     ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if well_data.kat_pvo == 2
                              else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ "
                                   "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения "
                                   "на производство "
                                   "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь "
                                   "за собой опасность для жизни людей"
                                   " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены."
                                   " Представитель ПАСФ приглашается за 24 часа до проведения "
                                   "проверки монтажа ПВО телефонограммой. произвести практическое обучение по"
                                   " команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                                   "подъёмного агрегата для ремонта скважины."]),
                     None, None, None, None, None, None, None,
                     'Мастер КРС', None],
                    [pvo_gno(well_data.kat_pvo)[1], None,
                     pvo_gno(well_data.kat_pvo)[0], None, None,
                     None, None, None, None, None,
                     ''.join([
                         'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                         if well_data.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                     [4.21 if 'схеме №1' in str(pvo_gno(well_data.kat_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][
                         0]],
                    [None, None,
                     f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ'
                     f' ЖУРНАЛЕ).',
                     None, None,
                     None, None, None, None, None,
                     None, None],
                    [None, None,
                     f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                     f'промывки с записью удельного веса в вахтовом журнале. ',
                     None, None,
                     None, None, None, None, None,
                     None, None],
                    [None, None,
                     f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                     None, None, None, None, None,
                     None, None],
                    [f'Поднять компоновку ОРЗ с глубины {well_data.dict_nkt["89"]}м', None,
                     f'Поднять компоновку ОРЗ на НКТ89мм с глубины {well_data.dict_nkt["89"]}м на поверхность '
                     f'с замером, '
                     f'накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {well_data.fluid_work}  '
                     f'в объеме {round(well_data.dict_nkt["89"] * 1.35 / 1000, 1)}м3 с контролем АСПО на стенках НКТ.',
                     None, None,
                     None, None, None, None, None,
                     'Мастер КРС', round(liftingNKT_norm(well_data.depth_fond_paker_do['do'], 1.3), 2)],
                ]

            lift_dict = {'пакер': lift_paker, 'ОРЗ': lift_orz, 'ОРД': lift_ord, 'воронка': lift_voronka,
                         'НН с пакером': lift_pump_nn_with_paker, 'НВ с пакером': lift_pump_nv_with_paker,
                         'ЭЦН с пакером': lift_ecn_with_paker, 'ЭЦН': lift_ecn, 'НВ': lift_pump_nv, 'НН': lift_pump_nn,
                         'ЭЦН с автономными пакерами': lift_ecn_with_2paker}

            lift_select = lift_dict[lift_key]
            if lift_key in ['ЭЦН с пакером', 'ЭЦН', 'ЭЦН с автономными пакерами']:
                posle_lift.append([None, None,
                                   'В случае негерметичности фондовых НКТ при опрессовке, по согласованию '
                                   'с УСРСиСТ и ПТО региона, произвести поинтервальную опрессовку фондовых'
                                   ' НКТ либо на СПО ПСШ, либо отдельным СПО',
                                   None, None, None, None, None, None, None, None, None])
            if well_data.konte_true:
                konte_list = konte(self)
            else:
                konte_list = []

            return krs_begin + lift_select + posle_lift + konte_list
        else:
            krs_begin = [
                [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
                [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None, 'Ответственный',
                 'Нормы времени \n мин/час.'],
            ]
            return krs_begin[:2]

    @staticmethod
    def calc_work_fluid(fluid_work_insert):
        well_data.fluid = float(fluid_work_insert)
        well_data.fluid_short = fluid_work_insert

        cat_h2s_list = [well_data.dict_category[plast]['по сероводороду'
                        ].category for plast in list(well_data.dict_category.keys()) if
                        well_data.dict_category[plast]['отключение'] == 'рабочий']

        if 2 in cat_h2s_list or 1 in cat_h2s_list:
            expenditure_h2s_list = []
            if well_data.plast_work:
                try:
                    for plast in well_data.plast_work:
                        poglot = [well_data.dict_category[plast]['по сероводороду'].poglot for plast in list(well_data.dict_category.keys())
                                  if well_data.dict_category[plast]['по сероводороду'].category in [1, 2]][0]
                        expenditure_h2s_list.append(poglot)
                except ValueError:
                    pass
            else:
                expenditure_h2s, _ = QInputDialog.getDouble(
                    None,
                    'Расчет поглотителя',
                    'Отсутствуют рабочие пласты, нужно ввести необходимый расчет поглотителя',
                    0.01, 0, 10, 2)

            expenditure_h2s = round(max(expenditure_h2s_list), 3)
            fluid_work = f'{fluid_work_insert}г/см3 с добавлением поглотителя сероводорода ' \
                         f'{well_data.type_absorbent} из ' \
                         f'расчета {expenditure_h2s}л/м3 либо аналог '
            fluid_work_short = f'{fluid_work_insert}г/см3 c ' \
                               f'{well_data.type_absorbent} - {expenditure_h2s}л/м3 '
        else:
            fluid_work = f'{fluid_work_insert}г/см3 '
            fluid_work_short = f'{fluid_work_insert}г/см3'

        return fluid_work, fluid_work_short
