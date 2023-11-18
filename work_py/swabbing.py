from PyQt5.QtWidgets import QInputDialog

from krs import well_volume


def swabbing_with_paker(self, paker_khost, pakerKompo):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select

    swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при свабе:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab ==  'Задача №2.1.13':#, 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля '\
         f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ '\
         f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n'\
         f'Пробы при свабировании отбирать в стандартной таре на {swab_volume-10}, {swab_volume-5}, {swab_volume}м3,' \
          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.16':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и '\
                       f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения '\
                       f'свабированием  не менее не менее {swab_volume}м3. \n'\
                       f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.11':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                      f'менее  {swab_volume}м3. \n ' \
                      f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                      f'Обязательная сдача в этот день в ЦДНГ'

    paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки пакера при освоении для перфорации {CreatePZ.dict_work_pervorations}', int(CreatePZ.perforation_roof - 40), 0,
                                          5000)
    paker_khost1 = int(CreatePZ.perforation_sole - paker_depth)
    print(f'хвостовик {paker_khost1}')
    # paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
    #                                       f'Введите длину хвостовика кровли ИП{CreatePZ.perforation_roof} и глубины посадки пакера {paker_depth}',
    #                                       10, 0, 4000)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м'
        dict_nkt = {73: paker_depth + paker_khost}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker_depth - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ73мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ73мм со снятыми фасками 10м'
        dict_nkt = {73: paker_depth + paker_khost}
    elif nkt_diam == 60:
        dict_nkt = {60: paker_depth + paker_khost}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м'
         f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
         f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            CreatePZ.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008 * CreatePZ.current_bottom / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
            2)],
        [None, None, f'Посадить пакер на глубине {paker_depth}м, воронку на глубине {paker_khost+paker_depth}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
         f' в течение 30 минут в присутствии представителя заказчика, составить акт.  '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1.],

        [None, None,
         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
         f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
         f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
         f'Определить приемистость НЭК.',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f' Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье {CreatePZ.max_admissible_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None],
        [None, None,
         swab_select,
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчика по ГИС', 30],
        [None, None,
         f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
         f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None],

        [None, None,
         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
         f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
         f'произвести промывку скважину обратной промывкой ' \
         f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
         f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 1.26],
        [None, None,
         f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
         f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
         f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
         f'или вычислить его расчетным методом.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 0.5],
        [None, None,
           f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
           f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
           None, None, None, None, None, None, None,
           'мастер КРС',
           round(0.25 + 0.033 * 1.2 * (paker_depth + paker_khost) / 9.5 * 1.04, 1)]
    ]
    if pakerKompo == 2:
        paker_list[2] = [None, None, f'Посадить пакера на глубине {paker_depth}/{paker_khost}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4]
    return paker_list

def swabbing_with_voronka(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select

    swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при свабе:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab ==  'Задача №2.1.13':#, 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля '\
         f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ '\
         f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n'\
         f'Пробы при свабировании отбирать в стандартной таре на {swab_volume-10}, {swab_volume-5}, {swab_volume}м3,' \
          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.16':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и '\
                       f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения '\
                       f'свабированием  не менее не менее {swab_volume}м3. \n'\
                       f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.11':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                      f'менее  {swab_volume}м3. \n ' \
                      f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                      f'Обязательная сдача в этот день в ЦДНГ'

    paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки пакера при освоении для перфорации {CreatePZ.dict_work_pervorations}', int(CreatePZ.perforation_roof - 40), 0,
                                          5000)
    paker_khost1 = int(CreatePZ.perforation_sole - paker_depth)
    print(f'хвостовик {paker_khost1}')
    # paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
    #                                       f'Введите длину хвостовика кровли ИП{CreatePZ.perforation_roof} и глубины посадки пакера {paker_depth}',
    #                                       10, 0, 4000)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional:
        paker_select = f'воронку + со свабоограничителем НКТ{nkt_diam}м +репер + НКТ 10м'
        dict_nkt = {73: paker_depth}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{60}мм  + НКТ60мм 10м '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker_depth - CreatePZ.head_column_additional)}
    # elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth > CreatePZ.head_column_additional:
    #     paker_select = f'воронку + НКТ73мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
    #                    f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ73мм со снятыми фасками 10м'
    #     dict_nkt = {73: paker_depth + paker_khost}
    # elif nkt_diam == 60:
    #     dict_nkt = {60: paker_depth + paker_khost}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм  воронкой до {paker_depth}м'
         f' с замером, шаблонированием шаблоном. ',
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            CreatePZ.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008 * paker_depth / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
            2)],

        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f' Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье {CreatePZ.max_admissible_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None],
        [None, None,
         swab_select,
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчика по ГИС', 30],
        [None, None,
         f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
         f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None],

        [None, None,
         f' При наличии избыточного давления: '
         f'произвести промывку скважину обратной промывкой ' \
         f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
         f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 1.26],
        [None, None,
         f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
         f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
         f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
         f'или вычислить его расчетным методом.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 0.5],
        [None, None,
           f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
           f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
           None, None, None, None, None, None, None,
           'мастер КРС',
           round(0.25 + 0.033 * 1.2 * (paker_depth) / 9.5 * 1.04, 1)]
    ]

    return paker_list
