import logging
from collections import namedtuple

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog

import H2S
import data_list
from selectPlast import CheckBoxDialog

from .rationingKRS import liftingNKT_norm, descentNKT_norm, well_volume_norm


def kot_select(self, current_bottom):
    if self.dict_data_well["column_additional"] is False \
            or (
            self.dict_data_well["column_additional"] is True and self.dict_data_well["current_bottom"] <= self.dict_data_well["head_column_additional"]._value):
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{self.dict_data_well["nkt_diam"]}мм 10м + репер '

    elif self.dict_data_well["column_additional"] is True and self.dict_data_well["column_additional_diametr"]._value < 110 and \
            current_bottom >= self.dict_data_well["head_column_additional"]._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) + НКТ{60}мм 10м + репер + ' \
                     f'НКТ60мм L- {round(current_bottom - self.dict_data_well["head_column_additional"]._value, 0)}м'
    elif self.dict_data_well["column_additional"] is True and self.dict_data_well["column_additional_diametr"]._value > 110 and \
            current_bottom >= self.dict_data_well["head_column_additional"]._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) + НКТ{73}мм со снятыми фасками 10м + репер + ' \
                     f'НКТ{self.dict_data_well["nkt_diam"]}мм со снятыми фасками' \
                     f' L- {round(current_bottom - self.dict_data_well["head_column_additional"]._value, 0)}м'

    return kot_select


