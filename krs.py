import H2S
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from datetime import datetime
from collections import namedtuple

from work_py.mkp import mkp_revision_1_kateg
from work_py.rationingKRS import liftingNKT_norm


def calculationFluidWork(vertical, pressure):
    from open_pz import CreatePZ

    if (isinstance(vertical, float) or isinstance(vertical, int)) and (
            isinstance(pressure, float) or isinstance(pressure, int)):

        # print(vertical, pressure)
        stockRatio = 0.1 if float(vertical) <= 1200 else 0.05

        fluidWork = round(float(str(pressure)) * (1 + stockRatio) / float(vertical) / 0.0981, 2)
        # print(fluidWork < 1.02 , (CreatePZ.region == 'КГМ' or CreatePZ.region == 'АГМ'))
        if fluidWork < 1.02 and (CreatePZ.region == 'КГМ' or CreatePZ.region == 'АГМ'):
            fluidWork = 1.02
        elif fluidWork < 1.02 and (CreatePZ.region == 'ИГМ' or CreatePZ.region == 'ТГМ' or CreatePZ.region == 'ЧГМ'):
            fluidWork = 1.01

        return fluidWork
    else:
        return None

def calc_work_fluid(self, work_plan):
    from open_pz import CreatePZ
    fluid_list = []
    if work_plan != 'gnkt_frez':
        CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                             'Введите забой до которого нужно нормализовать',
                                                             float(CreatePZ.current_bottom))
    # Задаем начальную и конечную даты периода
    current_date = datetime.now().date()
    if current_date.month > 4:
        start_date = datetime(current_date.year, 12, 1).date()
        end_date = datetime(current_date.year + 1, 4, 1).date()
    else:
        start_date = datetime(current_date.year-1, 12, 1).date()
        end_date =datetime(current_date.year, 4, 1).date()

    # Проверяем условие: если текущая дата находится в указанном периоде

    try:
        fluid_p = 1.01
        for plast in CreatePZ.plast_work:
            if float(list(CreatePZ.dict_perforation[plast]['рабочая жидкость'])[0]) > fluid_p:
                fluid_p = list(CreatePZ.dict_perforation[plast]['рабочая жидкость'])[0]
        fluid_list.append(fluid_p)
        if max(fluid_list) <= 1.18:

            if start_date <= current_date <= end_date and max(fluid_list) <= 1.18:
                fluid_max = 1.18
            else:
                fluid_max = max(fluid_list)
        else:
            fluid_max = max(fluid_list)
        if work_plan == 'gnkt_frez' or work_plan == 'gnkt_opz':
            fluid_max = 1.18
        fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                       'Введите удельный вес рабочей жидкости',
                                                       fluid_max, 0.87, 2, 2)
    except:
        mes = QMessageBox.warning(None,'Ошибка', 'Ошибка в определении удельного веса рабочей жидкости')

        if work_plan == 'gnkt_frez':
            fluid_max = fluid_p
        fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                       'Введите удельный вес жидкости глушения',
                                                       1.18, 0.87, 2, 2)

    CreatePZ.fluid = fluid_work_insert
    CreatePZ.fluid_short = fluid_work_insert

    cat_H2S_list = CreatePZ.dict_category[CreatePZ.plast_work[0]]['по сероводороду'].category

    if cat_H2S_list in [2, 1]:
        expenditure_h2s_list = []
        for plast in CreatePZ.plast_work:

            try:
                # print(CreatePZ.dict_category[plast]['по сероводороду'].poglot)
                expenditure_h2s_list.append([CreatePZ.dict_category[plast]['по сероводороду'].poglot][0])
                # print(f'поглотои {expenditure_h2s_list}')
            except:
                pass
        # print(expenditure_h2s_list)
        expenditure_h2s = round(max(expenditure_h2s_list), 3)
        fluid_work = f'{fluid_work_insert}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из ' \
                     f'расчета {expenditure_h2s}кг/м3 '
        fluid_work_short = f'{fluid_work_insert}г/см3 c ' \
                           f'ХИМТЕХНО 101 Марка А - {expenditure_h2s}кг/м3 '
    else:
        fluid_work = f'{fluid_work_insert}г/см3 '
        fluid_work_short = f'{fluid_work_insert}г/см3'


    return fluid_work, fluid_work_short

