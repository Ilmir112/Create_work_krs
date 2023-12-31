from PyQt5.QtWidgets import QMessageBox

from work_py.alone_oreration import privyazkaNKT
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm


def paker_diametr_select(depth_landing):
    from open_pz import CreatePZ

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and depth_landing <= CreatePZ.head_column_additional):
        diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
    else:
        diam_internal_ek = CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness

    for diam, diam_internal_paker in CreatePZ.paker_diam_dict.items():
        if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
            return diam
# Добавление строк с опрессовкой ЭК
def paker_list(self):
    from open_pz import CreatePZ
    from PyQt5.QtWidgets import QInputDialog


    print(f' кровля перфорации {CreatePZ.perforation_roof}')


    pressureZUMPF_question = QMessageBox.question(self, 'ЗУМПФ', 'Нужно ли опрессовывать ЗУМПФ?')
    if pressureZUMPF_question == QMessageBox.StandardButton.Yes:
        pakerDepthZumpf, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки пакера для опрессовки ЗУМПФА', int(CreatePZ.perforation_sole + 10), 0, int(CreatePZ.current_bottom))
        pressureZUMPF_answer = True
    else:
        pressureZUMPF_answer = False

    paker_depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки пакера для опрессовки колонны', int(CreatePZ.perforation_roof - 20), 0, int(CreatePZ.current_bottom-10))
    paker_khost, ok = QInputDialog.getInt(None, 'опрессовка ЭК', 'Введите длину хвостовика', 10, 0, 3000)
    try:

        while paker_khost + pakerDepthZumpf > CreatePZ.current_bottom:

            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ пакер на глубине {pakerDepthZumpf} и хв '
                                                             f'{paker_khost}  и ниже текущего забоя - {CreatePZ.current_bottom}')
            pakerDepthZumpf, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                      'Введите глубину посадки пакера для опрессовки ЗУМПФА',
                                                      int(CreatePZ.perforation_sole + 10),
                                                      int(CreatePZ.perforation_sole))

            paker_khost, ok = QInputDialog.getInt(None, 'опрессовка ЭК', 'Введите длину хвостовика', 10, 0, 3000)


    except:

        while paker_khost + paker_depth > CreatePZ.current_bottom:

            QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ пакер на глубине {paker_depth} и хв '
                                                             f'{paker_khost}  и ниже текущего забоя - {CreatePZ.current_bottom}')
            paker_khost, ok = QInputDialog.getInt(None, 'опрессовка ЭК', 'Введите длину хвостовика', 10, 0, 3000)



    def paker_select(self):
        if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth< CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + {nktOpress(self)[0]}'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth> CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог)  ' \
                           f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth-CreatePZ.head_column_additional,0)}м'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth> CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]}' \
                           f'+ НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- {round(paker_depth-CreatePZ.head_column_additional,0)}м'
        return paker_select
    nktOpress_list = nktOpress(self)
    if pressureZUMPF_answer:
        paker_list = [
            [None, None,
             f'Спустить {paker_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerDepthZumpf}м, воронкой до {pakerDepthZumpf + paker_khost}м'
             f' с замером, шаблонированием шаблоном. {nktOpress_list[1]} {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
             f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerDepthZumpf, 1.2)],
            [None, None,
             f'Посадить пакер. Опрессовать ЗУМПФ в интервале {pakerDepthZumpf} - {CreatePZ.current_bottom}м на Р={CreatePZ.max_admissible_pressure}атм в течение 30 минут в присутствии представителя заказчика, составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.77],
            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None, f'Приподнять и посадить пакер на глубине {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [None, None,
             f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
             f' в течение 30 минут  в присутствии представителя заказчика, составить акт.  '
             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],

            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Поднять {paker_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]

    else:
        paker_list = [
            [None, None,
                       f'Спустить {paker_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины {paker_depth}м, воронкой до {paker_depth+ paker_khost}м'
                        f' с замером, шаблонированием шаблоном. {nktOpress_list[1]} {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                       f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                       f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
        None, None, None, None, None, None, None,
        'мастер КРС', descentNKT_norm(paker_depth,1.2)],
            [None, None, f'Посадить пакер на глубине {paker_depth}м',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 0.4],
            [None, None, f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                         f' в течение 30 минут  в присутствии представителя заказчика, составить акт.  '
                         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],

            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Поднять {paker_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth*1.12/1000,1)}м3 удельным весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]
    dict_leakinest_keys = list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys())
    if len(CreatePZ.dict_leakiness) != 0 and int(dict_leakinest_keys[0][0]) < paker_depth:

        NEK_question = QMessageBox.question(self, 'Поинтервальная опрессовка НЭК', 'Нужна ли поинтервальная опрессовка НЭК?')
        if NEK_question == QMessageBox.StandardButton.Yes:

            pakerNEK, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                      'Введите глубину посадки пакера для под НЭК',
                                                      int(dict_leakinest_keys[0].split('-')[1]) + 10, 0,  int(CreatePZ.perforation_sole))
            paker_list = [
                [None, None,
                 f'Спустить {paker_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerNEK}м, воронкой до {pakerNEK + paker_khost}м'
                 f' с замером, шаблонированием шаблоном. {nktOpress_list[1]} {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(pakerNEK, 1.2)],
                [None, None, f'Посадить пакер на глубине {pakerNEK}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [None, None,
                 f'Опрессовать эксплуатационную колонну в интервале {pakerNEK}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                 f' в течение 30 минут  в присутствии представителя заказчика, составить акт.  '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС, предст. заказчика', 0.67],
                [None, None,
                 f'ПРИ НЕГЕРМЕТИЧНОСТИ: \n Произвести насыщение скважины в объеме 5м3 по затрубному пространству. Определить приемистость '
                 f'НЭК {dict_leakinest_keys[0]} при Р-{CreatePZ.max_admissible_pressure}атм по затрубному пространству'
                 f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                 f'после закачки, объем согласовать с подрядчиком по РИР).',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1.5],
                [None, None,
                 f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],
                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None]]
            ind_nek = 1
            while len(dict_leakinest_keys) - ind_nek != 0:
                print('запуск While')

                pakerNEK1, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                   'Введите глубину посадки пакера для под НЭК',
                                                   int(dict_leakinest_keys[ind_nek].split('-')[1]) + 10, 0,
                                                   int(CreatePZ.current_bottom))
                pressureNEK_list = [[None, None,
                                     f'При герметичности колонны в интервале 0 - {pakerNEK}м:  Допустить пакер до глубины {pakerNEK1}м',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', descentNKT_norm(pakerNEK1-pakerNEK, 1.2)],
                                    [None, None,
                                     f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в интервале {pakerNEK1}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                                     f' в течение 30 минут  в присутствии представителя заказчика, составить акт.',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', 0.77],
                                    [None, None,
                                     f'ПРИ НЕГЕРМЕТИЧНОСТИ: \n Произвести насыщение скважины в объеме 5м3 по затрубному пространству. Определить приемистость '
                                     f'НЭК {dict_leakinest_keys[ind_nek]} при Р-{CreatePZ.max_admissible_pressure}атм по затрубному пространству'
                                     f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                                     f'после закачки, объем согласовать с подрядчиком по РИР).',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', 1.5],
                                    [None, None,
                                     f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                                     f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', 0.7]]

                for i in pressureNEK_list:
                    paker_list.append(i)
                ind_nek += 1
                pakerNEK = pakerNEK1

            if len(dict_leakinest_keys) - ind_nek == 0:
                pressureNEK_list = [[None, None,
                                       f'При герметичности колонны в интервале 0 - {pakerNEK}м:  Допустить пакер до глубины {paker_depth}м',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС', 0.4],
                                      [None, None,
                                       f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                                    f' в течение 30 минут  в присутствии представителя заказчика, составить акт.',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС', 0.77],
                                      [None, None,
                                       f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
                                       f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                                       None, None, None, None, None, None, None,
                                       'мастер КРС', 0.7],
                                    [None, None,
                                     f'Поднять {paker_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                                     f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]
                                    ]
                for row in pressureNEK_list:
                    paker_list.append(row)

    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - float(paker_depth))) < 10 or abs(
                    float(interval[0] - float(paker_depth))) < 10:
                if privyazkaNKT(self)[0] not in paker_list:
                    paker_list.insert(1, privyazkaNKT(self)[0])

    return paker_list

def nktOpress(self):
    from open_pz import CreatePZ
    if CreatePZ.nktOpressTrue == False:
        CreatePZ.nktOpressTrue == True
        return 'НКТ + опрессовочное седло', 'Опрессовать НКТ на 200атм. Вымыть шар'
    else:
        return 'НКТ', ''