def kot_work(self, current_bottom=0):
    if current_bottom == 0:
        current_bottom, _ = QInputDialog.getDouble(None,
                                                   'Глубина забоя',
                                                   'Введите глубину необходимого текущего забоя',
                                                   self.dict_data_well["current_bottom"], 1, 10000, 1)

    kot_list = [
        [f'статической уровень {self.dict_data_well["static_level"]._value}', None,
         f'При отсутствии циркуляции:\n'
         f'Спустить {kot_select(self, current_bottom)} на НКТ{self.dict_data_well["nkt_diam"]}мм до глубины {current_bottom}м'
         f' с замером, шаблонированием шаблоном {self.dict_data_well["nkt_template"]}мм.',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(current_bottom, 1)],
        [f'{kot_select(self, current_bottom)} до H-{current_bottom} закачкой обратной промывкой', None,
         f'Произвести очистку забоя скважины до гл.{current_bottom}м закачкой обратной промывкой тех '
         f'жидкости уд.весом {self.dict_data_well["fluid_work"]}, по согласованию с Заказчиком',
         None, None, None, None, None, None, None, 'мастер КРС', 0.4],
        [None, None,
         f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', None],
        [None, None,
         f'Поднять {kot_select(self, current_bottom)} на НКТ{self.dict_data_well["nkt_diam"]}мм c глубины '
         f'{current_bottom}м с доливом скважины в объеме {round(float(current_bottom) * 1.12 / 1000, 1)}м3 '
         f'удельным весом {self.dict_data_well["fluid_work"]}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(float(current_bottom), 1)],
        [None, None,
         f'По согласованию с УСРСиСТ СПО КОТ повторить',
         None, None, None, None, None, None, None,
         'мастер КРС', None]
    ]
    self.dict_data_well["current_bottom"] = current_bottom
    return kot_list


def check_h2s(self, plast=0, fluid_new=0, expected_pressure=0):
    if len(self.dict_data_well["plast_project"]) != 0:
        if len(self.dict_data_well["plast_project"]) != 0:
            plast = self.dict_data_well["plast_project"][0]
        else:
            plast, ok = QInputDialog.getText(self, 'выбор пласта для расчета ЖГС ', 'введите пласт для перфорации')
            self.dict_data_well["plast_project"].append(plast)
        try:
            fluid_new = list(self.dict_data_well["dict_perforation_project"][plast]['рабочая жидкость'])[0]
        except:
            fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                   'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        if len(self.dict_data_well["dict_category"]) != 0:
            expected_pressure = self.dict_data_well["dict_category"][self.dict_data_well["plast_project"][0]]['по давлению'].data_pressuar
        else:
            expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                           'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)

    else:
        fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                               'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        plast, ok = QInputDialog.getText(self, 'выбор пласта для расчета ЖГС ', 'введите пласт для перфорации')

        expected_pressure, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                       'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)

    return fluid_new, plast, expected_pressure


def need_h2s(self, fluid_new, plast_edit, expected_pressure):
    asd = self.dict_data_well["dict_category"]
    сat_h2s_list = list(map(int, [self.dict_data_well["dict_category"][plast]['по сероводороду'].category for plast in
                                  self.dict_data_well['plast_work'] if self.dict_data_well["dict_category"].get(plast) and
                                  self.dict_data_well["dict_category"][plast]['отключение'] == 'рабочий']))

    cat_h2s_list_plan = list(map(int, [self.dict_data_well["dict_category"][plast]['по сероводороду'].category for plast in
                                       self.dict_data_well["plast_project"] if self.dict_data_well["dict_category"].get(plast) and
                                       self.dict_data_well["dict_category"][plast]['отключение'] == 'планируемый']))

    if len(cat_h2s_list_plan) != 0:

        if cat_h2s_list_plan[0] in [1, 2, '1', '2'] and len(self.dict_data_well['plast_work']) == 0:
            expenditure_h2s = round(
                max([self.dict_data_well["dict_category"][plast]['по сероводороду'].poglot for plast in self.dict_data_well["plast_project"]]), 3)
            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода {self.dict_data_well["type_absorbent"]} из ' \
                         f'расчета {expenditure_h2s}кг/м3 либо аналог'
            fluid_work_short = f'{fluid_new}г/см3 {self.dict_data_well["type_absorbent"]} {expenditure_h2s}кг/м3 '
        elif cat_h2s_list_plan[0] in [3, '3'] and len(self.dict_data_well['plast_work']) == 0:
            fluid_work = f'{fluid_new}г/см3 '
            fluid_work_short = f'{fluid_new}г/см3 '

        elif ((cat_h2s_list_plan[0] in [1, 2]) or (сat_h2s_list[0] in [1, 2])) and len(self.dict_data_well['plast_work']) != 0:
            try:
                expenditure_h2s_plan = max(
                    [self.dict_data_well["dict_category"][self.dict_data_well["plast_project"][0]]['по сероводороду'].poglot
                     for plast in self.dict_data_well["plast_project"]])
            except:
                expenditure_h2s_plan = QInputDialog.getDouble(None, 'нет данных',
                                                              'ВВедите расход поглотетеля сероводорода', 0.25, 0, 3)

            expenditure_h2s = max(
                [self.dict_data_well["dict_category"][self.dict_data_well['plast_work'][0]]['по сероводороду'].poglot])
            expenditure_h2s = round(max([expenditure_h2s, expenditure_h2s_plan]), 2)

            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода {self.dict_data_well["type_absorbent"]} из ' \
                         f'расчета {expenditure_h2s}кг/м3 либо аналог'
            fluid_work_short = f'{fluid_new}г/см3 {self.dict_data_well["type_absorbent"]} {expenditure_h2s}кг/м3 '
        else:
            fluid_work = f'{fluid_new}г/см3 '
            fluid_work_short = f'{fluid_new}г/см3 '
    else:

        cat_list = ['1', '2', '3']
        cat_pressuar, ok = QInputDialog.getItem(None, 'Категория скважины по давлению вскрываемого пласта',
                                                'Выберете категорию скважины',
                                                cat_list, 0, False)
        pressuar, ok = QInputDialog.getDouble(None, 'Значение по давлению вскрываемого пласта',
                                              'ВВедите давление вскрываемого пласта', 0, 0, 600, 1)

        cat_H2S, ok = QInputDialog.getItem(None, 'Категория скважины по сероводороду вскрываемого пласта',
                                           'Выберете категорию скважины по сероводороду вскрываемого пласта',
                                           cat_list, 0, False)

        cat_h2s_list_plan.append(cat_H2S)
        h2s_mg, _ = QInputDialog.getDouble(None, 'сероводород в мг/л',
                                           'Введите значение серовородода в мг/л', 0, 0, 100, 5)
        self.dict_data_well["h2s_mg"].append(h2s_mg)
        h2s_pr, _ = QInputDialog.getDouble(None, 'сероводород в процентах',
                                           'Введите значение серовородода в процентах', 0, 0, 100, 1)
        poglot = H2S.calv_h2s(None, cat_H2S, h2s_mg, h2s_pr)
        Data_h2s = namedtuple("Data_h2s", "category data_procent data_mg_l poglot")
        Pressuar = namedtuple("Pressuar", "category data_pressuar")
        self.dict_data_well["dict_category"].setdefault(plast_edit, {}).setdefault(
            'по давлению', Pressuar(int(cat_H2S), pressuar))
        self.dict_data_well["dict_category"].setdefault(plast_edit, {}).setdefault(
            'по сероводороду', Data_h2s(int(cat_pressuar), h2s_pr, h2s_mg, poglot))
        self.dict_data_well["dict_category"].setdefault(plast_edit, {}).setdefault(
            'отключение', 'планируемый')

        if cat_h2s_list_plan[0] in [1, 2]:

            expenditure_h2s = round(
                max([self.dict_data_well["dict_category"][plast]['по сероводороду'].poglot for plast in self.dict_data_well["plast_project"]]), 2)
            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода {self.dict_data_well["type_absorbent"]} из ' \
                         f'расчета {expenditure_h2s}кг/м3  либо аналог'
            fluid_work_short = f'{fluid_new}г/см3 {self.dict_data_well["type_absorbent"]} {expenditure_h2s}кг/м3 '
        else:
            fluid_work = f'{fluid_new}г/см3 '
            fluid_work_short = f'{fluid_new}г/см3 '

    return (fluid_work, fluid_work_short, plast_edit, expected_pressure)


def konte(self):
    konte_list = [
        [f'Скважина согласована на проведение работ по технологии контейнерно-канатных технологий', None,
         f'Скважина согласована на проведение работ по технологии контейнерно-канатных технологий по '
         f'технологическому плану Таграс-РС.'
         f'Вызвать геофизическую партию. Заявку оформить за 24 часов сутки через '
         f'геологическую службу {data_list.contractor}. '
         f'Произвести монтаж ПАРТИИ ГИС согласно утвержденной главным инженером от'
         f' {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}. Предварительно нужно заявить вставку №6',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.25],
        [None, None, f'Произвести работы указанные в плане работ силами спец подрядчика, при выполнении '
                     f'из основного плана работ работы исключить',
         None, None, None, None, None, None, None,
         'мастер КРС', 12]
    ]
    return konte_list


def definition_Q(self):
    definition_Q_list = [
        [f'Насыщение 5м3 определение Q при 80-120атм', None,
         f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
         f' на приемистость в трех режимах при Р=80-120атм в '
         f'присутствии представителя супервайзерской службы или подрядчика по РИР. '
         f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
         f'с подтверждением за 2 часа до '
         f'начала работ). ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.17 + 0.2 + 0.2 + 0.2 + 0.15 + 0.52]]
    return definition_Q_list


def definition_Q_nek(self):
    open_checkbox_dialog(self.dict_data_well)
    plast = data_list.plast_select
    definition_Q_list = [[f'Насыщение 5м3 Q-{plast} при {self.dict_data_well["max_admissible_pressure"]._value}', None,
                          f'Произвести насыщение скважины по затрубу до стабилизации давления закачки не '
                          f'менее 5м3. Опробовать по затрубу'
                          f' на приемистость {plast} при Р={self.dict_data_well["max_admissible_pressure"]._value}атм в присутствии '
                          f'представителя ЦДНГ. '
                          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                          f'с подтверждением за 2 часа до '
                          f'начала работ). ',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 0.17 + 0.2 + 0.2 + 0.2 + 0.15 + 0.52]]

    return definition_Q_list


def privyazka_nkt(self):
    priv_list = [[f'ГИС Привязка по ГК и ЛМ', None,
                  f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                  f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
                  f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                  f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
                  None, None, None, None, None, None, None,
                  'Мастер КРС, подрядчик по ГИС', 4]]
    return priv_list


def definitionBottomGKLM(self):
    priv_list = [[f'Отбить забой по ГК и ЛМ', None,
                  f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                  f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером  {data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                  f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
                  None, None, None, None, None, None, None,
                  'Мастер КРС, подрядчик по ГИС', 4]]
    return priv_list


def pressuar_gis(self):
    priv_list = [[f'Замер Рпл', None,
                  f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС {data_list.contractor}". '
                  f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером '
                  f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г. '
                  f'Произвести замер Рпл в течении 4часов. При необходимости согласовать с заказчиком смену категории',
                  None, None, None, None, None, None, None,
                  'Мастер КРС, подрядчик по ГИС', 8]]
    return priv_list


def pvo_cat1(self):
    if 'Ойл' in data_list.contractor:
        date_str = 'от 07.03.2024г'
    elif 'РН' in data_list.contractor:
        date_str = 'от 28.02.2024г'

    pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером {data_list.contractor} {date_str} ' \
            f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f' (при необходимости произвести монтаж переводника' \
            f' П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
            f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на ' \
            f'Р-{self.dict_data_well["max_admissible_pressure"]._value}атм ' \
            f'(на максимально допустимое давление опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. \n' \
            f'- Обеспечить о обогрев превентора, станции управления ПВО оборудовать теплоизоляционными ' \
            f'материалом в зимней период. \n Получить разрешение на производство работ в присутствии представителя ПФС'

    pvo_list = [
        [None, None,
         "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
         "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
         "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность" \
         " для жизни людей"
         " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
         "ПАСФ приглашается за 24 часа до проведения "
         "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. "
         "Пусковой комиссией составить акт готовности "
         "подъёмного агрегата для ремонта скважины.",
         None, None, None, None, None, None, None,
         'Мастер КРС', None],
        [f'монтаж ПВО по схеме № 2 c гидроПВО', None,
         pvo_1, None, None,
         None, None, None, None, None,
         'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком', 4.67]]
    self.dict_data_well["kat_pvo"] = 1
    return pvo_list


def fluid_change(self):
    from open_pz import CreatePZ

    try:
        fluid_work, fluid_work_short, plast, expected_pressure = check_h2s(self)

        self.dict_data_well["fluid_work"], self.dict_data_well["fluid_work_short"] = fluid_work, fluid_work_short

        fluid_change_list = [
            [f'Cмена объема {self.dict_data_well["fluid"]}г/см3- {round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3',
             None,
             f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {self.dict_data_well["fluid_work"]} '
             f'(по расчету по вскрываемому пласта Рожид- {expected_pressure}атм) в объеме не '
             f'менее {round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3  в присутствии '
             f'представителя заказчика, Составить акт. '
             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
             f'2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(well_volume(self, self.dict_data_well["current_bottom"]))]
        ]


    except Exception as e:
        logging.exception("Произошла ошибка")
        return

    return fluid_change_list


def update_fluid(self, index_plan, fluid_str, table_widget):
    row_index = index_plan - self.dict_data_well["count_row_well"]

    for index_row, data in enumerate(self.dict_data_well["data_list"]):
        if index_row == row_index:
            fluid_str_old = self.dict_data_well["data_list"][index_row][7]
        if row_index <= index_row:

            if self.dict_data_well["data_list"][index_row][7] == fluid_str_old:
                self.dict_data_well["data_list"][index_row][7] = fluid_str

                for column in range(table_widget.columnCount()):
                    if column == 2 or column == 0:
                        row_change = index_row + self.dict_data_well["count_row_well"]
                        value = table_widget.item(row_change, column).text()
                        if value != None or value != '':
                            if fluid_str_old in value:
                                new_value = value.replace(fluid_str_old, fluid_str)
                                new_value = QtWidgets.QTableWidgetItem(f'{new_value}')
                                table_widget.setItem(row_change, column, new_value)


def calculation_fluid_work(dict_data_well, vertical, pressure):
    if (isinstance(vertical, float) or isinstance(vertical, int)) and (
            isinstance(pressure, float) or isinstance(pressure, int)):

        # print(vertical, pressure)
        stockRatio = 0.1 if float(vertical) <= 1200 else 0.05

        fluidWork = round(float(str(pressure)) * (1 + stockRatio) / float(vertical) / 0.0981, 2)
        # print(fluidWork < 1.02 , (self.dict_data_well["region"] == 'КГМ' or self.dict_data_well["region"] == 'АГМ'))
        if fluidWork < 1.02 and (dict_data_well["region"] == 'КГМ' or dict_data_well["region"] == 'АГМ'):
            fluidWork = 1.02
        elif fluidWork < 1.02 and (
                dict_data_well["region"] == 'ИГМ' or dict_data_well["region"] == 'ТГМ' or dict_data_well["region"] == 'ЧГМ'):
            fluidWork = 1.01

        return fluidWork
    else:
        return None




def lifting_unit(self):
    aprs_40 = f'Установить подъёмный агрегат на устье не менее 40т.\n' \
              f' Пусковой комиссией составить акт готовности  подьемного агрегата и бригады для проведения ремонта скважины.' \
              f'ПРИМЕЧАНИЕ:  ПРИ ИСПОЛЬЗОВАНИИ ПОДЪЕМНОГО АГРЕТАТА АПРС-50, А5-40, АПРС-50 ДОПУСКАЕТСЯ РАБОТА БЕЗ ' \
              f'ПРИМЕНЕНИЯ ВЕТРОВЫХ ОТТЯЖЕК ПРИ НАГРУЗКАХ НЕ БОЛЕЕ 25ТН. ПРИ НЕОБХОДИМОСТИ УВЕЛИЧЕНИЯ НАГРУЗКИ ТРЕБУЕТСЯ ' \
              f'ОСНАСТИТЬ ПОДЪЕМНЫЙ АГРЕГАТ ВЕТРОВЫМИ ОТТЯЖКАМИ. ПРИ ЭТОМ МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ 80% ОТ' \
              f' СТРАГИВАЮЩЕЙ НАГРУЗКИ НА НКТ.ПРИ ИСПОЛЬЗОВАНИИ ПОДЬЕМНОГО АГРЕГАТА  УПА-60/80, БАРС, А-50, АПР 60/80 ' \
              f'РАБОТАТЬ ТОЛЬКО С ПРИМЕНЕНИЕМ  ОТТЯЖЕК МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ 80% ОТ СТРАГИВАЮЩЕЙ ' \
              f'НАГРУЗКИ НА НКТ. После монтажа подъёмника якоря ветровых оттяжек должны быть испытаны на нагрузки, ' \
              f'установленные инструкцией по эксплуатации завода - изготовителя в присутствии супервайзера Заказчика. ' \
              f'Составить акт готовности подъемного агрегата. Пусковой комиссией составить акт готовности  подьемного ' \
              f'агрегата и бригады для проведения ремонта скважины. Дальнейшие работы продолжить после проведения пусковой ' \
              f'комиссии заполнения пусковой документации. '
    upa_60 = f'Установить подъёмный агрегат на устье не менее 60т. Пусковой комиссией составить ' \
             f'акт готовности  подьемного агрегата и бригады для проведения ремонта скважины.'

    return upa_60 if self.dict_data_well["bottomhole_artificial"]._value >= 2300 else aprs_40


def volume_vn_ek(self, current):
    if self.dict_data_well["column_additional"] is False or self.dict_data_well["column_additional"] is True and current < self.dict_data_well["head_column_additional"]._value:
        volume = round(
            (self.dict_data_well["column_diametr"]._value - 2 * self.dict_data_well["column_wall_thickness"]._value) ** 2 * 3.14 / 4 / 1000, 2)
    else:
        volume = round(
            (self.dict_data_well["column_additional_diametr"]._value - 2 * self.dict_data_well["column_additional_wall_thickness"]._value
             ) ** 2 * 3.14 / 4 / 1000, 2)

    return round(volume, 1)


def volume_vn_nkt(dict_nkt):  # Внутренний объем одного погонного местра НКТ
    volume_vn_nkt = 0
    for nkt, lenght_nkt in dict_nkt.items():

        nkt = ''.join(c for c in str(nkt) if c.isdigit())
        if '60' in str(nkt):
            t_nkt = 5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)
        elif '73' in str(nkt):
            t_nkt = 5.5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)
        elif '89' in str(nkt):
            t_nkt = 6
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)

        elif '48' in str(nkt):
            t_nkt = 4.5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt * 1.1, 5)

    return round(volume_vn_nkt, 1)


def volume_rod(self, dict_sucker_rod):  # Объем штанг

    from find import FindIndexPZ
    volume_rod = 0
    # print(dict_sucker_rod)
    for diam_rod, lenght_rod in dict_sucker_rod.items():
        if diam_rod:
            volume_rod += (3.14 * (lenght_rod * (
                    FindIndexPZ.check_str_none(self, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
    return round(volume_rod, 5)


def volume_nkt(dict_nkt):  # Внутренний объем НКТ по фондовым НКТ
    volume_nkt = 0

    for nkt, length_nkt in dict_nkt.items():
        if nkt:
            volume_nkt += (float(nkt) - 2 * 7.6) ** 2 * 3.14 / 4 / 1000000 * length_nkt
    # print(f'объем НКТ {volume_nkt}')
    return volume_nkt


def weigth_pipe(dict_nkt):
    weigth_pipe = 0
    for nkt, lenght_nkt in dict_nkt.items():
        if '73' in str(nkt):
            weigth_pipe += lenght_nkt * 9.2 / 1000
        elif '60' in str(nkt):
            weigth_pipe += lenght_nkt * 7.5 / 1000
        elif '89' in str(nkt):
            weigth_pipe += lenght_nkt * 16 / 1000
        elif '48' in str(nkt):
            weigth_pipe += lenght_nkt * 4.3 / 1000
    return weigth_pipe


def volume_nkt_metal(dict_nkt):  # Внутренний объем НКТ железа по фондовым
    volume_nkt_metal = 0
    for nkt, length_nkt in dict_nkt.items():
        if '73' in str(nkt):
            volume_nkt_metal += 1.17 * length_nkt / 1000
        elif '60' in str(nkt):
            volume_nkt_metal += 0.87 * length_nkt / 1000
        elif '89' in str(nkt):
            volume_nkt_metal += 1.7 * length_nkt / 1000
        elif '48' in str(nkt):
            volume_nkt_metal += 0.55 * length_nkt / 1000
    return round(volume_nkt_metal, 1)


def well_volume(self, current_bottom):
    # print(self.dict_data_well["column_additional"])
    if self.dict_data_well["column_additional"] is False:
        # print(self.dict_data_well["column_diametr"]._value, self.dict_data_well["column_wall_thickness"]._value, current_bottom)
        volume_well = 3.14 * (
                self.dict_data_well["column_diametr"]._value - self.dict_data_well["column_wall_thickness"]._value * 2) ** 2 / 4 / 1000000 * (
                          current_bottom)

    else:
        # print(f' ghb [{self.dict_data_well["column_additional_diametr"]._value, self.dict_data_well["column_additional_wall_thickness"]._value}]')
        volume_well = (3.14 * (
                self.dict_data_well["column_additional_diametr"]._value - self.dict_data_well["column_additional_wall_thickness"]._value * 2) ** 2 / 4 / 1000 * (
                               current_bottom - float(self.dict_data_well["head_column_additional"]._value)) / 1000) + (
                              3.14 * (
                              self.dict_data_well["column_diametr"]._value - self.dict_data_well["column_wall_thickness"]._value * 2) ** 2 / 4 / 1000 * (
                                  float(self.dict_data_well["head_column_additional"]._value)) / 1000)
    # print(f'Объем скважины {volume_well}')
    return round(volume_well, 1)


def volume_pod_NKT(self):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем

    nkt_l = round(sum(list(self.dict_data_well["dict_nkt"].values())), 1)
    if self.dict_data_well["column_additional"] is False:
        v_pod_gno = 3.14 * (int(self.dict_data_well["column_diametr"]._value) - int(
            self.dict_data_well["column_wall_thickness"]._value) * 2) ** 2 / 4 / 1000 * (
                            float(self.dict_data_well["current_bottom"]) - int(nkt_l)) / 1000

    elif round(sum(list(self.dict_data_well["dict_nkt"].values())), 1) > float(self.dict_data_well["head_column_additional"]._value):
        v_pod_gno = 3.14 * (
                self.dict_data_well["column_diametr"]._value - self.dict_data_well["column_wall_thickness"]._value * 2) ** 2 / 4 / 1000 * (
                            float(self.dict_data_well["head_column_additional"]._value) - nkt_l) / 1000 + 3.14 * (
                            self.dict_data_well["column_additional_diametr"]._value - self.dict_data_well["column_additional_wall_thickness"]._value * 2) ** 2 / 4 / 1000 * (
                            self.dict_data_well["current_bottom"] - float(self.dict_data_well["head_column_additional"]._value)) / 1000
    elif nkt_l <= float(self.dict_data_well["head_column_additional"]._value):
        v_pod_gno = 3.14 * (
                self.dict_data_well["column_additional_diametr"]._value - self.dict_data_well["column_additional_wall_thickness"]._value * 2) ** 2 / 4 / 1000 * (
                            self.dict_data_well["current_bottom"] - nkt_l) / 1000
    volume_in_nkt = v_pod_gno + volume_vn_nkt(self.dict_data_well["dict_nkt"]) - volume_rod(self, self.dict_data_well["dict_sucker_rod"])
    # print(f'Внутренный объем + Зумпф{volume_in_nkt, v_pod_gno, volume_vn_nkt(self.dict_data_well["dict_nkt"])}, ')
    return round(volume_in_nkt, 1)


def volume_jamming_well(self, current_bottom):  # объем глушения скважины

    volume_jamming_well = round(
        (well_volume(self, current_bottom) - volume_nkt_metal(self.dict_data_well["dict_nkt"]) - volume_rod(self,
                                                                                               self.dict_data_well["dict_sucker_rod"])) * 1.1,
        1)

    return volume_jamming_well




def is_number(num):
    if num is None:
        return 0
    try:
        float(str(num).replace(",", "."))
        return True
    except ValueError or TypeError:
        return False


def open_checkbox_dialog(self):
    dialog = CheckBoxDialog(self)
    dialog.exec_()


