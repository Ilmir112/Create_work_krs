from PyQt5.QtWidgets import QInputDialog, QMessageBox

import krs
from work_py.acids_work import acid_work_list
from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm

def acid_work(self):
    from work_py.opressovka import paker_diametr_select
    from open_pz import CreatePZ

    from work_py.swabbing import swabbing_with_paker

    swabbing_true_quest = QMessageBox.question(self, 'Свабирование на данной компоновке',
                                               'Нужно ли Свабировать на данной компоновке?')

    if swabbing_true_quest == QMessageBox.StandardButton.Yes:
        swabbing_true_quest = True
    else:
        swabbing_true_quest = False



    paker_depth_bottom, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки нижнего пакера {CreatePZ.work_perforations["интервал"]}', int(CreatePZ.perforation_sole + 10), 0,
                                          int(CreatePZ.current_bottom))
    paker_depth_top, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                 'Введите глубину посадки вверхнего пакера {CreatePZ.work_perforations["интервал"]}', int(CreatePZ.perforation_sole- 10),
                                                 0, paker_depth_bottom)
    difference_paker =  paker_depth_bottom - paker_depth_top
    paker_khost_top = int(CreatePZ.perforation_sole - paker_depth_bottom)

    paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
                                          f'Введите длину хвостовика при посадке пакера нижнего пакера на {paker_depth_bottom} и текущем забое {CreatePZ.current_bottom}',
                                          paker_khost_top, 0, 4000)

    if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and paker_depth_bottom < CreatePZ.head_column_additional):
        paker_select = f'заглушку + сбивной с ввертышем + НКТ{CreatePZ.nkt_diam}м {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth_bottom)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr_select(paker_depth_bottom)} + НКТ{CreatePZ.nkt_diam}мм 20м +реперный патрубок на НКТ{CreatePZ.nkt_diam}'
        dict_nkt = {73: paker_depth_bottom}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and paker_depth_bottom > CreatePZ.head_column_additional:
        paker_select = f'заглушку + сбивной с ввертышем + НКТ{60}мм {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth_bottom)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ{60} {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr_select(paker_depth_bottom)} + НКТ{60}мм 20м +реперный патрубок на НКТ{60} {CreatePZ.head_column_additional-paker_depth_bottom}'
        dict_nkt = {73: CreatePZ.head_column_additional-10, 60: int(paker_depth_bottom - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth_bottom > CreatePZ.head_column_additional:
        paker_select = f'заглушку + сбивной с ввертышем + НКТ73 со снятыми фасками {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth_bottom)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + щелевой фильтр НКТ73 со снятыми фасками {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr_select(paker_depth_bottom)} + НКТ73 со снятыми фасками 20м +реперный патрубок на НКТ73 со снятыми фасками {CreatePZ.head_column_additional - paker_depth_bottom}'

        dict_nkt = {73: paker_depth_bottom}
    elif CreatePZ.nkt_diam == 60:
        dict_nkt = {60: paker_depth_bottom}



    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{CreatePZ.nkt_diam}мм до глубины нижнего пакера  до {paker_depth_bottom}, вверхнего пакера на {paker_depth_top}'
         f' с замером, шаблонированием шаблоном. /n {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
         f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
         f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
         None, None, None, None, None, None, None,
         'мастер КРС', descentNKT_norm(paker_depth_bottom, 1.2)],
        [None, None, f'Вызвать геофизическую партию. Заявку оформить за 16 часов сутки через ЦИТС "Ойл-сервис". '
                     f'При необходимости  подготовить место для установки партии ГИС напротив мостков. '
                     f'Произвести  монтаж ГИС согласно схемы №8а утвержденной главным инженером от 14.10.2021г',
         None, None, None, None, None, None, None,
         'Мастер КРС', None, None, None],
        [None, None, f'ЗАДАЧА 2.8.1 Привязка технологического оборудования скважины',
         None, None, None, None, None, None, None,
         'Мастер КРС', 4, None, None],
        [None, None, f'Посадить пакера на глубине {paker_depth_bottom}/{paker_depth_top}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.5],
        [None, None,
         f'Опрессовать эксплуатационную колонну в интервале {paker_depth_top}-0м на Р={CreatePZ.max_admissible_pressure}атм'
         f' в течение 30 минут в присутствии представителя заказчика, составить акт.  '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 0.83+0.58],
        [None, None,
         f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
         f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.7],
        [None, None,
         f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
         f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
         f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
         f'Определить приемистость НЭК.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        ]

    n = 0
    for row in acid_work_list(self, paker_depth_bottom, paker_khost, dict_nkt, CreatePZ.paker_layout):
        paker_list.append(row)
        n += 1

    reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, CreatePZ.nkt_diam, paker_depth_bottom)

    paker_list.extend(acid_true_quest_list)

    if swabbing_true_quest:

        swabbing_with_paker = swabbing_with_paker(self, difference_paker, 2)[1:]
        for row in swabbing_with_paker:
            paker_list.append(row)
    else:

        paker_list.append([None, None,
                                 f'Поднять {paker_select} на НКТ{CreatePZ.nkt_diam} c глубины {paker_depth_bottom}м с доливом скважины в '
                                 f'объеме {round(paker_depth_bottom * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', liftingNKT_norm(paker_depth_bottom, 1.2)])
    return paker_list

acid_true_quest_list = []
def reply_acid(self, difference_paker,  paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom):
    from open_pz import CreatePZ
    acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                           'Нужно ли планировать кислоту на следующий объет?')

    if acid_true_quest == QMessageBox.StandardButton.Yes:

        paker_depth_bottom, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                     f'Введите глубину нижнего пакера посадки пакера ',
                                                     int(CreatePZ.perforation_roof - 20), 0,
                                                     5000)
        acid_true_quest_list.append([None, None, f'Приподнять пакера на глубине {paker_depth_bottom}/{paker_depth_bottom-difference_paker}м', None, None, None, None, None, None, None,
                           'мастер КРС', 0.83+0.05])

        for row in acid_work_list(self,  paker_depth_bottom, paker_khost, dict_nkt, CreatePZ.paker_layout):
            acid_true_quest_list.append(row)

        # print(reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom))
        reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom)

    else:
        return acid_true_quest_list


