from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QPushButton
from datetime import datetime

import data_list

from work_py.alone_oreration import weigth_pipe, volume_pod_nkt, volume_jamming_well
from work_py.calculate_work_parametrs import volume_nkt_metal, volume_nkt, volume_well_pod_nkt_calculate
from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import lifting_nkt_norm, well_jamming_norm, liftingGNO, lifting_sucker_rod
from work_py.parent_work import TabPageUnion, TabWidgetUnion, WindowUnion


class TabPageGno(TabPageUnion):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.work_plan = self.data_well.work_plan

        self.current_bottom_label = QLabel('Забой текущий')
        self.current_bottom_edit = QLineEdit(self)

        if self.data_well.need_depth:
            self.current_bottom_edit.setText(f'{self.data_well.need_depth}')
        else:
            self.current_bottom_edit.setText(f'{self.data_well.current_bottom}')

        self.fluid_label = QLabel("уд.вес жидкости глушения", self)
        self.fluid_edit = QLineEdit(self)

        self.volume_jumping_label = QLabel("Объем глушения", self)
        self.volume_jumping_edit = QLineEdit(self)
        volume_well_jamming = self.volume()
        if abs(float(self.data_well.well_volume_in_pz[0]) - volume_well_jamming) > 0.5:
            QMessageBox.warning(None, 'Некорректный объем скважины',
                                f'Объем скважины указанный в ПЗ -{self.data_well.well_volume_in_pz}м3 '
                                f'не совпадает '
                                f'с расчетным {volume_well_jamming}м3')

            self.data_well.check_data_in_pz.append(f'Ошибка в расчете объема глушения:\nОбъем скважины указанный в ПЗ -'
                                                   f'{self.data_well.well_volume_in_pz[0]}м3 не совпадает '
                                                   f'с расчетным {volume_well_jamming}м3')
            volume_well_jamming, _ = QInputDialog.getDouble(self,
                                                            "корректный объем",
                                                            'Введите корректный объем', volume_well_jamming, 1, 80, 1)
        self.volume_jumping_edit.setText(f'{volume_well_jamming}')

        self.gno_label = QLabel("вид поднимаемого ГНО", self)
        self.gno_combo = QComboBox(self)
        gno_list = ['пакер', 'ОРЗ', 'ОРД', 'воронка', 'НН с пакером', 'НВ с пакером',
                    'ЭЦН с пакером', 'ЭЦН', 'НВ', 'НН', 'ЭЦН с автономными пакерами']
        self.gno_combo.addItems(gno_list)
        lift_key = self.select_gno(self.data_well)

        self.surfactant_hydrofabizer_label = QLabel("Необходимость гидрофабизатора ПАВ", self)
        self.surfactant_hydrofabizer_combo = QComboBox(self)
        self.surfactant_hydrofabizer_combo.addItems(['Нет', 'Да'])

        self.gno_combo.setCurrentIndex(gno_list.index(lift_key))

        # self.grid = QGridLayout(self)

        self.grid.addWidget(self.gno_label, 4, 3)
        self.grid.addWidget(self.gno_combo, 5, 3)
        self.grid.addWidget(self.current_bottom_label, 4, 4)
        self.grid.addWidget(self.current_bottom_edit, 5, 4)
        self.grid.addWidget(self.fluid_label, 4, 5)
        self.grid.addWidget(self.fluid_edit, 5, 5)
        self.grid.addWidget(self.volume_jumping_label, 4, 6)
        self.grid.addWidget(self.volume_jumping_edit, 5, 6)
        self.grid.addWidget(self.surfactant_hydrofabizer_label, 4, 7)
        self.grid.addWidget(self.surfactant_hydrofabizer_combo, 5, 7)

        for plast in self.data_well.plast_work:
            if plast in ['Сбоб-рад', 'Сбоб', 'Crr-bb', 'CI', 'CII', 'CIII', 'СIV0', 'CIV', 'CV',
                         'CVI', 'CVI0', 'D2ps',
                         'Дпаш', 'Дкын', 'C1rd-bb-tl', 'Ctl']:
                self.surfactant_hydrofabizer_combo.setCurrentIndex(1)
        self.gno_combo.currentTextChanged.connect(self.update_select_gno)

        self.fluid_edit.textChanged.connect(self.update_fluid_edit)
        self.fluid_edit.setText(f'{self.calc_fluid(self.work_plan, self.data_well.current_bottom)}')

    def update_fluid_edit(self):
        fluid = self.fluid_edit.text()
        if fluid != '':
            self.pntzh_label = QLabel('пункт налива тяжелой жидкости')
            self.pntzh_combo = QComboBox(self)
            self.pntzh_combo.addItems(['', 'КРЕЗОЛ', 'ВЕТЕРАН', 'ПНТЖ', 'Силами КРС'])
            if float(fluid) <= 1.18:
                self.pntzh_label.setParent(None)
                self.pntzh_combo.setParent(None)
            else:

                self.grid.addWidget(self.pntzh_label, 4, 8)
                self.grid.addWidget(self.pntzh_combo, 5, 8)

    def update_select_gno(self, index):
        self.current_bottom_ecn_label = QLabel('голова извлекаемых пакеров')
        self.current_bottom_ecn_edit = QLineEdit(self)

        if index == 'ЭЦН с автономными пакерами':
            self.grid.addWidget(self.current_bottom_ecn_label, 4, 10)
            self.grid.addWidget(self.current_bottom_ecn_edit, 5, 10)
        else:
            # self.grid.addWidget(self.current_bottom_ecn_label, 4, 7)
            # self.grid.addWidget(self.current_bottom_ecn_edit, 5, 7)
            self.current_bottom_ecn_edit.setParent(None)
            self.current_bottom_ecn_label.setParent(None)

    def select_gno(self, data_well):
        lift_key = ''
        if self.check_if_none(data_well.dict_pump_ecn["before"]) != 'отсут' and \
                self.check_if_none(data_well.dict_pump_shgn["before"]) != 'отсут':
            lift_key = 'ОРД'
        elif self.check_if_none(data_well.dict_pump_ecn["before"]) != 'отсут' and \
                self.check_if_none(data_well.paker_before["before"]) == 'отсут':
            lift_key = 'ЭЦН'
        elif self.check_if_none(data_well.dict_pump_ecn["before"]) != 'отсут' and \
                self.check_if_none(data_well.paker_before["before"]) != 'отсут':
            lift_key = 'ЭЦН с пакером'
        elif self.check_if_none(data_well.dict_pump_shgn["before"]) != 'отсут' and \
                data_well.dict_pump_shgn["before"].upper() != 'НН' \
                and self.check_if_none(data_well.paker_before["before"]) == 'отсут':
            lift_key = 'НВ'
        elif self.check_if_none(data_well.dict_pump_shgn["before"]) != 'отсут' and \
                self.check_if_none(data_well.dict_pump_shgn["before"]).upper() != 'НН' \
                and self.check_if_none(data_well.paker_before["before"]) != 'отсут':
            lift_key = 'НВ с пакером'
        elif 'НН' in self.check_if_none(data_well.dict_pump_shgn["before"]).upper() \
                and self.check_if_none(data_well.paker_before["before"]) == 'отсут':
            lift_key = 'НН'
        elif 'НН' in self.check_if_none(data_well.dict_pump_shgn["before"]).upper() and \
                self.check_if_none(self.check_if_none(data_well.paker_before["before"])) != 'отсут':
            lift_key = 'НН с пакером'
        elif self.check_if_none(data_well.dict_pump_shgn["before"]) == 'отсут' and \
                self.check_if_none(data_well.paker_before["before"]) == 'отсут' \
                and self.check_if_none(data_well.dict_pump_ecn["before"]) == 'отсут':
            lift_key = 'воронка'

        elif '89' in data_well.dict_nkt_before.keys() and '48' in data_well.dict_nkt_before.keys() and \
                self.check_if_none(
                    data_well.paker_before["before"]) != 'отсут':
            lift_key = 'ОРЗ'
        elif self.check_if_none(data_well.dict_pump_shgn["before"]) == 'отсут' and \
                self.check_if_none(data_well.paker_before["before"]) != 'отсут' \
                and self.check_if_none(data_well.dict_pump_ecn["before"]) == 'отсут':
            lift_key = 'пакер'
        return lift_key


    def volume(self):
        from work_py.alone_oreration import volume_jamming_well, volume_rod, volume_nkt_metal

        volume_well_jamming = round((volume_jamming_well(self, self.data_well.current_bottom) - volume_nkt_metal(
            self.data_well.dict_nkt_before) - volume_rod(self, self.data_well.dict_sucker_rod) - 0.2) * 1.1, 1)

        return volume_well_jamming

    def calc_fluid(self, work_plan, current_bottom):
        fluid_list = []
        if work_plan != 'gnkt_frez':
            self.data_well.current_bottom = current_bottom
        # Задаем начальную и конечную даты периода
        current_date = data_list.current_date.date()
        if current_date.month >= 4:
            start_date = datetime(current_date.year, 12, 1).date()
            end_date = datetime(current_date.year + 1, 3, 31).date()
        else:
            start_date = datetime(current_date.year - 1, 12, 1).date()
            end_date = datetime(current_date.year, 3, 31).date()

        # Проверяем условие: если текущая дата находится в указанном периоде
        if self.data_well.region in ['КГМ', 'АГМ']:
            fluid_p = 1.02
        else:
            fluid_p = 1.01

        for plast in self.data_well.plast_work:
            if float(list(self.data_well.dict_perforation[plast]['рабочая жидкость'])[0]) > fluid_p:
                fluid_p = list(self.data_well.dict_perforation[plast]['рабочая жидкость'])[0]
        fluid_list.append(fluid_p)
        fluid_max = None
        if max(fluid_list) <= 1.16:
            if start_date <= current_date <= end_date and max(fluid_list) <= 1.18 and \
                    self.data_well.region in ['КГМ', 'АГМ', 'ИГМ', 'ТГМ']:
                if self.data_well.region in ['КГМ']:
                    fluid_max = 1.16
                elif self.data_well.region in ['КГМ', 'АГМ', 'ИГМ', 'ТГМ']:
                    fluid_max = 1.18
            else:
                fluid_max = max(fluid_list)
        else:
            fluid_max = max(fluid_list)
        try:

            if fluid_max not in self.data_well.well_fluid_in_pz:
                self.data_well.check_data_in_pz.append(f'Не корректный удельный вес в ПЗ, по расчету '
                                                       f'необходимо {fluid_max}г/см3')
                QMessageBox.warning(self, 'Удельный вес', f'Расчетный удельный вес {fluid_max}г/см3 не соответствует '
                                                          f'указанному в ПЗ {self.data_well.well_fluid_in_pz}')
            if work_plan == 'gnkt_frez' or work_plan == 'gnkt_opz':
                fluid_max = 1.18
        except Exception as e:
            print(f'Ошибка {e}')

        return fluid_max


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageGno(parent), 'Подъем ГНО')


