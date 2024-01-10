from PyQt5.QtWidgets import QInputDialog, QMessageBox

import H2S
import krs
from krs import well_volume
from work_py.alone_oreration import privyazkaNKT
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm


def swabbing_opy(self):
    from open_pz import CreatePZ

    depth_opy, ok = QInputDialog.getInt(self, 'Понижение уровня', 'Введите глубину понижения уровня:', 1000, 0, 3000)
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 or (
            CreatePZ.column_diametr > 110 and CreatePZ.column_additional == True and CreatePZ.head_column_additional < depth_opy == True) else '60'])

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and CreatePZ.current_bottom < CreatePZ.head_column_additional and CreatePZ.head_column_additional > 600:
        paker_select = f'воронку со свабоограничителем + НКТ{nkt_diam}м  + НКТ 10м + репер'
        dict_nkt = {73: depth_opy}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        paker_select = f'воронку со свабоограничителем + НКТ60мм 10м + репер +НКТ60мм {round(CreatePZ.current_bottom - CreatePZ.head_column_additional + 10, 0)}м'
        dict_nkt = {73: CreatePZ.head_column_additional,
                    60: int(CreatePZ.current_bottom - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        paker_select = f'воронку со свабоограничителем+ НКТ{CreatePZ.nkt_diam}мм со снятыми фасками  + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 10м {round(CreatePZ.current_bottom - CreatePZ.head_column_additional + 10, 0)}м'
        dict_nkt = {73: depth_opy}
    elif nkt_diam == 60:
        dict_nkt = {60: depth_opy}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм  до глубины {CreatePZ.current_bottom}м'
         f' с замером, шаблонированием шаблоном. ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [None, None,
         f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  при расходе жидкости 6-8 л/сек '
         f'в присутствии представителя Заказчика в объеме {round(well_volume(self, CreatePZ.current_bottom) * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ ДАВЛЕНИЕ {CreatePZ.max_admissible_pressure}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: 0,5-1,0 ТН',
         None, None, None, None, None, None, None,
         'Мастер КРС, представитель ЦДНГ', 1.5],
        [None, None, f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
                     f'{CreatePZ.fluid_work} до глубины {CreatePZ.current_bottom}м.', None, None, None, None, None,
         None, None,
         'Мастер КРС', None],
        [None, None, f'Приподнять  воронку до глубины {depth_opy + 200}м',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(float(CreatePZ.current_bottom)-(depth_opy + 200),1)],
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
         'Мастер КРС, подрядчик по ГИС', 1.35],
        [None, None,
         f'Фоновая запись. Произвести  опрессовку колонны снижением уровня свабированием по Задаче №2.1.17 Понижение уровня '
         f'до глубины {depth_opy}м, тех отстой 3ч.  КВУ в течение 3 часов после тех.отстоя. Интервал времени между  замерами '
         f'1 час. В случае негерметичности произвести записи по тех карте 2.1.13 с целью определения НЭК',
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчика по ГИС', 20],
        [None, None,
         f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
         f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None]]

    fluid_change_quest = QMessageBox.question(self, 'Смена объема',
                                              'Нужна ли смена удельного веса рабочей жидкости?')
    if fluid_change_quest == QMessageBox.StandardButton.Yes:
        if len(CreatePZ.dict_perforation_project) != 0:
            plast, ok = QInputDialog.getItem(self, 'выбор пласта для расчета ЖГС ', 'выберете пласта для перфорации',
                                             CreatePZ.plast_project, -1, False)
            print(f'раб {plast,CreatePZ.dict_perforation_project}')
            try:
                fluid_new = CreatePZ.dict_perforation_project[plast]['рабочая жидкость']
                expected_pressure = CreatePZ.dict_perforation_project[plast['давление']]
            except:
                expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                               'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
                fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                       'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        else:
            plast, ok = QInputDialog.getText(self, 'выбор пласта для расчета ЖГС ', 'введите пласт для перфорации')

            expected_pressure, ok = QInputDialog.getDouble(self, 'Ожидаемое давление по пласту',
                                                           'Введите Ожидаемое давление по пласту', 0, 0, 300, 1)
            fluid_new, ok = QInputDialog.getDouble(self, 'Новое значение удельного веса жидкости',
                                                   'Введите значение удельного веса жидкости', 1.02, 1, 1.72, 2)
        if len(CreatePZ.plast_work) == 0 and len(CreatePZ.cat_H2S_list) > 1:
            if '2' in str(CreatePZ.cat_H2S_list[1]):
                CreatePZ.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                      f'расчета {H2S.calv_h2s(self, CreatePZ.cat_H2S_list[1], CreatePZ.H2S_mg[1], CreatePZ.H2S_pr[1])}кг/м3 '
            else:
                CreatePZ.fluid_work = f'{fluid_new}г/см3 '

        if len(CreatePZ.cat_H2S_list) == 1:
            CreatePZ.cat_H2S_list.append(
                QInputDialog.getInt(self, 'Категория', 'Введите категорию скважины по H2S на вскрываемый пласт', 2,
                                    1, 3))
            CreatePZ.H2S_pr.append(float(
                QInputDialog.getDouble(self, 'Сероводород', 'Введите содержание сероводорода в %', 50, 0, 1000, 2)[
                    0]))
            CreatePZ.H2S_mg.append(float(
                QInputDialog.getDouble(self, 'Сероводород', 'Введите содержание сероводорода в мг/л', 50, 0, 1000,
                                       2)[0]))

        if ('2' in str(CreatePZ.cat_H2S_list[1]) or '1' in str(CreatePZ.cat_H2S_list[1])) and (
                '2' not in str(CreatePZ.cat_H2S_list[0]) or '1' not in str(CreatePZ.cat_H2S_list[0])):
            CreatePZ.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {H2S.calv_h2s(self, CreatePZ.cat_H2S_list[1], CreatePZ.H2S_mg[1], CreatePZ.H2S_pr[1])}кг/м3 '
        elif ('2' in str(CreatePZ.cat_H2S_list[0]) or '1' in str(CreatePZ.cat_H2S_list[0])) and (
                '2' not in str(CreatePZ.cat_H2S_list[1]) or '1' not in str(CreatePZ.cat_H2S_list[1])):
            CreatePZ.fluid_work = f'{fluid_new}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                                  f'расчета {H2S.calv_h2s(self, CreatePZ.cat_H2S_list[0], CreatePZ.H2S_mg[0], CreatePZ.H2S_pr[0])}кг/м3 '
        else:
            CreatePZ.fluid_work = f'{fluid_new}г/см3 '


        fluid_change_list = [[None, None,
                              f'Допустить до {CreatePZ.current_bottom}м. Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {CreatePZ.fluid_work} '
                              f'(по расчету по вскрываемому пласта {plast} Рожид- {expected_pressure}атм) в объеме не '
                              f'менее {round(krs.well_volume(self, CreatePZ.current_bottom), 1)}м3  в присутствии представителя заказчика, Составить акт. '
                              f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
                              None, None, None, None, None, None, None,
                              'мастер КРС', round(well_volume_norm(well_volume(self, CreatePZ.current_bottom)) +  descentNKT_norm(CreatePZ.current_bottom-depth_opy-200, 1),1)],
                             [None, None,
                              f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {CreatePZ.current_bottom}м с доливом скважины в '
                              f'объеме {round((CreatePZ.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                              None, None, None, None, None, None, None,
                              'мастер КРС',
                              liftingNKT_norm(CreatePZ.current_bottom,1)]
                             ]

        for row in fluid_change_list:
            paker_list.append(row)
    else:
        paker_list.append([None, None,
                           f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {depth_opy + 200}м с доливом скважины в '
                           f'объеме {round((depth_opy + 200) * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                           None, None, None, None, None, None, None,
                           'мастер КРС',
                           liftingNKT_norm(depth_opy + 200, 1)])
    return paker_list


