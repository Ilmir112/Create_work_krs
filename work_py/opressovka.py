from PyQt5.QtWidgets import QInputDialog


def paker_diametr_select(depth_landing):
    from open_pz import CreatePZ

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and depth_landing < CreatePZ.head_column_additional):
        diam_internal_ek = CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness
    else:
        diam_internal_ek = CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness

    for diam, diam_internal_paker in CreatePZ.paker_diam_dict.items():
        if diam_internal_paker[0] <= diam_internal_ek << diam_internal_paker[1]:
            return diam
# Добавление строк с опрессовкой ЭК
def paker_list():
    from open_pz import CreatePZ
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    paker_depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                      'Введите глубину посадки пакера', 500, 0, 10000)
    paker_khost, ok = QInputDialog.getInt(None, 'опрессовка ЭК', 'Введите длину хвостовика', 10, 0, 3000)

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth< CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth> CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м '
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth> CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ73мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ73мм со снятыми фасками 10м'

    paker_list = [
        [None, None,
                   f'Спустить {paker_select} на НКТ{nkt_diam} до глубины {paker_depth}, воронкой до {paker_depth+ paker_khost}'
                    f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
                   f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                   f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
     None, None, None, None, None, None, None,
     'мастер КРС', round(
        CreatePZ.current_bottom / 9.52 * 1.51 / 60 * 1.2 *1.2* 1.04 + 0.18 + 0.008 * CreatePZ.current_bottom / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
        2)],
        [None, None, f'Посадить пакер на глубине {paker_depth}м'
                   ,
                   None, None, None, None, None, None, None,
                   'мастер КРС', 0.4],
        [None, None, f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
                     f' в течение 30 минут {["на наличие перетоков " if len(CreatePZ.leakiness) != 0 and min(CreatePZ.leakiness[0]) <= paker_depth else " "]} в присутствии представителя заказчика, составить акт.  '
                     f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1.],
        [None, None, f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                     f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                     f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                     f'Определить приемистость НЭК.',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
         f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.7],
        [None, None,
         f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
         f'объеме {round(paker_depth*1.12/1000,1)}м3 удельным весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', round(0.25+0.033*1.2*(paker_depth+paker_khost)/9.5*1.04,1) ]]



