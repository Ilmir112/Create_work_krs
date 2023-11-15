def kot_select(self):
    from open_pz import CreatePZ
    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and CreatePZ.current_bottom> CreatePZ.head_column_additional:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{CreatePZ.nkt_diam}мм 10м + репер '
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and CreatePZ.current_bottom> CreatePZ.head_column_additional:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{60}мм 10м + репер + НКТ60мм L- {round(CreatePZ.current_bottom-CreatePZ.head_column_additional,0)}м'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and CreatePZ.current_bottom> CreatePZ.head_column_additional:
        kot_select = f'КОТ-50 (клапан обратный тарельчатый) +НКТ{73}мм со снятыми фасками 10м + репер + НКТ73мм со снятыми фасками' \
                       f' L- {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м'

    return kot_select

def kot_work(self):
    from open_pz import CreatePZ


    kot_list = [[None, None,
                   f'Спустить {kot_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины {CreatePZ.current_bottom}м'
                   f' с замером, шаблонированием шаблоном.',
    None, None, None, None, None, None, None,
    'мастер КРС', round(
        CreatePZ.current_bottom / 9.52 * 1.51 / 60 * 1.2 *1.2* 1.04 + 0.18 + 0.008 * CreatePZ.current_bottom / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
        2)],
        [None, None, f'Произвести очистку забоя скважины до гл.{CreatePZ.current_bottom}м закачкой обратной промывкой тех жидкости уд.весом {CreatePZ.fluid_work}, по согласованию с Заказчиком',
                   None, None, None, None, None, None, None,
                   'мастер КРС', 0.4],
        [None, None, f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1],

        [None, None,
         f'Поднять {kot_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {CreatePZ.current_bottom}м с доливом скважины в '
         f'объеме {round(CreatePZ.current_bottom*1.12/1000,1)}м3 удельным весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', round(0.25+0.033*1.2*(CreatePZ.current_bottom)/9.5*1.04,1) ]
    ]
    return kot_list