def swabbing_with_paker(self, paker_khost, pakerKompo):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select

    swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при свабе:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля ' \
                      f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                      f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.16':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и ' \
                      f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения ' \
                      f'свабированием  не менее не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.11':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                      f'менее  {swab_volume}м3. \n ' \
                      f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                      f'Обязательная сдача в этот день в ЦДНГ'

    paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки пакера при освоении для перфорации ',
                                          int(CreatePZ.perforation_roof - 40), 0,
                                          5000)

    paker_khost1 = int(CreatePZ.perforation_sole - paker_depth)
    print(f'хвостовик {paker_khost1}')
    if pakerKompo == 1:
        paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
                                              f'Введите длину хвостовика кровли ИП{CreatePZ.perforation_roof} и глубины посадки пакера {paker_depth}',
                                              10, 0, 4000)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 or (
                CreatePZ.column_diametr > 110 and CreatePZ.column_additional == True and CreatePZ.head_column_additional > 700) else '60'])

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional and CreatePZ.head_column_additional > 600:
        paker_select = f'воронку со свабоограничителем + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м'
        dict_nkt = {73: paker_depth + paker_khost}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронку со свабоограничителем+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker_depth - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронку со свабоограничителем+ НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 10м'
        dict_nkt = {73: paker_depth + paker_khost}
    elif nkt_diam == 60:
        dict_nkt = {60: paker_depth + paker_khost}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м'
         f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
         f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(paker_depth,1.2)],
        [None, None, f'Посадить пакер на глубине {paker_depth}м, воронку на глубине {paker_khost + paker_depth}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
         f' в течение 30 минут в присутствии представителя заказчика, составить акт.  '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 0.67],

        [None, None,
         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
         f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
         f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
         f'Определить приемистость НЭК.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f' Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье {CreatePZ.max_expected_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 1.3],
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
         liftingNKT_norm(paker_depth, 1.2)]
    ]
    ovtr = 'ОВТР 4ч' if CreatePZ.region == 'ЧГМ' else 'ОВТР 10ч'
    ovtr4 = 4 if CreatePZ.region == 'ЧГМ' else 10
    if swab == 'Задача №2.1.13' and CreatePZ.region not in ['ИГМ']:
        paker_list.insert(3, [None, None, ovtr,
                              None, None, None, None, None, None, None,
                              'мастер КРС', ovtr4])
    if pakerKompo == 2:
        paker_list[1] = [None, None, f'Посадить пакера на глубине {paker_depth}/{paker_depth - paker_khost}м'
            ,
                         None, None, None, None, None, None, None,
                         'мастер КРС', 0.4]
    # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - paker_depth)) < 10 or abs(float(interval[0] - paker_depth)) < 10:
                if privyazkaNKT(self) not in paker_list and CreatePZ.privyazkaSKO == 0:
                    CreatePZ.privyazkaSKO += 1
                    paker_list.insert(1, privyazkaNKT(self))

    return paker_list


