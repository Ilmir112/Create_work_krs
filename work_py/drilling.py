from PyQt5.QtWidgets import QInputDialog, QMessageBox, QComboBox
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
def drilling_nkt(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    from krs import well_volume
    bottomType_list = ['ЦМ', 'РПК', 'РПП', 'ВП']
    bottomType, ok = QInputDialog.getItem(self, 'забой', 'Чем представлени забой', bottomType_list, 0, False)
    if ok and bottomType_list:
        self.le.setText(bottomType)

    currentBottom = CreatePZ.current_bottom

    drillingBit_diam = paker_diametr_select(CreatePZ.current_bottom) + 2

    if CreatePZ.column_additional == True:
        nkt_pod = ['60мм' if CreatePZ.column_additional_diametr < 110 else '73мм со снятыми фасками']
        nkt_pod = ''.join(nkt_pod)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and CreatePZ.head_column_additional >= CreatePZ.current_bottom):
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                       f' забойный двигатель +НКТ{nkt_diam}м 20м + репер '
        drilling_short = f'долото-{drillingBit_diam}  +' \
                       f' забойный двигатель  +НКТ{nkt_diam}м 20м + репер '


    elif CreatePZ.column_additional == True:
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                       f'{CreatePZ.column_additional_wall_thickness}мм + забойный двигатель Д-76 +НКТ{nkt_pod}мм 20м + репер + ' \
                       f'НКТ{nkt_pod} {round(CreatePZ.current_bottom - CreatePZ.head_column_additional,0)}м'
        drilling_str = f'долото-{drillingBit_diam}  + забойный двигатель Д-76 +НКТ{nkt_pod}мм 20м + репер + ' \
                       f'НКТ{nkt_pod} {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м'

    current_depth, ok = QInputDialog.getInt(None, 'Нормализация забоя',
                                            'Введите глубину необходимого забоя',
                                            int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_artificial + 500))
    CreatePZ.drilling_interval.append([CreatePZ.current_bottom, current_depth])
    drilling_list = [
        [f'СПО {drilling_str} до т.з -', None,
         f'Спустить {drilling_str}  на НКТ{nkt_diam}мм до до текущего забоя с замером, '
         f'шаблонированием шаблоном\n'
         f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
         f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
         f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
         f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1.2)],
        [None, None,
         f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
         f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', round(0.14+0.17+0.08+0.48,1)],
        [f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм', None,
         f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
         f'В случае негерметичности произвести РИР по согласованию с заказчиком',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 0.67],
        [f'бурение {"".join(["" if bottomType == "ВП" or bottomType == "РПП" else "с провалом"])} до Н= {current_depth}м',
         None,
         f'Произвести разбуривание {bottomType} {"".join(["" if bottomType == "ВП" or bottomType == "РПП" else "с провалом"])} до Н= {current_depth}м '
         f' с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
         'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
         'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
         f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
         f' представителя заказчика.',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 16],
        [None, None,
         f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
         f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
         f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
         f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', None],
        [f'Промывка в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3 {CreatePZ.fluid_work_short}',
         None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
         f'в присутствии представителя заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3. Составить акт.',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', well_volume_norm(well_volume(self,CreatePZ.current_bottom))],
    ]
    drilling_work_list = []
    if len(CreatePZ.plast_work) == 0:
        drilling_list.append([f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм', None,
                              f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
                              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
                              f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, УСРСиСТ', 0.67])
    else:
        drilling_list.pop(2)
    CreatePZ.current_bottom = current_depth
    reply_drilling(self, drilling_str, nkt_diam, drilling_work_list)
    for row in drilling_work_list:
        drilling_list.append(row)

    if bottomType == "РПК" or bottomType == "РПП":
        CreatePZ.current_bottom = currentBottom
        drilling_list.append([f'Завоз СБТ', None,
                              f'В случае возможности завоза тяжелого оборудования и установки УПА-60 (АПР60/80), '
                              f'по согласованию с Заказчиком нормализацию выполнить по следующему пункту',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, УСРСиСТ', None])

        for row in drilling_sbt(self):
            drilling_list.append(row)

    return drilling_list

def drilling_sbt(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    from krs import well_volume


    drillingBit_diam = paker_diametr_select(CreatePZ.current_bottom) + 2
    nkt_pod = "2' 3/8"

    nkt_diam = ''.join(["2 7/8" if CreatePZ.column_diametr > 110 else "2 3/8"])

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and CreatePZ.head_column_additional >= CreatePZ.current_bottom):
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм '
        drilling_short = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм '


    elif CreatePZ.column_additional == True:
        drilling_str = f'долото-{drillingBit_diam} для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                       f'{CreatePZ.column_additional_wall_thickness}мм + СБТ{nkt_pod} ' \
                       f'{CreatePZ.current_bottom - CreatePZ.head_column_additional}м'
        drilling_short = f'долото-{drillingBit_diam}  + СБТ{nkt_pod} {CreatePZ.current_bottom - CreatePZ.head_column_additional}м'
    current_depth, ok = QInputDialog.getInt(None, 'Нормализация забоя',
                                            'Введите глубину необходимого забоя',
                                            int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_artificial + 500))
    CreatePZ.drilling_interval.append([CreatePZ.current_bottom, current_depth])
    drilling_list = [
        [f'СПО {drilling_short} на СБТ{nkt_diam} до Н= {CreatePZ.current_bottom - 30}', None,
         f'Спустить {drilling_str}  на СБТ{nkt_diam} до Н= {CreatePZ.current_bottom - 30}м с замером, '
         f' (При СПО первых десяти СБТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
         f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
         f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
         f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1.1)],
        [f'монтаж мех.ротора', None,
         f'Произвести монтаж мех.ротора. Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
         f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', round(0.14+0.17+0.08+0.48 +1.1,1)],
        [f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм', None,
         f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
         f'В случае негерметичности произвести РИР по согласованию с заказчиком',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 0.67],
        [f'нормализацию до Н= {current_depth}м', None,
         f'Произвести нормализацию до Н= {current_depth}м с наращиванием, с периодической   промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
         'При отсутствии проходки более 4ч, согласовать с УСРСиСТ подьем компоновки на ревизию. '
         'При наработке долото более 80ч, произвести подьем и заменить долото и (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
         f'до начала работ). Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
         f' представителя заказчика.',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', 16, ],
        [None, None,
         f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
         f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ  И ДОЛОТА);'
         f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ)) \n'
         f'ПРИПОДНИМАЕМ ИНСТРУМЕНТ ПОСЛЕ 15-20 МИНУТ РАБОТЫ',
         None, None, None, None, None, None, None,
         'Мастер КРС, УСРСиСТ', None],
        [f'Промыть  {CreatePZ.fluid_work}  '
         f'в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3', None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
         f'в присутствии представителя заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3. Составить акт.',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', well_volume_norm(well_volume(self,CreatePZ.current_bottom))],
    ]
    drilling_work_list = []
    if len(CreatePZ.plast_work) == 0:
        drilling_list.append([f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм', None,
                              f'Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика. Составить акт. '
                              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) \n'
                              f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, УСРСиСТ', 0.67])
    else:
        drilling_list.pop(2)
    CreatePZ.current_bottom = current_depth
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
        drilling_true_quest_list = [[f'Произвести нормализацию до Н= {current_depth}м', None,
                                     f'Произвести нормализацию до Н= {current_depth}м с наращиванием, промывкой тех жидкостью уд.весом {CreatePZ.fluid_work}.'
                                     f'Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
                                     f' представителя заказчика.',
                                     None, None, None, None, None, None, None,
                                     'Мастер КРС, УСРСиСТ', 8, ],
                                    [f'Промыть  {CreatePZ.fluid_work} в объеме '
                                     f'{round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3', None,
                                     f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
                                     f'в присутствии представителя заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 2, 1)}м3. Составить акт.',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС, предст. заказчика', 1.5],
                                    ]
        CreatePZ.drilling_interval.append([CreatePZ.current_bottom, current_depth])
        if len(CreatePZ.plast_work) == 0:
            drilling_true_quest_list.append([f' Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм', None,
                                             f' Опрессовать ЭК и ЦМ на Р={CreatePZ.max_admissible_pressure}атм в '
                                             f'присутствии представителя заказчика. Составить акт. '
                                             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с '
                                             f'подтверждением за 2 часа до начала работ) \n'
                                             f'В случае негерметичности произвести РИР по согласованию с заказчиком',
                                             None, None, None, None, None, None, None,
                                             'Мастер КРС, УСРСиСТ', 0.67])

        for row in drilling_true_quest_list:
            drilling_work_list.append(row)

        CreatePZ.current_bottom = current_depth

        reply_drilling(self, drilling_str, nkt_diam, drilling_work_list)


    else:

        drilling_list_end = [
            [None, None,
             f'Поднять  {drilling_str} на СБТ{nkt_diam} с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom * 1.4 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1.3)]]



        drilling_list_end.insert(0, [f'приподнять на 30м от забоя. Тех отстой 2ч.', None,
             f'приподнять на 30м от забоя. Тех отстой 2ч. Определение текущего забоя, при необходимости  произвести'
             f'повторную промывку скважины.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 2.5])

        for row in drilling_list_end:
            drilling_work_list.append(row)

        return drilling_work_list
