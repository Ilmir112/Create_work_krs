from main import MyWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog

from work_py.alone_oreration import privyazkaNKT
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm

def paker_diametr_select(depth_landing):
    from open_pz import CreatePZ

    if CreatePZ.column_additional == False or (
            CreatePZ.column_additional == True and depth_landing <= CreatePZ.head_column_additional):
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



    pressureZUMPF_question = QMessageBox.question(self, 'ЗУМПФ', 'Нужно ли опрессовывать ЗУМПФ?')
    if pressureZUMPF_question == QMessageBox.StandardButton.Yes:
        pakerDepthZumpf, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                  'Введите глубину посадки пакера для опрессовки ЗУМПФА',
                                                  int(CreatePZ.perforation_sole + 10), 0, int(CreatePZ.current_bottom))
        pakerDepthZumpf = MyWindow.true_set_Paker(self, pakerDepthZumpf)
        pressureZUMPF_answer = True
    else:
        pressureZUMPF_answer = False

    paker_depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки пакера для опрессовки колонны',
                                          int(CreatePZ.perforation_roof - 20), 0, int(CreatePZ.current_bottom - 10))

    paker_depth = MyWindow.true_set_Paker(self, paker_depth)

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
        if CreatePZ.column_additional == False or CreatePZ.column_additional == True \
                and paker_depth < CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}м {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                           f' {nktOpress(self)[0]}'
            paker_short = f'в-у + НКТ{CreatePZ.nkt_diam}м {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм  +' \
                           f' {nktOpress(self)[0]}'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and \
                paker_depth > CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr_select(paker_depth)}мм ' \
                           f'(либо аналог)  ' \
                           f'для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                           f'{CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth - CreatePZ.head_column_additional, 0)}м'
            paker_short = f'в-у + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr_select(paker_depth)}мм ' \
                           f' + {nktOpress(self)[0]} ' \
                           f'+ НКТ60мм L- {round(paker_depth - CreatePZ.head_column_additional, 0)}м'
        elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and \
                paker_depth > CreatePZ.head_column_additional:
            paker_select = f'воронку + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                           f'для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                           f'{CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]}' \
                           f'+ НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'
            paker_short = f'в-у + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм + {nktOpress(self)[0]}' \
                           f'+ НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'

        return paker_select, paker_short

    nktOpress_list = nktOpress(self)
    if pressureZUMPF_answer:
        paker_list = [
            [f'СПО {paker_select(self)[1]} до глубины {pakerDepthZumpf}', None,
             f'Спустить {paker_select(self)[0]} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerDepthZumpf}м,'
             f' воронкой до {pakerDepthZumpf + paker_khost}м'
             f' с замером, шаблонированием шаблоном. {nktOpress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
             f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(pakerDepthZumpf, 1.2)],
            [f'Опрессовать ЗУМПФ в инт {pakerDepthZumpf} - {CreatePZ.current_bottom}м на '
             f'Р={CreatePZ.max_admissible_pressure}атм', None,
             f'Посадить пакер. Опрессовать ЗУМПФ в интервале {pakerDepthZumpf} - {CreatePZ.current_bottom}м на '
             f'Р={CreatePZ.max_admissible_pressure}атм в течение 30 минут в присутствии представителя заказчика, '
             f'составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, '
             f'с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.77],
            [f'срыв пакера 30мин + 1ч', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [f'Приподнять и посадить пакер на глубине {paker_depth}м',
             None, f'Приподнять и посадить пакер на глубине {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [testing_pressure(self, paker_depth)[1], None,
             testing_pressure(self, paker_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [f'срыв пакера 30мин + 1ч', None,
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
            [f'СПо {paker_select(self)[1]} до глубины {paker_depth}м', None,
             f'Спустить {paker_select(self)[0]} на НКТ{CreatePZ.nkt_diam}мм до глубины {paker_depth}м, '
             f'воронкой до {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном. {nktOpress_list[1]} '
             f'{("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
             f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [None, None, f'Посадить пакер на глубине {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [testing_pressure(self, paker_depth)[1],
             None, testing_pressure(self, paker_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],
            [f'cрыв пакера 30мин +1ч', None,
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

    if len(CreatePZ.dict_leakiness) != 0:
        dict_leakinest_keys = list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys())
        if int(dict_leakinest_keys[0][0]) < paker_depth:

            NEK_question = QMessageBox.question(self, 'Поинтервальная опрессовка НЭК',
                                                'Нужна ли поинтервальная опрессовка НЭК?')
            if NEK_question == QMessageBox.StandardButton.Yes:

                pakerNEK, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                   'Введите глубину посадки пакера для под НЭК',
                                                   int(dict_leakinest_keys[0].split('-')[1]) + 10, 0,
                                                   int(CreatePZ.perforation_sole))
                paker_list = [
                    [f'СПО {paker_select(self)[1]} до глубины {pakerNEK}', None,
                     f'Спустить {paker_select(self)[0]} на НКТ{CreatePZ.nkt_diam}мм до глубины {pakerNEK}м, воронкой '
                     f'до {pakerNEK + paker_khost}м'
                     f' с замером, шаблонированием шаблоном. {nktOpress_list[1]}'
                     f' {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                     f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО'
                     f' КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                     None, None, None, None, None, None, None,
                     'мастер КРС', descentNKT_norm(pakerNEK, 1.2)],
                    [f'Посадить пакер на глубине {pakerNEK}м', None, f'Посадить пакер на глубине {pakerNEK}м',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 0.4],
                    [None, None,
                     f'Опрессовать эксплуатационную колонну в интервале {pakerNEK}-0м на '
                     f'Р={CreatePZ.max_admissible_pressure}атм'
                     f' в течение 30 минуТ в присутствии представителя заказчика, составить акт. '
                     f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                     f'часа до начала работ)',
                     None, None, None, None, None, None, None,
                     'мастер КРС, предст. заказчика', 0.67],
                    [f'Опрессовать  в инт 0-{pakerNEK}м на '
                     f'Р={CreatePZ.max_admissible_pressure}атм. Определение Q',
                     None,
                     f'ПРИ НЕГЕРМЕТИЧНОСТИ: \n Произвести насыщение скважины в объеме 5м3 по затрубному пространству. '
                     f'Определить приемистость '
                     f'НЭК {dict_leakinest_keys[0]} при Р-{CreatePZ.max_admissible_pressure}атм по '
                     f'затрубному пространству'
                     f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                     f'после закачки, объем согласовать с подрядчиком по РИР).',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 1.5],
                    [f'срыв пакера 30мин', None,
                     f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в'
                     f' течении 30мин и с выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                     None, None, None, None, None, None, None,
                     'мастер КРС', 0.7],
                    [None, None,
                     f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения '
                     f'интервала негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, '
                     f'ВЧТ с целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                     f'Определить приемистость НЭК.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', None]]
                ind_nek = 1
                while len(dict_leakinest_keys) - ind_nek != 0:
                    # print('запуск While')

                    pakerNEK1, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                        'Введите глубину посадки пакера для под НЭК',
                                                        int(dict_leakinest_keys[ind_nek].split('-')[1]) + 10, 0,
                                                        int(CreatePZ.current_bottom))
                    pressureNEK_list = [[f'При герметичности колонны в интервале 0 - {pakerNEK}м:  Допустить'
                                         f' пакер до глубины {pakerNEK1}м', None,
                                         f'При герметичности колонны в интервале 0 - {pakerNEK}м:  Допустить'
                                         f' пакер до глубины {pakerNEK1}м',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', descentNKT_norm(pakerNEK1 - pakerNEK, 1.2)],
                                        [f'Опрессовать в '
                                         f'инт 0-{pakerNEK1}м на Р={CreatePZ.max_admissible_pressure}атм',
                                         None,
                                         f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну в '
                                         f'интервале 0-{pakerNEK1}м на Р={CreatePZ.max_admissible_pressure}атм'
                                         f' в течение 30 минуТ в присутствии представителя заказчика, составить акт.',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 0.77],
                                        [f'Насыщение 5м3. Определение Q при Р-{CreatePZ.max_admissible_pressure}', None,
                                         f'ПРИ НЕГЕРМЕТИЧНОСТИ: \n Произвести насыщение скважины в объеме 5м3 по '
                                         f'затрубному пространству. Определить приемистость '
                                         f'НЭК {dict_leakinest_keys[ind_nek]} при Р-{CreatePZ.max_admissible_pressure}'
                                         f'атм по затрубному пространству'
                                         f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль '
                                         f'за отдачей жидкости '
                                         f'после закачки, объем согласовать с подрядчиком по РИР).',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 1.5],
                                        [f'срыв пакера 30мин', None,
                                         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса '
                                         f'НКТ в течении 30мин и с '
                                         f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 0.7]]

                    for i in pressureNEK_list:
                        paker_list.append(i)
                    ind_nek += 1
                    pakerNEK = pakerNEK1

                if len(dict_leakinest_keys) - ind_nek == 0:
                    pressureNEK_list = [[f'При герметичности:  Допустить пакер до '
                                         f'глубины {paker_depth}м', None,
                                         f'При герметичности колонны в интервале 0 - {pakerNEK}м:  Допустить пакер до '
                                         f'глубины {paker_depth}м',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 0.4],
                                        [f'Опрессовать '
                                         f'в инт {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм', None,
                                         f'{nktOpress_list[1]}. Посадить пакер. Опрессовать эксплуатационную колонну '
                                         f'в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                                         f' в течение 30 минуТ в присутствии представителя заказчика, составить акт.',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 0.77],
                                        [f'срыв пакера 30мин', None,
                                         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса '
                                         f'НКТ в течении 30мин и с '
                                         f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                                         None, None, None, None, None, None, None,
                                         'мастер КРС', 0.7],
                                        [None, None,
                                         f'Поднять {paker_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины '
                                         f'{paker_depth}м с доливом скважины в '
                                         f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом '
                                         f'{CreatePZ.fluid_work}',
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


# функция проверки спуска пакера выше прошаблонированной колонны
def check_for_template_paker(self, depth):
    from open_pz import CreatePZ

    check_true = False

    while check_true == False:
        if depth < float(CreatePZ.head_column_additional) and depth <= CreatePZ.template_depth and CreatePZ.column_additional:
            check_true = True
        elif depth > float(CreatePZ.head_column_additional) and depth <= CreatePZ.template_depth_addition and CreatePZ.column_additional:
            check_true = True
        elif depth <= CreatePZ.template_depth and CreatePZ.column_additional is False:
            check_true = True

        if check_true == False:

            false_template = QMessageBox.question(None, 'Проверка глубины пакера',
                                                  f'Проверка показала пакер опускается ниже глубины шаблонирования ЭК'
                                                  f'изменить глубину ?')
            if false_template is QMessageBox.StandardButton.Yes:
                depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                'Введите глубину посадки пакера для опрессовки колонны',
                                                int(CreatePZ.perforation_roof - 20), 0,
                                                int(CreatePZ.current_bottom))
            else:
                check_true = True




    return int(depth), check_true




def testing_pressure(self, depth):
    from open_pz import CreatePZ

    interval_list = []

    for plast in CreatePZ.plast_work:
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            interval_list.append(interval)

    if CreatePZ.leakiness == True:

        for nek in CreatePZ.dict_leakiness['НЭК']['интервал']:
            if nek['отключение'] == False:
                interval_list.append(nek.split('-'))


    if any([float(interval[1]) < float(depth) for interval in interval_list]):
        testing_pressure_str = f'Закачкой тех жидкости в затрубное пространство при Р=' \
                               f'{CreatePZ.max_admissible_pressure}атм' \
                               f' удостоверить в отсутствии выхода тех жидкости и герметичности пакера, составить акт. ' \
                               f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                               f'до начала работ)'
        testing_pressure_short = f'Закачкой в затруб при Р=' \
                               f'{CreatePZ.max_admissible_pressure}атм' \
                               f' удостоверить в герметичности пакера'

    else:

        testing_pressure_str = f'Опрессовать эксплуатационную колонну в интервале {depth}-0м на ' \
                               f'Р={CreatePZ.max_admissible_pressure}атм' \
                               f' в течение 30 минуТ в присутствии представителя заказчика, составить акт. ' \
                               f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа ' \
                               f'до начала работ)'
        testing_pressure_short = f'Опрессовать в {depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'

    return testing_pressure_str, testing_pressure_short