def swabbing_with_2paker(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select

    swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при свабе:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля ' \
                      f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                      f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.16':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и ' \
                      f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения ' \
                      f'свабированием  не менее не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.11':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                      f'менее  {swab_volume}м3. \n ' \
                      f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                      f'Обязательная сдача в этот день в ЦДНГ'

    paker1_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки НИЖНЕГО пакера при освоении для перфорации ',
                                          int(CreatePZ.perforation_sole + 10), 0,
                                          5000)
    paker2_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки ВВЕРХНЕГО пакера при освоении для перфорации ',
                                          int(CreatePZ.perforation_roof - 10), 0,
                                          5000)


    paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
                                              f'Введите длину хвостовика кровли ИП{CreatePZ.perforation_roof} и глубины посадки пакера {paker1_depth}',
                                              10, 0, 4000)

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 or (
                CreatePZ.column_diametr > 110 and CreatePZ.column_additional == True and CreatePZ.head_column_additional > 700) else '60'])

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker1_depth < float(CreatePZ.head_column_additional) and  float(CreatePZ.head_column_additional) > 600:
        paker_select = f'заглушка + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker1_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр + ' \
                       f'НКТ l-{round(paker1_depth-paker2_depth,0)} + пакер ПУ для ЭК ' \
                       f'{CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ{nkt_diam} 20мм + репер'
        dict_nkt = {73: paker1_depth + paker_khost}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker1_depth > float(CreatePZ.head_column_additional):
        paker_select = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker1_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр + ' \
                       f'НКТ l-{round(paker1_depth-paker2_depth,0)} + НКТ{60} 20мм + репер + НКТ60мм {round(float(CreatePZ.head_column_additional) - paker2_depth,0)}м '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker1_depth - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker1_depth > CreatePZ.head_column_additional:
        paker_select = f'заглушка + НКТ{73}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker1_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр + ' \
                       f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + НКТ{73}мм со снятыми фасками 20мм + репер + НКТ{73}мм со снятыми фасками {round(float(CreatePZ.head_column_additional) - paker2_depth, 0)}м '
        dict_nkt = {73: paker1_depth + paker_khost}
    elif nkt_diam == 60:
        dict_nkt = {60: paker1_depth + paker_khost}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм до глубины {paker1_depth}/{paker2_depth}м'
         f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
         f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(paker1_depth,1.2)],
        [None, None, f'Посадить пакера на глубине {paker1_depth}/{paker2_depth}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Опрессовать эксплуатационную колонну в интервале {paker2_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
         f' в течение 30 минут в присутствии представителя заказчика, составить акт.  '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 0.67],

        [None, None,
         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
         f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
         f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
         f'Определить приемистость НЭК.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f' Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье {CreatePZ.max_expected_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 1.3],
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
         f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker1_depth) * 1.5, 1)}м3 ' \
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
         f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker1_depth}м с доливом скважины в '
         f'объеме {round(paker1_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС',
         liftingNKT_norm(paker1_depth, 1.2)]
    ]

    # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - paker1_depth)) < 10 or abs(float(interval[0] - paker1_depth)) < 10:
                if privyazkaNKT(self) not in paker_list and CreatePZ.privyazkaSKO == 0:
                    CreatePZ.privyazkaSKO += 1
                    paker_list.insert(1, privyazkaNKT(self))

    return paker_list