class GnoWindow(WindowUnion):
    def __init__(self, insert_index, table_widget, parent=None):
        super(GnoWindow, self).__init__(parent)
        self.lift_key = None
        self.current_widget = None
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.insert_index = insert_index
        self.data_well.insert_index2 = insert_index
        self.table_widget = table_widget
        self.work_plan = parent.work_plan
        self.tab_widget = TabWidget(self.data_well)

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from work_py.advanted_file import definition_plast_work

        self.current_widget = self.tab_widget.currentWidget()
        try:
            self.lift_key = self.current_widget.gno_combo.currentText()

            self.fluid = self.current_widget.fluid_edit.text().replace(',', '.')
            if 0.85 > float(self.fluid) > 1.64:
                QMessageBox.warning(self, 'Ошибка',
                                    'удельный вес рабочей жидкости не может быть меньше 0.85 и больше 1.64')
                return

            current_bottom = round(float(self.current_widget.current_bottom_edit.text().replace(',', '.')),
                                   1)
            self.data_well.fluid_work, self.data_well.fluid_work_short = \
                self.calc_work_fluid(self.fluid)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

            return
        self.data_well.current_bottom = current_bottom
        definition_plast_work(self)
        lift_strategy = None
        if self.lift_key == 'пакер':
            lift_strategy = LiftPaker(self)
        elif self.lift_key == 'ОРЗ':
            lift_strategy = LiftOrz(self)
        elif self.lift_key == 'ОРД':
            lift_strategy = LiftOrd(self)
        elif self.lift_key == 'воронка':
            lift_strategy = LiftVoronka(self)
        elif self.lift_key == 'НН с пакером':
            lift_strategy = LiftPumpNnWithPaker(self)
        elif self.lift_key == 'НВ с пакером':
            lift_strategy = LiftPumpNvWithPaker(self)
        elif self.lift_key == 'ЭЦН с пакером':
            lift_strategy = LiftEcnWithPaker(self)
        elif self.lift_key == 'ЭЦН':
            lift_strategy = LiftEcn(self)
        elif self.lift_key == 'НВ':
            lift_strategy = LiftPumpNv(self)
        elif self.lift_key == 'НН':
            lift_strategy = LiftPumpNn(self)
        elif self.lift_key == 'ЭЦН с автономными пакерами':
            lift_strategy = LiftEcnWith2Paker(self)

        if lift_strategy:
            work_list = lift_strategy.add_work_lift()

            if self.lift_key == 'ЭЦН с автономными пакерами':
                current_bottom_ecn_edit = self.current_widget.current_bottom_ecn_edit.text()
                if current_bottom_ecn_edit != '':
                    current_bottom_ecn_edit = round(float(self.current_widget.current_bottom_ecn_edit.text()), 1)
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Не введена глубина после стыковочного седла')
                    return
                self.data_well.current_bottom = current_bottom_ecn_edit
            check_question = QMessageBox.question(self, 'Корректность забой', f'Забой который можно нормализовать '
                                                                              f'без использования ВЗД на '
                                                                              f'глубине {current_bottom}м, корректен?')

            if check_question == QMessageBox.StandardButton.No:
                return
            if work_list:
                if self.data_well.work_plan not in ['krs', 'prs']:
                    work_list = work_list[2:]

                self.populate_row(self.insert_index, work_list, self.table_widget)

                data_list.pause = False
                self.close()
                self.close_modal_forcefully()


