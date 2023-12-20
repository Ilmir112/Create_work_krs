from PyQt5.QtWidgets import QMessageBox, QInputDialog

from krs import volume_vn_ek, volume_vn_nkt, well_volume
from work_py.acids_work import open_checkbox_dialog
from work_py.alone_oreration import fluid_change
from work_py.drilling import drilling_nkt
from work_py.raiding import Raid
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from work_py.sand_filling import sandFilling, sand_select, sandWashing


def rir_rpp(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_list, paker_diametr_select
    rir_list = []
    open_checkbox_dialog()


    rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
    if rir_rpk_question == QMessageBox.StandardButton.Yes:
        rir_rpk_plast_true = True
    else:
        rir_rpk_plast_true = False
    rpkDepth, ok = QInputDialog.getInt(None, 'глубина посадки глухого пакера',
                                       'Введите глубину посадки  глухого пакера',
                                       int(CreatePZ.perforation_roof + 10), 0, int(CreatePZ.bottomhole_artificial))
    for row in paker_list(self):
        rir_list.append(row)
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])



    rir_work_list = [[None, None,
                   f'Спустить   пакер глухой {rpk_nkt(self, rpkDepth)}  на тНКТ{nkt_diam}мм до глубины {rpkDepth}м с замером, шаблонированием шаблоном. '
                   f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
                   f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя РИР или УСРСиСТ.',
        None, None, None, None, None, None, None,
    'мастер КРС', descentNKT_norm(rpkDepth,1.2)],
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
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.5+0.6],
     [None, None,
      f'Произвести установку глухого пакера по технологическому плану подрядчика по РИР силами подрядчика по РИР '
      f'с установкой пакера  на глубине {rpkDepth}м',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],

     [None, None,
      f'{"".join([f"Опрессовать эксплуатационную колонну на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика" if  rir_rpk_plast_true == False else ""])} '
      f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
     [None, None,
      f'Поднять стыковочное устройство с глубины {rpkDepth}м с доливом скважины в объеме '
      f'{round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work} ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(rpkDepth, 1.2)]]
    for row in rir_work_list:
        rir_list.append(row)
    CreatePZ.current_bottom = rpkDepth
    perf_new(self, rpkDepth, CreatePZ.current_bottom)
    return rir_list



def rir_rpk(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_list, paker_diametr_select
    rir_list = []
    open_checkbox_dialog()

    plast = CreatePZ.plast_select
    rir_rpk_question = QMessageBox.question(self, 'посадку между пластами?', 'посадку между пластами?')
    if rir_rpk_question == QMessageBox.StandardButton.Yes:
        rir_rpk_plast_true = True
    else:
        rir_rpk_plast_true = False
    rpkDepth, ok = QInputDialog.getInt(None, 'Определение приемистости',
                                       'Введите глубину посадки пакера РПК для определения приемистости',
                                       int(CreatePZ.perforation_roof + 10), 0, int(CreatePZ.bottomhole_artificial))
    for row in paker_list(self):
        rir_list.append(row)
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])




    if rir_rpk_plast_true:
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
        'мастер КРС', 1.35]]
        for row in rir_q_list:
            rir_list.insert(-1, row)
    else:
        rir_rpk_plast_true = False

        rir_q_list = [
                      [None, None,
                       f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast} при Р-80, 100, 120атм '
                       f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                       f'после закачки, объем согласовать с подрядчиком по РИР).  В случае приёмистости менее  250м3/сут '
                       f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                       f'приемистости по технологическому плану',
                       None, None, None, None, None, None, None,
                       'мастер КРС', 1.35]]
        for row in rir_q_list[::-1]:
            rir_list.insert(-1, row)

    rir_work_list = [[None, None,
                   f'Спустить   пакера РПК {rpk_nkt(self, rpkDepth)}  на тНКТ{nkt_diam}мм до глубины {rpkDepth}м с замером, шаблонированием шаблоном. '
                   f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) \n'
                   f'Перед спуском технологического пакера произвести визуальный осмотр в присутствии представителя РИР или УСРСиСТ.',
        None, None, None, None, None, None, None,
    'мастер КРС', descentNKT_norm(rpkDepth,1.2)],
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
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
     [None, None,
      f'Произвести РИР {plast} по технологическому плану подрядчика по РИР силами подрядчика по РИР '
      f'с установкой пакера РПК на глубине {rpkDepth}м',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
     [None, None,
      f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
      f'технологического "СТОП" ОЗЦ без давления.',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 16],
     [None, None,
      f'{"".join([f"Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика" if rir_rpk_plast_true == False else ""])} '
      f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ',0.67],
     [None, None,
      f'Во время ОЗЦ поднять стыковочное устройство с глубины {rpkDepth}м с доливом скважины в объеме '
      f'{round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work} ',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(rpkDepth,1)]]
    for row in rir_work_list:
        rir_list.append(row)
    perf_new(self, rpkDepth, CreatePZ.current_bottom)
    CreatePZ.current_bottom = rpkDepth

    return rir_list

def perf_new(self, roofRir, solePir):
    from open_pz import CreatePZ

    print(f' пласта до изоляции {CreatePZ.plast_work}')
    for plast in CreatePZ.plast_work:
        for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
           if roofRir <= list(interval)[0] <= solePir:
                    CreatePZ.dict_perforation[plast]['отключение'] = True
    for plast in CreatePZ.plast_all:
        for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
            if roofRir <= list(interval)[0] <= solePir:
                CreatePZ.dict_perforation[plast]['отключение'] = True


    CreatePZ.definition_plast_work(self)
    if len(CreatePZ.dict_leakiness) != 0:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            print(roofRir, float(nek.split('-')[0]), solePir)
            if roofRir <= float(nek.split('-')[0]) <= solePir:
                CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отключение'] = True
        print(f"при {CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отключение']}")

    print(CreatePZ.dict_leakiness)

    print(f' пласта рабоче {CreatePZ.plast_work}')



def rpk_nkt(self, paker_depth):
    from open_pz import CreatePZ
    from work_py.opressovka import nktOpress
    CreatePZ.nktOpressTrue = False


    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth< CreatePZ.head_column_additional:
        rpk_nkt_select = f' для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм ' \
                       f'+ {nktOpress(self)[0]} + НКТ + репер'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth> CreatePZ.head_column_additional:
        rpk_nkt_select = f' для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]} ' \
                       f'+ НКТ60мм + репер + НКТ60мм L- {round(paker_depth-CreatePZ.head_column_additional, 0)}м '
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth> CreatePZ.head_column_additional:
        rpk_nkt_select = f' для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм  + {nktOpress(self)[0]}' \
                       f'+ НКТ + репер + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- {round(paker_depth-CreatePZ.head_column_additional, 0)}м '

    return rpk_nkt_select


def rirWithPero(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_list, paker_diametr_select
    from krs import volume_vn_nkt

    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

    open_checkbox_dialog()

    plast = CreatePZ.plast_select
    rirSole, ok = QInputDialog.getInt(None, 'Подошва цементного моста',
                                      'Введите глубину подошвы цементного моста ',
                                      int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_drill))
    rirRoof, ok = QInputDialog.getInt(None, 'Кровля цементного моста',
                                      'Введите глубину кровлю цементного моста ',
                                      int(CreatePZ.perforation_roof-50), 0, int(CreatePZ.bottomhole_drill))
    if CreatePZ.column_additional == True and CreatePZ.column_additional_diametr <110:
        dict_nkt = {73: CreatePZ.head_column_additional, 60: CreatePZ.head_column_additional-rirSole}
    else:
        dict_nkt = {73: rirSole}


    volume_cement = round(volume_vn_ek(self) * (rirSole - rirRoof)/1000, 1)

    uzmPero_list = [
        [None, None,
         f'Спустить {pero_select(self, rirSole)}  на тНКТ{nkt_diam}мм до глубины {rirSole}м с замером, шаблонированием '
         f'шаблоном. Опрессовать НКТ на 150атм. Вымыть шар. \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС',descentNKT_norm(rirSole, 1)],
        [None, None,
         f'Произвести установку  цементного моста  в интервале {rirRoof}-{rirSole}м в присутствии представителя УСРСиСТ',
         None, None, None, None, None, None, None,
         'мастер КРС', 2.5],
        [None, None,
         f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
         f' (сухой цемент{round(volume_cement*1.25,1)}т) ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме 0,5м3, цементный раствор в объеме {volume_cement}м3, '
         f'довести тех.жидкостью у=1,00г/см3 в объёме 1,5м3, тех. жидкостью  в объёме {round(volume_vn_nkt(dict_nkt)-1.5,1)}м3. '
         f'Уравновешивание цементного раствора',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Приподнять перо до гл.{rirRoof}м. ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
         f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом {CreatePZ.fluid_work} (Полуторакратный объем НКТ) '
         f'с расходом жидкости 8л/с (срезка) до чистой воды.',
         None, None, None, None, None, None, None,
         'мастер КРС', well_volume_norm(16)],
        [None, None,
         f'Поднять перо на безопасную зону до гл. {rirRoof-300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}.',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
         f'ОЗЦ без давления.',
         None, None, None, None, None, None, None,
         'мастер КРС',24],
        [None, None,
         f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на гл. {rirRoof}м'
         f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной телефонограммой.',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],
        [None, None,
         f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя '
         f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
         f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
         f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.67],
        [None, None,
         f'Поднять перо на тНКТ{nkt_diam}мм с глубины {rirRoof}м с доливом скважины в объеме 2,2м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(rirRoof, 1)],
    ]

    rirPero_list = [
        [None, None,
         f'Спустить {pero_select(self, rirSole)}  на тНКТ{nkt_diam}мм до глубины {rirSole}м с замером, шаблонированием '
         f'шаблоном. Опрессовать НКТ на 150атм. Вымыть шар. \n'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(rirSole, 1)],
        [None, None,
         f'Произвести цементную заливку с целью изоляции пласта  в интервале {rirRoof}-{rirSole}м в присутствии '
         f'представителя УСРС и СТ',
         None, None, None, None, None, None, None,
         'мастер КРС', 2.5],
        [None, None,
         f'Приготовить цементный раствор у=1,82г/см3 в объёме {volume_cement}м3'
         f' (сухой цемент{round(volume_cement * 1.25, 1)}т) ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Вызвать циркуляцию. Закачать в НКТ тех. воду у=1,00г/см3 в объеме 0,5м3, цементный раствор в объеме {volume_cement}м3, '
         f'довести тех.жидкостью у=1,00г/см3 в объёме 1,5м3, тех. жидкостью  в объёме {round(volume_vn_nkt(dict_nkt) - 1.5, 1)}м3. '
         f'Уравновешивание цементного раствора',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Приподнять перо до гл.{rirRoof}м. Закрыть трубное простанство. Продавить по затрубному пространству '
         f'тех.жидкостью  при давлении не более {CreatePZ.max_admissible_pressure}атм (до получения технологического СТОП).',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Открыть трубное пространство. Промыть скважину обратной промывкой (срезка) по круговой циркуляции '
         f'тех.жидкостью  в объеме не менее {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 уд.весом {CreatePZ.fluid_work} '
         f'(Полуторакратный объем НКТ) '
         f'с расходом жидкости 8л/с (срезка) до чистой воды.',
         None, None, None, None, None, None, None,
         'мастер КРС', well_volume_norm(16)],
        [None, None,
         f'Поднять перо на безопасную зону до гл. {rirRoof - 300}м с доливом скважины в объеме 0,3м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}.',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],
        [None, None,
         f'ОЗЦ - 23 часа (с момента завершения срезки цементного раствора - 24 часа (по качеству пробы))) \n'
         f'ОЗЦ без давления.',
         None, None, None, None, None, None, None,
         'мастер КРС', 24],
        [None, None,
         f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на гл. {rirRoof}м'
         f' с прямой промывкой и разгрузкой на забой 3т. Текущий забой согласовать с Заказчиком письменной телефонограммой.',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],
        [None, None,
         f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя '
         f'УСРСиСТ Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
         f'начала работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком '
         f'В случае головы ЦМ ниже планового РИР повторить  с учетом корректировки мощности моста ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.67],
        [None, None,
         f'Поднять перо на тНКТ{nkt_diam}мм с глубины {rirRoof}м с доливом скважины в объеме {round(rirRoof * 1.12 / 1000, 1)}м3 тех. жидкостью '
         f'уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(rirRoof, 1)],
    ]
    print(f'количество пластов {len(CreatePZ.plast_work)}')

    if len(CreatePZ.plast_work) == 0:
        rir_list = []
        for row in uzmPero_list:
            rir_list.append(row)
        perf_new(self, rirRoof, rirSole)
        CreatePZ.current_bottom = rirRoof

        if len(CreatePZ.plast_work) != 0:
            rir_list.pop(-2)

    else:
        rir_list = []
        for row in paker_list(self):
            rir_list.append(row)
        glin_list = [
            [None, None,
             f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast} при Р-80, 100, 120атм '
             f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
             f'после закачки, объем согласовать с подрядчиком по РИР). В случае приёмистости менее  250м3/сут '
             f'при Р={CreatePZ.max_admissible_pressure}атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
             f'приемистости по технологическому плану',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.77],
            [None, None,
             f'По результатам определения приёмистости выполнить следующие работы: \n'
             f'В случае приёмистости свыше 480 м3/сут при Р=100атм выполнить работы по закачке гдинистого раствора '
             f'(по согласованию с ГС и ПТО ООО Ойл-сервис и заказчика). \n'
             f'В случае приёмистости менее 480 м3/сут при Р=100атм и более 120м3/сут при Р=100атм продолжить работы с п. 17',
             None, None, None, None, None, None, None,
             'мастер КРС, заказчик', None],
            [None, None,
             f'Объём глинистого р-ра скорректировать на устье на основании тех.возможности. \n'
             f'Приготовить глинистый раствор в объёме 5м3 (расчет на 1 м3 - сухой глинопорошок массой 0,3т + '
             f'вода у=1,00г/см3 в объёме 0,9м3) плотностью у=1,24г/см3',
             None, None, None, None, None, None, None,
             'мастер КРС', 3.5],
            [None, None,
             f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме 5м3 + тех. воду  в объёме {volume_vn_nkt(dict_nkt) - 5}м3. Закрыть затруб. '
             f'Продавить в НКТ  тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более {CreatePZ.max_admissible_pressure}атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Коагуляция 4 часа (на основании конечного давления при продавке. '
             f'В случае конечного давления менее 50атм, согласовать объем глинистого раствора с '
             f'Заказчиком и продолжить приготовление следующего объема глинистого объема).',
             None, None, None, None, None, None, None,
             'мастер КРС', 4],
            [None, None,
             f'Определить приёмистость по НКТ при Р=100атм.',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.35],
            [None, None,
             f'В случае необходимости выполнить работы по закачке глнистого раствора, с корректировкой по объёму раствора.',
             None, None, None, None, None, None, None,
             'мастер КРС', None ],
            [None, None,
             f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью '
             f'в объеме не менее 24м3 с расходом жидкости не менее 8 л/с.',
             None, None, None, None, None, None, None,
             'мастер КРС', well_volume_norm(24)]
        ]
        if volume_vn_nkt(dict_nkt) <= 5:
            glin_list[3] = [None, None,
                            f'Закачать в НКТ при открытом затрубном пространстве глинистый раствор в объеме {volume_vn_nkt(dict_nkt)}м3. Закрыть затруб. '
                            f'Продавить в НКТ остаток глинистого раствора в объеме {round(5 - volume_vn_nkt(dict_nkt), 1)} и тех. воду  в объёме {volume_vn_nkt(dict_nkt)}м3 при давлении не более {CreatePZ.max_admissible_pressure}атм.',
                            None, None, None, None, None, None, None,
                            'мастер КРС', 0.5]

        for row in glin_list:
            rir_list.insert(-2, row)

        for row in rirPero_list:
            rir_list.append(row)
        perf_new(self, rirRoof, CreatePZ.current_bottom)
        CreatePZ.current_bottom = rirRoof

        if len(CreatePZ.plast_work) != 0:
            rir_list.pop(-2)
        else:
            acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                   'Нужно ли изменять удельный вес?')
            if acid_true_quest == QMessageBox.StandardButton.Yes:
                for row in fluid_change():
                    rir_list.insert(-2, row)

    return rir_list


def pero_select(self, rirSole):
    from open_pz import CreatePZ
    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and rirSole < CreatePZ.head_column_additional:
        pero_select = f'перо + опрессовочное седло + НКТ{CreatePZ.nkt_diam} 20м + репер'

    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and rirSole > CreatePZ.head_column_additional:
        pero_select = f'перо + опрессовочное седло + НКТ60мм 20м + репер + НКТ60мм L- {rirSole - CreatePZ.head_column_additional}м'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and rirSole > CreatePZ.head_column_additional:
        pero_select  = f'воронку + опрессовочное седло + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками 20м + НКТ{CreatePZ.nkt_diam}мм со снятыми фасками' \
                       f' L- {rirSole - CreatePZ.head_column_additional}м'
    return pero_select

def rir_paker(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_list,paker_diametr_select
    rir_list = []
    for row in paker_list(self):
        rir_list.append(row)

    rirRoof, ok = QInputDialog.getInt(None, 'Кровля цементного моста',
                                      'Введите глубину кровлю цементного моста ',
                                      int(CreatePZ.perforation_roof - 20), 0, int(CreatePZ.bottomhole_drill))

    open_checkbox_dialog()
    plast = CreatePZ.plast_select



    rir_q_list = [None, None,
                   f'Произвести насыщение скважины в объеме 5м3. Определить приемистость {plast} при Р-80, 100, 120атм '
                   f'в присутствии представителя УСРСиСТ или подрядчика по РИР. (Вести контроль за отдачей жидкости '
                   f'после закачки, объем согласовать с подрядчиком по РИР).  В случае приёмистости менее  250м3/сут '
                   f'при Р=100атм произвести соляно-кислотную обработку скважины в объеме 1м3 HCl-12% с целью увеличения '
                   f'приемистости по технологическому плану',
                   None, None, None, None, None, None, None,
                   'мастер КРС', 1.77]
    rir_list.insert(-3, rir_q_list)

    rir_paker_list = [[None, None,
      f'Произвести РИР {plast} c плановой кровлей на глубине {rirRoof}м по технологическому плану подрядчика по РИР силами подрядчика по РИР '
      f'Перед спуском технологического пакера произвести испытание гидроякоря в присутсвии представителя РИР или УСРСиСТ.',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 8],
     [None, None,
      f'ОЗЦ 16-24 часа: (по качеству пробы) с момента отстыковки пакера В случае не получения '
      f'технологического "СТОП" ОЗЦ без давления.',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 24],
      [None, None,
       f'Допустить компоновку с замером и шаблонированием НКТ до кровли цементного моста (плановый на гл. {rirRoof}м'
       f' с прямой промывкой и разгрузкой на забой 3т',
       None, None, None, None, None, None, None,
       'Мастер КРС, подрядчик РИР, УСРСиСТ', 1.2],
     [None, None,
      f'Опрессовать цементный мост на Р={CreatePZ.max_admissible_pressure}атм в присутствии представителя заказчика '
      f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала '
      f'работ) В случае негерметичности цементного моста дальнейшие работы согласовать с Заказчиком.',
      None, None, None, None, None, None, None,
      'Мастер КРС, подрядчик РИР, УСРСиСТ', 0.67],
      [None, None,
       f'Поднять компоновку РИР на тНКТ{CreatePZ.nkt_diam}мм с глубины {rirRoof}м с доливом скважины в объеме '
       f'{round(rirRoof * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
       None, None, None, None, None, None, None,
       'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(rirRoof,1.2)]
        ]
    perf_new(self, rirRoof, CreatePZ.current_bottom)
    CreatePZ.current_bottom = rirRoof

    if len(CreatePZ.plast_work) != 0:
        rir_paker_list.pop(-2)
    for row in rir_paker_list:
        rir_list.append(row)
    return rir_list

def rir_izvelPaker(self):
    from open_pz import CreatePZ
    pakerIzvPaker, ok = QInputDialog.getInt(None, 'Глубина извлекаемого пакера',
                                      'Введите глубину установки извлекаемого пакера ',
                                      int(CreatePZ.perforation_roof-50), 0, int(CreatePZ.bottomhole_drill))
    CreatePZ.pakerIzvPaker = pakerIzvPaker
    rir_list = [[None, None,
       f'Спустить   пакера извлекаемый компании НЕОИНТЕХ +НКТ73мм 20м + реперный патрубок 2м на тНКТ73мм до'
       f' глубины {pakerIzvPaker}м с замером, шаблонированием шаблоном 59,6мм.'
       f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
       None, None, None, None, None, None, None,
       'Мастер КРС, подрядчик РИР, УСРСиСТ', liftingNKT_norm(pakerIzvPaker,1.2)],
    [None, None,
     f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
     f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
     None, None, None, None, None, None, None,
     'Мастер КРС, подрядчик по ГИС', 4],
    [None, None,
     f'Произвести установку извлекаемого пакера на глубине {pakerIzvPaker}м по технологическому плану работ плана подрядчика.',
     None, None, None, None, None, None, None,
     'Мастер КРС, подрядчик по ГИС', 4 ],
    [None, None,
     f'Поднять ИУГ с доливом тех жидкости в объеме  {round(pakerIzvPaker * 1.12 / 1000, 1)}м3 уд.весом {CreatePZ.fluid_work}',
     None, None, None, None, None, None, None,
     'Мастер КРС, подрядчик по ГИС', 4]]
    CreatePZ.current_bottom2 = CreatePZ.current_bottom

    filling_list = [
        [None, None,
         f' Спустить  {sand_select(self)}  на НКТ{CreatePZ.nkt_diam}мм до глубины {round(pakerIzvPaker - 100, 0)}м с замером, шаблонированием шаблоном. (При СПО первых десяти НКТ на '
         f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'Мастер КР', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [None, None, f'Произвести отсыпку кварцевым песком в инт. {pakerIzvPaker-20} - {pakerIzvPaker} '
                     f' в объеме {round(well_volume(self, pakerIzvPaker) / pakerIzvPaker * 1000 * (20), 0)}л '
                     f'Закачать в НКТ кварцевый песок  с доводкой тех.жидкостью {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', 3.5],
        [None, None, f'Ожидание оседания песка 4 часа.',
         None, None, None, None, None, None, None,
         'мастер КРС', 4],
        [None, None,
         f'Допустить компоновку с замером и шаблонированием НКТ до кровли песчаного моста (плановый забой - {pakerIzvPaker-20}м).'
         f' Определить текущий забой скважины (перо от песчаного моста не поднимать, упереться в песчаный мост).',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],

        [None, None,
         f'В случае если кровля песчаного моста на гл.{pakerIzvPaker-20}м дальнейшие работы продолжить дальше по плану'
         f'В случае пеcчаного моста ниже гл.{pakerIzvPaker-20}м работы повторить с корректировкой обьема и технологических глубин.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Поднять {sand_select(self)} НКТ{CreatePZ.nkt_diam}мм с глубины {pakerIzvPaker-20 }м с доливом скважины в '
         f'объеме {round(pakerIzvPaker * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(pakerIzvPaker, 1)]
    ]

    sand_question = QMessageBox.question(None, 'Отсыпка', 'Нужна ли отсыпка головы пакера?')
    if sand_question == QMessageBox.StandardButton.Yes:
        for row in filling_list:
            rir_list.append(row)
        CreatePZ.current_bottom = pakerIzvPaker-20
        for row in rir_paker(self):
            rir_list.append()
        for row in drilling_nkt(self):
            rir_list.append(row)
        for row in Raid.raidingColumn(self):
            rir_list.append(row)
        for row in izvlech_paker(self):
            rir_list.append(row)
    else:
        CreatePZ.current_bottom = pakerIzvPaker

    return rir_list

def izvlech_paker(self):
    from open_pz import CreatePZ
    rir_list = [[None, None,
     f' Спустить  {sand_select(self).replace("перо", "перо-110мм")}  на НКТ{CreatePZ.nkt_diam}мм до глубины {round(CreatePZ.current_bottom,0)}м с замером, шаблонированием шаблоном. '
     f'(При СПО первых десяти НКТ на '
     f'спайдере дополнительно устанавливать элеватор ЭХЛ)',
     None, None, None, None, None, None, None,
     'Мастер КР', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [None, None, f'Произвести нормализацию забоя (вымыв кварцевого песка) с наращиванием, комбинированной  промывкой по круговой циркуляции '
                     f'жидкостью  с расходом жидкости не менее 8 л/с до гл.{CreatePZ.pakerIzvPaker-10}м. \n'
                     f'Тех отстой 2ч. Повторное определение текущего забоя, при необходимости повторно вымыть.',
         None, None, None, None, None, None, None,
         'мастер КРС', 3.5],
        [None, None,
         f'Поднять {sand_select(self)} НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.pakerIzvPaker-10}м с доливом скважины'
         f' в объеме {round(CreatePZ.pakerIzvPaker-10 * 1.12 / 1000, 1)}м3 тех. '
         f'жидкостью  уд.весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker-10, 1)]]

    emer_list = [[None, None,
         f'Спустить с замером ловильный инструмент на НКТ73 до Н= {CreatePZ.current_bottom}м с замером. ',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom, 1)],
                 [None, None,
                  f'Произвести нормализацию (вымыв кварцевого песка) на ловильном инструменте до глубины {CreatePZ.pakerIzvPaker}м обратной '
                  f'промывкой уд.весом {CreatePZ.fluid_work} \n'
                  f'Произвести  ловильный работы при представителе заказчика на глубине {CreatePZ.pakerIzvPaker}м.',
                  None, None, None, None, None, None, None,
                  'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker, 1)],
                 [None, None,
                  f'Рассхадить и поднять компоновку НКТ{CreatePZ.nkt_diam}мм с глубины {CreatePZ.pakerIzvPaker}м с доливом скважины в объеме {round(CreatePZ.pakerIzvPaker * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
                  None, None, None, None, None, None, None,
                  'мастер КРС', liftingNKT_norm(CreatePZ.pakerIzvPaker, 1)]]
    for row in emer_list:
        rir_list.append(row)

    CreatePZ.current_bottom = CreatePZ.current_bottom2
    return rir_list
