import logging
from collections import namedtuple

from PyQt5.QtWidgets import QInputDialog, QMessageBox

import H2S
import well_data
from selectPlast import CheckBoxDialog

from .rationingKRS import liftingNKT_norm, descentNKT_norm, well_volume_norm


def kot_select(self, current_bottom):


    if well_data.column_additional is False \
            or (well_data.column_additional is True and well_data.current_bottom <= well_data.head_column_additional._value):
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{well_data.nkt_diam}мм 10м + репер '

    elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and\
            current_bottom >= well_data.head_column_additional._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{60}мм 10м + репер + ' \
                     f'НКТ60мм L- {round(current_bottom - well_data.head_column_additional._value, 0)}м'
    elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and\
            current_bottom >= well_data.head_column_additional._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{73}мм со снятыми фасками 10м + репер + ' \
                     f'НКТ{well_data.nkt_diam}мм со снятыми фасками' \
                     f' L- {round(current_bottom - well_data.head_column_additional._value, 0)}м'

    return kot_select


def kot_work(self, current_bottom):


    kot_list = [[f'статической уровень {well_data.static_level._value}', None,
                 f'При отсутствии циркуляции:\n'
                 f'Спустить {kot_select(self, current_bottom)} на НКТ{well_data.nkt_diam}мм до глубины {current_bottom}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(current_bottom, 1)],
                [f'{kot_select(self, current_bottom)} до H-{current_bottom} закачкой обратной промывкой', None,
                 f'Произвести очистку забоя скважины до гл.{current_bottom}м закачкой обратной промывкой тех '
                 f'жидкости уд.весом {well_data.fluid_work}, по согласованию с Заказчиком',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [None, None,
                 f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', None],

                [None, None,
                 f'Поднять {kot_select(self, current_bottom)} на НКТ{well_data.nkt_diam}мм c глубины {current_bottom}м с доливом '
                 f'скважины в '
                 f'объеме {round(current_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(current_bottom, 1)]
                ]

    return kot_list




def check_h2s(self, plast= 0, fluid_new = 0, expected_pressure = 0):

    if len(well_data.plast_project) != 0:
        if len(well_data.plast_project) != 0:
            plast = well_data.plast_project[0]
        else:
            plast, ok = QInputDialog.getText(self, 'выбор пласта для расчета ЖГС ', 'введите пласт для перфорации')
            well_data.plast_project.append(plast)
        try:
            fluid_new = list(well_data.dict_perforation_project[plast]['рабочая жидкость'])[0]
        except:
            fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                   'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        if len(well_data.dict_category) != 0:
            expected_pressure = well_data.dict_category[well_data.plast_project[0]]['по давлению'].data_pressuar
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

def need_h2s(fluid_new, plast_edit, expected_pressure):
    сat_h2s_list = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                  well_data.plast_work if well_data.dict_category.get(plast) and
                                  well_data.dict_category[plast]['отключение'] == 'рабочий']))

    cat_h2s_list_plan = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                  well_data.plast_project if well_data.dict_category.get(plast) and
                                  well_data.dict_category[plast]['отключение'] == 'планируемый']))

    if len(cat_h2s_list_plan) != 0:

        if cat_h2s_list_plan[0] in [1, 2, '1', '2'] and len(well_data.plast_work) == 0:
            expenditure_h2s = round(max([well_data.dict_category[plast]['по сероводороду'].poglot for plast in well_data.plast_project]), 3)
            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {expenditure_h2s}кг/м3 '
            fluid_work_short = f'{fluid_new}г/см3 ХИМТЕХНО 101 {expenditure_h2s}кг/м3 '
        elif cat_h2s_list_plan[0] in [3, '3'] and len(well_data.plast_work) == 0:
            fluid_work = f'{fluid_new}г/см3 '
            fluid_work_short = f'{fluid_new}г/см3 '

        elif ((cat_h2s_list_plan[0] in [1, 2]) or (сat_h2s_list[0] in [1, 2])) and len(well_data.plast_work) != 0:
            try:
                expenditure_h2s_plan = max(
                    [well_data.dict_category[well_data.plast_project[0]]['по сероводороду'].poglot
                     for plast in well_data.plast_project])
            except:
                expenditure_h2s_plan = QInputDialog.getDouble(None, 'нет данных',
                                                              'ВВедите расход поглотетеля сероводорода', 0.25, 0, 3)

            expenditure_h2s = max(
                [well_data.dict_category[well_data.plast_work[0]]['по сероводороду'].poglot])
            expenditure_h2s = round(max([expenditure_h2s, expenditure_h2s_plan]), 2)

            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {expenditure_h2s}кг/м3 '
            fluid_work_short = f'{fluid_new}г/см3 ХИМТЕХНО 101 {expenditure_h2s}кг/м3 '
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
        well_data.h2s_mg.append(h2s_mg)
        h2s_pr, _ = QInputDialog.getDouble(None, 'сероводород в процентах',
                                           'Введите значение серовородода в процентах', 0, 0, 100, 1)
        poglot = H2S.calv_h2s(None, cat_H2S, h2s_mg, h2s_pr)
        Data_h2s = namedtuple("Data_h2s", "category data_procent data_mg_l poglot")
        Pressuar = namedtuple("Pressuar", "category data_pressuar")
        well_data.dict_category.setdefault(plast_edit, {}).setdefault(
            'по давлению', Pressuar(int(cat_H2S), pressuar))
        well_data.dict_category.setdefault(plast_edit, {}).setdefault(
            'по сероводороду', Data_h2s(int(cat_pressuar), h2s_pr, h2s_mg, poglot))
        well_data.dict_category.setdefault(plast_edit, {}).setdefault(
            'отключение', 'планируемый')

        if cat_h2s_list_plan[0] in [1, 2]:

            expenditure_h2s = round(
                max([well_data.dict_category[plast]['по сероводороду'].poglot for plast in well_data.plast_project]), 2)
            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                    f'расчета {expenditure_h2s}кг/м3 '
            fluid_work_short = f'{fluid_new}г/см3 ХИМТЕХНО 101 {expenditure_h2s}кг/м3 '
        else:
            fluid_work = f'{fluid_new}г/см3 '
            fluid_work_short = f'{fluid_new}г/см3 '
    print(f'')
    return (fluid_work, fluid_work_short, plast_edit, expected_pressure)

