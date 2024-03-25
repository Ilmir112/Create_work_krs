from PyQt5.QtWidgets import QInputDialog, QMessageBox

import H2S
import well_data
from work_py.acids_work import pressure_mode
from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm, well_volume_norm


def kot_select(self):


    if well_data.column_additional == False \
            or (well_data.column_additional == True and well_data.current_bottom <= well_data.head_column_additional._value):
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{well_data.nkt_diam}мм 10м + репер '

    elif well_data.column_additional == True and well_data.column_additional_diametr._value < 110 and\
            well_data.current_bottom >= well_data.head_column_additional._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{60}мм 10м + репер + ' \
                     f'НКТ60мм L- {round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м'
    elif well_data.column_additional == True and well_data.column_additional_diametr._value > 110 and\
            well_data.current_bottom >= well_data.head_column_additional._value:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{73}мм со снятыми фасками 10м + репер + ' \
                     f'НКТ{well_data.nkt_diam}мм со снятыми фасками' \
                     f' L- {round(well_data.current_bottom - well_data.head_column_additional._value, 0)}м'

    return kot_select


def kot_work(self, current_bottom):

    current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                         'Введите забой до которого нужно нормализовать',
                                                         float(current_bottom))

    kot_list = [[f'статической уровень {well_data.static_level._value}', None,
                 f'При отсутствии циркуляции:\n'
                 f'Спустить {kot_select(self)} на НКТ{well_data.nkt_diam}мм до глубины {well_data.current_bottom}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
                [f'{kot_select(self)} до H-{current_bottom} закачкой обратной промывкой', None,
                 f'Произвести очистку забоя скважины до гл.{current_bottom}м закачкой обратной промывкой тех '
                 f'жидкости уд.весом {well_data.fluid_work}, по согласованию с Заказчиком',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [None, None,
                 f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', None],

                [None, None,
                 f'Поднять {kot_select(self)} на НКТ{well_data.nkt_diam}мм c глубины {current_bottom}м с доливом '
                 f'скважины в '
                 f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1)]
                ]
    well_data.current_bottom = current_bottom
    return kot_list


def fluid_change(self):

    from krs import well_volume

    well_data.fluid_work, well_data.fluid_work_short, plast, expected_pressure = check_h2s(self)

    fluid_change_list = [[f'Cмена объема {well_data.fluid}г/см3- {round(well_volume(self, well_data.current_bottom), 1)}м3' ,
                          None,
                          f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {well_data.fluid_work} '
                          f'(по расчету по вскрываемому пласта Рожид- {expected_pressure}атм) в объеме не '
                          f'менее {round(well_volume(self, well_data.current_bottom), 1)}м3  в присутствии '
                          f'представителя заказчика, Составить акт. '
                          f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
                          f'2 часа до начала работ)',
                          None, None, None, None, None, None, None,
                          'мастер КРС', well_volume_norm(well_volume(self, well_data.current_bottom))]]

    return fluid_change_list

def check_h2s(self):


    cat_H2S_list = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                  well_data.plast_work if well_data.dict_category.get(plast) and
                                  well_data.dict_category[plast]['отключение'] == 'рабочий']))
    H2S_mg = list(map(int, [well_data.dict_category[plast]['по сероводороду'].data_mg_l for plast in
                                  well_data.plast_work if  well_data.dict_category.get(plast) and
                                  well_data.dict_category[plast]['отключение'] == 'рабочий']))
    H2S_pr = list(map(int, [well_data.dict_category[plast]['по сероводороду'].data_procent for plast in
                                  well_data.plast_work if  well_data.dict_category.get(plast) and
                                  well_data.dict_category[plast]['отключение'] == 'рабочий']))

    if len(well_data.dict_perforation_project) != 0:
        plast, ok = QInputDialog.getItem(self, 'выбор пласта для расчета ЖГС ', 'выбирете пласт для перфорации',
                                         well_data.plast_project, -1, False)
        try:
            fluid_new = well_data.dict_perforation_project[plast]['рабочая жидкость']
            fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                   'Введите значение удельного веса жидкости', fluid_new, 1, 1.72, 2)
        except:
            fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                   'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        try:
            expected_pressure = list(well_data.dict_perforation_project[plast]['давление'])[0]

            expected_pressure, ok = QInputDialog.getDouble(None, 'Ожидаемое давление по пласту',
                                                           'Введите Ожидаемое давление по пласту',
                                                           expected_pressure, 0, 300, 1)

        except:
            mes = QMessageBox.warning(self, 'Ошибка', 'ошибка в определении планового пластового давления')
            expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                           'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
    else:
        plast, ok = QInputDialog.getText(self, 'выбор пласта для расчета ЖГС ', 'введите пласт для перфорации')

    try:
        print()
        print(well_data.dict_category)
        cat_H2S_list_plan = list(map(float,
                                     [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                      well_data.plast_project]))
    except:

        cat_H2S_list_plan_int, ok = QInputDialog.getInt(self, 'Категория',
                                                         'Введите категорию скважины по H2S на вскрываемый пласт',
                                                         2,
                                                         1, 3)
        cat_H2S_list_plan = []
        cat_H2S_list_plan.append(cat_H2S_list_plan_int)
        H2S_pr_plan_int, ok = QInputDialog.getDouble(self,
                                                      'Сероводород', 'Введите содержание сероводорода в %', 50, 0,
                                                      1000, 2)
        H2S_pr_plan_plan = []
        H2S_pr_plan_plan.append(H2S_pr_plan_int)
        H2S_mg_plan_int, ok = QInputDialog.getDouble(self, 'Сероводород',
                                                      'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
        H2S_mg_plan = []
        H2S_mg_plan.append(H2S_mg_plan_int)


    if len(cat_H2S_list) != 0:
        fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                               'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                       'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
        if cat_H2S_list_plan[0] in [1, 2] and len(well_data.plast_work) == 0:
            expenditure_h2s = round(max([well_data.dict_category[plast]['по сероводороду'].poglot for plast in well_data.plast_project]), 3)
            well_data.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {expenditure_h2s}кг/м3 '


        elif ((cat_H2S_list_plan[0] in [1, 2]) or (cat_H2S_list[0] in [1, 2])) and len(well_data.plast_work) != 0:
            expenditure_h2s_plan = max(
                [well_data.dict_category[well_data.plast_work[0]]['по сероводороду'].poglot for plast in well_data.plast_project])
            expenditure_h2s = max(
                [well_data.dict_category[well_data.plast_work[0]]['по сероводороду'].poglot])
            expenditure_h2s = round(max([expenditure_h2s, expenditure_h2s_plan]), 1)

            well_data.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {expenditure_h2s}кг/м3 '
        else:
            try:
                well_data.fluid_work = f'{fluid_new}г/см3 '
            except:

                expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                               'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)

    else:
        fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                               'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                       'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
        if cat_H2S_list_plan[0] in [1, 2]:


            expenditure_h2s = round(
                max([well_data.dict_category[plast]['по сероводороду'].poglot for plast in well_data.plast_project]), 3)
            well_data.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                    f'расчета {expenditure_h2s}кг/м3 '

        else:
            well_data.fluid_work = f'{fluid_new}г/см3 '

    return (well_data.fluid_work, well_data.fluid_work_short, plast, expected_pressure)

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

    definition_Q_list = [[f'Насыщение 5м3 определение Q при {pressure_mode(well_data.expected_P, "пласт")}', None,
                           f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                           f' на приемистость в трех режимах при Р={pressure_mode(well_data.expected_P, "пласт")}атм в '
                           f'присутствии представителя ЦДНГ. '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до '
                           f'начала работ). ',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 0.17+0.2+0.2+0.2+0.15+0.52]]
    return definition_Q_list

def definition_Q_nek(self):

    from work_py.acids_work import open_checkbox_dialog

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

def pvo_cat1(self):


    pvo_1 = f'Установить ПВО  по  схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г ' \
            f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f' (при необходимости произвести монтаж переводника' \
            f' П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
            f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до ' \
            f'концевых задвижек на Р-{well_data.max_admissible_pressure._value}атм ' \
            f'(на максимально допустимое давление опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. Опрессовать ' \
            f'выкидную линию после концевых задвижек на ' \
            f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на' \
            f'давление до 210 кгс/см2 ((21 МПа)\n' \
            f'- Обеспечить о обогрев превентора, станции управления ПВО оборудовать теплоизоляционными ' \
            f'материалом в зимней период. \n Получить разрешение на производство работ в присутствии представителя ПФС'

    pvo_list = [[None, None,
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
