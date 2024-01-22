from PyQt5.QtWidgets import QInputDialog, QMessageBox

from krs import well_volume
from work_py.acids_work import pressure_mode
from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm, well_volume_norm


def kot_select(self):
    from open_pz import CreatePZ
    
    if CreatePZ.column_additional == False \
            or (CreatePZ.column_additional == True and CreatePZ.current_bottom <= CreatePZ.head_column_additional):
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{CreatePZ.nkt_diam}мм 10м + репер '

    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and\
            CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{60}мм 10м + репер + ' \
                     f'НКТ60мм L- {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and\
            CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{73}мм со снятыми фасками 10м + репер + ' \
                     f'НКТ{CreatePZ.nkt_diam}мм со снятыми фасками' \
                     f' L- {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м'

    return kot_select


def kot_work(self):
    from open_pz import CreatePZ
    current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                         'Введите забой до которого нужно нормализовать',
                                                         float(CreatePZ.current_bottom))

    kot_list = [[f'Нст {CreatePZ.static_level}', None,
                 f'При отсутствии циркуляции при указанном статическом уровне в ПЗ {CreatePZ.static_level}м:\n'
                 f'Спустить {kot_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м'
                 f' с замером, шаблонированием шаблоном.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1)],
                [f'{kot_select(self)} до H-{current_bottom}', None,
                 f'Произвести очистку забоя скважины до гл.{current_bottom}м закачкой обратной промывкой тех '
                 f'жидкости уд.весом {CreatePZ.fluid_work}, по согласованию с Заказчиком',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [None, None,
                 f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', None],

                [None, None,
                 f'Поднять {kot_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {current_bottom}м с доливом '
                 f'скважины в '
                 f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1)]
                ]
    CreatePZ.current_bottom = current_bottom
    return kot_list


def fluid_change(self):
    from open_pz import CreatePZ
    import H2S
    expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                   'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
    fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                           'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
    CreatePZ.fluid = fluid_new
    try:
        CreatePZ.fluid_work = check_h2s(self, fluid_new)

    except:
        print(CreatePZ.cat_H2S_list, CreatePZ.H2S_mg, CreatePZ.H2S_pr)
        CreatePZ.H2S_mg = CreatePZ.H2S_mg[:1]
        print()
        CreatePZ.H2S_pr = CreatePZ.H2S_pr[:1]
        CreatePZ.cat_H2S_list = CreatePZ.cat_H2S_list[:1]
        print(CreatePZ.cat_H2S_list, CreatePZ.H2S_mg, CreatePZ.H2S_pr)
        cat_H2S = QInputDialog.getInt(self, 'Сероводород',
                                        'Введите Категорию скважины по сероводороду по вскрываемому пласту', 2, 1, 3)
        while cat_H2S in [1, 2, 3]:
            mes = QMessageBox.warning(self, 'Некорретные данные', 'Введены не корректноые данные')
            cat_H2S = QInputDialog.getDouble(self, 'Сероводород',
                                                  'Введите Категорию скважины по сероводороду по вскрываемому пласту',
                                                  50, 0, 1000, 2)
        CreatePZ.cat_H2S_list.append(cat_H2S[0])
        if cat_H2S != 3:
            H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                            'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
            while H2S_mg in [int, float]:
                mes = QMessageBox.warning(self, 'Некорретные данные', 'Введены не корректноые данные')
                H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                                'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)

            CreatePZ.H2S_mg.append(H2S_mg[0])
            H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                            'Введите содержание сероводорода в %', 0.5, 0, 1000, 6)
            while H2S_pr in [int, float]:
                mes = QMessageBox.warning(self, 'Некорретные данные', 'Введены не корректные данные')
                H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                'Введите содержание сероводорода в %', 0.5, 0, 1000, 6)

            CreatePZ.H2S_pr.append(H2S_pr[0])
        print(f' после добавления {CreatePZ.cat_H2S_list, CreatePZ.H2S_mg, CreatePZ.H2S_pr}')
        CreatePZ.fluid_work = check_h2s(self, fluid_new)





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
    return fluid_change_list

def check_h2s(self, fluid_new):
    from open_pz import CreatePZ
    from H2S import calv_h2s

    if len(CreatePZ.plast_work) == 0 and len(CreatePZ.cat_H2S_list) > 1:
        if 3 != str(CreatePZ.cat_H2S_list[1]):
            fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {calv_h2s(self, CreatePZ.cat_H2S_list[1], CreatePZ.H2S_mg[1], CreatePZ.H2S_pr[1])}кг/м3 '
        else:
            fluid_work = f'{fluid_new}г/см3 '
    else:
        if len(CreatePZ.cat_H2S_list) > 1:


            if ('2' in str(CreatePZ.cat_H2S_list[1]) or '1' in str(CreatePZ.cat_H2S_list[1])) and (
                    '2' not in str(CreatePZ.cat_H2S_list[0]) or '1' not in str(CreatePZ.cat_H2S_list[0])):
                fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                      f'расчета {calv_h2s(self, CreatePZ.cat_H2S_list[1], CreatePZ.H2S_mg[1], CreatePZ.H2S_pr[1])}кг/м3 '
            elif ('2' in str(CreatePZ.cat_H2S_list[0]) or '1' in str(CreatePZ.cat_H2S_list[0])) and (
                    '2' not in str(CreatePZ.cat_H2S_list[1]) or '1' not in str(CreatePZ.cat_H2S_list[1])):
                fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                      f'расчета {calv_h2s(self, CreatePZ.cat_H2S_list[0], CreatePZ.H2S_mg[0], CreatePZ.H2S_pr[0])}кг/м3 '
            else:
                fluid_work = f'{fluid_new}г/см3 '
        else:
            if ('2' in str(CreatePZ.cat_H2S_list[0]) or '1' in str(CreatePZ.cat_H2S_list[0])):
                fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                      f'расчета {calv_h2s(self, CreatePZ.cat_H2S_list[0], CreatePZ.H2S_mg[0], CreatePZ.H2S_pr[0])}кг/м3 '

            else:
                fluid_work = f'{fluid_new}г/см3 '
    return fluid_work

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
    from open_pz import CreatePZ
    definition_Q_list = [[f'Насыщение 5м3 Q-{pressure_mode(CreatePZ.expected_P, "пласт")}', None,
                           f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                           f' на приемистость в трех режимах при Р={pressure_mode(CreatePZ.expected_P, "пласт")}атм в '
                           f'присутствии представителя ЦДНГ. '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до '
                           f'начала работ). ',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 0.17+0.2+0.2+0.2+0.15+0.52]]
    return definition_Q_list

def definition_Q_nek(self):
    from open_pz import CreatePZ
    from work_py.acids_work import open_checkbox_dialog

    open_checkbox_dialog()
    plast = CreatePZ.plast_select
    definition_Q_list = [[f'Насыщение 5м3 Q-{plast} при {CreatePZ.max_expected_pressure}', None,
                           f'Произвести насыщение скважины по затрубу до стабилизации давления закачки не '
                           f'менее 5м3. Опробовать  '
                           f' на приемистость {plast} при Р={CreatePZ.max_expected_pressure}атм в присутствии '
                           f'представителя ЦДНГ. '
                           f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
                           f'с подтверждением за 2 часа до '
                           f'начала работ). ',
                           None, None, None, None, None, None, None,
                           'мастер КРС', 0.17+0.2+0.2+0.2+0.15+0.52]]

    return definition_Q_list
def privyazkaNKT(self):
    priv_list = [[f'Привязка ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
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
    from open_pz import CreatePZ
    pvo_1 = f'Установить ПВО  по  схеме №1 утвержденной главным инженером ООО "Ойл-сервис" от 14.10.2021г  (тип ' \
            f'плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f'блока дросселирования -БД 65х21, блок-глушения БГ 65х21 находится на ' \
            f'базе БПО, если расстояние от БПО до ремонтируемой скважины составляет менее 150км (при необходимости ' \
            f'произвести монтаж переводника П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки) и спустить и посадить пакер на ' \
            f'глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до ' \
            f'концевых задвижек на Р-{CreatePZ.max_expected_pressure}атм (на максимально ожидаемое давление на устье, ' \
            f'но не выше максимально допустимого давления опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. ' \
            f'В случае невозможности опрессовки по ' \
            f'результатам определения приемистости и по согласованию с ' \
            f'заказчиком  опрессовать трубные плашки ПВО на давление поглощения, но не менее 30атм. Опрессовать ' \
            f'выкидную линию после концевых задвижек на ' \
            f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на давление ' \
            f'до 210 кгс/см2 ((21 МПа)'
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
    [f'монтаж ПВО по схеме № 1', None,
     pvo_1, None, None,
     None, None, None, None, None,
     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком',  4.67]]
    CreatePZ.kat_pvo = 1
    return pvo_list
