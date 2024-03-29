from PyQt5.QtWidgets import QInputDialog, QMessageBox

import krs
import well_data
from work_py.acids_work import acid_work_list
from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm
from work_py.opressovka import TabPage_SO
from work_py.swabbing import Swab_Window, TabPage_SO_swab

def acid_work(self):


    swabbing_true_quest = QMessageBox.question(self, 'Свабирование на данной компоновке',
                                               'Нужно ли Свабировать на данной компоновке?')

    if swabbing_true_quest == QMessageBox.StandardButton.Yes:
        swabbing_true_quest = True
    else:
        swabbing_true_quest = False



    paker_depth_bottom, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                          'Введите глубину посадки нижнего пакера {well_data.work_perforations["интервал"]}', int(well_data.perforation_sole + 10), 0,
                                          int(well_data.current_bottom))
    paker_depth_top, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                 'Введите глубину посадки вверхнего пакера {well_data.work_perforations["интервал"]}', int(well_data.perforation_sole- 10),
                                                 0, paker_depth_bottom)
    difference_paker =  paker_depth_bottom - paker_depth_top
    paker_khost_top = int(well_data.perforation_sole - paker_depth_bottom)

    paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
                                          f'Введите длину хвостовика при посадке пакера нижнего пакера на {paker_depth_bottom} и текущем забое {well_data.current_bottom}',
                                          paker_khost_top, 0, 4000)
    paker_diametr = TabPage_SO.paker_diametr_select(self, paker_depth_bottom)
    if well_data.column_additional is False or (well_data.column_additional is True and paker_depth_bottom < well_data.head_column_additional._value):
        paker_select = f'заглушку + сбивной с ввертышем + НКТ{well_data.nkt_diam}мм {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                       f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр НКТ {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr} + НКТ{well_data.nkt_diam}мм 20м +реперный патрубок на НКТ{well_data.nkt_diam}мм'
        dict_nkt = {73: paker_depth_bottom}
    elif well_data.column_additional == True and well_data.column_additional_diametr._value < 110 and paker_depth_bottom > well_data.head_column_additional._value:
        paker_select = f'заглушку + сбивной с ввертышем + НКТ{60}мм {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr }мм (либо аналог) ' \
                       f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр НКТ{60} {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr } + НКТ{60}мм 20м +реперный патрубок на НКТ{60} {well_data.head_column_additional-paker_depth_bottom}'
        dict_nkt = {73: well_data.head_column_additional-10, 60: int(paker_depth_bottom - well_data.head_column_additional._value)}
    elif well_data.column_additional == True and well_data.column_additional_diametr._value > 110 and paker_depth_bottom > well_data.head_column_additional._value:
        paker_select = f'заглушку + сбивной с ввертышем + НКТ73 со снятыми фасками {paker_khost}м  + пакер ПРО-ЯМО-{paker_diametr }мм (либо аналог) ' \
                       f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр НКТ73 со снятыми фасками {difference_paker}м ' \
                       f'+ пакер ПУ - {paker_diametr } + НКТ73 со снятыми фасками 20м +реперный патрубок на НКТ73 со снятыми фасками {well_data.head_column_additional._value - paker_depth_bottom}'

        dict_nkt = {73: paker_depth_bottom}
    elif well_data.nkt_diam == 60:
        dict_nkt = {60: paker_depth_bottom}



    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины нижнего пакера  до {paker_depth_bottom}, вверхнего пакера на {paker_depth_top}'
         f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. /n {("Произвести пробную посадку на глубине 50м" if well_data.column_additional == False else "")} '
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
         f'Опрессовать эксплуатационную колонну в интервале {paker_depth_top}-0м на Р={well_data.max_admissible_pressure._value}атм'
         f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
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
    for row in acid_work_list(self, paker_depth_bottom, paker_khost, dict_nkt, well_data.paker_layout):
        paker_list.append(row)
        n += 1

    reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, well_data.nkt_diam, paker_depth_bottom)

    paker_list.extend(acid_true_quest_list)

    if swabbing_true_quest:

        swabbing_with_paker = TabPage_SO_swab.swabbing_with_paker(self, difference_paker, 2)[1:]
        for row in swabbing_with_paker:
            paker_list.append(row)
    else:

        paker_list.append([None, None,
                                 f'Поднять {paker_select} на НКТ{well_data.nkt_diam}мм c глубины {paker_depth_bottom}м с доливом скважины в '
                                 f'объеме {round(paker_depth_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС', liftingNKT_norm(paker_depth_bottom, 1.2)])
    return paker_list

