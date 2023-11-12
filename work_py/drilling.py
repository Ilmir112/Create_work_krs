from PyQt5.QtWidgets import QInputDialog, QMessageBox




def drilling_nkt(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    from krs import well_volume

    drillingBit_diam = paker_diametr_select(CreatePZ.current_bottom) + 2

    if CreatePZ.column_additional == True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr < 110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    if CreatePZ.column_additional == False:
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                       f' забойный двигатель Д-106 +НКТ{nkt_diam}м 20м + репер '


    elif CreatePZ.column_additional == True:
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                       f'{CreatePZ.column_additional_wall_thickness}мм + забойный двигатель Д-76 +НКТ{nkt_pod}мм 20м + репер + ' \
                       f'НКТ{nkt_pod} {CreatePZ.current_bottom - CreatePZ.head_column_additional}м'
    current_depth, ok = QInputDialog.getInt(None, 'Нормализация забоя',
                                            'Введите глубину необходимого забоя',
                                            int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_artificial + 500))
    drilling_list = [
        [None, None,
         f'Спустить {drilling_str}  на НКТ{nkt_diam}мм до Н= {CreatePZ.perforation_roof - 30}м с замером, '
         f'шаблонированием шаблоном\n'
         f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
         f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
         f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
         f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            (CreatePZ.perforation_roof - 30) / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 * 0.9 + 0.18 + 0.008 * (
                    CreatePZ.perforation_roof - 30) / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
            2)],
        [None, None,
         f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
         f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 8],
        [None, None,
         f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
         f'В случае негерметичности произвести РИР по согласованию с заказчиком',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', None],
        [None, None,
         f'Произвести бурение ЦМ до Н= {current_depth}м с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
         'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
         'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
         f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
         f' представителя заказчика.',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 16, ],
        [None, None,
         f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
         f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
         f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
         f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', None],
        [None, None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
         f'в присутствии представителя заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3. Составить акт.',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1.5],
    ]
    drilling_work_list = []
    if len(CreatePZ.dict_work_pervorations) == 0:
        drilling_list.append([None, None,
                              f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
                              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
                              f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, УСРСиСТ', None])
    else:
        drilling_list.pop(2)

    reply_drilling(self, drilling_str, nkt_diam, drilling_work_list)
    for row in drilling_work_list:
        drilling_list.append(row)

    return drilling_list



def reply_drilling(self, drilling_str, nkt_diam, drilling_work_list):
    from open_pz import CreatePZ
    from krs import well_volume
    drilling_true_quest = QMessageBox.question(self, 'Необходимость дальнейшей нормализации',
                                               'Нужно ли добавить поинтервальное бурение?')

    if drilling_true_quest == QMessageBox.StandardButton.Yes:

        current_depth, ok = QInputDialog.getInt(None, 'Нужный забой',
                                                f'Введите глубину следующей глубины для нормализации',
                                                int(CreatePZ.current_bottom), int(CreatePZ.current_bottom),
                                                5000)
        drilling_true_quest_list = [[None, None,
                                     f'Произвести бурение ЦМ до Н= {current_depth}м с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                                     'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
                                     'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
                                     f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
                                     f' представителя заказчика.',
                                     None, None, None, None, None, None, None,
                                     'Мастер КРС, УСРСиСТ', 16, ],
                                    [None, None,
                                     f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
                                     f'в присутствии представителя заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3. Составить акт.',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС, предст. заказчика', 1.5],
                                    ]
        if len(CreatePZ.dict_work_pervorations) == 0:
            drilling_true_quest_list.append([None, None,
                                             f' Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
                                             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
                                             f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                                             None, None, None, None, None, None, None,
                                             'Мастер КРС, УСРСиСТ', None])

        for row in drilling_true_quest_list:
            drilling_work_list.append(row)

        CreatePZ.current_bottom = current_depth

        reply_drilling(self, drilling_str, nkt_diam, drilling_work_list)


    else:

        drilling_list_end = [
            [None, None,
             f'Поднять  {drilling_str} на НКТ{nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', round(0.25 + 0.033 * 1.2 * (CreatePZ.current_bottom) / 9.5 * 1.04 * 0.9, 1)]]
        gis_true_quest = QMessageBox.question(self, 'Привязка',
                                                   'Нужно ли привязывать НКТ?')
        if gis_true_quest == QMessageBox.StandardButton.Yes:
             drilling_list_end.insert(0, [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                         f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4])
             drilling_list_end.insert(1, [None, None,
                                     f'По привязанному НКТ убедится в наличии что текущий забой соответствует забоя {CreatePZ.current_bottom}м, '
                                     f'При необходимости восстановить забой до глубины {CreatePZ.current_bottom}',
                                     None, None, None, None, None, None, None,
                                     'Мастер КРС, подрядчик по ГИС', 4])
        else:
            drilling_list_end.insert(0, [None, None,
             f'приподнять на 30м от забоя. Тех отстой 2ч. Определение текущего забоя, при необходимости '
             f'повторную промывку скважины.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 3.5])

        for row in drilling_list_end:
            drilling_work_list.append(row)

        return drilling_work_list
