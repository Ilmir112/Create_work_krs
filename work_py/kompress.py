from PyQt5.QtWidgets import QInputDialog
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from work_py.template_work import well_volume


def kompress(self):

    from open_pz import CreatePZ

    swab_list = ['Задача №2.1.15', 'своя задача']
    swab, ok = QInputDialog.getItem(self, 'Вид освоения', 'Введите задачу при компрессор:', swab_list, 0, False)
    if ok and swab_list:
        self.le.setText(swab)
    swab_volume, ok = QInputDialog.getInt(self, 'объем освоения', 'Введите Объем освоения', 20, 2, 60)

    if swab == 'Задача №2.1.15':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
        swab_select = f'ЗАДАЧА 2.1.5. Определение профиля и состава притока, дебита, источника обводнения и ' \
                      f'технического состояния эксплуатационной колонны при компрессировании' \
                      f' с отбором жидкости не менее {swab_volume}м3. \n' \
                      f'Пробы при освоении отбирать в стандартной таре на {swab_volume - 10}, {swab_volume - 5}, {swab_volume}м3,' \
                      f' своевременно подавать телефонограммы на завоз тары и вывоз проб'


    voronka_depth, ok = QInputDialog.getInt(None, 'глубина воронки',
                                          f'Введите глубину воронки при освоении  ',
                                          int(CreatePZ.perforation_roof - 10), 0,
                                          int(CreatePZ.current_bottom))
    mufta1, ok = QInputDialog.getInt(None, 'глубина муфты',
                                          f'Введите глубину первой муфты',
                                          int(voronka_depth-200), 0,
                                          int(CreatePZ.current_bottom))
    mufta2, ok = QInputDialog.getInt(None, 'глубина муфты',
                                 f'Введите глубину второй муфты',
                                 int(mufta1 - 200), 0,
                                 int(CreatePZ.current_bottom))
    mufta3, ok = QInputDialog.getInt(None, 'глубина муфты',
                                 f'Введите глубину второй муфты',
                                 int(mufta2 - 200), 0,
                                 int(CreatePZ.current_bottom))


    nkt_diam = CreatePZ.nkt_diam

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and voronka_depth < CreatePZ.head_column_additional:
        paker_select = f'воронку + НКТ{nkt_diam} {round(voronka_depth-mufta1)}м + ПМ с отв 3мм + НКТ{nkt_diam} {round(mufta1-mufta2)}м ' \
                       f'+ ПМ с отв 2мм НКТ{nkt_diam} {round(mufta2-mufta3)}м + ПМ с отв 2мм '
        paker_short = f'в-ку + НКТ{nkt_diam} {round(voronka_depth - mufta1)}м + ПМ с отв 3мм + НКТ{nkt_diam} {round(mufta1 - mufta2)}м ' \
                       f'+ ПМ с отв 2мм НКТ{nkt_diam} {round(mufta2 - mufta3)}м + ПМ с отв 2мм '
        dict_nkt = {73: voronka_depth}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and voronka_depth > CreatePZ.head_column_additional:
        paker_select = f'в-ку + НКТ{60} {round(voronka_depth - mufta1)}м + ПМ с отв 3мм + НКТ{nkt_diam} {round(mufta1 - mufta2)}м ' \
                       f'+ ПМ с отв 2мм НКТ{60} {round(mufta2 - mufta3)}м + ПМ с отв 2мм '
        paker_short = f'в-ку + НКТ{60} {round(voronka_depth - mufta1)}м + ПМ с отв 3мм + НКТ{nkt_diam} {round(mufta1 - mufta2)}м ' \
                       f'+ ПМ с отв 2мм НКТ{60} {round(mufta2 - mufta3)}м + ПМ с отв 2мм '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(voronka_depth - CreatePZ.head_column_additional)}

    paker_list = [
        [f'СПО {paker_short} на НКТ{nkt_diam}мм  воронкой до {voronka_depth}м Пусковые муфты на глубине {mufta1}м, {mufta2}м, {mufta3}м', None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм  воронкой до {voronka_depth}м'
         f' с замером, шаблонированием шаблоном. Пусковые муфты на глубине {mufta1}м, {mufta2}м, {mufta3}м,',
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            descentNKT_norm(voronka_depth, 1))],

        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f' Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести  монтаж ГИС согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально ожидаемое давление на устье '
         f'{CreatePZ.max_expected_pressure}атм,'
         f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
         f'сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 1.2],
        [f'Компрессирование', None,
         swab_select,
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчика по ГИС', 30],
        [None, None,
         f'Освоение проводить в емкость для дальнейшей утилизации на НШУ'
         f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', None],

        [f'Промывка скважины  не менее {round(well_volume() * 1.5, 1)}м3', None,
         f' При наличии избыточного давления: '
         f'произвести промывку скважину обратной промывкой ' \
         f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
         f'менее 6-8 л/сек в объеме не менее {round(well_volume() * 1.5, 1)}м3 ' \
         f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
         None, None, None, None, None, None, None,
         'Мастер КРС', well_volume_norm(well_volume())],
        [f'выполнить снятие КВУ в течение часа с интервалом 15 минут',
         None,
         f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
         f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
         f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
         f'или вычислить его расчетным методом.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 0.5],
        [None, None,
         f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {voronka_depth}м с доливом скважины в '
         f'объеме {round(voronka_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС',
         liftingNKT_norm(voronka_depth,1)]
    ]

    return paker_list