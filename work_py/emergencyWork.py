from PyQt5.QtWidgets import QInputDialog


def magnet_select(self):
    from open_pz import CreatePZ
    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and CreatePZ.current_bottom <= CreatePZ.head_column_additional:
        magnet_select = f'магнит-ловитель + опрессовочное седло + НКТ{CreatePZ.nkt_diam} 20м + репер'

    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and CreatePZ.current_bottom > CreatePZ.head_column_additional:
        magnet_select = f'перо + опрессовочное седло + НКТ60мм 20м + репер + НКТ60мм L- {CreatePZ.current_bottom - CreatePZ.head_column_additional}м'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and CreatePZ.current_bottom > CreatePZ.head_column_additional:
        magnet_select = f'воронку + опрессовочное седло + НКТ73мм со снятыми фасками 20м + НКТ73мм со снятыми фасками' \
                      f' L- {CreatePZ.current_bottom - CreatePZ.head_column_additional}м'
    return magnet_select

def magnetWork(self):
    from open_pz import CreatePZ
    magnet_list = [
        [None, None,
     f'Спустить {magnet_select(self)}  на тНКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м с замером, шаблонированием '
     f'шаблоном. Опрессовать НКТ на 150атм. Вымыть шар. \n'
     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
     None, None, None, None, None, None, None,
     'мастер КРС', 2.5],
        [None, None,
         f'Произвести работу магнитом на глубине {CreatePZ.current_bottom}м',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.5],
        [None, None,
         f'Поднять {magnet_select(self)} на тНКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.current_bottom}м '
         f'с доливом скважины в объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'ПО результатам ревизии СПО магнита повторить',
         None, None, None, None, None, None, None,
         'мастер КРС', None]
    ]
    return magnet_list


def emergencyECN(self):
    emergency_list = [[None, None,
         f'При отрицательных результатах по срыву ЭЦН, по согласованию с УСРСиСТ увеличить нагрузку до 33т.При отрицательных результатах:',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
                      [None, None,
                       f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". Составить акт готовности скважины и передать его начальнику партии  ',
                       None, None, None, None, None, None, None,
                       'мастер КРС', None],
                      [None, None,
                       f'Произвести запись ПО по НКТ, по результатам произвести отстрел тНКТ в внемуфтовое соединие в интервале согласованном с УСРСиСТ. '
                       f'Поднять аварийные НКТ до устья. ЗАДАЧА 2.9.3. \nПри выявлении отложений солей и гипса, отобрать шлам. Сдать в лабораторию для проведения хим. анализа.',
                       None, None, None, None, None, None, None,
                       'Мастер, подрядчик по ГИС', 12],
                      [None, None,
                       f'Поднять аварийные НКТ до устья. При выявлении отложений солей и гипса, отобрать шлам. Сдать в лабораторию для проведения хим. анализа.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 6.5],
                      [None, None,
                       f'Завоз на скважину СБТф73мм – Укладка труб на стеллажи.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 6.5],
                      [None, None,
                       f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: Крючки, ВТ-73, ОВ-122, кольцевой фрез (типоразмер согласовать с аварийной службой УСРСиСТ)',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 1.7],
                      [None, None,
                       f'Завоз на скважину инструмента для проведения аварийно-ловильных работ: Крючки, ВТ-73, ОВ-122, кольцевой фрез (типоразмер согласовать с аварийной службой УСРСиСТ)',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 1.7],
    ]
    return emergency_list

def emergencyNKT(self):
    from open_pz import  CreatePZ
    emergenceBottom, ok  = QInputDialog.getDouble(self, 'Аварийный забой',
                                  'Введите глубину аварийного забоя:', int(CreatePZ.current_bottom), 2, int(CreatePZ.bottomhole_drill),1)
    emergencyNKT_list = emergency_list = [[None, None,
         f'Спустить с замером торцевую печать на НКТ до Н={emergenceBottom}м (Аварийная голова) с замером . (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
                      [None, None,
                       f'Произвести работу печатью на глубине {emergenceBottom}м с обратной промывкой с разгрузкой до 5т.',None, None, None, None, None, None, None,
                       'мастер КРС', None],
                      [None, None,
                       f'Поднять компоновку с доливом тех жидкости в объеме 1,8м3.',
                       None, None, None, None, None, None, None,
                       'Мастер, подрядчик по ГИС', 6],
                      [None, None,
                       f'По результату ревизии печати, согласовать с ПТО  и УСРСиСТ  ООО "Башнефть-добыча" и подобрать ловильный инструмент',
                       None, None, None, None, None, None, None,
                       'мастер КРС', None],
                      [None, None,
                       f'Спустить с замером ловильный инструмент НКТдо Н= {emergenceBottom}м с замером . ',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 6.5],
                      [None, None,
                       f'Произвести  ловильные работы при представителе заказчика на глубине {emergenceBottom}м.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 1.7],
                      [None, None,
                       f'Рассхадить и извлечь аварийный инструмент.',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 7.2]]
    CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Текущий забой',
                                                         'Введите Текущий забой после ЛАР', CreatePZ.bottomhole_artificial, 1,
                                                         CreatePZ.bottomhole_drill, 1)
    return emergencyNKT_list

