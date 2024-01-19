from PyQt5.QtWidgets import QMessageBox, QInputDialog

from work_py.alone_oreration import privyazkaNKT
from work_py.opressovka import testing_pressure
from work_py.rationingKRS import well_volume_norm, descentNKT_norm, descent_sucker_pod
from work_py.calc_fond_nkt import CalcFond


def gno_down(self):
    from open_pz import CreatePZ

    paker_descent = [
        [None, None,
         f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной '
         f'патрубок на сертифицированный. Для опрессовки фондовых НКТ необходимо заявить в '
         f'ЦДНГ за 24 часа клапан А-КСШ-89-48-30. По согласованию с ТС и ГС настроить клапан '
         f'А-КСШ-89-48-30 на необходимое давление (1,5 кратное от планируемого '
         f'давления закачки) открытия путем регулирования количества срезных винтов. \n'
         f'Перед спуском подрядчик ТКРС определяет статический уровень Нст (эхолот подрядчика ТКРС, '
         f'при необходимости Нст определяется заказчиком)  и согласовывает с заказчиком (ЦДНГ, ПТО) давление '
         f'опрессовки НКТ и срезки винтов (открытие клапана). По результатам расчета давления открытия клапана '
         f'(согласованный с заказчиком), подрядчик производит отворот необходимого количества винтов. '
         f'(согласно паспорта клапана А-КСШ-89-48-30)',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.2],
        [None, None,
         f'Спустить подземное оборудование  согласно расчету и карте спуска ЦДНГ НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)}мм с пакером {CreatePZ.paker_do["posle"]} '
         f'на глубину {CreatePZ.H_F_paker_do["posle"]}м, воронку на глубину {sum(CreatePZ.dict_nkt_po.values())}м. НКТ прошаблонировать для проведения ГИС.',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(sum(CreatePZ.dict_nkt_po.values()),1.2)],
        [None, None,
         f'Демонтировать превентор. Посадить пакер на глубине {CreatePZ.H_F_paker_do["posle"]}м. Отревизировать и ориентировать планшайбу для проведения ГИС. '
         f'Заменить и установить устьевую арматуру для ППД. Обвязать с нагнетательной линией.',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.25 + 0.5 + 0.5],
        [None, None,
         f'{testing_pressure(self, CreatePZ.H_F_paker_do["posle"])}',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 0.67],
        [None, None, ''.join(['ОВТР 10ч' if CreatePZ.region != 'ЧГМ' else 'ОВТР 4ч']),
         None, None, None, None, None, None, None,
         'мастер КРС', ''.join(['10' if CreatePZ.region != 'ЧГМ' else '4'])],
        [None, None, 'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис".  Составить'
                     ' акт готовности скважины и передать его начальнику партии. При необходимости подготовить площадку'
                     ' напротив мостков для постановки партии ГИС.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Произвести запись по техкарте 2.3.2: определение профиля приемистости и оценку технического состояния '
         f'эксплуатационной колонны и НКТ при закачке не менее {PzakPriGis(self)}атм '
         f'при открытой затрубной задвижке',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 20],
        [None, None,
         f'Интерпретация данных ГИС',
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчик по ГИС', 8],
    ]
    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - float(CreatePZ.H_F_paker_do["posle"]))) < 10 or abs(
                    float(interval[0] - float(CreatePZ.H_F_paker_do["posle"]))) < 10:
                if privyazkaNKT(self)[0] not in paker_descent:
                    paker_descent.insert(2, privyazkaNKT(self)[0])
    calc_fond_nkt_str = calc_fond_nkt(self, sum(list(CreatePZ.dict_nkt_po.values())))
    gno_list = [[None, None,
                 f'За 48 часов до спуска запросить КАРТУ спуска на ГНО и заказать оборудование согласно карты спуска.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', None],
                [None, None,
                 f'До спуска ГНО произвести опрессовку фонтанной арматуры после монтажа на устье скважины на давление {CreatePZ.max_admissible_pressure}атм'
                 f'(давление на максимальное возможное давление опрессовки эскплуатационной колонны)',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', None],
                ]

    descent_nv = [[None, None,
                   f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],
                  [None, None,
                   calc_fond_nkt_str,
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],

                  [None, None,
                   f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить сальниковые '
                   f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм.  \n'
                   f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на гл {CreatePZ.dict_pump_SHGN_h["posle"]}м. (в компоновке предусмотреть установку '
                   f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
                   f'компоновка НКТ: {gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые).\n'
                   f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб.  ',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1)],
                  [None, None,
                   f'Демонтировать превентор. Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
                   f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.  ',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 0.67+0.5],

                  [None, None,
                   f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
                    f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на 40атм.'
                   f'Спустить {CreatePZ.dict_pump_SHGN["posle"]} на компоновке штанг: {gno_nkt_opening(CreatePZ.dict_sucker_rod_po)}  Окончательный компоновку штанг производить по расчету '
                   f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
                   f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descent_sucker_pod(float(CreatePZ.dict_pump_SHGN_h["posle"]))],
                  [None, None,
                   f'Перед пуском  произвести подгонку штанг и '
                   f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 1.5],
                  ]

    descent_nn = [[None, None,
                   f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],
                  [None, None,
                   calc_fond_nkt_str,
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],

                  [None, None,
                   f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить сальниковые '
                   f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм.  \n'
                   f'Предварительно, по согласованию с ЦДНГ, спустить {CreatePZ.dict_pump_SHGN["posle"]} на гл {float(CreatePZ.dict_pump_SHGN_h["posle"])}м. (в компоновке предусмотреть установку '
                   f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
                   f'компоновка НКТ: {gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые).\n'
                   f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб.  ',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1)],
                  [None, None,
                   f'Демонтировать превентор. Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
                   f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.  ',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 1.27],

                  [None, None,
                   f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
                    f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на 40атм.'
                   f'Спустить плунжер на компоновке штанг: {gno_nkt_opening(CreatePZ.dict_sucker_rod_po)}  Окончательный компоновку штанг производить по расчету '
                   f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
                   f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descent_sucker_pod(float(CreatePZ.dict_pump_SHGN_h["posle"]))],
                  [None, None,
                   f'Перед пуском  произвести подгонку штанг и '
                   f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 1.5],
                  ]

    descent_nv_with_paker = [[None, None,
                              f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', None],
                             [None, None,
                              calc_fond_nkt_str,
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', None],

                             [None, None,
                              f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить сальниковые '
                              f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм.  \n'
                              f'Предварительно, по согласованию с ЦДНГ, спустить замковую опору на гл {float(CreatePZ.dict_pump_SHGN_h["posle"])}м. (в компоновке предусмотреть установку '
                              f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
                              f'компоновка НКТ: {gno_nkt_opening(CreatePZ.dict_nkt_po)} пакер - {CreatePZ.paker_do["posle"]} на глубину {CreatePZ.H_F_paker_do["posle"]}м  (завоз с УСО ГНО, ремонтные/новые).\n'
                              f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб.  ',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1.2)],

                             [None, None,
                              f'Демонтировать превентор. Посадить пакер на глубине {CreatePZ.H_F_paker_do["posle"]}м. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
                              f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.  ',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 1.27],
                             [None, None,
                              f'{testing_pressure(self, CreatePZ.H_F_paker_do["posle"])}',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 0.67],
                             [None, None,
                              f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
                              f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на 40атм.'
                              f'Спустить {CreatePZ.dict_pump_SHGN["posle"]} на компоновке штанг: {gno_nkt_opening(CreatePZ.dict_sucker_rod_po)}  Окончательный компоновку штанг производить по расчету '
                              f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
                              f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', descent_sucker_pod(float(CreatePZ.dict_pump_SHGN_h["posle"]))],
                             [None, None,
                              f'Перед пуском  произвести подгонку штанг и '
                              f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 1.5],
                             ]
    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - float(CreatePZ.H_F_paker_do["posle"]))) < 10 or abs(
                    float(interval[0] - float(CreatePZ.H_F_paker_do["posle"]))) < 10:
                if privyazkaNKT(self)[0] not in descent_nv_with_paker:
                    descent_nv_with_paker.insert(3, privyazkaNKT(self)[0])

    descent_nn_with_paker = [[None, None,
                              f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', None],
                             [None, None,
                              calc_fond_nkt_str,
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', None],

                             [None, None,
                              f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ). В ЦДНГ заявить сальниковые '
                              f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм.  \n'
                              f'Предварительно, по согласованию с ЦДНГ, спустить {CreatePZ.dict_pump_SHGN["posle"]} на гл {float(CreatePZ.dict_pump_SHGN_h["posle"])}м. '
                              f'пакер - {CreatePZ.paker_do["posle"]} на глубину {CreatePZ.H_F_paker_do["posle"]}м (в компоновке предусмотреть установку '
                              f'противополетных узлов (з.о. меньшего диаметра или заглушка с щелевым фильтром)) '
                              f'компоновка НКТ: {gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые).\n'
                              f' спуск ФНКТ произвести с шаблонированием  сотбраковкой с калибровкой резьб.  ',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1)],
                             [None, None,
                              f'Демонтировать превентор. Посадить пакер на глубине {CreatePZ.paker_do["posle"]}м. Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
                              f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН.  ',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 1.77],
                             [None, None,
                              f'{testing_pressure(self, CreatePZ.H_F_paker_do["posle"])}',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 0.67],
                             [None, None,
                              f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
                                f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на 40атм.'
                              f'Спустить плунжер на компоновке штанг: {gno_nkt_opening(CreatePZ.dict_sucker_rod_po)}  Окончательный компоновку штанг производить по расчету '
                              f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
                              f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', descent_sucker_pod(float(CreatePZ.dict_pump_SHGN_h["posle"]))],
                             [None, None,
                              f'Перед пуском  произвести подгонку штанг и '
                              f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика',
                              None, None, None, None, None, None, None,
                              'Мастер КРС, предст. заказчика', 1.5],
                             ]
    for plast in list(CreatePZ.dict_perforation.keys()):
        for interval in CreatePZ.dict_perforation[plast]['интервал']:
            if abs(float(interval[1] - float(CreatePZ.H_F_paker_do["posle"]))) < 10 or abs(
                    float(interval[0] - float(CreatePZ.H_F_paker_do["posle"]))) < 10:
                if privyazkaNKT(self)[0] not in descent_nn_with_paker:
                    descent_nn_with_paker.insert(3, privyazkaNKT(self)[0])
    descentORD = [[None, None,
                   f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],
                  [None, None,
                   calc_fond_nkt_str,
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', None],
                  [None, None,
                   f'Заявить  комплект подгоночных штанг,полированный шток (вывоз согласовать с ТС ЦДНГ), комплект НКТ.  В ЦДНГ заявить сальниковые '
                   f'уплотнения, подвесной патрубок, штанговые переводники, ЯГ-73мм.  \n',
                   None, None, None, None, None, None, None,
                   'Мастер КРС', None],
                  [None, None,
                   f'Спустить предварительно {CreatePZ.dict_pump_ECN["posle"]} на НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)} c пакером {CreatePZ.paker_do["posle"]} на'
                   f' глубину {CreatePZ.H_F_paker_do["posle"]}м'
                   f'(завоз с УСО ГНО, ремонтные/новые) на гл. {CreatePZ.dict_pump_ECN_h["posle"]}м. Спуск НКТ производить с шаблонированием и '
                   f'смазкой резьбовых соединений, замером изоляции каждые 100м.',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1.2)],
                  [None, None,
                   f'Демонтировать превентор. Посадить пакер на глубине {CreatePZ.H_F_paker_do["posle"]}м.  Монтаж  устьевой арматуры. При монтаже использовать только сертифицированное'
                   f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. произвести разделку'
                   f' кабеля под устьевой сальник '
                   f'произвести герметизацию устья. \n{testing_pressure(self, CreatePZ.H_F_paker_do["posle"])}',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 1.77],
                  [None, None,
                   f'Обвязать устье скважины согласно схемы №3 утвержденной главным '
                    f'инженером от 14.10.2021г при СПО штанг (ПМШ 62х21 либо аналог). Опрессовать ПВО на 40атм.'
                   f'Спустить {CreatePZ.dict_pump_SHGN["posle"]} на компоновке штанг: {gno_nkt_opening(CreatePZ.dict_sucker_rod_po)}  Окончательный компоновку штанг производить по расчету '
                   f'ГНО после утверждения заказчиком. ПРИ НЕОБХОДИМОСТИ ПОИНТЕРВАЛЬНОЙ ОПРЕССОВКИ: АВТОСЦЕП УСТАНАВЛИВАТЬ '
                   f'НЕ МЕНЕЕ ЧЕМ ЧЕРЕЗ ОДНУ ШТАНГУ ОТ ПЛУНЖЕРА ИЛИ ПЕРЕВОДНИКА ШТОКА НАСОСА!',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', descent_sucker_pod(float(CreatePZ.dict_pump_ECN_h["posle"]))],
                  [None, None,
                   f'Перед пуском  произвести подгонку штанг и '
                   f'опрессовать ГНО на давление 40атм в течении 30 минут в присутствии представителя заказчика с помощью ЦА-320 '
                   f'(составить акт). Предоставить Заказчику замер НКТ.',
                   None, None, None, None, None, None, None,
                   'Мастер КРС, предст. заказчика', 1.5],

                  ]
    descent_voronka = [
        [None, None,
         f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', None],
        [None, None,
         f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ,  произвести спуск '
         f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', None],

        [None, None,
         f'Спустить предварительно воронку на НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые) на '
         f'гл. {sum(list(CreatePZ.dict_nkt_po.values()))}м. Спуск НКТ производить с шаблонированием и '
         f'смазкой резьбовых соединений.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1)],
        [None, None,
         f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
         f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. произвести разделку'
         f' кабеля под устьевой сальник произвести герметизацию устья. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 1.27]]

    descent_orz = [
        [None, None,
         f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', None],
        [None, None,
         f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ,  произвести спуск '
         f'фондовых НКТ с поинтервальной опрессовкой через каждые 300м  с учетом статического уровня уровня',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', None],

        [None, None,
         f'Спустить двух пакерную компоновку ОРЗ на НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые) '
         f'на гл. {CreatePZ.H_F_paker_do["posle"]}/{float(CreatePZ.H_F_paker2_do["posle"])}м. Спуск НКТ производить с шаблонированием и '
         f'смазкой резьбовых соединений.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика',  descentNKT_norm(sum(list(CreatePZ.dict_nkt_po.values())), 1.2)],
        [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                     f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                     f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4],
        [None, None,
         f'Демонтировать превентор. Монтаж устьевой арматуры согласно схемы ОРЗ. При монтаже использовать только сертифицированное'
         f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. '
         f'акачать в межтрубное пространство раствор ингибитора коррозии.  ',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 1.77],
        [None, None,
         f'Опрессовать пакер и ЭК и арматуру ППД на Р= {CreatePZ.max_admissible_pressure}атм с открытым трубном пространством '
         f'в присутствии представителя заказчика на наличие перетоков.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 0.67],
        [None, None,
         f'Спустить стыковочное устройство на НКТ48мм до глубины {float(CreatePZ.H_F_paker2_do["posle"])}м с замером и шаблонированием. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', descentNKT_norm(float(CreatePZ.H_F_paker2_do["posle"]),1)],
        [None, None,
         f'Произвести стыковку. Смонтировать арматуру ОРЗ. Опрессовать пакер и арматуру ОРЗ в межтрубное пространство'
         f' на Р= {CreatePZ.max_admissible_pressure}атм с открытым трубном пространством '
         f'в присутствии представителя заказчика на наличие перетоков.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 0.67],
        [None, None,
         f'Произвести насыщение скважины в объеме не менее 5м3 в НКТ48мм. Произвести определение приемистости при давлении 100атм в присутствии '
         f'представителя заказчика. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 0.67+0.2+0.17],
        [None, None,
         f'Произвести насыщение скважины в объеме не менее 5м3 в межтрубное пространство. Произвести определение приемистости при давлении 100атм в присутствии '
         f'представителя заказчика. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', 0.67+0.2+0.17],
        [None, None,
         f'Согласовать с заказчиком завершение скважины.',
         None, None, None, None, None, None, None,
         'Мастер КРС, предст. заказчика', None],




    ]

    descent_ecn = [[None, None,
                    f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', None],
                   [None, None,
                    calc_fond_nkt_str,
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', None],

                   [None, None,
                    'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт).  '
                    'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного клапанов. ',
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', 0.3],
                   [None, None,
                    f'Спустить предварительно {CreatePZ.dict_pump_ECN["posle"]} на НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)} (завоз с УСО ГНО, ремонтные/новые) на '
                    f'гл. {CreatePZ.dict_pump_ECN_h["posle"]}м. Спуск НКТ производить с шаблонированием и '
                    f'смазкой резьбовых соединений, замером изоляции каждые 100м.  ',
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', descentNKT_norm(float(CreatePZ.dict_pump_ECN_h["posle"]), 1.2)],
                   [None, None,
                    f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
                    f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. произвести разделку'
                    f' кабеля под устьевой сальник '
                    f'произвести герметизацию устья. Опрессовать кабельный ввод устьевой арматуры',
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', 1.27],
                   [None, None,
                    f'Перед пуском УЭЦН опрессовать ГНО на 50атм в течении 30 минут в присутствии представителя заказчика с помощью ЦА-320 '
                    f'(составить акт). Предоставить Заказчику замер НКТ.',
                    None, None, None, None, None, None, None,
                    'Мастер КРС, предст. заказчика', 1],
                   ]
    descent_ecn_with_paker = [[None, None,
                               f'Заменить технологические НКТ на опрессованные эксплуатационные НКТ. Заменить подвесной патрубок на сертифицированный.',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', None],
                              [None, None,
                               calc_fond_nkt_str,
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', None],
                              [None, None,
                               'Опрессовать НКТ между УЭЦН и обратным клапаном, отдельно до спуска УЭЦН (составить акт).  '
                               'При монтаже УЭЦН провести калибровку резьбы: ловильной головки ЭЦН, обратного и сбивного клапанов. ',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', 0.3],
                              [None, None,
                               f'Спустить предварительно {CreatePZ.dict_pump_ECN["posle"]} на НКТ{gno_nkt_opening(CreatePZ.dict_nkt_po)}, '
                               f'пакер - {CreatePZ.paker_do["posle"]} на глубину {CreatePZ.H_F_paker_do["posle"]}м. (завоз с УСО ГНО, ремонтные/новые) '
                               f'на гл. {CreatePZ.dict_pump_ECN["posle"]}м. Спуск НКТ производить с шаблонированием и '
                               f'смазкой резьбовых соединений, замером изоляции каждые 100м.  ',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', descentNKT_norm(float(CreatePZ.dict_pump_ECN_h["posle"]), 1.2)],
                              [None, None,
                               f'Демонтировать превентор. Монтаж устьевой арматуры. При монтаже использовать только сертифицированное'
                               f' оборудование (переводники, муфты, переходные катушки). МОНТАЖ БЕЗ ПОДВЕСНОГО ПАТРУБКА ЗАПРЕЩЕН. произвести разделку'
                               f' кабеля под устьевой сальник '
                               f'произвести герметизацию устья. Опрессовать кабельный ввод устьевой арматуры',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', 1.77],
                              [None, None,
                               f'{testing_pressure(self, CreatePZ.H_F_paker_do["posle"])} Опрессовать кабельный ввод устьевой арматуры',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', 0.67],
                              [None, None,
                               f'Перед пуском УЭЦН опрессовать ГНО на 50атм в течении 30 минут в присутствии представителя заказчика с помощью ЦА-320 '
                               f'(составить акт). Предоставить Заказчику замер НКТ.',
                               None, None, None, None, None, None, None,
                               'Мастер КРС, предст. заказчика', 1],
                              ]

    lift_dict = {'НН с пакером': descent_nn_with_paker, 'НВ с пакером': descent_nv_with_paker,
                 'ЭЦН с пакером': descent_ecn_with_paker, 'пакер': paker_descent,
                 'ЭЦН': descent_ecn, 'НВ': descent_nv, 'НН': descent_nn, 'ОРД': descentORD, 'воронка': descent_voronka,
                 'ОРЗ': descent_orz}  # 'ОРЗ': lift_orz, 'ОРД': lift_ord, 'Воронка': lift_voronka,
    # 'НН с пакером': lift_pump_nn_with_paker, 'НВ с пакером': lift_pump_nv_with_paker,
    # 'ЭЦН с пакером': lift_ecn_with_paker,
    lift_sel = ['ЭЦН', 'НВ', 'НН', 'пакер', 'ОРД', 'НН с пакером', 'ЭЦН с пакером', 'НВ с пакером',
                'воронка', 'ОРЗ']  # 'ОРЗ', 'Воронка',

    lift_key = 'НВ'



    # print(('НВ' in CreatePZ.dict_pump_SHGN["posle"].upper() or 'ШГН' in CreatePZ.dict_pump_SHGN["posle"].upper()),
    #       CreatePZ.if_None(CreatePZ.paker_do["posle"]) != '0')
    if CreatePZ.dict_pump_ECN["posle"] != '0' and str(CreatePZ.paker_do["posle"]) == '0':
        lift_select = descent_ecn
        lift_key = 'ЭЦН'
    elif 89 in CreatePZ.dict_nkt_po.keys() and 48 in CreatePZ.dict_nkt_po.keys() and CreatePZ.if_None(
            CreatePZ.paker_do["posle"]) != '0':
        lift_select = descent_orz
        lift_key = 'ОРЗ'

    elif CreatePZ.dict_pump_ECN["posle"] != '0' and (CreatePZ.if_None(CreatePZ.paker_do["posle"]) == '0'):

        lift_select = descent_ecn_with_paker
        lift_key = 'ЭЦН с пакером'
        print('Подьем ЭЦН с пакером ')

    elif ('НВ' in CreatePZ.dict_pump_SHGN["posle"].upper() or 'ШГН' in CreatePZ.dict_pump_SHGN[
        "posle"].upper()) and CreatePZ.if_None(CreatePZ.paker_do["posle"]) == '0':
        lift_select = descent_nv
        lift_key = 'НВ'
    elif ('НВ' in CreatePZ.dict_pump_SHGN["posle"].upper() or 'ШГН' in CreatePZ.dict_pump_SHGN[
        "posle"].upper()) and CreatePZ.if_None(CreatePZ.paker_do["posle"]) != '0':
        lift_select = descent_nv_with_paker
        lift_key = 'НВ с пакером'

    elif 'НН' in CreatePZ.dict_pump_SHGN["posle"].upper() and CreatePZ.if_None(CreatePZ.paker_do["posle"]) == '0':
        lift_select = descent_nn
        lift_key = 'НН'
    elif 'НН' in CreatePZ.dict_pump_SHGN["posle"].upper() and CreatePZ.if_None(CreatePZ.paker_do["posle"]) != '0':
        lift_select = descent_nn_with_paker
        lift_key = 'НН с пакером'
    elif CreatePZ.dict_pump_SHGN["posle"] != '0' and CreatePZ.dict_pump_ECN["posle"] != '0':
        lift_select = descentORD
        lift_key = "ОРД"
    elif 'НН' in CreatePZ.dict_pump_SHGN["posle"] and CreatePZ.if_None(CreatePZ.paker_do["posle"]) != '0':
        lift_select = descent_nn_with_paker
        lift_key = "НН с пакером"
        print('Подьем НН с пакером ')

    elif CreatePZ.dict_pump_SHGN["posle"] == '0' and CreatePZ.dict_pump_ECN["posle"] == '0' and CreatePZ.if_None(
            CreatePZ.paker_do["posle"]) == '0':
        lift_select = descent_voronka
        lift_key = 'воронка'
        print('Подьем  воронки')
    elif CreatePZ.dict_pump_SHGN["posle"] == '0' and CreatePZ.dict_pump_ECN["posle"] == '0' and CreatePZ.if_None(
            CreatePZ.paker_do["posle"]) != '0':
        lift_select = paker_descent
        lift_key = 'пакер'
        lift_s = f'пакер ППД  {CreatePZ.paker_do["posle"]}'
    # elif 89 in CreatePZ.dict_nkt.keys() and 48 in CreatePZ.dict_nkt.keys() and CreatePZ.if_None(
    #         CreatePZ.paker_do["posle"]) != '0':
    #     lift_select = lift_orz
    #     print('Подьем ОРЗ')

    lift, ok = QInputDialog.getItem(self, 'Спуcкаемое  оборудование', 'выбор спуcкаемого оборудования',
                                    lift_sel, lift_sel.index(lift_key), False)

    if ok and lift_sel:
        self.le.setText(lift)
    lift_select = lift_dict[lift]
    for row in lift_select:
        gno_list.append(row)



    end_list = [[None, None,
                 f'Все работы производить с соблюдением т/б и технологии'
                 f' согласно утвержденному плану. Демонтировать подьемный агрегат и оборудование. Пустить скважину в работу.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', float(8.5)],
                [None, None,
                 f'При всех работах не допускать утечек пластовой жидкости и жидкости глушения. В случае пропуска, разлива,'
                 f' немедленно производить зачистку территории.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1],
                [None, None,
                 f'Произвести заключительные работы  после ремонта скважины.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 1],
                [None, None,
                 f'Сдать скважину представителю ЦДНГ.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', 1]]

    for row in end_list:
        gno_list.append(row)

    return gno_list


def gno_nkt_opening(dict_nkt_po):
    print(dict_nkt_po)
    str_gno = ''
    for nkt, length_nkt in dict_nkt_po.items():
        str_gno += f'{nkt}мм - {length_nkt}м, '
    return str_gno


def PzakPriGis(self):
    from open_pz import CreatePZ
    if CreatePZ.region == 'ЧГМ' and CreatePZ.expected_P < 80:
        return 80
    else:
        return CreatePZ.expected_P

def calc_fond_nkt(self, len_nkt):

    from open_pz import CreatePZ
    # расчет необходимого давления опрессовки НКТ при спуске
    static_level = CreatePZ.static_level
    fluid = CreatePZ.fluid
    distance_between_nkt, ok = QInputDialog.getInt(self, 'Расстояние между НКТ',
                                                   f'Расстояние между НКТ для опрессовки', 300, 50,
                                                   501)
    pressuar = 40
    print(f' ЭЦН {CreatePZ.dict_pump_ECN["posle"]}')
    if CreatePZ.dict_pump_ECN["posle"] != "0":
        pressuar = 50

    pressuar_nkt, ok = QInputDialog.getInt(self, 'Давление опрессовки ГНО ',
                                          f'Давление опрессовки ГНО расчетное', pressuar, 20, 100)

    calc = CalcFond(static_level, len_nkt, fluid, pressuar_nkt, distance_between_nkt)
    calc_fond_dict = calc.calc_pressuar_list()
    press_str = f'В случае незавоза новых или завоза неопрессованных НКТ, согласовать алгоритм опрессовки с ЦДНГ, ' \
                f'произвести спуск  фондовых НКТ с поинтервальной опрессовкой через каждые {distance_between_nkt}м '\
                 f'с учетом статического уровня уровня на на глубине {static_level}м  по телефонограмме заказчика '\
                 f'в следующей последовательности:\n'
    n = 0
    for nkt, pressuar in calc_fond_dict.items():

        press_str += f'Опрессовать НКТ в интервале {n} - {nkt} на давление {pressuar}атм \n'
        n = nkt

    return  press_str