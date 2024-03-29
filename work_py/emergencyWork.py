from PyQt5.QtWidgets import QInputDialog

import well_data
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm


def magnet_select(self):

    if well_data.column_additional == False or well_data.column_additional == True and\
            well_data.current_bottom <= well_data.head_column_additional._value:
        magnet_select = f'НКТ{well_data.nkt_diam}мм 20м + репер'

    elif well_data.column_additional == True and well_data.column_additional_diametr._value < 110 and \
            well_data.current_bottom >= well_data.head_column_additional._value:
        magnet_select = f'НКТ60мм 20м + репер + НКТ60мм L- {round(well_data.current_bottom - well_data.head_column_additional._value, 1)}м'
    elif well_data.column_additional == True and well_data.column_additional_diametr._value > 110 and\
            well_data.current_bottom >= well_data.head_column_additional._value:
        magnet_select = f'НКТ{well_data.nkt_diam}мм со снятыми фасками 20м +' \
                        f' НКТ{well_data.nkt_diam}мм со снятыми фасками' \
                        f' L- {round(well_data.current_bottom - well_data.head_column_additional._value, 1)}м'
    return magnet_select


def sbt_select(self):

    if well_data.column_additional == False or well_data.column_additional == True and \
            well_data.current_bottom <= well_data.head_column_additional._value:
        sbt_select = ''

    elif well_data.column_additional == True and well_data.column_additional_diametr._value < 127:
        sbt_select = f'СБТ 2 3/8 L- {round(well_data.current_bottom - well_data.head_column_additional._value,0)}м '

    return sbt_select


