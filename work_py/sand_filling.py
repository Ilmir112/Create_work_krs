from PyQt5.QtWidgets import QInputDialog, QMessageBox
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm




def sand_select(self):
    from open_pz import CreatePZ
    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and CreatePZ.current_bottom <= CreatePZ.head_column_additional):
        sand_select = f'перо +  НКТ{CreatePZ.nkt_diam}мм 20м + реперный патрубок'

    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        sand_select = f'перо + НКТ{60}мм 20м + реперный патрубок + НКТ60мм {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м '
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and CreatePZ.current_bottom >= CreatePZ.head_column_additional:
        sand_select = f'перо + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {20}м + реперный патрубок + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками {round(CreatePZ.current_bottom - CreatePZ.head_column_additional, 0)}м'
    return sand_select

def sandFilling(self):
    from open_pz import CreatePZ
    from krs import well_volume, volume_vn_ek
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])


    filling_depth, ok = QInputDialog.getInt(None, 'Отсыпка песком',
                                          'Введите кровлю необходимого песчанного моста',
                                          int(CreatePZ.perforation_roof - 20), 0, int(CreatePZ.current_bottom))


    sand_volume = round(volume_vn_ek(self,filling_depth) * (CreatePZ.current_bottom - filling_depth), 1)


    filling_list = [
        [f'Спустить  {sand_select(self)}  на НКТ{nkt_diam}мм до глубины {round(CreatePZ.current_bottom-100,0)}м', None,
     f' Спустить  {sand_select(self)}  на НКТ{nkt_diam}мм до глубины {round(CreatePZ.current_bottom-100,0)}м с замером, '
     f'шаблонированием шаблоном {CreatePZ.nkt_template}мм. (При СПО первых десяти НКТ на '
     f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
     None, None, None, None, None, None, None,
     'Мастер КР', descentNKT_norm(CreatePZ.current_bottom,1)],
        [f'отсыпка кварцевым песком в инт. {filling_depth} - {CreatePZ.current_bottom} в объеме {sand_volume}л',
         None, f'Произвести отсыпку кварцевым песком в инт. {filling_depth} - {CreatePZ.current_bottom} '
                     f' в объеме {sand_volume}л '
                     f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', 3.5],
        [f'Ожидание оседания песка 4 часа.',
         None, f'Ожидание оседания песка 4 часа.',
         None, None, None, None, None, None, None,
         'мастер КРС', 4],
        [None, None, f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста (плановый забой - {filling_depth}м).'
                     f' Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". При необходимости '
         f'подготовить место для установки партии ГИС напротив мостков. Произвести  монтаж ГИС согласно схемы  №8 при '
         f'привязке утвержденной главным инженером оТ 14.10.2021г.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [f'Привязка ', None,
         f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4],
        [f'Определение кровли', None,
         f'В случае если кровля песчаного моста на гл.{filling_depth}м дальнейшие работы продолжить дальше по плану'
         f'В случае пеcчаного моста ниже гл.{filling_depth}м работы повторить с корректировкой обьема и технологических глубин.'
         f' В случае песчаного моста выше гл.{filling_depth}м вымыть песок до гл.{filling_depth}м',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Поднять {sand_select(self)} НКТ{nkt_diam}мм с глубины {filling_depth}м с доливом скважины в объеме {round(filling_depth * 1.12/1000,1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(filling_depth,1)]
    ]
    if CreatePZ.leakiness == False and CreatePZ.perforation_roof > filling_depth:
        filling_list.insert(-1,
                            [f'Опрессовать в инт{filling_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм',
                             None, f'Опрессовать эксплуатационную колонну в интервале {filling_depth}-0м на'
                                   f'Р={CreatePZ.max_admissible_pressure}атм'
                     f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
                     f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа'
                                   f' до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 0.67])
        filling_list.insert(-1,
                            [None, None,
                     f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                     f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                     f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                     f'Определить приемистость НЭК.',
                     None, None, None, None, None, None, None,
                     'мастер КРС', None] )
    gis_true_quest = QMessageBox.question(self, 'привязка компоновки',
                                          'Нужно ли привязывать компоновку?')

    if gis_true_quest == QMessageBox.StandardButton.Yes:
        pass
    else:
        filling_list.pop(5)
        filling_list.pop(4)


    CreatePZ.current_bottom = filling_depth

    return filling_list

def sandWashing(self):
    from open_pz import CreatePZ
    from krs import volume_vn_nkt
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])



    washingDepth, ok = QInputDialog.getDouble(None, 'вымыв песка',
                                                'Введите глубину вымыва песчанного моста',
                                                CreatePZ.current_bottom, 0, 6000, 1)
    washingOut_list = [
        [f'СПО пера до {round(CreatePZ.current_bottom,0)}м', None,
     f' Спустить  {sand_select(self)}  на НКТ{nkt_diam}мм до глубины {round(CreatePZ.current_bottom,0)}м с замером, '
     f'шаблонированием шаблоном {CreatePZ.nkt_template}мм. '
     f'(При СПО первых десяти НКТ на '
     f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
     None, None, None, None, None, None, None,
     'Мастер КР', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [f'вымыв песка до {washingDepth}м',
         None, f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной  промывкой по круговой циркуляции '
                     f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{washingDepth}м. \n'
                     f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
         None, None, None, None, None, None, None,
         'мастер КРС', 3.5],
        [None, None,
         f'Поднять {sand_select(self)} НКТ{nkt_diam}мм с глубины {washingDepth}м с доливом скважины в объеме {round(washingDepth * 1.12 / 1000, 1)}м3 тех. '
         f'жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(washingDepth, 1.2)]]
    CreatePZ.current_bottom = washingDepth

    return washingOut_list