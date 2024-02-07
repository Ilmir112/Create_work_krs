from PyQt5.QtWidgets import QInputDialog, QMessageBox

import math
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from work_py.alone_oreration import kot_work


def well_volume():
    from open_pz import CreatePZ
    # print(CreatePZ.column_additional)
    if not CreatePZ.column_additional:

        volume_well = 3.14 * (CreatePZ.column_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000000 * (
            CreatePZ.current_bottom)
        return volume_well
    else:
        volume_well = (3.14 * (
                CreatePZ.column_additional_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000 * (
                               CreatePZ.current_bottom - float(CreatePZ.head_column_additional)) / 1000) + (
                              3.14 * (CreatePZ.column_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000 * (
                          CreatePZ.head_column_additional) / 1000)
        return volume_well


template_second_diam_dict = {
    84: (88, 92),
    90: (92.1, 97),
    94: (97.1, 102),
    102: (102.1, 109),
    106: (109, 115),
    114: (118, 120),
    116: (120.1, 121.9),
    118: (122, 123.9),
    120: (124, 127.9),
    124: (128, 133),
    140: (144, 148),
    144: (148.1, 154),
    152: (154.1, 164),
    164: (166, 176),
    190: (190.6, 203.6),
    210: (215, 221)
}


def template_diam_ek():
    from open_pz import CreatePZ
    global template_second_diam_dict
    diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness

    template_first_diam_dict = {
        80: (88, 97),
        89: (97.1, 102),
        92: (102.1, 120),
        112: (120.1, 121.9),
        114: (122, 133),
        118: (144, 221)
    }
    # определение диаметра  шаблонов первого и второго
    for diam, diam_internal in template_second_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
            template_second_diam = diam
    for diam, diam_internal in template_first_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
            template_first_diam = diam
    return (template_first_diam, template_second_diam)


def template_diam_additional_ek():  # Выбор диаметра шаблонов при наличии в скважине дополнительной колонны
    from open_pz import CreatePZ
    diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
    diam_internal_ek_addition = float(CreatePZ.column_additional_diametr) - 2 * float(
        CreatePZ.column_additional_wall_thickness)
    global template_second_diam_dict

    for diam, diam_internal in template_second_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
            template_second_diam = diam
    for diam, diam_internal in template_second_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1]:
            # print(diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1], diam_internal[0],diam_internal_ek_addition,diam_internal[1])
            template_first_diam = diam
    return (template_first_diam, template_second_diam)


def template_ek_without_skm(self):
    from open_pz import CreatePZ

    roof_plast, roof_add_column_plast = definition_roof_not_raiding(self) # кровля отрайбированных интервалов перфорции

    length_template_addition = int(''.join(['30' if CreatePZ.lift_ecn_can_addition is True else '2']))
    first_template = template_diam_ek()[0]
    second_template = template_diam_ek()[1]
    if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
        second_template = 126
    second_template, ok = QInputDialog.getInt(None, 'Диаметр шаблон',
                                              f'диаметр шаблона',
                                              int(second_template), 70,
                                              200)
    if CreatePZ.column_additional is False and float(CreatePZ.shoe_column) < float(CreatePZ.current_bottom):
        CreatePZ.open_trunk_well = True


    elif CreatePZ.column_additional is True and float(CreatePZ.shoe_column_additional) < float(
            CreatePZ.current_bottom):
        CreatePZ.open_trunk_well = True

    if CreatePZ.column_additional is True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr < 110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

    lift_ecn_can = {True: 30, False: 4}
    # print(f' кровля ПВР {CreatePZ.perforation_roof}')
    # print(CreatePZ.dict_perforation)
    CreatePZ.nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    if CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:

        template_str = f'перо + шаблон-{first_template}мм L-2м + НКТ{CreatePZ.nkt_diam}мм ' \
                       f'{int(CreatePZ.current_bottom - math.ceil(roof_plast))}м ' \
                       f'+  НКТ{CreatePZ.nkt_diam}мм + шаблон-{second_template}мм' \
                       f' L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон-{second_template}мм до гл.{math.ceil(roof_plast)}м)'
        CreatePZ.template_depth = math.ceil(roof_plast - 8)
    elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
        template_str = f'фильтр-направление L-2м + НКТ{CreatePZ.nkt_diam}мм ' \
                       f'{math.ceil(CreatePZ.current_bottom - roof_plast + 8)}м' \
                       f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{second_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон-{second_template}мм до гл.{math.ceil(roof_plast - 8)}м)'
        CreatePZ.template_depth = math.ceil(roof_plast - 8)
    elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is True:
        template_str = f'перо + шаблон-{second_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м + ' \
                       f'НКТ{CreatePZ.nkt_diam}мм 10м + репер'
        ckm_teml = f'шаблон-{second_template}мм до гл.{math.ceil(CreatePZ.current_bottom)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom)
    elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
        template_str = f'обточная муфта + НКТ{nkt_pod}мм ' \
                       f'{math.ceil(CreatePZ.current_bottom - math.ceil(roof_add_column_plast - 10))}м +' \
                       f' шаблон-{first_template}мм L-{length_template_addition}м + НКТ{nkt_pod}мм' \
                       f' {math.ceil(roof_add_column_plast - float(CreatePZ.head_column_additional) - 20 - length_template_addition)}м ' \
                       f' + НКТ{CreatePZ.nkt_diam} {CreatePZ.head_column_additional-roof_plast}м + шаблон-{second_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(шаблон-{first_template}мм до гл.{math.ceil(roof_add_column_plast - 10)}м, ' \
                   f'шаблон-{first_template}мм до гл.{CreatePZ.head_column_additional - 10}м)'
        CreatePZ.template_depth = math.ceil(roof_plast)
        CreatePZ.template_depth_addition = math.ceil(roof_add_column_plast - 8)

    elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
        template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {math.ceil(CreatePZ.current_bottom - math.ceil(roof_add_column_plast) + 8)}м ' \
                       f'шаблон-{first_template}мм L-{length_template_addition} + {math.ceil(roof_add_column_plast) + 8 - float(CreatePZ.head_column_additional) - length_template_addition - 6}' \
                       f'+ шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(шаблон-{first_template}мм до {math.ceil(roof_add_column_plast) - 10}м, шаблон Ф-{template_diam_additional_ek()[1]}мм до гл.{CreatePZ.head_column_additional - 10}м)'
        CreatePZ.template_depth_addition = math.ceil(roof_add_column_plast - 8)
        CreatePZ.template_depth = math.ceil(roof_plast - 8)
    elif CreatePZ.column_additional is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is True:
        template_str = f'обточная муфта + шаблон-{first_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can_addition]}м + НКТ{nkt_pod} ' \
                       f'{round(CreatePZ.current_bottom - roof_plast, 0)}м + шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(шаблон-{first_template}мм до гл.{math.ceil(CreatePZ.current_bottom)}м, шаблон-{template_diam_additional_ek()[1]}мм' \
                   f' до глубины {round(CreatePZ.current_bottom - lift_ecn_can[CreatePZ.lift_ecn_can_addition] - (CreatePZ.current_bottom - CreatePZ.head_column_additional), 0)}м'
        # print(f' шаблонирование {math.ceil(CreatePZ.current_bottom - 10)}')
        CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - 10)

        CreatePZ.template_depth = math.ceil(CreatePZ.head_column_additional - 8)


    list_template_ek = [
        [None, None,
         f'Спустить  {template_str}на 'f'НКТ{CreatePZ.nkt_diam}мм {ckm_teml} с замером, шаблонированием НКТ. \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1.2)],

        [None, None,
         f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
         f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
         f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
         f'в объеме {round(3 * CreatePZ.current_bottom / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
         f'пространство. Реагирование 2 часа.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 4],
        [f'Нормализовать до глубины {CreatePZ.current_bottom}м.',
         None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                     f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None,
         None, None,
         'Мастер КРС', None],
        [f'Промыть в объеме {round(well_volume() * 1.5, 1)}м3',
         None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume() * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', well_volume_norm(well_volume() * 1.5)],
        [f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя',
         None,
         f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, при '
         f'необходимости повторная промывка.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 2.49],
        [None, None,
         f'Поднять {template_str} на НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
         f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1.2)]
    ]
    if CreatePZ.column_additional is False:
        temlate_ek = second_template
    else:
        temlate_ek = first_template

    notes_list = [[None, None,
                   f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного двигателя с райбером d={temlate_ek + 1}мм, '
                   f'{temlate_ek - 1}мм, {temlate_ek - 3}мм, {temlate_ek - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до гл.{CreatePZ.current_bottom}м с последующим'
                   f' СПО шаблона {temlate_ek}мм на ТНКТ под промывку скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
                   f'на ТНКТ с гл. {CreatePZ.current_bottom}м вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в '
                   f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 ',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, None],
                  [None, None,
                   f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с долотом {temlate_ek};'
                   f' {temlate_ek - 2}; {temlate_ek - 4}мм  фрезера-{temlate_ek}мм, райбера-{temlate_ek + 1}мм и другого оборудования и '
                   f'инструмента, (при необходимости  ловильного), при необходимости на СБТ для восстановления проходимости ствола  '
                   f'и забоя скважины с применением мех.ротора, до текущего забоя с последующей нормализацией до планового '
                   f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{CreatePZ.current_bottom}м вести с доливом '
                   f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС',
                   None],
                  [None, None,
                   f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию №2 произвести '
                   f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м вести с '
                   f'доливом скважины до устья т/ж удел.весом с доливом c'
                   f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None],

                  [None, None,
                   f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 или КОС до планового '
                   f'текущего забоя. СПО КОТ-50 или КОС повторить до полной нормализации. При жесткой посадке  '
                   f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
                   f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
                  [None, None,
                   f'Примечание №5: В случае необходимости по результатам восстановления проходимости экплуатационной колонны '
                   f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
                   f'проходимость. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
                   f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

    privyazka_nkt = [f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины. По привязому НКТ '
                     f'удостовериться в наличии', None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис".'
                     f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины. По привязому НКТ удостовериться в наличии'
                     f'текущего забоя с плановым, при необходимости нормализовать забой обратной промывкой тех жидкостью '
                     f'уд.весом {CreatePZ.fluid_work}   до глубины {CreatePZ.current_bottom}м',
                     None, None, None, None, None, None, None, 'Мастер КРС', 4, None]

    if CreatePZ.current_bottom - CreatePZ.perforation_sole <= 10 and CreatePZ.open_trunk_well is False:
        privyazka_question = QMessageBox.question(self, 'Привязка оборудования',
                                                  f'зумпф составляет {int(CreatePZ.current_bottom - CreatePZ.perforation_sole)}м '
                                                  f'нужно ли привязывать компоновку?'
                                                  )
        if privyazka_question == QMessageBox.StandardButton.Yes:
            list_template_ek.insert(-1, privyazka_nkt)

    if float(CreatePZ.static_level) > 700:
        kot_question = QMessageBox.question(self, 'Низкий Статический уровень', 'Нужно ли произвести СПО '
                                                                                'обратных клапанов перед ПСШ?')
        if kot_question == QMessageBox.StandardButton.Yes:
            for row in kot_work(self)[::-1]:
                list_template_ek.insert(0, row)

    if CreatePZ.gipsInWell is True:
        gips = pero(self)
        for row in gips[::-1]:
            list_template_ek.insert(0, row)




    if CreatePZ.count_template == 0:
        list_template_ek = list_template_ek + notes_list
        CreatePZ.count_template += 1
    else:
        list_template_ek = list_template_ek
        list_template_ek.pop(1)
    return list_template_ek


def template_ek(self):
    from open_pz import CreatePZ
    from work_py.advanted_file import skm_interval, raid

    roof_plast, roof_add_column_plast = definition_roof_not_raiding(self)

    if CreatePZ.column_additional is True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr < 110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

        # temlate_ek = template_ek()
    else:
        nkt_pod = '60'
        template_ek = template_diam_ek()

    lift_ecn_can = {True: 30, False: 4}
    liftEcn = lift_ecn_can[CreatePZ.lift_ecn_can]

    if CreatePZ.column_additional is False and float(CreatePZ.shoe_column) < float(CreatePZ.current_bottom):
        CreatePZ.open_trunk_well = True
        # print(CreatePZ.column_additional is False and float(CreatePZ.shoe_column), float(CreatePZ.current_bottom),
        #       CreatePZ.column_additional is False and float(CreatePZ.shoe_column) < float(CreatePZ.current_bottom))

    elif CreatePZ.column_additional is True and float(CreatePZ.shoe_column_additional) < float(
            CreatePZ.current_bottom):
        CreatePZ.open_trunk_well = True

    if CreatePZ.column_additional is False or (
            CreatePZ.column_additional is True and CreatePZ.head_column_additional >= CreatePZ.current_bottom):
        first_template = template_diam_ek()[0]
        second_template = template_diam_ek()[1]
        # print(f'нижний шаблон {first_template}')
    else:
        first_template = template_diam_additional_ek()[0]
        second_template = template_diam_additional_ek()[1]
    if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
        second_template = 126

    second_template, ok = QInputDialog.getInt(None, 'Диаметр шаблона',
                                              f'диаметр шаблона для вверхнего колонны',
                                              int(second_template), 70,
                                              200)
    first_template, ok = QInputDialog.getInt(None, 'Диаметр шаблона для доп колонны',
                                             f'диаметр шаблона для Нижнего шаблона колонны',
                                             int(first_template), 70,
                                             200)
    ckm_teml_SKM_EK, ckm_teml_SKM_EK_open, ckm_teml_SKM_EK_without, ckm_teml_SKM_DP_EK, \
    ckm_teml_SKM_DP, ckm_teml_SKM_DP_without,\
    ckm_teml_SKM_DP_open, ckm_teml_SKM_EK_open_True = 0, 0, 0, 0, 0, 0, 0, 0

    roof_skm = 0
    # print(f'отрайбировани {[CreatePZ.dict_perforation[plast]["отрайбировано"] for plast in CreatePZ.plast_work]}')
    CreatePZ.nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    length_template_addition = int(''.join(['30' if CreatePZ.lift_ecn_can_addition is True else '2']))
    # print(f' кровля перфорации {int(CreatePZ.current_bottom),int(CreatePZ.shoe_column), 8}')
    template_SKM_EK = f'перо + шаблон-{first_template}мм L-2м + НКТ{CreatePZ.nkt_diam}мм ' \
                      f'{int(CreatePZ.current_bottom - roof_plast + 8)}м ' \
                      f'+ СКМ-{int(CreatePZ.column_diametr)} +10м НКТ{CreatePZ.nkt_diam}мм + ' \
                      f'шаблон-{second_template}мм L-{liftEcn}м '

    template_SKM_EK_open = f'фильтр-направление L-2м + НКТ{CreatePZ.nkt_diam}мм ' \
                           f'{int(CreatePZ.current_bottom) - roof_plast + 8}м' \
                           f'+ СКМ-{int(CreatePZ.column_diametr)} + 10м ' \
                           f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{second_template}мм L-{liftEcn}м '
    template_SKM_EK_open_true = f'фильтр-направление L-2м + НКТ{CreatePZ.nkt_diam}мм ' \
                           f'{int(CreatePZ.current_bottom) - int(roof_plast) + 8}м' \
                           f'+ СКМ-{int(CreatePZ.column_diametr)} + 10м ' \
                           f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{second_template}мм L-{liftEcn}м '

    template_SKM_EK_without = f'перо + СКМ-{int(CreatePZ.column_diametr)} + 10м ' \
                              f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{second_template}мм L-{liftEcn}м '

    template_SKM_DP_EK = f'обточная муфта  + {round(CreatePZ.current_bottom - roof_add_column_plast + 10, 0)}м ' \
                         f'НКТ{nkt_pod} + шаблон-{first_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can_addition]}м + ' \
                         f'НКТ{nkt_pod} ' \
                         f'{round(float(CreatePZ.current_bottom) - float(CreatePZ.head_column_additional) - lift_ecn_can[CreatePZ.lift_ecn_can_addition] - (float(CreatePZ.current_bottom) - roof_add_column_plast + 10), 0)}м ' \
                         f'+ НКТ{CreatePZ.nkt_diam} {CreatePZ.head_column_additional - roof_plast +10}м + СКМ + шаблон-{second_template}мм L-{liftEcn}м '

    template_SKM_DP = f'обточная муфта + НКТ{nkt_pod} {int(CreatePZ.current_bottom) - math.ceil(roof_add_column_plast) + 10}м ' \
                      f'+ СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + шаблон-{first_template}мм ' \
                      f'L-{length_template_addition}м' \
                      f' + НКТ{nkt_pod} {math.ceil(roof_add_column_plast - 10 - length_template_addition - float(CreatePZ.head_column_additional))}м + ' \
                      f'+ НКТ{CreatePZ.nkt_diam} {CreatePZ.head_column_additional - roof_plast}м'+\
                      f'шаблон-{second_template}мм L-{liftEcn}м '

    template_SKM_DP_open = f'фильтр направление L-2м + НКТ{nkt_pod} {math.ceil(CreatePZ.current_bottom - roof_add_column_plast + 10)}м ' \
                           f'+ СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + ' \
                           f'шаблон-{first_template}мм L-{length_template_addition}м' \
                           f' + НКТ{nkt_pod} {int(CreatePZ.current_bottom - (int(CreatePZ.current_bottom - roof_add_column_plast + 10)) - 13 - length_template_addition - float(CreatePZ.head_column_additional) + 10)}м' \
                           f'+ НКТ{CreatePZ.nkt_diam} {CreatePZ.head_column_additional - roof_plast +10}м +  шаблон-{second_template}мм L-{liftEcn}м '


    template_SKM_DP_without = f'обточная муфта + СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + ' \
                              f'шаблон-{first_template}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can_addition]}м + НКТ{nkt_pod} ' \
                              f'{round(CreatePZ.current_bottom - float(CreatePZ.head_column_additional) - 10, 0)}м + ' \
                              f'НКТ{CreatePZ.nkt_diam} {CreatePZ.head_column_additional - roof_plast +10}м + шаблон-{second_template}мм L-{liftEcn}м '


    if (CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False) or \
            (CreatePZ.column_additional is True and float(CreatePZ.current_bottom) <= float(
                CreatePZ.head_column_additional) and all(
                [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False):
        template_str = template_SKM_EK

        CreatePZ.template_depth = math.ceil(int(roof_plast - 20))
        ckm_teml_SKM_EK = f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м)'
        template_key = 'ПСШ ЭК'

    elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:

        CreatePZ.template_depth = int(int(roof_plast - 20))
        template_str = template_SKM_EK_open
        ckm_teml_SKM_EK_open = f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м)'
        template_key = 'ПСШ открытый ствол'
        print(f'ключ {template_key}')
    elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] is False for plast in CreatePZ.plast_work]) is False:

        CreatePZ.template_depth = int(CreatePZ.shoe_column) - 20
        template_str = template_SKM_EK_open
        ckm_teml_SKM_EK_open_True = f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м)'
        template_key = 'ПСШ открытый ствол + ИП отрайбирован'
        print(f'ключ {template_key}')
    elif CreatePZ.column_additional is False and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is True:

        CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 10)
        template_str = template_SKM_EK_without
        ckm_teml_SKM_EK_without = f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м)'
        template_key = 'ПСШ без хвоста'
    elif CreatePZ.column_additional is True and CreatePZ.head_column_additional > roof_skm:

        CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - 10)

        CreatePZ.template_depth = math.ceil(CreatePZ.head_column_additional - 8)
        template_str = template_SKM_DP_EK
        ckm_teml_SKM_DP_EK = f'шаблон-{second_template}мм до гл.{int(CreatePZ.head_column_additional) - 20}м))'
        template_key = 'ПСШ Доп колонна СКМ в основной колонне'
    elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is False and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:

        CreatePZ.template_depth = math.ceil(CreatePZ.head_column_additional - 8)
        CreatePZ.template_depth_addition = math.ceil(CreatePZ.perforation_roof - 18)
        template_str = template_SKM_DP

        ckm_teml_SKM_DP = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                  f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м))'
        template_key = 'ПСШ СКМ в доп колонне c хвостом'
    elif CreatePZ.column_additional is True and CreatePZ.open_trunk_well is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in CreatePZ.plast_work]) is False:
        CreatePZ.template_depth = math.ceil(CreatePZ.head_column_additional - 8)
        CreatePZ.template_depth_addition = math.ceil(CreatePZ.shoe_column_additional - 18)


        template_str = template_SKM_DP_open
        ckm_teml_SKM_DP_open = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                   f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м))'
        template_key = 'ПСШ СКМ в доп колонне + открытый ствол'
    elif CreatePZ.column_additional is True and all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] for plast in
             CreatePZ.plast_work]) is True and CreatePZ.open_trunk_well is False:
        CreatePZ.template_depth_addition = math.ceil(CreatePZ.current_bottom - 10)
        CreatePZ.template_depth = math.ceil(CreatePZ.head_column_additional - 8)

        template_str = template_SKM_DP_without
        ckm_teml_SKM_DP_without = f'шаблон-{first_template}мм до гл.{CreatePZ.template_depth_addition}м, ' \
                   f'шаблон-{second_template}мм до гл.{CreatePZ.template_depth}м))'
        template_key = 'ПСШ СКМ в доп колонне без хвоста'

    template_sel = ['ПСШ ЭК', 'ПСШ открытый ствол', 'ПСШ без хвоста', 'ПСШ Доп колонна СКМ в основной колонне', 'ПСШ СКМ в доп колонне c хвостом',
                    'ПСШ СКМ в доп колонне + открытый ствол', 'ПСШ СКМ в доп колонне без хвоста', 'ПСШ открытый ствол + ИП отрайбирован']
    template_dict = {
        'ПСШ ЭК': template_SKM_EK,
        'ПСШ открытый ствол': template_SKM_EK_open,
        'ПСШ без хвоста': template_SKM_EK_without,
        'ПСШ Доп колонна СКМ в основной колонне': template_SKM_DP_EK,
        'ПСШ СКМ в доп колонне c хвостом': template_SKM_DP,
        'ПСШ СКМ в доп колонне без хвоста': template_SKM_DP_without,
        'ПСШ СКМ в доп колонне + открытый ствол': template_SKM_DP_open,
        'ПСШ открытый ствол + ИП отрайбирован': template_SKM_EK_open_true
    }
    SKM_dict = {
        'ПСШ ЭК': ckm_teml_SKM_EK,
        'ПСШ открытый ствол': ckm_teml_SKM_EK_open,
        'ПСШ без хвоста': ckm_teml_SKM_EK_without,
        'ПСШ Доп колонна СКМ в основной колонне': ckm_teml_SKM_DP_EK,
        'ПСШ СКМ в доп колонне c хвостом': ckm_teml_SKM_DP,
        'ПСШ СКМ в доп колонне без хвоста': ckm_teml_SKM_DP_without,
        'ПСШ СКМ в доп колонне + открытый ствол': ckm_teml_SKM_DP_open,
        'ПСШ открытый ствол + ИП отрайбирован': ckm_teml_SKM_EK_open_True
    }
    # print(f'открытй ствол {CreatePZ.open_trunk_well} , башмак НКТ {CreatePZ.shoe_column}, забой P{CreatePZ.current_bottom}')
    template, ok = QInputDialog.getItem(self, 'Спуcкаемое  оборудование', 'выбор спуcкаемого оборудования',
                                        template_sel, template_sel.index(template_key), False)

    if ok and template_sel:
        self.le.setText(template)

    template_str = template_dict[template]
    ckm_teml = SKM_dict[template]

    # определение интервала скреперования


    skm_interval_tuple = skm_interval(self, template)

    # roof_skm = skm_interval_tuple[0][1]
    skm_interval = raid(skm_interval_tuple)
    list_template_ek = [
        [f'СПО  {template_str} на 'f'НКТ{CreatePZ.nkt_diam}мм', None,
         f'Спустить  {template_str} на 'f'НКТ{CreatePZ.nkt_diam}мм {ckm_teml} с замером, шаблонированием НКТ. \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1.2)],
        [f'скреперование э/к в интервале {skm_interval}м Допустить низ НКТ до гл. {CreatePZ.current_bottom}м',
         None,
         f'Произвести скреперование э/к в интервале {skm_interval}м обратной промывкой и проработкой 5 раз каждого '
         'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
         f'представителя Заказчика. Допустить низ НКТ до гл. {CreatePZ.current_bottom}м, шаблон '
         f'до глубины {CreatePZ.template_depth}м. Составить акт. \n'
         '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ). ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель УСРСиСТ', round(0.012 * 90 * 1.04 + 1.02 + 0.77, 2)],
        [f'Очистить колонну от АСПО растворителем - 2м3', None,
         f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
         f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
         f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
         f'в объеме {round(3 * CreatePZ.current_bottom / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
         f'пространство. Реагирование 2 часа.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 4],
        [f'Промывка скважину уд.весом {CreatePZ.fluid_work_short} в объеме {round(well_volume() * 1.5, 1)}м3 ',
         None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе '
         f'жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume() * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ '
         f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, '
         f'ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', well_volume_norm(well_volume() * 1.5)],
        [None, None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                     f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None,
         None, None,
         'Мастер КРС', None],
        [f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч', None,
         f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
         f'при необходимости повторная промывка.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 2.49],
        [None, None,
         f'Поднять {template_str} на НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
         f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1.2)]
    ]
    if CreatePZ.column_additional is False or (
            CreatePZ.column_additional is True and float(CreatePZ.head_column_additional) >= CreatePZ.current_bottom):
        temlate_ek = second_template
    else:
        temlate_ek = template_diam_additional_ek()[0]

    notes_list = [[None, None,
                   f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного '
                   f'двигателя с райбером d={temlate_ek + 1}мм, {temlate_ek - 1}мм, {temlate_ek - 3}мм, '
                   f'{temlate_ek - 5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до '
                   f'гл.{CreatePZ.current_bottom}м с последующим СПО шаблона {temlate_ek}мм на ТНКТ под промывку '
                   f'скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
                   f'на ТНКТ с гл. {CreatePZ.current_bottom}м вести с доливом скважины до устья т/ж '
                   f'удел.весом {CreatePZ.fluid_work} в '
                   f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 ',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, None],
                  [None, None,
                   f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с '
                   f'долотом {temlate_ek};'
                   f' {temlate_ek - 2}; {temlate_ek - 4}мм  фрезера-{temlate_ek}мм, райбера-{temlate_ek + 1}мм и '
                   f'другого оборудования и '
                   f'инструмента, (при необходимости  ловильного), при необходимости на СБТ для восстановления '
                   f'проходимости ствола  '
                   f'и забоя скважины с применением мех.ротора, до текущего забоя с последующей нормализацией до '
                   f'планового '
                   f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{CreatePZ.current_bottom}м '
                   f'вести с доливом '
                   f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС',
                   None],
                  [None, None,
                   f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию '
                   f'№2 произвести '
                   f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.'
                   f'{CreatePZ.current_bottom}м вести с '
                   f'доливом скважины до устья т/ж удел.весом с доливом c'
                   f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None],

                  [None, None,
                   f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 '
                   f'до планового '
                   f'текущего забоя. СПО КОТ-50 повторить до полной нормализации. При жесткой посадке  '
                   f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки '
                   f'на ТНКТ с гл.{CreatePZ.current_bottom}м'
                   f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в '
                   f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, ''],
                  [None, None,
                   f'Примечание №5: В случае необходимости по результатам восстановления проходимости '
                   f'экплуатационной колонны '
                   f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
                   f'проходимость. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
                   f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме '
                   f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
                   None, None, None, None, None, None, None, 'Мастер КРС', None, None]]

    privyazka_nkt = [f'Привязка по ГК и ЛМ По привязому НКТ удостовериться в наличии текущего забоя', None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис".'
                     f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины.'
                     f' По привязому НКТ удостовериться в наличии'
                     f'текущего забоя с плановым, при необходимости нормализовать забой обратной промывкой тех жидкостью '
                     f'уд.весом {CreatePZ.fluid_work}   до глубины {CreatePZ.current_bottom}м',
                     None, None, None, None, None, None, None, 'Мастер КРС', None, None]
    if CreatePZ.current_bottom - CreatePZ.perforation_sole <= 10 and CreatePZ.open_trunk_well is False:
        privyazka_question = QMessageBox.question(self, 'Привязка оборудования',
                                                  f'зумпф составляет {int(CreatePZ.current_bottom - CreatePZ.perforation_sole)}м '
                                                  f'нужно ли привязывать компоновку?'
                                                                                )
        if privyazka_question == QMessageBox.StandardButton.Yes:
            list_template_ek.insert(-1, privyazka_nkt)

    if float(CreatePZ.static_level) > 700:
        kot_question = QMessageBox.question(self, 'Низкий Статический уровень', 'Нужно ли произвести СПО '
                                                                                'обратных клапанов перед ПСШ?')
        if kot_question == QMessageBox.StandardButton.Yes:
            # print(f'Нужно вставить коты')
            for row in kot_work(self)[::-1]:
                list_template_ek.insert(0, row)

    if CreatePZ.gipsInWell is True :  # Добавление работ при наличии Гипсово-солевх отложений
        gips = pero(self)
        for row in gips[::-1]:
            list_template_ek.insert(0, row)


    if CreatePZ.count_template == 0:
        list_template_ek = list_template_ek + notes_list
        CreatePZ.count_template += 1
    else:
        list_template_ek = list_template_ek
        list_template_ek.pop(2)




    return list_template_ek


def paker_diametr_select(depth_landing):
    from open_pz import CreatePZ

    if CreatePZ.column_additional is False or (
            CreatePZ.column_additional is True and depth_landing < CreatePZ.head_column_additional):
        diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
    else:
        diam_internal_ek = CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness

    for diam, diam_internal_paker in CreatePZ.paker_diam_dict.items():
        if diam_internal_paker[0] <= diam_internal_ek << diam_internal_paker[1]:
            return diam


def pero(self):
    from work_py.rir import pero_select
    from open_pz import CreatePZ
    from work_py.drilling import drilling_nkt
    pero_list = pero_select(self, CreatePZ.current_bottom)
    gipsPero_list = [
        [f'Спустить {pero_list}  на тНКТ{CreatePZ.nkt_diam}мм', None,
         f'Спустить {pero_list}  на тНКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м '
         f'с замером, шаблонированием шаблоном. Опрессовать НКТ на 150атм. Вымыть шар. \n'
         f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', 2.5],
        [f'Промывка уд.весом {CreatePZ.fluid_work_short} в объеме {round(well_volume() * 1.5, 1)}м3 ',
         None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости '
         f'6-8 л/сек в присутствии представителя Заказчика в объеме {round(well_volume() * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ '
         f'ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ '
         f'НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 1.5],
        [None, None,
         f'Приподнять до глубины {round(CreatePZ.current_bottom - 20, 1)}м. Тех отстой 2ч. Определение текущего забоя, '
         f'при необходимости повторная промывка.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 2.49],
        [None, None,
         f'Поднять {pero_list} на НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
         f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС',
         round(CreatePZ.current_bottom / 9.5 * 0.028 * 1.2 * 1.04 + 0.005 * CreatePZ.current_bottom / 9.5 + 0.17 + 0.5,
               2)],
        [None, None,
         f'В случае недохождения пера до текущего забоя работы продолжить:',
         None, None, None, None, None, None, None,
         'Мастер КРС',
         None]
    ]
    if CreatePZ.gipsInWell is True:
        if CreatePZ.dict_pump_SHGN["do"] != 0:

            gipsPero_list = [gipsPero_list[-1]]
            drilling_list = drilling_nkt(self)
            drilling_list[2] = [f'нормализацию забоя до Н= {CreatePZ.current_bottom}м', None,
                                f'Произвести нормализацию забоя до Н= {CreatePZ.current_bottom}м с наращиванием, '
                                f'промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                                'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
                                'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя '
                                'осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
                                f'до начала работ). Работы производить согласно сборника технологических регламентов и '
                                f'инструкций в присутствии'
                                f' представителя заказчика.',
                                None, None, None, None, None, None, None,
                                'Мастер КРС, УСРСиСТ', 16, ]

            for row in drilling_list:
                gipsPero_list.append(row)
        else:
            drilling_list = drilling_nkt(self)
            drilling_list[2] = [f'Произвести нормализацию забоя до Н= {CreatePZ.current_bottom}м', None,
                                f'Произвести нормализацию забоя до Н= {CreatePZ.current_bottom}м с наращиванием, промывкой '
                                f'тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                                'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
                                'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя '
                                'осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
                                f'до начала работ). Работы производить согласно сборника технологических регламентов и '
                                f'инструкций в присутствии представителя заказчика.',
                                None, None, None, None, None, None, None,
                                'Мастер КРС, УСРСиСТ', 16, ]
            for row in drilling_list:
                gipsPero_list.append(row)

    return gipsPero_list

def definition_roof_not_raiding(self):
    from open_pz import CreatePZ
    dict_perforation = CreatePZ.dict_perforation
    plast_all = list(dict_perforation.keys())

    if CreatePZ.column_additional is False or (
            CreatePZ.column_additional and CreatePZ.head_column_additional >= CreatePZ.current_bottom):
        for plast in plast_all:
            roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))

            if dict_perforation[plast]['отрайбировано']:
                roof_plast = CreatePZ.current_bottom
                roof_add_column_plast = roof_plast
            else:
                roof_plast = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
                roof_add_column_plast = roof_plast
                break
    elif CreatePZ.column_additional:
        for plast in plast_all:
            roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
            print(roof)
            if CreatePZ.head_column_additional <= roof:

                if dict_perforation[plast]['отрайбировано']:
                    print('приветствуууу')
                    print(dict_perforation[plast]['отрайбировано'])
                    roof_add_column_plast = CreatePZ.current_bottom
                    roof_plast = CreatePZ.head_column_additional
                else:
                    roof_add_column_plast = roof
                    roof_plast = CreatePZ.head_column_additional
                    break
            else:
                if dict_perforation[plast]['отрайбировано']:
                    print('приветств')
                    print(dict_perforation[plast]['отрайбировано'])
                    roof_add_column_plast = CreatePZ.current_bottom
                    roof_plast = CreatePZ.head_column_additional
                else:
                    roof_add_column_plast = CreatePZ.current_bottom
                    roof_plast = roof
                    break

        # for plast in plast_all:
        #     roof = min(list(map(lambda x: x[0], list(dict_perforation[plast]['интервал']))))
        #     if CreatePZ.head_column_additional > roof:
        #         if dict_perforation[plast]['отрайбировано']:
        #             roof_plast = CreatePZ.head_column_additional
        #         else:
        #             roof_plast = roof
        #             break
    print(f' кровля отрайбированного интервал доп кол{roof_add_column_plast}')
    print(f' кровля отрайбированного интервал {roof_plast}')
    return roof_plast, roof_add_column_plast