def magnetWork(self):

    magnet_list = [
        [f'СПО МАгниТ до '
         f'глубины {well_data.current_bottom}м',
         None,
         f'Спустить магнит-ловитель + опрессовочное седло  +{magnet_select(self)} на тНКТ{well_data.nkt_diam}мм до '
         f'глубины {well_data.current_bottom}м с замером, шаблонированием '
         f'шаблоном {well_data.nkt_template}мм. Опрессовать НКТ на 150атм. Вымыть шар. \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
        [None, None,
         f'Произвести работу магнитом на глубине {well_data.current_bottom}м',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.5],
        [None, None,
         f'Поднять {magnet_select(self)} на тНКТ{well_data.nkt_diam}мм с глубины {well_data.current_bottom}м '
         f'с доливом скважины в объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью '
         f'уд.весом {well_data.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(well_data.current_bottom, 1)],
        [None, None,
         f'ПО результатам ревизии СПО магнита повторить',
         None, None, None, None, None, None, None,
         'мастер КРС', None]
    ]
    return magnet_list


def emergencyECN(self):
    emergency_list = [[None, None,
                       f'При отрицательных результатах по срыву ЭЦН, по согласованию с УСРСиСТ увеличить нагрузку до 33т. '
                       f'При отрицательных результатах:',
                       None, None, None, None, None, None, None,
                       'мастер КРС', None],
                      [None, None,
                       f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
                       f'Составить акт готовности скважины и передать его начальнику партии  ',
                       None, None, None, None, None, None, None,
                       'мастер КРС', None],
                      [f'Произвести запись ПО по НКТ', None,
                       f'Произвести запись ПО по НКТ, по результатам произвести отстрел тНКТ в внемуфтовое соединие в '
                       f'интервале согласованном с УСРСиСТ. Поднять аварийные НКТ до устья. ЗАДАЧА 2.9.3. \n'
                       f'При выявлении отложений солей и гипса, отобрать шлам. Сдать в лабораторию для проведения хим. '
                       f'анализа.',
                       None, None, None, None, None, None, None,
                       'Мастер, подрядчик по ГИС', 12],
                      [None, None,
                       f'Поднять аварийные НКТ до устья. При выявлении отложений солей и гипса, отобрать шлам. '
                       f'Сдать в лабораторию для проведения хим. анализа.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 6.5],
                      [f'Завоз на скважину СБТ', None,
                       f'Завоз на скважину СБТф73мм – Укладка труб на стеллажи.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 6.5],
                      [None, None,
                       f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: Крючки, ВТ-73, ОВ-122, '
                       f'кольцевой фрез (типоразмер согласовать с аварийной службой УСРСиСТ)',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 1.7],
                      ]
    return emergency_list


def emergencyNKT(self):

    emergenceBottom, ok = QInputDialog.getDouble(self, 'Аварийный забой',
                                                 'Введите глубину аварийного забоя:', int(well_data.current_bottom), 2,
                                                 int(well_data.bottomhole_drill._value), 1)
    emergencyNKT_list = [[f'СПо печати до Н={emergenceBottom}м', None,
                          f'Спустить с замером торцевую печать {magnet_select(self)} до Н={emergenceBottom}м '
                          f'(Аварийная голова) с замером.'
                          f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
                          None, None, None, None, None, None, None,
                          'мастер КРС', descentNKT_norm(emergenceBottom, 1)],
                         [None, None,
                          f'Произвести работу печатью на глубине {emergenceBottom}м с обратной промывкой с '
                          f'разгрузкой до 5т.',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 2.5],
                         [None, None,
                          f'Поднять {magnet_select(self)} с доливом тех жидкости в объеме '
                          f'{round(well_data.current_bottom * 1.25 / 1000, 1)}м3 удельным весом {well_data.fluid_work}.',
                          None, None, None, None, None, None, None,
                          'Мастер', liftingNKT_norm(emergenceBottom, 1.2)],
                         [None, None,
                          f'По результату ревизии печати, согласовать с ПТО  и УСРСиСТ и '
                          f'подобрать ловильный инструмент',
                          None, None, None, None, None, None, None,
                          'мастер КРС', None],
                         [None, None,
                          f'Спустить с замером ловильный инструмент НКТ до Н= {emergenceBottom}м с замером . ',
                          None, None, None, None, None, None, None,
                          'мастер КРС', descentNKT_norm(emergenceBottom, 1.2)],
                         [None, None,
                          f'Произвести  ловильные работы при представителе заказчика на глубине {emergenceBottom}м.',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 5.5],
                         [None, None,
                          f'Расходить и извлечь аварийный инструмент.',
                          None, None, None, None, None, None, None,
                          'мастер КРС', liftingNKT_norm(emergenceBottom, 1.2)]]
    well_data.current_bottom, ok = QInputDialog.getDouble(self, 'Текущий забой',
                                                         'Введите Текущий забой после ЛАР',
                                                         well_data.bottomhole_artificial._value, 1,
                                                         well_data.bottomhole_drill._value, 1)
    return emergencyNKT_list


def emergency_hook(self):


    emergency_list = [[f'СПо крючка', None,
                       f'Спустить с замером  удочка ловильная либо крючок (типоразмер согласовать с аварийной службой '
                       f'супервайзинга)'
                       f' на НКТ до "головы" аварийной компоновки, с замером длины труб. (При СПО первых десяти НКТ'
                       f' на спайдере '
                       f'дополнительно устанавливать элеватор ЭХЛ) ',
                       None, None, None, None, None, None, None,
                       'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
                      [None, None,
                       f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
                       f'инструмента  согласовать с аварийной службой супервайзинга.',
                       None, None, None, None, None, None, None,
                       'мастер КРС, УСРСиСТ', 4.5],
                      [None, None,
                       f'Поднять компоновку с доливом тех жидкости в объеме'
                       f' {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
                       f' удельным весом {well_data.fluid_work}.',
                       None, None, None, None, None, None, None,
                       'Мастер, подрядчик по ГИС', liftingNKT_norm(well_data.current_bottom, 1)],
                      [None, None,
                       f'При результатам ревизии поднятого количества кабеля  произвести, по согласованию с аварийной '
                       f'службой супервайзинга, повторить цикл работ - до полного извлечения из скважины '
                       f'кабеля расчётной длины',
                       None, None, None, None, None, None, None,
                       'мастер КРС', None]]

    return emergency_list


def emergence_sbt(self):

    emergence_sbt = [[f'СПО ловильного оборудования ', None,
                      f' По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: ловильного инструмента '
                      f'(типоразмер согласовать с аварийной службой УСРСиСТ) + удлинитель (L=2м) + БП {sbt_select(self)} '
                      f'на СБТ 2 7/8 до глубины нахождения аварийной головы. \n '
                      f'Включение в компоновку ударной компоновки дополнительно согласовать с УСРСиСТ',
                      None, None, None, None, None, None, None,
                      'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
                     [None, None,
                      f'Во избежание срабатывания механизма фиксации плашек в освобожденном положении, спуск '
                      f'следует производить без вращения труболовки',
                      None, None, None, None, None, None, None,
                      'мастер КРС', None],
                     [f'монтаж ведущей трубы', None,
                      f'Произвести монтаж ведущей трубы и мех.ротора.\n '
                      f'За 2-5 метров до верхнего конца аварийного объекта при наличии циркуляции рекомендуется '
                      f'восстановить '
                      f'циркуляцию и промыть скважину тех водой {well_data.fluid_work}. При прокачке промывочной '
                      f'жидкости спустить '
                      f'труболовку до верхнего конца аварийной колонны.\n'
                      f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
                      f'инструмента  согласовать с аварийной службой супервайзинга.'],
                     [None, None,
                      f'Произвести расхаживание аварийной компоновки с постепенным увеличением'
                      f' веса до 50т. Дальнейшие '
                      f'увеличение нагрузки согласовать с УСРСиСТ. При отрицательных '
                      f'результатах произвести освобождение ',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 10],
                     [None, None,
                      f'При положительных результатах расхаживания - демонтаж ведущей трубы и мех.ротора. '
                      f'Поднять компоновку с доливом тех жидкости в '
                      f'объеме {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
                      f' удельным весом {well_data.fluid_work}.',
                      None, None, None, None, None, None, None,
                      'Мастер', liftingNKT_norm(well_data.current_bottom, 1)],
                     [None, None,
                      f'При необходимости: Сборка и спуск компоновки: кольцевой фрезер с удлинителем '
                      f'L= 2,0м + СБТ, до глубины '
                      f'нахождения аварийной "головы"',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', descentNKT_norm(well_data.current_bottom, 1.2)],
                     [None, None,
                      f'Монтаж монтаж ведущей трубы и мех.ротора. Обуривание аварийной головы на глубины согласованной с '
                      f'УСРСиСТ демонтаж мех ротора',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 10],
                     [None, None,
                      f'Поднять компоновку с доливом тех жидкости в объеме {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
                      f' удельным весом {well_data.fluid_work}.',
                      None, None, None, None, None, None, None,
                      'Мастер, подрядчик по ГИС', liftingNKT_norm(well_data.current_bottom, 1)],
                     [None, None,
                      f'По согласованию заказчиком повторить ловильные аварийные работы'
                      f' с подбором аварийного оборудования',
                      None, None, None, None, None, None, None,
                      'Мастер, подрядчик по ГИС', None],
                     [None, None,
                      f'При отрицательном результате дальнейшие работы по дополнительному плану работ',
                      None, None, None, None, None, None, None,
                      'Мастер, подрядчик по ГИС', None]]
    return emergence_sbt


def emergency_sticking(self):

    emergence_type_list = ['ЭЦН', 'пакер', 'НКТ']
    emergence_type, ok = QInputDialog.getItem(self, 'Вид прихватченного оборудования',
                                              'введите вид прихваченного оборудования:', emergence_type_list, 0, False)
    if ok and emergence_type_list:
        self.le.setText(emergence_type)

    emergency_list = [
        [None, None,
         f'При отрицательных результатах по срыву {emergence_type}, по согласованию с '
         f'УСРСиСТ увеличить нагрузку до 33т. При отрицательных результатах:',
         None, None, None, None, None, None, None,
         'Аварийный Мастер КРС, УСРСиСТ', 12],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
         f'Составить акт готовности скважины и передать его начальнику партии',
         None, None, None, None, None, None, None,
         'Мастер, подрядчик по ГИС', None],
        [f' Запись ПО', None,
         f'Произвести запись по определению прихвата по НКТ',
         None, None, None, None, None, None, None,
         'Мастер, подрядчик по ГИС', 8],
        [None, None,
         f'По согласованию с аварийной службой супервайзинга, произвести ПВР - отстрел прихваченной части компоновки '
         f'НКТ с помощью ЗТК-С-54 (2 заряда) (или аналогичным ТРК).'
         f'Работы производить по техническому проекту на ПВР, согласованному с Заказчиком. ЗАДАЧА 2.9.3',
         None, None, None, None, None, None, None,
         'Мастер, подрядчик по ГИС', 5],
        [None, None,
         f'Поднять аварийные НКТ до устья. \nПри выявлении отложений солей и гипса, отобрать шлам. '
         f'Сдать в лабораторию для проведения хим. анализа.',
         None, None, None, None, None, None, None,
         'Мастер КРС', liftingNKT_norm(well_data.dict_nkt, 1.2)],
        [f'Завоз на скважину СБТ', None,
         f'Завоз на скважину СБТ – Укладка труб на стеллажи.',
         None, None, None, None, None, None, None,
         'Мастер', None],
        [None, None,
         f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: удочка ловильная, Метчик,'
         f' Овершот, Внутренние труболовки, кольцевой фрез (типоразмер оборудования согласовать с '
         f'аварийной службой УСРСиСТ)',
         None, None, None, None, None, None, None,
         'Мастер', None]]

    if emergence_type == 'ЭЦН':  # Добавление ловильного крючка при спущенном ЭЦН
        for row in emergency_hook(self):
            emergency_list.append(row)

    seal_list = [[f'СПо печати', None,
                  f'Спустить с замером торцевую печать {magnet_select(self)} до аварийная головы с замером.'
                  f' (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
                  None, None, None, None, None, None, None,
                  'мастер КРС', descentNKT_norm(well_data.current_bottom, 1.2)],
                 [None, None,
                  f'Произвести работу печатью  с обратной промывкой с разгрузкой до 5т.',
                  None, None, None, None, None, None, None,
                  'мастер КРС, УСРСиСТ', 2.5],
                 [None, None,
                  f'Поднять {magnet_select(self)} с доливом тех жидкости в объеме{round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
                  f' удельным весом {well_data.fluid_work}.',
                  None, None, None, None, None, None, None,
                  'Мастер КРС', liftingNKT_norm(well_data.current_bottom, 1.2)],
                 [None, None,
                  f'По результату ревизии печати, согласовать с ПТО  и УСРСиСТ и '
                  f'подобрать ловильный инструмент',
                  None, None, None, None, None, None, None,
                  'мастер КРС', None]]

    for row in seal_list:
        emergency_list.append(row)

    for row in emergence_sbt(self):
        emergency_list.append(row)

    well_data.current_bottom, ok = QInputDialog.getDouble(self, 'Текущий забой',
                                                         'Введите Текущий забой после ЛАР',
                                                         well_data.bottomhole_artificial._value, 1,
                                                         well_data.bottomhole_drill._value, 1)
    return emergency_list


def lapel_tubing(self):


    emergency_list = [[f'Завоз на скважину СБТл', None,
                       f'Завоз на скважину СБТл – Укладка труб на стеллажи.',
                       None, None, None, None, None, None, None,
                       'Мастер', None],
                      [None, None,
                       f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: Метчик,'
                       f' Овершот, Внутренние труболовки',
                       None, None, None, None, None, None, None,
                       'Мастер', None],
                      [f'СПО лов.инстр', None,
                       f' По согласованию с аварийной службой УСРСиСТ, сборка и спуск компоновки: ловильного инструмента '
                       f'(типоразмер согласовать с аварийной службой УСРСиСТ) + '
                       f'удлинитель (L=2м) + БП {sbt_select(self)} '
                       f'на СБТ 2 7/8 (левое) до глубины нахождения аварийной головы. \n '
                       f'Включение в компоновку ударной компоновки дополнительно согласовать с УСРСиСТ',
                       None, None, None, None, None, None, None,
                       'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
                      [f'монтаж ведущей трубы и мех.ротора', None,
                       f'Произвести монтаж ведущей трубы и мех.ротора.\n '
                       f'За 2-5 метров до верхнего конца аварийного объекта рекомендуется восстановить циркуляцию и '
                       f'промыть скважину тех водой {well_data.fluid_work}. При прокачке промывочной жидкости спустить '
                       f'труболовку до верхнего конца аварийной колонны.'
                       f'Произвести ловильные работы на "голове" аварийной компоновки. Количество подходов и оборотов '
                       f'инструмента  согласовать с аварийной службой супервайзинга.',
                       None, None, None, None, None, None, None,
                       'мастер КРС, УСРСиСТ', 4.5],
                      [f'Произвести искусственный отворот ', None,
                       f'Произвести натяжение колонны для заклинивания плашек, затем снизить растягивающую нагрузку на '
                       f'труболовку до значений расчетного веса аварийной компоновки. \n'
                       f'Произвести искусственный отворот '
                       f'аварийных НКТ При отрицательных результатах произвести освобождение',
                       None, None, None, None, None, None, None,
                       'мастер КРС, УСРСиСТ', 10],
                      [None, None,
                       f'При положительных результатах расхаживания - демонтаж ведущей трубы и мех.ротора. '
                       f'Поднять компоновку с доливом тех жидкости в '
                       f'объеме {round(well_data.current_bottom * 1.25 / 1000, 1)}м3'
                       f' удельным весом {well_data.fluid_work}.',
                       None, None, None, None, None, None, None,
                       'Мастер', liftingNKT_norm(well_data.current_bottom, 1)],
                      [None, None,
                       f'При необходимости по согласованию с УСРСиСТ работы повторить',
                       None, None, None, None, None, None, None,
                       'Мастер', None],
                      ]
    for row in emergence_sbt(self):
        emergency_list.append(row)

    return emergency_list
