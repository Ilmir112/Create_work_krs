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