def konte(self):

    konte_list = [[f'Скважина согласована на проведение работ по технологии контейнерно-канатных технологий',
                   None,
                          f'Скважина согласована на проведение работ по технологии контейнерно-канатных технологий по '
                          f'технологическому плану Таграс-РС.'
                          f'Вызвать геофизическую партию. Заявку оформить за 24 часов сутки через '
                          f'геологическую службу "Ойл-сервис". '
                          f'Произвести  монтаж ПАРТИИ ГИС согласно утвержденной главным инженером от 14.10.2021г.',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 1.25],
                  [None, None, f'Произвести работы указанные в плане работ силами спец подрядчика, при выполнении '
                               f'из основного плана работ работы исключить',
                   None, None, None, None, None, None, None,
                   'мастер КРС', 12]
                  ]
    return konte_list
def definition_Q(self):

    definition_Q_list = [[f'Насыщение 5м3 определение Q при 80-120атм', None,
                           f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                           f' на приемистость в трех режимах при Р=80-120атм в '
                           f'присутствии представителя супервайзерской службы или подрядчика по РИР. '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до '
                           f'начала работ). ',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 0.17+0.2+0.2+0.2+0.15+0.52]]
    return definition_Q_list

def definition_Q_nek(self):
    open_checkbox_dialog()
    plast = well_data.plast_select
    definition_Q_list = [[f'Насыщение 5м3 Q-{plast} при {well_data.max_admissible_pressure._value}', None,
                          f'Произвести насыщение скважины по затрубу до стабилизации давления закачки не '
                           f'менее 5м3. Опробовать  '
                           f' на приемистость {plast} при Р={well_data.max_admissible_pressure._value}атм в присутствии '
                           f'представителя ЦДНГ. '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до '
                           f'начала работ). ',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 0.17+0.2+0.2+0.2+0.15+0.52]]

    return definition_Q_list
