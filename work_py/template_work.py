from PyQt5.QtWidgets import QMessageBox

import H2S
import math

import main


def well_volume():
    from open_pz import CreatePZ
    # print(CreatePZ.column_additional)
    if CreatePZ.column_additional == False:

        volume_well = 3.14 * (CreatePZ.column_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000000 * (
            CreatePZ.current_bottom)
        return volume_well
    else:

        volume_well = (3.14 * (CreatePZ.column_additional_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000 * (
                CreatePZ.current_bottom - CreatePZ.head_column_additional) / 1000) + (
                                  3.14 * (CreatePZ.column_diametr - CreatePZ.column_wall_thickness * 2) ** 2 / 4 / 1000 * (
                              CreatePZ.head_column_additional) / 1000)
        return volume_well

def template_diam_ek():
    from open_pz import CreatePZ

    diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
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


def template_diam_additional_ek():
    from open_pz import CreatePZ
    diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
    diam_internal_ek_addition = CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness
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

    for diam, diam_internal in template_second_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek <= diam_internal[1]:
            template_second_diam = diam
    for diam, diam_internal in template_second_diam_dict.items():
        if diam_internal[0] <= diam_internal_ek_addition <= diam_internal[1]:
            template_first_diam = diam
    return (template_first_diam, template_second_diam)

def template_ek_without_skm(self):
    from open_pz import CreatePZ
    print(f' Башмака {CreatePZ.shoe_column, CreatePZ.current_bottom}')

    print(f' наличие открытого ствола {CreatePZ.shoe_column_additional, CreatePZ.open_trunk_well, CreatePZ.shoe_column, CreatePZ.current_bottom, CreatePZ.column_additional}')

    length_template_addition = int(''.join(['30' if CreatePZ.lift_ecn_can_addition == True else '2']))
    

    if CreatePZ.column_additional == True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr <110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

    lift_ecn_can = {True: 30, False: 4}

    print(f' кровля ПВР {CreatePZ.perforation_roof}')

    CreatePZ.nkt_diam = ''.join(['73' if CreatePZ.column_diametr >110 else '60'])
    if CreatePZ.column_additional == False and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == False:
        template_str = f'перо + шаблон-{template_diam_ek()[0]}мм L-2м + НКТ{CreatePZ.nkt_diam}мм {int(CreatePZ.current_bottom - math.ceil(CreatePZ.perforation_roof)+8)}м ' \
                       f'+  НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{math.ceil(CreatePZ.perforation_roof-8)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof-8)
    elif CreatePZ.column_additional == False and CreatePZ.open_trunk_well ==  True and CreatePZ.work_pervorations_approved == False:
        template_str = f'фильтр-направление L-2м + НКТ{CreatePZ.nkt_diam}мм {math.ceil(CreatePZ.current_bottom - CreatePZ.perforation_roof+8)}м' \
                       f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{math.ceil(CreatePZ.perforation_roof - 8)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 8)
    elif CreatePZ.column_additional == False and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == True:
        template_str = f'перо +НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{math.ceil(CreatePZ.current_bottom - 8)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 8)
    elif CreatePZ.column_additional == True and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == False:
        template_str = f'обточная муфта + НКТ{nkt_pod}мм {math.ceil(CreatePZ.current_bottom-math.ceil(CreatePZ.perforation_roof - 10))}м +' \
                       f' шаблон-{template_diam_additional_ek()[0]}мм L-{length_template_addition}м + НКТ{nkt_pod}мм' \
                       f' {math.ceil(CreatePZ.perforation_roof - CreatePZ.head_column_additional -20 -length_template_addition)}м ' \
               f' + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(шаблон; Ф-{template_diam_additional_ek()[0]}мм до гл.{math.ceil(CreatePZ.perforation_roof - 10)}м, шаблон; Ф-{template_diam_ek()[0]}мм до гл.{CreatePZ.head_column_additional-10}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 8)
    elif CreatePZ.column_additional == True and CreatePZ.open_trunk_well == True and CreatePZ.work_pervorations_approved == False:
        template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {math.ceil(CreatePZ.current_bottom - math.ceil(CreatePZ.perforation_roof) + 8)}м ' \
                        f'шаблон-{template_diam_additional_ek()[0]}мм L-{length_template_addition} + {math.ceil(CreatePZ.perforation_roof) + 8- CreatePZ.head_column_additional-length_template_addition -6}'\
                      f'+ шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(шаблон-{template_diam_additional_ek()[0]}мм до {math.ceil(CreatePZ.perforation_roof) - 10}м, шаблон Ф-{template_diam_additional_ek()[1]}мм до гл.{CreatePZ.head_column_additional- 10}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 8)
    elif CreatePZ.column_additional == True and CreatePZ.work_pervorations_approved == True:
        template_str = f'обточная муфта + шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'шаблон; Ф-{template_diam_additional_ek()[1]}мм до гл.{math.ceil(min(list(CreatePZ.current_bottom)))}м)'
        CreatePZ.template_depth = math.ceil(min(list(CreatePZ.current_bottom)))

    list_template_ek = [
        [None, None, f'Спустить  {template_str}на 'f'НКТ{CreatePZ.nkt_diam}мм {ckm_teml} с замером, шаблонированием НКТ. \n'
                     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', round(CreatePZ.current_bottom/9.52*1.51/60*1.2*1.04 +0.18+0.008*CreatePZ.current_bottom/9.52 +0.003 *CreatePZ.current_bottom/9.52,2)],

        [None, '№ п/п',
         f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
                        f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
                        f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
                        f'в объеме {round(3 * CreatePZ.current_bottom/1000,1)}м3. Приподнять. Закрыть трубное и затрубное '
         f'пространство. Реагирование 2 часа.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 4],
        [None, None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                        f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None, None, None,
         'Мастер КРС', None],
        [None, None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume()*1.5,1)}м3. ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 1.5],
        [None, '№ п/п', f'Приподнять до глубины {CreatePZ.current_bottom-20}м. Тех отстой 2ч. Определение текущего забоя, при необходимости повторная промывка.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 2.49],
        [None, '№ п/п', f'Поднять {template_str} на НКТ73мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
                        f'объеме {round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС', round(CreatePZ.current_bottom / 9.5 *0.028*1.2*1.04 +0.005 *CreatePZ.current_bottom/9.5+0.17+0.5,2)]
    ]
    if CreatePZ.column_additional == False:
        temlate_ek = template_diam_ek()[1]
    else:
        temlate_ek = template_diam_additional_ek()[0]

    notes_list = [[None,None,
                  f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного двигателя с райбером d={temlate_ek+1}мм, '
                  f'{temlate_ek-1}мм, {temlate_ek-3}мм, {temlate_ek-5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до гл.{CreatePZ.current_bottom}м с последующим'
                  f' СПО шаблона {temlate_ek}мм на ТНКТ под промывку скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
                  f'на ТНКТ с гл. {CreatePZ.current_bottom}м вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в '
                  f'объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3 ',
                  None, None, None, None, None, None, None,  'Мастер КРС', None, None],
    [None, None, f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с долотом {temlate_ek};'
           f' {temlate_ek-2}; {temlate_ek-4}мм  фрезера-{temlate_ek}мм, райбера-{temlate_ek+1}мм и другого оборудования и '
           f'инструмента, (при необходимости  ловильного),  при необходимости на СБТ для восстановления проходимости ствола  '
           f'и забоя скважины с применением мех.ротора,  до текущего забоя с последующей нормализацией до планового '
           f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{CreatePZ.current_bottom}м вести с доливом '
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None, 'Мастер КРС',
     None],
    [None, None, f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию №2 произвести '
           f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м вести с '
           f'доливом скважины до устья т/ж удел.весом с доливом c'
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None,  'Мастер КРС', None],

    [None, '№ п/п',
     f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 или КОС до планового '
     f'текущего забоя. СПО КОТ-50 или КОС повторить до полной нормализации. При жесткой посадке  '
     f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
     f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None,   'Мастер КРС', None,''],
    [None, '№ п/п', f'Примечание №5: В случае необходимости по результатам восстановления проходимости экплуатационной колонны '
    f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
    f'проходимость. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
     f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None, 'Мастер КРС',  None, None]]

    privyazka_nkt = [None, None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис".'
                     f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины. По привязому НКТ удостовериться в наличии'
                     f'текущего забоя с плановым, при необходимости нормализовать забой обратной промывкой тех жидкостью '
                     f'уд.весом {CreatePZ.fluid_work}   до глубины {CreatePZ.current_bottom}м',
                     None, None, None, None, None, None, None, 'Мастер КРС', None, None]

    if CreatePZ.current_bottom - CreatePZ.perforation_sole <= 10:
        list_template_ek.insert(-1, privyazka_nkt)
    if CreatePZ.gipsInWell == True: # and 'НВ' in str(CreatePZ.dict_pump["do"][0]).upper() and CreatePZ.if_None(CreatePZ.paker_do['do']) == 'отсут':
        gips = pero(self)
        for row in gips[::-1]:
            list_template_ek.insert(0,row)


    return list_template_ek + notes_list

def template_ek(self):
    from open_pz import CreatePZ


    print(f' Башмака {CreatePZ.shoe_column, CreatePZ.current_bottom}')

    print(f' наличие открытого ствола {CreatePZ.shoe_column_additional, CreatePZ.open_trunk_well,CreatePZ.shoe_column,  CreatePZ.current_bottom, CreatePZ.column_additional  }')

    if CreatePZ.column_additional == True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr <110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

        # temlate_ek = template_ek()
    else:
        template_ek = template_diam_ek()

    lift_ecn_can = {True: 30, False: 4}
    print(CreatePZ.plast_all)
    print(CreatePZ.dict_work_pervorations.keys())
    

    CreatePZ.nkt_diam = ''.join(['73' if CreatePZ.column_diametr >110 else '60'])
    length_template_addition = int(''.join(['30' if CreatePZ.lift_ecn_can_addition == True else '2']))
    if CreatePZ.column_additional == False and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == False:
        template_str = f'перо + шаблон-{template_diam_ek()[0]}мм L-2м + НКТ{CreatePZ.nkt_diam}мм {int(CreatePZ.current_bottom - CreatePZ.perforation_roof+8)}м ' \
                       f'+ СКМ-{int(CreatePZ.column_diametr)} +10м НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_diametr)} до Н={int(CreatePZ.perforation_roof-8)}м,' \
                   f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{int(CreatePZ.perforation_roof-18)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 18)
    elif CreatePZ.column_additional == False and CreatePZ.open_trunk_well ==  True and CreatePZ.work_pervorations_approved == False:
        template_str = f'фильтр-направление L-2м + НКТ{CreatePZ.nkt_diam}мм {int(CreatePZ.current_bottom - CreatePZ.perforation_roof+8)}м' \
                       f'+ СКМ-{int(CreatePZ.column_diametr)} +10м ' \
                       f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_diametr)} до Н={int(CreatePZ.perforation_roof - 8)}м,' \
                   f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{int(CreatePZ.perforation_roof - 18)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 18)
    elif CreatePZ.column_additional == False and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == True:
        template_str = f'перо + СКМ-{int(CreatePZ.column_diametr)} +10м ' \
                       f'НКТ{CreatePZ.nkt_diam}мм + шаблон-{template_diam_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_diametr)} до Н={int(CreatePZ.perforation_roof - 8)}м,' \
                   f'шаблон; Ф-{template_diam_ek()[1]}мм до гл.{int(CreatePZ.perforation_roof - 18)}м)'
        CreatePZ.template_depth = math.ceil(CreatePZ.current_bottom - 10)
    elif CreatePZ.column_additional == True and CreatePZ.open_trunk_well == False and CreatePZ.work_pervorations_approved == False:
        template_str = f'обточная муфта + НКТ{nkt_pod} {int(CreatePZ.current_bottom - math.ceil(CreatePZ.perforation_roof) + 10)}м ' \
               f'+ СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + шаблон-{template_diam_additional_ek()[0]}мм L-{length_template_addition}м' \
               f' + НКТ{nkt_pod} {int(CreatePZ.current_bottom - (int(CreatePZ.current_bottom - math.ceil(CreatePZ.perforation_roof) + 10)) - length_template_addition - CreatePZ.head_column_additional)}м + ' \
               f'шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_additional_diametr)} до Н={int(CreatePZ.perforation_roof - 10)}м,' \
                   f'шаблон; Ф-{template_diam_additional_ek()[0]}мм до гл.{int(CreatePZ.perforation_roof - 20)}м, ' \
                   f'шаблон; Ф-{template_diam_additional_ek()[1]}мм до гл.{int(CreatePZ.head_column_additional - 10)}м))'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 18)
    elif CreatePZ.column_additional == True and CreatePZ.open_trunk_well == True and CreatePZ.work_pervorations_approved == False:
        template_str = f'фильтр направление L-2м + НКТ{nkt_pod} {math.ceil(CreatePZ.current_bottom - CreatePZ.perforation_roof + 10)}м ' \
                       f'+ СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + шаблон-{template_diam_additional_ek()[0]}мм L-{length_template_addition}м' \
                    f' + НКТ{nkt_pod} {int(CreatePZ.current_bottom - (int(CreatePZ.current_bottom - CreatePZ.perforation_roof + 10)) - 13 - length_template_addition  - CreatePZ.head_column_additional+10)}м' \
                       f' шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_additional_diametr)} до Н={int(CreatePZ.perforation_roof - 8)}м,' \
                   f'шаблон; Ф-{template_diam_additional_ek()[0]}мм до гл.{int(CreatePZ.perforation_roof - 18)}м) ' \
                   f'шаблон; Ф-{template_diam_additional_ek()[1]}мм до гл.{int(CreatePZ.head_column_additional - 8)}м))'
        CreatePZ.template_depth = math.ceil(CreatePZ.perforation_roof - 18)
    elif CreatePZ.column_additional == True and CreatePZ.work_pervorations_approved == True:
        template_str = f'обточная муфта + СКМ-{int(CreatePZ.column_additional_diametr)} +10м НКТ{nkt_pod} + шаблон-{template_diam_additional_ek()[1]}мм L-{lift_ecn_can[CreatePZ.lift_ecn_can]}м '
        ckm_teml = f'(СКМ-{int(CreatePZ.column_additional_diametr)} до Н={int(min(list(CreatePZ.current_bottom)))}м,' \
                   f'шаблон; Ф-{template_diam_additional_ek()[0]}мм до гл.{int(min(list(CreatePZ.current_bottom)) - 10)}м)'\
                   f'шаблон; Ф-{template_diam_additional_ek()[1]}мм до гл.{int(CreatePZ.head_column_additional - 8)}м))'
        CreatePZ.template_depth = math.ceil(min(list(CreatePZ.current_bottom)) - 10)
    list_template_ek = [
        [None, None, f'Спустить  {template_str}на 'f'НКТ{CreatePZ.nkt_diam}мм {ckm_teml} с замером, шаблонированием НКТ. \n'
                     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', round(CreatePZ.current_bottom/9.52*1.51/60*1.2*1.04 +0.18+0.008*CreatePZ.current_bottom/9.52 +0.003 *CreatePZ.current_bottom/9.52,2)],
        [None, None, f'Произвести скреперование э/к в интервале  {int(CreatePZ.perforation_roof-8-90)}-{int(CreatePZ.perforation_roof-8)}м  обратной промывкой и проработкой 5 раз каждого '
                     'наращивания. Работы производить согласно сборника технологических регламентов и инструкций в присутствии '
                     f'представителя Заказчика. Допустить компоновку до гл. {CreatePZ.current_bottom}м (НИЗ) Составить акт. \n'
                     '(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ). ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель УСРСиСТ', round(0.012*90*1.04+1.02+0.77,2)],
        [None, '№ п/п',
         f'По результатам ревизии ГНО, в случае наличия отложений АСПО:\n'
                        f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
                        f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
                        f'в объеме {round(3 * CreatePZ.current_bottom/1000,1)}м3. Приподнять. Закрыть трубное и затрубное '
         f'пространство. Реагирование 2 часа.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 4],
        [None, '№ п/п',
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume() * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 1.5],
        [None, '№ п/п', f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                        f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None, None, None,
         'Мастер КРС', None],
        [None, '№ п/п', f'Приподнять до глубины {CreatePZ.current_bottom-20}м. Тех отстой 2ч. Определение текущего забоя, при необходимости повторная промывка.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 2.49],
        [None, '№ п/п', f'Поднять {template_str} на НКТ73мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
                        f'объеме {round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'Мастер КРС', round(CreatePZ.current_bottom / 9.5 *0.028*1.2*1.04 +0.005 *CreatePZ.current_bottom/9.5+0.17+0.5,2)]
    ]
    if CreatePZ.column_additional == False:
        temlate_ek = template_diam_ek()[1]
    else:
        temlate_ek = template_diam_additional_ek()[1]

    notes_list = [[None,None,
                  f'ПРИМЕЧАНИЕ №1: При непрохождении шаблона d={temlate_ek}мм предусмотреть СПО забойного двигателя с райбером d={temlate_ek+1}мм, '
                  f'{temlate_ek-1}мм, {temlate_ek-3}мм, {temlate_ek-5}мм на ТНКТ под проработку в интервале посадки инструмента с допуском до гл.{CreatePZ.current_bottom}м с последующим'
                  f' СПО шаблона {temlate_ek}мм на ТНКТ под промывку скважины (по согласованию Заказчиком). Подъем райбера (шаблона {temlate_ek}мм) '
                  f'на ТНКТ с гл. {CreatePZ.current_bottom}м вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в '
                  f'объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3 ',
                  None, None, None, None, None, None, None,  'Мастер КРС', None, None],
    [None, None, f'ПРИМЕЧАНИЕ №2: При отсутствия планового текущего забоя произвести СПО забойного двигателя с долотом {temlate_ek};'
           f' {temlate_ek-2}; {temlate_ek-4}мм  фрезера-{temlate_ek}мм, райбера-{temlate_ek+1}мм и другого оборудования и '
           f'инструмента, (при необходимости  ловильного),  при необходимости на СБТ для восстановления проходимости ствола  '
           f'и забоя скважины с применением мех.ротора,  до текущего забоя с последующей нормализацией до планового '
           f'текущего забоя. Подъем долота с забойным двигателем на  ТНКТ с гл.{CreatePZ.current_bottom}м вести с доливом '
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None, 'Мастер КРС',
     None],
    [None, None, f'ПРИМЕЧАНИЕ №3: В случае отсутствия проходки более 4 часов при нормализации забоя по примечанию №2 произвести '
           f'СПО МЛ с последующим СПО торцевой печати. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м вести с '
           f'доливом скважины до устья т/ж удел.весом с доливом c'
           f'скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None,  'Мастер КРС', None],

    [None, '№ п/п',
     f'Примечание №4: В случае отсутствия циркуляции при нормализации забоя произвести СПО КОТ-50 или КОС до планового '
     f'текущего забоя. СПО КОТ-50 или КОС повторить до полной нормализации. При жесткой посадке  '
     f'КОТ-50 или КОС произвести взрыхление с СПО забойного двигателя с долотом . Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
     f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None,   'Мастер КРС', None,''],
    [None, '№ п/п', f'Примечание №5: В случае необходимости по результатам восстановления проходимости экплуатационной колонны '
    f'по согласованию с УСРСиСТ произвести СПО пера под промывку скважины до планового текущего забоя на '
    f'проходимость. Подъем компоновки на ТНКТ с гл.{CreatePZ.current_bottom}м'
     f' вести с доливом скважины до устья т/ж удел.весом {CreatePZ.fluid_work} в объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3',
     None, None, None, None, None, None, None, 'Мастер КРС',  None, None]]

    privyazka_nkt = [None, None,
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис".'
                     f' ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины. По привязому НКТ удостовериться в наличии'
                     f'текущего забоя с плановым, при необходимости нормализовать забой обратной промывкой тех жидкостью '
                     f'уд.весом {CreatePZ.fluid_work}   до глубины {CreatePZ.current_bottom}м',
                     None, None, None, None, None, None, None, 'Мастер КРС', None, None]
    if CreatePZ.current_bottom - CreatePZ.perforation_sole <=10 and CreatePZ.open_trunk_well == False:
        list_template_ek.insert(-1, privyazka_nkt)
    if CreatePZ.gipsInWell == True: # and 'НВ' in str(CreatePZ.dict_pump["do"][0]).upper() and CreatePZ.if_None(CreatePZ.paker_do['do']) == 'отсут':
        gips = pero(self)
        for row in gips[::-1]:
            list_template_ek.insert(0, row)
    return list_template_ek + notes_list



def paker_diametr_select(depth_landing):
    from open_pz import CreatePZ

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and depth_landing < CreatePZ.head_column_additional):
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
        [None, None,
         f'Спустить {pero_list}  на тНКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м '
         f'с замером, шаблонированием шаблоном. Опрессовать НКТ на 150атм. Вымыть шар. \n'
         f'С ГЛУБИНЫ 1100м СНИЗИТЬ СКОРОСТЬ  СПУСКА до 0.25м/с ВОЗМОЖНО ОТЛОЖЕНИЕ ГИПСА'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', 2.5],
        [None, None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume() * 1.5, 1)}м3. ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 1.5],
        [None, None,
         f'Приподнять до глубины {CreatePZ.current_bottom - 20}м. Тех отстой 2ч. Определение текущего забоя, при необходимости повторная промывка.',
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

    if 'ЭЦН' not in str(CreatePZ.dict_pump["posle"]).upper():

        gipsPero_list = [gipsPero_list[-1]]
        drilling_list = drilling_nkt(self)
        drilling_list[2] = [None, None,
                            f'Произвести нормализацию забоя до Н= {CreatePZ.current_bottom}м с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                            'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
                            'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
                            f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
                            f' представителя заказчика.',
                            None, None, None, None, None, None, None,
                            'Мастер КРС, УСРСиСТ', 16, ]

        for row in drilling_list:
            gipsPero_list.append(row)
    else:
        drilling_list = drilling_nkt(self)
        drilling_list[2] = [None, None,
                            f'Произвести нормализацию забоя до Н= {CreatePZ.current_bottom}м с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                            'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
                            'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
                            f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
                            f' представителя заказчика.',
                            None, None, None, None, None, None, None,
                            'Мастер КРС, УСРСиСТ', 16, ]
        for row in drilling_list:
            gipsPero_list.append(row)


    return gipsPero_list