def work_krs(self, work_plan):
    from open_pz import CreatePZ
    from work_py.rationingKRS import lifting_sucker_rod, well_jamming_norm, liftingGNO
    from krs import well_jamming
    from work_py.descent_gno import gno_nkt_opening
    # print(f' пакер {CreatePZ.paker_do}), ЭЦН {CreatePZ.dict_pump_ECN}, ШГН {CreatePZ.dict_pump_SHGN}')

    CreatePZ.fluid_work, CreatePZ.fluid_work_short = calc_work_fluid(self, work_plan)
    nkt_diam_fond = gno_nkt_opening(CreatePZ.dict_nkt)

    if work_plan != 'dop_plan':
        if CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"]) != 'отсут' and \
                CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]) != 'отсут':
            # print(CreatePZ.dict_pump_ECN["do"], )
            lift_key = 'ОРД'
        elif CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"]) != 'отсут' and \
                CreatePZ.if_None(CreatePZ.paker_do["do"]) == 'отсут':
            lift_key = 'ЭЦН'
        elif CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"]) != 'отсут' and \
                CreatePZ.if_None(CreatePZ.paker_do['do']) != 'отсут':
            lift_key = 'ЭЦН с пакером'
        elif CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]) != 'отсут' and\
                CreatePZ.dict_pump_SHGN["do"].upper() != 'НН' \
                and CreatePZ.if_None(CreatePZ.paker_do['do']) == 'отсут':
            lift_key = 'НВ'
        elif CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]) != 'отсут' and \
                CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]).upper() != 'НН' \
                and CreatePZ.if_None(CreatePZ.paker_do['do']) != 'отсут':
            lift_key = 'НВ с пакером'
            print('Подьем НВ с пакером ')
        elif 'НН' in CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]).upper() \
                and CreatePZ.if_None(CreatePZ.paker_do['do']) == 'отсут':
            lift_key = 'НН'
            print('Подьем НН')
        elif 'НН' in CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]).upper() and \
                CreatePZ.if_None(CreatePZ.if_None(CreatePZ.paker_do['do'])) != 'отсут':
            lift_key = 'НН с пакером'
            print('Подьем НН с пакером ')
        elif CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]) == 'отсут' and \
                CreatePZ.if_None(CreatePZ.paker_do['do']) == 'отсут' \
                and CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"]) == 'отсут':
            lift_key = 'воронка'
            print('Подьем  воронки')
        elif CreatePZ.if_None(CreatePZ.dict_pump_SHGN["do"]) == 'отсут' and \
                CreatePZ.if_None(CreatePZ.paker_do['do']) != 'отсут' \
                and CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"]) == 'отсут':
            lift_key = 'пакер'
            print('Подьем пакера')
        elif '89' in CreatePZ.dict_nkt.keys() and '48' in CreatePZ.dict_nkt.keys() and \
                CreatePZ.if_None(
                CreatePZ.paker_do['do']) != 'отсут':
            lift_key = 'ОРЗ'

        # print(f'Лифт ключ {lift_key}')

        without_damping_True = CreatePZ.without_damping

        if any([cater == 1 for cater in CreatePZ.cat_P_1]):
            CreatePZ.kat_pvo, _ = QInputDialog.getInt(None, 'Категория скважины',
                                                   f'Категория скважины № {CreatePZ.kat_pvo}, корректно?',
                                                   CreatePZ.kat_pvo, 1, 2)


        well_jamming_str_in_nkt = " " if without_damping_True is True\
            else f"По результату приемистости произвести глушение скважины в НКТ тех.жидкостью в объеме обеспечивающим " \
                 f"заполнение трубного пространства и скважины в подпакерной зоне в объеме {volume_pod_NKT(self)} м3 " \
                 f"жидкостью уд.веса {CreatePZ.fluid_work} при давлении не более {CreatePZ.max_admissible_pressure._value}атм. " \
                 f"Тех отстой 1-2 часа. Произвести замер избыточного давления в скважине."

        krs_begin = [
            [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
            [None, None, 'Наименование работ', None, None, None, None, None, None, None, 'Ответственный',
             'Нормы времени \n мин/час.'],
            [None, None,
             f'Начальнику смены ЦТКРС, вызвать телефонограммой представителя Заказчика для оформления АКТа '
             f'приёма-передачи скважины в ремонт. \n'
             f'Совместно с представителем Заказчика оформить схему расстановки оборудования при КРС с обязательной '
             f'подписью представителя Заказчика на схеме.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст-ль Заказчика.', float(0.5)],
            [None, None,
             f'Принять скважину в ремонт у Заказчика с составлением АКТа. Переезд  бригады. Подготовительные работы '
             f'к КРС. Определить технологические '
             f'точки откачки жидкости у Заказчика согласно Договора.',
             None, None, None, None, None, None, None,
             ' Предст-тель Заказчика, мастер КРС', float(0.5)],
            [None, 3,
             f'Перед началом работ по освоению, капитальному и текущему ремонту скважин бригада должна быть ознакомлена '
             f'с возможными осложнениями и авариями'
             f'в процессе работ, планом локализации и ликвидации аварии (ПЛА) и планом работ. С работниками должен '
             f'быть проведен инструктаж по выполнению работ, '
             f'связанных с применением новых технических устройств и технологий с соответствующим оформлением в'
             f'журнал инструктажей на рабочем месте ',
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [None, 4,
             f'При подъеме труб из скважины производить долив тех. жидкостью Y- {CreatePZ.fluid_work}. Долив скважины '
             f'должен быть равен объему извлекаемого металла.'
             f'По мере расхода жидкости из ёмкости, производить своевременное её заполнение. При всех технологических '
             f'спусках НКТ 73мм х 5,5мм и 60мм х 5мм производить '
             f'контрольный замер и отбраковку + шаблонирование шаблоном {CreatePZ.nkt_template}мм d=59,6мм и 47,9мм '
             f'соответственно.',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', None],
            [None, None, f'ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ ПРОИЗВОДИТЬ НА ТЕХ ЖИДКОСТИ УД. ВЕСОМ РАВНОЙ {CreatePZ.fluid_work}', None,
             None, None, None, None, None, None, None,
             None],
            [None, None, f'Замерить Ризб. При наличии избыточного давления произвести замер Ризб и уд.вес '
                         f'жидкости излива, по результату замеру произвести перерасчет и корректировку удельного веса тех.жидкости',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', 0.5],
            [None, None,
             f'Согласно инструкции ООО Башнефть-Добыча ПЗ-05 И-102089Ю ЮЛ-305 версия 2 п. 9.1.9 при отсутствии '
             f'избыточного давления и '
             f'наличии риска поглощения жидкости глушения. произвести замер статического уровня силами ЦДНГ перед '
             f'началом работ и в '
             f'процессе ремонта (с периодичностью определяемой ответственным руководителем работ, по согласованию с '
             f'представителем Заказчика '
             f'Результаты замеров статического уровня фиксировать в вахтовом журнале и передавать в сводке '
             f'При изменении '
             f'уровня в скважине от первоначально замеренного на 100м и более метров в сторону уменьшения или '
             f'возрастания, '
             f'необходимо скорректировать объем долива идобиться стабилизации уровня в скважине. Если по данным '
             f'замера уровень в '
             f'скважине растет, необходимо выполнить повторноеглушение скважины, сделав перерасчет плотности '
             f'жидкости глушения в '
             f'соответствии суточненными геологической службой данными по пластовому давлению.',
             None, None, None, None, None, None, None,
             ' Мастер КРС.', 1.5]
        ]
        if CreatePZ.bvo is True:
            for row in mkp_revision_1_kateg(self):
                krs_begin.insert(-3, row)

        posle_lift = [[None, None,
                       f'По результатам подъема провести ревизию НКТ в присутствии представителя ЦДНГ. В случае '
                       f'обнаружения дефекта НКТ, вызвать '
                       f'представителя ЦДНГ, составить акт. На Отказные НКТ закрепить бирку " на расследование", '
                       f'сдать в ООО "РН-Ремонт НПО" '
                       f'отдельно, с пометкой в БНД-25 "на расследование". Произвести Фотофиксацию отказных элементов, '
                       f'БНД-25. Фото предоставить в '
                       f'технологический отдел В течение 24 часов после подъема согласовать с ЦДНГ необходимость замены,'
                       f' пропарки, промывки ГНО, '
                       f'технологию опрессовки НКТ согласовать с ПТО', None, None,
                       None, None, None, None, None,
                       'Мастер КРС, представитель Заказчика', 0.5],
                      [None, None,
                       f'Опрессовать глухие плашки превентора на  '
                       f'{CreatePZ.max_admissible_pressure._value}атм на '
                       f'максимально допустимое давление опрессовки эксплуатационной колонны с выдержкой в течении 30 '
                       f'минут,в случае невозможности '
                       f'опрессовки по результатам определения приемистости и по согласованию с заказчиком  опрессовать '
                       f'глухие плашки ПВО на давление поглощения, '
                       f'но не менее 30атм и  с составлением акта на опрессовку ПВО с представителем Заказчика. ', None,
                       None,
                       None, None, None, None, None,
                       'Мастер КРС', 0.67],
                      [None, None,
                       f'Скорость спуска (подъема) погружного оборудования в скважину не должна превышать 0,25 м/с '
                       f'в наклонно-направленных и '
                       f'горизонтальных скважинах. В скважинах набором кривизны более 1,5 градуса на 10 м скорость '
                       f'пуска (подъёма) не должна превышать '
                       f'0,1 м/с в интервалах искривления. Произвести визуальный осмотр колонной муфты и ниппеля '
                       f'колонного патрубка, отревизировать переводники. '
                       f'При отбраковке дать заявку в цех Заказчика на замену. Составить акт (при изменении альтитуды '
                       f'муфты э/колонны указать в акте).',
                       None, None,
                       None, None, None, None, None,
                       'Мастер КРС', None],
                      [None, None,
                       f'В СЛУЧАЕ ВЫНУЖДЕННОГО ПРОДОЛЖИТЕЛЬНОГО ПРОСТОЯ ПО ЗАВОЗУ ТЕХНОЛОГИЧЕСКОГО ИЛИ ФОНДОВОГО ОБОРУДОВАНИЯ В СКВАЖИНУ НЕОБХОДИМО СПУСКАТЬ '
                       f'ПРОТИВОФОНТАННЫЙ ЛИФТ ДЛИНОЙ 300м. ', None, None,
                       None, None, None, None, None,
                       'Мастер КРС представитель Заказчика', None]]
        kvostovik = f' + хвостовиком  {round(sum(list(CreatePZ.dict_nkt.values())) - float(CreatePZ.depth_fond_paker_do["do"]), 1)}м '\
            if CreatePZ.region == 'ТГМ' else ''
        well_jamming_str = well_jamming(self, without_damping_True, lift_key) # экземпляр функции расчета глушения
        well_jamming_ord = volume_jamming_well(self, float(CreatePZ.depth_fond_paker_do["do"]))
        lift_ord = [
            [ f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.67],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'подьем {CreatePZ.dict_pump_SHGN["do"]}', None,
             f'Сорвать насос штанговый насос {CreatePZ.dict_pump_SHGN["do"]}(зафиксировать вес при срыве). Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на {CreatePZ.max_admissible_pressure._value}атм. '
             f'{"".join([" " if without_damping_True == True else f"Приподнять штангу. Произвести глушение в затрубное пространство в объеме{well_jamming_ord}м3 (объем колонны от пакера до устья уд.весом {CreatePZ.fluid_work}. Техостой 2ч."])}'
             f'Поднять на штангах насос с гл. {CreatePZ.dict_pump_SHGN_h["do"]}м с доливом тех жидкости уд.весом {CreatePZ.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(CreatePZ.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер  не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с выдержкой 30мин для возврата резиновых элементов в исходное положение'
             f'в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 + АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона -  для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 0.67+1+0.07+0.32+0.45+0.3+0.23+0.83],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', 2.8],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с пакером {CreatePZ.paker_do["do"]}',
             None,
             f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с пакером {CreatePZ.paker_do["do"]} с '
             f'глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м (компоновка НКТ {nkt_diam_fond} на поверхность '
             f'с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО '
             f'на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)]
        ]
        lift_ecn = [
            [f'Опрессовать ГНО на Р=50атм', None,
             'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. (Вызов представителя осуществлять '
             'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [f'Сбить сбивной клапан. {well_jamming_str[2]}', None,
             f'Сбить сбивной клапан. {well_jamming_str[0]}',
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', 3.2],
            [None, None, well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'Сорвать планшайбу не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [ pvo_gno(CreatePZ.kat_pvo)[1], None,
             'Заглубить оставшийся  кабель в скважину на 1-3 технологических НКТ' + pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м', None,
             f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м '
             f'(компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины '
             f'тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО'
             f' на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)],
        ]

        lift_ecn_with_paker = [
            ['Опрессовать ГНО на Р=50атм', None,
             'Опрессовать ГНО на Р=50атм в течении 30мин в присутствии представителя ЦДНГ. Составить акт. '
             '(Вызов представителя осуществлять '
             'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ'
             ' ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [None, None,
             f'Сбить сбивной клапан. '
             f'{"".join([" " if without_damping_True == True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Произвести глушение в НКТ в объеме {volume_pod_NKT(self)}м3. {CreatePZ.fluid_work}"])}'

                , None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'срыв пакера не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки '
             f'с выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
             f'более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
             f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, '
             f'через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона -  для составления '
             f'алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС',None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на "
                           "производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                           "опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                           "ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. "
                           "Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, '
                                                                                                     'представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
             f'промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с пакером {CreatePZ.paker_do["do"]}', None,
             f'Поднять  {CreatePZ.dict_pump_ECN["do"]} с пакером {CreatePZ.paker_do["do"]}'
             f'с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) '
             f'на поверхность с замером, накручиванием '
             f'колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.22 / 1000, 1)}м3 с контролем'
             f' АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)],
        ]
        lift_pump_nv = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ '
             f'ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'Поднять {CreatePZ.dict_pump_SHGN["do"]} с гл. {CreatePZ.dict_pump_SHGN_h["do"]}м', None,
             f'Сорвать насос {CreatePZ.dict_pump_SHGN["do"] } (зафиксировать вес при срыве). Обвязать устье скважины '
             f'согласно схемы №3 утвержденной главным '
             f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{CreatePZ.max_admissible_pressure._value}атм. Поднять на штангах насос '
             f'с гл. {int(CreatePZ.dict_pump_SHGN_h["do"])}м с доливом тех жидкости уд.весом {CreatePZ.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), '
             f'без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(CreatePZ.dict_sucker_rod)],
            [f'Сорвать планшайбу не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, '
             f'через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
             f'для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой "
                           "опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель "
                           "ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде "
                           "ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и промывки с '
             f'записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'{"".join(["Допустить фНКТ для определения текущего забоя. " if CreatePZ.gipsInWell == True else ""])}Поднять  замковую опору с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м',
             None,
             f'{"".join(["Допустить фНКТ для определения текущего забоя. " if CreatePZ.gipsInWell == True else ""])}Поднять  замковую опору  на НКТ с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', liftingGNO(CreatePZ.dict_nkt)],
        ]
        lift_pump_nv_with_paker = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ '
             f'НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'Поднять насос {CreatePZ.dict_pump_SHGN["do"]}', None,
             f'Сорвать насос {CreatePZ.dict_pump_SHGN["do"]} (зафиксировать вес при срыве). Обвязать устье скважины '
             f'согласно схемы №3 утвержденной главным '
             f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). '
             f'Опрессовать ПВО на {CreatePZ.max_admissible_pressure._value}атм. '
             f'{"".join([" " if without_damping_True == True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу. Произвести глушение в НКТ в объеме{volume_pod_NKT(self)}м3. Техостой 2ч."])}'
             f' Поднять на штангах насос с гл. {float(CreatePZ.dict_pump_SHGN_h["do"])}м с '
             f'доливом тех жидкости уд.весом {CreatePZ.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  '
             f'насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с последующим '
             f'комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением супервайзера, '
             f'распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(CreatePZ.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
             f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
             f'в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
             f'противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не '
             f'более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
             f'для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [ f'Поднять  З.О. с пакером {CreatePZ.paker_do["do"]}', None,
             f'Поднять  замковую опору с пакером {CreatePZ.paker_do["do"]} с глубины'
             f' {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м  (компоновка НКТ{nkt_diam_fond}) на '
             f'поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)],
        ]
        lift_pump_nn = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ НЕГЕРМЕТИЧНОСТИ НКТ '
             f'ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            [f'поднять плунжен', None,
             f'Сорвать  плунжер. (зафиксировать вес при срыве). Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на '
             f'{CreatePZ.max_admissible_pressure._value}атм. Заловить конус спуском одной '
             f'штанги. Поднять на штангах плунжер с гл. {float(CreatePZ.dict_pump_SHGN_h["do"])}м с доливом тех '
             f'жидкости уд.весом {CreatePZ.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  '
             f'постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с последующим '
             f'комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением '
             f'супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(CreatePZ.dict_sucker_rod)],
            [f'Сорвать планшайбу не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ '
             f'не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с'
             f' противодавлением в НКТ '
             f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, '
             f'через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
             f'алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                           "собой опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                           "Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение "
                           "по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
             f'промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'Поднять  {CreatePZ.dict_pump_SHGN["do"]}', None,
             f'Поднять  {CreatePZ.dict_pump_SHGN["do"]} с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м '
             f'(компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с доливом скважины '
             f'тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО '
             f'на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', liftingGNO(CreatePZ.dict_nkt)],
        ]
        lift_pump_nn_with_paker = [
            [f'Опрессовать ГНО на Р={40}атм', None,
             f'Опрессовать ГНО на Р={40}атм в течении 30мин в присутствии представителя ЦДНГ. '
             f'Составить акт. (Вызов представителя осуществлять '
             f'телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ) ПРИ '
             f'НЕГЕРМЕТИЧНОСТИ НКТ ПОДЪЕМ ВЕСТИ С КАЛИБРОВКОЙ',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика ', 0.7],
            [None, None,
             f'{lifting_unit(self)}', None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
            ['Поднять плунжер', None,
             f'Сорвать плунжер насоса (зафиксировать вес при срыве). Обвязать устье скважины согласно схемы №3 утвержденной главным '
             f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на {CreatePZ.max_admissible_pressure._value}атм. Спуском одной штанги заловить конус. '
             f'{"".join([" " if without_damping_True == True else f"При наличии Избыточного давления не позволяющее сорвать пакера: Приподнять штангу. Произвести глушение в НКТ в объеме{volume_pod_NKT(self)}м3. Техостой 2ч."])}'
    
             f' Поднять на штангах плунжер с гл. {int(CreatePZ.dict_pump_SHGN_h["do"])}м с доливом тех жидкости уд.весом {CreatePZ.fluid_work} '
             f'Обеспечить не превышение расчетных нагрузок на штанговые колонны при срыве  насосов (не более 8 тн), без учета веса '
             f'штанг в  0,9т. При отрицательном результате согласов технологической службой ЦДНГ или ПТО региона  постепенное увеличение нагрузки до 15тн ( по 1т - 1 час), либо искусственный  отворот НШ с последующим комбинированным подъемом ГНО НВ. В случае невозможности отворота колонны НШ с подтверждением супервайзера, распиловку НШ согласовать с ПТО по направлению сектора учета НКТ и НШ.',
             None, None, None, None, None, None, None,
             'Мастер КРС представитель Заказчика, пусков. Ком. ',
             lifting_sucker_rod(CreatePZ.dict_sucker_rod)],
            [f'Сорвать планшайбу и пакер  не '
             f'более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)',
             None,
             f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
             f'выдержкой 30мин для возврата резиновых элементов в исходное положение в присутствии представителя ЦДНГ, с '
             f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не '
             f'более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
             f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном '
             f'результате согласовать с УСРСиСТ ступенчатое увеличение '
             f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  '
             f'с противодавлением в НКТ (время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на '
             f'расхаживание - не более 6 часов, через 5 часов'
             f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления алгоритма'
             f' последующих работ. ', None, None,
             None, None, None, None, None,
             'Мастер КРС представитель Заказчика', 1.5],
            [well_jamming_str[2], None,
             well_jamming_str[0],
             None, None, None, None, None, None, None,
             'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True == False else None][0]],
            [None, None,
             well_jamming_str[1],
             None, None, None, None, None, None, None,
             ' Мастер КРС', None],
            [None, None,
             ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                      else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                           "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                           "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность для жизни людей"
                           " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель ПАСФ приглашается за 24 часа до проведения "
                           "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                           "подъёмного агрегата для ремонта скважины."]),
             None, None, None, None, None, None, None,
             'Мастер КРС', None],
            [pvo_gno(CreatePZ.kat_pvo)[1], None,
             pvo_gno(CreatePZ.kat_pvo)[0], None, None,
             None, None, None, None, None,
             ''.join([
                 'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
             [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
            [None, None,
             f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
             None, None,
             None, None, None, None, None,
             None, None],
            [None, None,
             f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
             f'промывки с записью удельного веса в вахтовом журнале. ',
             None, None,
             None, None, None, None, None,
             None, None],
           [None, None,
             f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
             None, None, None, None, None,
             None, 1.2],
            [f'Поднять  насос {CreatePZ.dict_pump_SHGN["do"]} с пакером {CreatePZ.paker_do["do"]}',
             None,
             f'Поднять  насос {CreatePZ.dict_pump_SHGN["do"]} с пакером {CreatePZ.paker_do["do"]} с глубины '
             f'{round(sum(list(CreatePZ.dict_nkt.values())), 1)}м (компоновка НКТ{nkt_diam_fond}) на поверхность с '
             f'замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
             f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с контролем АСПО '
             f'на стенках НКТ.',
             None, None,
             None, None, None, None, None,
             'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)],
        ]
        lift_voronka = [[well_jamming_str[2], None, well_jamming_str[0],
                         None, None, None, None, None, None, None,
                         'Мастер КРС, представ заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                        [None, None,
                         well_jamming_str[1],
                         None, None, None, None, None, None, None,
                         ' Мастер КРС', None],
                        [None, None,
                         f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                         'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                        [f'Сорвать планшайбу не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
                         f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)',
                         None,
                         f'Разобрать устьевое оборудование. Сорвать планшайбу в присутствии представителя ЦДНГ, с '
                         f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на НКТ не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
                         f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                         f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с противодавлением в НКТ '
                         f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 часов, через 5 часов'
                         f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления алгоритма'
                         f' последующих работ. ', None, None,
                         None, None, None, None, None,
                         'Мастер КРС представитель Заказчика', 1.5],
                        [None, None,
                         ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                                  else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                                       "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на производство " \
                                       "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за собой опасность для жизни людей"
                                       " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. Представитель ПАСФ приглашается за 24 часа до проведения "
                                       "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                                       "подъёмного агрегата для ремонта скважины."]),
                         None, None, None, None, None, None, None,
                         'Мастер КРС', None],
                        [pvo_gno(CreatePZ.kat_pvo)[1], None,
                         pvo_gno(CreatePZ.kat_pvo)[0], None, None,
                         None, None, None, None, None,
                         ''.join([
                             'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                         [ 4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
                        [None, None,
                         f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                         None, None,
                         None, None, None, None, None,
                         None, None],
                        [None, None,
                         f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и промывки с записью удельного веса в вахтовом журнале. ',
                         None, None,
                         None, None, None, None, None,
                         None, None],
                        [None, None,
                         f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                         None, None, None, None, None,
                         None, None],
                        [f'Поднять воронку  с Н-{round(sum(list(CreatePZ.dict_nkt.values())), 1)}м',
                         None,
                         f'Поднять  воронку с глубины {round(sum(list(CreatePZ.dict_nkt.values())), 1)}м'
                         f' (компоновка НКТ{nkt_diam_fond}) на поверхность с замером, накручиванием колпачков с '
                         f'доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
                         f'в объеме {round(round(sum(list(CreatePZ.dict_nkt.values())), 1) * 1.12 / 1000, 1)}м3 с'
                         f' контролем АСПО на стенках НКТ.',
                         None, None,
                         None, None, None, None, None,
                         'Мастер КРС', liftingGNO(CreatePZ.dict_nkt)],
                        ]


        lift_paker = [[f'Опрессовать эксплуатационную колонну и пакер на Р={CreatePZ.max_admissible_pressure._value}атм',
                       None,
                       f'Опрессовать эксплуатационную колонну и пакер на Р={CreatePZ.max_admissible_pressure._value}атм в '
                       f'присутствии представителя ЦДНГ. '
                       f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением '
                       f'за 2 часа до начала работ)',
                       None, None, None, None, None, None, None,
                       'Мастер КРС, Представ заказчика', 1.2],
                      [f'При наличии Избыточного давления не позволяющее сорвать пакера:\n'
                       f'Произвести определение приемистости скважины', None,
                       f'При наличии Избыточного давления не позволяющее сорвать пакера:\n '
                       f'Произвести определение приемистости скважины при давлении не более {CreatePZ.max_admissible_pressure._value}атм. '
                       f'{well_jamming_str_in_nkt}',
                       None, None,
                       None, None, None, None, None,
                       'Мастер КРС, Представ заказчика', 1.2],
                      [None, None,
                       f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                       'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                      [f'Произвести срыв пакера не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
                       f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%)', None,
                       f'Разобрать устьевое оборудование. Произвести срыв пакера с поэтапным увеличением нагрузки '
                       f'на 3-4т выше веса НКТ в течении 30мин и с выдержкой '
                       f'1ч  для возврата резиновых элементов в исходное положение. Сорвать планшайбу в присутствии'
                       f' представителя ЦДНГ, с '
                       f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
                       f'НКТ не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
                       f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                       f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                       f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости '
                       f'с противодавлением в НКТ '
                       f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - '
                       f'не более 6 часов, через 5 часов'
                       f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - '
                       f'для составления алгоритма'
                       f' последующих работ. ', None, None,
                       None, None, None, None, None,
                       'Мастер КРС представитель Заказчика', 3.2],
                      [well_jamming_str[2], None, well_jamming_str[0], None, None,
                       None, None, None, None, None,
                       'Мастер КРС представитель Заказчика', [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                      ['глушение', None,
                       well_jamming_str[1],
                       None, None, None, None, None, None, None,
                       'Мастер КРС', None],
                      [None, None,
                       ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                                else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                                     "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения на"
                                     " производство " \
                                     "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь за "
                                     "собой опасность для жизни людей"
                                     " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены. "
                                     "Представитель ПАСФ приглашается за 24 часа до проведения "
                                     "проверки монтажа ПВО телефонограммой. произвести практическое обучение по команде"
                                     "ВЫБРОС. Пусковой комиссией составить акт готовности "
                                     "подъёмного агрегата для ремонта скважины."]),
                       None, None, None, None, None, None, None,
                       'Мастер КРС', None],
                      [pvo_gno(CreatePZ.kat_pvo)[1], None,
                       pvo_gno(CreatePZ.kat_pvo)[0], None, None,
                       None, None, None, None, None,
                       ''.join([
                           'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком' if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                       [4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
                      [None, None,
                       f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и'
                       f'промывки с записью удельного веса в вахтовом журнале. ',
                       None, None,
                       None, None, None, None, None,
                       None, None],
                      [None, None,
                       f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                       None, None, None, None, None,
                       None, None],
                      [ f'Поднять  пакер {CreatePZ.paker_do["do"]} с глубины {CreatePZ.depth_fond_paker_do["do"]}м',
                        None,
                       f'Поднять  пакер {CreatePZ.paker_do["do"]} с глубины {CreatePZ.depth_fond_paker_do["do"]}м {kvostovik}'
                       f'на поверхность с замером, накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
                       f'в объеме 1,7м3 с контролем АСПО на стенках НКТ.', None, None,
                       None, None, None, None, None,
                       'Мастер КРС', round(liftingGNO(CreatePZ.dict_nkt)*1.2,2)]
                      ]
        # print(f'ключ НКТ {list(map(int, CreatePZ.dict_nkt.keys())), CreatePZ.dict_nkt}')
        lift_orz = [[]]
        if 89 in list(map(int, CreatePZ.dict_nkt.keys())) and 48 in list(map(int, CreatePZ.dict_nkt.keys())):
            lift_orz = []
            # try:
            lift_key = 'ОРЗ'
            lift_orz = [
                [f'глушение скважины в НКТ48мм в объеме {round(1.3 * CreatePZ.dict_nkt["48"] / 1000, 1)}м3, '
                 f'Произвести глушение скважины в '
                 f'НКТ89мм тех.жидкостью на поглощение в объеме {round(1.3 * CreatePZ.dict_nkt["89"] * 1.1 / 1000, 1)}м3', None,
                 f'Произвести глушение скважины в НКТ48мм тех.жидкостью в объеме обеспечивающим заполнение трубного '
                 f'пространства в объеме {round(1.3 * CreatePZ.dict_nkt["48"] / 1000, 1)}м3 жидкостью уд.веса '
                 f'{CreatePZ.fluid_work}на давление поглощения до {CreatePZ.max_admissible_pressure._value}атм. '
                 f'Произвести глушение скважины в '
                 f'НКТ89мм тех.жидкостью на поглощение в объеме обеспечивающим заполнение '
                 f'межтрубного и подпакерного пространства '
                 f'в объеме {round(1.3 * CreatePZ.dict_nkt["89"] * 1.1 / 1000, 1)}м3 '
                 f'жидкостью уд.веса {CreatePZ.fluid_work}. Тех отстой 1-2 часа. '
                 f'Произвести замер избыточного давления в скважине.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика ', 0.7],
                [None, None,
                 f'{lifting_unit(self)}', None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ', 4.2],
                [f'Поднять стыковочное устройство на НКТ48мм', None,
                 f'Поднять стыковочное устройство на НКТ48мм  с гл. {CreatePZ.dict_nkt["48"]}м с доливом тех жидкости '
                 f'уд.весом {CreatePZ.fluid_work}',
                 None, None, None, None, None, None, None,
                 'Мастер КРС представитель Заказчика, пусков. Ком. ',
                 round((0.17 + 0.015 * CreatePZ.dict_nkt["48"] / 8.5 + 0.12 + 1.02), 1)],
                [f'Сорвать планшайбу и пакер', None,
                 f'Разобрать устьевое оборудование. Сорвать планшайбу и пакер с поэтапным увеличением нагрузки с '
                 f'выдержкой 30мин для возврата резиновых элементов в исходное положение'
                 f'в присутствии представителя ЦДНГ, с '
                 f'составлением акта. При срыве нагрузка не должна превышать предельно допустимую нагрузку на '
                 f'НКТ не более {round(weigth_pipe(CreatePZ.dict_nkt) * 1.2, 1)}т. '
                 f'(вес подвески ({round(weigth_pipe(CreatePZ.dict_nkt), 1)}т) + 20%). ПРИМЕЧАНИЕ: '
                 f'При отрицательном результате согласовать с УСРСиСТ ступенчатое увеличение '
                 f'нагрузки до 28т ( страг нагрузка НКТ по паспорту), по 3 т – 0,5 час , при необходимости  с '
                 f'противодавлением в НКТ '
                 f'(время на прибытие СТП ЦА 320 +  АЦ не более 4 часов). Общие время на расхаживание - не более 6 '
                 f'часов, через 5 часов'
                 f' с момента расхаживания пакера - выйти с согласование на УСРСиСТ, ПТО Региона - для составления '
                 f'алгоритма'
                 f' последующих работ. ', None, None,
                 None, None, None, None, None,
                 'Мастер КРС представитель Заказчика', 1.5],
                [well_jamming_str[2], None,
                 well_jamming_str[0],
                 None, None, None, None, None, None, None,
                 'Мастер КРС, представ заказчика',
                 [str(well_jamming_norm(volume_pod_NKT(self))) if without_damping_True is False else None][0]],
                [None, None,
                 well_jamming_str[1],
                 None, None, None, None, None, None, None,
                 ' Мастер КРС',
                 None],
                [None, None,
                 ''.join(["За 24 часа до готовности вызвать пусковую комиссию" if CreatePZ.kat_pvo == 2
                          else "На скважинах первой категории Подрядчик обязан пригласить представителя ПАСФ " \
                               "для проверки качества м/ж и опрессовки ПВО, документации и выдачи разрешения "
                               "на производство " \
                               "работ по ремонту скважин. При обнаружении нарушений, которые могут повлечь "
                               "за собой опасность для жизни людей"
                               " и/или возникновению ГНВП и ОФ, дальнейшие работы должны быть прекращены."
                               " Представитель ПАСФ приглашается за 24 часа до проведения "
                               "проверки монтажа ПВО телефонограммой. произвести практическое обучение по"
                               " команде ВЫБРОС. Пусковой комиссией составить акт готовности "
                               "подъёмного агрегата для ремонта скважины."]),
                 None, None, None, None, None, None, None,
                 'Мастер КРС', None],
                [pvo_gno(CreatePZ.kat_pvo)[1], None,
                 pvo_gno(CreatePZ.kat_pvo)[0], None, None,
                 None, None, None, None, None,
                 ''.join([
                     'Мастер КРС, представ-ли ПАСФ и Заказчика, Пуск. ком'
                     if CreatePZ.kat_pvo == 1 else 'Мастер КРС, представ-ли  Заказчика']),
                 [4.21 if 'схеме №1' in str(pvo_gno(CreatePZ.kat_pvo)[0]) else 0.23+0.3+0.83+0.67+ 0.14][0]],
                [None, None,
                 f'Опрессовку ПВО проводить после каждого монтажа. (ОПРЕССОВКУ ПВО ЗАФИКСИРОВАТЬ В ВАХТОВОМ ЖУРНАЛЕ).',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Мастеру бригады КРС осуществлять входной контроль за плотностью ввозимой жидкости глушения и '
                 f'промывки с записью удельного веса в вахтовом журнале. ',
                 None, None,
                 None, None, None, None, None,
                 None, None],
                [None, None,
                 f'Провести практическое обучение вахт по сигналу ВЫБРОС.', None, None,
                 None, None, None, None, None,
                 None, None],
                [f'Поднять компоновку ОРЗ с глубины {CreatePZ.dict_nkt["89"]}м', None,
                 f'Поднять компоновку ОРЗ на НКТ89мм с глубины {CreatePZ.dict_nkt["89"]}м на поверхность с замером, '
                 f'накручиванием колпачков с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  '
                 f'в объеме {round(CreatePZ.dict_nkt["89"] * 1.35 / 1000, 1)}м3 с контролем АСПО на стенках НКТ.',
                 None, None,
                 None, None, None, None, None,
                 'Мастер КРС', round(liftingNKT_norm(CreatePZ.depth_fond_paker_do['do'], 1.3), 2)],
            ]



        lift_dict = {'пакер': lift_paker, 'ОРЗ': lift_orz, 'ОРД': lift_ord, 'воронка': lift_voronka,
                     'НН с пакером': lift_pump_nn_with_paker, 'НВ с пакером': lift_pump_nv_with_paker,
                     'ЭЦН с пакером': lift_ecn_with_paker, 'ЭЦН': lift_ecn, 'НВ': lift_pump_nv, 'НН': lift_pump_nn}
        lift_sel = ['пакер', 'ОРЗ', 'ОРД', 'воронка', 'НН с пакером', 'НВ с пакером',
                    'ЭЦН с пакером', 'ЭЦН', 'НВ', 'НН']
        # print(f' перед выбором {lift_key}')
        lift, ok = QInputDialog.getItem(self, 'Спущенное оборудование', 'выбор спущенного оборудования',
                                        lift_sel, lift_sel.index(lift_key), False)
        if ok and lift_sel:
            self.le.setText(lift)
        lift_select = lift_dict[lift]
        return krs_begin + lift_select + posle_lift
    else:
        krs_begin = [
            [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
            [None, None, 'Наименование работ', None, None, None, None, None, None, None, 'Ответственный',
             'Нормы времени \n мин/час.'],
            [None, 1,
             'Ранее проведенные работ:',
             None, None, None, None, None, None, None,
             None, None]]
        return krs_begin[:2]

def pvo_gno(kat_pvo):
    from open_pz import CreatePZ
    # print(f' ПВО {kat_pvo}')
    pvo_2 = f'Установить ПВО по схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г (тип плашечный ' \
            f'сдвоенный ПШП-2ФТ-152х21) и посадить пакер. ' \
            f'Спустить пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до концевых ' \
            f'задвижек на Р-{CreatePZ.max_admissible_pressure._value}атм на максимально допустимое давление ' \
            f'опрессовки эксплуатационной колонны в течении ' \
            f'30мин), сорвать пакер. В случае невозможности опрессовки по ' \
            f'результатам определения приемистости и по согласованию с заказчиком  опрессовать трубные плашки ПВО на ' \
            f'давление поглощения, но не менее 30атм. '

    pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером ООО "Ойл-сервис" от 07.03.2024г ' \
            f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
            f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
            f' (при необходимости произвести монтаж переводника' \
            f' П178х168 или П168 х 146 или ' \
            f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
            f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и линии манифольда до ' \
            f'концевых задвижек на Р-{CreatePZ.max_admissible_pressure._value}атм ' \
            f'(на максимально допустимое давление опрессовки ' \
            f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. Опрессовать ' \
            f'выкидную линию после концевых задвижек на ' \
            f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на' \
            f'давление до 210 кгс/см2 ((21 МПа)\n' \
            f'- Обеспечить обогрев превентора и СУП в зимнее время . \n Получить разрешение на производство работ в присутствии представителя ПФС'
    if kat_pvo == 1:
        return pvo_1, f'Монтаж ПВО по схеме №2 + ГидроПревентор'
    else:
        # print(pvo_2)
        return pvo_2, f'Монтаж ПВО по схеме №2'



def lifting_unit(self):
    from open_pz import CreatePZ
    aprs_40 = f'Установить подъёмный агрегат на устье не менее 40т.\n' \
              f' Пусковой комиссией составить акт готовности  подьемного агрегата и бригады для проведения ремонта скважины.' \
              f'ПРИМЕЧАНИЕ:  ПРИ ИСПОЛЬЗОВАНИИ ПОДЪЕМНОГО АГРЕТАТА АПРС-50, А5-40, АПРС-50 ДОПУСКАЕТСЯ РАБОТА БЕЗ ' \
              f'ПРИМЕНЕНИЯ ВЕТРОВЫХ ОТТЯЖЕК ПРИ НАГРУЗКАХ НЕ БОЛЕЕ 25ТН. ПРИ НЕОБХОДИМОСТИ УВЕЛИЧЕНИЯ НАГРУЗКИ ТРЕБУЕТСЯ ' \
              f'ОСНАСТИТЬ ПОДЪЕМНЫЙ АГРЕГАТ ВЕТРОВЫМИ ОТТЯЖКАМИ. ПРИ ЭТОМ МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ 80% ОТ' \
              f' СТРАГИВАЮЩЕЙ НАГРУЗКИ НА НКТ.ПРИ ИСПОЛЬЗОВАНИИ ПОДЬЕМНОГО АГРЕГАТА  УПА-60/80, БАРС, А-50, АПР 60/80 ' \
              f'РАБОТАТЬ ТОЛЬКО С ПРИМЕНЕНИЕМ  ОТТЯЖЕК МАКСИМАЛЬНУЮ НАГРУЗКА НЕ ДОЛЖНА ПРЕВЫШАТЬ 80% ОТ СТРАГИВАЮЩЕЙ ' \
              f'НАГРУЗКИ НА НКТ. После монтажа подъёмника якоря ветровых оттяжек должны быть испытаны на нагрузки, ' \
              f'установленные инструкцией по эксплуатации завода - изготовителя в присутствии супервайзера Заказчика. ' \
              f'Составить акт готовности подъемного агрегата. Пусковой комиссией составить акт готовности  подьемного ' \
              f'агрегата и бригады для проведения ремонта скважины. Дальнейшие работы продолжить после проведения пусковой ' \
              f'комиссии заполнения пусковой документации. '
    upa_60 = f'Установить подъёмный агрегат на устье не менее 60т. Пусковой комиссией составить ' \
             f'акт готовности  подьемного агрегата и бригады для проведения ремонта скважины.'

    return upa_60 if CreatePZ.bottomhole_artificial._value >= 2300 else aprs_40


def volume_vn_ek(self, current):
    from open_pz import CreatePZ
    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and current < CreatePZ.head_column_additional._value:
        volume = round((CreatePZ.column_diametr._value - 2 * CreatePZ.column_wall_thickness._value) ** 2 * 3.14 / 4 / 1000, 2)
    else:
        volume = round((CreatePZ.column_additional_diametr._value - 2 * CreatePZ.column_additional_wall_thickness._value) ** 2 * 3.14 / 4 / 1000,
            2)
    print(f'внутренний объем ЭК {volume}')
    return volume


def volume_vn_nkt(dict_nkt):  # Внутренний объем одного погонного местра НКТ
    # print(dict_nkt)
    for nkt, lenght_nkt in dict_nkt.items():
        volume_vn_nkt = 0
        if ''.join(filter(str.isdecimal, str(nkt))) == '73':
            t_nkt = 5.5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)
        elif ''.join(filter(str.isdecimal, str(nkt))) == '89':
            t_nkt = 6
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)
        elif ''.join(filter(str.isdecimal, str(nkt))) == '60':
            t_nkt = 5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt, 5)
        elif ''.join(filter(str.isdecimal, str(nkt))) == '48':
            t_nkt = 4.5
            volume_vn_nkt += round(3.14 * (int(nkt) - 2 * t_nkt) ** 2 / 4000000 * lenght_nkt * 1.1, 5)

    return round(volume_vn_nkt, 1)


def volume_rod(self, dict_sucker_rod):  # Объем штанг
    from open_pz import CreatePZ
    from find import FindIndexPZ
    volume_rod = 0
    # print(dict_sucker_rod)
    for diam_rod, lenght_rod in dict_sucker_rod.items():
        if diam_rod:
            volume_rod += (3.14 * (lenght_rod * (
                    FindIndexPZ.check_str_None(self, diam_rod) / 1000) / lenght_rod) ** 2) / 4 * lenght_rod
    return round(volume_rod, 5)


def volume_nkt(dict_nkt):  # Внутренний объем НКТ по фондовым НКТ
    volume_nkt = 0
    for nkt, length_nkt in dict_nkt.items():
        if nkt:
            volume_nkt += volume_vn_nkt(nkt) * length_nkt
    return volume_nkt


def weigth_pipe(dict_nkt):
    weigth_pipe = 0
    for nkt, lenght_nkt in dict_nkt.items():
        if '73' in str(nkt):
            weigth_pipe += lenght_nkt * 9.2 / 1000
        elif '60' in str(nkt):
            weigth_pipe += lenght_nkt * 7.5 / 1000
        elif '89' in str(nkt):
            weigth_pipe += lenght_nkt * 16 / 1000
        elif '48' in str(nkt):
            weigth_pipe += lenght_nkt * 4.3 / 1000
    return weigth_pipe


def volume_metal_nkt(d_nkt):  # объем металла
    if ''.join(filter(str.isdecimal, str(d_nkt))) == '73':
        t_nkt = 5.5
    elif ''.join(filter(str.isdecimal, str(d_nkt))) == '89':
        t_nkt = 6
    elif ''.join(filter(str.isdecimal, str(d_nkt))) == '60':
        t_nkt = 5
    elif ''.join(filter(str.isdecimal, str(d_nkt))) == '48':
        t_nkt = 4.5
    # print(f'объем между ЭК и НКТ{well_volume()-3.14 * (d_nkt) ** 2 / 4000000 * 1141}' )
    return round(3.14 * (d_nkt) ** 2 / 4000000 - 3.14 * (d_nkt - 2 * t_nkt) ** 2 / 4000000, 6)


def volume_nkt_metal(dict_nkt):  # Внутренний объем НКТ железа по фондовым
    volume_nkt_metal = 0
    for nkt, length_nkt in dict_nkt.items():
        if '73' in str(nkt):
            volume_nkt_metal += 1.17 * length_nkt / 1000
        elif '60' in str(nkt):
            volume_nkt_metal += 0.87 * length_nkt / 1000
        elif '89' in str(nkt):
            volume_nkt_metal += 1.7 * length_nkt / 1000
        elif '48' in str(nkt):
            volume_nkt_metal += 0.55 * length_nkt / 1000
    return round(volume_nkt_metal, 1)

def well_volume(self, current_bottom):
    from open_pz import CreatePZ

    # print(CreatePZ.column_additional)
    if CreatePZ.column_additional == False:
        # print(CreatePZ.column_diametr, CreatePZ.column_wall_thickness, current_bottom)
        volume_well = 3.14 * (CreatePZ.column_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000000 * (
            current_bottom)

    else:
        # print(f' ghb [{CreatePZ.column_additional_diametr, CreatePZ.column_additional_wall_thickness._value}]')
        volume_well = (3.14 * (
                CreatePZ.column_additional_diametr._value - CreatePZ.column_additional_wall_thickness._value  * 2) ** 2 / 4 / 1000 * (
                               current_bottom -float(CreatePZ.head_column_additional._value)) / 1000) + (
                              3.14 * (CreatePZ.column_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
                         float(CreatePZ.head_column_additional._value)) / 1000)
    # print(f'Объем скважины {volume_well}')
    return round(volume_well, 1)


def volume_pod_NKT(self):  # Расчет необходимого объема внутри НКТ и между башмаком НКТ и забоем

    from open_pz import CreatePZ
    nkt_l = round(sum(list(CreatePZ.dict_nkt.values())), 1)
    if CreatePZ.column_additional == False:
        v_pod_gno = 3.14 * (int(CreatePZ.column_diametr._value) - int(CreatePZ.column_wall_thickness._value) * 2) ** 2 / 4 / 1000 * (
                float(CreatePZ.current_bottom) - int(nkt_l)) / 1000

    elif round(sum(list(CreatePZ.dict_nkt.values())), 1) >float(CreatePZ.head_column_additional._value):
        v_pod_gno = 3.14 * (CreatePZ.column_diametr._value - CreatePZ.column_wall_thickness._value * 2) ** 2 / 4 / 1000 * (
               float(CreatePZ.head_column_additional._value) - nkt_l) / 1000 + 3.14 * (
                            CreatePZ.column_additional_diametr._value - CreatePZ.column_additional_wall_thickness._value  * 2) ** 2 / 4 / 1000 * (
                            CreatePZ.current_bottom -float(CreatePZ.head_column_additional._value)) / 1000
    elif nkt_l < float(CreatePZ.head_column_additional._value):
        v_pod_gno = 3.14 * (
                CreatePZ.column_additional_diametr._value - CreatePZ.column_additional_wall_thickness._value  * 2) ** 2 / 4 / 1000 * (
                            CreatePZ.current_bottom - nkt_l) / 1000
    volume_in_nkt = v_pod_gno + volume_vn_nkt(CreatePZ.dict_nkt) - volume_rod(self, CreatePZ.dict_sucker_rod)
    # print(f'Внутренный объем + Зумпф{volume_in_nkt, v_pod_gno, volume_vn_nkt(CreatePZ.dict_nkt)}, ')
    return round(volume_in_nkt, 1)


def volume_jamming_well(self, current_bottom): # объем глушения скважины
    from open_pz import CreatePZ
    volume_jamming_well = round((well_volume(self, current_bottom) - volume_nkt_metal(CreatePZ.dict_nkt) - volume_rod(self,
            CreatePZ.dict_sucker_rod)) * 1.1, 1)
    # print(f' объем глушения {well_volume(self, CreatePZ.current_bottom), volume_jamming_well}')
    # print(f' объем {volume_nkt_metal(CreatePZ.dict_nkt)} , {volume_rod(CreatePZ.dict_sucker_rod)}')
    return volume_jamming_well


def get_leakiness(self):

    from open_pz import CreatePZ

    leakiness_column, ok = QInputDialog.getText(self, 'Нарушение колонны',
                                                'Введите нарушение колонны через тире')
    try:
        leakiness_column_min = min(map(float,leakiness_column.split('-')))
        leakiness_column_max = max(map(float,leakiness_column.split('-')))

        leakiness_column_len = len(leakiness_column.split('-'))
        leakiness_column = leakiness_column_min, leakiness_column_max

    except:
        leakiness_column_len = 0
    # print(leakiness_column_len)
    while leakiness_column_len != 2:
        mes = QMessageBox.warning(None, 'Некорректные данные', "Введены не корректные данные")
        leakiness_column, ok = QInputDialog.getText(self, 'Нарушение колонны',
                                                    'Введите нарушение колонны через тире')
        try:
            leakiness_column_min = min(map(float, leakiness_column.split('-')))
            leakiness_column_max = max(map(float, leakiness_column.split('-')))
            # print(leakiness_column_min, leakiness_column_max)
            leakiness_column_len = len(leakiness_column.split('-'))
            leakiness_column = leakiness_column_min, leakiness_column_max
        except:
            leakiness_column_len = 0

    CreatePZ.leakiness_interval.append(leakiness_column)
    # print(f'Наруше {CreatePZ.leakiness_interval}')

    leakiness_rir = QMessageBox.question(self, 'изолированы ли',
                                         'изолировано ли нарушение')
    leakiness_True = {}
    CreatePZ.dict_leakiness.setdefault('НЭК', {}).setdefault('интервал', {}).setdefault(leakiness_column,
                                                                                        {}).setdefault('отрайбировано',
                                                                                                       False)
    CreatePZ.dict_leakiness.setdefault('НЭК', {}).setdefault('интервал', {}).setdefault(leakiness_column,
                                                                                        {}).setdefault(
        'Прошаблонировано', False)
    if leakiness_rir == QMessageBox.StandardButton.Yes:
        CreatePZ.dict_leakiness.setdefault('НЭК', {}).setdefault('интервал', {}).setdefault(leakiness_column,
                                                                                            {}).setdefault('отключение',
                                                                                                           True)
    else:
        CreatePZ.dict_leakiness.setdefault('НЭК', {}).setdefault('интервал', {}).setdefault(leakiness_column,
                                                                                            {}).setdefault('отключение',
                                                                                                           False)

    leakiness_quest = QMessageBox.question(self, 'Нарушение колонны',
                                           'Есть ли еще нарушения?')
    if leakiness_quest == QMessageBox.StandardButton.Yes:
        get_leakiness(self)
    else:
        # print(CreatePZ.dict_leakiness)
        pass


def well_jamming(self, without_damping, lift_key):
    from open_pz import CreatePZ
    # print(f' выбранный {lift_key}')

    # print(f'расстояние ПВР {abs(sum(list(CreatePZ.dict_nkt.values())) - CreatePZ.perforation_roof), volume_jamming_well(self), volume_nkt_metal(CreatePZ.dict_nkt), volume_rod(CreatePZ.dict_sucker_rod)}')
    well_jamming_list2 = f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия  на последнем кубе глушения  жидкости ' \
                         f'уд.веса равной удельному весу ЖГ, дальнейшие промывки и удельный вес жидкостей промывок согласовать с Заказчиком,' \
                         f' при наличии Ризб - произвести замер, перерасчет ЖГ и повторное глушение с корректировкой удельного веса жидкости' \
                         f' глушения. В СЛУЧАЕ ОТСУТСТВИЯ ЦИРКУЛЯЦИИ ПРИ ГЛУШЕНИИ СКВАЖИНЫ, А ТАКЖЕ ПРИ ГАЗОВОМ ФАКТОРЕ БОЛЕЕ 200м3/сут ' \
                         f'ПРОИЗВЕСТИ ЗАМЕР СТАТИЧЕСКОГО УРОВНЯ В ТЕЧЕНИИ ЧАСА С ОТБИВКОЙ УРОВНЯ В СКВАЖИНЕ С ИНТЕРВАЛОМ 15 МИНУТ.' \
                         f'ПО РЕЗУЛЬТАТАМ ЗАМЕРОВ ПРИНИМАЕТСЯ РЕШЕНИЕ ОБ ПРОДОЛЖЕНИИ ОТБИВКИ УРОВНЯ В СКВАЖИНЕ ДО КРИТИЧЕСКОЙ ГЛУБИНЫ ЗА ' \
                         f'ПРОМЕЖУТОК ВРЕМЕНИ.'
    volume_well_jaming = round((volume_jamming_well(self, CreatePZ.current_bottom) - volume_nkt_metal(CreatePZ.dict_nkt) - volume_rod(self, CreatePZ.dict_sucker_rod)-0.2) * 1.1, 1)
    # print(f' Глушение {volume_jamming_well(self, CreatePZ.current_bottom), volume_nkt_metal(CreatePZ.dict_nkt), volume_rod(CreatePZ.dict_sucker_rod)}')
    # print(CreatePZ.well_volume_in_PZ)
    if abs(float(CreatePZ.well_volume_in_PZ[0]) - volume_well_jaming) > 0.5:
        mes = QMessageBox.warning(None, 'Некорректный объем скважины',
                                     f'Объем скважины указанный в ПЗ -{CreatePZ.well_volume_in_PZ}м3 не совпадает '
                                     f'с расчетным {volume_well_jaming}м3')
        volume_well_jaming, _ = QInputDialog.getDouble(None, 'Корректный объем',
                                                    'Введите корректный объем скважины', volume_well_jaming, 3, 80)



    if without_damping == True:
        well_jamming_str = f'Скважина состоит в перечне скважин ООО Башнефть-Добыча, на которых допускается проведение ТКРС без предварительного глушения на текущий квартал'
        well_jamming_short = f'Скважина без предварительного глушения'
        well_jamming_list2 = f'В случае наличия избыточного давления необходимость повторного глушения скважины дополнительно согласовать со специалистами ПТО  и ЦДНГ.'
    elif without_damping is False and lift_key in ['НН с пакером', 'НВ с пакером', 'ЭЦН с пакером', 'ОРЗ']:

        well_after = f'Произвести закачку на поглощение не более {CreatePZ.max_admissible_pressure._value}атм тех жидкости в ' \
                             f'объеме {round(volume_well_jaming-well_volume(self, sum(list(CreatePZ.dict_nkt_po.values()))),1)}м3.' if round(volume_well_jaming-well_volume(self, sum(list(CreatePZ.dict_nkt_po.values()))),1) > 0.1 else ''
        well_jamming_str = f'Произвести закачку в трубное пространство тех жидкости уд.весом {CreatePZ.fluid_work} в ' \
                             f'объеме {round(well_volume(self, sum(list(CreatePZ.dict_nkt.values())))-volume_pod_NKT(self),1)}м3 на циркуляцию. ' \
                           f'{well_after} Закрыть затрубное пространство. ' \
                             f' Закрыть скважину на  стабилизацию не менее 2 часов. (согласовать ' \
                             f'глушение в коллектор, в случае отсутствия на желобную емкость)'
        well_jamming_short = f'Глушение в НКТ уд.весом {CreatePZ.fluid_work_short} ' \
                             f'объеме {round(well_volume(self, sum(list(CreatePZ.dict_nkt.values()))) - volume_pod_NKT(self), 1)}м3 ' \
                             f'на циркуляцию. {well_after} '
    elif without_damping == False and lift_key in ['ОРД']:
        well_jamming_str = f'Произвести закачку в затрубное пространство тех жидкости уд.весом {CreatePZ.fluid_work_short}в ' \
                             f'объеме {round(well_volume(self, CreatePZ.current_bottom) - well_volume(self, CreatePZ.depth_fond_paker_do["do"]),1)}м3 ' \
                             f'на поглощение при давлении не более {CreatePZ.max_admissible_pressure._value}атм. Закрыть ' \
                             f'затрубное пространство. Закрыть скважину на стабилизацию не менее 2 часов. (согласовать ' \
                             f'глушение в коллектор, в случае отсутствия на желобную емкость)'
        well_jamming_short = f'Глушение в затруб уд.весом {CreatePZ.fluid_work_short} в ' \
                             f'объеме {round(well_volume(self, CreatePZ.current_bottom) - well_volume(self, CreatePZ.depth_fond_paker_do["do"]), 1)}м3 ' \

    elif abs(sum(list(CreatePZ.dict_nkt.values())) - CreatePZ.perforation_roof) > 150:
        well_jamming_str = f'Произвести глушение скважины прямой промывкой в объеме {volume_well_jaming}м3 тех ' \
                             f'жидкостью уд.весом {CreatePZ.fluid_work}' \
                             f' на циркуляцию в следующим алгоритме: \n Произвести закачку в затрубное пространство ' \
                           f'тех жидкости в ' \
                             f'объеме {round(well_volume(self, sum(list(CreatePZ.dict_nkt.values()))),1)}м3 на ' \
                           f'циркуляцию. Закрыть трубное пространство. ' \
                             f'Произвести закачку на поглощение не более {CreatePZ.max_admissible_pressure._value}атм ' \
                           f'тех жидкости в ' \
                             f'объеме {round(volume_well_jaming-well_volume(self, sum(list(CreatePZ.dict_nkt.values()))),1)}м3. Закрыть скважину на ' \
                             f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае ' \
                           f'отсутствия на желобную емкость'
        well_jamming_short = f'Глушение в затруб в объеме {volume_well_jaming}м3 тех ' \
                             f'жидкостью уд.весом {CreatePZ.fluid_work_short}'
    elif abs(sum(list(CreatePZ.dict_nkt.values())) - CreatePZ.perforation_roof) <= 150:
        well_jamming_str = f'Произвести глушение скважины прямой промывкой в объеме {volume_well_jaming}м3 тех ' \
                           f'жидкостью уд.весом {CreatePZ.fluid_work}' \
                             f' на циркуляцию. Закрыть скважину на ' \
                             f'стабилизацию не менее 2 часов. (согласовать глушение в коллектор, в случае отсутствия ' \
                           f'на желобную емкость)'
        well_jamming_short = f'Глушение в затруб в объеме {volume_well_jaming}м3 уд.весом {CreatePZ.fluid_work_short}'

        # print([well_jamming_str, well_jamming_list2, well_jamming_short])
    return [well_jamming_str, well_jamming_list2, well_jamming_short]


def is_number(num):
    if num is None:
        return 0
    try:
        float(str(num).replace(",","."))
        return True
    except ValueError or TypeError:
        return False
# def without_damping(self):
#
#     print('начался второй поток')
#     self.worker_thread = ExcelWorker()
#     self.worker_thread.finished.connect(self.on_finished)
#     self.worker_thread.start()


def on_finished(self):
    print("Работа с файлом Excel завершена.")

