from PyQt5.QtWidgets import QInputDialog, QMessageBox

import krs
from main import MyWindow
from work_py.alone_oreration import kot_select
from work_py.opressovka import testing_pressure
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm

def grpGpp(self):
    from open_pz import CreatePZ

    nkt_diam = ''.join(['89' if CreatePZ.column_diametr > 110 else '60'])

    gPP_depth, ok = QInputDialog.getInt(None, 'глубина ',
                                        'Введите глубину установки',
                                        int(CreatePZ.perforation_roof - 50), 0, int(CreatePZ.bottomhole_drill))


    gpp_list = [
        ['За 48 часов оформить заявку на завоз оборудования ГРП.',
         None, f'За 48 часов оформить заявку на завоз оборудования ГРП. Уложить НКТ на дополнительные стеллажи',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [None, None,
         f'Спуск производить с применением спец.смазки  и рекомендуемым моментом свинчивания для НКТ{nkt_diam}мм(N-80)'
         f' согласно плана от подрядчика по ГРП.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [f'СПО: {gpp_select(gPP_depth)[0]} на НКТ{nkt_diam} на Н {gPP_depth}м', None,
         f'Спустить компоновку с замером и шаблонированием НКТ: {gpp_select(gPP_depth)[0]} на НКТ{nkt_diam} на глубину {gPP_depth}м, с замером, шаблонированием НКТ. '
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(gPP_depth, 1.2)],
        [None, None, f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
                     f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
                     f'В случае отсутствия представителя подрядчика по ГРП ltd оповестить Заказчика письменной '
                     f'телефонограммой и выйти в вынужденный простой.',
         None, None, None, None, None, None, None,
         'мастер КРС', ''],
        [f'Привязка по ГК и ЛМ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                     f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                     f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4],
        [f'Установить ГПП  на гл. {gPP_depth}м', None, f'Установить ГПП  на гл. {gPP_depth}м. В случае отсутствия представителя подрядчика по ГРП ltd '
                     f'оповестить Заказчика письменной телефонограммой и выйти в вынужденный простой.',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП', 1.2],
        [None, None,
         f'Письменно согласовать с Заказчиком: 1. ожидание ГРП за обваловкой; 2.переезд на другую скважину.',
         None, None, None, None, None, None, None,
         'Мастер КРС, заказчик', " "],
        [None, None,
         f'Обвязать устье скважины согасно схемы ПВО №7 утвержденной главным инженером ООО "Ойл-сервис" '
         f'от 14.10.2021г для проведения ГРП на месторождениях ООО "БашнефтьДобыча". Посадить планшайбу. Произвести демонтаж'
         f' оборудования. Опрессовать установленную арматуру для ГРП на Р={CreatePZ.max_admissible_pressure}атм, '
         f'составить акт в присутствии следующих представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. '
         f'В случае негерметичности арматуры, составить акт и устранить негерметичность под руководством следующих '
         f'представителей:  УСРСиСТ (супервайзер), подрядчика по ГРП .',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП, УСРСиСТ', 1.2],
        [None, None,
         f'Освободить территорию куста от оборудования бригады.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ заказчика', 7.2],
        [None, None,
         f'Проведение работ ГРП силами  подрядчика по ГРП по дизайну, сформированному технологической службой подрядчика'
         f' по ГРП (дизайн ГРП)',
         None, None, None, None, None, None, None,
         'Подрядчик по ГРП', None],
        [None, None,
         f'За 24 часа дать заявку на вывоз оборудования ГРП.',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП', None],
        [None, None,
         f'Принять территорию скважины у представителя заказчика с составлением 3-х стороннего акта. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика, подрядчик по ГРП', None],
        [None, None,
         f'ПРИ ПРИЕМЕ СКВАЖИНЫ В РЕМОНТ УБЕДИТЬСЯ В ОТСУТСТВИИ ИЗБЫТОЧНОГО ДАВЛЕНИЯ (ДАВЛЕНИЕ РАВНО АТМОСФЕРНОМУ) '
         f'И В СВОДНОМ ОТКРЫТИИ ЗАДВИЖЕК), ПРИ НЕОБХОДИМОСТИ ДАТЬ ЗАЯВКУ в ЦДНГ ОБ ОТОГРЕВЕ АРМАТУРЫ С ИСПОЛЬЗОВАНИЕМ ППУ.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика, подрядчик по ГРП', 2.5],
        [None, None,
         f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
         f'глушения скважины, работы производить в присутствии представителей подрядной организации по проведению ГРП и УСРСиСТ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 0.37],
        [None, None,
         f'После разрядки скважины в объеме не менее 25м3, подтвержденной представителями ЦДНГ согласовать проведение '
         f'ГИС -пластомер для расчета жидкости глушения, произвести перерасчет ЖГ и проглушить скважину соответствующей '
         f'жидкостью. Дальнейшие работы продолжить на жидкости глушения согласно расчета. В случае отрицательных '
         f'результатов согласовать съезд бригады',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 8],
        [None, None,
         krs.lifting_unit(self),
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 4.2],
        [f'смену объема  уд.весом {CreatePZ.fluid_work} на циркуляцию '
         f'в объеме {krs.volume_jamming_well(self, CreatePZ.current_bottom)}м3', None,
         f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {CreatePZ.fluid_work} на циркуляцию '
         f'в объеме {krs.volume_jamming_well(self, CreatePZ.current_bottom)}м3. Закрыть скважину на стабилизацию не менее 2 часов. \n'
         f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', well_volume_norm(krs.volume_jamming_well(self, CreatePZ.current_bottom))],
        [None, None,
         f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
         f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей промывок '
         f'согласовать с Заказчиком.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', None],
        [None, None,
         krs.pvo_gno(CreatePZ.kat_pvo)[0],
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 4.67],
        [None, None,
         f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 1],
        [None, None,
         f'Поднять устройство ГПП на НКТ{nkt_diam}мм с глубины {gPP_depth}м на поверхность, '
         f'с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  в объеме '
         f'{round(gPP_depth * 1.12 / 1000, 1)}м3. \n'
         f'На демонтаж пригласить представителя подрядчика по ГРП',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', liftingNKT_norm(gPP_depth,1.2)],
    ]

    gisOTZ_true_quest = QMessageBox.question(self, 'отбивка забоя ',
                                             'Нужно ли отбивать забой после подьема пакера ГРП?')

    if gisOTZ_true_quest == QMessageBox.StandardButton.Yes:
        gpp_list.append(
            [f'Отбить забой по ГК и ЛМ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                         f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4])
    else:
        pass
    normalization_true_quest = QMessageBox.question(self, 'Нормализация забоя ',
                                                    'Нужно ли нормализовывать забой после подьема пакера ГРП?')
    if normalization_true_quest == QMessageBox.StandardButton.Yes:
        for row in normalization(self):
            gpp_list.append(row)
    else:
        pass
    return gpp_list


def normalization(self):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])

    current_depth, ok = QInputDialog.getInt(None, 'Нормализация забоя',
                                            'Введите глубину необходмого забоя',
                                            int(CreatePZ.current_bottom), 0, int(CreatePZ.bottomhole_artificial + 500))
    normalization_list = [
        [f'Согласовать Алгоритм нормализации до H- {current_depth}м', None, f'Алгоритм работ согласовать с Заказчиком: \n'
                     f'В случае освоения скважины ГНКТ и дохождение до гл. не ниже {CreatePZ.current_bottom}м перейти к отбивки забоя '
                     f'В случае если скважину не осваивали ГНКТ продолжить работы со следующего пункта.\n'
                     f'В случае наличия ЗУМПФА не менее 10м продолжить работы со следующего пункта.\n'
                     f'В случае наличия циркуляции при глушении скважины произвести работы  СПО пера \n'
                     f'В случае отсутствия циркуляции при глушении скважины произвести работы  СПО ГВЖ',
         None, None, None, None, None, None, None,
         'Мастер КРС', None],
        [None, None,
         f'Спустить компоновку с замером и шаблонированием НКТ: перо (1м), {nktGrp(self)} на НКТ{nkt_diam} до гл.текущего забоя.'
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
         None, None, None, None, None, None, None,
         'Мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [f'нормализацию забоя до гл. {current_depth}м', None,
         f'Произвести нормализацию забоя  с наращиванием, комбинированной  промывкой по круговой циркуляции  жидкостью '
         f'с расходом жидкости не менее 8 л/с до гл. {current_depth}м. Тех отстой 2ч. Повторное определение '
         f'текущего забоя, при необходимости повторно вымыть.',
         None, None, None, None, None, None, None,
         'Мастер КРС', 2.5],
        [None, None,
         f'Поднять перо с глубины {current_depth}м с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  в объеме '
         f'{round(current_depth * 1.12 / 1000, 1)}м3',
         None, None, None, None, None, None, None,
         'Мастер КРС', liftingNKT_norm(current_depth, 1)],
        [None, None,
         f'Спустить {kot_select(self)} на НКТ{CreatePZ.nkt_diam}мм до глубины текущего забоя'
         f' с замером, шаблонированием шаблоном.',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(CreatePZ.current_bottom, 1)],
        [None, None,
         f'Произвести очистку забоя скважины до гл.{current_depth}м закачкой обратной промывкой тех жидкости уд.весом {CreatePZ.fluid_work}, по согласованию с Заказчиком',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'При необходимости согласовать закачку блок пачки по технологическому плану работ подрядчика',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', None],
        [None, None,
         f'Поднять {kot_select(self)} на НКТ{CreatePZ.nkt_diam} c глубины {current_depth}м с доливом скважины в '
         f'объеме {round(current_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
         None, None, None, None, None, None, None,
         'мастер КРС', liftingNKT_norm(current_depth, 1)],
        [None, None,
         f'В случае наличия ЗУМПФа 10м и более продолжить работы с п. по отбивки забоя '
         f'В случае ЗУМПФа менее 10м: и не жесткая посадка компоновки СПО ГВЖ повторить. '
         f'В случае образование твердой корки (жесткой посадки): выполнить взрыхление ПМ с ВЗД'
         f' и повторить работы СПО ГВЖ.',
         None, None, None, None, None, None, None,
         'Мастер КРС', None],
        [None, None,
         f'Спустить компоновку с замером и шаблонированием НКТ:  долото Д={paker_diametr_select(CreatePZ.current_bottom) + 2}мм, забойный двигатель,'
         f' НКТ - 20м, вставной фильтр, НКТмм до кровли проппантной пробки. '
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) ',
         None, None, None, None, None, None, None,
         'Мастер КРС', descentNKT_norm(current_depth, 1.2)],
        [None, None,
         f'Подогнать рабочую трубу патрубками на заход 9-10м. Вызвать циркуляцию прямой промывкой. '
         f'Произвести допуск с прямой промывкой и рыхление проппантной пробки 10м с проработкой э/колонны по 10 раз. ',
         None, None, None, None, None, None, None,
         'Мастер КРС', 0.9],
        [None, None,
         f'Поднять компоновку с глубины {current_depth}м с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  в объеме '
         f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3',
         None, None, None, None, None, None, None,
         'Мастер КРС', liftingNKT_norm(current_depth,1.2)],
        [f'по согласованию с заказчиком: Отбивка забоя', None, f'по согласованию с заказчиком: \n'
                     f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                     f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                     f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4]]
    return normalization_list


def gpp_select(paker_depth):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    if CreatePZ.column_diametr > 120:
        nkt_diam = '89'
    else:
        nkt_diam = '60'
    if CreatePZ.column_additional == True and CreatePZ.column_additional_diametr <= 120:
        nkt_diam_add = '60'

    if CreatePZ.column_additional == False or (
            CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional):
        paker_select = f'гидропескоструйный перфоратор под ЭК {CreatePZ.column_diametr}мм-{CreatePZ.column_wall_thickness}мм+' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м,'
        paker_short = f'ГПП под ЭК {CreatePZ.column_diametr}мм-{CreatePZ.column_wall_thickness}мм+' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, репер НКТ{nkt_diam}мм - 2м,'
    else:

        paker_select = f'гидропескоструйный перфоратор под ЭК {CreatePZ.column_additional_diametr}мм-{CreatePZ.column_additional_wall_thickness}мм +' \
                       f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, реперный патрубок НКТ{nkt_diam_add}мм - 2м, + НКТ{nkt_diam_add} L-' \
                       f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'
        paker_short = f'ГПП под ЭК {CreatePZ.column_additional_diametr}мм-{CreatePZ.column_additional_wall_thickness}мм +' \
                       f'опрессовочный узел +НКТ{nkt_diam_add}мм - 10м, репер НКТ{nkt_diam_add}мм - 2м, + НКТ{nkt_diam_add} L-' \
                       f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'

    return paker_select, paker_short


def paker_select(paker_depth):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    if CreatePZ.column_diametr > 120:
        nkt_diam = '89'
    elif 110 < CreatePZ.column_diametr < 120:
        nkt_diam = '73'
    else:
        nkt_diam = '60'
    paker_select = ''
    print(f'пакер ГРП {paker_diametr_select(paker_depth)}')
    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional):
        paker_select = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ГРП для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м'
        paker_short = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ГРП для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м'

    else:
        paker_select = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ГРП для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм+' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м, + НКТ{nkt_diam} ' \
                       f' L-{round(paker_depth - CreatePZ.head_column_additional, 0)}м'
        paker_short = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ГРП для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм+' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м, + НКТ{nkt_diam} ' \
                       f' L-{round(paker_depth - CreatePZ.head_column_additional, 0)}м'
    return paker_select, paker_short


def grpPaker(self):
    from open_pz import CreatePZ

    nkt_diam = ''.join(['89' if CreatePZ.column_diametr > 110 else '60'])

    paker_depth, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки пакера ГРП',
                                          int(CreatePZ.perforation_roof - 50), 0, int(CreatePZ.current_bottom - 10))
    paker_depth = MyWindow.true_set_Paker(self, paker_depth)
    paker_list = [
        [f'За 48 часов оформить заявку на завоз оборудования ГРП.', None, f'За 48 часов оформить заявку на завоз оборудования ГРП. Уложить НКТ на дополнительные стеллажи',
         None, None, None, None, None, None, None,
         'мастер КРС', None],

        [None, None,
         f'Спуск производить с применением спец.смазки  и рекомендуемым моментом свинчивания для НКТ{nkt_diam}мм(N-80)'
         f' согласно плана от подрядчика по ГРП.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],

        [f'СПО: {paker_select(self, paker_depth)[1]} на НКТ{nkt_diam}мм на Н {paker_depth}м', None,
         f'Спустить компоновку с замером и шаблонированием НКТ: {paker_select(self, paker_depth)[0]} на НКТ{nkt_diam}мм на глубину {paker_depth}м, с замером, шаблонированием НКТ. '
         f'{"".join(["(Произвести пробную посадку на глубине 50м)" if CreatePZ.column_additional == False else " "])}',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(paker_depth,1.2)],
        [None, None, f'При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ) '
                     f'Сборку компоновки производить только под руководством представителя подрядчика по ГРП'
                     f'В случае отсутствия представителя подрядчика по ГРП ltd оповестить Заказчика письменной '
                     f'телефонограммой и выйти в вынужденный простой.',
         None, None, None, None, None, None, None,
         'мастер КРС', ''],
        [f'Привязка по ГК и ЛМ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                     f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                     f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины Отбить забой по ГК и ЛМ',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 4],
        [None, None,
         f'Посадить пакер с учетом расположения муфтовых соединений э/колонны под руководством представителя '
         f'подрядчика по ГРП. на гл. {paker_depth}м. В случае отсутствия представителя подрядчика по ГРП ltd '
         f'оповестить Заказчика письменной телефонограммой и выйти в вынужденный простой.',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП', 0.77],
        [testing_pressure(self, paker_depth)[1], None,
         f'{testing_pressure(self, paker_depth)[0]}. Опрессовку производить в присутствии следующих '
         f'представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. \n В случае негерметичности пакера, дальнейшие '
         f'работы согласовать с Заказчиком. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП, УСРСиСТ', 0.67],
        [None, None,
         f'Письменно согласовать с Заказчиком: 1. ожидание ГРП за обваловкой; 2.переезд на другую скважину.',
         None, None, None, None, None, None, None,
         'Мастер КРС, заказчик', " "],
        [None, None,
         f'Демонтировать ПВО. Обвязать устье скважины согасно схемы ПВО №7а утвержденной главным инженером ООО "Ойл-сервис" '
         f'от 14.10.2021г для проведения ГРП на месторождениях ООО "БашнефтьДобыча". Посадить планшайбу. Произвести демонтаж'
         f' оборудования. Опрессовать установленную арматуру для ГРП на Р={CreatePZ.max_admissible_pressure}атм, '
         f'составить акт в присутствии следующих представителей: УСРСиСТ (супервайзер), подрядчика по ГРП. '
         f'В случае негерметичности арматуры, составить акт и устранить негерметичность под руководством следующих '
         f'представителей:  УСРСиСТ (супервайзер), подрядчика по ГРП .',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП, УСРСиСТ', 1.2],
        [None, None,
         f'Освободить территорию куста от оборудования бригады.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ заказчика', 7.2],
        [None, None,
         f'Проведение работ ГРП силами  подрядчика по ГРП по дизайну, сформированному технологической службой подрядчика'
         f' по ГРП (дизайн ГРП)',
         None, None, None, None, None, None, None,
         'Подрядчик по ГРП', None],
        [None, None,
         f'За 24 часа дать заявку на вывоз оборудования ГРП.',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГРП', None],
        [None, None,
         f'Принять территорию скважины у представителя заказчика с составлением 3-х стороннего акта. ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика, подрядчик по ГРП', None],
        [None, None,
         f'ПРИ ПРИЕМЕ СКВАЖИНЫ В РЕМОНТ УБЕДИТЬСЯ В ОТСУТСТВИИ ИЗБЫТОЧНОГО ДАВЛЕНИЯ (ДАВЛЕНИЕ РАВНО АТМОСФЕРНОМУ) '
         f'И В СВОДНОМ ОТКРЫТИИ ЗАДВИЖЕК), ПРИ НЕОБХОДИМОСТИ ДАТЬ ЗАЯВКУ в ЦДНГ ОБ ОТОГРЕВЕ АРМАТУРЫ С ИСПОЛЬЗОВАНИЕМ ППУ.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика, подрядчик по ГРП', 2.5],
        [None, None,
         f'При избыточном давлении менее 10атм и изливе до 30м3/сут предусмотреть срыв пакера для последующего'
         f'глушения скважины, работы производить в присутствии представителей подрядной организации по проведению ГРП и УСРСиСТ',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 0.5],
        [f'При избыточном давлении более 10атм - разрядка не более 25м3', None,
         f'После разрядки скважины в объеме не менее 25м3, подтвержденной представителями ЦДНГ согласовать проведение '
         f'ГИС -пластомер для расчета жидкости глушения, произвести перерасчет ЖГ и проглушить скважину соответствующей '
         f'жидкостью. Дальнейшие работы продолжить на жидкости глушения согласно расчета. В случае отрицательных '
         f'результатов согласовать съезд бригады',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 8],
        [None, None,
         krs.lifting_unit(self),
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 4.2],
        [f'сменf объема уд.весом {CreatePZ.fluid_work} на циркуляцию '
         f'в объеме {krs.volume_jamming_well(self, CreatePZ.current_bottom)}м3', None,
         f'Произвести смену объема обратной промывкой тех жидкостью уд.весом {CreatePZ.fluid_work} на циркуляцию '
         f'в объеме {krs.volume_jamming_well(self, CreatePZ.current_bottom)}м3. Закрыть скважину на стабилизацию не менее 2 часов. \n'
         f'(согласовать глушение в коллектор, в случае отсутствия на желобную емкость)',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', well_volume_norm((krs.volume_jamming_well(self, CreatePZ.current_bottom)))],
        [None, None,
         f'Вести контроль плотности на  выходе в конце глушения. В случае отсутствия циркуляции на выходе жидкости '
         f'глушения уд.весом  или Рбуф при глушении скважины, дальнейшие промывки и удельный вес жидкостей промывок '
         f'согласовать с Заказчиком.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', None],
        [krs.pvo_gno(CreatePZ.kat_pvo)[1], None,
         krs.pvo_gno(CreatePZ.kat_pvo)[0],
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 1.67],
        [None, None,
         f'Провести практическое обучение вахт по сигналу ВЫБРОС.',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', 1],
        [None, None,
         f'Поднять пакер ГРП на НКТ{nkt_diam}мм с глубины {paker_depth}м на поверхность, '
         f'с доливом скважины тех.жидкостью уд. весом {CreatePZ.fluid_work}  в объеме '
         f'{round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3. \n'
         f'На демонтаж пригласить представителя подрядчика по ГРП',
         None, None, None, None, None, None, None,
         'Мастер КРС, представ. заказчика', liftingNKT_norm(paker_depth,1.2)],
        [None, None,
         f'Опрессовать глухие плашки превентора на максимально ожидаемое давление {CreatePZ.max_expected_pressure}атм, но не выше '
         f'максимально допустимого давления опрессовки эксплуатационной колонны с выдержкой в течении 30 минут,в случае невозможности '
         f'опрессовки по результатам определения приемистости и по согласованию с заказчиком  опрессовать глухие плашки ПВО на давление поглощения, '
         f'но не менее 30атм и  с составлением акта на опрессовку ПВО с представителем Заказчика. ', None,
         None,
         None, None, None, None, None,
         'Мастер КРС', 0.67],

    ]

    gisOTZ_true_quest = QMessageBox.question(self, 'отбивка забоя ',
                                             'Нужно ли отбивать забой после подьема пакера ГРП?')

    if gisOTZ_true_quest == QMessageBox.StandardButton.Yes:
        paker_list.append(
            [f'Отбить забой по ГК и ЛМ', None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                         f'Произвести  монтаж ПАРТИИ ГИС согласно схемы  №8а утвержденной главным инженером от 14.10.2021г. '
                         f'ЗАДАЧА 2.8.2 Отбить забой по ГК и ЛМ',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 4])
    else:
        pass
    normalization_true_quest = QMessageBox.question(self, 'Нормализация забоя ',
                                                    'Нужно ли нормализовывать забой после подьема пакера ГРП?')
    if normalization_true_quest == QMessageBox.StandardButton.Yes:
        for row in normalization(self):
            paker_list.append(row)
    else:
        pass
    return paker_list





def paker_select(self, paker_depth):
    from open_pz import CreatePZ
    from work_py.opressovka import paker_diametr_select
    if CreatePZ.column_diametr > 120:
        nkt_diam = '89'
    elif 110 < CreatePZ.column_diametr < 120:
        nkt_diam = '73'
    else:
        nkt_diam = '60'

    if CreatePZ.column_additional == False or CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional:
        paker_select = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)} (либо аналог) +' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м,'
        paker_short = f'в-ка, НКТ{nkt_diam}мм - 1,5м, пакер {paker_diametr_select(paker_depth)}  +' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, репер НКТ{nkt_diam}мм - 2м,'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth > CreatePZ.head_column_additional:
        paker_select = f'воронка, НКТ{nkt_diam}мм - 1,5м, пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)} (либо аналог) +' \
                       f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, реперный патрубок НКТ{nkt_diam}мм - 2м, + НКТ{nkt_diam} L-' \
                       f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'
        paker_short = f'в-ка, НКТ{nkt_diam}мм - 1,5м, пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}' \
                      f'опрессовочный узел +НКТ{nkt_diam}мм - 10м, репер НКТ{nkt_diam}мм - 2м,' \
                      f'{round(paker_depth - CreatePZ.head_column_additional, 0)}м'


    return paker_select, paker_short


def nktGrp(self):
    from open_pz import CreatePZ

    if CreatePZ.column_additional == False or (
            CreatePZ.column_additional == True and CreatePZ.current_bottom >= CreatePZ.head_column_additional):
        return f'НКТ{CreatePZ.nkt_diam}мм'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110:
        return f'НКТ60мм L- {round(CreatePZ.current_bottom - CreatePZ.head_column_additional + 20, 0)}'
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110:
        return f'НКТ{CreatePZ.nkt_diam}мм со снятыми фасками L- {round(CreatePZ.current_bottom - CreatePZ.head_column_additional + 20, 0)}'