acid_true_quest_list = []
def reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom):
    
    acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                           'Нужно ли планировать кислоту на следующий объет?')

    if acid_true_quest == QMessageBox.StandardButton.Yes:

        paker_depth_bottom, ok = QInputDialog.getInt(None, 'опрессовка ЭК',
                                                     f'Введите глубину нижнего пакера посадки пакера ',
                                                     int(well_data.perforation_roof - 20), 0,
                                                     5000)
        acid_true_quest_list.append([None, None, f'Приподнять пакера на глубине {paker_depth_bottom}/{paker_depth_bottom-difference_paker}м', None, None, None, None, None, None, None,
                           'мастер КРС', 0.83+0.05])

        for row in acid_work_list(self, paker_depth_bottom, paker_khost, dict_nkt, well_data.paker_layout):
            acid_true_quest_list.append(row)

        # print(reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom))
        reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom)

    else:
        return acid_true_quest_list


def acidGons(self):
    
    plast, ok = QInputDialog.getItem(self, 'выбор пласта для ОПЗ ', 'выберете пласта дл перфорации',
                                     well_data.plast_work, 0, False)
    acid_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка']
    acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты:', acid_list, 0, False)
    if ok and acid_list:
        self.le.setText(acid)
    acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
    acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
    acid_countOfpoint, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите объем кислоты на точку', 5, 1, 24)
    acid_points, ok = QInputDialog.getText(self, 'точки ГОНС', 'Введите точки ГОНС ')
    bottom_point = max(list(map(int, acid_points.replace('м', '').replace(',', '').split())))
    gons_list = [[f'Спуск гидроманиторную насадку до глубины нижней точки до {bottom_point}', None,
     f'Спустить  гидроманиторную насадку {"".join([f" + НКТ60мм {round(well_data.current_bottom -well_data.head_column_additional._value, 0)}" if well_data.column_additional == True else ""])} '
     f'на НКТ{well_data.nkt_diam}мм до глубины нижней точки до {bottom_point}'
     f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
     None, None, None, None, None, None, None,
     'мастер КРС', descentNKT_norm(bottom_point,1)],
     [f' ГОНС пласта {plast} (общий объем {acid_V}м3) в инт. {acid_points}', None,
      f'Провести ОПЗ пласта {plast} силами СК Крезол по технологии ГОНС в инт. {acid_points} с закачкой HCL '
      f'{acid_pr}% в объеме по {acid_countOfpoint}м3/точке (общий объем {acid_V}м3)  в присутствии представителя '
      f'сектора супервайзерского контроля за текущим и капитальным ремонтом скважин (ГОНС произвести снизу-вверх).',
      None, None, None, None, None, None, None,
      'мастер КРС', 8],
     [None, None,
      f'По согласованию с заказчиком  допустить компоновку до глубины {well_data.current_bottom}м, промыть скважину '
      f'прямой промывкой через желобную ёмкость водой у= {well_data.fluid_work} в присутствии представителя заказчика в '
      f'объеме {round(krs.well_volume(self, well_data.current_bottom), 1)}м3. Промывку производить в емкость для дальнейшей утилизации на НШУ с целью недопущения попадания кислоты в систему сбора.',
      None, None, None, None, None, None, None,
      'мастер КРС', 1.2],
     [None, None,
      f'Поднять гидроманиторную насадку на НКТ{well_data.nkt_diam}мм c глубины {well_data.current_bottom}м с доливом скважины в '
      f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
      None, None, None, None, None, None, None,
      'мастер КРС',
      liftingNKT_norm(well_data.current_bottom, 1)]]
    return gons_list