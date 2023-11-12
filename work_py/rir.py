from PyQt5.QtWidgets import QMessageBox, QInputDialog


def rir_rpk(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_list,paker_diametr_select
    rir_list = []
    for row in paker_list(self):
        rir_list.append(row)
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    rpkDepth, ok = QInputDialog.getInt(None, 'Определение приемистости',
                                       'Введите глубину посадки пакера РПК для определения приемистости',
                                       int(CreatePZ.perforation_roof+10), 0, int(CreatePZ.bottomhole_artificial))
    plast, ok = QInputDialog.getItem(self, 'выбор пласта или НЭК для РИР ', 'выберете пласт или НЭК для изоляции',
                                     CreatePZ.plast_work, 0, False)
    if ok and plast:
        self.le.setText(plast)

    rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
    if rir_rpk_question == QMessageBox.StandardButton.Yes:
        rir_rpk_plast_true = True
        rir_q_list = [[None, None,
      f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
      f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
      f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик по ГИС', 4],
      [None, None,
                   f'посадить пакер на глубину {rpkDepth}м',
                    None, None, None, None, None, None, None,
                    'мастер КРС', 1],
      [None, None,
                   f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast} при Р-80, 100, 120атм '
                   f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                   f'после закачки, объем согласовать с подрядчиком по РИР).  В случае приёмистости менее  250м3/сут '
                   f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                   f'приемистости по технологическому плану',
        None, None, None, None, None, None, None,
    'мастер КРС', 2.5]]
        for row in rir_q_list:
            rir_list.insert(-1, row)
    else:
        rir_rpk_plast_true = False
        rir_q_list = [[None, None,
                   f'посадить пакер на глубину {rpkDepth}м',
                    None, None, None, None, None, None, None,
                    'мастер КРС', 1],
                      [None, None,
                       f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast} при Р-80, 100, 120атм '
                       f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                       f'после закачки, объем согласовать с подрядчиком по РИР).  В случае приёмистости менее  250м3/сут '
                       f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                       f'приемистости по технологическому плану',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 2.5]]
        for row in rir_q_list[::-1]:
            rir_list.insert(-1, row)

    rir_work_list = [[None, None,
                   f'Спустить   пакера РПК  + {rpk_nkt(self, rpkDepth)}  на тНКТ{nkt_diam}мм до глубины {rpkDepth}м с замером, шаблонированием шаблоном. '
                   f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
                   f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя РИР или УСРСиСТ.',
        None, None, None, None, None, None, None,
    'мастер КРС', 2.5],
     [None, None,
      f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
      f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
      f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик по ГИС', 4],
     [None, None,
      f'При наличии циркуляции опрессовать НКТ на 200атм '
      f'в присутствии порядчика по РИР. Составить акт. Вымыть шар обратной промывкой ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 4],
     [None, None,
      f'Произвести РИР {plast} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
      f'с установкой пакера РПК на глубине {rpkDepth}м',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 16],
     [None, None,
      f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
      f'технологического "СТОП" ОЗЦ без давления.',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 16],
     [None, None,
      f'{"".join([f"Опрессовать цементный мост на Р={CreatePZ.max_expected_pressure}атм в присутствии представителя заказчика" if rir_rpk_question == False else ""])} '
      f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
     [None, None,
      f'Во время ОЗЦ поднять стыковочное устройство с глубины {rpkDepth}м с доливом скважины в объеме '
      f'{round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work} ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', round(0.25+0.033*1.2*(rpkDepth)/9.5*1.04,1)]]
    for row in rir_work_list:
        rir_list.append(row)
    CreatePZ.current_bottom = rpkDepth
    for plast in CreatePZ.plast_work:
        for i in list(CreatePZ.dict_work_pervorations[plast]['интервал']):
            if i[0] > CreatePZ.current_bottom:
                print(CreatePZ.dict_work_pervorations[plast]['интервал'])
                CreatePZ.dict_work_pervorations[plast]['интервал'].discard(i)
        if CreatePZ.dict_work_pervorations[plast]['интервал'] == set():
            del CreatePZ.dict_work_pervorations[plast]

    CreatePZ.plast_work = list(CreatePZ.dict_work_pervorations.keys())
    try:
        CreatePZ.perforation_roof = min(min(
            [min(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
        CreatePZ.perforation_sole = max(max(
            [max(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
        print(f'мин {CreatePZ.perforation_roof}, мак {CreatePZ.perforation_sole}')
    except:
        CreatePZ.perforation_roof = CreatePZ.current_bottom
        CreatePZ.perforation_sole = CreatePZ.current_bottom
    return rir_list



def rpk_nkt(self, paker_depth):
    from open_pz import CreatePZ
    from work_py.opressovka import nktOpress
    CreatePZ.nktOpressTrue = False


    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth< CreatePZ.head_column_additional:
        rpk_nkt_select = f'РПК (либо аналог) для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм ' \
                       f'+ {nktOpress(self)[0]} + НКТ + репер'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth> CreatePZ.head_column_additional:
        rpk_nkt_select = f'РПК (либо аналог) для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]} ' \
                       f'+ НКТ60мм + репер + НКТ60мм L- {paker_depth-CreatePZ.head_column_additional}м '
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth> CreatePZ.head_column_additional:
        rpk_nkt_select = f'РПК (либо аналог) для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]}' \
                       f'+ НКТ + репер + НКТ73мм со снятыми фасками L- {paker_depth-CreatePZ.head_column_additional}м '
    return rpk_nkt_select