def privyazkaNKT(self):
    priv_list = [[f'ГИС Привязка по ГК и ЛМ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                 f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
     None, None, None, None, None, None, None,
     'Мастер КРС, подрядчик по ГИС', 4]]
    return priv_list

def definitionBottomGKLM(self):
    priv_list = [[f'Отбить забой по ГК и ЛМ', None,
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                 f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 4]]
    return priv_list

def pressuar_gis(self):
    priv_list = [[f'Замер Рпл', None,
                 f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                 f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                 f'Произвести замер Рпл в течении 4часов. При необходимости согласовать с заказчиком смену категории',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 8]]
    return priv_list

def pvo_cat1(self):

    pvo_1 = f'Установить ПВО  по  схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г ' \
            f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f' (при необходимости произвести монтаж переводника' \
            f' П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
            f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на Р-{well_data.max_admissible_pressure._value}атм ' \
            f'(на максимально допустимое давление опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. \n' \
            f'- Обеспечить о обогрев превентора, станции управления ПВО оборудовать теплоизоляционными ' \
            f'материалом в зимней период. \n Получить разрешение на производство работ в присутствии представителя ПФС'

    pvo_list = [
        [None, None,
         "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность"\
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
    well_data.kat_pvo = 1
    return pvo_list

def fluid_change(self):
    from open_pz import CreatePZ

    try:
        CreatePZ.fluid_work, CreatePZ.fluid_work_short, plast, expected_pressure = check_h2s(self)


        fluid_change_list = [[f'Cмена объема {CreatePZ.fluid}г/см3- {round(well_volume(self, CreatePZ.current_bottom), 1)}м3' ,
                              None,
                              f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {CreatePZ.fluid_work} '
                              f'(по расчету по вскрываемому пласта Рожид- {expected_pressure}атм) в объеме не '
                              f'менее {round(well_volume(self, CreatePZ.current_bottom), 1)}м3  в присутствии '
                              f'представителя заказчика, Составить акт. '
                              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
                              f'2 часа до начала работ)',
                              None, None, None, None, None, None, None,
                              'мастер КРС', well_volume_norm(well_volume(self, CreatePZ.current_bottom))]]
    except Exception as e:
        logging.exception("Произошла ошибка")
        return

    return fluid_change_list

def calculationFluidWork(vertical, pressure):
    if (isinstance(vertical, float) or isinstance(vertical, int)) and (
            isinstance(pressure, float) or isinstance(pressure, int)):

        # print(vertical, pressure)
        stockRatio = 0.1 if float(vertical) <= 1200 else 0.05

        fluidWork = round(float(str(pressure)) * (1 + stockRatio) / float(vertical) / 0.0981, 2)
        # print(fluidWork < 1.02 , (well_data.region == 'КГМ' or well_data.region == 'АГМ'))
        if fluidWork < 1.02 and (well_data.region == 'КГМ' or well_data.region == 'АГМ'):
            fluidWork = 1.02
        elif fluidWork < 1.02 and (
                well_data.region == 'ИГМ' or well_data.region == 'ТГМ' or well_data.region == 'ЧГМ'):
            fluidWork = 1.01

        return fluidWork
    else:
        return None


def pvo_gno(kat_pvo):
    # print(f' ПВО {kat_pvo}')
    pvo_2 = f'Установить ПВО по схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г (тип плашечный ' \
            f'сдвоенный ПШП-2ФТ-152х21) и посадить пакер. ' \
            f'Спустить пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до концевых ' \
            f'задвижек на Р-{well_data.max_admissible_pressure._value}атм на максимально допустимое давление ' \
            f'опрессовки эксплуатационной колонны в течении ' \
            f'30мин), сорвать пакер. ' \
            # f'В случае невозможности опрессовки по ' \
            # f'результатам определения приемистости и по согласованию с заказчиком  опрессовать трубные плашки ПВО на ' \
            # f'давление поглощения, но не менее 30атм. '

    pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г ' \
            f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f' (при необходимости произвести монтаж переводника' \
            f' П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
            f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на ' \
            f'Р-{well_data.max_admissible_pressure._value}атм ' \
            f'(на максимально допустимое давление опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. Опрессовать ' \
            f'выкидную линию после концевых задвижек на ' \
            f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на' \
            f'давление до 210 кгс/см2 ((21 МПа)\n' \
            f'- Обеспечить обогрев превентора и СУП в зимнее время . \n Получить разрешение на производство работ в ' \
            f'присутствии представителя ПФС'
    if kat_pvo == 1:
        return pvo_1, f'Монтаж ПВО по схеме №2 + ГидроПревентор'
    else:
        # print(pvo_2)
        return pvo_2, f'Монтаж ПВО по схеме №2'


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

    return upa_60 if well_data.bottomhole_artificial._value >= 2300 else aprs_40


def volume_vn_ek(current):
    if well_data.column_additional is False or well_data.column_additional is True and current < well_data.head_column_additional._value:
        volume = round(
            (well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value) ** 2 * 3.14 / 4 / 1000, 2)
    else:
        volume = round((well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value
                        ) ** 2 * 3.14 / 4 / 1000, 2)

    return round(volume, 1)


def volume_vn_nkt(dict_nkt):  # Внутренний объем одного погонного местра НКТ
    # print(dict_nkt)
    for nkt, lenght_nkt in dict_nkt.items():
        volume_vn_nkt = 0
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
                    FindIndexPZ.check_str_None(self, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
    return round(volume_rod, 5)


def volume_nkt(dict_nkt):  # Внутренний объем НКТ по фондовым НКТ
    volume_nkt = 0

    for nkt, length_nkt in dict_nkt.items():
        if nkt:
            volume_nkt += (float(nkt) - 2 * 7.6)**2 * 3.14 /4/1000000 * length_nkt
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
    # print(well_data.column_additional)
    if well_data.column_additional is False:
        # print(well_data.column_diametr._value, well_data.column_wall_thickness._value, current_bottom)
        volume_well = 3.14 * (
                well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000000 * (
                          current_bottom)

    else:
        # print(f' ghb [{well_data.column_additional_diametr._value, well_data.column_additional_wall_thickness._value}]')
        volume_well = (3.14 * (
                well_data.column_additional_diametr._value - well_data.column_additional_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                               current_bottom - float(well_data.head_column_additional._value)) / 1000) + (
                              3.14 * (
                              well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                                  float(well_data.head_column_additional._value)) / 1000)
    # print(f'Объем скважины {volume_well}')
    return round(volume_well, 1)


def volume_pod_NKT(self):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем

    nkt_l = round(sum(list(well_data.dict_nkt.values())), 1)
    if well_data.column_additional is False:
        v_pod_gno = 3.14 * (int(well_data.column_diametr._value) - int(
            well_data.column_wall_thickness._value) * 2) ** 2 / 4 / 1000 * (
                            float(well_data.current_bottom) - int(nkt_l)) / 1000

    elif round(sum(list(well_data.dict_nkt.values())), 1) > float(well_data.head_column_additional._value):
        v_pod_gno = 3.14 * (
                well_data.column_diametr._value - well_data.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                            float(well_data.head_column_additional._value) - nkt_l) / 1000 + 3.14 * (
                            well_data.column_additional_diametr._value - well_data.column_additional_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                            well_data.current_bottom - float(well_data.head_column_additional._value)) / 1000
    elif nkt_l <= float(well_data.head_column_additional._value):
        v_pod_gno = 3.14 * (
                well_data.column_additional_diametr._value - well_data.column_additional_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                            well_data.current_bottom - nkt_l) / 1000
    volume_in_nkt = v_pod_gno + volume_vn_nkt(well_data.dict_nkt) - volume_rod(self, well_data.dict_sucker_rod)
    # print(f'Внутренный объем + Зумпф{volume_in_nkt, v_pod_gno, volume_vn_nkt(well_data.dict_nkt)}, ')
    return round(volume_in_nkt, 1)


def volume_jamming_well(self, current_bottom):  # объем глушения скважины

    volume_jamming_well = round(
        (well_volume(self, current_bottom) - volume_nkt_metal(well_data.dict_nkt) - volume_rod(self,
                                                                                               well_data.dict_sucker_rod)) * 1.1,
        1)
    # print(f' объем глушения {well_volume(self, well_data.current_bottom), volume_jamming_well}')
    # print(f' объем {volume_nkt_metal(well_data.dict_nkt)} , {volume_rod(self, well_data.dict_sucker_rod)}')
    return volume_jamming_well

def well_jamming(self, without_damping, lift_key, volume_well_jaming):
    # print(f' выбранный {lift_key}')

    # print(f'расстояние ПВР {abs(sum(list(well_data.dict_nkt.values())) - well_data.perforation_roof), volume_jamming_well(self), volume_nkt_metal(well_data.dict_nkt), volume_rod(well_data.dict_sucker_rod)}')
    well_jamming_list2 = f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия  на последнем кубе глушения  жидкости ' \
                         f'уд.веса равной удельному весу ЖГ, дальнейшие промывки и удельный вес жидкостей промывок согласовать с Заказчиком,' \
                         f' при наличии Ризб - произвести замер, перерасчет ЖГ и повторное глушение с корректировкой удельного веса жидкости' \
                         f' глушения. В СЛУЧАЕ ОТСУТСТВИЯ ЦИРКУЛЯЦИИ ПРИ ГЛУШЕНИИ СКВАЖИНЫ, А ТАКЖЕ ПРИ ГАЗОВОМ ФАКТОРЕ БОЛЕЕ 200м3/сут ' \
                         f'ПРОИЗВЕСТИ ЗАМЕР СТАТИЧЕСКОГО УРОВНЯ В ТЕЧЕНИИ ЧАСА С ОТБИВКОЙ УРОВНЯ В СКВАЖИНЕ С ИНТЕРВАЛОМ 15 МИНУТ.' \
                         f'ПО РЕЗУЛЬТАТАМ ЗАМЕРОВ ПРИНИМАЕТСЯ РЕШЕНИЕ ОБ ПРОДОЛЖЕНИИ ОТБИВКИ УРОВНЯ В СКВАЖИНЕ ДО КРИТИЧЕСКОЙ ГЛУБИНЫ ЗА ' \
                         f'ПРОМЕЖУТОК ВРЕМЕНИ.'

    # print(f' Глушение {volume_jamming_well(self, well_data.current_bottom), volume_nkt_metal(well_data.dict_nkt), volume_rod(well_data.dict_sucker_rod)}')
    # print(well_data.well_volume_in_PZ)


    if without_damping is True:
        well_jamming_str = f'Скважина состоит в перечне скважин ООО Башнефть-Добыча, на которых допускается проведение ТКРС без предварительного глушения на текущий квартал'
        well_jamming_short = f'Скважина без предварительного глушения'
        well_jamming_list2 = f'В случае наличия избыточного давления необходимость повторного глушения скважины дополнительно согласовать со специалистами ПТО  и ЦДНГ.'
    elif without_damping is False and lift_key in ['НН с пакером', 'НВ с пакером', 'ЭЦН с пакером', 'ОРЗ']:

        well_after = f'Произвести закачку на поглощение не более {well_data.max_admissible_pressure._value}атм тех жидкости в ' \
                     f'объеме {round(volume_well_jaming - well_volume(self, sum(list(well_data.dict_nkt_po.values()))), 1)}м3.' if round(
            volume_well_jaming - well_volume(self, sum(list(well_data.dict_nkt_po.values()))), 1) > 0.1 else ''
        well_jamming_str = f'Произвести закачку в трубное пространство тех жидкости уд.весом {well_data.fluid_work} в ' \
                           f'объеме {round(well_volume(self, sum(list(well_data.dict_nkt.values()))) - volume_pod_NKT(self), 1)}м3 на циркуляцию. ' \
                           f'{well_after} Закрыть затрубное пространство. ' \
                           f' Закрыть скважину на  стабилизацию не менее 2 часов. (согласовать ' \
                           f'глушение в коллектор, в случае отсутствия на желобную емкость)'
        well_jamming_short = f'Глушение в НКТ уд.весом {well_data.fluid_work_short} ' \
                             f'объеме {round(well_volume(self, sum(list(well_data.dict_nkt.values()))) - volume_pod_NKT(self), 1)}м3 ' \
                             f'на циркуляцию. {well_after} '
    elif without_damping is False and lift_key in ['ОРД']:
        well_jamming_str = f'Произвести закачку в затрубное пространство тех жидкости уд.весом {well_data.fluid_work_short}в ' \
                           f'объеме {round(well_volume(self, well_data.current_bottom) - well_volume(self, well_data.depth_fond_paker_do["do"]), 1)}м3 ' \
                           f'на поглощение при давлении не более {well_data.max_admissible_pressure._value}атм. Закрыть ' \
                           f'затрубное пространство. Закрыть скважину на стабилизацию не менее 2 часов. (согласовать ' \
                           f'глушение в коллектор, в случае отсутствия на желобную емкость)'
        well_jamming_short = f'Глушение в затруб уд.весом {well_data.fluid_work_short} в ' \
                             f'объеме {round(well_volume(self, well_data.current_bottom) - well_volume(self, well_data.depth_fond_paker_do["do"]), 1)}м3 '
    elif abs(sum(list(well_data.dict_nkt.values())) - well_data.perforation_roof) > 150:
        well_jamming_str = f'Произвести глушение скважины прямой промывкой в объеме {volume_well_jaming}м3 тех ' \
                           f'жидкостью уд.весом {well_data.fluid_work}' \
                           f' на циркуляцию в следующим алгоритме: \n Произвести закачку в затрубное пространство ' \
                           f'тех жидкости в ' \
                           f'объеме {round(well_volume(self, sum(list(well_data.dict_nkt.values()))), 1)}м3 на ' \
                           f'циркуляцию. Закрыть трубное пространство. ' \
                           f'Произвести закачку на поглощение не более {well_data.max_admissible_pressure._value}атм ' \
                           f'тех жидкости в ' \
                           f'объеме {round(volume_well_jaming - well_volume(self, sum(list(well_data.dict_nkt.values()))), 1)}м3. Закрыть скважину на ' \
                           f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае ' \
                           f'отсутствия на желобную емкость'
        well_jamming_short = f'Глушение в затруб в объеме {volume_well_jaming}м3 тех ' \
                             f'жидкостью уд.весом {well_data.fluid_work_short}'
    elif abs(sum(list(well_data.dict_nkt.values())) - well_data.perforation_roof) <= 150:
        well_jamming_str = f'Произвести глушение скважины прямой промывкой в объеме {volume_well_jaming}м3 тех ' \
                           f'жидкостью уд.весом {well_data.fluid_work}' \
                           f' на циркуляцию. Закрыть скважину на ' \
                           f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае отсутствия ' \
                           f'на желобную емкость)'
        well_jamming_short = f'Глушение в затруб в объеме {volume_well_jaming}м3 уд.весом {well_data.fluid_work_short}'

        # print([well_jamming_str, well_jamming_list2, well_jamming_short])
    return [well_jamming_str, well_jamming_list2, well_jamming_short]

def is_number(num):
    if num is None:
        return 0
    try:
        float(str(num).replace(",", "."))
        return True
    except ValueError or TypeError:
        return False



def open_checkbox_dialog():
    dialog = CheckBoxDialog()
    dialog.exec_()




# Определение трех режимов давлений при определении приемистости
def pressure_mode(mode, plast):


    mode = float(mode) / 10 * 10
    if mode > well_data.max_admissible_pressure._value and (plast != 'D2ps' or plast.lower() != 'дпаш'):
        mode_str = f'{float(mode)}, {float(mode)-10}, {float(mode)-20}'
    elif (plast == 'D2ps' or plast.lower() == 'дпаш') and well_data.region == 'ИГМ':
        mode_str = f'{120}, {140}, {160}'
    else:
        mode_str = f'{float(mode)-10}, {float(mode)}, {float(mode) + 10}'
    return mode_str