def acidGons(self):
    from open_pz import CreatePZ
    plast, ok = QInputDialog.getItem(self, 'выбор пласта для ОПЗ ', 'выберете пласта дл перфорации',
                                     CreatePZ.plast_work, 0, False)
    acid_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка']
    acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты:', acid_list, 0, False)
    if ok and acid_list:
        self.le.setText(acid)
    acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
    acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
    acid_countOfpoint, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите объем кислоты на точку', 5, 1, 24)
    acid_points, ok = QInputDialog.getText(self, 'точки ГОНС', 'Введите точки ГОНС ')
    bottom_point = max(list(map(int, acid_points.replace('м', '').replace(',', '').split())))
    gons_list = [[None, None,
     f'Спустить  гидроманиторную насадку {"".join([f" + НКТ60мм {round(CreatePZ.current_bottom -CreatePZ.head_column_additional, 0)}" if CreatePZ.column_additional == True else ""])} '
     f'на НКТ{CreatePZ.nkt_diam}мм до глубины нижней точки до {bottom_point}'
     f' с замером, шаблонированием шаблоном.',
     None, None, None, None, None, None, None,
     'мастер КРС', descentNKT_norm(bottom_point,1)],
     [None, None,
      f'Провести ОПЗ пласта {plast} силами СК Крезол по технологии ГОНС в инт. {acid_points} с закачкой HCL '
      f'{acid_pr}% в объеме по {acid_countOfpoint}м3/точке (общий объем {acid_V}м3)  в присутствии представителя '
      f'сектора супервайзерского контроля за текущим и капитальным ремонтом скважин (ГОНС произвести снизу-вверх).',
      None, None, None, None, None, None, None,
      'мастер КРС', 8],
     [None, None,
      f'По согласованию с заказчиком  допустить компоновку до глубины {CreatePZ.current_bottom}м, промыть скважину '
      f'прямой промывкой через желобную ёмкость водой у= {CreatePZ.fluid_work} в присутствии представителя заказчика в '
      f'объеме {round(krs.well_volume(self, CreatePZ.current_bottom), 1)}м3. Промывку производить в емкость для дальнейшей утилизации на НШУ с целью недопущения попадания кислоты в систему сбора.',
      None, None, None, None, None, None, None,
      'мастер КРС', 1.2],
     [None, None,
      f'Поднять гидроманиторную насадку на НКТ{CreatePZ.nkt_diam} c глубины {CreatePZ.current_bottom}м с доливом скважины в '
      f'объеме {round(CreatePZ.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
      None, None, None, None, None, None, None,
      'мастер КРС',
      liftingNKT_norm(CreatePZ.current_bottom, 1)]]
    return gons_list