class GnoParent(ABC):
    def __init__(self, parent=None):

        self.data_well = parent.data_well
        self.fluid = parent.fluid

        self.calculate_chemistry = parent.calculate_chemistry
        self.current_widget = parent.tab_widget.currentWidget()
        if float(self.fluid) > 1.18:
            self.pntzh_combo = self.current_widget.pntzh_combo.currentText()

        self.lift_key = parent.lift_key
        self.pvo_gno = parent.pvo_gno
        self.length_nkt = sum(list(self.data_well.dict_nkt_before.values()))
        try:
            self.surfactant_hydrofabizer_combo = self.current_widget.surfactant_hydrofabizer_combo.currentText()
            self.current_bottom = round(float(self.current_widget.current_bottom_edit.text().replace(',', '.')), 1)
            self.volume_well_jamming = round(float(self.current_widget.volume_jumping_edit.text().replace(',', '.')), 1)
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Не корректное сохранение параметра: {type(e).__name__}\n\n{str(e)}')

        from work_py.descent_gno import TabPageGno
        self.nkt_diam_fond = TabPageGno.gno_nkt_opening(self.data_well.dict_nkt_before)

        self.without_damping_true = self.data_well.without_damping
        if self.without_damping_true and self.data_well.category_pressure in [1, '1', 2, '2']:
            question = QMessageBox.question(None, 'Нестыковка',
                                            f'Скважина состоит в перечне скважин не подлежащих '
                                            f'глушению, но так же скважина {self.data_well.category_pressure} '
                                            f'по давлению, есть ли необходимость ее глушить?')
            # question = QMessageBox.question(self, 'Корректность забой', f'Забой который можно нормализовать '
            #                                                  f'без использования ВЗД на '
            #                                                  f'глубине м, корректен?')
            if question == QMessageBox.StandardButton.Yes:
                self.without_damping_true = False

        self.well_jamming_str = self.well_jamming()

        self.well_jamming_ord = volume_jamming_well(self, float(self.data_well.depth_fond_paker_before["before"]))
        self.sucker_pod_jamming = "".join([
            " " if self.without_damping_true is True else f"Приподнять штангу. Произвести глушение в "
                                                          f"трубное пространство в объеме{self.well_jamming_ord}м3 "
                                                          f"(объем колонны от пакера до устья уд.весом"
                                                          f" {self.data_well.fluid_work}. Техостой 2ч."])

        if self.data_well.work_plan == 'krs' or self.data_well.curator == 'ВНС':
            if any([str(cater) == '1' for cater in self.data_well.category_pressure_list]):
                self.data_well.category_pvo = 1
                self.data_well.category_pvo, _ = QInputDialog.getInt(
                    None, 'Категория скважины', f'Категория скважины № {self.data_well.category_pvo}, корректно?',
                    self.data_well.category_pvo, 1, 2)
        self.text_pvo = f'{self.data_well.max_admissible_pressure.get_value}атм не ниже ' \
                        f'максимально ожидаемого давления с ' \
                        f'выдержкой в течении 30 минут, но не менее 30атм  '
        if self.data_well.curator == 'ВНС':
            self.text_pvo = f'{self.data_well.max_admissible_pressure.get_value * 1.1:.1f}атм  на ' \
                        f'максимально не ниже ожидаемого давления с выдержкой в течении 30 минут ' \
                            f'(+10% на скважинах освоения), но не менее 30атм '

    def lifting_unit(self):
        aprs_40 = 'Установить подъёмный агрегат на устье не менее 40т.\n' \
                  'ПРИМЕЧАНИЕ:  ПРИ ИСПОЛЬЗОВАНИИ ПОДЪЕМНОГО АГРЕТАТА АПРС-40, А5-40, АПРС-50 ДОПУСКАЕТСЯ РАБОТА ' \
                  'БЕЗ ПРИМЕНЕНИЯ ВЕТРОВЫХ ОТТЯЖЕК при скорости ветра не более 14 м/с и плотности грунта не менее 5 ' \
                  'кг см2.ПРИ ИСПОЛЬЗОВАНИИ подъемного АГРЕГАТА  УПА-60/80, А-50 РАБОТАТЬ ТОЛЬКО С ПРИМЕНЕНИЕМ 4 ' \
                  'ОТТЯЖЕК. При использовании подъемного агрегата АПР 60/80, Барс-80 допускается работа без применения ' \
                  'ветровых оттяжек до 50 тн. при скорости ветра менее 14 м/с и плотности грунта не менее 5 кг см2. ' \
                  'При выполнении работ по ликвидации  аварии обязательно оснащение всех видов ПОДЪЕМНЫХ АГРЕГАТОВ 4 ' \
                  'ОТТЯЖКАМИ. При превышении 75% от страгивающей нагрузки на все подъемные агрегаты оформляется ' \
                  'наряд допуск на проведение работ повышенной опасности. МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ ' \
                  '80% ОТ СТРАГИВАЮЩЕЙ НАГРУЗКИ НА НКТ. После монтажа подъёмника якоря ветровых оттяжек должны ' \
                  'быть испытаны на нагрузки, установленные инструкцией по эксплуатации завода - изготовителя в ' \
                  'присутствии супервайзера Заказчика. '

        upa_60 = 'Установить подъёмный агрегат на устье не менее 60т.  \n' \
                 'ПРИМЕЧАНИЕ:  ПРИ ИСПОЛЬЗОВАНИИ ПОДЪЕМНОГО АГРЕТАТА АПРС-40, А5-40, АПРС-50 ДОПУСКАЕТСЯ РАБОТА ' \
                 'БЕЗ ПРИМЕНЕНИЯ ВЕТРОВЫХ ОТТЯЖЕК при скорости ветра не более 14 м/с и плотности грунта не менее 5 ' \
                 'кг см2.ПРИ ИСПОЛЬЗОВАНИИ подъемного АГРЕГАТА  УПА-60/80, А-50 РАБОТАТЬ ТОЛЬКО С ПРИМЕНЕНИЕМ 4 ' \
                 'ОТТЯЖЕК. При использовании подъемного агрегата АПР 60/80, Барс-80 допускается работа без применения ' \
                 'ветровых оттяжек до 50 тн. при скорости ветра менее 14 м/с и плотности грунта не менее 5 кг см2. ' \
                 'При выполнении работ по ликвидации  аварии обязательно оснащение всех видов ПОДЪЕМНЫХ АГРЕГАТОВ 4 ' \
                 'ОТТЯЖКАМИ. При превышении 75% от страгивающей нагрузки на все подъемные агрегаты оформляется ' \
                 'наряд допуск на проведение работ повышенной опасности. МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ ' \
                 '80% ОТ СТРАГИВАЮЩЕЙ НАГРУЗКИ НА НКТ. После монтажа подъёмника якоря ветровых оттяжек должны ' \
                 'быть испытаны на нагрузки, установленные инструкцией по эксплуатации завода - изготовителя в ' \
                 'присутствии супервайзера Заказчика. '

        return upa_60 if self.data_well.bottom_hole_artificial.get_value >= 2300 else aprs_40

    def append_posle_lift(self):
        text = ""
        if self.data_well.region == 'КГМ':
            text = "\nПРИ НЕГЕРМЕТИЧНОСТИ НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ. \n"
        posle_lift = [
            [None, None,
             f'По результатам подъема провести ревизию НКТ в присутствии представителя ЦДНГ. {text} В случае '
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
             f'{self.text_pvo},в случае невозможности '
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
        return posle_lift

    @abstractmethod
    def add_work_lift(self):
        raise NotImplementedError('Не выбран метод реализации, метож должен быть переопределен')

    def begin_work(self):

        type_of_chemistry = 'СГС-18'
        surfactant_hydrofabizer_str = ''
        volume_chemistry = None
        if self.surfactant_hydrofabizer_combo == 'Да':
            self.calculate_chemistry('гидрофабизатор', round(self.volume_well_jamming * 0.05, 2))
            surfactant_hydrofabizer_str = 'с добавлением в жидкость глушения гидрофобизатора из расчёта' \
                                          ' 0,05% на 1м3 (0,5л)'
        if 1.2 < float(self.fluid) < 1.62:
            type_of_chemistry = 'СГС-18'
            water_fresh = data_list.DICT_SGS[float(self.fluid)][0]
            volume_chemistry = data_list.DICT_SGS[float(self.fluid)][1]
        elif 1.19 < float(self.fluid) < 1.34:
            type_of_chemistry = 'CaCl'
            water_fresh = data_list.DICT_CALC_CACL[float(self.fluid)][0]
            volume_chemistry = data_list.DICT_CALC_CACL[float(self.fluid)][1]
        elif 1.34 <= float(self.fluid) < 1.6:
            type_of_chemistry = 'CaЖГ'
            water_fresh = data_list.DICT_CALC_CAZHG[float(self.fluid)][0]
            volume_chemistry = data_list.DICT_CALC_CAZHG[float(self.fluid)][1]

        krs_begin = [
            [None, 'Порядок работы', None, None, None, None, None, None, None, None, None, None, None,
             None, None, None],
            [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None,
             'Ответственный',
             'Нормы времени \n мин/час.'],
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
             f'ознакомлена с возможными осложнениями и авариямив процессе работ, планом локализации и ликвидации '
             f'аварии (ПЛА) и планом работ. При выполнении работ, связанных с применением новых технических'
             f' устройств и технологий персоналу бригад должен быть проведен внеплановый инструктаж, с'
             f' соответствующим оформлением в журнале инструктажей на рабочем месте ',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, 4,
             f'При подъеме труб из скважины производить долив тех. жидкостью Y- {self.data_well.fluid_work}. '
             f'Долив скважины '
             f'должен быть равен объему извлекаемого металла.'
             f'По мере расхода жидкости из ёмкости, производить своевременное её заполнение. При всех '
             f'технологических '
             f'спусках НКТ 73мм х 5,5мм и 60мм х 5мм производить '
             f'контрольный замер и отбраковку + шаблонирование шаблоном {self.data_well.nkt_template}мм '
             f'd=59,6мм и 47,'
             f'9мм '
             f'соответственно.',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', None],
            [None, None,
             f'ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ ПРОИЗВОДИТЬ НА ТЕХ ЖИДКОСТИ УД. ВЕСОМ РАВНОЙ'
             f' {self.data_well.fluid_work} '
             f'{surfactant_hydrofabizer_str}', None,
             None, None, None, None, None, None, None,
             None],
            [None, None, f'Замерить Ризб. При наличии избыточного давления произвести замер Ризб и уд.вес '
                         f'жидкости излива, по результату замеру произвести перерасчет и корректировку удельного '
                         f'веса тех.жидкости',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', 0.5],
            [None, None,
             f'Согласно инструкции ООО Башнефть-Добыча ПЗ-05 И-102089 ЮЛ-305 версия 3 п. 8.1.9 при отсутствии '
             f'избыточного давления и '
             f'наличии риска поглощения жидкости глушения. произвести замер статического уровня силами ЦДНГ перед '
             f'началом работ и в '
             f'процессе ремонта (с периодичностью определяемой ответственным руководителем работ, по согласованию с'
             f' представителем Заказчика '
             f'Результаты замеров статического уровня фиксировать в вахтовом журнале и передавать в сводке '
             f'При изменении '
             f'уровня в скважине от первоначально замеренного на 100м и более метров в сторону уменьшения или '
             f'возрастания, '
             f'необходимо скорректировать объем долива и добиться стабилизации уровня в скважине. Если по данным '
             f'замера уровень в '
             f'скважине растет, необходимо выполнить повторное глушение скважины, сделав перерасчет плотности '
             f'жидкости глушения в '
             f'соответствии с уточненными геологической службой данными по пластовому давлению.',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', 1.5]
        ]
        if float(self.fluid) > 1.18:
            if self.pntzh_combo == '':
                QMessageBox.warning(None, 'Ошибка', 'Не выбрано пункт налива')
                return

            if self.pntzh_combo == 'Силами КРС':
                krs_begin.insert(-2,
                                 [None, None,
                                  f'Для приготовления жидкости в объеме 10м3 уд.весом {self.fluid}г/см3 необходимо завезти:\n'
                                  f'{type_of_chemistry} весом {10 * volume_chemistry / 1000:.1f}т (из расчета '
                                  f'{10 * volume_chemistry:.1f}кг/м3 на {water_fresh:.1f}л  пресной воды) на основе '
                                  f'тех жидкости '
                                  f'уд. весом 1,01г/см3 в объеме {water_fresh * 10:.1f}м3 доставленной автоцистернами '
                                  f'из ПНТЖ заказчика уд. весом 1,01г/см3 '
                                  f'Заявку на завоз тех жидкости подать за 24 часа до начала работ через '
                                  f'ведущего инженера РИТС {data_list.contractor}',
                                  None, None, None, None, None, None, None,
                                  ' Мастер КРС.', 10]
                                 )
        if self.data_well.bvo:
            for row in mkp_revision_1_kateg(self):
                krs_begin.insert(-3, row)

        update_change_fluid_str = [
            [None, None,
             f'При отсутствии избыточного давления произвести замер статического уровня в присутствии представителя'
             f' заказчика. Составить акт. По результатам замера статического уровня согласовать с заказчиком '
             f'глушение скважины уд. весом 1,17{self.data_well.fluid_work[4:]} в алгоритме указанном ниже. '
             f'При положительном результате глушения дальнейшие работ продолжить с учетом изменения уд.веса '
             f'рабочей жидкости.',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', None]]

        if float(self.fluid) + 0.02 > 1.18:
            krs_begin.insert(-1, update_change_fluid_str[0])

        kvostovika_length = round(
            self.length_nkt - float(
                self.data_well.depth_fond_paker_before["before"]), 1)

        self.kvostovik = f' + хвостовиком {kvostovika_length}м ' if self.data_well.region == 'ТГМ' and \
                                                                    kvostovika_length > 0.001 else ''

        # экземпляр функции расчета глушения
        well_jamming_ord = volume_jamming_well(self, float(self.data_well.depth_fond_paker_before["before"]))
        self.sucker_pod_jamming = "".join([
            " " if self.without_damping_true is True else f"Приподнять штангу. Произвести глушение в "
                                                          f"трубное пространство в объеме{well_jamming_ord}м3 "
                                                          f"(объем колонны от пакера до устья уд.весом"
                                                          f" {self.data_well.fluid_work}. Техостой 2ч."])

        work_hard_fluid_list = self.calculate_hard_fluid()
        if work_hard_fluid_list:
            krs_begin.extend(work_hard_fluid_list)
        return krs_begin

    def well_jamming(self):
        from work_py.calculate_work_parametrs import volume_work, volume_well_pod_nkt_calculate, volume_nkt, \
            volume_rod, volume_jamming_well

        well_jamming_list2 = f'Вести контроль плотности на  выходе в конце глушения. В случае ' \
                             f'отсутствия на последнем кубе глушения  жидкости ' \
                             f'уд.веса равной удельному весу ЖГ, дальнейшие промывки и удельный ' \
                             f'вес жидкостей промывок согласовать с Заказчиком,' \
                             f' при наличии Ризб - произвести замер, перерасчет ЖГ и повторное ' \
                             f'глушение с корректировкой удельного веса жидкости' \
                             f' глушения. В СЛУЧАЕ ОТСУТСТВИЯ ЦИРКУЛЯЦИИ ПРИ ГЛУШЕНИИ СКВАЖИНЫ,' \
                             f' А ТАКЖЕ ПРИ ГАЗОВОМ ФАКТОРЕ БОЛЕЕ 200м3/сут ' \
                             f'ПРОИЗВЕСТИ ЗАМЕР СТАТИЧЕСКОГО УРОВНЯ В ТЕЧЕНИИ ЧАСА С ОТБИВКОЙ ' \
                             f'УРОВНЯ В СКВАЖИНЕ С ИНТЕРВАЛОМ 15 МИНУТ.' \
                             f'ПО РЕЗУЛЬТАТАМ ЗАМЕРОВ ПРИНИМАЕТСЯ РЕШЕНИЕ ОБ ПРОДОЛЖЕНИИ ОТБИВКИ ' \
                             f'УРОВНЯ В СКВАЖИНЕ ДО КРИТИЧЕСКОЙ ГЛУБИНЫ ЗА ' \
                             f'ПРОМЕЖУТОК ВРЕМЕНИ.'

        well_volume = volume_jamming_well(self.data_well)
        volume_pod_nkt_str = volume_well_pod_nkt_calculate(self.data_well)
        volume_nkt_str = volume_nkt(self.data_well)
        volume_nkt_metal_str = volume_nkt_metal(self.data_well)
        volume_rod_str = volume_rod(self.data_well)
        volume_nkt_ustie = round(self.volume_well_jamming - volume_pod_nkt_str, 1)
        well_volume_str_after = f'{round(self.volume_well_jamming - well_volume, 1)}м3.' if round(
            self.volume_well_jamming - well_volume, 1) > 0.1 else ''
        h2s_string_volume = ''
        if self.data_well.plast_work:
            poglot_h2s = [self.data_well.dict_category[plast]['по сероводороду'].poglot
                          for plast in self.data_well.dict_category
                          if self.data_well.dict_category[plast]['отключение'] == 'рабочий' and
                          self.data_well.dict_category[plast]['по сероводороду'].category != 3]
            if poglot_h2s:
                poglot_h2s = max(poglot_h2s)
                volume_h2s = round(well_volume * poglot_h2s, 1)
                h2s_string_volume = f'Необходимое кол-во поглотителя сероводорода на объем глушение - {volume_h2s}л'

        if self.without_damping_true:
            well_jamming_str = f'Скважина состоит в перечне скважин ООО Башнефть-Добыча, на которых допускается ' \
                               f'проведение ТКРС без предварительного глушения на текущий квартал'
            well_jamming_short = f'Скважина без предварительного глушения'
            well_jamming_list2 = f'В случае наличия избыточного давления необходимость повторного глушения скважины ' \
                                 f'дополнительно согласовать со специалистами ПТО  и ЦДНГ.'
        elif abs(self.length_nkt - self.data_well.perforation_roof) <= 150:
            well_jamming_str = f'Произвести глушение скважины в объеме {self.volume_well_jamming}м3 тех ' \
                               f'жидкостью уд.весом {self.data_well.fluid_work}' \
                               f' на циркуляцию. Закрыть скважину на ' \
                               f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, ' \
                               f'в случае отсутствия ' \
                               f'на желобную емкость). '
            well_jamming_short = (f'Глушение в НКТ в объеме {self.volume_well_jamming}м3 уд.весом '
                                  f'{self.data_well.fluid_work_short}')
        elif abs(self.length_nkt - self.data_well.perforation_roof) > 150:
            well_jamming_str = f'Произвести глушение скважины объеме {self.volume_well_jamming}м3 тех ' \
                               f'жидкостью уд.весом {self.data_well.fluid_work}' \
                               f' на циркуляцию в следующим алгоритме: \n Произвести закачку ' \
                               f'в трубное пространство ' \
                               f'тех жидкости в ' \
                               f'объеме {volume_nkt_ustie}м3 на ' \
                               f'циркуляцию. Закрыть трубное пространство. ' \
                               f'Произвести закачку на поглощение не более ' \
                               f'{self.data_well.max_admissible_pressure.get_value}атм ' \
                               f'тех жидкости в ' \
                               f'объеме {round((volume_pod_nkt_str + volume_nkt_str) * 1.1, 1)}м3. ' \
                               f'Закрыть скважину на ' \
                               f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае ' \
                               f'отсутствия на желобную емкость. '
            well_jamming_short = f'Глушение в НКТ в объеме {self.volume_well_jamming}м3 тех ' \
                                 f'жидкостью уд.весом {self.data_well.fluid_work_short}'

        elif self.without_damping_true is False and self.lift_key in ['НН с пакером', 'НВ с пакером', 'ЭЦН с пакером',
                                                                      'ОРЗ']:

            well_jamming_str = f'Произвести закачку в трубное пространство тех жидкости уд.весом ' \
                               f'{self.data_well.fluid_work} в ' \
                               f'объеме {round(self.volume_well_jamming - volume_pod_nkt_str, 1)}м3 на циркуляцию. ' \
                               f'Закрыть трубное пространство.  Закрыть скважину на стабилизацию не менее 2 часов. ' \
                               f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость). '

            well_jamming_short = f'Глушение в НКТ уд.весом {self.data_well.fluid_work_short} ' \
                                 f'объеме {volume_nkt_str}м3 ' \
                                 f'на циркуляцию.  '

        elif self.without_damping_true is False and self.lift_key in ['ОРД', 'ЭЦН']:
            well_jamming_str = f'Произвести закачку в трубное пространство тех жидкости уд.весом ' \
                               f'{self.data_well.fluid_work_short} в ' \
                               f'объеме {round(volume_nkt_ustie, 1)}м3 ' \
                               f'на поглощение при давлении не более ' \
                               f'{self.data_well.max_admissible_pressure.get_value}атм. Закрыть ' \
                               f'затрубное пространство. Закрыть скважину на стабилизацию не менее 2 часов. ' \
                               f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость). '
            well_jamming_short = f'Глушение в НКТ уд.весом {self.data_well.fluid_work_short} в ' \
                                 f'объеме ' \
                                 f'{round(volume_nkt_ustie, 1)}м3 '
        elif self.without_damping_true is False and self.lift_key in ['НН', 'НВ']:
            well_jamming_str = f'Произвести глушение скважины в объеме {self.volume_well_jamming}м3 тех ' \
                               f'жидкостью уд.весом {self.data_well.fluid_work}' \
                               f' на циркуляцию в следующим алгоритме: \n Произвести закачку в' \
                               f' затрубное пространство тех жидкости в объеме {volume_nkt_ustie}м3 на ' \
                               f'циркуляцию. Закрыть трубное пространство. ' \
                               f'Произвести закачку на поглощение не более ' \
                               f'{self.data_well.max_admissible_pressure.get_value}атм ' \
                               f'тех жидкости в ' \
                               f'объеме {volume_pod_nkt_str:.1f}м3. ' \
                               f'Закрыть скважину на ' \
                               f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае ' \
                               f'отсутствия на желобную емкость. '
            well_jamming_short = f'Глушение в затруб в объеме {self.volume_well_jamming}м3 тех ' \
                                 f'жидкостью уд.весом {self.data_well.fluid_work_short}'

        if len(self.data_well.plast_work) == 0 and len(self.data_well.dict_leakiness) == 0:
            well_jamming_str = f'Опрессовать эксплуатационную колонну в интервале 0-' \
                               f'{self.data_well.current_bottom}м на ' \
                               f'Р={self.data_well.max_admissible_pressure.get_value}атм' \
                               f' в течение 30 минут в присутствии представителя заказчика, составить акт. ' \
                               f'(Вызов представителя осуществлять телефонограммой за 12 часов, ' \
                               f'с подтверждением за 2 часа ' \
                               f'до начала работ). '

            well_jamming_list2 = 'При негерметичности согласовать ' \
                                 'глушение скважины по дополнительному плану работ'

            well_jamming_short = 'Рабочие интервалы отсутствуют, При необходимости необходимо согласовать ' \
                                 'глушение скважины по дополнительному плану работ'
        if 'в перечне скважин' not in well_jamming_str:
            well_jamming_str += h2s_string_volume

        return [well_jamming_str + f'\nОпределить приемистость пласта при Р={self.data_well.max_admissible_pressure.get_value}атм', well_jamming_list2,
                well_jamming_short + f'\nОпределить приемистость пласта при Р={self.data_well.max_admissible_pressure.get_value}атм']

    def calculate_hard_fluid(self):
        current_date = data_list.current_date.date()
        if current_date.month > 4:
            start_date = datetime(current_date.year, 12, 1).date()
            end_date = datetime(current_date.year + 1, 4, 1).date()
        else:
            start_date = datetime(current_date.year - 1, 12, 1).date()
            end_date = datetime(current_date.year, 4, 1).date()
        work_list = []
        if start_date <= current_date <= end_date and float(self.fluid) <= 1.18:
            volume_hard_fluid = self.volume_well_jamming * float(self.fluid) / 1.18

            work_list = [
                [None, None,
                 f'Согласно методических указаний  по определению ЖГ в зимнее время '
                 f'№ П2-05.01 М-0037 ЮЛ-305 версия 1, утвержденного приказом от 22 февраля 2024г, в связи с рисками '
                 f'с замерзанием пресной жидкости при проведении глушения скважин '
                 f'жидкостью с расчетными параметрами  плотности жидкости склонной к замерзанию и необходимостью '
                 f'исключения прекращения , промывки и долива связанными допускается применение жидкости повышенной '
                 f'плотности не позволяющей проведения работ без ее замерзания с ближайшего пункта '
                 f'набора 1.16-1,18г/см3. ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 f'Если расчетная плотность меньше плотности жидкости, находящейся на ближайшем пункте набора, при '
                 f'таких условиях применять в работе жидкость той плотности которая есть в наличии на ближайшем '
                 f'пункте набора. Объем закачки определяется исходя из требуемого гидростатического давления '
                 f'(при соблюдении условий предотвращения возможного ГНВП) и определяется по формуле 6.2 мероприятий: \n'
                 f'Vжг = ((Рпл*(1+П)*106 / ρ (пнсв)*9,81 ) + L) * V1м.эк - Vнкт мет -Vшт \n'
                 f'и составляет {volume_hard_fluid:.1f}м3 при использовании жидкости на ближайшем пункте набора'
                 f' удельным весом 1,18г/см3',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', None],
                [None, None,
                 f'Если по результату прослеживания за изменением уровня жидкости в процессе проведения глушения и '
                 f'при ПО обнаруживается падение уровня на 100 и более метров, тогда при ведении ремонтных работ и '
                 f'при проведении промывки скважины, необходимо работы вести с установкой БСГ на перфорированный '
                 f'интервал скважины от забоя до уровня 50-150 метров над верхними отверстиями перфорации с продавкой '
                 f'на давление поглощения но не выше максимально допустимого давления на эксплуатационную колонну '
                 f'по дополнительному плану работ',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', None],
            ]
        return work_list


class LiftPaker(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.well_jamming_str_in_nkt = " " if self.without_damping_true is True \
            else f'По результату приемистости произвести глушение скважины в НКТ тех.жидкостью в объеме ' \
                 f'обеспечивающим ' \
                 f'заполнение трубного пространства и скважины в подпакерной зоне в объеме ' \
                 f'{volume_well_pod_nkt_calculate(self.data_well) + volume_nkt(self.data_well):.1f} м3 ' \
                 f'жидкостью уд.веса {self.data_well.fluid_work} при давлении не более ' \
                 f'{self.data_well.max_admissible_pressure.get_value}атм. ' \
                 f'Тех отстой 1-2 часа. Произвести замер избыточного давления в скважине.'

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_paker())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_paker(self):
        kvostovika_length = round(self.length_nkt - float(self.data_well.depth_fond_paker_before["before"]), 1)

        kvostovik = f' + хвостовиком {kvostovika_length}м ' if self.data_well.region == 'ТГМ' and \
                                                               kvostovika_length > 0.001 else ''

        lift_paker = [
            [f'Опрессовать эксплуатационную колонну и пакер на Р='
             f'{self.data_well.max_admissible_pressure.get_value}атм',
             None,
             f'Опрессовать эксплуатационную колонну и пакер на Р='
             f'{self.data_well.max_admissible_pressure.get_value}атм в '
             f'присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением '
             f'за 2 часа до начала работ)', None, None, None, None, None, None, None,
             'Мастер КРС, Представ заказчика', 1.2],
            [f'При наличии Избыточного давления не позволяющее сорвать пакера:\n'
             f'Произвести определение приемистости скважины', None,
             f'При наличии Избыточного давления не позволяющее сорвать пакера:\n '
             f'Произвести определение приемистости скважины при давлении не более '
             f'{self.text_pvo}'
             f'{self.well_jamming_str_in_nkt}',
             None, None, None, None, None, None, None,
             'Мастер КРС, Представ заказчика', 1.2],
            [None, None, f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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

            [f'Произвести срыв пакера не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Произвести срыв пакера с поэтапным увеличением нагрузки '
             f'на 3-4т выше веса НКТ в течении 30мин и с выдержкой '
             f'1ч  для возврата резиновых элементов в исходное положение. Сорвать планшайбу в присутствии'
             f' представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
             f'НКТ не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
             f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости '
             f'с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
             f'не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
             f'для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 3.2],
            [self.well_jamming_str[2], None, self.well_jamming_str[0], None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            ['глушение', None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                 if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять  пакер {self.data_well.paker_before["before"]} с глубины '
             f'{self.data_well.depth_fond_paker_before["before"]}м',
             None,
             f'Поднять  пакер {self.data_well.paker_before["before"]} с глубины '
             f'{self.data_well.depth_fond_paker_before["before"]}м '
             f'{kvostovik}'
             f'на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд.'
             f' весом {self.data_well.fluid_work}  '
             f'в объеме 1,7м3 с контролем АСПО на стенках НКТ.', None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)]
        ]

        return lift_paker


class LiftOrz(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_orz())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_orz(self):
        lift_orz = [[]]
        if '89' in list(map(str, self.data_well.dict_nkt_before.keys())) and '48' in list(
                map(str, self.data_well.dict_nkt_before.keys())):

            lift_orz = [
                [f'глушение скважины в НКТ48мм в объеме '
                 f'{round(1.3 * self.data_well.dict_nkt_before["48"] / 1000, 1)}м3, '
                 f'Произвести глушение скважины в '
                 f'НКТ89мм тех.жидкостью на поглощение в объеме '
                 f'{round(1.3 * self.data_well.dict_nkt_before["89"] * 1.1 / 1000, 1)}м3', None,
                 f'Произвести глушение скважины в НКТ48мм тех.жидкостью в объеме обеспечивающим заполнение трубного '
                 f'пространства в объеме {round(1.3 * self.data_well.dict_nkt_before["48"] / 1000, 1)}м3 '
                 f'жидкостью уд.веса '
                 f'{self.data_well.fluid_work}на давление поглощения до'
                 f' {self.text_pvo}'
                 f'Произвести глушение скважины в '
                 f'НКТ89мм тех.жидкостью на поглощение в объеме обеспечивающим заполнение '
                 f'межтрубного и подпакерного пространства '
                 f'в объеме {round(1.3 * self.data_well.dict_nkt_before["89"] * 1.1 / 1000, 1)}м3 '
                 f'жидкостью уд.веса {self.data_well.fluid_work}. Тех отстой 1-2 часа. '
                 f'Произвести замер избыточного давления в скважине.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [None, None,
                 f'{self.lifting_unit()}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
                [f'Поднять стыковочное устройство на НКТ48мм', None,
                 f'Поднять стыковочное устройство на НКТ48мм  с гл. {self.data_well.dict_nkt_before["48"]}м'
                 f' с доливом тех жидкости '
                 f'уд.весом {self.data_well.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 round((0.17 + 0.015 * self.data_well.dict_nkt_before["48"] / 8.5 + 0.12 + 1.02), 1)],
                [f'Сорвать планшайбу и пакер', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                 f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
                 f'в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
                 f'НКТ не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                 f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                 f'часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                 f'алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [self.well_jamming_str[2], None,
                 self.well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
                [None, None,
                 self.well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС',
                 None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
                [self.pvo_gno(self.data_well.category_pvo)[1], None,
                 self.pvo_gno(self.data_well.category_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(
                     self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][
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
                [f'Поднять компоновку ОРЗ с глубины {self.data_well.dict_nkt_before["89"]}м', None,
                 f'Поднять компоновку ОРЗ на НКТ89мм с глубины {self.data_well.dict_nkt_before["89"]}м на поверхность '
                 f'с замером, '
                 f'накручиванием колпачков с доливом скважины тех.жидкостью уд. весом '
                 f'{self.data_well.fluid_work}  '
                 f'в объеме {round(self.data_well.dict_nkt_before["89"] * 1.35 / 1000, 1)}м3 '
                 f'с контролем АСПО на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(lifting_nkt_norm(self.data_well.depth_fond_paker_before["before"], 1.3), 2)],
            ]
            if self.without_damping_true:
                lift_orz = lift_orz[1:]
        return lift_orz


class LiftOrd(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        work_list.extend(self.lifting_ord())
        work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_ord(self):
        lift_ord = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ '
                ,
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.67],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'подьем {self.data_well.dict_pump_shgn["before"]}', None,
             f'Сорвать насос штанговый насос {self.data_well.dict_pump_shgn["before"]}(зафиксировать вес при срыве).'
             f' Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.text_pvo} '
             f'{self.sucker_pod_jamming}'
             f'Поднять на штангах насос с гл. {self.data_well.dict_pump_shgn_depth["before"]}м с доливом тех жидкости '
             f'уд.весом {self.data_well.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве '
             f'насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО '
             f'региона  постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный отворот НШ с '
             f'последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с '
             f'подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(self.data_well.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер  не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
             f'выдержкой 30мин для возврата резиновых элементов в исходное положение '
             f'в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
             f'более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). '
             f'ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т (страг нагрузка НКТ по паспорту),  при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 + АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
             f'часов, через 5 часов '
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона -  для составления '
             f'алгоритма '
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 0.67 + 1 + 0.07 + 0.32 + 0.45 + 0.3 + 0.23 + 0.83],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(self.volume_well_jamming)) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(
                 ["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и '
                 'Заказчика, Пуск. ком' if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять  {self.data_well.dict_pump_ecn["before"]} с пакером {self.data_well.paker_before["before"]}',
             None,
             f'Поднять  {self.data_well.dict_pump_ecn["before"]} с пакером {self.data_well.paker_before["before"]} с '
             f'глубины {round(self.length_nkt, 1)}м (компоновка НКТ {self.nkt_diam_fond} '
             f'на поверхность '
             f'с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд.'
             f' весом {self.data_well.fluid_work} '
             f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с '
             f'контролем АСПО '
             f'на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)]
        ]

        return lift_ord


class LiftVoronka(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_voronka())
            work_list.extend(self.append_posle_lift())
            return work_list

    def lifting_voronka(self):
        lift_voronka = [
            [self.well_jamming_str[2], None, self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][
                 0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'Сорвать планшайбу не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)',
             None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую '
             f'нагрузку на НКТ не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
             f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при '
             f'необходимости  с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на '
             f'расхаживание - не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО '
             f'Региона - для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join(
                 ['Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if self.data_well.category_pvo == 1
                  else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять воронку  с Н-{round(self.length_nkt, 1)}м',
             None,
             f'Поднять  воронку с глубины {round(self.length_nkt, 1)}м'
             f' (компоновка НКТ{self.nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с '
             f'доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  '
             f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с'
             f' контролем АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', liftingGNO(self.data_well.dict_nkt_before)],
        ]
        if not self.data_well.dict_nkt_before:
            lift_voronka.pop(-1)
        return lift_voronka


class LiftPumpNnWithPaker(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_nn_with_paker())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_nn_with_paker(self):
        sucker_jamming = ""
        if self.without_damping_true is False:
            sucker_jamming = f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу." \
                             f" Произвести глушение в НКТ в объеме {volume_pod_nkt(self)}м3"
        lift_pump_nn_with_paker = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            ['Поднять плунжер', None,
             f'Сорвать плунжер насоса (зафиксировать вес при срыве). Обвязать устье скважины согласно '
             f'схемы №3 утвержденной главным '
             f'инженером {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.text_pvo} Спуском одной штанги заловить конус. '
             f'{sucker_jamming}м3. Техостой 2ч. '
             f'Поднять на штангах плунжер с гл. {int(self.data_well.dict_pump_shgn_depth["before"])}м с доливом тех '
             f'жидкости уд.весом {self.data_well.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве '
             f'насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с '
             f'последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с'
             f' подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора '
             f'учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(self.data_well.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер  не '
             f'более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)',
             None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
             f'выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя'
             f' ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
             f'более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
             f'При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  '
             f'с противодавлением в НКТ (время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на '
             f'расхаживание - не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления'
             f' алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if
                 self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
                f'Поднять  насос {self.data_well.dict_pump_shgn["before"]} с пакером '
                f'{self.data_well.paker_before["before"]}',
                None,
                f'Поднять  насос {self.data_well.dict_pump_shgn["before"]} с пакером '
                f'{self.data_well.paker_before["before"]} с глубины '
                f'{round(self.length_nkt, 1)}м '
                f'(компоновка НКТ{self.nkt_diam_fond}) на '
                f'поверхность с '
                f'замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом '
                f'{self.data_well.fluid_work}  '
                f'в объеме '
                f'{round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с контролем '
                f'АСПО '
                f'на стенках НКТ.',
                None, None,
                None, None, None, None, None,
                'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)],
        ]
        return lift_pump_nn_with_paker


class LiftPumpNvWithPaker(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_nv_with_paker())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_nv_with_paker(self):
        lift_pump_nv_with_paker = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'Поднять насос {self.data_well.dict_pump_shgn["before"]}', None,
             f'Сорвать насос {self.data_well.dict_pump_shgn["before"]} (зафиксировать вес при срыве). '
             f'Обвязать устье скважины '
             f'согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). '
             f'Опрессовать ПВО на {self.text_pvo} '
             f'{"".join([" " if self.without_damping_true is True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу. Произвести глушение в НКТ в объеме{volume_pod_nkt(self)}м3. Техостой 2ч."])}'
             f' Поднять на штангах насос с гл. {float(self.data_well.dict_pump_shgn_depth["before"])}м с '
             f'доливом тех жидкости уд.весом {self.data_well.fluid_work} '
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
             lifting_sucker_rod(self.data_well.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
             f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
             f'в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не '
             f'более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
             f'для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if self.data_well.category_pvo == 1 else \
                     'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять  З.О. с пакером {self.data_well.paker_before["before"]}', None,
             f'Поднять  замковую опору с пакером {self.data_well.paker_before["before"]} с глубины'
             f' {round(self.length_nkt, 1)}м  (компоновка НКТ{self.nkt_diam_fond}) на '
             f'поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  '
             f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с '
             f'контролем АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)],
        ]
        return lift_pump_nv_with_paker


class LiftEcnWithPaker(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_ecn_with_paker())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_ecn_with_paker(self):
        enc_jamming = "".join([" " if self.without_damping_true is True
                               else f"При наличии Избыточного давления не позволяющее сорвать пакера: "
                                    f"Произвести глушение в НКТ в объеме {volume_pod_nkt(self)}м3."
                                    f" {self.data_well.fluid_work}"])

        lift_ecn_with_paker = [
            ['Опрессовать ГНО на Р=50атм', None,
             'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. '
             '(Вызов представителя осуществлять '
             'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [None, None,
             f'Сбить сбивной клапан. '
             f'{enc_jamming}', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'срыв пакера не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки '
             f'с выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя '
             f'ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
             f'более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
             f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
             f'не более 6 часов, '
             f'через 5 часов с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона '
             f'- для составления алгоритма последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                 if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять  {self.data_well.dict_pump_ecn["before"]} с пакером {self.data_well.paker_before["before"]}',
             None,
             f'Поднять  {self.data_well.dict_pump_ecn["before"]} с пакером {self.data_well.paker_before["before"]}'
             f'с глубины {round(self.length_nkt, 1)}м (компоновка НКТ{self.nkt_diam_fond}) '
             f'на поверхность с замером, накручиванием '
             f'колпачков с доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  '
             f'в объеме {round(round(self.length_nkt, 1) * 1.22 / 1000, 1)}м3 с контролем'
             f' АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)],
        ]
        return lift_ecn_with_paker


class LiftEcn(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_ecn())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_ecn(self):
        lift_ecn = [
            [f'Опрессовать ГНО на Р=50атм', None,
             'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. (Вызов '
             'представителя осуществлять '
             'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [f'Сбить сбивной клапан. {self.well_jamming_str[2]}', None,
             f'Сбить сбивной клапан. {self.well_jamming_str[0]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', 3.2],
            [None, None, self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'Сорвать планшайбу не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном'
             f' результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  '
             f'с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
             f'часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
             f'алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             'Заглубить оставшийся  кабель в скважину на 1-3 технологических НКТ' +
             self.pvo_gno(self.data_well.category_pvo)[0],
             None,
             None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                 if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
                f'Поднять  {self.data_well.dict_pump_ecn["before"]} с глубины {round(self.data_well.dict_pump_ecn_depth["before"], 1)}м',
                None,
                f'Поднять  {self.data_well.dict_pump_ecn["before"]} с глубины '
                f'{round(self.data_well.dict_pump_ecn_depth["before"], 1)}м '
                f'на поверхность с замером, накручиванием колпачков с доливом скважины '
                f'тех.жидкостью уд. весом {self.data_well.fluid_work}  '
                f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с '
                f'контролем АСПО'
                f' на стенках НКТ.',
                None, None,
                None, None, None, None, None,
                'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)],
        ]

        return lift_ecn


class LiftPumpNv(GnoParent):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        work_list.extend(self.lifting_nv())
        work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_nv(self):
        lift_pump_nv = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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

            [f'Поднять {self.data_well.dict_pump_shgn["before"]} с гл. '
             f'{self.data_well.dict_pump_shgn_depth["before"]}м', None,
             f'Сорвать насос {self.data_well.dict_pump_shgn["before"]} (зафиксировать вес при срыве). '
             f'Обвязать устье скважины '
             f'согласно схемы №3 утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.text_pvo} Поднять на штангах насос '
             f'с гл. {int(self.data_well.dict_pump_shgn_depth["before"])}м с доливом тех жидкости уд.весом '
             f'{self.data_well.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), '
             f'без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ '
             f'с последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с'
             f' подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ '
             f'и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(self.data_well.dict_sucker_rod)],
            [f'Сорвать планшайбу не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  с '
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
                 ["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if self.data_well.category_pvo == 1 else
                 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
                f'{"".join(["Допустить фНКТ для определения текущего забоя. " if self.data_well.gips_in_well is True else ""])}Поднять  замковую опору с глубины {round(self.length_nkt, 1)}м',
                None,
                f'{"".join(["Допустить фНКТ для определения текущего забоя. " if self.data_well.gips_in_well is True else ""])}Поднять  замковую опору  на НКТ с глубины {round(self.length_nkt, 1)}м (компоновка НКТ{self.nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {self.data_well.fluid_work}  '
                f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 '
                f'с контролем АСПО на стенках НКТ.',
                None, None,
                None, None, None, None, None,
                'Мастер КРС', liftingGNO(self.data_well.dict_nkt_before)],
        ]
        return lift_pump_nv


class LiftPumpNn(GnoParent):
    def __init__(self, parent=None):
        super(LiftPumpNn, self).__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_nn())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_nn(self):
        lift_pump_nn = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [self.well_jamming_str[2], None,
             self.well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика',
             [str(well_jamming_norm(volume_pod_nkt(self))) if self.without_damping_true is False else None][0]],
            [None, None,
             self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'поднять плунжер', None,
             f'Сорвать  плунжер. (зафиксировать вес при срыве). Обвязать устье скважины согласно схемы №3 '
             f'утвержденной главным '
             f'инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г при СПО штанг '
             f'(ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{self.text_pvo} Заловить конус спуском одной '
             f'штанги. Поднять на штангах плунжер с гл. '
             f'{float(self.data_well.dict_pump_shgn_depth["before"])}м с доливом тех '
             f'жидкости уд.весом {self.data_well.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов '
             f'(не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с '
             f'последующим '
             f'комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением '
             f'супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(self.data_well.dict_sucker_rod)],
            [f'Сорвать планшайбу не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). '
             f'ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  с'
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
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
            [f'Поднять  {self.data_well.dict_pump_shgn["before"]}', None,
             f'Поднять  {self.data_well.dict_pump_shgn["before"]} с глубины {round(self.data_well.dict_pump_shgn_depth["before"], 1)}м '
             f'(компоновка НКТ{self.nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины '
             f'тех.жидкостью уд. весом {self.data_well.fluid_work}  '
             f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с контролем АСПО '
             f'на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', liftingGNO(self.data_well.dict_nkt_before)],
        ]

        return lift_pump_nn


class LiftEcnWith2Paker(GnoParent):
    def __init__(self, parent=None):
        super(LiftEcnWith2Paker, self).__init__(parent)

    def add_work_lift(self):
        work_list = self.begin_work()
        if work_list:
            work_list.extend(self.lifting_with2_paker())
            work_list.extend(self.append_posle_lift())
        return work_list

    def lifting_with2_paker(self):
        lift_ecn_with_2paker = [
            [f'Опрессовать ГНО на Р=50атм', None,
             'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. (Вызов '
             'представителя осуществлять '
             'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [f'Сбить сбивной клапан. {self.well_jamming_str[2]}', None,
             f'Сбить сбивной клапан. {self.well_jamming_str[0]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', 3.2],
            [None, None, self.well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{self.lifting_unit()}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
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
            [f'Сорвать планшайбу не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(self.data_well.dict_nkt_before) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(self.data_well.dict_nkt_before), 1)}т) + 20%). '
             f'ПРИМЕЧАНИЕ: При отрицательном'
             f' результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту),  при необходимости  '
             f'с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
             f'часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
             f'алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if self.data_well.category_pvo == 2
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
            [self.pvo_gno(self.data_well.category_pvo)[1], None,
             self.pvo_gno(self.data_well.category_pvo)[0],
             None,
             None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                 if self.data_well.category_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(
                 self.pvo_gno(self.data_well.category_pvo)[0]) else 0.23 + 0.3 + 0.83 + 0.67 + 0.14][0]],
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
                f'Поднять {self.data_well.dict_pump_ecn["before"]} с глубины'
                f' {round(self.data_well.dict_pump_ecn_depth["before"], 1)}м',
                None,
                f'Поднять  {self.data_well.dict_pump_ecn["before"]} с глубины '
                f'{round(self.data_well.dict_pump_ecn_depth["before"], 1)}м '
                f' на поверхность с замером, '
                f'накручиванием колпачков с доливом скважины '
                f'тех.жидкостью уд. весом {self.data_well.fluid_work}  '
                f'в объеме {round(round(self.length_nkt, 1) * 1.12 / 1000, 1)}м3 с '
                f'контролем АСПО'
                f' на стенках НКТ.',
                None, None,
                None, None, None, None, None,
                'Мастер КРС', round(liftingGNO(self.data_well.dict_nkt_before) * 1.2, 2)],
        ]
        return lift_ecn_with_2paker
