def raidingColumn(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    from work_py.template_work import well_volume
    ryber_diam = paker_diametr_select(CreatePZ.current_bottom) + 3

    if CreatePZ.column_additional == True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr <110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)



    lift_ecn_can = {True: 30, False: 4}

    print(f' кровля ПВР {CreatePZ.pervoration_min}')

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr >110 else '60'])
    if CreatePZ.column_additional == False:
        ryber_str = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                    f' забойный двигатель Д-106 +НКТ{nkt_diam}м 20м + репер '


    elif CreatePZ.column_additional == True:
        ryber_str = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                       f'{CreatePZ.column_additional_wall_thickness}мм + забойный двигатель Д-76 +НКТ{nkt_pod}мм 20м + репер + ' \
                       f'НКТ{nkt_pod} {CreatePZ.current_bottom - CreatePZ.head_column_additional}м'


    ryber_list = [
        [None, None,
         f'Спустить {ryber_str}  на НКТ{nkt_diam}мм до Н={min(min(raiding_interval(self)))-30}м с замером, '
         f'шаблонированием шаблоном 59,6мм (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
         f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
         f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
         f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            (min(min(raiding_interval(self)))-30) / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04*0.9 + 0.18 + 0.008 * (CreatePZ.perforation_roof-30) / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
            2)],
        [None, None, f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
                     f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 8],
        [None, None,
         f'Произвести райбирование ЭК в инт. {raid(raiding_interval(self))}м с наращиванием, с промывкой и проработкой 5 раз каждого наращивания. '
         f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
         f'до начала работ) Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
         f' представителя заказчика. Допустить до текущего забоя {CreatePZ.current_bottom}м.',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 8],
        [None, None,
         f' ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
         f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
         f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
         f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', None],
        [None, None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
         f'в присутствии представителя заказчика в объеме {round(well_volume()*2,1)}м3. Составить акт.',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1.5],
        [None, None,
         f'Поднять  {ryber_str} на НКТ{nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
         f'объеме {round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', round(0.25 + 0.033 * 1.2 * (CreatePZ.current_bottom) / 9.5 * 1.04*0.9, 1)]]

    CreatePZ.work_pervorations_approved = True
    for plast in CreatePZ.plast_work:

        if min(min(CreatePZ.dict_work_pervorations[plast]['интервал'])) > CreatePZ.current_bottom:
            del CreatePZ.dict_work_pervorations[plast]


    return ryber_list


def raiding_interval(self):
    from open_pz import CreatePZ

    str_raid = []
    for plast in CreatePZ.dict_perforation.keys():
        crt = []
        str_min = 10000
        str_max = 0
        for i in CreatePZ.dict_perforation[plast]['интервал']:
            if i[0] <= str_min:
                str_min = i[0]
            if i[1] >= str_max:
                str_max = i[1]
            if str_max + 30 <= CreatePZ.current_bottom:
                crt = [str_min - 30, str_max + 30]
            else:
                crt = [str_min - 30, CreatePZ.current_bottom]

        str_raid.append(crt)

    a = []
    b = 0
    c = 0
    for i in range(1, len(str_raid)):
        if str_raid[i][0] <= str_raid[i - 1][0] <= str_raid[i][1]:
            b = str_raid[i][0]
        else:
            b = str_raid[i - 1][0]
        if str_raid[i][0] <= str_raid[i - 1][1] <= str_raid[i][1]:
            c = str_raid[i][1]
        else:
            c = str_raid[i - 1][1]
        a.append([b, c])
    # if CreatePZ.perforation_sole + 30 < CreatePZ.current_bottom:
    #     str_raid = f'{round(CreatePZ.perforation_roof-30,0)} - {round(CreatePZ.perforation_sole + 30,0)}'
    # else:
    #     str_raid = f'{round(CreatePZ.perforation_roof - 30, 0)} - {CreatePZ.current_bottom}'
    a = sorted(a)
    return a
def raid(a):
    d = ''
    for i in a:
        d += f'{i[0]} - {i[1]}, '
    return d