def swabbing_with_voronka(self):
    from open_pz import CreatePZ

    swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при свабе:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.13 Определение профиля ' \
                      f'и состава притока, дебита, источника обводнения и технического состояния эксплуатационной колонны и НКТ ' \
                      f'после свабирования с отбором жидкости не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.16':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.16 Определение дебита и ' \
                      f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного давления после освоения ' \
                      f'свабированием  не менее не менее {swab_volume}м3. \n' \
                      f'Пробы при свабировании отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
    elif swab == 'Задача №2.1.11':
        swab_select = f'Произвести  геофизические исследования по технологической задаче № 2.1.11  свабирование в объеме не ' \
                      f'менее  {swab_volume}м3. \n ' \
                      f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба (объем не менее 10литров).' \
                      f'Обязательная сдача в этот день в ЦДНГ'

    paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          f'Введите глубину посадки пакера при освоении для перфорации ',
                                          int(CreatePZ.perforation_roof - 40), 0,
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
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье '
         f'{CreatePZ.max_expected_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 1.2],
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
         'Мастер КРС', well_volume_norm(well_volume(self, paker_depth))],
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
         liftingNKT_norm(paker_depth, 1)]
    ]
    ovtr = 'ОВТР 4ч' if CreatePZ.region == 'ЧГМ' else 'ОВТР 10ч'
    ovtr4 = 4 if CreatePZ.region == 'ЧГМ' else 10
    if swab == 'Задача №2.1.13' and CreatePZ.region not in ['ИГМ']:
        paker_list.insert(1, [None, None, ovtr,
                              None, None, None, None, None, None, None,
                              'мастер КРС', ovtr4])
    return paker_list
