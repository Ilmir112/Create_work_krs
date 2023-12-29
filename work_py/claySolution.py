from PyQt5.QtWidgets import QInputDialog, QMessageBox

from krs import volume_vn_ek, volume_vn_nkt
from work_py.rationingKRS import descentNKT_norm
from work_py.rir import rirWithPero


def claySolutionDef(self):
    from open_pz import CreatePZ
    from work_py.rir import pero_select
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])


    rirSole, ok = QInputDialog.getInt(None, 'Подошва глинистого раствора',
                                      'Введите глубину глинистого раствора ',
                                      int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_drill))
    rirRoof, ok = QInputDialog.getInt(None, 'Кровля глинистого раствора',
                                      'Введите глубину глинистого раствора',
                                      int(CreatePZ.perforation_sole +20), 0, int(CreatePZ.bottomhole_drill))
    if CreatePZ.column_additional == True and CreatePZ.column_additional_diametr <110:
        dict_nkt = {73: CreatePZ.head_column_additional, 60: CreatePZ.head_column_additional-rirSole}
    else:
        dict_nkt = {73: rirSole}


    volume_cement = round(volume_vn_ek(self, rirRoof) * (rirSole - rirRoof)/1000, 1)
    dict_nkt = {73: rirRoof}
    pero_list = [
        [None, None,
         f'Спустить {pero_select(self, rirSole)}  на тНКТ{nkt_diam}мм до глубины {rirSole}м с замером, шаблонированием '
         f'шаблоном.  \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС',descentNKT_norm(rirSole, 1)],
        [None, None,
         f'Произвести закачку глинистого раствора с добавлением ингибитора коррозии {round(volume_cement*11,1)}гр с удельной дозировкой 11гр/м3 '
         f'удельным весом не менее 1,24г/см3 в интервале {rirSole}-{rirRoof}м.\n'
         f'- Приготовить и закачать в глинистый раствор уд.весом не менее 1,24г/см3 в объеме {volume_cement}м3 ({round(volume_cement*0.45,2)}т'
         f' сухого порошка).\n'
         f'-Продавить тех жидкостью  в объеме {volume_vn_nkt(dict_nkt)}м3.',
         None, None, None, None, None, None, None,
         'мастер КРС', 2.5]]
    CreatePZ.current_bottom = rirRoof
    rirPlan_quest = QMessageBox.question(self, 'Планировать ли РИР', 'Нужно ставить "висящий" мост в колонне')
    if rirPlan_quest  == QMessageBox.StandardButton.No:
        pero_list.append([None, None,
         f'Поднять перо на тНКТ{nkt_diam}мм с глубины {rirSole}м с доливом скважины в объеме 1.1м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(rirRoof, 1)])
    else:
        pero_list.append([None, None,
                          f'Поднять перо на тНКТ{nkt_diam}мм до глубины {rirRoof}м с доливом скважины в объеме 0.3м3 тех. жидкостью '
                          f'уд.весом {CreatePZ.fluid_work}',
                          None, None, None, None, None, None, None,
                          'мастер КРС', descentNKT_norm(float(rirSole)-float(rirRoof), 1)])
        if (CreatePZ.plast_work) != 0:
            pero_list.extend(rirWithPero(self)[-9:])
        else:
            pero_list.extend(rirWithPero(self)[-10:])
    return pero_list